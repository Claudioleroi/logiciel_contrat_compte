import sys
from PyQt5.QtWidgets import QApplication, QTabWidget, QVBoxLayout, QWidget
from ui.home import HomeTab
from ui.contracts import ContractTab
from ui.accounts import AccountsTab

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create home tab
        self.home_tab = HomeTab()

        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.home_tab, "Accueil")
        self.tabs.addTab(ContractTab(self.home_tab), "Contrats")
        self.tabs.addTab(AccountsTab(), "Tenue des Comptes")

        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.setWindowTitle('Contract Management System')
        self.resize(1000, 700)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
