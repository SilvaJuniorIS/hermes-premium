# Instalacao do Backup - Projeto Hermes Premium

Este pacote contem uma copia do Projeto Hermes Premium pronta para instalar em outro computador Windows.

## Requisitos

- Python 3.10 ou superior
- PowerShell
- Internet para instalar dependencias e consultar o PNCP

## Passo a passo

1. Extraia o arquivo ZIP em uma pasta, por exemplo:

```powershell
C:\Projeto_Hermes_Premium
```

2. Entre na pasta do projeto:

```powershell
cd C:\Projeto_Hermes_Premium
```

3. Crie um ambiente virtual:

```powershell
python -m venv venv
```

4. Ative o ambiente virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

5. Instale as dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

6. Inicie a API e o dashboard:

```powershell
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

7. Abra no navegador:

```text
http://127.0.0.1:8000
```

## Rodar coleta pelo terminal

```powershell
python -m src.main
```

## Dashboard Streamlit opcional

```powershell
streamlit run dashboard.py
```

## Observacoes importantes

- O banco principal fica em `data/hermes.sqlite3`.
- O ambiente virtual `venv` nao vai no backup; ele deve ser recriado no novo computador.
- A pasta `.git` tambem nao vai no backup.
- Se o PowerShell bloquear a ativacao do ambiente virtual, rode:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Depois tente ativar o ambiente novamente.

## Seguranca

Antes de usar envio de e-mail ou WhatsApp, revise `src/notifier.py` e mova credenciais para variaveis de ambiente. Nao deixe senhas dentro do codigo em uma instalacao de producao.
