import re

ASK_NAME, ASK_ADDRESS, ASK_CPF, ASK_GAMES, ASK_NOTIFS = range(5)

AVAILABLE_GAMES = [
    "Apex Legends", "Counter-Strike 2", "Futebol de 7",
    "League of Legends", "PUBG", "Rainbow Six",
    "Rocket League", "VALORANT"
]

GAME_ALIASES = {
    "apex": "Apex Legends",
    "csgo": "Counter-Strike 2",
    "cs": "Counter-Strike 2",
    "lol": "League of Legends",
}

ALL_VALID_GAME_INPUTS = AVAILABLE_GAMES + list(GAME_ALIASES.keys())

GAME_PATTERN = re.compile(
    r"^(" + "|".join(re.escape(name) for name in ALL_VALID_GAME_INPUTS) + r")$",
    flags=re.IGNORECASE
)

NOTIFICATION_OPTIONS = ["Resultados", "Notícias", "Alertas de Jogos"]

CPF_PATTERN = re.compile(r'^(\d{3}\.?\d{3}\.?\d{3}-?\d{2})$')
