from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu():
    keyboard = [
        [InlineKeyboardButton("👁️ Активное окно", callback_data="live")],
        [InlineKeyboardButton("🎮 Запущенные игры", callback_data="games")],
        [InlineKeyboardButton("📊 Live Отчёт", callback_data="live_report")],
        [InlineKeyboardButton("🌐 Браузер", callback_data="browser")],
        [InlineKeyboardButton("📸 Сделать скрин", callback_data="make_screenshot")],
        [InlineKeyboardButton("📸 Последние скриншоты", callback_data="screenshots")],
    ]
    return InlineKeyboardMarkup(keyboard)

def screenshots_menu(files):
    """Создаёт клавиатуру со списком скриншотов"""
    keyboard = []
    for i, filename in enumerate(files[:8]):
        keyboard.append([InlineKeyboardButton(f"📸 {filename[-20:]}", callback_data=f"view_screenshot|{filename}")])
    
    keyboard.append([InlineKeyboardButton("← Назад", callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)