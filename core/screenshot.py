import mss
from datetime import datetime
import os
import config

def cleanup_screenshots(max_keep=10):
    """Удаляем старые скриншоты, оставляем только последние"""
    screenshot_dir = "screenshots"
    
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir, exist_ok=True)
        return
    
    try:
        files = [f for f in os.listdir(screenshot_dir) if f.endswith(".png")]
        files.sort(key=lambda x: os.path.getctime(os.path.join(screenshot_dir, x)), reverse=True)
        
        for old_file in files[max_keep:]:
            try:
                os.remove(os.path.join(screenshot_dir, old_file))
                print(f"Удалён старый скриншот: {old_file}")
            except Exception as e:
                print(f"Не удалось удалить {old_file}: {e}")
                
        print(f"Очистка скриншотов завершена. Оставлено: {min(len(files), max_keep)}")
        
    except Exception as e:
        print(f"Ошибка очистки скриншотов: {e}")

def take_screenshot():
    """Сделать скриншот"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join("screenshots", filename)
        
        os.makedirs("screenshots", exist_ok=True)
        
        with mss.mss() as sct:
            sct.shot(output=filepath)
        
        return filepath
    except Exception as e:
        print(f"Ошибка скриншота: {e}")
        return None