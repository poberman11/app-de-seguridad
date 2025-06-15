# ui/programs_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QMessageBox
import subprocess
from database.shortcuts import get_shortcuts, update_shortcut

class ProgramsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programas")
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.grid = QGridLayout()
        layout.addLayout(self.grid)

        self.botones = []
        self.programas = get_shortcuts("programs")

        for i, (id, nombre, ruta) in enumerate(self.programas):
            btn = QPushButton(nombre)
            btn.clicked.connect(lambda checked, r=ruta: self.abrir_programa(r))
            self.grid.addWidget(btn, i // 2, i % 2)
            self.botones.append(btn)

    def abrir_programa(self, ruta):
        if not ruta:
            QMessageBox.warning(self, "Sin ruta", "Este botón no tiene programa asignado.")
            return
        try:
            subprocess.Popen(ruta, shell=True)
        except Exception as e:
            QMessageBox.critical(self, "Error al abrir", f"No se pudo abrir:\n{e}")
