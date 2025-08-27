# ========================================
#    AUTOMACAO VR/VA - SETUP POWERSHELL
# ========================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    AUTOMACAO VR/VA - SETUP POWERSHELL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Função para verificar se um comando existe
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# 1. Verificar Python
Write-Host "[1/5] Verificando Python..." -ForegroundColor Yellow
if (Test-Command "python") {
    $pythonVersion = python --version 2>&1
    Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "ERRO: Python não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, instale o Python 3.8+ de https://python.org" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# 2. Verificar Ollama
Write-Host "[2/5] Verificando Ollama..." -ForegroundColor Yellow
if (Test-Command "ollama") {
    $ollamaVersion = ollama --version
    Write-Host "Ollama encontrado: $ollamaVersion" -ForegroundColor Green
} else {
    Write-Host "AVISO: Ollama não encontrado!" -ForegroundColor Yellow
    Write-Host "Instalando Ollama..." -ForegroundColor Yellow
    
    try {
        # Tenta instalar via winget
        if (Test-Command "winget") {
            Write-Host "Instalando via winget..." -ForegroundColor Cyan
            winget install Ollama.Ollama
        } else {
            # Tenta instalar via Chocolatey
            if (Test-Command "choco") {
                Write-Host "Instalando via Chocolatey..." -ForegroundColor Cyan
                choco install ollama
            } else {
                Write-Host "ERRO: Nenhum gerenciador de pacotes encontrado!" -ForegroundColor Red
                Write-Host "Instale manualmente de https://ollama.ai/download" -ForegroundColor Red
                Read-Host "Pressione Enter para sair"
                exit 1
            }
        }
        
        # Aguarda instalação
        Start-Sleep -Seconds 5
        
        # Verifica se foi instalado
        if (Test-Command "ollama") {
            Write-Host "Ollama instalado com sucesso!" -ForegroundColor Green
        } else {
            throw "Falha na verificação pós-instalação"
        }
    } catch {
        Write-Host "ERRO: Falha na instalação do Ollama" -ForegroundColor Red
        Write-Host "Instale manualmente de https://ollama.ai/download" -ForegroundColor Red
        Read-Host "Pressione Enter para sair"
        exit 1
    }
}

Write-Host ""

# 3. Baixar modelo Gemma3
Write-Host "[3/5] Baixando modelo Gemma3..." -ForegroundColor Yellow
try {
    Write-Host "Isso pode demorar alguns minutos..." -ForegroundColor Cyan
    ollama pull gemma3
    Write-Host "Modelo Gemma3 baixado com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "ERRO: Falha no download do modelo Gemma3" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# 4. Instalar dependências Python
Write-Host "[4/5] Instalando dependências Python..." -ForegroundColor Yellow
try {
    pip install -r requiremts.txt
    Write-Host "Dependências instaladas com sucesso!" -ForegroundColor Green
} catch {
    Write-Host "ERRO: Falha na instalação das dependências" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# 5. Configuração concluída
Write-Host "[5/5] Configuração concluída!" -ForegroundColor Green
Write-Host ""

# Verificar arquivos Excel
Write-Host "Verificando arquivos de dados..." -ForegroundColor Cyan
$excelFiles = @(
    "ATIVOS.xlsx",
    "FÉRIAS.xlsx", 
    "DESLIGADOS.xlsx",
    "ADMISSÃO ABRIL.xlsx",
    "Base sindicato x valor.xlsx",
    "Base dias uteis.xlsx",
    "AFASTAMENTOS.xlsx",
    "EXTERIOR.xlsx",
    "ESTÁGIO.xlsx",
    "APRENDIZ.xlsx"
)

$missingFiles = @()
foreach ($file in $excelFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file" -ForegroundColor Red
        $missingFiles += $file
    }
}

Write-Host ""

if ($missingFiles.Count -gt 0) {
    Write-Host "AVISO: Alguns arquivos estão faltando!" -ForegroundColor Yellow
    Write-Host "Arquivos faltando: $($missingFiles -join ', ')" -ForegroundColor Yellow
    Write-Host ""
}

# Instruções finais
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "           INSTRUÇÕES DE USO" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para executar a aplicação:" -ForegroundColor White
Write-Host "1. Inicie o Ollama: ollama serve" -ForegroundColor Yellow
Write-Host "2. Execute: streamlit run app.py" -ForegroundColor Yellow
Write-Host "3. Acesse: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""

# Pergunta se quer iniciar agora
$startNow = Read-Host "Deseja iniciar a aplicação agora? (s/n)"
if ($startNow -eq "s" -or $startNow -eq "S" -or $startNow -eq "sim" -or $startNow -eq "SIM") {
    Write-Host "Iniciando Ollama..." -ForegroundColor Cyan
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Minimized
    
    Write-Host "Aguardando Ollama inicializar..." -ForegroundColor Cyan
    Start-Sleep -Seconds 10
    
    Write-Host "Iniciando aplicação..." -ForegroundColor Cyan
    streamlit run app.py
} else {
    Write-Host "Configuração concluída! Execute manualmente quando desejar." -ForegroundColor Green
}

Read-Host "Pressione Enter para sair" 