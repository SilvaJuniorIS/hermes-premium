Copiar

# Projeto Hermes
### Robô de Inteligência de Licitações Públicas — PNCP

---

## Visão Geral

O **Projeto Hermes** é um robô automatizado que coleta licitações públicas
diretamente da API oficial do Portal Nacional de Contratações Públicas (PNCP),
filtra por relevância ao perfil da empresa e gera um relatório Excel estruturado
pronto para uso pelo time comercial.

Foco atual:
- Equipamentos de informática
- Eletroeletrônicos
- Utensílios domésticos e eletroportáteis

---

## O que o Hermes faz

1. Consulta a API oficial do PNCP em dois endpoints validados.
2. Coleta licitações por estado e modalidade dentro de um período configurável.
3. Filtra por palavras-chave alinhadas ao perfil da empresa.
4. Calcula automaticamente os dias restantes até a abertura de cada licitação.
5. Aplica análise de IA (simulada) para:
   - Classificar relevância (Alta / Média / Baixa)
   - Gerar resumo do objeto
   - Identificar riscos
   - Sugerir ação (Avaliar / Monitorar / Descartar)
6. Gera relatório Excel ordenado por prioridade e dias restantes.

---

## Estrutura do Projeto
Projeto_Hermes/ │ ├── src/ │ ├── init.py │ ├── main.py # Orquestrador principal │ └── pncp_api_client.py # Cliente da API do PNCP │ ├── output/ # Relatórios Excel gerados automaticamente │ └── licitacoes_projeto_hermes_YYYYMMDD_HHMMSS.xlsx │ ├── venv/ # Ambiente virtual Python ├── requirements.txt └── README.md

---

## Requisitos

- Python 3.8 ou superior
- Conexão com a internet (acesso ao domínio `pncp.gov.br`)

### Dependências
requests pandas openpyxl

Instale com:


bash
Copiar

pip install -r requirements.txt




---

### Configuração segura (API / e-mail)

- Copie [`.env.example`](.env.example) para `.env` (o `.env` não deve ir para o Git).
- Leia [docs/BLINDAGEM_E_COMERCIALIZACAO.md](docs/BLINDAGEM_E_COMERCIALIZACAO.md): variáveis de ambiente, endurecimento no código e lacunas para comercialização.
- Checklist acionável: [docs/COMMERCIALIZACAO_CHECKLIST.md](docs/COMMERCIALIZACAO_CHECKLIST.md) (passos 1–8; **Passo 1** inclui validação `HERMES_ENV=production` no arranque da API).

---

## Como Executar

### 1. Ative o ambiente virtual


bash
Copiar

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate




### 2. Execute o projeto


bash
Copiar

python -m src.main




### 3. Encontre o relatório gerado
output/licitacoes_projeto_hermes_YYYYMMDD_HHMMSS.xlsx

---

## Configurações Principais

Todas as configurações ficam no topo do arquivo `src/main.py`.

| Parâmetro | Valor padrão | Descrição |
|---|---|---|
| `LIMITE_LICITACOES` | 1000 | Máximo de licitações únicas a coletar |
| `DIAS_MINIMOS_ABERTURA` | 7 | Mínimo de dias até abertura (filtro) |
| `DIAS_MAXIMOS_ABERTURA` | 60 | Máximo de dias até abertura (filtro) |
| `KEYWORDS` | Ver código | Palavras-chave de filtro no objeto |
| `STATES` | 14 estados | Estados brasileiros a pesquisar |

---

## API do PNCP — Endpoints Utilizados

### Endpoint 1 — Propostas em Aberto
GET https://pncp.gov.br/api/consulta/v1/contratacoes/proposta

Parâmetros:

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `dataInicial` | YYYYMMDD | Data inicial do período |
| `dataFinal` | YYYYMMDD | Data final do período |
| `pagina` | int | Número da página (começa em 1) |
| `tamanhoPagina` | int | Itens por página (máximo 50) |

### Endpoint 2 — Publicação por Modalidade + UF
GET https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao

Parâmetros:

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `dataInicial` | YYYYMMDD | Data inicial do período |
| `dataFinal` | YYYYMMDD | Data final do período |
| `codigoModalidadeContratacao` | int | Código da modalidade (ver tabela) |
| `codigoUf` | string | Sigla do estado (ex: SP) |
| `pagina` | int | Número da página |
| `tamanhoPagina` | int | Itens por página (máximo 50) |

### Códigos de Modalidade

| Código | Modalidade |
|---|---|
| 4 | Concorrência Eletrônica |
| 5 | Concorrência Presencial |
| 6 | Pregão Eletrônico |
| 7 | Pregão Presencial |
| 8 | Dispensa de Licitação |
| 9 | Inexigibilidade |
| 12 | Credenciamento |

### Estrutura do JSON retornado


json
Copiar

{
  "data": [...],
  "totalRegistros": 1500,
  "totalPaginas": 30,
  "numeroPagina": 1,
  "paginasRestantes": 29,
  "empty": false
}




### Campos mapeados por licitação

