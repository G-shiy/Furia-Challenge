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

Aqui estão os comandos disponíveis:

/start - Inicia a conversa com o bot.
/help - Mostra esta mensagem de ajuda.
/personalize - Permite escolher quais jogos e notificações você quer receber.
/next_games ou /jogos - Mostra os próximos jogos da FURIA para os jogos que você selecionou.
/about ou /sobre - Mostra informações sobre a FURIA.
/fanchat - Inicia o simulador de conversa de torcida (em breve!).
/live - Mostra o status de jogos ao vivo (em breve!).
/cancel - Cancela a operação atual (como a personalização).

Use /personalize para começar!""",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='HTML'
    )
