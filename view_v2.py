# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:46:23 2019

@author: nayab
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import random
from functions import *
from controler import Controler
import sys
import datetime as dt
import matplotlib.dates as mdates



# =============================================================================
# Fenetres Principal

class MainWindow(QMainWindow):
    def __init__(self, controler):
        super().__init__()
        self.setWindowTitle("Gestion du porte-monnaie")
        # self.mainwidget = MainWidget(self, controler)
        self.mainwidget = MyTableWidget(self, controler)
        self.setCentralWidget(self.mainwidget)


# =============================================================================
# Widget pour créer de fenêtres
class MyTableWidget(QWidget):

    def __init__(self, parent, controler):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.setUsesScrollButtons(True)
        self.tab1 = Info_compte_tab(self, controler)
        self.tab2 = Budget_tab(self, controler)
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        #        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Information compte")
        self.tabs.addTab(self.tab2, "Actions compte")
        self.tabs.addTab(self.tab3, "Bourse (par exemple)")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


########################################################################################################################
################################################# TAB: Info Compte #####################################################
########################################################################################################################

class Info_compte_tab(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.setMinimumSize(700, 500)
        # widgets
        self.actionwidget = ActionWidget(self, controler)
        self.informationwidget = InformationWidget(self, controler)
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.actionwidget)
        layoutH.addWidget(self.informationwidget)
        self.setLayout(layoutH)


# ======================================================================================================================

# Widget contenent les boutons des actions disponible pour un compte
class ActionWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
        self.setMaximumWidth(200)
        # initialisation de la fenetre d'action
        self.fenetre = None
        if self.controler.compte != None:
            pass
        else:
            self.ouvrir_select_compte()
        # widgets
        self.infocompte = QLabel("<b>Compte</b><br/><i>Type</i><br/>Montant")
        self.infocompte.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.infocompte.setLineWidth(3)
        self.infocompte.setFixedSize(180, 60)
        self.button_ajouterdepense = QPushButton("Ajouter une dépense")
        self.button_ajoutergain = QPushButton("Ajouter un gain")
        self.button_virementauto = QPushButton("Virement automatique")
        self.button_virementcomptes = QPushButton("Virement entre comptes")
        self.button_ajouterbudget = QPushButton("Ajouter budget")
        self.button_acheteraction = QPushButton("Acheter actions")
        self.button_vendreaction = QPushButton("Vendre actions")
        self.button_changercompte = QPushButton("Changer compte")
        self.button_supprimercompte = QPushButton("Supprimer compte")
        # layouts
        layoutV = QVBoxLayout()
        layoutV1 = QVBoxLayout()
        layoutV1.addWidget(self.button_ajouterdepense)
        layoutV1.addWidget(self.button_ajoutergain)
        layoutV1.addWidget(self.button_virementauto)
        layoutV1.addWidget(self.button_virementcomptes)
        layoutV1.addWidget(self.button_ajouterbudget)
        layoutV1.addWidget(self.button_acheteraction)
        layoutV1.addWidget(self.button_vendreaction)
        layoutV.addWidget(self.infocompte)
        layoutV.addLayout(layoutV1)
        layoutV.addWidget(self.button_changercompte)
        layoutV.addWidget(self.button_supprimercompte)
        layoutV.setAlignment(self.infocompte, Qt.AlignTop)
        layoutV.setAlignment(self.button_changercompte, Qt.AlignBottom)
        self.setLayout(layoutV)
        # connecter les boutons
        self.button_changercompte.clicked.connect(self.ouvrir_select_compte)
        self.button_supprimercompte.clicked.connect(self.ouvrir_supprime_compte)
        self.button_ajouterdepense.clicked.connect(self.ajouter_depense)
        self.button_ajoutergain.clicked.connect(self.ajouter_gain)

    def ouvrir_select_compte(self):
        self.fenetre = SelectCompte(None, self.controler)
        self.fenetre.setWindowModality(Qt.ApplicationModal)
        self.fenetre.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre.show()

    def ouvrir_supprime_compte(self):
        self.fenetre = SupprimeCompte(None, self.controler, self)
        self.fenetre.setWindowModality(Qt.ApplicationModal)
        self.fenetre.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre.show()

    def ajouter_depense(self):
        self.fenetre_temp = Ajouter_depense(None, self.controler)
        self.fenetre_temp.setWindowModality(Qt.ApplicationModal)
        self.fenetre_temp.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre_temp.show()

    def ajouter_gain(self):
        self.fenetre_temp = Ajouter_gain(None, self.controler)
        self.fenetre_temp.setWindowModality(Qt.ApplicationModal)
        self.fenetre_temp.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre_temp.show()

    def refresh(self):
        try:
            self.infocompte.setText("<b>{}</b><br/><i>{}</i><br/>{:,.2f} €".
                                    format(self.controler.compte.name,
                                           self.controler.compte.type,
                                           self.controler.compte.balance))
        except:
            pass


