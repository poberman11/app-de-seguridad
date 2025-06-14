# ui/passwords_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QListWidget, QLabel
)
from database.passwords import add_password, get_passwords
from database.auth import validate_user

class PasswordsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Contraseñas")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # === Autenticación ===
        self.auth_user = QLineEdit()
        self.auth_user.setPlaceholderText("Usuario")
        self.auth_pass = QLineEdit()
        self.auth_pass.setPlaceholderText("Contraseña")
        self.auth_pass.setEchoMode(QLineEdit.Password)

        self.auth_btn = QPushButton("Entrar")
        self.auth_btn.clicked.connect(self.auth)

        self.layout.addWidget(QLabel("Ingresa usuario y contraseña para acceder:"))
        self.layout.addWidget(self.auth_user)
        self.layout.addWidget(self.auth_pass)
        self.layout.addWidget(self.auth_btn)

        # === Área protegida (oculta al principio) ===
        self.password_list = QListWidget()
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Nueva contraseña")

        self.btn_save = QPushButton("Guardar")
        self.btn_show = QPushButton("Mostrar")

        self.btn_save.clicked.connect(self.save_password)
        self.btn_show.clicked.connect(self.show_passwords)

        self.protected_area = QVBoxLayout()
        self.protected_area.addWidget(QLabel("Contraseñas guardadas:"))
        self.protected_area.addWidget(self.password_list)

        self.input_area = QHBoxLayout()
        self.input_area.addWidget(self.password_input)
        self.input_area.addWidget(self.btn_save)

        self.protected_area.addLayout(self.input_area)
        self.protected_area.addWidget(self.btn_show)

        # Contenedor
        self.protected_container = QWidget()
        self.protected_container.setLayout(self.protected_area)
        self.layout.addWidget(self.protected_container)

        self.protected_container.setVisible(False)
        self.current_user = None

    def auth(self):
        user = self.auth_user.text()
        pwd = self.auth_pass.text()
        if validate_user(user, pwd):
            self.current_user = user
            self.auth_user.setEnabled(False)
            self.auth_pass.setEnabled(False)
            self.auth_btn.setEnabled(False)
            self.protected_container.setVisible(True)
        else:
            QMessageBox.warning(self, "Acceso denegado", "Usuario o contraseña incorrectos")

    def save_password(self):
        pwd = self.password_input.text()
        if pwd:
            add_password(self.current_user, pwd)
            self.password_input.clear()
            self.show_passwords()
        else:
            QMessageBox.warning(self, "Error", "Ingresa una contraseña para guardar")

    def show_passwords(self):
        self.password_list.clear()
        for p in get_passwords(self.current_user):
            self.password_list.addItem(p)
