# Manual do desenvolvedor local HERMES

## 1. Objetivo

Este manual explica como rodar, configurar, testar e manter o HERMES localmente
em ambiente de desenvolvimento.

O HERMES usa:

- FastAPI em `api.py`;
- dashboard HTML em `dashboard.html`;
- SQLite em `data/hermes.sqlite3`;
- configuracoes em `config/`;
- rotinas Python em `src/`;
- vitrine estatica em `docs/`;
- scripts auxiliares em `scripts/`.

## 2. Requisitos

- Windows com PowerShell.
- Python 3.10+ recomendado.
- Ambiente virtual em `venv/`.
- Internet para consultar PNCP.
- Dependencias em `requirements.txt`.

## 3. Estrutura principal

```text
C:\Projeto_Hermes_Premium
├── api.py
├── dashboard.html
├── requirements.txt
├── config/
│   ├── perfis_negocio.json
│   └── agendamento.json
├── data/
│   └── hermes.sqlite3
├── docs/
│   ├── index.html
│   ├── vitrine.html
│   ├── atlasnex.html
│   └── produtos/
├── output/
├── scripts/
│   ├── start_demo.ps1
│   └── seed_demo_data.py
└── src/
    ├── coletor.py
    ├── hermes_db.py
    ├── main.py
    ├── notifier.py
    └── pncp_api_client.py
```

## 4. Preparar ambiente

Abra PowerShell:

```powershell
cd C:\Projeto_Hermes_Premium
```

Ative o ambiente virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

Se precisar reinstalar dependencias:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 5. Variaveis de ambiente

Use `.env.example` como referencia.

Variaveis principais:

```powershell
$env:HERMES_ADMIN_USER="demo"
$env:HERMES_ADMIN_PASSWORD="senha-forte"
$env:HERMES_RESET_ADMIN_PASSWORD="1"
```

Para desenvolvimento local com dica de login:

```powershell
$env:HERMES_DEV_LOGIN_HINT="true"
```

Para simular producao:

```powershell
$env:HERMES_ENV="production"
$env:HERMES_ADMIN_PASSWORD="SenhaForte_local_9"
$env:HERMES_COOKIE_SECURE="true"
Remove-Item Env:\HERMES_DEV_LOGIN_HINT -ErrorAction SilentlyContinue
```

Observacao:

Com `HERMES_COOKIE_SECURE=true`, login em `http://127.0.0.1` pode nao manter
sessao porque o cookie seguro exige HTTPS.

## 6. Rodar a demo local

Forma recomendada:

```powershell
.\scripts\start_demo.ps1
```

Abrir:

```text
http://127.0.0.1:8000
```

Rodar em outra porta:

```powershell
.\scripts\start_demo.ps1 -Port 8001
```

Checar dependencias sem iniciar:

```powershell
.\scripts\start_demo.ps1 -CheckOnly
```

## 7. Rodar manualmente com Uvicorn

```powershell
.\venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Com recarregamento automatico:

```powershell
.\venv\Scripts\python.exe -m uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

## 8. Carregar base demo

Para garantir dados bons em apresentacao:

```powershell
.\venv\Scripts\python.exe scripts\seed_demo_data.py
```

O script grava oportunidades demonstrativas no SQLite.

## 9. Banco de dados

Banco principal:

```text
data/hermes.sqlite3
```

Schema e operacoes ficam em:

```text
src/hermes_db.py
```

Funcoes importantes:

- `init_db`;
- `upsert_licitacoes`;
- `load_recent_licitacoes`;
- `load_licitacao_detail`;
- `update_licitacao_comercial`;
- `load_recent_api_runs`.

Para testar importacao e schema:

```powershell
.\venv\Scripts\python.exe -c "from src.hermes_db import init_db; init_db(); print('db ok')"
```

## 10. Coleta PNCP

Arquivos principais:

```text
src/coletor.py
src/main.py
src/pncp_api_client.py
```

Rodar pipeline via Python:

```powershell
.\venv\Scripts\python.exe -c "from src.main import run_pipeline, DEFAULT_CONFIG; print(run_pipeline('limpeza_higiene', DEFAULT_CONFIG)['stats'])"
```

## 11. Perfis de negocio

Arquivo:

```text
config/perfis_negocio.json
```

Cada perfil define:

- nome de exibicao;
- descricao;
- keywords;
- keywords fortes;
- termos positivos;
- termos negativos;
- valores de corte;
- score de media e alta prioridade.

Tenha cuidado ao editar JSON manualmente. Um erro de virgula quebra a leitura.

## 12. API principal

Arquivo:

```text
api.py
```

Rotas importantes:

- `GET /`
- `GET /login`
- `POST /login`
- `POST /logout`
- `POST /run`
- `POST /run-geral`
- `GET /licitacoes`
- `GET /licitacao`
- `PUT /licitacao/comercial/{pncp_id}`
- `GET /licitacoes/export/local`
- `POST /licitacoes/export/email`
- `GET /runs`
- `GET /schedule`
- `PUT /schedule`
- `GET /perfis`
- `POST /perfis`
- `PUT /perfis/{perfil_id}`
- `DELETE /perfis/{perfil_id}`
- `GET /health`

