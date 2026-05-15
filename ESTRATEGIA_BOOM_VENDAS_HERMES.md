# Estrategia para transformar o HERMES em produto vendavel

Data de referencia: 15/05/2026

## 1. Diagnostico executivo

O HERMES ja deixou de ser apenas um coletor tecnico de licitacoes. Hoje ele se
posiciona como uma plataforma de inteligencia B2G com:

- backend FastAPI;
- login por cookie;
- banco SQLite;
- coleta PNCP;
- perfis de negocio;
- score;
- dashboard operacional;
- filtro por abertura futura;
- acompanhamento comercial por oportunidade;
- exportacao Excel/CSV;
- envio de planilha por e-mail;
- agendamento local;
- historico de execucoes;
- vitrine estatica em GitHub Pages;
- identidade HERMES;
- expansao de ecossistema AtlasNex com roadmap de produtos B2G.

Status real: **bom para demo vendavel e piloto controlado**.

Ainda nao esta pronto para venda escalada SaaS sem as etapas de seguranca,
juridico, hospedagem, suporte e precificacao.

## 2. Status atual medido

Validacoes locais realizadas em 15/05/2026:

```text
api import ok
total de registros na base: 617
oportunidades com abertura futura: 11
oportunidades vencidas: 606
historico de execucoes lidas: 50
git status: limpo
```

Leitura comercial:

- A base tem volume, mas a maior parte esta vencida.
- O produto deve vender **priorizacao acionavel**, nao quantidade bruta.
- A tela com `Abertura futura` como padrao esta correta.
- Para demo, usar base real futura + dados demonstrativos fortes.

## 3. Checklist de comercializacao: status interpretado

Fonte principal:

```text
docs/COMMERCIALIZACAO_CHECKLIST.md
```

### Passo 1: seguranca operacional e segredos

Status: **parcialmente concluido**.

Concluido:

- validacao de ambiente quando `HERMES_ENV=production`;
- senha forte obrigatoria em producao;
- cookie seguro obrigatorio em producao;
- dica de login dev desligada em producao;
- protecao basica contra forca bruta;
- cabecalhos HTTP basicos;
- `.env.example`;
- SMTP sem segredo fixo no codigo.

Pendente:

- revogar senhas antigas que possam ter aparecido no historico;
- criar `.env` local seguro;
- testar positivo/negativo de `HERMES_ENV=production`;
- testar envio SMTP real;
- registrar quem tem acesso ao servidor e segredos.

Factibilidade: **alta**. E etapa de 1 a 2 dias.

### Passo 2: hospedagem e continuidade

Status: **pendente**.

Pendente:

- dominio proprio;
- HTTPS;
- reverse proxy;
- backup automatico do SQLite;
- reinicio automatico;
- teste de restauracao.

Factibilidade: **alta para piloto**, media para SaaS escalado.

### Passo 3: juridico e privacidade

Status: **pendente**.

Pendente:

- termos de uso;
- politica de privacidade;
- clausula LGPD;
- limitacao de responsabilidade sobre PNCP;
- contrato/order form.

Factibilidade: **alta**, mas exige revisao juridica antes de venda paga.

### Passo 4: comercial e oferta

Status: **em construcao**.

Concluido:

- identidade HERMES;
- vitrine;
- demo operacional;
- roadmap AtlasNex;
- documentos de negocio iniciais.

Pendente:

- oferta em uma pagina;
- precificacao;
- proposta comercial;
- pacote piloto;
- SLA e suporte.

Factibilidade: **alta**. Essa e a etapa mais importante para vender.

### Passo 5: produto e suporte

Status: **parcial**.

Concluido:

- acompanhamento comercial;
- exportacoes;
- envio por e-mail;
- agendamento;
- historico.

Pendente:

- troca de senha;
- usuarios/perfis de acesso;
- canal de suporte;
- manual curto para cliente;
- observabilidade de erros.

Factibilidade: **alta para piloto**, media para escala.

### Passo 6: engenharia

Status: **pendente para escala**.

Pendente:

- pin de dependencias;
- auditoria de dependencias;
- rate limit em rotas pesadas;
- CSP;
- sessao persistente/JWT se houver multiplas instancias.

Factibilidade: **media**. Nao bloqueia demo, mas bloqueia escala madura.

### Passo 7: go-to-market

Status: **pendente**.

Pendente:

- escolher nicho inicial;
- prospectar clientes piloto;
- roteiro de demo por segmento;
- pagina de captura;
- material de venda;
- metricas de sucesso.

Factibilidade: **alta**, desde que o foco seja estreito.

### Passo 8: pre-lancamento

Status: **pendente**.

Pendente:

