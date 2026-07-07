from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import config
from bot.keyboard import main_menu, screenshots_menu
from core.apps import get_active_window, get_running_apps
from core.browser import get_chrome_tabs, get_edge_tabs
import os
from datetime import datetime

bot_instance = None

async def safe_edit(query, text, reply_markup=None):
    try:
        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    except Exception:
        await query.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👨‍👦 <b>{config.BOT_NAME} v{config.VERSION}</b>\n\n"
        "✅ Система родительского контроля активна.\n\n"
        "Выберите действие:",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "live":
        active = get_active_window()
        text = f"""👁️ <b>Текущее активное окно</b>

🪟 Окно: <code>{active['title']}</code>
🎮 Это игра: {'✅ Да' if active.get('is_game') else '❌ Нет'}
⏰ Время: {datetime.now().strftime('%H:%M:%S')}
"""
        await safe_edit(query, text, main_menu())

    elif query.data == "games":
        apps = get_running_apps()
        games = [name for name in apps.keys() if any(g in name.lower() for g in config.GAME_PROCESSES) or "cs2" in name.lower()]
        active = get_active_window()
        if active['is_game'] and active['title'] not in games:
            games.append(active['title'])
        if games:
            text = "🎮 <b>Запущенные игры:</b>\n\n"
            for game in games[:15]:
                text += f"• {game}\n"
            text += f"\n⏰ Обновлено: {datetime.now().strftime('%H:%M:%S')}"
        else:
            text = "🎮 <b>Запущенные игры</b>\n\nСейчас игры не обнаружены."
        await safe_edit(query, text, main_menu())

    elif query.data == "live_report":
        active = get_active_window()
        games = [name for name in get_running_apps().keys() if any(g in name.lower() for g in config.GAME_PROCESSES) or "cs2" in name.lower()]
        text = f"""📊 <b>Live Отчёт</b>

🕒 {datetime.now().strftime('%H:%M:%S')}

👁️ Активное окно:
<code>{active['title']}</code>

🎮 Запущенных игр: {len(games)}
{"\n".join([f"• {g}" for g in games[:8]]) if games else "Игры не запущены"}

📸 Скриншотов: {len([f for f in os.listdir('screenshots') if f.endswith('.png')])}
"""
        await safe_edit(query, text, main_menu())

    elif query.data == "browser":
        keyboard = [
            [InlineKeyboardButton("🌐 Chrome Вкладки", callback_data="chrome_tabs")],
            [InlineKeyboardButton("🌐 Edge Вкладки", callback_data="edge_tabs")],
            [InlineKeyboardButton("← Назад", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = """🌐 <b>Мониторинг браузеров</b>

Выберите браузер:"""
        await safe_edit(query, text, reply_markup)

    elif query.data == "chrome_tabs":
        titles, urls, total = get_chrome_tabs()
        if not titles:
            await safe_edit(query, "🌐 Chrome не найден.", main_menu())
            return

        text = "🌐 <b>Открытые вкладки Chrome</b>\n\n"
        for i, title in enumerate(titles, 1):
            text += f"{i}. {title[:60]}\n"

        keyboard = []
        for i in range(len(titles)):
            keyboard.append([InlineKeyboardButton(f"Открыть {i+1}", callback_data=f"open_url|chrome|{i}")])
        keyboard.append([InlineKeyboardButton("← Назад", callback_data="browser")])
        await safe_edit(query, text, InlineKeyboardMarkup(keyboard))

    elif query.data == "edge_tabs":
        titles, urls, total = get_edge_tabs()
        if not titles:
            await safe_edit(query, "🌐 Edge не найден.", main_menu())
            return

        text = "🌐 <b>Открытые вкладки Edge</b>\n\n"
        for i, title in enumerate(titles, 1):
            text += f"{i}. {title[:60]}\n"

        keyboard = []
        for i in range(len(titles)):
            keyboard.append([InlineKeyboardButton(f"Открыть {i+1}", callback_data=f"open_url|edge|{i}")])
        keyboard.append([InlineKeyboardButton("← Назад", callback_data="browser")])
        await safe_edit(query, text, InlineKeyboardMarkup(keyboard))

    elif query.data == "make_screenshot":
        from core.screenshot import take_screenshot
        filepath = take_screenshot()
        if filepath and os.path.exists(filepath):
            await query.message.reply_photo(
                photo=open(filepath, 'rb'),
                caption=f"📸 Скриншот сделан\n⏰ {datetime.now().strftime('%H:%M:%S')}",
                reply_markup=main_menu()
            )
            await safe_edit(query, "✅ Скриншот сделан и отправлен.", main_menu())
        else:
            await safe_edit(query, "❌ Не удалось сделать скриншот.", main_menu())

    elif query.data.startswith("open_url|"):
        _, browser, index = query.data.split("|")
        index = int(index)
        if browser == "chrome":
            titles, urls, _ = get_chrome_tabs()
        else:
            titles, urls, _ = get_edge_tabs()
        if index < len(urls):
            url = urls[index]
            await query.message.reply_text(f"🔗 {url}")
        await safe_edit(query, "✅ Ссылка выбрана.", main_menu())

    elif query.data == "screenshots":
        files = sorted([f for f in os.listdir("screenshots") if f.endswith(".png")], reverse=True)
        if files:
            text = f"📸 <b>Последние скриншоты ({len(files)})</b>\n\nВыберите для просмотра:"
            await safe_edit(query, text, screenshots_menu(files))
        else:
            await safe_edit(query, "📸 Нет скриншотов.", main_menu())

    elif query.data.startswith("view_screenshot|"):
        filename = query.data.split("|")[1]
        filepath = os.path.join("screenshots", filename)
        if os.path.exists(filepath):
            await query.message.reply_photo(photo=open(filepath, 'rb'), caption=f"📸 {filename}")
            await safe_edit(query, f"✅ Скриншот отправлен.", main_menu())
        else:
            await safe_edit(query, "❌ Скриншот не найден.")

    elif query.data == "back_to_main":
        await safe_edit(query, "Главное меню:", main_menu())

    else:
        await safe_edit(query, "Функция в разработке... 🔧", main_menu())

async def send_game_notification(game_name):
    global bot_instance
    if bot_instance:
        try:
            await bot_instance.send_message(
                chat_id=config.PARENT_CHAT_ID,
                text=f"🎮 <b>Игра запущена</b>\n\n{game_name}",
                parse_mode="HTML"
            )
        except:
            pass

def run_bot():
    global bot_instance
    app = ApplicationBuilder().token(config.TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    bot_instance = app.bot
    print("🤖 Бот запущен!")
    app.run_polling(drop_pending_updates=True)