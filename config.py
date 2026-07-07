from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
PARENT_CHAT_ID = os.getenv("PARENT_CHAT_ID")

SCREENSHOT_INTERVAL = 300  
MONITOR_INTERVAL = 30       

GAME_PROCESSES = [
    "steam", "cs2", "counter", "dota", "gameoverlay",
    "roblox", "minecraft", "fortnite", "valorant", "league", "genshin", 
    "epic", "origin", "uplay", "battle", "xbox", "ea", "riot"
]
BOT_NAME = "ParentalGuard"
VERSION = "0.1"
NOTIFY_ON_GAMES = True
NOTIFY_ON_SUSPICIOUS = True

SUSPICIOUS_WORDS = ["porn", "xxx", "adult", "hentai", "18+", "sex", "гей", "порно"]
USE_SAME_CHAT = True