from src.infra.db import get_conn
from src.core.collector import run_collection
from src.infra.logger import log


def run_pipeline(perfil: str):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO api_runs (start_time, status, perfil)
        VALUES (datetime('now'), 'running', ?)
    """, (perfil,))

    run_id = cursor.lastrowid

    log(run_id, "info", "Iniciando coleta")

    try:
        data, stats = run_collection(perfil)

        log(run_id, "info", "Coleta finalizada", total=len(data))

        cursor.execute("""
            UPDATE api_runs
            SET end_time = datetime('now'),
                status = ?,
                stats = ?
            WHERE id = ?
        """, ("finished", str(stats), run_id))

        conn.commit()

        return data

    except Exception as e:
        log(run_id, "error", str(e))

        cursor.execute("""
            UPDATE api_runs
            SET status = 'error',
                end_time = datetime('now'),
                notes = ?
            WHERE id = ?
        """, (str(e), run_id))

        conn.commit()

        raise