# Implantacao online do Hermes Premium

O endereco do GitHub Pages serve para publicar a demonstracao estatica em `docs/`.

O sistema real que esta funcionando localmente usa:

- FastAPI em `api.py`;
- banco SQLite em `data/hermes.sqlite3`;
- autenticacao por cookie;
- chamadas externas ao PNCP;
- rotinas Python de coleta e scoring.

Por isso, ele nao roda diretamente no GitHub Pages. GitHub Pages hospeda apenas HTML, CSS, JavaScript e arquivos estaticos.

## Caminho recomendado agora

1. Use o GitHub Pages como vitrine publica:
   - `docs/index.html`
   - dados ficticios
   - logo em `docs/assets/logo-hermes.png`

2. Use um servidor separado para a versao real:
   - VPS Windows ou Linux;
   - Render, Railway, Fly.io, Azure, AWS ou similar;
   - servidor local com acesso por VPN ou dominio proprio.

3. Aponte um botao da vitrine para a versao real quando ela estiver hospedada:

```html
<a href="https://app.seudominio.com">Acessar sistema</a>
```

## Opcao simples para demonstracao real

Para uma demonstracao controlada, rode o sistema em uma maquina Windows e use um tunel seguro temporario, como Cloudflare Tunnel ou ngrok.

O projeto agora inclui um inicializador de demo:

```powershell
.\scripts\start_demo.ps1
```

Ou, no Windows, de duplo clique em:

```text
INICIAR_DEMO_HERMES.bat
```

Credenciais locais padrao da demo:

- Usuario: `demo`
- Senha: `HermesDemo2026!`

Para publicar temporariamente por tunel, defina uma senha propria antes:

```powershell
$env:HERMES_ADMIN_USER="demo"
$env:HERMES_ADMIN_PASSWORD="troque-por-uma-senha-forte"
.\scripts\start_demo.ps1 -PublicTunnel
```

Depois o tunel publica uma URL HTTPS temporaria apontando para `http://127.0.0.1:8000`.

Use esse caminho apenas para demonstracoes acompanhadas, porque o sistema tem login e banco local.

## Opcao de producao

Para colocar o Hermes real online de forma profissional:

1. Criar servidor Linux ou Windows.
2. Instalar Python 3.10+.
3. Copiar o projeto sem `venv`, `.git`, caches e backups antigos.
4. Criar ambiente virtual.
5. Instalar `requirements.txt`.
6. Definir usuario e senha por variaveis de ambiente:

```powershell
$env:HERMES_ADMIN_USER="admin"
$env:HERMES_ADMIN_PASSWORD="uma-senha-forte"
```

7. Rodar a API com Uvicorn/Gunicorn ou servico do sistema.
8. Colocar proxy HTTPS na frente, como Nginx, Caddy ou IIS.
9. Configurar backup do banco `data/hermes.sqlite3`.

## Checklist para demo vendavel

Antes de apresentar o Hermes para um cliente ou socio, use este roteiro:

1. Rodar uma coleta recente para 2 ou 3 perfis comerciais fortes.
2. Conferir o dashboard em `http://127.0.0.1:8000`.
3. Abrir uma oportunidade de alta prioridade e mostrar:
   - objeto da licitacao;
   - orgao e municipio;
   - valor estimado;
   - motivo do score;
   - link da fonte.
4. Mostrar filtros por classe, estado e texto.
5. Exportar CSV para provar que o dado sai do sistema para analise comercial.
6. Abrir o historico de coletas para demonstrar recorrencia operacional.
7. Mostrar o agendamento diario como rotina automatizada.

## Caminho recomendado para primeira demo online

Para uma demonstracao acompanhada, o caminho mais rapido e controlado e:

1. Manter o Hermes rodando localmente:

```powershell
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

2. Publicar temporariamente com Cloudflare Tunnel ou ngrok.
3. Usar uma senha forte definida por variavel de ambiente.
4. Levar somente uma base de demonstracao, sem dados sensiveis de clientes.
5. Desativar o tunel ao final da apresentacao.

Esse formato evita custo inicial de servidor e permite validar a proposta comercial antes de contratar infraestrutura.

## Caminho recomendado para piloto

Quando houver cliente piloto, avance para hospedagem real:

1. VPS pequena ou plataforma como Render, Railway, Fly.io, Azure ou AWS.
2. HTTPS obrigatorio.
3. Variaveis `HERMES_ADMIN_USER` e `HERMES_ADMIN_PASSWORD`.
4. Backup automatico de `data/hermes.sqlite3`.
5. Processo de atualizacao via Git.
6. Agendamento diario ligado no proprio backend ou em um job externo.
7. Monitoramento simples de erro e disponibilidade.

## Resumo

- GitHub Pages: ideal para a demo publica.
- Sistema real: precisa de backend hospedado.
- Logo da demo: salvar em `docs/assets/logo-hermes.png`.
