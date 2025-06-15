# === database/shortcuts.py ===
import sqlite3
from config.settings import DB_PATH

# Inicializar las 3 tablas de accesos

def init_shortcuts_tables():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS main_shortcuts (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                ruta TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS programs (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                ruta TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                ruta TEXT
            )
        """)

        for tabla in ("main_shortcuts", "programs", "games"):
            for i in range(1, 9):
                conn.execute(f"""
                    INSERT OR IGNORE INTO {tabla} (id, nombre, ruta) VALUES (?, ?, ?)
                """, (i, f"{tabla}_{i}", ""))
        conn.commit()

# Obtener los accesos de cada tabla
def get_shortcuts(tabla):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(f"SELECT id, nombre, ruta FROM {tabla}")
        return cursor.fetchall()

# Actualizar un acceso
def update_shortcut(tabla, id, nombre, ruta):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(f"UPDATE {tabla} SET nombre = ?, ruta = ? WHERE id = ?", (nombre, ruta, id))
        conn.commit()

