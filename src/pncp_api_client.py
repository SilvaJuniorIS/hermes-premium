from __future__ import annotations

import random
import time
import os
from datetime import datetime, timedelta
from typing import Any

import requests

BASE_URL = "https://pncp.gov.br/api/consulta/v1"
DEFAULT_TIMEOUT = int(os.getenv("HERMES_TIMEOUT_SEGUNDOS", "25"))
PAGE_SIZE = 50


# ============================================================
# USER AGENTS ROTATIVOS
# ============================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/120.0.0.0 Safari/537.36",
]


class PNCPClient:
    def __init__(
        self,
        *,
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        min_delay: float = float(os.getenv("HERMES_MIN_DELAY", "1.5")),
        max_delay: float = float(os.getenv("HERMES_MAX_DELAY", "4.0")),
        max_retries: int = int(os.getenv("HERMES_MAX_RETRIES", "3")),
        circuit_breaker_limit: int = 20,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.max_retries = max_retries
        self.circuit_breaker_limit = circuit_breaker_limit
        self.consecutive_blocks = 0

        self.stats = {
            "total": 0,
            "sucesso": 0,
            "erro_400": 0,
            "erro_403": 0,
            "rate_limit": 0,
            "timeout": 0,
            "erro_conexao": 0,
            "outros": 0,
        }

        self.session = self._new_session()

    def _new_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
            "Referer": "https://pncp.gov.br/app/editais",
            "Origin": "https://pncp.gov.br",
        })
        return session

    def _sleep(self, attempt: int = 0) -> None:
        base = random.uniform(self.min_delay, self.max_delay)
        backoff = (2 ** attempt) + random.uniform(0.5, 1.5)
        time.sleep(base + backoff)

    def blocked(self) -> bool:
        return self.consecutive_blocks >= self.circuit_breaker_limit

    def _rotate_identity(self):
        self.session.close()
        self.session = self._new_session()

    # ============================================================
    # REQUEST BLINDADO
    # ============================================================
    def get_json(self, path: str, params: dict[str, Any]) -> tuple[int | None, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"

        for attempt in range(self.max_retries + 1):

            if self.blocked():
                print("⚠️ Circuit breaker ativado.")
                return None, None

            self.stats["total"] += 1
            self._sleep(attempt)

            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
            except (requests.exceptions.Timeout, TimeoutError):
                self.stats["timeout"] += 1
                self._rotate_identity()
                continue
            except (requests.exceptions.RequestException, OSError):
                self.stats["erro_conexao"] += 1
                self._rotate_identity()
                continue

            status = response.status_code

            # ✅ SUCESSO
            if status == 200:
                self.stats["sucesso"] += 1
                self.consecutive_blocks = 0
                try:
                    return status, response.json()
                except ValueError:
                    return status, None

            # ⚠️ ERROS CONTROLADOS
            if status == 400:
                self.stats["erro_400"] += 1
                self.consecutive_blocks += 1
                return status, None

            if status == 403:
                self.stats["erro_403"] += 1
                self.consecutive_blocks += 1
                print(f"⚠️ 403 detectado — rotacionando identidade")
                self._rotate_identity()
                time.sleep(random.uniform(5, 10))
                continue

            if status == 429:
                self.stats["rate_limit"] += 1
                self.consecutive_blocks += 1
                print("⏳ Rate limit — aguardando")
                time.sleep(random.uniform(10, 20))
                continue

            if 500 <= status <= 599:
                self.stats["outros"] += 1
                time.sleep(random.uniform(3, 6))
                continue

            self.stats["outros"] += 1
            return status, None

        return None, None


# ============================================================
# HELPERS
# ============================================================
def _fmt_date(dt: datetime) -> str:
    return dt.strftime("%Y%m%d")


def _as_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for k in ("data", "content", "items", "resultado"):
            if isinstance(payload.get(k), list):
                return payload[k]
    return []


# ============================================================
# FETCH PRINCIPAL (ULTRA ESTÁVEL)
# ============================================================
def fetch_licitacoes_from_pncp_api(
    *,
    keywords: list[str],
    states: list[str],
    max_total: int,
    days_forward: int = 60,
    max_pages_per_endpoint: int = 25,
    max_runtime_minutes: int = 20,
    run_id: int | None = None,
    event_logger=None,
    page_callback=None,
):

    client = PNCPClient()
    started_at = datetime.now()

    start = started_at
    end = start + timedelta(days=days_forward)

    found = {}
    endpoints = ["contratacoes/proposta", "contratacoes/publicacao"]

    def log(msg):
        if event_logger:
            try:
                event_logger(run_id, "api_error", msg)
            except Exception:
                pass

    for uf in states:
        for endpoint in endpoints:

            page = 1

            while page <= max_pages_per_endpoint:

                params = {
                    "dataInicial": _fmt_date(start),
                    "dataFinal": _fmt_date(end),
                    "uf": uf,
                    "pagina": page,
                    "tamanhoPagina": PAGE_SIZE,
                }

                status, payload = client.get_json(endpoint, params)

                # 🔴 PROTEÇÃO TOTAL
                if status is None:
                    log(f"Resposta None em {endpoint}")
                    break

                if status != 200:
                    log(f"{status} em {endpoint}")
                    break

                rows = _as_list(payload)

                if not rows:
                    break

                matches = []

                for item in rows:
                    texto = str(item).lower()

                    if any(k.lower() in texto for k in keywords):
                        pid = str(item.get("numeroControlePNCP") or item.get("id"))

                        if pid and pid not in found:
                            found[pid] = item
                            matches.append(item)

                print(f"[{uf}] {endpoint} pág {page}: {len(matches)} | total {len(found)}")

                if page_callback and matches:
                    try:
                        page_callback(matches)
                    except Exception:
                        pass

                if len(found) >= max_total:
                    break

                page += 1

    return list(found.values()), client.stats