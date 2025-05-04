# Documentação dos Arquivos do Projeto

Este documento descreve a finalidade de cada arquivo principal no projeto do Bot Telegram da FURIA.

## Raiz do Projeto

-   **`README.md`**: Arquivo principal de documentação. Contém informações sobre o projeto, requisitos, instalação, execução, estrutura de pastas e funcionalidades.
-   **`requirements.txt`**: Lista todas as dependências Python necessárias para o projeto. Utilizado pelo `pip` para instalar os pacotes.
-   **`start_bot.bat`**: Script Batch para iniciar o bot em sistemas Windows. Automatiza a criação/ativação do ambiente virtual, instalação de dependências e execução do bot.
-   **`start_bot.sh`**: Script Shell para iniciar o bot em sistemas Linux/macOS. Possui a mesma funcionalidade do `.bat`, mas para ambientes baseados em Unix.
-   **`.gitignore`**: Define quais arquivos e pastas devem ser ignorados pelo Git (sistema de controle de versão). Isso inclui o ambiente virtual, arquivos de cache, logs e o arquivo `.env`.
-   **`.env`** (Não versionado): Arquivo para armazenar variáveis de ambiente sensíveis, como o `TELEGRAM_BOT_TOKEN`. É carregado pelo `python-dotenv`.
-   **`docs.MD`**: Este arquivo, contendo a documentação detalhada da estrutura de arquivos do projeto.

## `src/telegram_bot/`

Diretório principal contendo o código fonte do bot.

-   **`__init__.py`**: Torna o diretório `telegram_bot` um pacote Python, permitindo importações relativas.
-   **`config.py`**: Carrega configurações (como o token do bot a partir do `.env`) e inicializa os dicionários em memória que atuam como banco de dados temporário (`USERS`, `GAMES`, `USER_GAME_PREFERENCES`, etc.).
-   **`main.py`**: Ponto de entrada principal da aplicação do bot. Configura o logging, inicializa a aplicação `python-telegram-bot`, registra todos os handlers (comandos e conversas) e inicia o polling para receber atualizações do Telegram.
-   **`models.py`**: Define funções simples para manipular os dados armazenados em memória (dicionários definidos em `config.py`). Funciona como uma camada de acesso a dados básica para usuários, jogos e preferências.

### `src/telegram_bot/utils/`

Contém módulos utilitários usados em diferentes partes do bot.

-   **`db_service.py`**: Camada de serviço para interagir com os dados. Abstrai as operações de leitura/escrita das preferências e informações do usuário, atualmente usando as funções de `models.py` (armazenamento em memória). Poderia ser adaptado para usar um banco de dados real no futuro.
-   **`scraper.py`**: Contém a lógica de web scraping usando a biblioteca Playwright. É responsável por acessar o site `draft5.gg`, extrair e retornar informações sobre os próximos campeonatos da FURIA.

### `src/telegram_bot/handlers/`

Contém os handlers para os diferentes comandos e interações do Telegram. Cada subdiretório geralmente corresponde a um comando ou funcionalidade.

-   **`__init__.py`**: Agrupa e exporta todos os handlers principais para serem facilmente importados em `main.py`.
-   **`about/`**: Handler para os comandos `/about` e `/sobre`.
    -   `handler.py`: Contém a função `about` que envia informações sobre a FURIA.
-   **`cancel/`**: Handler para o comando `/cancel`.
    -   `handler.py`: Contém a função `cancel` que encerra conversas ativas (como a de personalização) e limpa dados temporários do usuário.
-   **`fan_chat/`**: Handler para o comando `/fanchat` (placeholder).
    -   `handler.py`: Contém a função `fan_chat_start` que informa que a funcionalidade está em desenvolvimento.
-   **`help/`**: Handler para o comando `/help`.
    -   `handler.py`: Contém a função `help_command` que lista todos os comandos disponíveis.
-   **`live_game/`**: Handler para o comando `/live` (placeholder).
    -   `handler.py`: Contém a função `live_game_status` que informa que a funcionalidade está em desenvolvimento.
-   **`next_games/`**: Handler para os comandos `/next_games` e `/jogos`.
    -   `handler.py`: Contém a função `next_games` que busca as preferências do usuário (se existirem), chama o `scraper.py` para obter os dados dos campeonatos e envia a lista para o usuário.
-   **`personalize/`**: Handler para a conversa iniciada pelo comando `/personalize`.
    -   `constants.py`: Define constantes usadas na conversa, como os estados (`ASK_NAME`, `ASK_GAMES`, etc.), listas de jogos disponíveis, aliases e padrões de regex (CPF, jogos).
    -   `handler.py`: Contém a lógica principal da `ConversationHandler`, definindo as funções para cada passo da conversa (pedir nome, endereço, CPF, jogos, notificações) e gerenciando o estado.
    -   `utils.py`: Funções auxiliares específicas para a personalização, como salvar/buscar preferências e dados pessoais usando o `db_service.py` e o armazenamento em memória (`context.bot_data`).
-   **`start/`**: Handler para o comando `/start`.
    -   `handler.py`: Contém a função `start` que envia a mensagem de boas-vindas e registra/atualiza o usuário usando o `db_service.py`.
-   **`*/__init__.py`**: Em cada subdiretório de handler, este arquivo torna o diretório um pacote e geralmente exporta a(s) função(ões) handler principal(is) desse módulo.

## Observações

-   Um banco de dados dedicado (como SQLite, PostgreSQL) não foi implementado neste estágio inicial. Os dados são armazenados em memória (dicionários Python) e são perdidos quando o bot é reiniciado.
-   Não foram utilizadas APIs externas (além da API do Telegram e do web scraping) para obter informações sobre jogos ou outras funcionalidades. A prioridade foi entregar um MVP (Minimum Viable Product) funcional com os recursos essenciais, dado o tempo disponível.

