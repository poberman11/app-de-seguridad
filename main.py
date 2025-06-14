# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui.login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Crear e iniciar la ventana de login
    window = LoginWindow()
    window.showFullScreen()

    sys.exit(app.exec())
