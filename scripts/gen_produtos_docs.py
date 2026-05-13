"""Gera fichas estáticas em docs/produtos/ a partir de dados declarativos."""
from __future__ import annotations

import html
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "produtos"

PRODUCTS = [
    {
        "slug": "cadastro-fornecedores",
        "pilar": "Pandora",
        "title": "Cadastro & qualificação de fornecedores",
        "lede": "Central de documentos e conformidade para reduzir risco de desclassificação e acelerar habilitação.",
        "problema": "Certidões vencidas, anexos dispersos em e-mail e falta de visão única do que falta para cada certame.",
        "mvps": [
            "Cadastro mestre de documentos com validade",
            "Alertas de vencimento e checklist por edital",
            "Perfis de acesso (jurídico, fiscal, comercial)",
        ],
        "hermes": "Após o Hermes priorizar oportunidades, este módulo garante que a equipe esteja pronta para habilitação sem correria de última hora.",
    },
    {
        "slug": "gestao-propostas-prazos",
        "pilar": "Ícaro",
        "title": "Gestão de propostas e prazos",
        "lede": "Orquestração da resposta ao edital: tarefas, versões e marcos críticos (impugnação, envio, esclarecimentos).",
        "problema": "Equipes perdem prazos intermediários ou trabalham em versões conflitantes de proposta.",
        "mvps": [
            "Linha do tempo por licitação com responsáveis",
            "Repositório de versão de proposta e anexos",
            "Lembretes e visão Kanban por etapa",
        ],
        "hermes": "Conecta-se ao funil do Hermes: da oportunidade priorizada até a entrega da proposta, com rastreabilidade.",
    },
    {
        "slug": "precificacao-b2g",
        "pilar": "Minerva",
        "title": "Precificação e composição de custos",
        "lede": "Simulação de custos, BDI e cenários para alinhar comercial, controladoria e engenharia antes do arremate.",
        "problema": "Decisão de preço baseada em planilhas frágeis, sem histórico nem sensibilidade a cenário.",
        "mvps": [
            "Estrutura de custos diretos e indiretos",
            "Cenários de margem e preço mínimo",
            "Exportação para a proposta e auditoria de hipóteses",
        ],
        "hermes": "Usa o valor estimado e o objeto priorizado no Hermes como ponto de partida para modelagem.",
    },
    {
        "slug": "inteligencia-concorrentes",
        "pilar": "Minerva",
        "title": "Inteligência de concorrentes (B2G)",
        "lede": "Leitura de padrões públicos de resultados para antecipar comportamento de concorrentes e de compradores.",
        "problema": "Decidir preço e estratégia sem entender quem vence, onde e em quais faixas.",
        "mvps": [
            "Painel por órgão/segmento com histórico de vencedores",
            "Indicadores de dispersão de preço (onde dados públicos permitirem)",
            "Alertas quando surgir padrão atípico em certame-alvo",
        ],
        "hermes": "Complementa a triagem do Hermes com contexto competitivo na mesma conta AtlasNex.",
    },
    {
        "slug": "contratos-entregas",
        "pilar": "Ícaro",
        "title": "Contratos e entregas pós-arrematação",
        "lede": "Gestão do ciclo pós-arremate: entregas, medições, aditivos e risco operacional.",
        "problema": "Ganhar a licitação e perder margem ou prazo na execução por falta de controle contratual.",
        "mvps": [
            "Linha do tempo de entregas e marcos contratuais",
            "Registro de aditivos e documentação",
            "Alertas de SLA e renovação",
        ],
        "hermes": "Estende o valor do Hermes além da disputa: do edital ao cumprimento contratual.",
    },
    {
        "slug": "due-diligence-orgaos",
        "pilar": "Minerva",
        "title": "Due diligence de órgãos e compradores",
        "lede": "Sinais de risco e histórico para apoiar decisão de crédito, priorização comercial e política de relacionamento.",
        "problema": "Ausência de visão consolidada sobre risco de pagamento e maturidade do comprador público.",
        "mvps": [
            "Score de risco com metodologia transparente",
            "Histórico de certames e litígios públicos relevantes",
            "Relatório executivo exportável",
        ],
        "hermes": "Ajuda a decidir se uma oportunidade alta no Hermes merece investimento comercial proporcional.",
    },
    {
        "slug": "portal-fornecedor-publico",
        "pilar": "Ícaro",
        "title": "Portal do fornecedor (lado órgão público)",
        "lede": "Canal institucional para fornecedores acompanharem status, documentos e comunicação com o órgão.",
        "problema": "Atendimento fragmentado por e-mail e falta de transparência operacional.",
        "mvps": [
            "Área do fornecedor com autenticação",
            "Status de pagamento e pendências",
            "Base de conhecimento e comunicados",
        ],
        "hermes": "Do lado do fornecedor privado, o Hermes continua sendo o cockpit; o portal atende o lado comprador.",
    },
    {
        "slug": "academia-certificacao-b2g",
        "pilar": "Ícaro",
        "title": "Treinamento & certificação B2G",
        "lede": "Trilhas de aprendizagem, atualização legal e simuladores para acelerar onboarding de equipes.",
        "problema": "Equipes desatualizadas em regras e processos, com custo alto de erro em licitação.",
        "mvps": [
            "Trilhas por perfil (comercial, compras, jurídico)",
            "Banco de questões e simulados",
            "Certificado de conclusão AtlasNex",
        ],
        "hermes": "Capacita quem usa o Hermes a extrair valor real das funcionalidades e do processo B2G.",
    },
    {
        "slug": "integracao-fiscal",
        "pilar": "Pandora",
        "title": "Integração fiscal-documental",
        "lede": "Conexão entre pedidos administrativos, notas fiscais e conciliação para reduzir retrabalho fiscal.",
        "problema": "NF-e e documentos espalhados sem amarração com o contrato e com o financeiro.",
        "mvps": [
            "Cadastro de contratos e pedidos",
            "Importação de NF-e e match sugerido",
            "Painel de pendências fiscais",
        ],
        "hermes": "Após a oportunidade virar contrato, este produto sustenta a operação documental.",
    },
    {
        "slug": "observatorio-esg-licitacoes",
        "pilar": "Pandora",
        "title": "Observatório ESG em compras públicas",
        "lede": "Monitoramento de critérios socioambientais em editais e evolução de maturidade de compras sustentáveis.",
        "problema": "ESG tratado como slogan, sem dados comparáveis entre órgãos e segmentos.",
        "mvps": [
            "Taxonomia de critérios ESG em editais",
            "Painel comparativo por UF/tema",
            "Relatórios para sustentabilidade e compliance",
        ],
        "hermes": "Cruza com o objeto e palavras-chave coletadas para mostrar tendência ESG no pipeline.",
    },
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render(p: dict) -> str:
    mvps = "\n".join(f'            <span>{esc(t)}</span>' for t in p["mvps"])
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="{esc(p["title"])} — roadmap AtlasNex ({esc(p["pilar"])}).">
    <title>{esc(p["title"])} — AtlasNex</title>
    <link rel="stylesheet" href="../assets/eco-product.css">
</head>
<body>
    <header class="topbar">
        <div class="wrap">
            <a class="back" href="../atlasnex.html#ecossistema">← AtlasNex · ecossistema</a>
            <a class="back" href="index.html">Portfólio de produtos</a>
        </div>
    </header>
    <div class="wrap">
        <header class="hero">
            <span class="pillar">Roadmap · linha {esc(p["pilar"])}</span>
            <h1>{esc(p["title"])}</h1>
            <p class="lede">{esc(p["lede"])}</p>
        </header>

        <section class="sheet">
            <h2>Problema que resolve</h2>
            <p>{esc(p["problema"])}</p>
        </section>

        <section class="sheet">
            <h2>MVP sugerido (fase 1)</h2>
            <div class="mvp">
{mvps}
            </div>
        </section>

        <section class="sheet">
            <h2>Conexão com o Hermes</h2>
            <p>{esc(p["hermes"])}</p>
        </section>

        <div class="cta-row">
            <a class="btn btn-gold" href="../index.html">Apresentação Hermes</a>
            <a class="btn btn-ghost" href="../atlasnex.html">Voltar à holding</a>
        </div>

        <footer class="foot">AtlasNex — Inteligência que constrói o futuro · Ficha de produto em roadmap.</footer>
    </div>
</body>
</html>
"""


def hub_cards() -> str:
    parts = []
    for p in PRODUCTS:
        parts.append(
            f"""            <article class="card">
                <span class="tag">{esc(p["pilar"])}</span>
                <h2><a href="{esc(p["slug"])}.html">{esc(p["title"])}</a></h2>
                <p>{esc(p["lede"])}</p>
                <a class="more" href="{esc(p["slug"])}.html">Abrir ficha →</a>
            </article>"""
        )
    return "\n".join(parts)


def hub_html() -> str:
    cards = hub_cards()
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Portfólio de produtos — AtlasNex</title>
    <link rel="stylesheet" href="../assets/eco-product.css">
    <style>
        .hub-hero {{ text-align: center; padding: 20px 0 8px; }}
        .card {{
            background: rgba(19, 36, 61, 0.55);
            border: 1px solid rgba(230, 232, 235, 0.12);
            border-radius: 14px;
            padding: 18px 18px 20px;
        }}
        .hub-hero h1 {{ font-size: clamp(1.4rem, 3vw, 1.85rem); margin: 0 0 10px; }}
        .hub-hero p {{ margin: 0 auto; max-width: 56ch; color: var(--silver); font-size: 0.95rem; }}
        .grid {{ display: grid; gap: 18px; margin-top: 28px; }}
        @media (min-width: 720px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
        @media (min-width: 1100px) {{ .grid {{ grid-template-columns: repeat(3, 1fr); }} }}
        .card .tag {{ font-size: 0.65rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--gold); font-weight: 700; display: block; margin-bottom: 8px; }}
        .card h2 {{ margin: 0 0 8px; font-size: 1rem; }}
        .card h2 a {{ color: var(--ice); text-decoration: none; }}
        .card h2 a:hover {{ color: var(--gold); }}
        .card p {{ margin: 0 0 12px; font-size: 0.88rem; color: var(--silver); }}
        .more {{ font-size: 0.85rem; }}
    </style>
</head>
<body>
    <header class="topbar">
        <div class="wrap">
            <a class="back" href="../atlasnex.html#ecossistema">← AtlasNex</a>
            <a class="back" href="../index.html">Hermes (apresentação)</a>
        </div>
    </header>
    <div class="wrap">
        <header class="hub-hero">
            <span class="pillar">Portfólio · roadmap</span>
            <h1>Linhas de produto AtlasNex</h1>
            <p>Dez frentes comerciais alinhadas ao B2G e à operação pós-licitação. Cada ficha descreve problema, MVP sugerido e encaixe com o Hermes.</p>
        </header>
        <div class="grid">
{cards}
        </div>
        <p style="margin-top:28px;font-size:0.82rem;color:var(--silver);text-align:center">
            Dados canónicos em <code><a href="../config/ecossistema_portfolio.json" style="color:inherit">config/ecossistema_portfolio.json</a></code> (publicado no site).
        </p>
        <footer class="foot">AtlasNex — Inteligência que constrói o futuro.</footer>
    </div>
</body>
</html>
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for p in PRODUCTS:
        (OUT / f"{p['slug']}.html").write_text(render(p), encoding="utf-8")
    (OUT / "index.html").write_text(hub_html(), encoding="utf-8")
    src = ROOT / "config" / "ecossistema_portfolio.json"
    dst = ROOT / "docs" / "config" / "ecossistema_portfolio.json"
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    print(f"Gerados {len(PRODUCTS)} produtos + index em {OUT}")


if __name__ == "__main__":
    main()
