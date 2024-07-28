import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from openpyxl import Workbook
import plotly.graph_objects as go
import plotly.io as pio
import data.database as database  # Assurez-vous que ce module est disponible

class HomeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create buttons layout
        button_layout = QHBoxLayout()
        
        # Create Export button
        self.export_button = QPushButton("Export to Excel")
        self.export_button.clicked.connect(self.export_to_excel)
        button_layout.addWidget(self.export_button)

        # Create Delete Selected button
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setEnabled(False)  # Initially disabled
        self.delete_button.clicked.connect(self.delete_selected_row)
        button_layout.addWidget(self.delete_button)

        # Add buttons layout to main layout
        layout.addLayout(button_layout)

        # Create table for displaying data
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Contract Name", "Author", "Recipient", "Date Signed", "Amount"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable cell editing
        self.table.selectionModel().selectionChanged.connect(self.update_delete_button_state)  # Connect selection change
        layout.addWidget(self.table)

        # Create graphs
        self.graphs_layout = QHBoxLayout()
        self.expense_chart = QWebEngineView()
        self.revenue_chart = QWebEngineView()
        self.graphs_layout.addWidget(self.expense_chart)
        self.graphs_layout.addWidget(self.revenue_chart)
        layout.addLayout(self.graphs_layout)

        self.setLayout(layout)
        self.update_home_tab()

    def update_home_tab(self):
        # Update table with all contracts
        self.update_table()
        # Update graphs
        self.update_graphs()

    def update_table(self):
        contracts = database.get_contracts()
        self.table.setRowCount(len(contracts))

        for row_idx, contract in enumerate(contracts):
            for col_idx, item in enumerate(contract):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def update_graphs(self):
        # Plot expense categories as a pie chart
        expense_categories = database.get_expense_categories()
        expense_sources = [row[0] for row in expense_categories]
        expense_amounts = [row[1] for row in expense_categories]

        expense_pie_chart = go.Figure(data=[go.Pie(labels=expense_sources, values=expense_amounts)])
        expense_pie_chart.update_layout(title_text='Répartition des Dépenses')

        # Convert plotly graph to HTML and display in QWebEngineView
        expense_pie_chart_html = pio.to_html(expense_pie_chart, full_html=False)
        self.expense_chart.setHtml(expense_pie_chart_html)

        # Plot revenue sources as a pie chart
        revenue_sources = database.get_revenue_sources()
        revenue_labels = [row[0] for row in revenue_sources]
        revenue_amounts = [row[1] for row in revenue_sources]

        revenue_pie_chart = go.Figure(data=[go.Pie(labels=revenue_labels, values=revenue_amounts)])
        revenue_pie_chart.update_layout(title_text='Répartition des Revenus')

        # Convert plotly graph to HTML and display in QWebEngineView
        revenue_pie_chart_html = pio.to_html(revenue_pie_chart, full_html=False)
        self.revenue_chart.setHtml(revenue_pie_chart_html)

    def export_to_excel(self):
        contracts = database.get_contracts()
        if not contracts:
            QMessageBox.warning(self, 'No Data', 'No data to export.')
            return

        # Create a workbook and add a sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Contracts"

        # Add headers
        headers = [
            "ID", "Contract Name", "Author", "Recipient", "Date Signed", "Amount"
        ]
        ws.append(headers)

        # Add rows
        for contract in contracts:
            ws.append(contract)

        # Save the workbook
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Excel File", "", "Excel Files (*.xlsx)")
        if file_name:
            wb.save(file_name)
            QMessageBox.information(self, 'Export Successful', f'Data exported to: {file_name}')

    def delete_selected_row(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, 'No Selection', 'Please select a row to delete.')
            return

        for row in selected_rows:
            row_id = self.table.item(row.row(), 0).text()  # ID is in the first column
            reply = QMessageBox.question(self, 'Confirm Delete', 
                                         f'Are you sure you want to delete the row with ID {row_id}?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                database.delete_contract(row_id)
                self.update_table()
                QMessageBox.information(self, 'Success', 'Row deleted successfully!')
            else:
                QMessageBox.information(self, 'Cancelled', 'Deletion cancelled.')

    def update_delete_button_state(self):
        selected_rows = self.table.selectionModel().selectedRows()
        self.delete_button.setEnabled(bool(selected_rows))  # Enable if any row is selected

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomeTab()
    window.show()
    sys.exit(app.exec_())
