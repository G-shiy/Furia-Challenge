import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def fan_chat_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the fan chat simulation (placeholder)."""
    if update.message:
        await update.message.reply_text(
            "🗣️ Simulador de Conversa de Torcida 🗣️\n\n"
            "Esta funcionalidade ainda está em desenvolvimento! Em breve você poderá interagir com outros torcedores aqui. Aguarde!",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        logger.warning("Update message is None in fan_chat_start handler")
