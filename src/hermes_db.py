import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any

from src.config import DB_PATH


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def parse_money(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        return 0.0

    try:
        text = (
            text.replace("R$", "")
            .replace(" ", "")
            .replace(".", "")
            .replace(",", ".")
        )
        return float(text)
    except (TypeError, ValueError):
        return 0.0


@contextmanager
def connect(db_path: Path | str = DB_PATH):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}


def _add_column(conn: sqlite3.Connection, table: str, column: str, ddl: str) -> None:
    if column not in _columns(conn, table):
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}")


def ensure_schema(db_path: Path | str = DB_PATH) -> None:
    with connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT NOT NULL,
                end_time TEXT,
                status TEXT NOT NULL,
                stats TEXT,
                perfil TEXT,
                notes TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                nome TEXT,
                role TEXT NOT NULL DEFAULT 'admin',
                ativo INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                last_login_at TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                run_id INTEGER,
                event_type TEXT,
                message TEXT NOT NULL,
                meta TEXT
            )
        """)
        _add_column(conn, "api_events", "run_id", "INTEGER")
        _add_column(conn, "api_events", "event_type", "TEXT")
        _add_column(conn, "api_events", "meta", "TEXT")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS licitacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                perfil TEXT,
                pncp_id TEXT,
                objeto TEXT,
                valor_estimado_num REAL DEFAULT 0,
                estado TEXT,
                municipio TEXT,
                orgao TEXT,
                keyword TEXT,
                data_abertura TEXT,
                score REAL DEFAULT 0,
                classificacao TEXT,
                oportunidade TEXT,
                delta_preco REAL DEFAULT 0,
                score_motivos TEXT,
                link TEXT,
                source TEXT,
                raw_json TEXT,
                first_seen_at TEXT,
                last_seen_at TEXT
            )
        """)

        for column, ddl in {
            "id": "INTEGER",
            "perfil": "TEXT",
            "pncp_id": "TEXT",
            "objeto": "TEXT",
            "valor_estimado_num": "REAL DEFAULT 0",
            "estado": "TEXT",
            "municipio": "TEXT",
            "orgao": "TEXT",
            "keyword": "TEXT",
            "data_abertura": "TEXT",
            "score": "REAL DEFAULT 0",
            "classificacao": "TEXT",
            "oportunidade": "TEXT",
            "delta_preco": "REAL DEFAULT 0",
            "score_motivos": "TEXT",
            "link": "TEXT",
            "source": "TEXT",
            "raw_json": "TEXT",
            "first_seen_at": "TEXT",
            "last_seen_at": "TEXT",
        }.items():
            if column != "id":
                _add_column(conn, "licitacoes", column, ddl)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pncp_id TEXT,
                keyword TEXT,
                estado TEXT,
                valor_estimado_num REAL,
                collected_at TEXT NOT NULL
            )
        """)

        conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_licitacoes_pncp_id "
            "ON licitacoes(pncp_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_licitacoes_last_seen "
            "ON licitacoes(last_seen_at)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_licitacoes_score "
            "ON licitacoes(score)"
        )
        conn.execute(
            """
            DELETE FROM licitacoes
            WHERE pncp_id IS NULL
               OR TRIM(COALESCE(pncp_id, '')) = ''
               OR LOWER(TRIM(COALESCE(pncp_id, ''))) = 'none'
               OR objeto IS NULL
               OR TRIM(COALESCE(objeto, '')) = ''
               OR LOWER(TRIM(COALESCE(objeto, ''))) = 'none'
            """
        )


def get_user_by_username(
    username: str,
    db_path: Path | str = DB_PATH,
) -> dict[str, Any] | None:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT *
            FROM usuarios
            WHERE username = ?
              AND ativo = 1
            """,
            (username,),
        ).fetchone()

    return dict(row) if row else None


def get_user_by_id(
    user_id: int,
    db_path: Path | str = DB_PATH,
) -> dict[str, Any] | None:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT *
            FROM usuarios
            WHERE id = ?
              AND ativo = 1
            """,
            (user_id,),
        ).fetchone()

    return dict(row) if row else None


def create_user(
    username: str,
    password_hash: str,
    nome: str | None = None,
    role: str = "admin",
    db_path: Path | str = DB_PATH,
) -> int:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO usuarios (
                username, password_hash, nome, role, ativo, created_at
            ) VALUES (?, ?, ?, ?, 1, ?)
            """,
            (username, password_hash, nome or username, role, now_iso()),
        )
        return int(cur.lastrowid)


def update_user_password(
    username: str,
    password_hash: str,
    db_path: Path | str = DB_PATH,
) -> None:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        conn.execute(
            "UPDATE usuarios SET password_hash = ?, ativo = 1 WHERE username = ?",
            (password_hash, username),
        )


