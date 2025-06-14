# database/auth.py
import sqlite3
from config.settings import DB_PATH
from core.security import hash_password, check_password

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB
    )''')
    conn.commit()
    return conn

def user_exists():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0] > 0

def register_user(username, password):
    conn = connect()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_login(username, password):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        return check_password(password, row[0])
    return False
