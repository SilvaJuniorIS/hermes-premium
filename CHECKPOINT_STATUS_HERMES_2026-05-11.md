# Checkpoint do projeto Hermes Premium

Data: 11/05/2026

## Status executivo

O Hermes Premium esta em estado de demo operacional local com publicacao externa
temporaria funcionando via Cloudflare Tunnel.

A vitrine estatica para GitHub Pages esta preparada em `docs/`. O sistema real
continua rodando localmente com FastAPI, SQLite, login por cookie, dashboard,
coleta PNCP, scoring, historico, filtros e exportacao.

## Ultimo commit registrado

```text
e2278cf Prepara demo online do Hermes
```

Esse commit incluiu:

- roteiro `DEMO_HERMES.md`;
- documentacao `IMPLANTACAO_ONLINE_HERMES.md`;
- inicializador `INICIAR_DEMO_HERMES.bat`;
- script `scripts/start_demo.ps1`;
- ajustes na vitrine `docs/index.html`;
- ajustes em `docs/README.md`;
- alteracoes relacionadas a demo em `api.py` e `dashboard.html`.

## Estado atual do Git

Alteracoes locais apos o ultimo commit:

```text
M scripts/start_demo.ps1
M src/hermes_db.py
?? cloudflared.exe
?? ngrok.exe
```

Observacao:

- `scripts/start_demo.ps1` foi ajustado para sincronizar a senha da demo com o
  banco local.
- `src/hermes_db.py` recebeu suporte para atualizar senha do usuario existente
  quando `HERMES_RESET_ADMIN_PASSWORD=1`.
- `cloudflared.exe` e `ngrok.exe` sao ferramentas locais baixadas para tunel.
  Normalmente nao devem ser commitadas no repositorio.

## Demo externa validada

Cloudflare Tunnel foi iniciado com sucesso apontando para:

```text
http://127.0.0.1:8000
```

URL temporaria gerada:

```text
https://rotation-filled-delight-absorption.trycloudflare.com
```

Status informado pelo usuario:

```text
funcionou
```

Importante: essa URL e temporaria. Ela funciona apenas enquanto a janela do
`cloudflared.exe` estiver aberta. Ao encerrar o tunel, a URL deixa de servir a
demo.

## Credenciais de demo

Usuario usado:

```text
demo
```

Senha usada na validacao:

```text
@IsaiasLindao2026
```

Validacao tecnica executada:

```text
senha ok: True
```

Recomendacao: trocar a senha antes de novas demonstracoes e evitar registrar
senhas reais em documentacao versionada. Este checkpoint deve ser tratado como
registro operacional local.

## O que esta funcionando

- Backend FastAPI inicia localmente.
- Login por cookie esta ativo.
- Usuario `demo` consegue autenticar apos sincronizacao da senha.
- Dashboard real abre em `http://127.0.0.1:8000`.
- Cloudflare Tunnel publica a demo em URL HTTPS temporaria.
- Vitrine estatica do GitHub Pages esta em `docs/index.html`.
- Logo existe em `docs/assets/logo-hermes.png`.
- Documentacao de implantacao online existe.
- Script de inicializacao da demo existe.
- Atalho Windows para demo existe.

## O que precisa de atencao imediata

1. Decidir se as correcoes de senha devem ser commitadas.
2. Remover ou ignorar `cloudflared.exe` e `ngrok.exe` antes de commit.
3. Ocultar a senha no output do `scripts/start_demo.ps1`.
4. Atualizar `.gitignore` para ferramentas locais de tunel, se necessario.
5. Testar a demo do inicio ao fim antes de reunioes comerciais.

## Melhorias prioritarias

### Prioridade 1: demo vendavel

- Base demo limpa e convincente.
- 3 a 5 oportunidades fortes selecionadas.
- Roteiro de apresentacao curto.
- Exportacao testada.
- Detalhe de oportunidade mais claro.

### Prioridade 2: seguranca

- Nao imprimir senha no terminal.
- Limitar tentativas de login.
- Expirar sessoes.
- Tela para trocar senha.
- Diferenciar ambiente demo de ambiente real.

### Prioridade 3: produto

- Status comercial por oportunidade.
- Favoritos.
- Anotacoes internas.
- Funil comercial simples.
- Melhor explicacao do score.

### Prioridade 4: operacao

