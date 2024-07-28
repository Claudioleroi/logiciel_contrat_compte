import sys
import sqlite3
import pandas as pd
import plotly.graph_objects as go
from plotly.io import to_image
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QFileDialog, QScrollArea
)
from PyQt5.QtGui import QTextDocument, QImage, QPixmap
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtCore import Qt
from io import BytesIO

# Database functions
def create_connection(database):
    return sqlite3.connect(database)

def get_daily_results():
    conn = create_connection('data/recettes.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date, amount FROM recettes
    ''')
    daily_recettes = cursor.fetchall()
    conn.close()

    conn = create_connection('data/expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date, amount FROM expenses
    ''')
    daily_expenses = cursor.fetchall()
    conn.close()

    daily_results = []
    dates = set([r[0] for r in daily_recettes] + [e[0] for e in daily_expenses])
    for date in sorted(dates):
        recettes = [r[1] for r in daily_recettes if r[0] == date]
        expenses = [e[1] for e in daily_expenses if e[0] == date]
        total_recettes = sum(recettes)
        total_expenses = sum(expenses)
        brut = total_recettes - total_expenses
        taxes = brut * 0.18
        centimes_additionnels = brut * 0.05
        net = brut - taxes - centimes_additionnels
        daily_results.append([date, total_recettes, total_expenses, brut, taxes, centimes_additionnels, net])
    return daily_results

def get_monthly_results():
    conn = create_connection('data/recettes.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, amount FROM recettes
    ''')
    monthly_recettes = cursor.fetchall()
    conn.close()

    conn = create_connection('data/expenses.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT strftime('%Y-%m', date) as month, amount FROM expenses
    ''')
    monthly_expenses = cursor.fetchall()
    conn.close()

    monthly_results = []
    months = set([r[0] for r in monthly_recettes] + [e[0] for e in monthly_expenses])
    month_names = {
        '01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril',
        '05': 'Mai', '06': 'Juin', '07': 'Juillet', '08': 'Août',
        '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
    }
    for month in sorted(months):
        year, month_num = month.split('-')
        month_name = month_names.get(month_num, month_num)
        recettes = [r[1] for r in monthly_recettes if r[0] == month]
        expenses = [e[1] for e in monthly_expenses if e[0] == month]
        total_recettes = sum(recettes)
        total_expenses = sum(expenses)
        brut = total_recettes - total_expenses
        taxes = brut * 0.18
        centimes_additionnels = brut * 0.05
        net = brut - taxes - centimes_additionnels
        monthly_results.append([f'{month_name} {year}', total_recettes, total_expenses, brut, taxes, centimes_additionnels, net])
    return monthly_results

def export_to_excel(filename, daily_data):
    daily_df = pd.DataFrame(daily_data, columns=['Date', 'Recettes', 'Dépenses', 'Résultat Brut', 'Taxes (18%)', 'Centimes Additionnels (5%)', 'Résultat Net'])
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        daily_df.to_excel(writer, sheet_name='Résultats Journaliers', index=False)

