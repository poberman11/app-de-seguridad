# ui/login.py
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QHBoxLayout
)
from PySide6.QtGui import QFont
from database.auth import user_exists, register_user, validate_login
from PySide6.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P13 HUB - Inicio de sesión")

        # Widgets
        self.label_title = QLabel("P13 HUB - Seguridad")
        self.label_title.setFont(QFont("Arial", 24, QFont.Bold))

        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Usuario")

        self.input_pass = QLineEdit()
        self.input_pass.setPlaceholderText("Contraseña")
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Iniciar sesión")
        self.btn_login.clicked.connect(self.check_login)

        # Si es el primer uso, cambia botón
        if not user_exists():
            self.btn_login.setText("Registrar usuario inicial")
            self.btn_login.clicked.disconnect()
            self.btn_login.clicked.connect(self.create_initial_user)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addSpacing(20)
        layout.addWidget(self.input_user)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.btn_login)

        container = QWidget()
        container.setLayout(layout)

        # Centrar todo
        outer = QHBoxLayout(self)
        outer.addStretch()
        outer.addWidget(container)
        outer.addStretch()

        layout.setContentsMargins(100, 100, 100, 100)
        self.setLayout(outer)

    def check_login(self):
        username = self.input_user.text()
        password = self.input_pass.text()

        if validate_login(username, password):
            self.accepted()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")

    def create_initial_user(self):
        username = self.input_user.text()
        password = self.input_pass.text()

        if username and password:
            if register_user(username, password):
                QMessageBox.information(self, "Éxito", "Usuario creado, ya puedes iniciar sesión.")
                self.btn_login.setText("Iniciar sesión")
                self.btn_login.clicked.disconnect()
                self.btn_login.clicked.connect(self.check_login)
            else:
                QMessageBox.warning(self, "Error", "Ese nombre de usuario ya existe.")
        else:
            QMessageBox.warning(self, "Error", "Debes ingresar usuario y contraseña.")

    def accepted(self):
        from ui.dashboard import DashboardWindow
        self.dashboard = DashboardWindow()

        # Restaurar ventana antes de mostrar
        self.dashboard.showMaximized()
        self.dashboard.setWindowFlag(Qt.FramelessWindowHint, False)
        self.dashboard.setWindowFlag(Qt.WindowStaysOnTopHint, False)
        self.dashboard.show()  # o showMaximized() si prefieres

        self.close()
