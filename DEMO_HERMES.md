# Demo operacional do Hermes Premium

Este roteiro sobe a versao real do Hermes: FastAPI, dashboard com login, banco SQLite, perfis, historico, agendamento e exportacao.

## Iniciar localmente

1. De duplo clique em `INICIAR_DEMO_HERMES.bat`.
2. Abra `http://127.0.0.1:8000`.
3. Entre com:
   - Usuario: `demo`
   - Senha: `HermesDemo2026!`

O usuario `demo` e criado automaticamente no primeiro acesso quando o banco ainda nao tiver esse usuario.

## Demo com tunel publico temporario

Antes de usar ngrok ou Cloudflare Tunnel, defina uma senha propria:

```powershell
$env:HERMES_ADMIN_USER="demo"
$env:HERMES_ADMIN_PASSWORD="troque-por-uma-senha-forte"
.\scripts\start_demo.ps1 -PublicTunnel
```

Depois aponte o tunel para:

```text
http://127.0.0.1:8000
```

Use esse modo apenas em apresentacoes acompanhadas e encerre o tunel ao final.

## Roteiro de apresentacao

Antes da apresentacao, se a coleta real nao tiver oportunidades fortes, carregue a base demonstrativa:

```powershell
.\venv\Scripts\python.exe scripts\seed_demo_data.py
```

1. Abra a tela de oportunidades e mostre os indicadores do topo.
2. Comece por uma oportunidade de alta prioridade e maior valor.
3. Abra o detalhe e explique a acao recomendada, janela comercial e origem.
4. Marque status comercial, favorito e anotacoes internas para mostrar acompanhamento.
5. Mostre objeto, orgao, municipio, valor estimado, motivos do score e link da fonte.
6. Mostre que o filtro padrao prioriza `Abertura futura` e que licitacoes vencidas ficam separadas.
7. Filtre por perfil, estado, classificacao, status comercial, favoritos e texto.
8. Exporte CSV ou Excel para provar que o dado sai do Hermes para analise.
9. Use `Enviar por e-mail` para solicitar o destinatario e enviar a planilha com texto explicativo sobre oportunidades e score.
10. Abra historico para mostrar recorrencia operacional.
11. Abra agendamento para demonstrar automacao diaria.

## Priorizacao por prazo

Por padrao, o dashboard usa o filtro `Abertura futura`. Isso evita que oportunidades ja vencidas aparecam no topo da apresentacao.

Opcoes do filtro:

- `Abertura futura`: mostra apenas oportunidades que ainda podem ser trabalhadas.
- `Todas as datas`: mostra futuras primeiro e vencidas depois.
- `Ja passaram`: mostra somente oportunidades vencidas para analise historica.

As exportacoes e o envio por e-mail respeitam o filtro de prazo selecionado.

## Acompanhamento comercial

No detalhe da oportunidade, o Hermes permite registrar:

- status comercial: `Novo`, `Em analise`, `Proposta`, `Monitorar` ou `Descartado`;
- favorito;
- anotacoes internas.

Esses campos ajudam a transformar a lista de editais em funil de trabalho. Eles tambem entram nas exportacoes CSV/Excel e podem ser usados nos filtros da tela.

## Envio de planilha por e-mail

Na tela de oportunidades:

1. Ajuste os filtros desejados.
2. Clique em `Enviar por e-mail`.
3. Informe o e-mail do destinatario.
4. O Hermes gera a planilha Excel com os filtros atuais.
5. O sistema envia o anexo com um texto explicando:
   - total de oportunidades;
   - filtros usados;
   - como interpretar o score;
   - oportunidades em destaque;
   - recomendacao de leitura comercial.

O envio usa `src/notifier.py`. Por padrao, ele reaproveita a configuracao SMTP existente. Em ambiente mais controlado, use variaveis de ambiente:

```powershell
$env:HERMES_SMTP_HOST="smtp.gmail.com"
$env:HERMES_SMTP_PORT="465"
$env:HERMES_SMTP_USER="seu-email@gmail.com"
$env:HERMES_SMTP_PASSWORD="sua-senha-de-app"
$env:HERMES_EMAIL_FROM="seu-email@gmail.com"
```

## Comandos uteis

Rodar em outra porta:

```powershell
.\scripts\start_demo.ps1 -Port 8001
```

Checar dependencias sem abrir o servidor:

```powershell
.\scripts\start_demo.ps1 -CheckOnly
```

Permitir acesso na rede local:

```powershell
.\scripts\start_demo.ps1 -HostAddress 0.0.0.0
```

Ao usar `0.0.0.0`, acesse pelo IP da maquina na rede.
