# Checklist de comercialização — Hermes Premium

Use este ficheiro como **lista de trabalho**: marque `[x]` quando cada item estiver concluído. A ordem reflete dependências típicas (segurança e jurídico antes de escalar vendas).

**Documentos relacionados:** [BLINDAGEM_E_COMERCIALIZACAO.md](BLINDAGEM_E_COMERCIALIZACAO.md) · [`.env.example`](../.env.example)

---

## Passo 1 — Segurança operacional e segredos

*Parte deste passo está automatizada no código: com `HERMES_ENV=production`, a API **não arranca** se a configuração mínima de produção for inválida (`api.py`).*

### Como testar a validação no ambiente local

**Desenvolvimento normal (sem simular produção)**  
Não defina `HERMES_ENV`, ou deixe o valor **vazio** / diferente de `production` (ex.: `development`). Nesse caso **nenhuma** regra extra de arranque é aplicada: o comportamento é o de sempre (senha inicial `admin123` se não houver `HERMES_ADMIN_PASSWORD`, dica de login se `HERMES_DEV_LOGIN_HINT=true`, etc.).

**Simular produção (validar que o arranque exige configuração mínima)**  
Defina **na mesma sessão de terminal** (antes de lançar o `uvicorn`) as variáveis abaixo. Os três critérios são verificados em conjunto: senha forte, cookie seguro e dica de dev desligada.

| Variável | Valor de teste |
|----------|----------------|
| `HERMES_ENV` | `production` |
| `HERMES_ADMIN_PASSWORD` | qualquer string **≠** `admin123` (ex.: `TesteSeguro_local_9`) |
| `HERMES_COOKIE_SECURE` | `true` |
| `HERMES_DEV_LOGIN_HINT` | omitir, `false`, ou `0` |

1. **Teste positivo:** com todas as linhas da tabela definidas, execute `uvicorn api:app --reload` (ou o comando que usar). O processo deve **subir** sem `RuntimeError`.
2. **Testes negativos (um de cada vez):** mantenha `HERMES_ENV=production` e altere **só uma** das outras condições — por exemplo remova `HERMES_ADMIN_PASSWORD`, volte a pôr `admin123`, defina `HERMES_COOKIE_SECURE=false`, ou `HERMES_DEV_LOGIN_HINT=true`. Em cada caso o arranque deve **falhar** com mensagem que lista o que falta (mensagem de `RuntimeError` no log).

**Nota sobre cookie `Secure` e `http://localhost`**  
Com `HERMES_COOKIE_SECURE=true`, o navegador **não envia** o cookie de sessão em ligações **HTTP** sem TLS. Ou seja: pode validar o **arranque** da API assim, mas o **login no dashboard** em `http://127.0.0.1` pode não manter sessão. Para testar login com perfil idêntico ao de produção, use HTTPS local (certificado de desenvolvimento, reverse proxy) ou um túnel HTTPS para a instância local.

**PowerShell (exemplo de sessão única)**

```powershell
$env:HERMES_ENV = "production"
$env:HERMES_ADMIN_PASSWORD = "TesteSeguro_local_9"
$env:HERMES_COOKIE_SECURE = "true"
Remove-Item Env:\HERMES_DEV_LOGIN_HINT -ErrorAction SilentlyContinue
uvicorn api:app --host 127.0.0.1 --port 8000
```

**Bash (exemplo equivalente)**

```bash
export HERMES_ENV=production
export HERMES_ADMIN_PASSWORD='TesteSeguro_local_9'
export HERMES_COOKIE_SECURE=true
unset HERMES_DEV_LOGIN_HINT
uvicorn api:app --host 127.0.0.1 --port 8000
```

- [x] **(Código)** Validação no arranque quando `HERMES_ENV=production` (senha forte obrigatória, cookie seguro, sem dica de login de desenvolvimento).
- [ ] **Revogar** no fornecedor (Google, etc.) qualquer palavra-passe de aplicação ou chave que tenha existido em commits antigos do repositório.
- [ ] Copiar [`.env.example`](../.env.example) para `.env` na raiz do projeto e preencher apenas o necessário (nunca commitar `.env`).
- [ ] Definir **`HERMES_ADMIN_PASSWORD`** com senha forte antes de expor o serviço à Internet.
- [ ] Em servidor público com HTTPS: `HERMES_ENV=production`, `HERMES_COOKIE_SECURE=true`, **sem** `HERMES_DEV_LOGIN_HINT` (ou `false`).
- [ ] Executar os **testes positivo e negativos** descritos na secção “Como testar a validação no ambiente local” (confirmar subida e falhas esperadas).
- [ ] Se usar e-mail: `HERMES_SMTP_*` e `HERMES_EMAIL_FROM` preenchidos; testar envio de planilha uma vez.
- [ ] Documentar internamente **quem** tem acesso ao `.env` e ao servidor (lista mínima de pessoas).

