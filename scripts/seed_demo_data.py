from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.hermes_db import upsert_licitacoes


def future_date(days: int) -> str:
    return (datetime.now() + timedelta(days=days)).isoformat(timespec="seconds")


DEMO_OPPORTUNITIES = [
    {
        "perfil": "limpeza_higiene",
        "pncp_id": "DEMO-LIMPEZA-001",
        "objeto": "Registro de precos para fornecimento de materiais de limpeza, higiene, descartaveis e saneantes para unidades municipais de saude.",
        "valor_estimado_num": 487500.00,
        "estado": "SP",
        "municipio": "Campinas",
        "orgao": "Secretaria Municipal de Saude de Campinas",
        "keyword": "material de limpeza",
        "data_abertura": future_date(12),
        "score": 93,
        "classificacao": "ALTA",
        "oportunidade": "Alta aderencia ao perfil, valor relevante e prazo adequado para proposta.",
        "delta_preco": 0,
        "score_motivos": [
            "Objeto menciona material de limpeza, higiene e descartaveis.",
            "Valor estimado acima da faixa muito atrativa do perfil.",
            "Prazo de abertura permite analise comercial e cotacao com fornecedores.",
        ],
        "link": "",
        "source": "demo",
        "raw": {"ambiente": "demo", "segmento": "limpeza"},
    },
    {
        "perfil": "moveis_corporativos",
        "pncp_id": "DEMO-MOVEIS-002",
        "objeto": "Aquisicao de mobiliario escolar, mesas, cadeiras, armarios e longarinas para modernizacao de escolas municipais.",
        "valor_estimado_num": 820000.00,
        "estado": "MG",
        "municipio": "Uberlandia",
        "orgao": "Secretaria Municipal de Educacao de Uberlandia",
        "keyword": "mobiliario escolar",
        "data_abertura": future_date(18),
        "score": 91,
        "classificacao": "ALTA",
        "oportunidade": "Pacote amplo de itens com ticket alto e forte aderencia a fornecedor de mobiliario.",
        "delta_preco": 0,
        "score_motivos": [
            "Objeto combina mobiliario escolar, mesas, cadeiras e armarios.",
            "Valor estimado muito atrativo para venda consultiva.",
            "Orgao e municipio claros para prospeccao direcionada.",
        ],
        "link": "",
        "source": "demo",
        "raw": {"ambiente": "demo", "segmento": "moveis"},
    },
    {
        "perfil": "informatica_ti",
        "pncp_id": "DEMO-TI-003",
        "objeto": "Contratacao para fornecimento de notebooks, monitores, nobreaks e perifericos para renovacao do parque tecnologico.",
        "valor_estimado_num": 1260000.00,
        "estado": "PR",
        "municipio": "Londrina",
        "orgao": "Fundacao Municipal de Tecnologia",
        "keyword": "notebooks",
        "data_abertura": future_date(9),
        "score": 89,
        "classificacao": "ALTA",
        "oportunidade": "Demanda concentrada de equipamentos de TI com valor alto e itens de fornecimento direto.",
        "delta_preco": 0,
        "score_motivos": [
            "Objeto menciona notebooks, monitores, nobreaks e perifericos.",
            "Valor estimado acima de R$ 1 milhao.",
            "Abertura proxima, mas ainda com janela para decisao rapida.",
        ],
        "link": "",
        "source": "demo",
        "raw": {"ambiente": "demo", "segmento": "ti"},
    },
    {
        "perfil": "manutencao_predial",
        "pncp_id": "DEMO-MANUT-004",
        "objeto": "Servicos continuados de manutencao predial preventiva e corretiva, com fornecimento de materiais, para predios administrativos.",
        "valor_estimado_num": 640000.00,
        "estado": "RJ",
        "municipio": "Niteroi",
        "orgao": "Autarquia Municipal de Administracao",
        "keyword": "manutencao predial",
        "data_abertura": future_date(21),
        "score": 78,
        "classificacao": "ALTA",
        "oportunidade": "Contrato recorrente com escopo claro e possibilidade de receita continuada.",
        "delta_preco": 0,
        "score_motivos": [
            "Escopo de manutencao predial preventiva e corretiva.",
            "Contrato continuado favorece previsibilidade operacional.",
            "Valor acima da faixa atrativa do perfil.",
        ],
        "link": "",
        "source": "demo",
        "raw": {"ambiente": "demo", "segmento": "servicos"},
    },
    {
        "perfil": "limpeza_higiene",
        "pncp_id": "DEMO-LIMPEZA-005",
        "objeto": "Aquisicao parcelada de papel toalha, sabonete liquido, alcool 70, lixeiras e produtos de higiene para escolas.",
        "valor_estimado_num": 148000.00,
        "estado": "SC",
        "municipio": "Joinville",
        "orgao": "Fundo Municipal de Educacao",
        "keyword": "higiene",
        "data_abertura": future_date(15),
        "score": 68,
        "classificacao": "MEDIA",
        "oportunidade": "Boa aderencia, mas com valor intermediario e mix pulverizado de itens.",
        "delta_preco": 0,
        "score_motivos": [
            "Objeto contem itens recorrentes de higiene e limpeza.",
            "Valor adequado para monitoramento comercial.",
            "Pode ser combinado com fornecedores locais.",
        ],
        "link": "",
        "source": "demo",
        "raw": {"ambiente": "demo", "segmento": "limpeza"},
    },
]


def main() -> None:
    total = upsert_licitacoes(DEMO_OPPORTUNITIES)
    print(f"Base demo carregada: {total} oportunidades.")


if __name__ == "__main__":
    main()
