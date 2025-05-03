import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def live_game_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Shows live game status (placeholder)."""
    if update.message:
        await update.message.reply_text(
            "🔴 Live Status de Jogos 🔴\n\n"
            "Esta funcionalidade ainda está em desenvolvimento! Em breve você poderá acompanhar os jogos da FURIA ao vivo por aqui. Aguarde!",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        logger.warning("Update message is None in live_game_status handler")
