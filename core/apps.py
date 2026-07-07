import psutil
import pygetwindow as gw
import config
from datetime import datetime

last_window = None
last_notified_games = set()

def get_running_apps():
    apps = {}
    for proc in psutil.process_iter(['name', 'pid']):
        try:
            name = proc.info['name']
            if name:
                name_lower = name.lower()
                apps[name] = {
                    'pid': proc.info['pid'],
                    'is_game': is_game_process(name_lower),
                    'is_browser': is_browser_process(name_lower)
                }
        except:
            continue
    return apps

def is_game_process(name_lower):
    keywords = config.GAME_PROCESSES + ["cs2", "counter", "dota", "gameoverlay"]
    return any(k in name_lower for k in keywords)

def is_browser_process(name_lower):
    return any(b in name_lower for b in ["chrome", "msedge", "firefox"])

def get_active_window():
    try:
        window = gw.getActiveWindow()
        if window:
            title = window.title.strip()
            title_lower = title.lower()
            is_game = is_game_process(title_lower) or "cs2" in title_lower
            return {
                'title': title if title else "Desktop",
                'is_game': is_game
            }
    except:
        pass
    return {"title": "Unknown", "is_game": False}

async def check_for_notifications(active_window):
    global last_window
    if not active_window or active_window['title'] == "Unknown":
        return
    
    if last_window != active_window['title']:
        last_window = active_window['title']
    
    if config.NOTIFY_ON_GAMES and active_window['is_game']:
        game_name = active_window['title']
        if game_name not in last_notified_games and "steam" not in game_name.lower():
            last_notified_games.add(game_name)
            from bot.bot import send_game_notification
            await send_game_notification(game_name)