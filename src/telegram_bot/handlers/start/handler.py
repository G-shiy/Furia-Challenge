import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from ...utils.db_service import register_user 

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if update.message is None or user is None:
        logger.error("Mensagem ou usuário não encontrado. Não é possível enviar resposta.")
        return

    user_registered = await register_user(
        telegram_id=user.id,
        first_name=user.first_name,
        username=user.username
    )
    
    if not user_registered:
        logger.warning(f"Failed to register user {user.id} in database")
    
    await update.message.reply_text(
        rf"""Olá {user.mention_html()}! 👋

Bem-vindo ao Bot da FURIA! 🐯

Eu posso te ajudar a acompanhar seus jogos favoritos da FURIA.

Use /personalize para escolher quais jogos e tipos de notificações você quer receber.
Use /next_games ou /jogos para ver os próximos jogos.
Use /help para ver todos os comandos disponíveis.""",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='HTML'
    )
