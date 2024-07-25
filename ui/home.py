from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
import data.database as database

class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Number of signed contracts
        self.contract_count_label = QLabel()
        layout.addWidget(self.contract_count_label)

        # Recent contracts list
        self.recent_contracts_list = QListWidget()
        layout.addWidget(self.recent_contracts_list)

        self.setLayout(layout)
        self.update_home_tab()

    def update_home_tab(self):
        self.contract_count_label.setText(f"Number of signed contracts: {database.get_contract_count()}")
        self.recent_contracts_list.clear()
        contracts = database.get_contracts()
        for contract in contracts[:10]:
            self.recent_contracts_list.addItem(f"ID: {contract[0]} - {contract[1]} signed by {contract[2]} on {contract[6]}")
