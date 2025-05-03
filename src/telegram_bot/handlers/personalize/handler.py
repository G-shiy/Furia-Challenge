import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

from .constants import (
    ASK_NAME, ASK_ADDRESS, ASK_CPF, ASK_GAMES, ASK_NOTIFS, 
    AVAILABLE_GAMES, GAME_ALIASES, GAME_PATTERN, NOTIFICATION_OPTIONS,
    CPF_PATTERN
)
from .utils import save_preferences_memory, save_preferences_db, save_personal_info_db
from ..cancel import cancel

logger = logging.getLogger(__name__)

async def personalize_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None: return await cancel(update, context)
    if context.user_data is None: return await cancel(update, context)

    context.user_data.clear()
    
    await update.message.reply_text(
        "✨ Vamos personalizar sua experiência! ✨\n\n"
        "Primeiro, vamos coletar alguns dados básicos:\n\n"
        "Por favor, digite seu nome completo:",
        reply_markup=ReplyKeyboardMarkup([["Cancelar"]], one_time_keyboard=True, resize_keyboard=True)
    )
    
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None: return await cancel(update, context)
    if context.user_data is None: return await cancel(update, context)

    text = update.message.text
    
    if text is None: return await cancel(update, context)
    if text.lower() == 'cancelar': return await cancel(update, context)
    
    context.user_data['full_name'] = text.strip()
    
    await update.message.reply_text(
        f"Obrigado, {text.split()[0]}!\n\n"
        "Agora, por favor, digite seu endereço completo:",
        reply_markup=ReplyKeyboardMarkup([["Cancelar"]], one_time_keyboard=True, resize_keyboard=True)
    )
    
    return ASK_ADDRESS

async def ask_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None: return await cancel(update, context)
    if context.user_data is None: return await cancel(update, context)

    text = update.message.text
    
    if text is None: return await cancel(update, context)
    if text.lower() == 'cancelar': return await cancel(update, context)
    
    context.user_data['address'] = text.strip()
    
    await update.message.reply_text(
        "Quase lá! Por último, por favor digite seu CPF (apenas números ou no formato XXX.XXX.XXX-XX):",
        reply_markup=ReplyKeyboardMarkup([["Cancelar"]], one_time_keyboard=True, resize_keyboard=True)
    )
    
    return ASK_CPF

