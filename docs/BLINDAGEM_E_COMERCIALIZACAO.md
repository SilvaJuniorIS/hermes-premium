# Blindagem do Hermes e caminho para comercialização

Este documento resume **medidas já aplicadas no código**, o **estado atual** do produto e **lacunas** típicas antes de vender a clientes (B2G / SaaS).

---

## 1. O que foi endurecido no repositório (técnico)

| Medida | Detalhe |
|--------|---------|
| **Segredos fora do código** | Removidas credenciais SMTP e telefone em claro de `src/notifier.py`. SMTP só funciona com `HERMES_SMTP_USER` / `HERMES_SMTP_PASSWORD` no ambiente. |
| **Falha explícita sem SMTP** | Se envio de e-mail for chamado sem credenciais, ocorre erro claro em vez de usar valores inventados. |
| **Cookie de sessão** | Em HTTPS, ative `HERMES_COOKIE_SECURE=true` para o atributo `Secure` no cookie. |
| **Dica de login default** | A frase “admin / admin123” **só** aparece se `HERMES_DEV_LOGIN_HINT=true`. Em produção mantenha **sem** esta variável. |
| **Proteção a força bruta (login)** | Após muitas falhas por IP numa janela de tempo, o `POST /login` responde `429` até a janela expirar. |
| **Cabeçalhos HTTP** | `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` em todas as respostas da API. |
| **Modelo de configuração** | Ficheiro `.env.example` na raiz com variáveis documentadas. |

### Ação obrigatória após histórico com segredos

Se alguma palavra-passe de aplicação (ex.: Gmail) chegou a estar no código ou no Git: **revogue essa palavra-passe na consola do fornecedor** e crie uma nova, mesmo que já tenha sido removida do ficheiro — o histórico do Git pode conservá-la.

---

## 2. Estado atual do Hermes (resumo honesto)

**Já existe (MVP sólido para piloto interno ou demo controlada):**

- API FastAPI com login por sessão, dashboard estático, SQLite, coleta PNCP por perfil e coleta geral.
- Perfis editáveis (`config/perfis_negocio.json`), score, exportação Excel, e-mail de planilha (com SMTP configurado).
- Agendamento local, histórico de execuções, campos comerciais (status, favorito, anotações).
- Site estático de apresentação (GitHub Pages) e vitrine.

**Limitações típicas de “um servidor, um ficheiro”:**

- Sessões em **memória** — reinício do processo invalida sessões; não serve para múltiplas instâncias sem sticky sessions ou Redis.
- **Um utilizador admin** inicial conhecido — exige alteração de senha e política de utilizadores para multi-tenant.
- **Sem** CSP estrito, **sem** WAF, **sem** auditoria formal de dependências no CI (recomendado acrescentar).
- **LGPD / contratos / SLA** não estão no código — são documentos e processos à parte.

---

## 3. O que falta para “comercializar” com mais segurança

### Jurídico e comercial

- Termos de uso, política de privacidade, registo de tratamento (LGPD), limitação de responsabilidade sobre dados públicos PNCP.
- Contrato de licença ou SaaS (preço, suporte, SLA, rescisão).
- Proposta de valor e packaging (por utilizador, por UF, por volume de coleta).

### Produto e operações

- Fluxo de **onboarding**: primeiro login obriga troca de senha; opcional 2FA.
- **Backups** agendados do SQLite e teste de restauro.
- **Observabilidade**: logs estruturados, métricas, alerta de falha de coleta.
- **Hardening de hospedagem**: TLS obrigatório, reverse proxy (nginx/Caddy), `HERMES_COOKIE_SECURE=true`.

### Engenharia (próximas melhorias no código)

- Armazenar sessões em backend partilhado ou JWT com rotação, se houver réplicas.
- Rate limit também em rotas sensíveis (`/run`, exportações).
- `pip-audit` / Dependabot e pin de versões em `requirements.txt`.
- Content-Security-Policy alinhado ao `dashboard.html` (hoje há muito inline — exige refatoração para CSP útil).

---

## 4. Variáveis de ambiente (referência rápida)

Ver `.env.example` na raiz do repositório.

---

*Última revisão alinhada ao código na data do commit que introduz este ficheiro e as alterações de blindagem.*
