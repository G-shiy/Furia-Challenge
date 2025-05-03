import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with information about FURIA."""
    if update.message:
        about_text = (
            "<b>Sobre a FURIA</b> 🐯\n\n"
            "FURIA é uma organização brasileira de eSports fundada em 2017. "
            "Competimos em diversos jogos, incluindo Counter-Strike 2, League of Legends, VALORANT, e mais.\n\n"
            "Nosso objetivo é representar o Brasil no cenário mundial de eSports com garra e paixão! #DIADEFURIA"
        )
        await update.message.reply_text(
            about_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='HTML'
        )
    else:
        logger.warning("Update message is None in about handler")

