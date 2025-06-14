# ui/games_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from ui.shortcut_grid import ShortcutGrid

class GamesView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Accesos rápidos a juegos"))
        layout.addWidget(ShortcutGrid("games"))
        self.setLayout(layout)
