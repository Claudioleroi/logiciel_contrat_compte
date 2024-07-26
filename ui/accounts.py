from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from ui.depenses import ExpensesTab
from ui.recettes import RecettesTab
from ui.resultat import ResultatsTab


class AccountsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create individual tabs
        self.expenses_tab = ExpensesTab()
        self.revenues_tab = RecettesTab()
        self.results_tab = ResultatsTab()
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.expenses_tab, "Dépenses")
        self.tab_widget.addTab(self.revenues_tab, "Recettes")
        self.tab_widget.addTab(self.results_tab, "Résultats")
        
        # Add tab widget to layout
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
