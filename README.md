# Bot Telegram da FURIA

Este projeto é um bot do Telegram para acompanhar os jogos e campeonatos da FURIA Esports. Ele permite que usuários personalizem preferências de jogos, recebam notificações e vejam informações sobre próximos campeonatos.

## Requisitos

- Python 3.9+
- [Playwright](https://playwright.dev/python/) (instalado automaticamente pelo script)
- [pip](https://pip.pypa.io/en/stable/)
- Conta no Telegram para obter o token do bot

## Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd telegram-bot
   ```

2. **Configure o ambiente:**
   - No Linux:
     ```bash
     ./start_bot.sh
     ```
   - No Windows:
     Clique duas vezes em `start_bot.bat` ou execute no terminal:
     ```bat
     start_bot.bat
     ```

   O script irá:
   - Criar e ativar um ambiente virtual (`venv`)
   - Instalar as dependências do `requirements.txt`
   - Instalar o navegador Chromium para o Playwright
   - Solicitar o arquivo `.env` com a variável `TELEGRAM_BOT_TOKEN`
   - Iniciar o bot

3. **Configuração do .env:**
   Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
   ```env
   TELEGRAM_BOT_TOKEN=seu_token_aqui
   ```

## Estrutura de Pastas

```
telegram-bot/
├── requirements.txt         # Dependências do projeto
├── start_bot.sh             # Script de inicialização para Linux/Mac
├── start_bot.bat            # Script de inicialização para Windows
├── .env                     # Variáveis de ambiente (não versionado)
├── src/
│   └── telegram_bot/
│       ├── main.py          # Ponto de entrada do bot
│       ├── config.py        # Configurações globais e memória
│       ├── models.py        # Modelos e funções de dados em memória
│       ├── utils/
│       │   ├── scraper.py   # Scraper de campeonatos (Playwright)
│       │   └── db_service.py# Serviços de dados (memória)
│       └── handlers/        # Handlers dos comandos do bot
│           ├── start/       # /start
│           ├── help/        # /help
│           ├── about/       # /about
│           ├── next_games/  # /next_games e /jogos
│           ├── personalize/ # /personalize (conversa)
│           ├── cancel/      # /cancel
│           ├── fan_chat/    # /fanchat (placeholder)
│           └── live_game/   # /live (placeholder)
```

## Principais Páginas e Funcionalidades

- **/start**: Inicia a conversa e registra o usuário.
- **/help**: Mostra todos os comandos disponíveis.
- **/personalize**: Fluxo de personalização para escolher jogos e notificações.
- **/next_games** ou **/jogos**: Mostra os próximos campeonatos da FURIA (scraping do draft5.gg).
- **/about** ou **/sobre**: Informações sobre a FURIA.
- **/fanchat**: Placeholder para chat de torcida.
- **/live**: Placeholder para status de jogos ao vivo.
- **/cancel**: Cancela a operação atual.

## Observações

- O bot utiliza armazenamento em memória (não há banco de dados persistente).
- O scraping dos campeonatos é feito em tempo real usando Playwright.
- Para rodar o bot, é necessário que o token do Telegram esteja corretamente configurado no `.env`.

---

Sinta-se à vontade para contribuir ou abrir issues!
