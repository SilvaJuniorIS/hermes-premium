@echo off
:: ============================================================
::  PROJETO HERMES - Execução Automática Diária
::  Ativa o ambiente virtual e executa o robô de licitações
:: ============================================================

:: Define o diretório raiz do projeto
cd /d "C:\Users\usu_compras12\OneDrive\Aulas Python\Projeto_Hermes_TI"

:: Ativa o ambiente virtual
call venv\Scripts\activate.bat

:: Executa o projeto
python -m src.main

:: Após a execução, identifica o último arquivo gerado em "output"
for /f "delims=" %%F in ('dir /b /a-d /o-d "output\licitacoes_projeto_hermes_*.xlsx"') do (
    set "LAST_REPORT=output\%%F"
    goto found_report
)

:found_report
if not defined LAST_REPORT (
    echo Nenhum relatório encontrado para envio em %date% %time% >> logs\execucao.log
    goto end
)

:: Envia o relatório por e-mail usando script Python
python send_report.py "%LAST_REPORT%"

:: Registra log de execução
echo Hermes executado e relatório enviado (%LAST_REPORT%) em %date% %time% >> logs\execucao.log

:end
:: Desativa o ambiente virtual
deactivate