# Main UI class
class ResultatsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Graphique
        self.plot_widget = QLabel()
        self.plot_widget.setAlignment(Qt.AlignCenter)

        # Table de résultats
        self.daily_table = QTableWidget()
        self.monthly_table = QTableWidget()
        self.monthly_table.setVisible(False)  # Cacher la table mensuelle au départ

        # Création des QScrollArea pour les tables
        self.daily_table_scroll = QScrollArea()
        self.daily_table_scroll.setWidget(self.daily_table)
        self.daily_table_scroll.setWidgetResizable(True)
        
        self.monthly_table_scroll = QScrollArea()
        self.monthly_table_scroll.setWidget(self.monthly_table)
        self.monthly_table_scroll.setWidgetResizable(True)

        # Boutons
        self.refresh_button = QPushButton("Actualiser")
        self.export_button = QPushButton("Exporter en Excel")
        self.print_button = QPushButton("Imprimer")
        self.show_monthly_button = QPushButton("Afficher Résultats Mensuels")

        # Connexion des boutons
        self.refresh_button.clicked.connect(self.update_results)
        self.export_button.clicked.connect(self.export_results)
        self.print_button.clicked.connect(self.print_results)
        self.show_monthly_button.clicked.connect(self.show_monthly_results)

        # Layout pour le graphique et le tableau
        graph_table_layout = QHBoxLayout()
        graph_table_layout.addWidget(self.plot_widget)
        graph_table_layout.addWidget(self.daily_table_scroll)

        # Ajout des widgets au layout principal
        layout.addLayout(graph_table_layout)
        layout.addWidget(self.show_monthly_button)
        layout.addWidget(self.monthly_table_scroll)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.print_button)

        self.setLayout(layout)
        self.setWindowTitle('Résultats')
        self.resize(800, 600)

        self.update_results()

    def update_results(self):
        try:
            daily_data = get_daily_results()
            self.update_table(self.daily_table, daily_data, ['Date', 'Recettes', 'Dépenses', 'Résultat Brut', 'Taxes (18%)', 'Centimes Additionnels (5%)', 'Résultat Net'])
            self.plot_daily_results(daily_data)
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f"Une erreur est survenue : {e}")

    def update_table(self, table, data, headers):
        table.setRowCount(len(data))
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        for row_idx, row_data in enumerate(data):
            for col_idx, cell_data in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(f"{cell_data:.2f}" if isinstance(cell_data, (int, float)) else cell_data))

    def plot_daily_results(self, data):
        fig = go.Figure()
        dates = [row[0] for row in data]
        recettes = [row[1] for row in data]
        expenses = [row[2] for row in data]

        fig.add_trace(go.Bar(x=dates, y=recettes, name='Recettes', marker_color='skyblue'))
        fig.add_trace(go.Bar(x=dates, y=expenses, name='Dépenses', marker_color='red'))

        fig.update_layout(
            title='Résultats Journaliers',
            xaxis_title='Date',
            yaxis_title='Montant',
            barmode='group'
        )

        # Convertir le graphique en image PNG
        image_bytes = to_image(fig, format='png')
        image = QImage.fromData(image_bytes)

        # Afficher l'image dans le QLabel
        pixmap = QPixmap.fromImage(image)
        self.plot_widget.setPixmap(pixmap)

    def show_monthly_results(self):
        try:
            monthly_data = get_monthly_results()
            self.update_table(self.monthly_table, monthly_data, ['Mois', 'Recettes', 'Dépenses', 'Résultat Brut', 'Taxes (18%)', 'Centimes Additionnels (5%)', 'Résultat Net'])
            self.plot_monthly_results(monthly_data)
            self.monthly_table.setVisible(True)  # Afficher la table mensuelle
        except Exception as e:
            QMessageBox.critical(self, 'Erreur', f"Une erreur est survenue : {e}")

    def plot_monthly_results(self, data):
        fig = go.Figure()
        months = [row[0] for row in data]
        recettes = [row[1] for row in data]
        expenses = [row[2] for row in data]

        fig.add_trace(go.Bar(x=months, y=recettes, name='Recettes', marker_color='skyblue'))
        fig.add_trace(go.Bar(x=months, y=expenses, name='Dépenses', marker_color='red'))

        fig.update_layout(
            title='Résultats Mensuels',
            xaxis_title='Mois',
            yaxis_title='Montant',
            barmode='group'
        )

        # Convertir le graphique en image PNG
        image_bytes = to_image(fig, format='png')
        image = QImage.fromData(image_bytes)

        # Afficher l'image dans le QLabel
        pixmap = QPixmap.fromImage(image)
        self.plot_widget.setPixmap(pixmap)

    def export_results(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier Excel", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if filename:
            daily_data = get_daily_results()
            export_to_excel(filename, daily_data)

    def print_results(self):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            document = QTextDocument()
            html = self.table_to_html(self.daily_table)
            document.setHtml(html)
            document.print_(printer)

    def table_to_html(self, table):
        rows = table.rowCount()
        columns = table.columnCount()
        html = "<table border='1'><tr>"
        for col in range(columns):
            html += f"<th>{table.horizontalHeaderItem(col).text()}</th>"
        html += "</tr>"
        for row in range(rows):
            html += "<tr>"
            for col in range(columns):
                item = table.item(row, col)
                html += f"<td>{item.text() if item else ''}</td>"
            html += "</tr>"
        html += "</table>"
        return html

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ResultatsTab()
    window.show()
    sys.exit(app.exec_())
