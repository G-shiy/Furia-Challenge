"""
Simple model functions for managing users and games in memory.
"""

from typing import Dict, List, Optional, Any
from .config import USERS, GAMES, USER_GAME_PREFERENCES, NOTIFICATION_PREFERENCES, USER_PERSONAL_INFO

def create_user(telegram_id: int, first_name: str, username: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a user dictionary object.
    """
    user = {
        "telegram_id": telegram_id,
        "first_name": first_name,
        "username": username
    }
    USERS[telegram_id] = user
    return user

def get_user(telegram_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a user by telegram_id.
    """
    return USERS.get(telegram_id)

def update_user(telegram_id: int, first_name: str, username: Optional[str] = None) -> Dict[str, Any]:
    """
    Update a user's information.
    """
    if telegram_id in USERS:
        USERS[telegram_id]["first_name"] = first_name
        USERS[telegram_id]["username"] = username
    else:
        create_user(telegram_id, first_name, username)
    return USERS[telegram_id]

def create_game(name: str) -> Dict[str, Any]:
    """
    Create a game dictionary object.
    """
    game = {
        "name": name
    }
    GAMES[name] = game
    return game

def get_game(name: str) -> Optional[Dict[str, Any]]:
    """
    Get a game by name.
    """
    return GAMES.get(name)

def get_all_games() -> List[Dict[str, Any]]:
    """
    Get all games.
    """
    return list(GAMES.values())

def set_user_game_preferences(telegram_id: int, game_names: List[str]) -> None:
    """
    Set a user's game preferences.
    """
    USER_GAME_PREFERENCES[telegram_id] = game_names

def get_user_game_preferences(telegram_id: int) -> List[str]:
    """
    Get a user's game preferences.
    """
    return USER_GAME_PREFERENCES.get(telegram_id, [])

def set_user_notification_preferences(telegram_id: int, notification_types: List[str]) -> None:
    """
    Set a user's notification preferences.
    """
    NOTIFICATION_PREFERENCES[telegram_id] = notification_types

def get_user_notification_preferences(telegram_id: int) -> List[str]:
    """
    Get a user's notification preferences.
    """
    return NOTIFICATION_PREFERENCES.get(telegram_id, [])

def set_user_personal_info(telegram_id: int, name: str, address: str, cpf: str) -> Dict[str, str]:
    """
    Set a user's personal information.
    
    Args:
        telegram_id: User's Telegram ID
        name: Full name
        address: Physical address
        cpf: Brazilian tax ID (CPF)
        
    Returns:
        Dict with the user's personal information
    """
    personal_info = {
        "name": name,
        "address": address,
        "cpf": cpf
    }
    USER_PERSONAL_INFO[telegram_id] = personal_info
    return personal_info

def get_user_personal_info(telegram_id: int) -> Optional[Dict[str, str]]:
    """
    Get a user's personal information.
    
    Args:
        telegram_id: User's Telegram ID
        
    Returns:
        Dict with user's personal info or None if not found
    """
    return USER_PERSONAL_INFO.get(telegram_id)

def update_user_personal_info(telegram_id: int, **kwargs) -> Optional[Dict[str, str]]:
    """
    Update specific fields of a user's personal information.
    
    Args:
        telegram_id: User's Telegram ID
        **kwargs: Fields to update (name, address, cpf)
        
    Returns:
        Updated personal info dict or None if user not found
    """
    if telegram_id not in USER_PERSONAL_INFO:
        return None
        
    for field, value in kwargs.items():
        if field in ["name", "address", "cpf"]:
            USER_PERSONAL_INFO[telegram_id][field] = value
            
    return USER_PERSONAL_INFO[telegram_id]
