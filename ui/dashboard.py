# ui/dashboard.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P13 HUB - Menú Principal")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # === Barra lateral ===
        self.sidebar = QVBoxLayout()
        self.sidebar.setAlignment(Qt.AlignTop)

        self.label_menu = QLabel("Menú")
        self.label_menu.setFont(QFont("Arial", 16, QFont.Bold))
        self.label_menu.setAlignment(Qt.AlignCenter)

        self.btn_games = QPushButton("🎮 Juegos")
        self.btn_programs = QPushButton("🖥️ Programas")
        self.btn_passwords = QPushButton("🔒 Contraseñas")
        self.btn_filesearch = QPushButton("📁 Buscar Archivos")
        self.btn_settings = QPushButton("⚙️ Configuración")
        self.btn_lock = QPushButton("🔒 Bloquear")

        # Añadir a barra lateral
        for widget in [
            self.label_menu, self.btn_games, self.btn_programs,
            self.btn_passwords, self.btn_filesearch,
            self.btn_settings, self.btn_lock
        ]:
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.sidebar.addWidget(widget)

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(self.sidebar)
        sidebar_widget.setFixedWidth(180)

        # === Contenido dinámico ===
        self.main_area = QStackedWidget()
        self.placeholder = QLabel("Aquí aparecerá el contenido")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.main_area.addWidget(self.placeholder)

        # === Layout general ===
        main_layout = QHBoxLayout()
        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.main_area)

        central_widget.setLayout(main_layout)

        # === Conexiones ===
        self.btn_lock.clicked.connect(self.lock_screen)

    def lock_screen(self):
        from ui.login import LoginWindow
        self.login = LoginWindow()
        self.login.showFullScreen()
        self.close()
