import logging
from ...utils.db_service import (
    save_user_preferences, 
    get_user_preferences, 
    save_user_personal_info,
    get_user_personal_data
)

logger = logging.getLogger(__name__)

async def save_personal_info_db(user_id: int, name: str, address: str, cpf: str) -> bool:
    """Save personal information to the in-memory storage"""
    return await save_user_personal_info(user_id, name, address, cpf)

async def get_personal_info_db(user_id: int) -> dict:
    """Get personal information from the in-memory storage"""
    return await get_user_personal_data(user_id) or {}

async def save_preferences_db(user_id: int, first_name: str, username: str, games: list[str], notifs: list[str]) -> bool:
    """Save preferences to the in-memory storage"""
    return await save_user_preferences(user_id, first_name, username, games, notifs)

async def get_preferences_db(user_id: int) -> tuple[list[str] | None, list[str] | None]:
    """Get preferences from the in-memory storage"""
    return await get_user_preferences(user_id)

def save_preferences_memory(store: dict, user_id: int, games: list[str], notifs: list[str]):
    store[user_id] = {"games": games, "notification_prefs": notifs}
    logger.info(f"Preferences saved/updated in memory for user {user_id}")

def get_preferences_memory(store: dict, user_id: int) -> tuple[list[str] | None, list[str] | None]:
    prefs = store.get(user_id)
    if prefs:
        return prefs.get("games", []), prefs.get("notification_prefs", [])
    return None, None
