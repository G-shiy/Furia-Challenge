"""
Data service module for handling user and game preferences.
Uses in-memory dictionaries to store data instead of a database.
"""
import logging
from typing import List, Tuple, Optional, Dict, Any

from ..models import (
    create_user, update_user, get_user, 
    create_game, get_game, get_all_games,
    set_user_game_preferences, get_user_game_preferences,
    set_user_notification_preferences, get_user_notification_preferences,
    set_user_personal_info, get_user_personal_info, update_user_personal_info
)

logger = logging.getLogger(__name__)

async def check_db_connection() -> bool:
    """
    Check connection to in-memory store.
    Always returns True since we're using in-memory dictionaries.
    """
    logger.info("In-memory data storage is active")
    return True

async def ensure_games_exist(available_games: List[str]) -> None:
    """
    Ensure all available games exist in the in-memory storage.
    Should be called during application startup.
    
    Args:
        available_games: List of game names to ensure exist
    """
    try:
        # Get existing games
        existing_games = list(get_all_games())
        existing_game_names = {game["name"] for game in existing_games}
        
        # Find games that need to be created
        games_to_create = [name for name in available_games if name not in existing_game_names]
        
        # Create missing games
        if games_to_create:
            for game_name in games_to_create:
                create_game(game_name)
            logger.info(f"Created {len(games_to_create)} missing games in memory")
        else:
            logger.info("All available games already exist in memory")
            
    except Exception as e:
        logger.error(f"Error ensuring games exist in memory: {e}")
        raise

async def save_user_preferences(
    telegram_id: int, 
    first_name: str, 
    username: Optional[str], 
    preferred_games: List[str], 
    notification_prefs: List[str]
) -> bool:
    """
    Save user preferences to in-memory storage.
    Returns True if successful, False otherwise.
    """
    try:
        # Update or create user
        update_user(telegram_id, first_name, username)
        
        # Set game preferences
        set_user_game_preferences(telegram_id, preferred_games)
        
        # Set notification preferences
        set_user_notification_preferences(telegram_id, notification_prefs)
        
        logger.info(f"Saved preferences for user {telegram_id}: games={preferred_games}, notifs={notification_prefs}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving preferences for user {telegram_id}: {e}")
        return False

async def get_user_preferences(telegram_id: int) -> Tuple[Optional[List[str]], Optional[List[str]]]:
    """
    Get user preferences from in-memory storage.
    Returns a tuple of (preferred_games, notification_prefs).
    If user doesn't exist, returns (None, None).
    """
    try:
        user = get_user(telegram_id)
        
        if user is None:
            return None, None
            
        game_preferences = get_user_game_preferences(telegram_id)
        notification_preferences = get_user_notification_preferences(telegram_id)
        
        return game_preferences, notification_preferences
        
    except Exception as e:
        logger.error(f"Error getting preferences for user {telegram_id}: {e}")
        return None, None

async def register_user(telegram_id: int, first_name: str, username: Optional[str] = None) -> bool:
    """
    Register a new user or update existing user details.
    Returns True if successful, False otherwise.
    """
    try:
        update_user(telegram_id, first_name, username)
        return True
    except Exception as e:
        logger.error(f"Error registering user {telegram_id}: {e}")
        return False

async def save_user_personal_info(
    telegram_id: int,
    name: str,
    address: str,
    cpf: str
) -> bool:
    """
    Save user personal information to in-memory storage.
    Returns True if successful, False otherwise.
    
    Args:
        telegram_id: User's Telegram ID
        name: Full name
        address: Physical address
        cpf: Brazilian ID (CPF)
    """
    try:
        set_user_personal_info(telegram_id, name, address, cpf)
        logger.info(f"Saved personal info for user {telegram_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving personal info for user {telegram_id}: {e}")
        return False

async def get_user_personal_data(telegram_id: int) -> Optional[Dict[str, str]]:
    """
    Get user personal information from in-memory storage.
    
    Args:
        telegram_id: User's Telegram ID
        
    Returns:
        Dict with user's personal info or None if not found
    """
    try:
        return get_user_personal_info(telegram_id)
    except Exception as e:
        logger.error(f"Error getting personal info for user {telegram_id}: {e}")
        return None

async def update_user_personal_data(telegram_id: int, **kwargs) -> bool:
    """
    Update specific fields of user personal information.
    
    Args:
        telegram_id: User's Telegram ID
        **kwargs: Fields to update (name, address, cpf)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        result = update_user_personal_info(telegram_id, **kwargs)
        if result is None:
            return False
        logger.info(f"Updated personal info for user {telegram_id}: fields={list(kwargs.keys())}")
        return True
    except Exception as e:
        logger.error(f"Error updating personal info for user {telegram_id}: {e}")
        return False