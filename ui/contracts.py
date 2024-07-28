from PyQt5.QtWidgets import QWidget, QVBoxLayout
from widgets.contract_generator import ContractGenerator

class ContractTab(QWidget):
    def __init__(self, home_tab):
        super().__init__()
        self.home_tab = home_tab
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add contract generator widget
        self.contract_generator = ContractGenerator()
        self.contract_generator.contract_generated.connect(self.home_tab.update_home_tab)  # Connect the signal
        layout.addWidget(self.contract_generator)

        self.setLayout(layout)
