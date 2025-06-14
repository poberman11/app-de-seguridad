from cryptography.fernet import Fernet
import sqlite3, os
from database.auth import DB_FILE

KEY_FILE = "secret.key"

def load_key():
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as f:
            f.write(Fernet.generate_key())
    with open(KEY_FILE, "rb") as f:
        return f.read()

fernet = Fernet(load_key())

def init_password_table():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT
            )
        """)
        conn.commit()

def add_password(password):
    encrypted = fernet.encrypt(password.encode())
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("INSERT INTO passwords (password) VALUES (?)", (encrypted,))
        conn.commit()

def get_passwords():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT password FROM passwords")
        return [fernet.decrypt(row[0]).decode() for row in cursor.fetchall()]
