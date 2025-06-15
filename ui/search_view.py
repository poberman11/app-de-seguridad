# ui/search_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QLabel, QFileDialog
)
from database.auth import validate_login
from utils.search_files import buscar_archivos

class FileSearchView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Buscar Archivos")
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

        # === Área protegida ===
        self.ruta_input = QLineEdit()
        self.ruta_input.setPlaceholderText("Ruta de carpeta (ej: C:/MisArchivos)")
        self.tipo_input = QLineEdit()
        self.tipo_input.setPlaceholderText("Tipo de archivo (ej: .txt)")

        self.btn_explorar = QPushButton("📁 Explorar")
        self.btn_explorar.clicked.connect(self.seleccionar_carpeta)

        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.buscar)

        self.resultados = QListWidget()

        # Layout protegido
        self.protected_area = QVBoxLayout()
        self.protected_area.addWidget(QLabel("Ruta de búsqueda:"))
        
        ruta_layout = QHBoxLayout()
        ruta_layout.addWidget(self.ruta_input)
        ruta_layout.addWidget(self.btn_explorar)
        self.protected_area.addLayout(ruta_layout)

        self.protected_area.addWidget(QLabel("Tipo de archivo:"))
        self.protected_area.addWidget(self.tipo_input)
        self.protected_area.addWidget(self.btn_buscar)
        self.protected_area.addWidget(QLabel("Resultados:"))
        self.protected_area.addWidget(self.resultados)

        self.protected_widget = QWidget()
        self.protected_widget.setLayout(self.protected_area)
        self.layout.addWidget(self.protected_widget)
        self.protected_widget.setVisible(False)

        self.current_user = None

    def auth(self):
        user = self.auth_user.text()
        pwd = self.auth_pass.text()
        if validate_login(user, pwd):
            self.current_user = user
            self.auth_user.setEnabled(False)
            self.auth_pass.setEnabled(False)
            self.auth_btn.setEnabled(False)
            self.protected_widget.setVisible(True)
        else:
            QMessageBox.warning(self, "Acceso denegado", "Usuario o contraseña incorrectos")

    def seleccionar_carpeta(self):
        ruta = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        if ruta:
            self.ruta_input.setText(ruta)

    def buscar(self):
        ruta = self.ruta_input.text().strip()
        extension = self.tipo_input.text().strip()
        self.resultados.clear()

        if not ruta or not extension:
            QMessageBox.warning(self, "Error", "Debes especificar ruta y tipo de archivo")
            return

        try:
            archivos = buscar_archivos(ruta, extension)
            if archivos:
                for a in archivos:
                    self.resultados.addItem(a)
            else:
                self.resultados.addItem("No se encontraron archivos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Hubo un problema:\n{e}")