def mark_user_login(
    user_id: int,
    db_path: Path | str = DB_PATH,
) -> None:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        conn.execute(
            "UPDATE usuarios SET last_login_at = ? WHERE id = ?",
            (now_iso(), user_id),
        )


def ensure_admin_user(
    password_hash_factory,
    db_path: Path | str = DB_PATH,
) -> None:
    ensure_schema(db_path)
    username = os.getenv("HERMES_ADMIN_USER", "admin")
    password = os.getenv("HERMES_ADMIN_PASSWORD", "admin123")
    existing_user = get_user_by_username(username, db_path)
    if existing_user:
        if os.getenv("HERMES_RESET_ADMIN_PASSWORD") == "1":
            update_user_password(username, password_hash_factory(password), db_path)
        return

    create_user(
        username=username,
        password_hash=password_hash_factory(password),
        nome="Administrador",
        role="admin",
        db_path=db_path,
    )


def init_db(db_path: Path | str = DB_PATH) -> None:
    ensure_schema(db_path)


def start_run(perfil: str | None = None, db_path: Path | str = DB_PATH) -> int:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO api_runs(start_time, status, perfil)
            VALUES (?, ?, ?)
            """,
            (now_iso(), "running", perfil),
        )
        return int(cur.lastrowid)


def finish_run(
    run_id: int,
    stats: dict[str, Any],
    status: str = "finished",
    notes: str = "",
    db_path: Path | str = DB_PATH,
) -> None:
    with connect(db_path) as conn:
        conn.execute(
            """
            UPDATE api_runs
            SET end_time = ?,
                status = ?,
                stats = ?,
                notes = ?
            WHERE id = ?
            """,
            (now_iso(), status, json.dumps(stats, ensure_ascii=False), notes, run_id),
        )


def log_event(
    run_id: int | None,
    event_type: str,
    message: str,
    db_path: Path | str = DB_PATH,
    **kwargs: Any,
) -> None:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO api_events (created_at, run_id, event_type, message, meta)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                now_iso(),
                run_id,
                event_type,
                message,
                json.dumps(kwargs, ensure_ascii=False) if kwargs else None,
            ),
        )


def upsert_licitacoes(
    licitacoes: list[dict[str, Any]],
    db_path: Path | str = DB_PATH,
) -> int:
    ensure_schema(db_path)
    saved = 0
    seen_at = now_iso()

    with connect(db_path) as conn:
        for lic in licitacoes:
            pncp_id = str(lic.get("pncp_id") or "").strip()
            if not pncp_id:
                continue

            valor = parse_money(lic.get("valor_estimado_num"))
            raw = lic.get("raw")

            conn.execute(
                """
                INSERT INTO licitacoes (
                    perfil, pncp_id, objeto, valor_estimado_num, estado, municipio,
                    orgao, keyword, data_abertura, score, classificacao,
                    oportunidade, delta_preco, score_motivos, link, source,
                    raw_json, first_seen_at, last_seen_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(pncp_id) DO UPDATE SET
                    perfil = excluded.perfil,
                    objeto = excluded.objeto,
                    valor_estimado_num = excluded.valor_estimado_num,
                    estado = excluded.estado,
                    municipio = excluded.municipio,
                    orgao = excluded.orgao,
                    keyword = excluded.keyword,
                    data_abertura = excluded.data_abertura,
                    score = excluded.score,
                    classificacao = excluded.classificacao,
                    oportunidade = excluded.oportunidade,
                    delta_preco = excluded.delta_preco,
                    score_motivos = excluded.score_motivos,
                    link = excluded.link,
                    source = excluded.source,
                    raw_json = excluded.raw_json,
                    last_seen_at = excluded.last_seen_at
                """,
                (
                    lic.get("perfil"),
                    pncp_id,
                    lic.get("objeto"),
                    valor,
                    lic.get("estado"),
                    lic.get("municipio"),
                    lic.get("orgao"),
                    lic.get("keyword"),
                    lic.get("data_abertura"),
                    lic.get("score", 0),
                    lic.get("classificacao"),
                    lic.get("oportunidade"),
                    lic.get("delta_preco", 0),
                    json.dumps(lic.get("score_motivos") or [], ensure_ascii=False),
                    lic.get("link"),
                    lic.get("source", "pncp"),
                    json.dumps(raw, ensure_ascii=False) if raw is not None else None,
                    seen_at,
                    seen_at,
                ),
            )

            if valor > 0:
                conn.execute(
                    """
                    INSERT INTO price_history (
                        pncp_id, keyword, estado, valor_estimado_num, collected_at
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    (pncp_id, lic.get("keyword"), lic.get("estado"), valor, seen_at),
                )

            saved += 1

    return saved


def load_recent_licitacoes(
    limit: int = 100,
    perfil: str | None = None,
    classificacao: str | None = None,
    estado: str | None = None,
    q: str | None = None,
    valor_min: float | None = None,
    valor_max: float | None = None,
    db_path: Path | str = DB_PATH,
) -> list[dict[str, Any]]:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        where_parts: list[str] = []
        params: list[Any] = []
        if perfil:
            where_parts.append("perfil = ?")
            params.append(perfil)
        if classificacao:
            where_parts.append("classificacao = ?")
            params.append(classificacao.upper())
        if estado:
            where_parts.append("estado = ?")
            params.append(estado.upper())
        if q:
            where_parts.append(
                "(LOWER(objeto) LIKE ? OR LOWER(orgao) LIKE ? OR LOWER(municipio) LIKE ? OR LOWER(keyword) LIKE ?)"
            )
            q_like = f"%{q.lower()}%"
            params.extend([q_like, q_like, q_like, q_like])
        if valor_min is not None:
            where_parts.append("valor_estimado_num >= ?")
            params.append(valor_min)
        if valor_max is not None:
            where_parts.append("valor_estimado_num <= ?")
            params.append(valor_max)
        where = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
        params.append(limit)
        rows = conn.execute(
            f"""
            SELECT
                perfil, pncp_id, objeto, valor_estimado_num, estado, municipio, orgao,
                keyword, data_abertura, score, classificacao, oportunidade,
                delta_preco, score_motivos, link, source, first_seen_at, last_seen_at
            FROM licitacoes
            {where}
            ORDER BY score DESC, valor_estimado_num DESC, last_seen_at DESC
            LIMIT ?
            """,
            params,
        ).fetchall()

    return [_format_licitacao_row(row) for row in rows]


def _format_licitacao_row(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    motivos = data.get("score_motivos")
    if isinstance(motivos, str) and motivos.strip():
        try:
            data["score_motivos"] = json.loads(motivos)
        except json.JSONDecodeError:
            data["score_motivos"] = [motivos]
    else:
        data["score_motivos"] = _fallback_score_motivos(data)
    return data


def _fallback_score_motivos(data: dict[str, Any]) -> list[str]:
    motivos: list[str] = []
    keyword = data.get("keyword")
    valor = parse_money(data.get("valor_estimado_num"))
    score = float(data.get("score") or 0)
    if keyword:
        motivos.append(f"Encontrou keyword principal: {keyword}")
    if valor > 0:
        motivos.append("Valor estimado considerado na pontuacao")
    if score >= 75:
        motivos.append("Score final acima do corte de alta prioridade")
    elif score >= 50:
        motivos.append("Score final acima do corte de media prioridade")
    else:
        motivos.append("Score final mantido para monitoramento")
    return motivos


def load_licitacao_detail(
    pncp_id: str,
    db_path: Path | str = DB_PATH,
) -> dict[str, Any] | None:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        row = conn.execute(
            """
            SELECT
                pncp_id, objeto, valor_estimado_num, estado, municipio, orgao,
                perfil, keyword, data_abertura, score, classificacao, oportunidade,
                delta_preco, score_motivos, link, source, raw_json,
                first_seen_at, last_seen_at
            FROM licitacoes
            WHERE pncp_id = ?
            """,
            (pncp_id,),
        ).fetchone()

    if not row:
        return None

    data = _format_licitacao_row(row)
    raw = data.get("raw_json")
    if isinstance(raw, str) and raw.strip():
        try:
            data["raw"] = json.loads(raw)
        except json.JSONDecodeError:
            data["raw"] = None
    else:
        data["raw"] = None
    data.pop("raw_json", None)
    return data


def load_recent_api_runs(db_path: Path | str = DB_PATH) -> list[dict[str, Any]]:
    ensure_schema(db_path)
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM api_runs
            ORDER BY id DESC
            LIMIT 50
            """
        ).fetchall()

    result: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        stats = item.get("stats")
        if isinstance(stats, str) and stats.strip():
            try:
                item["stats"] = json.loads(stats)
            except json.JSONDecodeError:
                item["stats"] = {"raw": stats}
        else:
            item["stats"] = {}
        result.append(item)
    return result


def get_price_reference(
    keyword: str | None,
    estado: str | None,
    db_path: Path | str = DB_PATH,
) -> dict[str, Any]:
    if not keyword or not estado:
        return {"media": None}

    ensure_schema(db_path)
    with connect(db_path) as conn:
        rows = conn.execute(
            """
            SELECT valor_estimado_num
            FROM price_history
            WHERE keyword = ?
              AND estado = ?
              AND valor_estimado_num > 0
            ORDER BY collected_at DESC
            LIMIT 200
            """,
            (keyword, estado),
        ).fetchall()

    values = [float(row["valor_estimado_num"]) for row in rows]
    if not values:
        return {"media": None}

    return {
        "media": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
        "amostras": len(values),
    }