# ======================================================================================================================

class SelectCompte(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.setFixedSize(300, 150)
        # Page 1: choisir compte
        # widgets
        self.titre1 = QLabel("<b>Selectionner un compte</b>")
        self.titre1.setAlignment(Qt.AlignCenter)
        self.titre1.setMaximumHeight(20)
        self.menu_deroulant = QComboBox()
        self.menu_deroulant.addItems([c.name
                                      for c in controler.liste_comptes])
        self.button_valider = QPushButton("Acceder au compte")
        self.button_new = QPushButton("Nouveau compte")
        self.button_new.setMaximumWidth(200)
        # layouts
        layoutV = QVBoxLayout()
        layoutV1 = QVBoxLayout()
        layoutV1.addWidget(self.titre1)
        layoutV1.addWidget(self.menu_deroulant)
        layoutV1.addWidget(self.button_valider)
        layoutV.addLayout(layoutV1)
        layoutV.addWidget(self.button_new)
        layoutV.setAlignment(self.button_new, Qt.AlignCenter)
        # connecter les boutons
        self.button_valider.clicked.connect(self.click_valider)
        self.button_new.clicked.connect(self.click_new)
        # Page 2: creer compte
        # widgets
        self.titre2 = QLabel("<b>Création d'un nouveau compte</b>")
        self.label_nom = QLabel("Nom du compte:")
        self.label_type = QLabel("Type du compte:")
        self.label_montant = QLabel("Montant initial (€):")
        self.label_credit = QLabel("Credit possible (€):")
        self.label_interet = QLabel("Intéret sur le crédit (%/mois):")
        self.label_erreur = QLabel("")
        self.text_nom = QLineEdit()
        self.text_type = QLineEdit()
        self.text_montant = QLineEdit()
        self.text_montant.setValidator(QDoubleValidator())
        self.text_credit = QLineEdit("Optionnel")
        self.text_credit.setValidator(QDoubleValidator())
        self.text_interet = QLineEdit("Optionnel")
        self.text_interet.setValidator(QDoubleValidator(0.0, 100.0, 2))
        self.button_creer = QPushButton("Créer")
        self.button_creer.setStyleSheet('font: bold')
        self.button_retour = QPushButton("Retour")
        # layouts
        layoutG = QGridLayout()
        layoutG.addWidget(self.titre2, 0, 0, 1, 2)
        layoutG.setAlignment(self.titre2, Qt.AlignCenter)
        layoutG.addWidget(self.label_nom, 1, 0)
        layoutG.setAlignment(self.label_nom, Qt.AlignRight)
        layoutG.addWidget(self.label_type, 2, 0)
        layoutG.setAlignment(self.label_type, Qt.AlignRight)
        layoutG.addWidget(self.label_montant, 3, 0)
        layoutG.setAlignment(self.label_montant, Qt.AlignRight)
        layoutG.addWidget(self.label_credit, 5, 0)
        layoutG.setAlignment(self.label_credit, Qt.AlignRight)
        layoutG.addWidget(self.label_interet, 6, 0)
        layoutG.setAlignment(self.label_interet, Qt.AlignRight)
        layoutG.addWidget(self.text_nom, 1, 1)
        layoutG.addWidget(self.text_type, 2, 1)
        layoutG.addWidget(self.text_montant, 3, 1)
        layoutG.addWidget(self.text_credit, 5, 1)
        layoutG.addWidget(self.text_interet, 6, 1)
        layoutG.addWidget(self.button_retour, 7, 0)
        layoutG.addWidget(self.button_creer, 7, 1)
        layoutG.addWidget(self.label_erreur, 4, 1)
        layoutG.setAlignment(self.button_creer, Qt.AlignCenter)
        # connecter les boutons
        self.button_creer.clicked.connect(self.click_creer)
        self.button_retour.clicked.connect(self.click_retour)
        # Layout stacked
        self.layoutS = QStackedLayout()
        page1 = QWidget()
        page1.setLayout(layoutV)
        page2 = QWidget()
        page2.setLayout(layoutG)
        self.layoutS.addWidget(page1)
        self.layoutS.addWidget(page2)
        self.setLayout(self.layoutS)

    def click_valider(self):
        self.controler.select_compte_from_index(
            self.menu_deroulant.currentIndex())
        self.close()

    def click_new(self):
        self.setFixedSize(400, 250)
        self.layoutS.setCurrentIndex(1)

    def click_creer(self):
        if self.controler.nouveau_compte(self.text_nom.text(),
                                         self.text_type.text(),
                                         self.text_montant.text(),
                                         self.text_credit.text(),
                                         self.text_interet.text()):
            self.close()
        else:
            self.label_erreur.setText(
                "<b><p style='color:red;'>Informations Manquantes")

    def click_retour(self):
        self.setFixedSize(300, 150)
        self.layoutS.setCurrentIndex(0)


# ======================================================================================================================

class SupprimeCompte(QWidget):
    def __init__(self, parent, controler, main_widget):
        super().__init__(parent)
        self.controler = controler
        self.main_widget = main_widget
        self.setFixedSize(250, 100)
        # widgets
        self.label = QLabel("Supprimer le compte <b>{}</b>".
                            format(self.controler.compte.name))
        self.button_oui = QPushButton("OUI")
        self.button_non = QPushButton("NON")
        self.button_non.setStyleSheet('font: bold')
        # layouts
        layoutV = QVBoxLayout()
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.button_non)
        layoutH.addWidget(self.button_oui)
        layoutV.addWidget(self.label)
        layoutV.setAlignment(self.label, Qt.AlignCenter)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)
        # connecter les boutons
        self.button_oui.clicked.connect(self.click_oui)
        self.button_non.clicked.connect(self.click_non)

    def click_oui(self):
        self.controler.delete_compte()
        self.close()
        self.main_widget.ouvrir_select_compte()

    def click_non(self):
        self.close()


