from __future__ import annotations

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
