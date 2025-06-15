# === ui/config_view.py ===
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog,
    QTabWidget, QGridLayout, QHBoxLayout, QMessageBox
)
from PySide6.QtGui import QIcon
from database.auth import add_user, remove_user, get_users
from database.shortcuts import get_shortcuts, update_shortcut
import os
import sys
if sys.platform.startswith("win"):
    import win32gui
else:
    win32gui = None  # o usa un valor dummy si vas a llamar funciones


class ConfigView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración")
        self.resize(700, 500)

        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        tabs.addTab(self._usuarios_tab(), "Usuarios")
        tabs.addTab(self._shortcuts_tab("main_shortcuts"), "Menú principal")
        tabs.addTab(self._shortcuts_tab("programs"), "Programas")
        tabs.addTab(self._shortcuts_tab("games"), "Juegos")

        layout.addWidget(tabs)

    def _usuarios_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.user_input = QLineEdit()
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Nuevo usuario"))
        layout.addWidget(self.user_input)
        layout.addWidget(QLabel("Nueva contraseña"))
        layout.addWidget(self.pass_input)

        btn_add = QPushButton("Agregar usuario")
        btn_add.clicked.connect(self._agregar_usuario)
        layout.addWidget(btn_add)

        self.remove_user_input = QLineEdit()
        layout.addWidget(QLabel("Eliminar usuario"))
        layout.addWidget(self.remove_user_input)

        btn_remove = QPushButton("Eliminar usuario")
        btn_remove.clicked.connect(self._eliminar_usuario)
        layout.addWidget(btn_remove)

        return widget

    def _shortcuts_tab(self, table):
        widget = QWidget()
        grid = QGridLayout(widget)

        self.shortcut_inputs = {}

        shortcuts = get_shortcuts(table)
        for i, (id_, nombre, ruta) in enumerate(shortcuts):
            name_input = QLineEdit(nombre)
            path_input = QLineEdit(ruta)
            btn_file = QPushButton("...")
            btn_file.clicked.connect(lambda _, i=i, p=path_input: self._explorar_archivo(i, p))
            btn_save = QPushButton("Guardar")
            btn_save.clicked.connect(lambda _, t=table, i=id_, n=name_input, p=path_input: self._guardar_acceso(t, i, n, p))

            grid.addWidget(QLabel(f"Acceso {i+1}"), i, 0)
            grid.addWidget(name_input, i, 1)
            grid.addWidget(path_input, i, 2)
            grid.addWidget(btn_file, i, 3)
            grid.addWidget(btn_save, i, 4)

        return widget

    def _agregar_usuario(self):
        usuario = self.user_input.text()
        clave = self.pass_input.text()
        if usuario and clave:
            add_user(usuario, clave)
            QMessageBox.information(self, "Listo", "Usuario creado")
        else:
            QMessageBox.warning(self, "Error", "Completa usuario y contraseña")

    def _eliminar_usuario(self):
        usuario = self.remove_user_input.text()
        if usuario:
            remove_user(usuario)
            QMessageBox.information(self, "Listo", f"Usuario eliminado: {usuario}")
        else:
            QMessageBox.warning(self, "Error", "Ingresa el usuario a eliminar")

    def _explorar_archivo(self, idx, input_path):
        archivo, _ = QFileDialog.getOpenFileName(self, "Selecciona archivo ejecutable", os.getenv("USERPROFILE"), "Aplicaciones (*.exe)")
        if archivo:
            input_path.setText(archivo)

    def _guardar_acceso(self, tabla, id_, name_input, path_input):
        nombre = name_input.text()
        ruta = path_input.text()
        if nombre and ruta:
            update_shortcut(tabla, id_, nombre, ruta)
            QMessageBox.information(self, "Guardado", f"Acceso actualizado en {tabla}")
        else:
            QMessageBox.warning(self, "Error", "Debes llenar nombre y ruta")
