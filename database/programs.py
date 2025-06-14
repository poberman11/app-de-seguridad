# database/programs.py
import sqlite3
from database.auth import DB_FILE

def init_programs_table():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS programs (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                ruta TEXT
            )
        """)
        # Prellenar 8 programas si no existen
        for i in range(1, 9):
            conn.execute("""
                INSERT OR IGNORE INTO programs (id, nombre, ruta) VALUES (?, ?, ?)
            """, (i, f"Programa {i}", ""))
        conn.commit()

def get_programs():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute("SELECT id, nombre, ruta FROM programs")
        return cursor.fetchall()

def update_program(id, nombre, ruta):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("UPDATE programs SET nombre = ?, ruta = ? WHERE id = ?", (nombre, ruta, id))
        conn.commit()


def update_program(id, nombre, ruta):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("UPDATE programs SET nombre = ?, ruta = ? WHERE id = ?", (nombre, ruta, id))
        conn.commit()
