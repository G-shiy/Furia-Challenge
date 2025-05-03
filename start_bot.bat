@echo off
title Bot Telegram da FURIA

:: Configuração de cores no Windows
color 0A

echo ================================================
echo Iniciando o Bot Telegram da FURIA
echo ================================================
echo.

:: Verificando se o Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo Python nao esta instalado ou nao esta no PATH.
    echo Por favor, instale o Python e adicione-o ao PATH.
    pause
    exit /b 1
)

:: Criando ambiente virtual se não existir
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        color 0C
        echo Falha ao criar ambiente virtual. Verifique se o Python tem o modulo venv instalado.
        pause
        exit /b 1
    )
    echo Ambiente virtual criado com sucesso!
)

:: Ativando o ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    color 0C
    echo Falha ao ativar ambiente virtual.
    pause
    exit /b 1
)
echo Ambiente virtual ativado!

:: Instalando os requisitos
echo Instalando ou atualizando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    color 0C
    echo Falha ao instalar dependencias. Verifique o arquivo requirements.txt.
    pause
    exit /b 1
)
echo Dependencias instaladas/atualizadas com sucesso!

:: Verificando configurações
if not exist .env (
    color 0E
    echo Arquivo .env nao encontrado. Certifique-se de configurar as variaveis de ambiente necessarias.
    echo Exemplo de configuracao:
    echo TELEGRAM_BOT_TOKEN=seu_token_aqui
    set /p continuar="Deseja continuar mesmo sem o arquivo .env? (s/n): "
    if /i not "%continuar%"=="s" (
        color 0C
        echo Inicializacao cancelada.
        pause
        exit /b 1
    )
)

:: Executando o bot
echo Iniciando o bot...
echo ================================================
playwright install chromium
python -m src.telegram_bot.main
echo ================================================
echo Bot encerrado.
pause