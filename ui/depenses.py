import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QDateEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QFileDialog, QComboBox
)
from PyQt5.QtCore import QDate
from openpyxl import Workbook

# Database functions
def create_connection():
    conn = sqlite3.connect('data/expenses.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            source TEXT NOT NULL,
            payment_method TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_expense(date, amount, source, payment_method):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, amount, source, payment_method)
        VALUES (?, ?, ?, ?)
    ''', (date, amount, source, payment_method))
    conn.commit()
    conn.close()

def get_daily_expenses():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_monthly_expenses():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, 
               GROUP_CONCAT(source, ', ') as sources, 
               SUM(amount) as total_amount 
        FROM expenses 
        GROUP BY month 
        ORDER BY month DESC
    ''')
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def convert_month_to_french(month_str):
    # Convert YYYY-MM to Month YYYY
    year, month = month_str.split('-')
    months = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]
    return f"{months[int(month) - 1]} {year}"

# Main UI class
class ExpensesTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Create form fields
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.date.setCalendarPopup(True)  # Enable calendar popup

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Saisir le montant")

        self.source = QLineEdit()
        self.source.setPlaceholderText("Saisir la source")

        # Create a combo box for payment methods
        self.payment_method = QComboBox()
        payment_methods = ["Espèce", "Chèque", "Virement", "Carte Bancaire", "Autre"]
        self.payment_method.addItems(payment_methods)
        self.payment_method.setPlaceholderText("Choisir le mode de paiement")

        # Add form fields to layout
        form_layout.addRow("Date:", self.date)
        form_layout.addRow("Montant:", self.amount)
        form_layout.addRow("Source:", self.source)
        form_layout.addRow("Mode de Paiement:", self.payment_method)

        # Create buttons
        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.save_data)

        self.load_daily_button = QPushButton("Charger Dépenses Quotidiennes")
        self.load_daily_button.clicked.connect(self.load_daily_data)

        self.load_monthly_button = QPushButton("Charger Dépenses Mensuelles")
        self.load_monthly_button.clicked.connect(self.load_monthly_data)

        self.export_button = QPushButton("Exporter en Excel")
        self.export_button.clicked.connect(self.export_to_excel)

        # Create table for displaying data
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable cell editing

        # Add widgets to layout
        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_daily_button)
        layout.addWidget(self.load_monthly_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.setWindowTitle('Gestion des Dépenses')
        self.resize(1000, 700)

        # Create the table if it doesn't exist
        create_table()

    def save_data(self):
        date = self.date.date().toString("yyyy-MM-dd")
        amount = self.amount.text()
        source = self.source.text()
        payment_method = self.payment_method.currentText()  # Get the selected text from the combo box

        if not (amount and source and payment_method):
            QMessageBox.warning(self, 'Données Incomplètes', 'Veuillez remplir tous les champs obligatoires.')
            return

        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, 'Montant Invalide', 'Le montant doit être un nombre.')
            return

        insert_expense(date, amount, source, payment_method)
        QMessageBox.information(self, 'Succès', 'Dépense enregistrée avec succès !')
        self.clear_form()

    def load_daily_data(self):
        expenses = get_daily_expenses()
        self.table.setRowCount(len(expenses))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Montant", "Source", "Mode de Paiement"])

        for row_idx, expense in enumerate(expenses):
            for col_idx, item in enumerate(expense):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

    def load_monthly_data(self):
        expenses = get_monthly_expenses()
        self.table.setRowCount(len(expenses))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Mois", "Sources", "Montant Total"])

        for row_idx, expense in enumerate(expenses):
            month_french = convert_month_to_french(expense[0])
            self.table.setItem(row_idx, 0, QTableWidgetItem(month_french))
            self.table.setItem(row_idx, 1, QTableWidgetItem(expense[1]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(f"{expense[2]:.2f}"))

    def export_to_excel(self):
        expenses = get_daily_expenses()
        if not expenses:
            QMessageBox.warning(self, 'Aucune Donnée', 'Aucune donnée à exporter.')
            return

        # Create a workbook and add a sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Dépenses"

        # Add headers
        headers = ["ID", "Date", "Montant", "Source", "Mode de Paiement"]
        ws.append(headers)

        # Add rows
        for expense in expenses:
            ws.append(expense)

        # Save the workbook
        file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier Excel", "", "Fichiers Excel (*.xlsx)")
        if file_name:
            wb.save(file_name)
            QMessageBox.information(self, 'Exportation Réussie', f'Données exportées vers : {file_name}')

    def clear_form(self):
        self.date.setDate(QDate.currentDate())
        self.amount.clear()
        self.source.clear()
        self.payment_method.setCurrentIndex(0)  # Reset combo box selection to the first item

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExpensesTab()
    window.show()
    sys.exit(app.exec_())
