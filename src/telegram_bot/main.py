import logging
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler

from . import handlers
from .config import TELEGRAM_BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

user_preferences_store = {}

def main() -> None:

    load_dotenv()
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables or config.")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.bot_data['user_preferences_store'] = user_preferences_store

    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("help", handlers.help_command))
    application.add_handler(CommandHandler("next_games", handlers.next_games)) 
    application.add_handler(CommandHandler("jogos", handlers.next_games)) 
    application.add_handler(CommandHandler("about", handlers.about))
    application.add_handler(CommandHandler("sobre", handlers.about))
    application.add_handler(CommandHandler("fanchat", handlers.fan_chat_start))
    application.add_handler(CommandHandler("live", handlers.live_game_status))

    conv_handler = handlers.get_personalize_conv_handler()
    application.add_handler(conv_handler)

    logger.info("Starting bot polling...")
    application.run_polling()

if __name__ == "__main__":
    main()