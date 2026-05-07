import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from src.config import DB_PATH


# ============================================================
# UTIL
# ============================================================
def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def parse_money(value: Any) -> float:
    if value is None:
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    try:
        text = str(value).replace("R$", "").replace(".", "").replace(",", ".")
        return float(text)
    except:
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


# ============================================================
# INIT DATABASE (BLINDADO)
# ============================================================
def init_db(db_path=DB_PATH):
    with connect(db_path) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS licitacoes (
            pncp_id TEXT PRIMARY KEY,
            objeto TEXT,
            valor_estimado_num REAL,
            estado TEXT,
            municipio TEXT,
            data_abertura TEXT,
            last_seen_at TEXT
        );

        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pncp_id TEXT,
            keyword TEXT,
            estado TEXT,
            valor_estimado_num REAL,
            collected_at TEXT
        );

        CREATE TABLE IF NOT EXISTS api_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT,
            end_time TEXT,
            status TEXT,
            stats TEXT,
            notes TEXT
        );

        CREATE TABLE IF NOT EXISTS api_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            message TEXT
        );
        """)


# ============================================================
# RUN CONTROL
# ============================================================
def start_run(perfil=None, db_path=DB_PATH):
    with connect(db_path) as conn:
        cur = conn.execute(
            """
            INSERT INTO api_runs(start_time, status, perfil)
            VALUES (?, ?, ?)
            """,
            (now_iso(), "running", perfil),
        )
        return cur.lastrowid

def finish_run(run_id, stats, status="finished", notes="", db_path=DB_PATH):
    try:
        with connect(db_path) as conn:
            conn.execute("""
                UPDATE api_runs
                SET end_time = ?,
                    status = ?,
                    stats = ?,
                    notes = ?
                WHERE id = ?
            """, (
                now_iso(),
                status,
                json.dumps(stats, ensure_ascii=False),
                notes,
                run_id
            ))
    except Exception as e:
        print(f"[ERRO finish_run]: {e}")


# ============================================================
# LOG EVENT (AGORA PERSISTENTE)
# ============================================================
def log_event(run_id, event_type, message, db_path=DB_PATH, **kwargs):
    try:
        with connect(db_path) as conn:
            conn.execute("""
                INSERT INTO api_events (created_at, message)
                VALUES (?, ?)
            """, (
                now_iso(),
                f"[run={run_id}] {event_type}: {message} {kwargs}"
            ))
    except Exception:
        pass


# ============================================================
# UPSERT
# ============================================================
def upsert_licitacoes(licitacoes: Iterable[dict], db_path=DB_PATH):
    saved = 0
    now = now_iso()

    with connect(db_path) as conn:
        for lic in licitacoes:
            pncp_id = str(lic.get("pncp_id"))

            valor = parse_money(lic.get("valor_estimado_num"))

            conn.execute("""
                INSERT OR REPLACE INTO licitacoes (
                    pncp_id, objeto, valor_estimado_num,
                    estado, municipio, data_abertura, last_seen_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                pncp_id,
                str(lic.get("objeto")),
                valor,
                str(lic.get("estado")),
                str(lic.get("municipio")),
                str(lic.get("data_abertura")),
                now
            ))

            conn.execute("""
                INSERT INTO price_history (
                    pncp_id, keyword, estado, valor_estimado_num, collected_at
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                pncp_id,
                str(lic.get("keyword")),
                str(lic.get("estado")),
                valor,
                now
            ))

            saved += 1

    return saved


# ============================================================
# CONSULTAS
# ============================================================
def load_recent_licitacoes(limit=1000, db_path=DB_PATH):
    with connect(db_path) as conn:
        rows = conn.execute("""
            SELECT * FROM licitacoes
            ORDER BY last_seen_at DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return [dict(r) for r in rows]


def load_recent_api_runs(db_path=DB_PATH):
    with connect(db_path) as conn:
        rows = conn.execute("""
            SELECT * FROM api_runs
            ORDER BY id DESC
            LIMIT 50
        """).fetchall()

    return [dict(r) for r in rows]


# ============================================================
# RANKING
# ============================================================
def get_price_reference(keyword, estado, db_path=DB_PATH):
    if not keyword:
        return {"media": None}

    with connect(db_path) as conn:
        rows = conn.execute("""
            SELECT valor_estimado_num
            FROM price_history
            WHERE keyword = ?
              AND estado = ?
              AND valor_estimado_num > 0
        """, (keyword, estado)).fetchall()

    values = [r["valor_estimado_num"] for r in rows]

    if not values:
        return {"media": None}

    return {
        "media": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
        "amostras": len(values)
    }


# ============================================================
# SCHEMA SAFETY (ANTI-CRASH)
# ============================================================
def ensure_schema(cursor):
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS api_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT,
        end_time TEXT,
        status TEXT,
        stats TEXT,
        notes TEXT
    );
    """)

# ============================================================
# MIGRAÇÃO FORÇADA
# ============================================================

def ensure_schema(db_path=DB_PATH):
    with connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS api_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        );
        """)

        cols = [r[1] for r in cursor.execute("PRAGMA table_info(api_runs)").fetchall()]

        def add(col, ddl):
            if col not in cols:
                print(f"[MIGRAÇÃO] criando coluna {col}")
                cursor.execute(ddl)

        add("start_time", "ALTER TABLE api_runs ADD COLUMN start_time TEXT")
        add("end_time", "ALTER TABLE api_runs ADD COLUMN end_time TEXT")
        add("status", "ALTER TABLE api_runs ADD COLUMN status TEXT")
        add("stats", "ALTER TABLE api_runs ADD COLUMN stats TEXT")
        add("notes", "ALTER TABLE api_runs ADD COLUMN notes TEXT")
        add("perfil", "ALTER TABLE api_runs ADD COLUMN perfil TEXT")

        conn.commit()

        def detectar_oportunidade(lic, referencia):
            valor = lic.get("valor_estimado_num", 0)
            media = referencia.get("media")

            if not media or media == 0:
                return {"oportunidade": "desconhecida", "delta": 0}

            delta = (valor - media) / media

            if delta > 0.5:
                nivel = "🔥 MUITO ACIMA (OURO)"
            elif delta > 0.2:
                nivel = "🟡 ACIMA"
            elif delta < -0.2:
                nivel = "🔵 ABAIXO"
            else:
                nivel = "⚖️ NORMAL"

            return {
                "oportunidade": nivel,
                "delta": round(delta, 2)
        }
    
        def ensure_schema(cursor):
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_time TEXT,
                end_time TEXT,
                status TEXT,
                stats TEXT,
                notes TEXT
            )
            """)