

param(
    [string]$Modo = "",
    [string]$Preset = "",
    [string]$Perfil = "",
    [switch]$ListarPresets,
    [switch]$ListarPerfis,
    [switch]$CriarPerfil,
    [switch]$ColetaTodosPerfis 
    
    # Novo parâmetro para execução via linha de comando
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "🚀 HERMES SYSTEM"

$ErrorActionPreference = "Stop" # Garante que erros sejam tratados como exceções

# ==============================================================================
# CONFIGURAÇÕES DE CAMINHO
# ==============================================================================
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ProjectRoot "venv\Scripts\python.exe"
$PresetFile = Join-Path $ProjectRoot "config\relatorios.json"
$PerfilFile = Join-Path $ProjectRoot "config\perfis_negocio.json"

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

function Clear-HermesFilterEnv {
    # Limpa todas as variáveis de ambiente relacionadas a filtros do Hermes
    $names = @(
        "HERMES_PRESET",
        "HERMES_PERFIL",
        "HERMES_FILTRO_UF",
        "HERMES_FILTRO_KEYWORD",
        "HERMES_FILTRO_RELEVANCIA",
        "HERMES_FILTRO_ALERTA_PRECO",
        "HERMES_FILTRO_TEXTO",
        "HERMES_FILTRO_SCORE_MIN",
        "HERMES_FILTRO_SCORE_MAX",
        "HERMES_FILTRO_VALOR_MIN",
        "HERMES_FILTRO_VALOR_MAX",
        "HERMES_FILTRO_DIAS_MIN",
        "HERMES_FILTRO_DIAS_MAX"
    )

    foreach ($name in $names) {
        Remove-Item "Env:\$name" -ErrorAction SilentlyContinue
    }
}

function Get-HermesPresets {
    # Carrega os presets de relatório do arquivo JSON
    if (-not (Test-Path $PresetFile)) {
        Write-Host "Arquivo de presets não encontrado: $PresetFile" -ForegroundColor Yellow
        return @()
    }

    try {
        $json = Get-Content $PresetFile -Raw -Encoding UTF8 | ConvertFrom-Json
        return $json.PSObject.Properties.Name
    } catch {
        Write-Host "Erro ao ler ou parsear o arquivo de presets: $($_.Exception.Message)" -ForegroundColor Red
        return @()
    }
}

function Get-HermesPerfis {
    # Carrega os perfis de negócio do arquivo JSON
    if (-not (Test-Path $PerfilFile)) {
        Write-Host "Arquivo de perfis não encontrado: $PerfilFile" -ForegroundColor Yellow
        return @()
    }

    try {
        $json = Get-Content $PerfilFile -Raw -Encoding UTF8 | ConvertFrom-Json
        return $json.PSObject.Properties.Name
    } catch {
        Write-Host "Erro ao ler ou parsear o arquivo de perfis: $($_.Exception.Message)" -ForegroundColor Red
        return @()
    }
}

function Show-Presets {
    # Exibe a lista de presets disponíveis
    $presets = Get-HermesPresets
    if ($presets.Count -eq 0) {
        Write-Host "Nenhum preset configurado." -ForegroundColor Yellow
        return
    }

    Write-Host ""
    Write-Host "Presets disponíveis:" -ForegroundColor Cyan
    for ($i = 0; $i -lt $presets.Count; $i++) {
        Write-Host ("  {0,2}. {1}" -f ($i + 1), $presets[$i])
    }
}

function Show-Perfis {
    # Exibe a lista de perfis de negócio disponíveis
    $perfis = Get-HermesPerfis
    if ($perfis.Count -eq 0) {
        Write-Host "Nenhum perfil de negócio configurado." -ForegroundColor Yellow
        return
    }

    Write-Host ""
    Write-Host "Perfis de negócio disponíveis:" -ForegroundColor Cyan
    for ($i = 0; $i -lt $perfis.Count; $i++) {
        Write-Host ("  {0,2}. {1}" -f ($i + 1), $perfis[$i])
    }
}

function Select-Preset {
    # Permite ao usuário selecionar um preset interativamente
    $presets = Get-HermesPresets
    if ($presets.Count -eq 0) {
        return ""
    }

    Show-Presets
    Write-Host ""
    $choice = Read-Host "Digite o número ou o nome do preset"

    $index = 0
    if ([int]::TryParse($choice, [ref]$index)) {
        if ($index -ge 1 -and $index -le $presets.Count) {
            return $presets[$index - 1]
        }
    }

    if ($presets -contains $choice) {
        return $choice
    }

    Write-Host "Preset inválido." -ForegroundColor Yellow
    return ""
}

function Select-Perfil {
    # Permite ao usuário selecionar um perfil interativamente
    $perfis = Get-HermesPerfis
    if ($perfis.Count -eq 0) {
        Write-Host "Nenhum perfil configurado. Usando perfil padrão 'ti_eletro_domesticos'." -ForegroundColor Yellow
        return "ti_eletro_domesticos" # Retorna o padrão se não houver perfis
    }

    Show-Perfis
    Write-Host ""
    $choice = Read-Host "Digite o número ou o nome do perfil (Enter para padrão: ti_eletro_domesticos)"
    if ([string]::IsNullOrWhiteSpace($choice)) {
        return "ti_eletro_domesticos" # Perfil padrão
    }

    $index = 0
    if ([int]::TryParse($choice, [ref]$index)) {
        if ($index -ge 1 -and $index -le $perfis.Count) {
            return $perfis[$index - 1]
        }
    }

    if ($perfis -contains $choice) {
        return $choice
    }

    Write-Host "Perfil inválido. Usando perfil padrão 'ti_eletro_domesticos'." -ForegroundColor Yellow
    return "ti_eletro_domesticos" # Retorna o padrão se a escolha for inválida
}

function Set-HermesPerfil {
    # Define a variável de ambiente HERMES_PERFIL
    param([string]$PerfilName)

    if (-not [string]::IsNullOrWhiteSpace($PerfilName)) {
        $env:HERMES_PERFIL = $PerfilName
    }
}

function Invoke-Hermes {
    # Define o caminho completo para o python.exe dentro do venv
    $venvPythonPath = Join-Path $ProjectRoot "venv\Scripts\python.exe"

    if (-not (Test-Path $venvPythonPath)) {
        throw "Python do venv não encontrado em: $venvPythonPath. Verifique se o ambiente virtual está configurado corretamente."
    }

    Write-Host "`n=== INICIANDO PROJETO HERMES ===`n" -ForegroundColor Green
    Write-Host "Tentando executar Python em: $venvPythonPath" -ForegroundColor DarkGray # DEBUG LINE

    # Garante que o script Python seja executado a partir da raiz do projeto
    Set-Location $ProjectRoot

    # Tenta ativar o ambiente virtual explicitamente antes de chamar o python
    # Isso pode ajudar a configurar variáveis de ambiente que o Python espera
    $activateScript = Join-Path $ProjectRoot "venv\Scripts\Activate.ps1"
    if (Test-Path $activateScript) {
        Write-Host "Ativando ambiente virtual: $activateScript" -ForegroundColor DarkGray # DEBUG LINE
        . $activateScript # Usa dot-sourcing para ativar na sessão atual
    } else {
        Write-Host "Script de ativação do venv não encontrado: $activateScript" -ForegroundColor Yellow
    }

    # Executa o script Python usando o caminho completo para o executável do venv
    & $venvPythonPath -m src.main
    Write-Host "`n=== EXECUÇÃO DO HERMES CONCLUÍDA ===`n" -ForegroundColor Green
}

function Read-OptionalEnv {
    # Função auxiliar para ler variáveis de ambiente opcionais
    param(
        [string]$Prompt,
        [string]$EnvName
    )

    $value = Read-Host $Prompt
    if (-not [string]::IsNullOrWhiteSpace($value)) {
        Set-Item "Env:\$EnvName" $value
    }
}

function Start-ReportPreset {
    param(
        [string]$PresetName,
        [string]$PerfilName
    )

    Clear-HermesFilterEnv
    $env:HERMES_MODO = "relatorio"
    $env:HERMES_ENVIAR_EMAIL = "0" # Mantido como 0 para relatórios interativos
    $env:HERMES_LIMITE_LICITACOES = "600"
    $env:HERMES_PRESET = $PresetName
    Set-HermesPerfil -PerfilName $PerfilName
    Invoke-Hermes
}

function Start-ManualReport {
    param([string]$PerfilName)

    Clear-HermesFilterEnv
    $env:HERMES_MODO = "relatorio"
    $env:HERMES_ENVIAR_EMAIL = "0" # Mantido como 0 para relatórios interativos
    $env:HERMES_LIMITE_LICITACOES = "600"
    Set-HermesPerfil -PerfilName $PerfilName

    Write-Host ""
    Write-Host "Filtros manuais. Pressione Enter para deixar vazio." -ForegroundColor Cyan
    Read-OptionalEnv "UFs (ex: SP,RJ,MG)" "HERMES_FILTRO_UF"
    Read-OptionalEnv "Keywords (ex: notebook,computador,impressora)" "HERMES_FILTRO_KEYWORD"
    Read-OptionalEnv "Score mínimo (ex: 75)" "HERMES_FILTRO_SCORE_MIN"
    Read-OptionalEnv "Valor mínimo (ex: 50000)" "HERMES_FILTRO_VALOR_MIN"
    Read-OptionalEnv "Dias máximo (ex: 60)" "HERMES_FILTRO_DIAS_MAX"
    Read-OptionalEnv "Texto livre no objeto/órgão/município" "HERMES_FILTRO_TEXTO"

    Invoke-Hermes
}

function Start-Collection {
    param([string]$PerfilName)

    Clear-HermesFilterEnv
    $env:HERMES_MODO = "coleta"
    $env:HERMES_ENVIAR_EMAIL = "1" # Habilitado para envio de e-mail na coleta
    $env:HERMES_MAX_PAGES_PER_ENDPOINT = "20"
    $env:HERMES_MAX_RUNTIME_MINUTES = "20"
    $env:HERMES_LIMITE_LICITACOES = "600"
    Set-HermesPerfil -PerfilName $PerfilName
    Invoke-Hermes
}

function Start-CollectionForAllPerfis {
    Write-Host "`n=== INICIANDO COLETA PARA TODOS OS PERFIS ===`n" -ForegroundColor Green
    $allPerfis = Get-HermesPerfis

    if ($allPerfis.Count -eq 0) {
        Write-Host "Nenhum perfil de negócio configurado. Nenhuma coleta será realizada." -ForegroundColor Yellow
        return
    }

    foreach ($perfilName in $allPerfis) {
        Write-Host "`n--- Iniciando coleta para o perfil: '$perfilName' ---`n" -ForegroundColor Cyan
        try {
            # Chama a função Start-Collection para cada perfil
            Start-Collection -PerfilName $perfilName
            Write-Host "`n--- Coleta para o perfil '$perfilName' CONCLUÍDA ---`n" -ForegroundColor Green
        } catch {
            Write-Host "`n--- ERRO na coleta para o perfil '$perfilName': $($_.Exception.Message) ---`n" -ForegroundColor Red
        }
    }
    Write-Host "`n=== COLETA PARA TODOS OS PERFIS FINALIZADA ===`n" -ForegroundColor Green
}

# ==============================================================================
# FUNÇÕES DO ASSISTENTE DE CRIAÇÃO DE PERFIL
# ==============================================================================

function Read-CommaSeparatedList {
    # Função auxiliar para ler listas de strings separadas por vírgula
    param(
        [string]$Prompt
    )
    $input = Read-Host $Prompt
    if ([string]::IsNullOrWhiteSpace($input)) {
        return @()
    }
    return ($input -split ',' | ForEach-Object { $_.Trim() } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
}

function Read-NumericInput {
    # Função auxiliar para ler valores numéricos com padrão
    param(
        [string]$Prompt,
        [int]$DefaultValue
    )
    $value = Read-Host "$Prompt (Padrão: $DefaultValue)"
    $num = 0
    if ([string]::IsNullOrWhiteSpace($value)) {
        return $DefaultValue
    } elseif ([int]::TryParse($value, [ref]$num)) {
        return $num
    } else {
        Write-Host "Valor inválido. Usando padrão: $DefaultValue" -ForegroundColor Yellow
        return $DefaultValue
    }
}

function CriarNovoPerfil {
    # Assistente interativo para criar um novo perfil de negócio
    Write-Host "`n=== ASSISTENTE DE CRIAÇÃO DE NOVO PERFIL ===`n" -ForegroundColor Green
    Write-Host "Preencha as informações para o novo perfil de negócio."

    # 1. ID do Perfil
    $profileId = ""
    while ([string]::IsNullOrWhiteSpace($profileId)) {
        $profileId = Read-Host "Digite um ID único para o perfil (ex: 'saude_hospitalar', use letras minúsculas e underscores)"
        if ([string]::IsNullOrWhiteSpace($profileId)) {
            Write-Host "O ID do perfil não pode ser vazio." -ForegroundColor Red
        } elseif ($profileId -match "[^a-z0-9_]") {
            Write-Host "O ID do perfil deve conter apenas letras minúsculas, números e underscores." -ForegroundColor Red
            $profileId = ""
        } elseif ((Get-HermesPerfis) -contains $profileId) {
            Write-Host "Já existe um perfil com este ID. Escolha outro." -ForegroundColor Red
            $profileId = ""
        }
    }

    # 2. Nome de Exibição
    $nomeExibicao = ""
    while ([string]::IsNullOrWhiteSpace($nomeExibicao)) {
        $nomeExibicao = Read-Host "Digite o nome de exibição do perfil (ex: 'Saúde e Hospitalar')"
        if ([string]::IsNullOrWhiteSpace($nomeExibicao)) {
            Write-Host "O nome de exibição não pode ser vazio." -ForegroundColor Red
        }
    }

    # 3. Descrição
    $descricao = Read-Host "Digite uma breve descrição para o perfil"

    # 4. Keywords
    $keywords = Read-CommaSeparatedList "Keywords gerais (separadas por vírgula, ex: 'medicamento,hospital,saude')"
    $keywordsFortes = Read-CommaSeparatedList "Keywords fortes (separadas por vírgula, mais peso no score)"
    $termosPositivos = Read-CommaSeparatedList "Termos positivos (separadas por vírgula, aumentam o score)"
    $termosNegativos = Read-CommaSeparatedList "Termos negativos (separadas por vírgula, diminuem o score)"
    $modalidadesPrioritarias = Read-CommaSeparatedList "Modalidades prioritárias (separadas por vírgula, ex: 'pregão,concorrência')"

    # 5. Valores de Interesse
    $valorMinimo = Read-NumericInput "Valor mínimo de interesse" 20000
    $valorAtrativo = Read-NumericInput "Valor atrativo" 50000
    $valorMuitoAtrativo = Read-NumericInput "Valor muito atrativo" 200000

    # 6. Scores de Relevância
    $scoreMedia = Read-NumericInput "Score mínimo para relevância 'Média'" 50
    $scoreAlta = Read-NumericInput "Score mínimo para relevância 'Alta'" 75

    # Constrói o novo perfil
    $newProfile = @{
        "nome_exibicao" = $nomeExibicao;
        "descricao" = $descricao;
        "keywords" = $keywords;
        "keywords_fortes" = $keywordsFortes;
        "termos_positivos" = $termosPositivos;
        "termos_negativos" = $termosNegativos;
        "modalidades_prioritarias" = $modalidadesPrioritarias;
        "valor_minimo_interesse" = $valorMinimo;
        "valor_atrativo" = $valorAtrativo;
        "valor_muito_atrativo" = $valorMuitoAtrativo;
        "score_relevancia_media" = $scoreMedia;
        "score_relevancia_alta" = $scoreAlta
    }

    # Carrega perfis existentes e adiciona o novo
    $existingPerfis = @{}
    if (Test-Path $PerfilFile) {
        try {
            $jsonContent = Get-Content $PerfilFile -Raw -Encoding UTF8 | ConvertFrom-Json
            $jsonContent.PSObject.Properties | ForEach-Object {
                $existingPerfis[$_.Name] = $_.Value
            }
        } catch {
            Write-Host "Erro ao ler perfis existentes. Criando novo arquivo: $($_.Exception.Message)" -ForegroundColor Yellow
        }
    }

    # Adiciona o novo perfil
    $existingPerfis[$profileId] = $newProfile

    # Salva de volta no arquivo usando o método .NET para garantir UTF-8 sem BOM
    try {
        $jsonString = $existingPerfis | ConvertTo-Json -Depth 100 -Compress
        [System.IO.File]::WriteAllText($PerfilFile, $jsonString, [System.Text.Encoding]::UTF8)
        Write-Host "`nPerfil '$profileId' criado e salvo com sucesso em $PerfilFile`n" -ForegroundColor Green
    } catch {
        Write-Host "`nERRO: Falha ao salvar o perfil '$profileId': $($_.Exception.Message)`n" -ForegroundColor Red
    }
}

# ==============================================================================
# MENU PRINCIPAL E LÓGICA DE EXECUÇÃO
# ==============================================================================

function Show-MainMenu {
    # Exibe o menu principal de opções
    Write-Host "`n=== PROJETO HERMES ===" -ForegroundColor Cyan
    Write-Host "1. Gerar relatório por preset"
    Write-Host "2. Gerar relatório com filtros manuais"
    Write-Host "3. Rodar coleta PNCP normal (para um perfil)"
    Write-Host "4. Rodar coleta PNCP para TODOS os perfis" # Nova opção
    Write-Host "5. Listar presets"
    Write-Host "6. Listar perfis de negócio"
    Write-Host "7. Criar novo perfil de negócio"
    Write-Host "0. Sair"
    Write-Host ""
}

# Lógica para execução via parâmetros de linha de comando
if ($PSBoundParameters.ContainsKey('Modo') -or $PSBoundParameters.ContainsKey('ListarPresets') -or $PSBoundParameters.ContainsKey('ListarPerfis') -or $PSBoundParameters.ContainsKey('CriarPerfil') -or $PSBoundParameters.ContainsKey('ColetaTodosPerfis')) {
    if ($ListarPresets) {
        Show-Presets
        exit 0
    } elseif ($ListarPerfis) {
        Show-Perfis
        exit 0
    } elseif ($CriarPerfil) {
        CriarNovoPerfil
        exit 0
    } elseif ($ColetaTodosPerfis) { # Novo bloco para o parâmetro
        Start-CollectionForAllPerfis
        exit 0
    } elseif ($PSBoundParameters.ContainsKey('Modo')) {
        # Execução direta via parâmetros de modo
        $currentPerfil = $Perfil
        if ([string]::IsNullOrWhiteSpace($currentPerfil)) {
            $currentPerfil = "ti_eletro_domesticos" # Perfil padrão se não especificado
        }

        switch ($Modo.ToLower()) {
            "relatorio" {
                if ([string]::IsNullOrWhiteSpace($Preset)) {
                    Write-Host "Para o modo 'relatorio' via parâmetro, o preset (-Preset) é obrigatório." -ForegroundColor Red
                    exit 1
                }
                Start-ReportPreset -PresetName $Preset -PerfilName $currentPerfil
            }
            "manual" {
                Write-Host "Modo 'manual' via parâmetro não suporta filtros interativos. Use o menu." -ForegroundColor Red
                exit 1
            }
            "coleta" {
                Start-Collection -PerfilName $currentPerfil
            }
            default {
                Write-Host "Modo inválido especificado via parâmetro: $Modo" -ForegroundColor Red
                exit 1
            }
        }
    }
} else {
    # Execução interativa via menu se nenhum parâmetro de modo foi fornecido
    while ($true) {
        Show-MainMenu
        $option = Read-Host "Escolha uma opção"

        switch ($option) {
            "1" { # Gerar relatório por preset
                $selectedPerfil = Select-Perfil
                $selectedPreset = Select-Preset
                if ($selectedPreset) {
                    Start-ReportPreset -PresetName $selectedPreset -PerfilName $selectedPerfil
                }
            }
            "2" { # Gerar relatório com filtros manuais
                $selectedPerfil = Select-Perfil
                Start-ManualReport -PerfilName $selectedPerfil
            }
            "3" { # Rodar coleta PNCP normal (para um perfil)
                $selectedPerfil = Select-Perfil
                Start-Collection -PerfilName $selectedPerfil
            }
            "4" { # Rodar coleta PNCP para TODOS os perfis
                Start-CollectionForAllPerfis
            }
            "5" { # Listar presets
                Show-Presets
            }
            "6" { # Listar perfis de negócio
                Show-Perfis
            }
            "7" { # Criar novo perfil de negócio
                CriarNovoPerfil
            }
            "0" { # Sair
                Write-Host "Obrigado por usar o Projeto Hermes. Até mais!" -ForegroundColor Green
                exit
            }
            default {
                Write-Host "Opção inválida. Tente novamente." -ForegroundColor Red
            }
        }
        Read-Host "Pressione Enter para continuar..." | Out-Null
    }
}