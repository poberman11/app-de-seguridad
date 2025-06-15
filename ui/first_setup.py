# ui/first_setup.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

from database.auth import register_user
from ui.dashboard import DashboardWindow


class FirstSetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración Inicial")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Configuración Inicial")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Nombre de usuario")

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Contraseña")
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.btn_create = QPushButton("Crear usuario")
        self.btn_create.clicked.connect(self.crear_usuario)

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(self.input_user)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.btn_create)

        self.setLayout(layout)

    def crear_usuario(self):
        usuario = self.input_user.text().strip()
        contraseña = self.input_pass.text().strip()

        if not usuario or not contraseña:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, completa todos los campos.")
            return

        try:
            register_user(usuario, contraseña)
            QMessageBox.information(self, "Usuario creado", "El usuario se ha creado correctamente.")
            self.abrir_dashboard()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear el usuario: {e}")

    def abrir_dashboard(self):
        self.dashboard = DashboardWindow()
        self.dashboard.showMaximized()
        self.close()
