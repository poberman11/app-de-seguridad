# database/config.py
import sqlite3
from database.auth import DB_FILE

def init_config_table():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS app_paths (
                key TEXT PRIMARY KEY,
                path TEXT
            )
        ''')
        conn.commit()

def set_path(key: str, path: str):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            INSERT INTO app_paths (key, path) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET path = excluded.path
        ''', (key, path))
        conn.commit()

def get_path(key: str) -> str:
    with sqlite3.connect(DB_FILE) as conn:
        result = conn.execute("SELECT path FROM app_paths WHERE key = ?", (key,)).fetchone()
        return result[0] if result else ""

def get_all_paths() -> dict:
    with sqlite3.connect(DB_FILE) as conn:
        rows = conn.execute("SELECT key, path FROM app_paths").fetchall()
        return {k: v for k, v in rows}
