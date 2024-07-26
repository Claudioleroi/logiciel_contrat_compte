import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit
)

class FactureTab(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Super Marché Ousmane Ndome")
        self.setGeometry(100, 100, 1000, 600)

        # Layout principal
        layout = QVBoxLayout()

        # Section d'information du client
        client_layout = QHBoxLayout()
        client_layout.addWidget(QLabel("Contact:"))
        self.contact_input = QLineEdit()
        client_layout.addWidget(self.contact_input)

        client_layout.addWidget(QLabel("Nom Client:"))
        self.nom_input = QLineEdit()
        client_layout.addWidget(self.nom_input)

        client_layout.addWidget(QLabel("Email:"))
        self.email_input = QLineEdit()
        client_layout.addWidget(self.email_input)

        layout.addLayout(client_layout)

        # Section de sélection du produit
        produit_layout = QHBoxLayout()
        produit_layout.addWidget(QLabel("Sélectionne Catégorie:"))
        self.categorie_combo = QComboBox()
        self.categorie_combo.addItems(["Vêtement", "Électronique", "Alimentation"])
        produit_layout.addWidget(self.categorie_combo)

        produit_layout.addWidget(QLabel("Sous Catégorie:"))
        self.sous_categorie_combo = QComboBox()
        self.sous_categorie_combo.addItems(["T-Shirt", "Smartphone", "Jus"])
        produit_layout.addWidget(self.sous_categorie_combo)

        produit_layout.addWidget(QLabel("Prix:"))
        self.prix_input = QLineEdit("1500")
        produit_layout.addWidget(self.prix_input)

        produit_layout.addWidget(QLabel("Quantité:"))
        self.quantite_input = QLineEdit("1")
        produit_layout.addWidget(self.quantite_input)

        layout.addLayout(produit_layout)

        # Section de la facture
        self.facture_text = QTextEdit()
        layout.addWidget(self.facture_text)

        # Section des boutons
        boutons_layout = QHBoxLayout()

        self.ajouter_btn = QPushButton("Ajouter Card")
        self.ajouter_btn.clicked.connect(self.ajouter_produit)
        boutons_layout.addWidget(self.ajouter_btn)

        self.generer_btn = QPushButton("Générer")
        self.generer_btn.clicked.connect(self.generer_facture)
        boutons_layout.addWidget(self.generer_btn)

        self.sauvegarde_btn = QPushButton("Sauvegarde Facture")
        self.sauvegarde_btn.clicked.connect(self.sauvegarder_facture)
        boutons_layout.addWidget(self.sauvegarde_btn)

        self.imprimer_btn = QPushButton("Imprimer")
        boutons_layout.addWidget(self.imprimer_btn)

        self.reinitialiser_btn = QPushButton("Réinitialiser")
        self.reinitialiser_btn.clicked.connect(self.reinitialiser)
        boutons_layout.addWidget(self.reinitialiser_btn)

        self.quitter_btn = QPushButton("Quitter")
        self.quitter_btn.clicked.connect(self.close)
        boutons_layout.addWidget(self.quitter_btn)

        layout.addLayout(boutons_layout)

        # Section des totaux
        total_layout = QHBoxLayout()

        total_layout.addWidget(QLabel("Total Bruite:"))
        self.total_bruite_input = QLineEdit()
        self.total_bruite_input.setReadOnly(True)
        total_layout.addWidget(self.total_bruite_input)

        total_layout.addWidget(QLabel("Taxe:"))
        self.taxe_input = QLineEdit()
        self.taxe_input.setReadOnly(True)
        total_layout.addWidget(self.taxe_input)

        total_layout.addWidget(QLabel("Total Net:"))
        self.total_net_input = QLineEdit()
        self.total_net_input.setReadOnly(True)
        total_layout.addWidget(self.total_net_input)

        layout.addLayout(total_layout)

        self.setLayout(layout)

    def ajouter_produit(self):
        # Récupérer les informations sur le produit
        categorie = self.categorie_combo.currentText()
        sous_categorie = self.sous_categorie_combo.currentText()
        prix = float(self.prix_input.text())
        quantite = int(self.quantite_input.text())

        # Calculer le total pour cet article
        total = prix * quantite

        # Ajouter le produit à la zone de facture
        produit_info = f"{sous_categorie} - {quantite} x {prix} = {total}\n"
        self.facture_text.append(produit_info)

        # Mettre à jour le total brut
        total_bruite = self.calculer_total_bruite() + total
        self.total_bruite_input.setText(f"{total_bruite:.2f}")

        # Mettre à jour la taxe et le total net
        taxe = total_bruite * 0.01  # 1% de taxe
        self.taxe_input.setText(f"{taxe:.2f}")
        total_net = total_bruite + taxe
        self.total_net_input.setText(f"{total_net:.2f}")

    def calculer_total_bruite(self):
        # Calculer le total brut actuel
        total_bruite = 0
        for line in self.facture_text.toPlainText().splitlines():
            if line:
                total_bruite += float(line.split('=')[-1])
        return total_bruite

    def generer_facture(self):
        # Afficher la facture dans le champ texte
        facture_details = f"""
        Bienvenu Chez Super Marché Ousmane Ndome
        
        Numéro Facture : 9801
        Nom Client : {self.nom_input.text()}
        Téléphone : {self.contact_input.text()}
        Email : {self.email_input.text()}
        
        Produits
        ***********************************************************
        {self.facture_text.toPlainText()}
        ***********************************************************
        
        Total Bruite : {self.total_bruite_input.text()}
        Taxe : {self.taxe_input.text()}
        Total Net : {self.total_net_input.text()}
        """
        self.facture_text.setText(facture_details)

    def sauvegarder_facture(self):
        # Sauvegarder la facture dans un fichier texte
        facture_details = self.facture_text.toPlainText()
        with open('facture.txt', 'w') as f:
            f.write(facture_details)

    def reinitialiser(self):
        # Réinitialiser tous les champs
        self.contact_input.clear()
        self.nom_input.clear()
        self.email_input.clear()
        self.prix_input.setText("1500")
        self.quantite_input.setText("1")
        self.facture_text.clear()
        self.total_bruite_input.clear()
        self.taxe_input.clear()
        self.total_net_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FactureTab()
    window.show()
    sys.exit(app.exec_())
