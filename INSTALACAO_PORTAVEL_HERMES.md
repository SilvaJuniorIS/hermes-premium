# Hermes Premium - Instalacao e uso portavel

Este pacote permite instalar o Hermes Premium em outro computador Windows ou rodar a partir de um pendrive.

## Modo mais simples

1. Extraia o ZIP em uma pasta ou no pendrive.
2. Entre na pasta extraida.
3. Execute `INICIAR_HERMES_PORTAVEL.bat`.
4. Aguarde a criacao do ambiente virtual e a instalacao das dependencias.
5. Acesse `http://127.0.0.1:8000`.

Login inicial:

```text
usuario: admin
senha: admin123
```

## Requisitos

- Windows.
- Python 3.10 ou superior instalado.
- Internet na primeira execucao para instalar dependencias.
- Internet nas coletas para consultar o PNCP.

## Rodar direto do pendrive

E possivel rodar direto do pendrive, desde que o computador tenha Python instalado. Na primeira execucao, o script cria a pasta `venv` dentro do proprio pendrive e instala as dependencias ali.

Observacao: a primeira execucao pode demorar. Depois disso, o sistema abre mais rapido.

## Arquivos importantes

- `api.py`: API e dashboard web principal.
- `dashboard.html`: interface web.
- `dashboard.py`: dashboard Streamlit opcional.
- `src/`: codigo principal de coleta, banco e regras.
- `config/perfis_negocio.json`: perfis de busca.
- `data/hermes.sqlite3`: banco principal atual.
- `output/`: relatorios gerados.
- `requirements.txt`: dependencias Python.

## Comandos manuais

Criar ambiente virtual:

```powershell
python -m venv venv
```

Ativar:

```powershell
.\venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Iniciar API:

```powershell
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

Dashboard Streamlit opcional:

```powershell
streamlit run dashboard.py
```

## Observacoes

- O backup nao inclui `venv`, `.git`, caches Python nem backups ZIP antigos.
- O banco atual foi incluido em `data/hermes.sqlite3`.
- Se a porta 8000 estiver ocupada, rode manualmente em outra porta:

```powershell
python -m uvicorn api:app --host 127.0.0.1 --port 8001
```

