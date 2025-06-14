# === ui/passwords_view.py ===
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel
from database.passwords import add_password, get_passwords, load_key

class PasswordsView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Contraseñas")

        layout = QVBoxLayout()

        # === Tabla de contraseñas ===
        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Contraseña"])
        layout.addWidget(self.table)

        # === Botón Mostrar ===
        self.btn_mostrar = QPushButton("Mostrar")
        self.btn_mostrar.clicked.connect(self.mostrar_passwords)
        layout.addWidget(self.btn_mostrar)

        # === Ingreso de nueva contraseña ===
        ingreso_layout = QHBoxLayout()
        ingreso_layout.addWidget(QLabel("Nueva contraseña:"))
        self.input_password = QLineEdit()
        ingreso_layout.addWidget(self.input_password)
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_password)
        ingreso_layout.addWidget(self.btn_guardar)

        layout.addLayout(ingreso_layout)
        self.setLayout(layout)

    def mostrar_passwords(self):
        self.table.setRowCount(0)
        passwords = get_passwords()
        for row, pw in enumerate(passwords):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(pw))

    def guardar_password(self):
        pw = self.input_password.text().strip()
        if pw:
            add_password(pw)
            self.input_password.clear()
            self.mostrar_passwords()
