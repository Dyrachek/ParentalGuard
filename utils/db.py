import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('activity.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS activity (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        app_name TEXT,
        window_title TEXT,
        is_game INTEGER,
        screenshot TEXT
    )''')
    conn.commit()
    conn.close()

def log_activity(app_name, window_title, is_game=False, screenshot=None):
    conn = sqlite3.connect('activity.db')
    c = conn.cursor()
    c.execute('''INSERT INTO activity 
                 (timestamp, app_name, window_title, is_game, screenshot)
                 VALUES (?, ?, ?, ?, ?)''',
              (datetime.now().isoformat(), app_name, window_title, int(is_game), screenshot))
    conn.commit()
    conn.close()