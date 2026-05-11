param(
    [int]$Port = 8000,
    [string]$HostAddress = "127.0.0.1",
    [switch]$PublicTunnel,
    [switch]$CheckOnly
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

$PythonPath = Join-Path $ProjectRoot "venv\Scripts\python.exe"
if (-not (Test-Path $PythonPath)) {
    Write-Host "Ambiente virtual nao encontrado em venv\Scripts\python.exe" -ForegroundColor Red
    Write-Host "Crie o ambiente e instale requirements.txt antes de iniciar a demo."
    exit 1
}

if (-not $env:HERMES_ADMIN_USER) {
    $env:HERMES_ADMIN_USER = "demo"
}

$usingDefaultPassword = $false
if (-not $env:HERMES_ADMIN_PASSWORD) {
    $env:HERMES_ADMIN_PASSWORD = "HermesDemo2026!"
    $usingDefaultPassword = $true
}

if ($PublicTunnel -and $usingDefaultPassword) {
    Write-Host "Para publicar por tunel, defina uma senha propria antes de iniciar:" -ForegroundColor Yellow
    Write-Host '$env:HERMES_ADMIN_PASSWORD="troque-por-uma-senha-forte"'
    Write-Host ".\scripts\start_demo.ps1 -PublicTunnel"
    exit 1
}

$depsCheck = @"
import fastapi
import uvicorn
import openpyxl
import requests
print("deps ok")
"@

try {
    $depsCheck | & $PythonPath -
}
catch {
    Write-Host "Dependencias incompletas. Rode:" -ForegroundColor Red
    Write-Host ".\venv\Scripts\python.exe -m pip install -r requirements.txt"
    exit 1
}

New-Item -ItemType Directory -Force -Path "data" | Out-Null
New-Item -ItemType Directory -Force -Path "output" | Out-Null

$appUrl = "http://${HostAddress}:$Port"
if ($CheckOnly) {
    Write-Host "Demo pronta para iniciar em $appUrl" -ForegroundColor Green
    Write-Host "Usuario: $env:HERMES_ADMIN_USER"
    exit 0
}

Write-Host ""
Write-Host "Hermes Premium - demo operacional" -ForegroundColor Green
Write-Host "URL:      $appUrl"
Write-Host "Usuario: $env:HERMES_ADMIN_USER"
Write-Host "Senha:   $env:HERMES_ADMIN_PASSWORD"
Write-Host ""
Write-Host "Para encerrar a demo, pressione Ctrl+C nesta janela."
if ($PublicTunnel) {
    Write-Host "Modo tunel: mantenha esta janela aberta e aponte o ngrok/Cloudflare Tunnel para $appUrl" -ForegroundColor Yellow
}
Write-Host ""

& $PythonPath -m uvicorn api:app --host $HostAddress --port $Port