async def ask_cpf(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None: return await cancel(update, context)
    if context.user_data is None: return await cancel(update, context)
    if update.effective_user is None: return await cancel(update, context)

    text = update.message.text
    
    if text is None: return await cancel(update, context)
    if text.lower() == 'cancelar': return await cancel(update, context)
    
    if not CPF_PATTERN.match(text.strip()):
        await update.message.reply_text(
            "❌ CPF inválido. Por favor, digite novamente no formato XXX.XXX.XXX-XX ou apenas os 11 números:",
            reply_markup=ReplyKeyboardMarkup([["Cancelar"]], one_time_keyboard=True, resize_keyboard=True)
        )
        return ASK_CPF
    
    context.user_data['cpf'] = text.strip()
    
    user_id = update.effective_user.id
    try:
        success = await save_personal_info_db(
            user_id, 
            context.user_data['full_name'], 
            context.user_data['address'], 
            context.user_data['cpf']
        )
        
        if not success:
            logger.warning(f"Failed to save personal info for user {user_id}")
            
    except Exception as e:
        logger.error(f"Error saving personal info for user {user_id}: {e}")
    
    reply_keyboard = [AVAILABLE_GAMES[i:i + 2] for i in range(0, len(AVAILABLE_GAMES), 2)]
    reply_keyboard.append(["Pronto", "Cancelar"])

    raw_text = (
        "Obrigado! Agora vamos personalizar seus interesses.\n\n"
        "Quais jogos da FURIA você gostaria de acompanhar? 🎮\n"
        "(Você pode escolher mais de um jogo: envie os nomes separados por vírgula ou toque nos botões abaixo. Quando terminar, envie 'pronto'.)"
        "\n\n<b>Jogos disponíveis:</b>\n"
        f"{', '.join(AVAILABLE_GAMES)}\n\n"
        "Você pode cancelar a qualquer momento enviando 'cancelar'."
    )

    await update.message.reply_text(
        text=raw_text,
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    context.user_data['chosen_games'] = set()
    return ASK_GAMES

async def ask_games(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None: return await cancel(update, context)
    if context.user_data is None: return await cancel(update, context)

    text = update.message.text
    user_data = context.user_data

    if text is None: return await cancel(update, context)

    if text.lower() == 'cancelar':
        user_data.clear()
        return await cancel(update, context)

    if text.lower() == 'pronto':
        if not user_data.get('chosen_games'):
            await update.message.reply_text("Você precisa escolher pelo menos um jogo. Quais jogos você quer acompanhar?",)
            return ASK_GAMES

        reply_keyboard = [NOTIFICATION_OPTIONS[i:i + 2] for i in range(0, len(NOTIFICATION_OPTIONS), 2)]
        reply_keyboard.append(["Pronto", "Cancelar"])
        await update.message.reply_text(
            "Excelente! Agora, como você gostaria de receber as notificações sobre esses jogos? 🔔\n"
            "(Escolha as opções desejadas: envie os nomes separados por vírgula ou clique nos botões abaixo. Quando terminar, envie 'pronto'.)\n\n"
            "Opções disponíveis:\n"
            "- Resultados 📊\n"
            "- Notícias 📰\n"
            "- Alertas de Jogos 🎮"
            "\n\nVocê pode cancelar a qualquer momento enviando 'cancelar'.",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
        )
        user_data['chosen_notifs'] = set()
        return ASK_NOTIFS

    selected_games = [game.strip() for game in text.split(',')] if text else []
    valid_games = []
    invalid_games = []

    for game_input in selected_games:
        match = GAME_PATTERN.fullmatch(game_input)
        if match:
            matched_text_lower = game_input.lower()
            if matched_text_lower in GAME_ALIASES:
                canonical_game_name = GAME_ALIASES[matched_text_lower]
            else:
                canonical_game_name = next((g for g in AVAILABLE_GAMES if g.lower() == matched_text_lower), game_input)
            user_data['chosen_games'].add(canonical_game_name)
            valid_games.append(canonical_game_name)
        else:
            invalid_games.append(game_input)

    response_message = ""
    if valid_games:
        response_message += f"Adicionado: {', '.join(valid_games)}.\n"
    if invalid_games:
        response_message += f"Não reconheci: {', '.join(invalid_games)}. Jogos disponíveis: {', '.join(AVAILABLE_GAMES)}.\n"

    response_message += "Escolha mais jogos ou envie 'pronto'."
    reply_keyboard = [AVAILABLE_GAMES[i:i + 2] for i in range(0, len(AVAILABLE_GAMES), 2)]
    reply_keyboard.append(["Pronto", "Cancelar"])

    await update.message.reply_text(
        response_message,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

    return ASK_GAMES

async def ask_notifs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message is None: return await cancel(update, context)
    if context.user_data is None: return await cancel(update, context)
    if context.bot_data is None: return await cancel(update, context)
    if update.effective_user is None: return await cancel(update, context)

    text = update.message.text
    user_data = context.user_data
    user_id = update.effective_user.id
    preferences_store = context.bot_data.setdefault('user_preferences_store', {})

    if text is None: return await cancel(update, context)

    if text.lower() == 'cancelar':
        user_data.clear()
        return await cancel(update, context)

    if text.lower() == 'pronto':
        if not user_data.get('chosen_notifs'):
            await update.message.reply_text("Você precisa escolher pelo menos uma forma de notificação. Como você quer acompanhar?",)
            return ASK_NOTIFS

        chosen_games_list = sorted(list(user_data.get('chosen_games', [])))
        chosen_notifs_list = sorted(list(user_data.get('chosen_notifs', [])))

        try:
            db_success = await save_preferences_db(
                user_id, 
                update.effective_user.first_name, 
                update.effective_user.username or "", 
                chosen_games_list, 
                chosen_notifs_list
            )
            
            save_preferences_memory(preferences_store, user_id, chosen_games_list, chosen_notifs_list)
            
            if not db_success:
                logger.warning(f"Failed to save user preferences to database for user {user_id}, but saved to memory")
                
            logger.info(f"Preferences saved for user {user_id}: Games={chosen_games_list}, Notifs={chosen_notifs_list}")

            next_games_example = f"""
            🔔 <b>Preferências Salvas com Sucesso!</b>

            Aqui está um exemplo do que você irá acompanhar:

            🎯 <i>Próximos jogos da FURIA</i> ({', '.join(chosen_games_list)}):
            - 🆚 FURIA vs. NAVI — 28/04/2025 às 15:00 BRT
            - 🆚 FURIA vs. G2 — 30/04/2025 às 13:00 BRT

            ✅ Você receberá atualizações sobre: <i>{', '.join(chosen_games_list)}</i>
            📢 Tipos de notificação selecionados: <i>{', '.join(chosen_notifs_list)}</i>

            Obrigado por personalizar sua experiência! 🚀
            """

            await update.message.reply_text(
                next_games_example,
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Failed to save preferences for user {user_id}: {e}")
            await update.message.reply_text(
                "⚠️ Ocorreu um erro ao salvar suas preferências. Por favor, tente novamente mais tarde.",
                reply_markup=ReplyKeyboardRemove(),
            )
        finally:
            user_data.clear()
            return ConversationHandler.END

    selected_notifs = [notif.strip() for notif in text.split(',')] if text else []
    valid_notifs = []
    invalid_notifs = []

    for notif in selected_notifs:
        matched = False
        for option in NOTIFICATION_OPTIONS:
            if notif.lower() == option.lower():
                user_data['chosen_notifs'].add(option)
                valid_notifs.append(option)
                matched = True
                break
        if not matched:
            invalid_notifs.append(notif)

    response_message = ""
    if valid_notifs:
        response_message += f"Adicionado: {', '.join(valid_notifs)}.\n"
    if invalid_notifs:
        response_message += f"Não reconheci: {', '.join(invalid_notifs)}. Opções disponíveis: {', '.join(NOTIFICATION_OPTIONS)}.\n"

    response_message += "Escolha mais opções ou envie 'pronto'."

    await update.message.reply_text(response_message)

    return ASK_NOTIFS

def get_personalize_conv_handler() -> ConversationHandler:
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("personalize", personalize_start)],
        states={
            ASK_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name),
            ],
            ASK_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_address),
            ],
            ASK_CPF: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_cpf),
            ],
            ASK_GAMES: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_games),
            ],
            ASK_NOTIFS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_notifs),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            MessageHandler(filters.Regex("(?i)^Cancelar$"), cancel)
        ],
    )
    return conv_handler
