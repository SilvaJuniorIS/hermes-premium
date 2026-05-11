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

1. Abra a tela de oportunidades e mostre os indicadores do topo.
2. Filtre por perfil, estado, classificacao e texto.
3. Abra o detalhe de uma oportunidade com score alto.
4. Mostre os motivos do score, valor estimado e link da fonte.
5. Exporte CSV ou Excel.
6. Abra historico para mostrar recorrencia operacional.
7. Abra agendamento para demonstrar automacao diaria.

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
