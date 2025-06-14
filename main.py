# main.py
import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from database.auth import connect, user_exists
from database.shortcuts import init_shortcuts_tables
from ui.login import LoginWindow
from ui.first_setup import FirstSetupWindow  # Asegúrate de tener esta vista

APP_ICON = "assets/icon.png"  # Ajusta si tu ícono está en otra ruta

def main():
    # === Inicialización base ===
    connect()
    init_shortcuts_tables()

    app = QApplication(sys.argv)
    app.setApplicationName("P13 HUB")
    if os.path.exists(APP_ICON):
        app.setWindowIcon(QIcon(APP_ICON))

    # === Mostrar configuración inicial o login ===
    if user_exists():
        ventana = LoginWindow()
    else:
        ventana = FirstSetupWindow()

    ventana.showFullScreen()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