- smoke test formal;
- revisao de URLs;
- lista de seguranca;
- teste de backup;
- teste de e-mail;
- teste de coleta agendada.

Factibilidade: **alta**.

## 4. Brainstorm passo a passo para virar produto de venda

### Etapa 1: escolher uma praia estreita

Objetivo:

Vender primeiro para um segmento especifico, nao para "todo mundo que participa
de licitacao".

Ideias:

- fornecedores de limpeza e higiene;
- moveis corporativos;
- equipamentos de TI;
- medicamentos/demanda judicial;
- manutencao predial.

Recomendacao:

Comecar com **limpeza/higiene** ou **TI**, porque sao segmentos amplos, com
recorrencia de edital e decisao facil de explicar.

Factibilidade: **muito alta**.

### Etapa 2: promessa comercial objetiva

Promessa recomendada:

```text
Receba oportunidades publicas filtradas por aderencia, prazo e valor, com score e acompanhamento comercial.
```

Evitar prometer:

- vencer licitacoes;
- garantir faturamento;
- IA perfeita;
- cobertura integral de todo o Brasil no primeiro piloto.

Factibilidade: **muito alta**.

### Etapa 3: pacote piloto

Oferta piloto:

```text
Piloto HERMES 30 dias
```

Inclui:

- configuracao de ate 3 perfis comerciais;
- monitoramento de 3 a 5 UFs;
- uma rotina diaria de coleta;
- dashboard com oportunidades futuras;
- exportacao Excel;
- envio de planilha por e-mail;
- reuniao semanal de leitura das oportunidades.

Preco sugerido para testar mercado:

- piloto acompanhado: R$ 497 a R$ 1.500 por 30 dias;
- mensal recorrente apos piloto: R$ 297 a R$ 997, dependendo do nicho e suporte.

Factibilidade: **alta**.

Observacao:

Antes de fixar preco definitivo, validar disposicao de pagamento com 5 a 10
prospects.

### Etapa 4: material de venda minimo

Criar:

- pagina "para quem e";
- PDF de uma pagina;
- print do dashboard;
- video curto de 2 minutos;
- roteiro de demo;
- proposta comercial simples.

Mensagem:

```text
HERMES nao substitui sua equipe comercial. Ele reduz tempo perdido filtrando edital ruim e destaca o que merece acao.
```

Factibilidade: **alta**.

### Etapa 5: roteiro de demo matador

Fluxo:

1. Mostrar problema: excesso de edital, prazo perdido e analise manual.
2. Mostrar dashboard com `Abertura futura`.
3. Abrir oportunidade alta.
4. Explicar score, valor, prazo, orgao e fonte.
5. Marcar status comercial e anotacao.
6. Exportar Excel.
7. Enviar por e-mail.
8. Mostrar agendamento.
9. Fechar com piloto de 30 dias.

Factibilidade: **muito alta**.

### Etapa 6: prova de valor semanal

Durante o piloto, enviar relatorio semanal:

- oportunidades encontradas;
- oportunidades realmente uteis;
- oportunidades descartadas;
- tempo economizado;
- editais que mereceram proposta;
- valor estimado total monitorado.

Metricas recomendadas:

- oportunidades futuras encontradas por semana;
- taxa de oportunidades uteis;
- tempo de analise reduzido;
- quantidade de propostas avaliadas;
- valor estimado em pipeline.

Factibilidade: **alta**.

### Etapa 7: criar "produto ao redor do produto"

Ideias com grande poder de venda:

- reuniao semanal de inteligencia B2G;
- configuracao de perfis feita por especialista;
- monitoramento personalizado por UF;
- alerta por e-mail/WhatsApp;
- relatorio executivo mensal;
- curadoria humana opcional.

Por que isso pode vender:

Muitos clientes pequenos nao querem apenas software. Querem resultado, criterio e
organizacao.

Factibilidade: **alta**.

### Etapa 8: virar ecossistema sem perder foco

O roadmap AtlasNex e bom, mas deve ser vendido em camadas:

1. HERMES: encontrar e priorizar oportunidades.
2. Gestao de propostas e prazos: organizar resposta ao edital.
3. Cadastro e qualificacao: reduzir risco de inabilitacao.
4. Precificacao B2G: decidir se vale entrar e com que preco.
5. Inteligencia de concorrentes: entender mercado.

Regra:

Nao tentar vender os 10 produtos agora. Usar o ecossistema como visao, mas vender
HERMES como produto inicial.

Factibilidade: **media-alta**, se houver disciplina.

## 5. Ideias para "boom de vendas"

### Ideia 1: campanha "edital perdido custa caro"

Conteudo:

- posts e videos curtos mostrando editais futuros reais;
- antes/depois: busca manual vs HERMES;
- chamada para diagnostico gratuito.

