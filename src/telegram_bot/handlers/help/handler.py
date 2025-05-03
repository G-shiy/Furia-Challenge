import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        help_text = (
            "Aqui estão os comandos que você pode usar:\n\n"
            "/start - Inicia a conversa com o bot.\n"
            "/help - Mostra esta mensagem de ajuda.\n"
            "/personalize - Permite escolher quais jogos e notificações você quer receber.\n"
            "/next_games ou /jogos - Mostra os próximos jogos da FURIA para os jogos que você selecionou.\n"
            "/about ou /sobre - Mostra informações sobre a FURIA.\n"
            "/fanchat - Inicia o simulador de conversa de torcida (em breve!).\n"
            "/live - Mostra o status de jogos ao vivo (em breve!).\n"
            "/cancel - Cancela a operação atual (como a personalização).\n"
        )
        await update.message.reply_text(help_text, reply_markup=ReplyKeyboardRemove())
    else:
        logger.warning("Update message is None in help_command")
