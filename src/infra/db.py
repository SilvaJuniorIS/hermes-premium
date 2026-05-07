import sqlite3
from pathlib import Path

DB_PATH = Path("data/hermes.sqlite3")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_time TEXT,
        end_time TEXT,
        status TEXT,
        stats TEXT,
        perfil TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()