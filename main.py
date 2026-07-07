import asyncio
import time
from datetime import datetime
import config
from core.apps import get_active_window, check_for_notifications
from core.screenshot import take_screenshot, cleanup_screenshots
from utils.db import init_db, log_activity
from bot.bot import run_bot
import threading

async def monitoring_loop():
    print(f"[{datetime.now()}] ParentalGuard запущен")
    init_db()
    cleanup_screenshots(max_keep=10)
    
    last_screenshot = 0
    last_notification_check = 0
    
    while True:
        try:
            active = get_active_window()
            
            if time.time() - last_notification_check > 5:
                await check_for_notifications(active)
                last_notification_check = time.time()
            
            if active and active['title'] != "Unknown":
                if time.time() - last_screenshot > 60 or active['is_game']:
                    screenshot = take_screenshot()
                    last_screenshot = time.time()
                    
                    log_activity(
                        app_name=active['title'][:100],
                        window_title=active['title'],
                        is_game=active.get('is_game', False),
                        screenshot=screenshot
                    )
            
            if datetime.now().hour == 22 and datetime.now().minute == 0:
                from bot.bot import send_daily_report
                await send_daily_report(None)
                await asyncio.sleep(60)
            
            await asyncio.sleep(config.MONITOR_INTERVAL)
            
        except Exception as e:
            await asyncio.sleep(10)

def run_monitoring():
    asyncio.run(monitoring_loop())

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=run_monitoring, daemon=True)
    monitor_thread.start()
    
    print("Запускаем Telegram бота...")
    run_bot()