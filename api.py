from __future__ import annotations

import json
import os
import secrets
import threading
import time
from base64 import urlsafe_b64decode, urlsafe_b64encode
from datetime import datetime
from hashlib import pbkdf2_hmac
from hmac import compare_digest
from pathlib import Path
from typing import Any

from fastapi import Cookie, Depends, FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.hermes_db import (
    ensure_admin_user,
    get_user_by_id,
    get_user_by_username,
    init_db,
    load_licitacao_detail,
    load_recent_api_runs,
    load_recent_licitacoes,
    mark_user_login,
)
from src.main import DEFAULT_CONFIG, run_pipeline


app = FastAPI(title="Hermes Premium")
PERFIS_PATH = Path("config/perfis_negocio.json")
SCHEDULE_PATH = Path("config/agendamento.json")
SESSION_COOKIE = "hermes_session"
SESSION_TOKENS: dict[str, int] = {}
SCHEDULER_LOCK = threading.Lock()
SCHEDULER_STARTED = False

Path("docs/assets").mkdir(parents=True, exist_ok=True)
app.mount("/assets", StaticFiles(directory="docs/assets"), name="assets")


class RunRequest(BaseModel):
    perfil: str = "limpeza_higiene"
    config: dict[str, Any] | None = None


class PerfilRequest(BaseModel):
    id: str
    nome_exibicao: str
    descricao: str = ""
    keywords: list[str] = Field(default_factory=list)
    keywords_fortes: list[str] = Field(default_factory=list)
    termos_positivos: list[str] = Field(default_factory=list)
    termos_negativos: list[str] = Field(default_factory=list)
    valor_minimo_interesse: float = 0
    valor_atrativo: float = 50000
    valor_muito_atrativo: float = 200000
    score_relevancia_media: float = 50
    score_relevancia_alta: float = 75


class ScheduleRequest(BaseModel):
    enabled: bool = False
    perfil: str = "limpeza_higiene"
    time: str = "08:00"
    config: dict[str, Any] | None = None


def _hash_password(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000)
    return (
        urlsafe_b64encode(salt).decode("ascii")
        + "$"
        + urlsafe_b64encode(digest).decode("ascii")
    )


def _verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_text, digest_text = stored_hash.split("$", 1)
        salt = urlsafe_b64decode(salt_text.encode("ascii"))
        expected = urlsafe_b64decode(digest_text.encode("ascii"))
    except (ValueError, TypeError):
        return False

    actual = pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120000)
    return compare_digest(actual, expected)


