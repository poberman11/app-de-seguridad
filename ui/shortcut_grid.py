# ui/shortcut_grid.py
import os
import subprocess
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QPushButton, QFileDialog, QLabel
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from database.shortcuts import get_shortcuts, update_shortcut


def get_icon_from_exe(ruta):
    if os.path.exists(ruta):
        return QIcon(ruta)
    return QIcon()  # Ícono por defecto


class ShortcutGrid(QWidget):
    def __init__(self, tabla):
        super().__init__()
        self.tabla = tabla
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.grid = QGridLayout()

        self.botones = []
        self.shortcuts = get_shortcuts(self.tabla)

        for i, (id_, nombre, ruta) in enumerate(self.shortcuts):
            btn = QPushButton(nombre)
            btn.setIcon(get_icon_from_exe(ruta))
            btn.setIconSize(QSize(64, 64))
            btn.setFixedSize(120, 120)
            btn.setToolTip(ruta)

            btn.clicked.connect(lambda checked, r=ruta: self.ejecutar(r))
            btn.setContextMenuPolicy(3)  # CustomContextMenu
            btn.customContextMenuRequested.connect(lambda pos, b=btn, i=id_: self.configurar_acceso(i, b))

            self.grid.addWidget(btn, i // 4, i % 4)
            self.botones.append(btn)

        layout.addLayout(self.grid)
        self.setLayout(layout)

    def ejecutar(self, ruta):
        if ruta and os.path.exists(ruta):
            try:
                subprocess.Popen(ruta, shell=True)
            except Exception as e:
                print(f"Error al ejecutar: {e}")

    def configurar_acceso(self, id_acceso, boton):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo .exe", "", "Ejecutables (*.exe)")
        if archivo:
            nombre = os.path.basename(archivo)
            update_shortcut(self.tabla, id_acceso, nombre, archivo)
            boton.setText(nombre)
            boton.setIcon(get_icon_from_exe(archivo))
            boton.setToolTip(archivo)
