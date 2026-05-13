# Checklist de comercialização — Hermes Premium

Use este ficheiro como **lista de trabalho**: marque `[x]` quando cada item estiver concluído. A ordem reflete dependências típicas (segurança e jurídico antes de escalar vendas).

**Documentos relacionados:** [BLINDAGEM_E_COMERCIALIZACAO.md](BLINDAGEM_E_COMERCIALIZACAO.md) · [`.env.example`](../.env.example)

---

## Passo 1 — Segurança operacional e segredos

*Parte deste passo está automatizada no código: com `HERMES_ENV=production`, a API **não arranca** se a configuração mínima de produção for inválida (`api.py`).*

- [x] **(Código)** Validação no arranque quando `HERMES_ENV=production` (senha forte obrigatória, cookie seguro, sem dica de login de desenvolvimento).
- [ ] **Revogar** no fornecedor (Google, etc.) qualquer palavra-passe de aplicação ou chave que tenha existido em commits antigos do repositório.
- [ ] Copiar [`.env.example`](../.env.example) para `.env` na raiz do projeto e preencher apenas o necessário (nunca commitar `.env`).
- [ ] Definir **`HERMES_ADMIN_PASSWORD`** com senha forte antes de expor o serviço à Internet.
- [ ] Em servidor público com HTTPS: `HERMES_ENV=production`, `HERMES_COOKIE_SECURE=true`, **sem** `HERMES_DEV_LOGIN_HINT` (ou `false`).
- [ ] Confirmar que o processo **sobe** com essas variáveis (`uvicorn api:app`) e que **falha de propósito** se remover a senha ou deixar `admin123` em produção (teste local de validação).
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
