# database/crypto.py
from cryptography.fernet import Fernet
import os

KEY_FILE = "app.key"

def generate_key():
    if not os.path.exists(KEY_FILE):
        with open(KEY_FILE, "wb") as f:
            f.write(Fernet.generate_key())

def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt(text: str) -> str:
    fernet = Fernet(load_key())
    return fernet.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    fernet = Fernet(load_key())
    return fernet.decrypt(token.encode()).decode()
