# teste_api.py - v4 final
import requests
import json
from datetime import datetime, timedelta

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"
}

hoje = datetime.now().strftime("%Y%m%d")
fim  = (datetime.now() + timedelta(days=60)).strftime("%Y%m%d")

BASE = "https://pncp.gov.br/api/consulta/v1"

# Endpoints documentados oficialmente
TESTES = [
    # Endpoint 1: Contratações com propostas em aberto (ideal para o Hermes)
    {
        "nome": "Propostas em aberto - SEM modalidade",
        "url":  f"{BASE}/contratacoes/proposta",
        "params": {
            "dataInicial":   hoje,
            "dataFinal":     fim,
            "pagina":        1,
            "tamanhoPagina": 10
        }
    },
    {
        "nome": "Propostas em aberto - Pregão Eletrônico (cod=6)",
        "url":  f"{BASE}/contratacoes/proposta",
        "params": {
            "dataInicial":                 hoje,
            "dataFinal":                   fim,
            "codigoModalidadeContratacao": 6,
            "pagina":                      1,
            "tamanhoPagina":               10
        }
    },
    {
        "nome": "Propostas em aberto - Dispensa (cod=8)",
        "url":  f"{BASE}/contratacoes/proposta",
        "params": {
            "dataInicial":                 hoje,
            "dataFinal":                   fim,
            "codigoModalidadeContratacao": 8,
            "pagina":                      1,
            "tamanhoPagina":               10
        }
    },
    # Endpoint 2: Publicação - tamanhoPagina minimo 10
    {
        "nome": "Publicacao - Pregão Eletrônico (cod=6) tamPag=10",
        "url":  f"{BASE}/contratacoes/publicacao",
        "params": {
            "dataInicial":                 hoje,
            "dataFinal":                   fim,
            "codigoModalidadeContratacao": 6,
            "pagina":                      1,
            "tamanhoPagina":               10
        }
    },
    {
        "nome": "Publicacao - Pregão Eletrônico (cod=6) com UF=SP",
        "url":  f"{BASE}/contratacoes/publicacao",
        "params": {
            "dataInicial":                 hoje,
            "dataFinal":                   fim,
            "codigoModalidadeContratacao": 6,
            "codigoUf":                    "SP",
            "pagina":                      1,
            "tamanhoPagina":               10
        }
    },
    # Endpoint 3: API de busca (alimenta o portal visual)
    {
        "nome": "API Busca (portal visual)",
        "url":  "https://pncp.gov.br/api/search/",
        "params": {
            "tipos_documento": "contratacao",
            "pagina":          1,
            "tam_pagina":      10,
            "status":          "recebendo_proposta"
        }
    },
    {
        "nome": "API Busca - q=software",
        "url":  "https://pncp.gov.br/api/search/",
        "params": {
            "tipos_documento": "contratacao",
            "q":               "software",
            "pagina":          1,
            "tam_pagina":      10
        }
    },
]

print("=" * 65)
print("  DIAGNÓSTICO API PNCP v4")
print(f"  Período: {hoje} a {fim}")
print("=" * 65)

for teste in TESTES:
    print(f"\n{'='*65}")
    print(f"Teste  : {teste['nome']}")
    print(f"URL    : {teste['url']}")
    print(f"Params : {teste['params']}")

    try:
        resp = requests.get(
            teste['url'],
            headers=HEADERS,
            params=teste['params'],
            timeout=30
        )
        print(f"Status : {resp.status_code}")
        print(f"URL real: {resp.url}")

        if resp.status_code == 200:
            print("\n*** FUNCIONOU! ***")
            try:
                d = resp.json()
                if isinstance(d, dict):
                    print(f"Chaves raiz: {list(d.keys())}")
                    # Procura a lista de itens
                    for chave in ['data', 'items', 'content',
                                  'contratacoes', 'resultado',
                                  'registros', 'result']:
                        if chave in d and isinstance(d[chave], list):
                            print(f"Lista em '{chave}': {len(d[chave])} itens")
                            if d[chave]:
                                item0 = d[chave][0]
                                print(f"Chaves item[0]: {list(item0.keys())}")
                                # Mostra campos mais relevantes
                                campos_interesse = [
                                    'objetoCompra', 'descricao', 'objeto',
                                    'dataAberturaProposta',
                                    'dataFimRecebimentoPropostas',
                                    'valorTotalEstimado',
                                    'modalidadeNome',
                                    'orgaoEntidade',
                                    'numeroControlePNCP',
                                    'unidadeOrgao'
                                ]
                                print("\nCampos relevantes do item[0]:")
                                for campo in campos_interesse:
                                    if campo in item0:
                                        print(f"  {campo}: {item0[campo]}")
                            break
                    else:
                        print("JSON completo:")
                        print(json.dumps(d, indent=2, ensure_ascii=False)[:1000])

                elif isinstance(d, list):
                    print(f"Lista com {len(d)} itens")
                    if d and isinstance(d[0], dict):
                        print(f"Chaves item[0]: {list(d[0].keys())}")
                        print(json.dumps(d[0], indent=2, ensure_ascii=False)[:800])

            except Exception as e:
                print(f"Erro JSON: {e}")
                print(f"Texto: {resp.text[:300]}")
        else:
            print(f"Resposta: {resp.text[:300]}")

    except requests.exceptions.Timeout:
        print("Status : TIMEOUT (30s)")
    except Exception as e:
        print(f"Erro   : {e}")

    print("-" * 65)

print("\nDiagnóstico v4 concluído.")