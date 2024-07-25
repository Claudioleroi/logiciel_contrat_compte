from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class AccountsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tenue des Comptes"))
        # Ajouter les widgets de comptes ici
        self.setLayout(layout)
