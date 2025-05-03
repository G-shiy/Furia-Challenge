import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

logger = logging.getLogger(__name__)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None: return ConversationHandler.END
    if context.user_data is None: return ConversationHandler.END
    if update.effective_user is None: return ConversationHandler.END

    user_data = context.user_data
    await update.message.reply_text(
        "Personalização cancelada.", reply_markup=ReplyKeyboardRemove()
    )
    user_data.clear()
    logger.info(f"User {update.effective_user.id} canceled the conversation.")
    return ConversationHandler.END