def _login_page(error: str = "") -> str:
    error_html = f'<div class="error">{error}</div>' if error else ""
    return f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login - Hermes Premium</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            min-height: 100vh;
            display: grid;
            place-items: center;
            background: #101418;
            color: #eef3f7;
            font-family: Arial, Helvetica, sans-serif;
        }}
        form {{
            width: min(420px, calc(100vw - 32px));
            border: 1px solid #2c343c;
            border-radius: 8px;
            background: #171d22;
            padding: 24px;
        }}
        h1 {{
            margin: 0 0 18px;
            font-size: 24px;
        }}
        label {{
            display: grid;
            gap: 6px;
            margin-bottom: 14px;
            color: #9fb0bf;
            font-size: 13px;
        }}
        input, button {{
            height: 40px;
            border: 1px solid #2c343c;
            border-radius: 6px;
            background: #101418;
            color: #eef3f7;
            padding: 0 12px;
            font-size: 15px;
        }}
        button {{
            width: 100%;
            border-color: #24785d;
            background: #17694f;
            cursor: pointer;
            font-weight: 700;
        }}
        .error {{
            margin-bottom: 14px;
            border: 1px solid #8f3939;
            border-radius: 6px;
            background: rgba(249, 115, 115, 0.12);
            color: #f97373;
            padding: 10px;
            font-size: 14px;
        }}
        p {{
            margin: 14px 0 0;
            color: #9fb0bf;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <form method="post" action="/login">
        <h1>Hermes Premium</h1>
        {error_html}
        <label>
            Usuario
            <input name="username" autocomplete="username" required autofocus>
        </label>
        <label>
            Senha
            <input name="password" type="password" autocomplete="current-password" required>
        </label>
        <button type="submit">Entrar</button>
        <p>Usuario inicial: admin. Senha inicial: admin123.</p>
    </form>
</body>
</html>
"""


def _current_user(hermes_session: str | None = Cookie(default=None)) -> dict[str, Any]:
    if not hermes_session:
        raise HTTPException(status_code=401, detail="Nao autenticado")

    user_id = SESSION_TOKENS.get(hermes_session)
    if not user_id:
        raise HTTPException(status_code=401, detail="Sessao invalida")

    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario inativo ou inexistente")

    return user


def _load_perfis() -> dict[str, Any]:
    if not PERFIS_PATH.exists():
        return {}
    try:
        return json.loads(PERFIS_PATH.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao ler perfis: {exc}") from exc


def _save_perfis(perfis: dict[str, Any]) -> None:
    PERFIS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PERFIS_PATH.write_text(
        json.dumps(perfis, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )


def _load_schedule() -> dict[str, Any]:
    default = {
        "enabled": False,
        "perfil": "limpeza_higiene",
        "time": "08:00",
        "config": {},
        "last_run_date": "",
        "last_run_status": "",
    }
    if not SCHEDULE_PATH.exists():
        return default
    try:
        data = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return default

    return {**default, **data}


def _save_schedule(data: dict[str, Any]) -> None:
    SCHEDULE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEDULE_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )


def _valid_schedule_time(value: str) -> str:
    try:
        datetime.strptime(value, "%H:%M")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Horario deve usar HH:MM") from exc
    return value


def _scheduler_loop() -> None:
    while True:
        try:
            schedule = _load_schedule()
            now = datetime.now()
            today = now.date().isoformat()
            if (
                schedule.get("enabled")
                and schedule.get("time") == now.strftime("%H:%M")
                and schedule.get("last_run_date") != today
            ):
                with SCHEDULER_LOCK:
                    schedule = _load_schedule()
                    if schedule.get("last_run_date") == today:
                        time.sleep(30)
                        continue

                    perfil = schedule.get("perfil") or "limpeza_higiene"
                    config = {**DEFAULT_CONFIG, **(schedule.get("config") or {})}
                    try:
                        result = run_pipeline(perfil, config)
                        schedule["last_run_status"] = (
                            f"finished: {result['stats'].get('salvas', 0)} registros"
                        )
                    except Exception as exc:  # pragma: no cover - defensive background loop
                        schedule["last_run_status"] = f"error: {exc}"
                    schedule["last_run_date"] = today
                    _save_schedule(schedule)
            time.sleep(30)
        except Exception:
            time.sleep(60)


def _start_scheduler_once() -> None:
    global SCHEDULER_STARTED
    if SCHEDULER_STARTED:
        return
    thread = threading.Thread(target=_scheduler_loop, daemon=True)
    thread.start()
    SCHEDULER_STARTED = True


def _perfil_payload(req: PerfilRequest) -> dict[str, Any]:
    return {
        "nome_exibicao": req.nome_exibicao,
        "descricao": req.descricao,
        "keywords": req.keywords,
        "keywords_fortes": req.keywords_fortes,
        "termos_positivos": req.termos_positivos,
        "termos_negativos": req.termos_negativos,
        "valor_minimo_interesse": req.valor_minimo_interesse,
        "valor_atrativo": req.valor_atrativo,
        "valor_muito_atrativo": req.valor_muito_atrativo,
        "score_relevancia_media": req.score_relevancia_media,
        "score_relevancia_alta": req.score_relevancia_alta,
    }


@app.on_event("startup")
def startup() -> None:
    init_db()
    ensure_admin_user(_hash_password)
    _start_scheduler_once()


@app.get("/", response_class=HTMLResponse)
def dashboard(hermes_session: str | None = Cookie(default=None)):
    user_id = SESSION_TOKENS.get(hermes_session or "")
    if not user_id or not get_user_by_id(user_id):
        return RedirectResponse("/login", status_code=303)

    dashboard_path = Path("dashboard.html")
    return HTMLResponse(dashboard_path.read_text(encoding="utf-8"))


@app.get("/login", response_class=HTMLResponse)
def login_form() -> str:
    init_db()
    ensure_admin_user(_hash_password)
    return _login_page()


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)) -> RedirectResponse:
    init_db()
    ensure_admin_user(_hash_password)
    user = get_user_by_username(username.strip())
    if not user or not _verify_password(password, user["password_hash"]):
        return HTMLResponse(_login_page("Usuario ou senha invalidos"), status_code=401)

    token = secrets.token_urlsafe(32)
    SESSION_TOKENS[token] = int(user["id"])
    mark_user_login(int(user["id"]))

    response = RedirectResponse("/", status_code=303)
    response.set_cookie(
        SESSION_COOKIE,
        token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 8,
    )
    return response


@app.post("/logout")
def logout(hermes_session: str | None = Cookie(default=None)) -> RedirectResponse:
    if hermes_session:
        SESSION_TOKENS.pop(hermes_session, None)

    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response


@app.post("/run")
def run(req: RunRequest, _: dict[str, Any] = Depends(_current_user)) -> dict[str, Any]:
    config = {**DEFAULT_CONFIG, **(req.config or {})}
    result = run_pipeline(req.perfil, config)
    return {
        "status": result["status"],
        "run_id": result["run_id"],
        "stats": result["stats"],
    }


@app.get("/licitacoes")
def listar(
    limit: int = 100,
    perfil: str | None = None,
    _: dict[str, Any] = Depends(_current_user),
) -> list[dict[str, Any]]:
    return load_recent_licitacoes(limit=limit, perfil=perfil)


@app.get("/licitacao")
def detalhe_licitacao(
    pncp_id: str,
    _: dict[str, Any] = Depends(_current_user),
) -> dict[str, Any]:
    detail = load_licitacao_detail(pncp_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Licitacao nao encontrada")
    return detail


@app.get("/runs")
def runs(_: dict[str, Any] = Depends(_current_user)) -> list[dict[str, Any]]:
    return load_recent_api_runs()


@app.get("/schedule")
def get_schedule(_: dict[str, Any] = Depends(_current_user)) -> dict[str, Any]:
    return _load_schedule()


@app.put("/schedule")
def update_schedule(
    req: ScheduleRequest,
    _: dict[str, Any] = Depends(_current_user),
) -> dict[str, Any]:
    data = _load_schedule()
    data.update(
        {
            "enabled": req.enabled,
            "perfil": req.perfil,
            "time": _valid_schedule_time(req.time),
            "config": req.config or {},
        }
    )
    _save_schedule(data)
    return data


@app.get("/health")
def health() -> dict[str, str]:
    init_db()
    return {"status": "ok"}


@app.get("/perfis")
def listar_perfis(_: dict[str, Any] = Depends(_current_user)) -> dict[str, Any]:
    return _load_perfis()


@app.post("/perfis")
def criar_perfil(
    req: PerfilRequest,
    _: dict[str, Any] = Depends(_current_user),
) -> dict[str, Any]:
    perfil_id = req.id.strip().lower().replace(" ", "_")
    if not perfil_id:
        raise HTTPException(status_code=400, detail="ID do perfil e obrigatorio")

    perfis = _load_perfis()
    if perfil_id in perfis:
        raise HTTPException(status_code=409, detail="Perfil ja existe")

    perfis[perfil_id] = _perfil_payload(req)
    _save_perfis(perfis)
    return {"id": perfil_id, "perfil": perfis[perfil_id]}


@app.put("/perfis/{perfil_id}")
def atualizar_perfil(
    perfil_id: str,
    req: PerfilRequest,
    _: dict[str, Any] = Depends(_current_user),
) -> dict[str, Any]:
    perfis = _load_perfis()
    perfil_id = perfil_id.strip().lower()
    if perfil_id not in perfis:
        raise HTTPException(status_code=404, detail="Perfil nao encontrado")

    novo_id = req.id.strip().lower().replace(" ", "_")
    if not novo_id:
        raise HTTPException(status_code=400, detail="ID do perfil e obrigatorio")
    if novo_id != perfil_id and novo_id in perfis:
        raise HTTPException(status_code=409, detail="Novo ID ja existe")

    payload = _perfil_payload(req)
    if novo_id != perfil_id:
        del perfis[perfil_id]
    perfis[novo_id] = payload
    _save_perfis(perfis)
    return {"id": novo_id, "perfil": payload}


@app.delete("/perfis/{perfil_id}")
def excluir_perfil(
    perfil_id: str,
    _: dict[str, Any] = Depends(_current_user),
) -> dict[str, str]:
    perfis = _load_perfis()
    perfil_id = perfil_id.strip().lower()
    if perfil_id not in perfis:
        raise HTTPException(status_code=404, detail="Perfil nao encontrado")

    del perfis[perfil_id]
    _save_perfis(perfis)
    return {"status": "deleted", "id": perfil_id}
