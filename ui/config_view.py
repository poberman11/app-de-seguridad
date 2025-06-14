# ui/config_view.py
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QFileDialog, QListWidget
)
from database.auth import register_user, connect

class ConfigView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración")
        self.layout = QVBoxLayout()

        # === Usuarios ===
        self.label_user = QLabel("Agregar nuevo usuario")
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Usuario")

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Contraseña")
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.btn_add_user = QPushButton("Agregar usuario")
        self.btn_add_user.clicked.connect(self.add_user)

        self.layout.addWidget(self.label_user)
        self.layout.addWidget(self.input_user)
        self.layout.addWidget(self.input_pass)
        self.layout.addWidget(self.btn_add_user)

        # === Eliminar usuario ===
        self.label_del = QLabel("Eliminar usuario")
        self.user_list = QListWidget()
        self.load_users()

        self.btn_delete = QPushButton("Eliminar seleccionado")
        self.btn_delete.clicked.connect(self.delete_selected_user)

        self.layout.addWidget(self.label_del)
        self.layout.addWidget(self.user_list)
        self.layout.addWidget(self.btn_delete)

        # === Configuración de accesos rápidos ===
        self.paths = {}
        self.btns_config = []

        for i in range(8):
            btn = QPushButton(f"Ruta Juego #{i+1}")
            btn.clicked.connect(lambda _, idx=i: self.select_path(idx, "game"))
            self.layout.addWidget(btn)
            self.btns_config.append(btn)

        for i in range(8):
            btn = QPushButton(f"Ruta Programa #{i+1}")
            btn.clicked.connect(lambda _, idx=i: self.select_path(idx, "prog"))
            self.layout.addWidget(btn)
            self.btns_config.append(btn)

        # === Ayuda ===
        self.btn_help = QPushButton("Ayuda (Discord)")
        self.btn_help.clicked.connect(self.open_help)
        self.layout.addWidget(self.btn_help)

        self.setLayout(self.layout)

    def add_user(self):
        user = self.input_user.text()
        pwd = self.input_pass.text()
        if user and pwd:
            if register_user(user, pwd):
                QMessageBox.information(self, "Éxito", "Usuario creado")
                self.load_users()
                self.input_user.clear()
                self.input_pass.clear()
            else:
                QMessageBox.warning(self, "Error", "Ese usuario ya existe")
        else:
            QMessageBox.warning(self, "Error", "Completa usuario y contraseña")

    def load_users(self):
        self.user_list.clear()
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        for (user,) in cursor.fetchall():
            self.user_list.addItem(user)

    def delete_selected_user(self):
        item = self.user_list.currentItem()
        if item:
            username = item.text()
            conn = connect()
            conn.execute("DELETE FROM users WHERE username = ?", (username,))
            conn.commit()
            QMessageBox.information(self, "Eliminado", f"Usuario {username} eliminado.")
            self.load_users()

    def select_path(self, index, tipo):
        path, _ = QFileDialog.getOpenFileName(self, "Selecciona una app o juego")
        if path:
            self.paths[f"{tipo}_{index}"] = path
            QMessageBox.information(self, "Guardado", f"Ruta guardada para {tipo} #{index+1}")

    def open_help(self):
        import webbrowser
        webbrowser.open("https://discord.com/")  # <-- Cambia por tu link real
