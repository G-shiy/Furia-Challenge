import os
from dotenv import load_dotenv

load_dotenv(override=True)


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


USERS = {} 
GAMES = {} 
USER_GAME_PREFERENCES = {} 
NOTIFICATION_PREFERENCES = {}  
USER_PERSONAL_INFO = {} 


def initialize_memory_store():
    global USERS, GAMES, USER_GAME_PREFERENCES, NOTIFICATION_PREFERENCES, USER_PERSONAL_INFO
    
    USERS.clear()
    GAMES.clear()
    USER_GAME_PREFERENCES.clear()
    NOTIFICATION_PREFERENCES.clear()
    USER_PERSONAL_INFO.clear()
