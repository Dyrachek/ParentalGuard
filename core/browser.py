import os
import sqlite3
import shutil

def get_chrome_tabs(page=0, per_page=8):
    """Получить вкладки Chrome с пагинацией"""
    try:
        db_path = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\History")
        if not os.path.exists(db_path):
            return [], [], 0

        temp_db = "temp_chrome.db"
        if os.path.exists(temp_db):
            os.remove(temp_db)
        shutil.copy2(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM urls")
        total = c.fetchone()[0]

        c.execute("""
            SELECT title, url 
            FROM urls 
            ORDER BY last_visit_time DESC 
            LIMIT ? OFFSET ?
        """, (per_page, page * per_page))
        tabs = c.fetchall()
        conn.close()
        os.remove(temp_db)

        titles = [title for title, url in tabs]
        urls = [url for title, url in tabs]
        return titles, urls, total
    except:
        return [], [], 0

def get_edge_tabs(page=0, per_page=8):
    """Получить вкладки Edge с пагинацией"""
    try:
        db_path = os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\History")
        if not os.path.exists(db_path):
            return [], [], 0

        temp_db = "temp_edge.db"
        if os.path.exists(temp_db):
            os.remove(temp_db)
        shutil.copy2(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM urls")
        total = c.fetchone()[0]

        c.execute("""
            SELECT title, url 
            FROM urls 
            ORDER BY last_visit_time DESC 
            LIMIT ? OFFSET ?
        """, (per_page, page * per_page))
        tabs = c.fetchall()
        conn.close()
        os.remove(temp_db)

        titles = [title for title, url in tabs]
        urls = [url for title, url in tabs]
        return titles, urls, total
    except:
        return [], [], 0