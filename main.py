import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QToolBar,
    QAction, QStyle
)
from PyQt5.QtGui import QIcon

# Assurez-vous d'avoir les modules 'ui.home', 'ui.contracts', 'ui.accounts', 'ui.traitement'
from ui.home import HomeTab
from ui.contracts import ContractTab
from ui.accounts import AccountsTab
from ui.traitement import TraitementTab


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Initialiser la fenêtre principale
        self.setWindowTitle('Contract Management System')
        self.resize(1000, 700)

        # Créer une barre d'outils
        self.toolbar = QToolBar("Barre d'outils principale")
        self.addToolBar(self.toolbar)

        # Créer les onglets principaux
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)  # Positionner les onglets en haut
        self.tabs.setMovable(False)  # Les onglets ne sont pas déplaçables

        self.home_tab = HomeTab()

        # Ajouter les onglets
        self.tabs.addTab(self.home_tab, "Accueil")
        self.tabs.addTab(ContractTab(self.home_tab), "Contrats")
        self.tabs.addTab(TraitementTab(), "Traitement")
        self.tabs.addTab(AccountsTab(), "Comptes")

        # Définir le widget central
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

        # Appliquer le stylesheet pour la personnalisation visuelle
        self.setStyleSheet("""
            QMainWindow {
                color: blue;
            }
            QVBoxLayout {
                background-color: #fff;
            }
            QLabel {
                font-size: 18px;
            }
            QPushButton {
                background-color: #007BFF;
                color: #fff;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTabWidget::pane { 
                border: px solid #0056b3; /* Supprimer la bordure autour du ruban */
            }
            QTabBar {
                background: #B2D2B2; /* Couleur de fond de la barre d'onglets (orange) */
                border: none;
                alignment: center; /* Aligner les onglets au centre */
            }
            QTabBar::tab {
                background-color: #B2D2B2; /* Couleur de fond des onglets (orange) */
                color: white; /* Couleur du texte des onglets */
                min-width: 120px; /* Largeur minimale des onglets */
                padding: 10px; /* Padding à l'intérieur des onglets */
                margin-right: 0px; /* Pas d'espacement entre les onglets */
                border: 1px solid #B2D2B2; /* Bordure pour chaque onglet (même couleur que le ruban) */
                border-top-left-radius: 5px; /* Coins arrondis pour le haut gauche */
                border-top-right-radius: 5px; /* Coins arrondis pour le haut droit */
            }
            QTabBar::tab:selected {
                background-color: white; /* Couleur de fond pour l'onglet sélectionné (blanc) */
                color: #B2D2B2; /* Couleur du texte pour l'onglet sélectionné (orange) */
                border: 1px solid #B2D2B2; /* Bordure orange pour l'onglet sélectionné */
                border-bottom: 1px solid white; /* Supprimer la bordure inférieure pour l'onglet sélectionné */
                border-top-left-radius: 5px; /* Garder les coins arrondis */
                border-top-right-radius: 5px; /* Garder les coins arrondis */
            }
            QTabBar::tab:hover {
                background-color: #FF8C00; /* Couleur de fond pour les onglets au survol (orange foncé) */
            }
            QToolBar {
                background: #B2D2B2; /* Couleur de fond de la barre d'outils */
                spacing: 10px;
            }
            QToolBar QToolButton {
                margin: 5px;
            }
        """)

    def init_toolbar(self):
        # Créer des actions pour la barre d'outils
        # Icones par défaut de PyQt5
        action_new = QAction(self.style().standardIcon(QStyle.SP_FileIcon), 'Nouveau', self)
        action_open = QAction(self.style().standardIcon(QStyle.SP_DirOpenIcon), 'Ouvrir', self)
        action_save = QAction(self.style().standardIcon(QStyle.SP_DriveFDIcon), 'Enregistrer', self)
        action_exit = QAction(self.style().standardIcon(QStyle.SP_DialogCloseButton), 'Quitter', self)

        # Ajouter les actions à la barre d'outils
        self.toolbar.addAction(action_new)
        self.toolbar.addAction(action_open)
        self.toolbar.addAction(action_save)
        self.toolbar.addSeparator()
        self.toolbar.addAction(action_exit)

        # Connecter les actions aux méthodes correspondantes
        action_new.triggered.connect(self.new_file)
        action_open.triggered.connect(self.open_file)
        action_save.triggered.connect(self.save_file)
        action_exit.triggered.connect(self.close)

    def new_file(self):
        print("Créer un nouveau fichier")

    def open_file(self):
        print("Ouvrir un fichier")

    def save_file(self):
        print("Enregistrer le fichier")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
