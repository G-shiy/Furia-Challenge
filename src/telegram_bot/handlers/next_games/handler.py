import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from ..personalize.utils import get_preferences_memory, get_preferences_db  # Import database function
from ...utils.scraper import fetch_draft5

logger = logging.getLogger(__name__)

async def next_games(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or context.bot_data is None or update.effective_user is None:
        return

    user_id = update.effective_user.id
    
    # Try to retrieve preferences from the database first
    preferred_games, notification_prefs = await get_preferences_db(user_id)
    
    # Fallback to memory store if not found in DB
    if preferred_games is None:
        preferences_store = context.bot_data.get('user_preferences_store', {})
        preferred_games, _ = get_preferences_memory(preferences_store, user_id)
        if preferred_games:
            logger.info(f"Falling back to memory store for user {user_id}'s preferences")

    # Check if preferences exist
    if preferred_games is None or not preferred_games:
        await update.message.reply_text(
            "Você precisa personalizar sua experiência primeiro! Use o comando /personalize para escolher seus jogos favoritos.",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    scraped_tournaments = await fetch_draft5()

    if scraped_tournaments is None or not scraped_tournaments:
        await update.message.reply_text(
            "Não encontrei próximos campeonatos agendados para a FURIA no momento.",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    message_parts = ["<b>🏆 Próximos Campeonatos da FURIA conforme Draft5.gg:</b>\n"]
    for tournament in scraped_tournaments:
        tournament_str = f"- <b>{tournament.get('name', 'TBD')}</b> - {tournament.get('dates', 'TBD')} (<a href='{tournament.get('url', '')}'>Link</a>)"
        message_parts.append(tournament_str)

    message = "\n".join(message_parts)

    await update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='HTML',
    )
