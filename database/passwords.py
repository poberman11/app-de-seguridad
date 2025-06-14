# database/passwords.py
import sqlite3
from database.auth import DB_FILE

def init_passwords_table():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                password TEXT
            )
        ''')
        conn.commit()

def add_password(user, pwd):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO passwords (user, password) VALUES (?, ?)", (user, pwd))
        conn.commit()

def get_passwords(user):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT password FROM passwords WHERE user = ?", (user,))
        return [row[0] for row in cursor.fetchall()]
