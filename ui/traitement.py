import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton,
    QDateEdit, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QFileDialog
)
from PyQt5.QtCore import QDate, QTime
from openpyxl import Workbook

# Database functions
def create_connection():
    conn = sqlite3.connect('data/traitement.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            code_journal TEXT NOT NULL,
            auteur TEXT NOT NULL,
            destinataire TEXT NOT NULL,
            devise TEXT NOT NULL,
            libelles TEXT,
            num_piece TEXT,
            montant REAL NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_transaction(code_journal, auteur, destinataire, devise, libelles, num_piece, montant, date, time):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (code_journal, auteur, destinataire, devise, libelles, num_piece, montant, date, time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (code_journal, auteur, destinataire, devise, libelles, num_piece, montant, date, time))
    conn.commit()
    conn.close()

def get_transactions():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions ORDER BY date DESC, time DESC')
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def delete_transaction(transaction_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()

# Main UI class
class TraitementTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Create form fields
        self.code_journal = QComboBox()
        self.code_journal.addItems(["ACH", "DEP", "VEN"])
        self.auteur = QLineEdit()
        self.destinataire = QLineEdit()
        self.devise = QLineEdit("Franc CFA")
        self.libelles = QLineEdit()
        self.num_piece = QLineEdit()
        self.montant = QLineEdit()
        self.montant.setPlaceholderText("Enter amount")
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.date.setCalendarPopup(True)  # Enable calendar popup

        # Add form fields to layout
        form_layout.addRow("Code Journal:", self.code_journal)
        form_layout.addRow("Auteur:", self.auteur)
        form_layout.addRow("Destinataire:", self.destinataire)
        form_layout.addRow("Devise:", self.devise)
        form_layout.addRow("Libellés:", self.libelles)
        form_layout.addRow("Numéro de la pièce:", self.num_piece)
        form_layout.addRow("Montant:", self.montant)
        form_layout.addRow("Date:", self.date)

        # Create buttons
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_data)
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        self.export_button = QPushButton("Export to Excel")
        self.export_button.clicked.connect(self.export_to_excel)
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected_row)

        # Create table for displaying data
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Code Journal", "Auteur", "Destinataire", "Devise", "Libellés", "Numéro de la pièce", "Montant", "Date", "Time"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable cell editing

        # Add widgets to layout
        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.setWindowTitle('Traitement')
        self.resize(1000, 700)

        # Create the table if it doesn't exist
        create_table()

    def save_data(self):
        code_journal = self.code_journal.currentText()
        auteur = self.auteur.text()
        destinataire = self.destinataire.text()
        devise = self.devise.text()
        libelles = self.libelles.text()
        num_piece = self.num_piece.text()
        montant = self.montant.text()
        date = self.date.date().toString("yyyy-MM-dd")
        time = QTime.currentTime().toString("HH:mm:ss")  # Include seconds in time

        if not (auteur and destinataire and devise and montant and date):
            QMessageBox.warning(self, 'Incomplete Data', 'Please fill in all required fields.')
            return

        try:
            insert_transaction(code_journal, auteur, destinataire, devise, libelles, num_piece, montant, date, time)
            QMessageBox.information(self, 'Success', 'Data saved successfully!')
            self.clear_fields()  # Clear fields after saving
            self.load_data()  # Reload the data
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while saving data: {str(e)}')

    def load_data(self):
        try:
            transactions = get_transactions()
            self.table.setRowCount(len(transactions))

            for row_idx, transaction in enumerate(transactions):
                for col_idx, item in enumerate(transaction):
                    self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while loading data: {str(e)}')

    def export_to_excel(self):
        transactions = get_transactions()
        if not transactions:
            QMessageBox.warning(self, 'No Data', 'No data to export.')
            return

        # Create a workbook and add a sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Transactions"

        # Add headers
        headers = [
            "ID", "Code Journal", "Auteur", "Destinataire", "Devise", "Libellés", "Numéro de la pièce", "Montant", "Date", "Time"
        ]
        ws.append(headers)

        # Add rows
        for transaction in transactions:
            ws.append(transaction)

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
                try:
                    delete_transaction(row_id)
                    self.load_data()
                    QMessageBox.information(self, 'Success', 'Row deleted successfully!')
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'An error occurred while deleting the row: {str(e)}')
            else:
                QMessageBox.information(self, 'Cancelled', 'Deletion cancelled.')

    def clear_fields(self):
        self.code_journal.setCurrentIndex(0)
        self.auteur.clear()
        self.destinataire.clear()
        self.devise.setText("Franc CFA")
        self.libelles.clear()
        self.num_piece.clear()
        self.montant.clear()
        self.date.setDate(QDate.currentDate())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TraitementTab()
    window.show()
    sys.exit(app.exec_())