| Campo da API | Campo no relatório |
|---|---|
| `objetoCompra` | `objeto` |
| `valorTotalEstimado` | `valor_estimado` |
| `modalidadeNome` | `modalidade` |
| `orgaoEntidade.razaoSocial` | `orgao` |
| `unidadeOrgao.ufSigla` | `estado` |
| `unidadeOrgao.municipioNome` | `municipio` |
| `numeroControlePNCP` | `pncp_id` |
| `dataAberturaProposta` | `data_abertura` |
| `dataEncerramentoProposta` | `data_encerramento` |
| `dataPublicacaoPncp` | `ultima_atualizacao` |
| `linkSistemaOrigem` | `link` |
| `situacaoCompraNome` | `situacao` |

---

## Relatório Excel — Colunas

| Coluna | Descrição |
|---|---|
| `id` | Identificador sequencial |
| `prioridade` | URGENTE / ALTA / MEDIA / BAIXA / N/A |
| `dias_restantes` | Dias até abertura |
| `data_abertura` | Data de abertura (DD/MM/AAAA) |
| `data_encerramento` | Data de encerramento das propostas |
| `ultima_atualizacao` | Última atualização no PNCP |
| `relevancia_ia` | Alta / Média / Baixa |
| `recomendacao_ia` | Ação sugerida pela IA |
| `objeto` | Descrição completa da licitação |
| `informacao_compl` | Informação complementar do edital |
| `resumo_ia` | Resumo gerado pela IA |
| `riscos_ia` | Riscos identificados pela IA |
| `valor_estimado` | Valor em R$ (padrão brasileiro) |
| `modalidade` | Tipo de licitação |
| `orgao` | Órgão responsável |
| `estado` | UF do órgão |
| `municipio` | Município do órgão |
| `keyword` | Palavra-chave que identificou a licitação |
| `situacao` | Situação atual no PNCP |
| `pncp_id` | ID único no PNCP |
| `link` | Link direto para o edital |
| `prazo_entrega_execucao` | Campo manual |
| `requisitos_especificos` | Campo manual |
| `contato_orgao` | Campo manual |
| `observacoes` | Campo manual |

---

## Lógica de Prioridade

| Dias restantes | Prioridade |
|---|---|
| Até 14 dias | URGENTE |
| 15 a 28 dias | ALTA |
| 29 a 45 dias | MEDIA |
| 46 a 60 dias | BAIXA |

---

## Lógica de Relevância (IA Simulada)

A IA classifica cada licitação em **Alta**, **Média** ou **Baixa** com base em:

- Presença de palavras-chave de alto interesse no objeto
  (computador, televisor, geladeira, purificador, etc.)
- Ausência de termos fora do foco
  (obra, alimento, manutenção predial, etc.)
- Valor estimado: licitações abaixo de R$ 20.000 são rebaixadas automaticamente

---

## Perfil de Negócio

A empresa atua com:

- Equipamentos de informática (computadores, notebooks, impressoras,
  roteadores, switches, storages, periféricos)
- Eletroeletrônicos (televisores, projetores, equipamentos de áudio e vídeo,
  nobreaks, estabilizadores)
- Utensílios domésticos e eletroportáteis (geladeiras, micro-ondas,
  liquidificadores, cafeteiras, ventiladores, aspiradores, bebedouros)

Ticket mínimo de interesse: **R$ 20.000,00**

Fora do escopo: obras de engenharia, manutenção predial,
fornecimento de alimentos e gêneros alimentícios.

---

## Performance Observada

| Indicador | Resultado |
|---|---|
| Tempo de execução | ~60 minutos |
| Licitações coletadas | ~323 |
| Aprovadas pelo filtro de data | ~86 |
| Tempo com Selenium (versão antiga) | ~4 a 5 horas |
| Ganho com migração para API | 95% mais rápido |

---

## Observações Importantes

- A API do PNCP apresenta timeouts intermitentes por instabilidade do servidor.
  O código trata automaticamente esses erros e segue para a próxima combinação.
- O parâmetro `codigoUf` é obrigatório no endpoint `/publicacao`.
  Sem ele, a requisição gera timeout.
- O parâmetro `codigoModalidadeContratacao` é obrigatório no endpoint `/publicacao`.
  Sem ele, a API retorna erro 400.
- Redes corporativas com proxy ou firewall restritivo podem causar
  timeouts adicionais. Nesse caso, teste via hotspot móvel para diagnóstico.

---

## Próximas Evoluções Planejadas

- [ ] Integração com IA real (OpenAI GPT-4o / Google Gemini)
- [ ] Agendamento automático diário (Task Scheduler / cron)
- [ ] Banco de dados local (SQLite) para histórico de licitações
- [ ] Notificação por e-mail para licitações de Alta relevância
- [ ] Formatação visual do Excel (cores por prioridade)
- [ ] Interface web simples (Streamlit) para configurar sem editar código
- [ ] Suporte a múltiplos perfis de empresa

---

## Autor

Projeto desenvolvido internamente.
Versão atual: **2.0**
Última atualização: **Abril / 2026**
Parâmetro	Tipo	Descrição
dataInicial	YYYYMMDD	Data inicial do período
dataFinal	YYYYMMDD	Data final do período
codigoModalidadeContratacao	int	Código da modalidade (ver tabela)
codigoUf	string	Sigla do estado (ex: SP)
pagina	int	Número da página
tamanhoPagina	int	Itens por página (máximo 50)
