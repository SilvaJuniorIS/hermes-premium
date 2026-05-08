from __future__ import annotations

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import requests

from src.config import KEYWORDS, STATES
from src.hermes_db import get_price_reference, parse_money


PNCP_URL = "https://pncp.gov.br/api/consulta/v1/contratacoes/proposta"
PERFIS_PATH = Path("config/perfis_negocio.json")


def _fmt_date(dt: datetime) -> str:
    return dt.strftime("%Y%m%d")


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, dict):
        return [str(item) for item in value.values() if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _load_perfil(perfil: str | None) -> dict[str, Any]:
    if not perfil or not PERFIS_PATH.exists():
        return {}

    try:
        perfis = json.loads(PERFIS_PATH.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}

    return perfis.get(perfil, {})


def build_config(perfil: str | None = None, overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    perfil_cfg = _load_perfil(perfil)
    overrides = overrides or {}

    keywords = (
        _as_list(overrides.get("keywords"))
        or _as_list(overrides.get("palavras_chave"))
        or _as_list(perfil_cfg.get("keywords"))
        or KEYWORDS
    )

    return {
        "perfil": perfil or overrides.get("perfil") or "default",
        "estados": overrides.get("estados") or overrides.get("states") or STATES,
        "keywords": keywords,
        "keywords_fortes": _as_list(perfil_cfg.get("keywords_fortes")),
        "termos_positivos": _as_list(perfil_cfg.get("termos_positivos")),
        "termos_negativos": _as_list(perfil_cfg.get("termos_negativos")),
        "valor_minimo_interesse": float(perfil_cfg.get("valor_minimo_interesse") or 0),
        "valor_atrativo": float(perfil_cfg.get("valor_atrativo") or 50000),
        "valor_muito_atrativo": float(perfil_cfg.get("valor_muito_atrativo") or 200000),
        "score_relevancia_media": float(perfil_cfg.get("score_relevancia_media") or 50),
        "score_relevancia_alta": float(perfil_cfg.get("score_relevancia_alta") or 75),
        "dias_a_frente": int(overrides.get("dias_a_frente") or 60),
        "max_paginas": int(overrides.get("max_paginas") or 5),
        "tamanho_pagina": int(overrides.get("tamanho_pagina") or 50),
        "max_total": int(overrides.get("max_total") or 300),
        "timeout": int(overrides.get("timeout") or 30),
        "delay": float(overrides.get("delay") or 0.8),
    }


def _first_match(text: str, terms: list[str]) -> str | None:
    lowered = text.lower()
    for term in terms:
        term_text = term.strip().lower()
        if term_text and term_text in lowered:
            return term
    return None


def _score_licitacao(lic: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    text = f"{lic.get('objeto') or ''} {lic.get('orgao') or ''}".lower()
    valor = parse_money(lic.get("valor_estimado_num"))

    score = 0.0
    keyword = _first_match(text, config["keywords"])
    strong = _first_match(text, config["keywords_fortes"])
    positive = _first_match(text, config["termos_positivos"])
    negative = _first_match(text, config["termos_negativos"])

    if keyword:
        score += 25
    if strong:
        score += 25
    if positive:
        score += 15
    if negative:
        score -= 25

    if valor >= config["valor_muito_atrativo"]:
        score += 25
    elif valor >= config["valor_atrativo"]:
        score += 15
    elif valor >= config["valor_minimo_interesse"]:
        score += 8

    referencia = get_price_reference(keyword, lic.get("estado")) if keyword else {"media": None}
    media = referencia.get("media")
    delta = 0.0
    if media:
        delta = round((valor - media) / media, 2)
        if delta > 0.5:
            score += 10
        elif delta < -0.2:
            score -= 5

    score = max(0.0, min(100.0, score))
    alta = config["score_relevancia_alta"]
    media_min = config["score_relevancia_media"]

    if score >= alta:
        classificacao = "ALTA"
        oportunidade = "MUITO ATRATIVA"
    elif score >= media_min:
        classificacao = "MEDIA"
        oportunidade = "ATRATIVA"
    else:
        classificacao = "BAIXA"
        oportunidade = "MONITORAR"

    return {
        "score": score,
        "classificacao": classificacao,
        "oportunidade": oportunidade,
        "delta_preco": delta,
        "keyword": keyword,
    }


def _normalize_item(item: dict[str, Any], estado: str, config: dict[str, Any]) -> dict[str, Any]:
    orgao = item.get("orgaoEntidade") or {}
    unidade = item.get("unidadeOrgao") or {}
    pncp_id = (
        item.get("numeroControlePNCP")
        or item.get("id")
        or item.get("sequencialCompra")
    )

    lic = {
        "pncp_id": str(pncp_id) if pncp_id is not None else "",
        "objeto": item.get("objetoCompra") or item.get("objeto") or "",
        "valor_estimado_num": item.get("valorTotalEstimado") or item.get("valorEstimado") or 0,
        "estado": estado,
        "municipio": orgao.get("municipioNome") or unidade.get("municipioNome"),
        "orgao": orgao.get("razaoSocial") or orgao.get("nome") or unidade.get("nomeUnidade"),
        "data_abertura": item.get("dataAberturaProposta") or item.get("dataAbertura"),
        "link": item.get("linkSistemaOrigem") or item.get("linkProcessoEletronico"),
        "source": "pncp",
        "raw": item,
    }
    lic.update(_score_licitacao(lic, config))
    return lic


def coletar_licitacoes(config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    requested = config or {}
    config = build_config(requested.get("perfil"), requested)
    resultados: dict[str, dict[str, Any]] = {}

    start = datetime.now()
    end = start + timedelta(days=config["dias_a_frente"])

    session = requests.Session()
    session.headers.update({
        "User-Agent": "HermesPremium/1.0 (+https://pncp.gov.br)",
        "Accept": "application/json",
    })

    for estado in config["estados"]:
        stop_estado = False
        for pagina in range(1, config["max_paginas"] + 1):
            if stop_estado or len(resultados) >= config["max_total"]:
                break

            params = {
                "dataInicial": _fmt_date(start),
                "dataFinal": _fmt_date(end),
                "uf": estado,
                "pagina": pagina,
                "tamanhoPagina": config["tamanho_pagina"],
            }

            for tentativa in range(1, 4):
                try:
                    response = session.get(PNCP_URL, params=params, timeout=config["timeout"])
                    if response.status_code != 200:
                        print(f"[{estado}] status {response.status_code} na pagina {pagina}")
                        break

                    payload = response.json()
                    itens = payload.get("data") or payload.get("content") or []
                    if not itens:
                        stop_estado = True
                        break

                    adicionados = 0
                    for item in itens:
                        lic = _normalize_item(item, estado, config)
                        pncp_id = lic.get("pncp_id")
                        if not pncp_id:
                            continue
                        if lic.get("keyword") or not config["keywords"]:
                            resultados[pncp_id] = lic
                            adicionados += 1

                    print(f"[{estado}] pagina {pagina}: {adicionados} registros relevantes")
                    time.sleep(config["delay"])
                    break
                except (requests.RequestException, ValueError) as exc:
                    print(f"[{estado}] tentativa {tentativa} falhou: {exc}")
                    time.sleep(2 * tentativa)

    return list(resultados.values())[: config["max_total"]]