Teste rapido:

```powershell
.\venv\Scripts\python.exe -c "import api; print('api ok')"
```

## 13. Dashboard

Arquivo:

```text
dashboard.html
```

O dashboard e servido pelo FastAPI em `/`.

Ele contem:

- HTML;
- CSS;
- JavaScript;
- chamadas `fetch` para API;
- filtros;
- modal de detalhe;
- exportacoes;
- envio por e-mail;
- acompanhamento comercial.

Ao alterar `api.py`, reinicie o servidor.

Ao alterar `dashboard.html`, normalmente basta recarregar o navegador.

## 14. E-mail

Arquivo:

```text
src/notifier.py
```

Variaveis SMTP:

```powershell
$env:HERMES_SMTP_HOST="smtp.gmail.com"
$env:HERMES_SMTP_PORT="465"
$env:HERMES_SMTP_USER="seu-email@gmail.com"
$env:HERMES_SMTP_PASSWORD="senha-de-app"
$env:HERMES_EMAIL_FROM="seu-email@gmail.com"
```

O envio de planilha usa:

```text
enviar_planilha_oportunidades
```

Nunca versionar senhas reais.

## 15. GitHub Pages

Arquivos estaticos:

```text
docs/
```

Principais paginas:

- `docs/index.html`;
- `docs/vitrine.html`;
- `docs/atlasnex.html`;
- `docs/produtos/index.html`.

GitHub Pages nao roda FastAPI, SQLite ou coleta PNCP. Ele serve apenas como
vitrine.

## 16. Tunel temporario

Cloudflare Tunnel:

```powershell
.\cloudflared.exe tunnel --url http://127.0.0.1:8000
```

ngrok:

```powershell
.\ngrok.exe http 8000
```

Use tunel apenas para demo acompanhada.

## 17. Smoke test local

Antes de apresentar:

1. Rodar `git status --short`.
2. Validar importacao:

```powershell
.\venv\Scripts\python.exe -c "import api; print('api ok')"
```

3. Carregar base demo:

```powershell
.\venv\Scripts\python.exe scripts\seed_demo_data.py
```

4. Iniciar servidor:

```powershell
.\scripts\start_demo.ps1
```

5. Abrir `http://127.0.0.1:8000`.
6. Fazer login.
7. Conferir filtro `Abertura futura`.
8. Abrir detalhe.
9. Salvar acompanhamento comercial.
10. Exportar Excel.
11. Se SMTP estiver configurado, testar envio por e-mail.
12. Conferir historico e agendamento.

## 18. Smoke test de producao

Antes de expor em servidor:

1. Definir `HERMES_ENV=production`.
2. Definir senha forte.
3. Definir `HERMES_COOKIE_SECURE=true`.
4. Desligar `HERMES_DEV_LOGIN_HINT`.
5. Subir com HTTPS.
6. Testar login.
7. Testar coleta.
8. Testar exportacao.
9. Testar backup.
10. Testar restore.

## 19. Backups

Arquivo critico:

```text
data/hermes.sqlite3
```

Recomendacao:

- backup diario;
- manter 7 copias diarias;
- manter 4 copias semanais;
- testar restauracao.

## 20. Cuidados com Git

Nao commitar:

- `.env`;
- bancos SQLite reais;
- backups grandes;
- `venv/`;
- `__pycache__/`;
- executaveis locais de tunel;
- senhas;
- chaves de API.

Antes de commit:

```powershell
git status --short
git diff --stat
```

## 21. Problemas comuns

### Login nao segura sessao

Verifique se `HERMES_COOKIE_SECURE=true` esta ativo em HTTP local. Em HTTP, use:

```powershell
$env:HERMES_COOKIE_SECURE="false"
```

### Senha nao atualiza

Use uma vez:

```powershell
$env:HERMES_RESET_ADMIN_PASSWORD="1"
```

Depois reinicie e remova a variavel.

### E-mail nao envia

Verifique:

- `HERMES_SMTP_USER`;
- `HERMES_SMTP_PASSWORD`;
- senha de app do provedor;
- conexao de rede;
- bloqueio do provedor.

### Poucas oportunidades futuras

Isso pode ser normal. O produto deve priorizar oportunidades acionaveis. Use:

- perfil mais amplo;
- mais UFs;
- `cobertura_maxima`;
- base demo para apresentacao.

## 22. Documentos relacionados

- `README.md`
- `DEMO_HERMES.md`
- `DOCUMENTACAO_DEMO_ONLINE_HERMES.md`
- `IDENTIDADE_MARCA_HERMES.md`
- `ESTRATEGIA_BOOM_VENDAS_HERMES.md`
- `docs/COMMERCIALIZACAO_CHECKLIST.md`
- `docs/BLINDAGEM_E_COMERCIALIZACAO.md`

