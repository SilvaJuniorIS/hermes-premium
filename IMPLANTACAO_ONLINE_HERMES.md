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

Exemplo conceitual:

```powershell
python -m uvicorn api:app --host 127.0.0.1 --port 8000
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

## Resumo

- GitHub Pages: ideal para a demo publica.
- Sistema real: precisa de backend hospedado.
- Logo da demo: salvar em `docs/assets/logo-hermes.png`.

