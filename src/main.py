from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.coletor import build_config, coletar_licitacoes
from src.hermes_db import (
    finish_run,
    init_db,
    load_recent_licitacoes,
    log_event,
    start_run,
    upsert_licitacoes,
)


DEFAULT_CONFIG: dict[str, Any] = {
    "estados": ["SP", "RJ", "MG"],
    "dias_a_frente": 60,
    "max_paginas": 5,
    "tamanho_pagina": 50,
    "max_total": 300,
    "delay": 0.8,
}

COLETA_GERAL = "__coleta_geral__"
PERFIS_PATH = Path("config/perfis_negocio.json")


def _list_perfil_ids() -> list[str]:
    if not PERFIS_PATH.exists():
        return []
    try:
        data = json.loads(PERFIS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    return sorted(data.keys())


def run_pipeline_coleta_geral(
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Executa `run_pipeline` para cada perfil cadastrado, em sequencia."""
    init_db()
    perfil_ids = _list_perfil_ids()
    if not perfil_ids:
        raise ValueError("Nenhum perfil cadastrado em config/perfis_negocio.json")

    merged = {**DEFAULT_CONFIG, **(config or {})}
    detalhes: list[dict[str, Any]] = []
    erros: list[dict[str, Any]] = []
    total_salvas = 0
    total_coletadas = 0
    last_run_id: int | None = None

    for pid in perfil_ids:
        try:
            result = run_pipeline(pid, merged)
            last_run_id = int(result["run_id"])
            st = result.get("stats") or {}
            detalhes.append({"perfil": pid, "run_id": result["run_id"], "stats": st})
            total_salvas += int(st.get("salvas") or 0)
            total_coletadas += int(st.get("coletadas") or 0)
        except Exception as exc:
            erros.append({"perfil": pid, "erro": str(exc)})

    if not detalhes and erros:
        raise RuntimeError(erros[0]["erro"]) from None

    status = "finished" if not erros else "finished_with_errors"
    return {
        "run_id": last_run_id,
        "status": status,
        "stats": {
            "modo": "coleta_geral",
            "perfis_total": len(perfil_ids),
            "perfis_ok": len(detalhes),
            "salvas": total_salvas,
            "coletadas": total_coletadas,
            "detalhes": detalhes,
            "erros": erros,
        },
        "licitacoes": load_recent_licitacoes(limit=100),
    }


def run_pipeline(
    perfil: str = "limpeza_higiene",
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    init_db()
    effective_config = build_config(perfil, {**DEFAULT_CONFIG, **(config or {})})
    run_id = start_run(perfil)

    print("=" * 60)
    print("PROJETO HERMES PREMIUM")
    print(f"Perfil: {perfil}")
    print("=" * 60)

    try:
        log_event(run_id, "info", "Iniciando coleta", perfil=perfil)
        licitacoes = coletar_licitacoes(effective_config)
        saved = upsert_licitacoes(licitacoes)

        stats = {
            "coletadas": len(licitacoes),
            "salvas": saved,
            "perfil": perfil,
            "estados": effective_config["estados"],
            "max_paginas": effective_config["max_paginas"],
        }

        finish_run(run_id, stats)
        log_event(run_id, "info", "Coleta finalizada", **stats)

        print(f"{saved} registros salvos com sucesso")
        return {
            "run_id": run_id,
            "status": "finished",
            "stats": stats,
            "licitacoes": load_recent_licitacoes(limit=100),
        }
    except Exception as exc:
        finish_run(run_id, {"erro": str(exc)}, status="error", notes=str(exc))
        log_event(run_id, "error", str(exc))
        raise


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