---

## Passo 2 — Hospedagem e continuidade

- [ ] Domínio próprio e certificado TLS (Let’s Encrypt ou equivalente).
- [ ] Reverse proxy (nginx, Caddy, Traefik) com timeouts e limite de tamanho de corpo adequados.
- [ ] **Backups** agendados do ficheiro SQLite (`data/hermes.sqlite3`) + teste de **restauro** documentado.
- [ ] Plano de **reinício** automático (systemd, Docker restart policy, ou PaaS equivalente).

---

## Passo 3 — Jurídico e privacidade (Brasil)

- [ ] **Termos de uso** do software (licença de uso, limitações, exclusão de garantia sobre resultados em licitação).
- [ ] **Política de privacidade** e alinhamento à **LGPD** (bases legais, retenção, direitos do titular, registo de operações de tratamento).
- [ ] **DPA** (contrato de tratamento) se usar subempreiteiros com acesso a dados (e-mail, hospedagem, IA).
- [ ] Cláusula sobre **dados públicos PNCP** e responsabilidade do cliente quanto ao uso das informações.

---

## Passo 4 — Comercial e oferta

- [ ] **Proposta de valor** em uma página (para quem é, problema, resultado, diferencial).
- [ ] **Packaging**: preço (mensal / anual / piloto), o que inclui (Ufs, perfis, suporte, SLAs).
- [ ] **Contrato** ou order form (pagamento, rescisão, propriedade intelectual, confidencialidade).
- [ ] Processo de **onboarding** do cliente (checklist interno de 1ª semana).

---

## Passo 5 — Produto e suporte

- [ ] Fluxo de **troca de senha** obrigatória após primeiro login (ou política escrita até existir no produto).
- [ ] Canal de suporte definido (e-mail, horário, tempo de resposta esperado).
- [ ] **Observabilidade**: logs de erro da API, alerta se a coleta falhar X vezes seguidas.
- [ ] Manual curto “como correr coleta / exportar / agendar” para o cliente piloto.

---

## Passo 6 — Engenharia (próximas melhorias técnicas)

- [ ] `pip-audit` ou Dependabot + pin de versões em `requirements.txt`.
- [ ] Rate limit em rotas pesadas (`/run`, exportações massivas).
- [ ] Sessões persistidas ou JWT se houver **várias instâncias** da API.
- [ ] Content-Security-Policy (exige reduzir JS/CSS inline no `dashboard.html`).

---

## Passo 7 — Go-to-market

- [ ] Caso de uso / **piloto** com 1 cliente e métricas acordadas (ex.: nº de oportunidades úteis por semana).
- [ ] Página pública de preços ou “falar com vendas” (coerente com GitHub Pages ou site AtlasNex).
- [ ] Material de demo (vitrine + vídeo ou capturas) alinhado ao que o produto **realmente** faz hoje.

---

## Passo 8 — Pré-lançamento (smoke test)

- [ ] Login, coleta por perfil, coleta geral, exportação Excel, e-mail (se contratado), agendamento.
- [ ] Revisão de **URLs** em documentação (túnel Cloudflare só se ainda for estratégia de demo).
- [ ] Lista de contactos de **segurança** (quem reage a incidente).

---

## Registo de conclusão (preencha na equipa)

| Data | Passo | Notas |
|------|-------|-------|
| | | |

---

### Encerramento

Este checklist deve ser **revisto a cada release** relevante. Quando todos os itens críticos dos passos 1–4 estiverem marcados, o produto costuma estar pronto para **primeiro cliente pago ou piloto formal**; os passos 5–8 reduzem risco operacional e de reputação.

*Última atualização: alinhada ao commit que introduz validação `HERMES_ENV=production` no arranque da API.*
