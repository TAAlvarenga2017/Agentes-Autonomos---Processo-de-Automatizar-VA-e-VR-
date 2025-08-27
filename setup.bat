@echo off
echo ========================================
echo    AUTOMACAO VR/VA - SETUP WINDOWS
echo ========================================
echo.

echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.8+ de https://python.org
    pause
    exit /b 1
)
echo Python encontrado!

echo.
echo [2/5] Verificando Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo AVISO: Ollama nao encontrado!
    echo Instalando Ollama...
    winget install Ollama.Ollama
    if errorlevel 1 (
        echo ERRO: Falha na instalacao do Ollama
        echo Instale manualmente de https://ollama.ai/download
        pause
        exit /b 1
    )
    echo Ollama instalado com sucesso!
) else (
    echo Ollama encontrado!
)

echo.
echo [3/5] Baixando modelo Gemma3...
ollama pull gemma3
if errorlevel 1 (
    echo ERRO: Falha no download do modelo Gemma3
    pause
    exit /b 1
)
echo Modelo Gemma3 baixado com sucesso!

echo.
echo [4/5] Instalando dependencias Python...
pip install -r requiremts.txt
if errorlevel 1 (
    echo ERRO: Falha na instalacao das dependencias
    pause
    exit /b 1
)
echo Dependencias instaladas com sucesso!

echo.
echo [5/5] Configuracao concluida!
echo.
echo Para executar a aplicacao:
echo 1. Inicie o Ollama: ollama serve
echo 2. Execute: streamlit run app.py
echo 3. Acesse: http://localhost:8501
echo.
echo Pressione qualquer tecla para sair...
pause >nul 