Factibilidade: **alta**.

Risco:

Precisa de constancia e bons exemplos reais.

### Ideia 2: diagnostico gratuito por segmento

Oferta:

```text
Eu rodo uma busca de 7 dias para seu segmento e te mostro quantas oportunidades futuras existem.
```

Isso transforma o produto em conversa comercial.

Factibilidade: **muito alta**.

### Ideia 3: relatorio semanal patrocinado

Criar uma newsletter:

```text
Radar HERMES de Licitacoes
```

Versoes por segmento:

- Radar Limpeza;
- Radar TI;
- Radar Moveis;
- Radar Medicamentos.

Factibilidade: **alta**.

Risco:

Demanda rotina de curadoria.

### Ideia 4: grupo fechado de WhatsApp

Entregar oportunidades curadas em grupo pago ou comunidade.

Factibilidade: **media**.

Risco:

Pode virar servico manual demais. Bom para validar demanda, ruim para escalar sem
processo.

### Ideia 5: parceria com contadores, consultores e despachantes

Parceiros que ja atendem empresas fornecedoras podem indicar HERMES.

Modelo:

- comissao por cliente;
- white-label simples;
- pacote consultor + HERMES.

Factibilidade: **alta**.

### Ideia 6: "primeira oportunidade gratis"

Mostrar 1 oportunidade real e cobrar pelo monitoramento continuo.

Factibilidade: **alta**.

Risco:

Precisa cuidar para nao parecer promessa de ganho garantido.

### Ideia 7: video demonstracao com numero concreto

Exemplo:

```text
Encontramos 11 oportunidades futuras em uma base de 617 registros. O HERMES separou o que ainda da tempo de atacar.
```

Factibilidade: **alta**.

## 6. O que e factivel agora

### Factivel em 7 dias

- definir nicho inicial;
- montar proposta de valor em uma pagina;
- criar oferta piloto;
- revisar vitrine;
- criar video curto;
- rodar 20 prospeccoes manuais;
- fechar 1 a 3 demos.

### Factivel em 30 dias

- colocar em VPS com HTTPS;
- fechar 1 piloto pago ou semi-pago;
- criar rotina semanal de relatorio;
- ajustar coleta por nicho;
- documentar onboarding;
- criar contrato simples com revisao juridica.

### Factivel em 90 dias

- 5 a 10 clientes piloto;
- precificacao validada;
- modulo de usuarios;
- troca de senha;
- backup automatico;
- alertas;
- primeira versao de gestao de propostas/prazos.

## 7. O que nao e factivel prometer ainda

- SaaS multi-tenant escalado sem refatorar sessoes, usuarios e isolamento de dados.
- Garantia de vencer licitacao.
- IA juridica completa de edital.
- Cobertura perfeita de todos os orgaos e portais fora do PNCP.
- Automacao completa de proposta.
- Escala nacional sem suporte, backup e juridico.

## 8. Estrategia recomendada

### Fase 1: venda assistida

Prazo: 0 a 30 dias.

Foco:

- vender HERMES como monitor inteligente acompanhado;
- cliente piloto;
- nicho unico;
- suporte proximo;
- preco acessivel;
- aprendizado rapido.

### Fase 2: produto com rotina

Prazo: 30 a 90 dias.

Foco:

- hospedagem real;
- onboarding;
- alertas;
- relatorio semanal;
- troca de senha;
- backup;
- contrato.

### Fase 3: ecossistema AtlasNex

Prazo: 90 a 180 dias.

Foco:

- gestao de propostas;
- cadastro documental;
- precificacao;
- inteligencia de concorrentes;
- upsell para clientes que ja usam HERMES.

## 9. Proximas acoes recomendadas

1. Escolher um nicho inicial.
2. Criar a oferta "Piloto HERMES 30 dias".
3. Montar uma pagina comercial curta.
4. Criar um video de demo de 2 minutos.
5. Rodar uma coleta limpa para o nicho escolhido.
6. Gerar 3 exemplos fortes de oportunidade.
7. Validar envio por e-mail real.
8. Definir preco piloto.
9. Prospectar 20 empresas.
10. Fazer 5 conversas de diagnostico.
11. Fechar 1 piloto acompanhado.

## 10. Conclusao

O projeto e factivel como produto vendavel, desde que a primeira venda seja
tratada como **piloto acompanhado**, nao como SaaS autossuficiente.

O caminho mais forte e:

```text
HERMES como assistente estrategico que encontra, prioriza e organiza oportunidades publicas ainda acionaveis.
```

O possivel "boom de vendas" nao vem de prometer tecnologia demais. Vem de uma
oferta simples, nichada, com prova rapida de valor e acompanhamento proximo nos
primeiros clientes.