- Tela de agendamento mais completa.
- Registro visivel de ultima coleta.
- Erros recentes no dashboard.
- Backup automatico do banco.
- Monitoramento basico.

### Prioridade 5: piloto

- Servidor com dominio fixo.
- HTTPS permanente.
- Variaveis de ambiente persistentes.
- Deploy via Git.
- Backup diario de `data/hermes.sqlite3`.

## Proximo passo recomendado

Fazer um pequeno hardening da demo:

1. Adicionar `cloudflared.exe` e `ngrok.exe` ao `.gitignore`.
2. Parar de mostrar a senha no terminal.
3. Commitar a correcao de sincronizacao de senha.
4. Criar uma base demo selecionada.
5. Publicar a vitrine no GitHub Pages.

## Atualizacao: envio de planilha por e-mail

Foi adicionado ao fluxo vendavel da demo:

- botao `Enviar por e-mail` no dashboard operacional;
- solicitacao do destinatario ao clicar;
- endpoint `POST /licitacoes/export/email`;
- geracao da planilha Excel com os filtros atuais;
- envio usando `src/notifier.py`;
- corpo de e-mail explicando oportunidades, filtros, score, classificacoes e destaques;
- documentacao do fluxo em `DEMO_HERMES.md` e `DOCUMENTACAO_DEMO_ONLINE_HERMES.md`.

Configuracao SMTP:

- o sistema reaproveita a configuracao existente em `src/notifier.py`;
- para producao ou piloto, preferir variaveis de ambiente `HERMES_SMTP_HOST`,
  `HERMES_SMTP_PORT`, `HERMES_SMTP_USER`, `HERMES_SMTP_PASSWORD` e
  `HERMES_EMAIL_FROM`.

## Atualizacao: acompanhamento comercial

Foi adicionada uma camada de funil comercial nas oportunidades:

- campos persistidos no SQLite: `status_comercial`, `favorito`, `anotacoes` e
  `comercial_updated_at`;
- endpoint `PUT /licitacao/comercial/{pncp_id}`;
- controles no detalhe da oportunidade para salvar status, favorito e anotacoes;
- filtros por status comercial e favoritos;
- exibicao do status na tabela;
- inclusao desses campos nas exportacoes CSV/Excel e no envio por e-mail;
- documentacao atualizada em `DEMO_HERMES.md` e
  `DOCUMENTACAO_DEMO_ONLINE_HERMES.md`.

Impacto comercial:

O Hermes deixa de ser apenas um monitor de editais e passa a apoiar a rotina de
priorizacao, triagem e acompanhamento de oportunidades.

## Atualizacao: prioridade para abertura futura

Foi ajustada a priorizacao de oportunidades para evitar que licitacoes ja
vencidas dominem o dashboard:

- API de listagem usa `prazo=futuras` por padrao;
- dashboard ganhou filtro `Abertura futura`, `Todas as datas` e `Ja passaram`;
- a tela inicia em `Abertura futura`;
- quando `Todas as datas` e usado, o backend ordena futuras antes das vencidas;
- tabela exibe a janela comercial junto da data de abertura;
- exportacoes CSV/Excel incluem `janela_comercial`;
- envio por e-mail respeita o filtro de prazo selecionado.

Impacto comercial:

A demonstracao passa a priorizar oportunidades acionaveis, com prazo aberto para
avaliacao, cotacao e proposta.

## Atualizacao: identidade de marca

Foi aplicado um passe de marca com base na direcao definida para HERMES:

- posicionamento como assistente estrategico de inteligencia licitatoria;
- tagline `Inteligencia em Licitacoes Publicas`;
- paleta com Azul Profundo `#0A2342`, Laranja Hermes `#F7931E`, Branco Gelo
  `#F5F7FA` e Cinza Grafite `#2D3748`;
- dashboard operacional com textos e cores alinhados;
- vitrine estatica `docs/index.html` ajustada para proposta premium;
- login com identidade visual HERMES;
- e-mail de envio de planilha com assinatura HERMES;
- planilha Excel com cabecalho de marca;
- novo guia `IDENTIDADE_MARCA_HERMES.md`.

Impacto comercial:

O produto passa a comunicar uma categoria mais forte: inteligencia e automacao
para compras governamentais, nao apenas um coletor de licitacoes.