# ======================================================================================================================

class Ajouter_depense(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.setFixedSize(300, 200)
        # Page 1: choisir compte
        # widgets
        self.titre1 = QLabel("<b>Ajout Depense</b>")
        self.titre1.setAlignment(Qt.AlignCenter)
        self.titre1.setMaximumHeight(20)

        # date, commentaire, entreprise
        self.label_montant = QLabel('Montant (euros)')
        self.label_montant.setAlignment(Qt.AlignVCenter)
        self.label_montant.resize(200, 100)
        self.label_montant.resize(self.label_montant.sizeHint())

        self.label_categorie = QLabel('Catégorie')
        self.label_categorie.setAlignment(Qt.AlignVCenter)
        self.label_categorie.resize(200, 100)
        self.label_categorie.resize(self.label_categorie.sizeHint())

        self.label_date = QLabel('Date')
        self.label_date.setAlignment(Qt.AlignVCenter)
        self.label_date.resize(200, 100)
        self.label_date.resize(self.label_date.sizeHint())

        self.label_commentaire = QLabel('Commentaire')
        self.label_commentaire.setAlignment(Qt.AlignVCenter)
        self.label_commentaire.resize(200, 100)
        self.label_commentaire.resize(self.label_commentaire.sizeHint())

        self.label_entreprise = QLabel('Entreprise')
        self.label_entreprise.setAlignment(Qt.AlignVCenter)
        self.label_entreprise.resize(200, 100)
        self.label_entreprise.resize(self.label_entreprise.sizeHint())

        # We create text box for the user to enter values of the sample
        self.montant_box = QLineEdit(self)
        self.montant_box.setAlignment(Qt.AlignVCenter)
        self.montant_box.resize(200, 100)
        self.montant_box.resize(self.montant_box.sizeHint())

        self.categorie_box = QLineEdit(self)
        self.categorie_box.setAlignment(Qt.AlignVCenter)
        self.categorie_box.resize(200, 100)
        self.categorie_box.resize(self.categorie_box.sizeHint())

        self.date_box = QLineEdit(self)
        self.date_box.setAlignment(Qt.AlignVCenter)
        self.date_box.resize(200, 100)
        self.date_box.resize(self.date_box.sizeHint())

        self.commentaire_box = QLineEdit(self)
        self.commentaire_box.setAlignment(Qt.AlignVCenter)
        self.commentaire_box.resize(200, 100)
        self.commentaire_box.resize(self.commentaire_box.sizeHint())

        self.entreprise_box = QLineEdit(self)
        self.entreprise_box.setAlignment(Qt.AlignVCenter)
        self.entreprise_box.resize(200, 100)
        self.entreprise_box.resize(self.entreprise_box.sizeHint())

        # We create a button to extract the information from the text boxes
        self.button = QPushButton('Ajouter', self)
        self.button.clicked.connect(self.on_click)

        self.button_cancel = QPushButton('Annuler', self)
        # self.button_cancel.clicked.connect(self.on_click_annuler)

        # Organisation layout
        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.hlayout3 = QHBoxLayout()
        self.hlayout4 = QHBoxLayout()
        self.hlayout5 = QHBoxLayout()
        self.vlayout = QVBoxLayout()

        self.hlayout1.addWidget(self.label_montant, 1)
        self.hlayout1.addWidget(self.montant_box, 0)

        self.hlayout2.addWidget(self.label_categorie, 1)
        self.hlayout2.addWidget(self.categorie_box, 0)

        self.hlayout3.addWidget(self.label_date, 1)
        self.hlayout3.addWidget(self.date_box, 0)

        self.hlayout4.addWidget(self.label_commentaire, 1)
        self.hlayout4.addWidget(self.commentaire_box, 0)

        self.hlayout5.addWidget(self.label_entreprise, 1)
        self.hlayout5.addWidget(self.entreprise_box, 0)

        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)
        self.vlayout.addLayout(self.hlayout3)
        self.vlayout.addLayout(self.hlayout4)
        self.vlayout.addLayout(self.hlayout5)
        self.vlayout.addWidget(self.button)
        self.setLayout(self.vlayout)

    def on_click(self):
        try:
            montant = float(self.montant_box.text())
        except:
            pass
        if montant > 0:
            pass
        else:
            montant = -montant
        categorie = self.categorie_box.text()
        date = self.date_box.text()  # Faire test date
        commentaire = self.commentaire_box.text()
        entreprise = self.entreprise_box.text()
        self.controler.ajout_depense(-montant, categorie, date, commentaire, entreprise)
        self.close()


