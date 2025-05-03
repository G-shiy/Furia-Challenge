#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' 

echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}Iniciando o Bot Telegram da FURIA${NC}"
echo -e "${BLUE}================================================${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 não está instalado. Por favor, instale o Python 3 antes de continuar.${NC}"
    exit 1
fi

if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Criando ambiente virtual...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Falha ao criar ambiente virtual. Verifique se o Python tem o módulo venv instalado.${NC}"
        exit 1
    fi
    echo -e "${GREEN}Ambiente virtual criado com sucesso!${NC}"
fi

echo -e "${YELLOW}Ativando ambiente virtual...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Falha ao ativar ambiente virtual.${NC}"
    exit 1
fi
echo -e "${GREEN}Ambiente virtual ativado!${NC}"

echo -e "${YELLOW}Instalando ou atualizando dependências...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Falha ao instalar dependências. Verifique o arquivo requirements.txt.${NC}"
    exit 1
fi
echo -e "${GREEN}Dependências instaladas/atualizadas com sucesso!${NC}"

if [ ! -f .env ]; then
    echo -e "${YELLOW}Arquivo .env não encontrado. Certifique-se de configurar as variáveis de ambiente necessárias.${NC}"
    echo -e "${YELLOW}Exemplo de configuração:${NC}"
    echo "TELEGRAM_BOT_TOKEN=seu_token_aqui"
    read -p "Deseja continuar mesmo sem o arquivo .env? (s/n): " continuar
    if [[ $continuar != "s" && $continuar != "S" ]]; then
        echo -e "${RED}Inicialização cancelada.${NC}"
        exit 1
    fi
fi

echo -e "${YELLOW}Iniciando o bot...${NC}"
echo -e "${BLUE}================================================${NC}"
playwright install chromium
python -m src.telegram_bot.main
echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}Bot encerrado.${NC}"