# ======================================================================================================================

class Ajouter_gain(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.setFixedSize(300, 150)
        # Page 1: choisir compte
        # widgets
        self.titre1 = QLabel("<b>Ajout Depense</b>")
        self.titre1.setAlignment(Qt.AlignCenter)
        self.titre1.setMaximumHeight(20)

        # date, commentaire, entreprise
        self.label_montant = QLabel('Montant (euros)')
        self.label_montant.setAlignment(Qt.AlignVCenter)
        self.label_montant.resize(200, 100)
        self.label_montant.resize(self.label_montant.sizeHint())

        self.label_categorie = QLabel('Catégorie')
        self.label_categorie.setAlignment(Qt.AlignVCenter)
        self.label_categorie.resize(200, 100)
        self.label_categorie.resize(self.label_categorie.sizeHint())

        self.label_date = QLabel('Date')
        self.label_date.setAlignment(Qt.AlignVCenter)
        self.label_date.resize(200, 100)
        self.label_date.resize(self.label_date.sizeHint())

        self.label_commentaire = QLabel('Commentaire')
        self.label_commentaire.setAlignment(Qt.AlignVCenter)
        self.label_commentaire.resize(200, 100)
        self.label_commentaire.resize(self.label_commentaire.sizeHint())

        self.label_entreprise = QLabel('Entreprise')
        self.label_entreprise.setAlignment(Qt.AlignVCenter)
        self.label_entreprise.resize(200, 100)
        self.label_entreprise.resize(self.label_entreprise.sizeHint())

        # We create text box for the user to enter values of the sample
        self.montant_box = QLineEdit(self)
        self.montant_box.setAlignment(Qt.AlignVCenter)
        self.montant_box.resize(200, 100)
        self.montant_box.resize(self.montant_box.sizeHint())

        self.categorie_box = QLineEdit(self)
        self.categorie_box.setAlignment(Qt.AlignVCenter)
        self.categorie_box.resize(200, 100)
        self.categorie_box.resize(self.categorie_box.sizeHint())

        self.date_box = QLineEdit(self)
        self.date_box.setAlignment(Qt.AlignVCenter)
        self.date_box.resize(200, 100)
        self.date_box.resize(self.date_box.sizeHint())

        self.commentaire_box = QLineEdit(self)
        self.commentaire_box.setAlignment(Qt.AlignVCenter)
        self.commentaire_box.resize(200, 100)
        self.commentaire_box.resize(self.commentaire_box.sizeHint())

        self.entreprise_box = QLineEdit(self)
        self.entreprise_box.setAlignment(Qt.AlignVCenter)
        self.entreprise_box.resize(200, 100)
        self.entreprise_box.resize(self.entreprise_box.sizeHint())

        # We create a button to extract the information from the text boxes
        self.button = QPushButton('Ajouter', self)
        self.button.clicked.connect(self.on_click)

        # Organisation layout
        self.hlayout1 = QHBoxLayout()
        self.hlayout2 = QHBoxLayout()
        self.hlayout3 = QHBoxLayout()
        self.hlayout4 = QHBoxLayout()
        self.hlayout5 = QHBoxLayout()
        self.vlayout = QVBoxLayout()

        self.hlayout1.addWidget(self.label_montant, 1)
        self.hlayout1.addWidget(self.montant_box, 0)

        self.hlayout2.addWidget(self.label_categorie, 1)
        self.hlayout2.addWidget(self.categorie_box, 0)

        self.hlayout3.addWidget(self.label_date, 1)
        self.hlayout3.addWidget(self.date_box, 0)

        self.hlayout4.addWidget(self.label_commentaire, 1)
        self.hlayout4.addWidget(self.commentaire_box, 0)

        self.hlayout5.addWidget(self.label_entreprise, 1)
        self.hlayout5.addWidget(self.entreprise_box, 0)

        self.vlayout.addLayout(self.hlayout1)
        self.vlayout.addLayout(self.hlayout2)
        self.vlayout.addLayout(self.hlayout3)
        self.vlayout.addLayout(self.hlayout4)
        self.vlayout.addLayout(self.hlayout5)
        self.vlayout.addWidget(self.button)
        self.setLayout(self.vlayout)

    def on_click(self):
        try:
            montant = float(self.montant_box.text())
        except:
            pass
        if montant > 0:
            pass
        else:
            montant = -montant
        categorie = self.categorie_box.text()
        date = self.date_box.text()  # Faire test pour date valide
        commentaire = self.commentaire_box.text()
        entreprise = self.entreprise_box.text()
        self.controler.ajout_depense(montant, categorie, date, commentaire, entreprise)
        self.close()


########################################################################################################################
# Widget contenant toutes les informations du compte selectionné
class InformationWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
        self.setMaximumWidth(500)
        self.test = QPushButton()
        layoutV = QVBoxLayout()
        layoutV.addWidget(self.test)
        self.setLayout(layoutV)

    def refresh(self):
        pass


########################################################################################################################
#################################################### TAB: Budget #######################################################
########################################################################################################################
class Budget_tab(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.setMinimumSize(700, 500)

        # widgets
        self.action_widget = ActionBudgetWidget(self, controler)
        self.affichage_widget = AffichageBudgetWidget(self, controler)
        self.historique_depenses_categorie_widget = HistoriqueDepensesCategorieWidget(self, controler)
        self.historique_depenses_categorie_graph_widget = HistoriqueDepensesCategorieGraphWidget(self, controler)

        # Creation layouts
        main_layout = QVBoxLayout()
        sub_layout_h = QHBoxLayout()
        sub_layout_h2= QHBoxLayout()

        # Organisation layouts
        sub_layout_h.addWidget(self.action_widget)
        sub_layout_h.addWidget(self.affichage_widget)
        sub_layout_h2.addWidget(self.historique_depenses_categorie_widget)
        sub_layout_h2.addWidget(self.historique_depenses_categorie_graph_widget)
        main_layout.addLayout(sub_layout_h)
        main_layout.addLayout(sub_layout_h2)

        self.setLayout(main_layout)


########################################################################################################################
class ActionBudgetWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
        self.setMaximumWidth(200)
        
        # Information compte
        self.infocompte = QLabel("<b>Compte</b><br/><i>Type</i><br/>Montant")
        self.infocompte.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.infocompte.setLineWidth(3)
        self.infocompte.setFixedSize(180, 60)
        
        # Boutton pour ajouter un budget
        self.button_ajout_budget = QPushButton("Ajout budget")
        self.button_ajout_budget.clicked.connect(self.ajout_budget)
        self.button_ajout_budget.setMaximumHeight(20)
        
        # Choisir la date de debut de la période d'observation, par defaut 1
        # mois avant la date du jour
        self.label_date_debut = QLabel("Date de début:")
        day=self.controler.periode_obs_dep[0].day
        month=self.controler.periode_obs_dep[0].month
        year=self.controler.periode_obs_dep[0].year
        date_debut_default=QDate(year,month,day)
        self.text_date_debut = QDateEdit(date_debut_default)
        
        
        # Choisir la date de fin de la période d'observation
        self.label_date_fin = QLabel("Date de de fin:")
        self.text_date_fin = QDateEdit(QDate.currentDate())
        
        # Boutton pour changer la période d'observation
        self.button_changer_periode = QPushButton("Changer période")
        self.button_changer_periode.clicked.connect(self.changer_periode)
        self.button_changer_periode.setMaximumHeight(20)

        # Creation Layout
        layout = QVBoxLayout() # Layout principal
        sub_layout_v = QVBoxLayout() # Layout contentant les 2 sub_layouts horizontaux + button pour changer date
        sub_layout_h1 = QHBoxLayout() # Layout contenant date debut periode
        sub_layout_h2 = QHBoxLayout() # Layout contenant date fin periode

        # Organisation Layout
        sub_layout_h1.addWidget(self.label_date_debut)
        sub_layout_h1.addWidget(self.text_date_debut)
        
        sub_layout_h2.addWidget(self.label_date_fin)
        sub_layout_h2.addWidget(self.text_date_fin)
        
        sub_layout_v.addLayout(sub_layout_h1)
        sub_layout_v.addLayout(sub_layout_h2)
        sub_layout_v.addWidget(self.button_changer_periode)
        
        layout.addWidget(self.infocompte)
        layout.addWidget(self.button_ajout_budget)
        layout.addLayout(sub_layout_v)

        self.setLayout(layout)

    def ajout_budget(self):
        self.fenetre_temp = Ajouter_Budget(None, self.controler)
        self.fenetre_temp.setWindowModality(Qt.ApplicationModal)
        self.fenetre_temp.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre_temp.show()
    
    def changer_periode(self):
        date_debut=dt.datetime(self.text_date_debut.date().year(),
                               self.text_date_debut.date().month(),
                               self.text_date_debut.date().day())
        date_fin=dt.datetime(self.text_date_fin.date().year(),
                               self.text_date_fin.date().month(),
                               self.text_date_fin.date().day())
        self.controler.change_periode_obs_dep(date_debut,date_fin)

    def refresh(self):
        try:
            self.infocompte.setText("<b>{}</b><br/><i>{}</i><br/>{:,.2f} €".
                                    format(self.controler.compte.name,
                                           self.controler.compte.type,
                                           self.controler.compte.balance))
        except:
            pass


class Ajouter_Budget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.setFixedSize(300, 300)

        ######### Creation widgets #########

        # Ligne 1
        self.categorie_label = QLabel("Catégorie")
        self.categorie_label.setAlignment(Qt.AlignCenter)
        self.categorie_label.setMaximumHeight(20)

        self.categorie_menu_deroulant = QComboBox()
        self.categorie_menu_deroulant.addItems(self.controler.get_categorie_list())

        # Ligne 2
        self.montant_label = QLabel("Montant")
        self.montant_label.setAlignment(Qt.AlignCenter)
        self.montant_label.setMaximumHeight(20)

        self.montant_box = QLineEdit()
        self.montant_box.setAlignment(Qt.AlignVCenter)

        # Ligne 3
        self.frequence_label = QLabel("Fréquence")
        self.frequence_label.setAlignment(Qt.AlignCenter)
        self.frequence_label.setMaximumHeight(20)

        self.frequence_menu_deroulant = QComboBox()
        self.frequence_menu_deroulant.addItems(['Jour', 'Semaine', 'Mois', 'Année'])

        # Ligne 4
        self.debut_label = QLabel("Debut")
        self.debut_label.setAlignment(Qt.AlignCenter)
        self.debut_label.setMaximumHeight(20)

        self.debut_date = QDateEdit(QDate.currentDate())
        self.debut_date.setAlignment(Qt.AlignCenter)

        # Ligne 5

        self.button_ajouter = QPushButton("Ajouter")
        self.button_ajouter.clicked.connect(self.ajouter)
        self.button_ajouter.setMaximumHeight(20)

        self.button_annuler = QPushButton("Annuler")
        self.button_annuler.clicked.connect(self.annuler)
        self.button_annuler.setMaximumHeight(20)

        ######## Creation Layout ########

        main_layout = QHBoxLayout()
        sub_layout_v1 = QVBoxLayout()
        sub_layout_v2 = QVBoxLayout()

        ######## Organisation Layout #########

        main_layout.addLayout(sub_layout_v1)
        main_layout.addLayout(sub_layout_v2)

        sub_layout_v1.addWidget(self.categorie_label)
        sub_layout_v1.addWidget(self.montant_label)
        sub_layout_v1.addWidget(self.frequence_label)
        sub_layout_v1.addWidget(self.debut_label)
        sub_layout_v1.addWidget(self.button_annuler)

        sub_layout_v2.addWidget(self.categorie_menu_deroulant)
        sub_layout_v2.addWidget(self.montant_box)
        sub_layout_v2.addWidget(self.frequence_menu_deroulant)
        sub_layout_v2.addWidget(self.debut_date)
        sub_layout_v2.addWidget(self.button_ajouter)

        self.setLayout(main_layout)

    def ajouter(self):
        categorie = str(self.categorie_menu_deroulant.currentText())
        montant = self.montant_box.text()
        frequence = str(self.frequence_menu_deroulant.currentText())
        debut = self.debut_date.text()
        self.controler.ajout_budget(categorie, montant, frequence, debut)
        self.close()

    def annuler(self):
        self.close()


########################################################################################################################
class AffichageBudgetWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
#        self.setMaximumWidth(500)
        layout = QVBoxLayout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.draw()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.drawgraph()

    def drawgraph(self):
        categorie_list=self.controler.get_categorie_list()
        n_groups = len(categorie_list)
        
        # On va crée une liste qui contient des listes à deux élements, le 
        # premier élement étant les depenses(class) par catégorie triées par
        # date et le deuxième élément la somme des dépenses
        depenses_triees=[]   
        for i in categorie_list:
            depenses_triees.append(self.controler.trier_depenses(i))
        
        # On cree les variable pour le diagramme à barres
        means_budget=[]
        means_depenses=[]
        for i in range(1,n_groups): # range(1,n_groups) pour ne pas compter la catégorie 'salaire'
            # On determine la somme du budget pour une catégorie donnée
            try:
                somme_budget=float(self.controler.compte.budgets[i].somme)
            except:
                somme_budget=0
            means_budget.append(somme_budget)
            
            # On determine la somme des dépenses pour une catégorie donnée
            somme_depense=depenses_triees[i][1]
            means_depenses.append(somme_depense if somme_depense>0 else
                                  -somme_depense)
#            print(self.controler.compte.budgets[i].somme,self.controler.compte.budgets[i].categorie)
#            print(self.controler.compte.depenses[i].somme,self.controler.compte.depenses[i].categorie)
#        sys.exit()
        
        ax = self.figure.add_subplot(111)
        ax.clear()

        index = np.arange(n_groups-1) # Le -1 est pour ne pas compter la catégirue 'salaire'
        bar_width = 0.35
        opacity = 0.8
        
        ax.bar(index, means_budget, bar_width, alpha=opacity,
                         color='b', label='Budget')
        for i, v in enumerate(means_budget):
            ax.text(i-0.25,v + 3, str(v), color='blue', fontweight='bold')
            
        ax.bar(index + bar_width, means_depenses, bar_width,
                         alpha=opacity, color='g', label='Dépenses')
        for i, v in enumerate(means_depenses):
            ax.text(i - 0.1 + bar_width,v + 3, str(v), color='green',
                    fontweight='bold')
        
        
        ax.set_xlabel('Catégorie',fontsize=8)
        ax.set_ylabel('Euros',fontsize=8)
        ax.set_title('Diagramme de comparaison budget/dépeneses',fontsize=8)
        ax.set_xticks(index+0.2)
        ax.set_xticklabels(categorie_list,fontsize=8)
        ax.legend()
        
        self.figure.tight_layout()
        self.canvas.draw()

    def refresh(self):
        self.drawgraph()


########################################################################################################################
class HistoriqueDepensesCategorieWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
        self.setMaximumWidth(500)
        # Création menu déroulant pour choisir catégorie
        self.menu_deroulant = QComboBox()
        self.menu_deroulant.addItems(self.controler.get_categorie_list())
        self.menu_deroulant.setMaximumHeight(20)
        # Création d'un boutton pour valider le choix de la categorie
        self.button_ok = QPushButton("Valider")
        self.button_ok.clicked.connect(self.valider_choix_categorie)
        self.button_ok.setMaximumHeight(20)
        # Creation widget log pour afficher historique dépenes par catégorie
        self.log_widget=logWidget(self,controler)
        # Creation layout
        layout = QVBoxLayout()
        sub_layout_h = QHBoxLayout() # Layout contenant le menu déroulant des catégories et le boutton pour valider le choix
        # Organisation layout
        sub_layout_h.addWidget(self.menu_deroulant)
        sub_layout_h.addWidget(self.button_ok)
        layout.addLayout(sub_layout_h)
        layout.addWidget(self.log_widget)
        self.setLayout(layout)
    
    def valider_choix_categorie(self):
        categorie_list=self.controler.get_categorie_list()
        self.controler.choix_categorie_depenses(categorie_list[
                self.menu_deroulant.currentIndex()])
            
    
    def refresh(self):
        pass
        

class logWidget(QTextEdit):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
        #        self.setFixedHeight(150)
        self.setReadOnly(True)
        
        depenses_triees=self.controler.trier_depenses(self.controler.categorie_evolution)
        self.append("Historique \n")
        self.append('Date         Somme (€) \n')
        for i in depenses_triees[0]:
            self.append(dt.datetime.strftime(i.date,'%d/%m/%Y')+f'   {abs(i.somme)} \n')


    def refresh(self):
        depenses_triees=self.controler.trier_depenses(self.controler.categorie_evolution)
        self.clear()
        self.append("Historique \n")
        self.append('Date              Somme (€) \n')
        for i in depenses_triees[0]:
            self.append(dt.datetime.strftime(i.date,'%d/%m/%Y')+f'   {i.somme} \n')

#########################################################################################################################
class HistoriqueDepensesCategorieGraphWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
        self.setMaximumWidth(500)
        # Creation de variable avec les depenses
        self.depenses=self.controler.trier_depenses(
                self.controler.categorie_evolution)
        # Création layout
        layout = QVBoxLayout()
        # Création figure pour affichage
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.draw()
        # Organisation layout
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        # Affichage de la figure
        self.drawgraph()

    def drawgraph(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_title("Evolution des dépenses par catégorie", fontsize=10)
        dates=[]
        sommes=[]
        if self.depenses[0]:
            somme=0
            for i in self.depenses[0]:
                somme=somme+i.somme
                dates.append(i.date.date())
                sommes.append(abs(somme))
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.plot(dates,sommes,'ro')
        ax.plot(dates,sommes,'r')  
        
        self.figure.tight_layout()
        self.canvas.draw()

    def refresh(self):
        self.depenses=depenses_triees=self.controler.trier_depenses(
                self.controler.categorie_evolution)
        self.drawgraph()
# =====================================================================================================================#
# ====================================================== Main app ======================================================#
# ======================================================================================================================#

def main():
    app = QApplication([])
    controler = Controler()
    win = MainWindow(controler)
    controler.init()
    win.show()
    app.exec()
    controler.close()


if __name__ == '__main__':
    main()
