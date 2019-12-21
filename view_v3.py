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
from dateutil.relativedelta import relativedelta
from statistics import mean
from _datetime import date



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
        self.setMinimumSize(900, 500)
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
        self.button_changercompte = QPushButton("Changer compte")
        self.button_supprimercompte = QPushButton("Supprimer compte")
        # layouts
        layoutV = QVBoxLayout()
        layoutV1 = QVBoxLayout()
        layoutV1.addWidget(self.button_ajouterdepense)
        layoutV1.addWidget(self.button_ajoutergain)
        layoutV1.addWidget(self.button_virementauto)
        layoutV1.addWidget(self.button_virementcomptes)
        layoutV.addWidget(self.infocompte)
        layoutV.addLayout(layoutV1)
        layoutV.addWidget(self.button_changercompte)
        layoutV.addWidget(self.button_supprimercompte)
        layoutV.setAlignment(self.infocompte, Qt.AlignTop)
        layoutV.setAlignment(self.button_changercompte, Qt.AlignBottom)
        self.setLayout(layoutV)
        # connecter les boutons
        self.button_ajouterdepense.clicked.connect(self.ouvrir_ajouter_depense)
        self.button_ajoutergain.clicked.connect(self.ouvrir_ajouter_gain)
        self.button_virementauto.clicked.connect(self.ouvrir_virement_auto)
        self.button_virementcomptes.clicked.connect(self.ouvrir_virement_compte)
        self.button_changercompte.clicked.connect(self.ouvrir_select_compte)
        self.button_supprimercompte.clicked.connect(self.ouvrir_supprime_compte)
        
    def ouvrir_ajouter_depense(self):
        self.fenetre = AjouterDepense(None,self.controler)
        self.fenetre.setWindowModality(Qt.ApplicationModal)
        self.fenetre.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre.show()
        
    def ouvrir_ajouter_gain(self):
        self.fenetre = AjouterGain(None,self.controler)
        self.fenetre.setWindowModality(Qt.ApplicationModal)
        self.fenetre.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre.show()
        
    def ouvrir_virement_auto(self):
        self.fenetre = VirementAutomatique(None,self.controler)
        self.fenetre.setWindowModality(Qt.ApplicationModal)
        self.fenetre.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre.show()
        
    def ouvrir_virement_compte(self):
        self.fenetre = VirementCompte(None,self.controler)
        self.fenetre.setWindowModality(Qt.ApplicationModal)
        self.fenetre.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre.show()
        
    def ouvrir_select_compte(self):
        self.fenetre = SelectCompte(None,self.controler)
        self.fenetre.setWindowModality(Qt.ApplicationModal)
        self.fenetre.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre.show()
        
    def ouvrir_supprime_compte(self):
        self.fenetre = SupprimeCompte(None,self.controler,self)
        self.fenetre.setWindowModality(Qt.ApplicationModal)
        self.fenetre.setWindowFlags(Qt.FramelessWindowHint)
        self.fenetre.show()

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

class AjouterDepense(QWidget):
    def __init__(self,parent,controler):
        super().__init__(parent)
        self.controler = controler
        self.setFixedSize(500,200)
        # widgets 
        self.label_titre = QLabel("<b>Ajouter une dépense</b>")
        self.label_montant = QLabel("Montant:")
        self.label_date = QLabel("Date:")
        self.label_entreprise = QLabel("Bénéficiaire:")
        self.label_categorie = QLabel("Catégorie:")
        self.label_commentaire = QLabel("Commentaire:")
        self.label_erreur = QLabel("")
        self.text_montant = QLineEdit()
        valid = QDoubleValidator()
        valid.setBottom(0)
        self.text_montant.setValidator(valid)
        self.text_date = QDateEdit(QDate.currentDate())
        self.text_date.setMaximumDate(QDate.currentDate())
        self.text_entreprise = QLineEdit()
        self.text_categorie = QComboBox()
        self.text_categorie.addItems(self.controler.get_categorie_list())
        self.text_commentaire = QLineEdit()
        self.button = QPushButton("Ajouter")
        self.button.setMinimumWidth(200)
        self.button_annuler = QPushButton("Annuler")
        self.button_annuler.setStyleSheet('font: bold')
        # layouts
        layoutG = QGridLayout()
        layoutG.addWidget(self.label_titre,0,0,1,4)
        layoutG.setAlignment(self.label_titre,Qt.AlignCenter)
        layoutG.addWidget(self.label_montant,1,0)
        layoutG.setAlignment(self.label_montant,Qt.AlignRight)
        layoutG.addWidget(self.text_montant,1,1)
        layoutG.addWidget(self.label_date,1,2)
        layoutG.setAlignment(self.label_date,Qt.AlignRight)
        layoutG.addWidget(self.text_date,1,3)
        layoutG.addWidget(self.label_entreprise,2,0)
        layoutG.setAlignment(self.label_entreprise,Qt.AlignRight)
        layoutG.addWidget(self.text_entreprise,2,1)
        layoutG.addWidget(self.label_categorie,2,2)
        layoutG.setAlignment(self.label_categorie,Qt.AlignRight)
        layoutG.addWidget(self.text_categorie,2,3)
        layoutG.addWidget(self.label_commentaire,3,0)
        layoutG.addWidget(self.text_commentaire,3,1,1,3)
        layoutG.addWidget(self.label_erreur,4,0)
        layoutG.addWidget(self.button,4,0,1,4)
        layoutG.setAlignment(self.button,Qt.AlignCenter)
        layoutG.addWidget(self.button_annuler,4,3)
        layoutG.setAlignment(self.button_annuler,Qt.AlignRight)
        self.setLayout(layoutG)
        # connecter les boutons
        self.button.clicked.connect(self.click)
        self.button_annuler.clicked.connect(self.click_annuler)
        
    def click(self):
        if self.controler.ajouter_somme_compte("-" + self.text_montant.text(),
                                               self.text_entreprise.text(),
                                               self.text_date.date(),
                                               self.text_categorie.currentText(),
                                               self.text_commentaire.text()):
            self.close()
        else:
            self.label_erreur.setText(
                    "<b><p style='color:red;'>Erreur")
    
    def click_annuler(self):
        self.close()


# ======================================================================================================================

class AjouterGain(QWidget):
    def __init__(self,parent,controler):
        super().__init__(parent)
        self.controler = controler
        self.setFixedSize(500,200)
        # widgets 
        self.label_titre = QLabel("<b>Ajouter un gain</b>")
        self.label_montant = QLabel("Montant:")
        self.label_date = QLabel("Date:")
        self.label_entreprise = QLabel("Emetteur:")
        self.label_categorie = QLabel("Catégorie:")
        self.label_commentaire = QLabel("Commentaire:")
        self.label_erreur = QLabel("")
        self.text_montant = QLineEdit()
        valid = QDoubleValidator()
        valid.setBottom(0)
        self.text_montant.setValidator(valid)
        self.text_date = QDateEdit(QDate.currentDate())
        self.text_date.setMaximumDate(QDate.currentDate())
        self.text_entreprise = QLineEdit()
        self.text_categorie = QComboBox()
        self.text_categorie.addItems(self.controler.get_categorie_list())
        self.text_commentaire = QLineEdit()
        self.button = QPushButton("Ajouter")
        self.button.setMinimumWidth(200)
        self.button_annuler = QPushButton("Annuler")
        self.button_annuler.setStyleSheet('font: bold')
        # layouts
        layoutG = QGridLayout()
        layoutG.addWidget(self.label_titre,0,0,1,4)
        layoutG.setAlignment(self.label_titre,Qt.AlignCenter)
        layoutG.addWidget(self.label_montant,1,0)
        layoutG.setAlignment(self.label_montant,Qt.AlignRight)
        layoutG.addWidget(self.text_montant,1,1)
        layoutG.addWidget(self.label_date,1,2)
        layoutG.setAlignment(self.label_date,Qt.AlignRight)
        layoutG.addWidget(self.text_date,1,3)
        layoutG.addWidget(self.label_entreprise,2,0)
        layoutG.setAlignment(self.label_entreprise,Qt.AlignRight)
        layoutG.addWidget(self.text_entreprise,2,1)
        layoutG.addWidget(self.label_categorie,2,2)
        layoutG.setAlignment(self.label_categorie,Qt.AlignRight)
        layoutG.addWidget(self.text_categorie,2,3)
        layoutG.addWidget(self.label_commentaire,3,0)
        layoutG.addWidget(self.text_commentaire,3,1,1,3)
        layoutG.addWidget(self.label_erreur,4,0)
        layoutG.addWidget(self.button,4,0,1,4)
        layoutG.setAlignment(self.button,Qt.AlignCenter)
        layoutG.addWidget(self.button_annuler,4,3)
        layoutG.setAlignment(self.button_annuler,Qt.AlignRight)
        self.setLayout(layoutG)
        # connecter les boutons
        self.button.clicked.connect(self.click)
        self.button_annuler.clicked.connect(self.click_annuler)
        
    def click(self):
        if self.controler.ajouter_somme_compte(self.text_montant.text(),
                                               self.text_entreprise.text(),
                                               self.text_date.date(),
                                               self.text_categorie.currentText(),
                                               self.text_commentaire.text()):
            self.close()
        else:
            self.label_erreur.setText(
                    "<b><p style='color:red;'>Erreur")
    
    def click_annuler(self):
        self.close()
        

class VirementAutomatique(QWidget):
    def __init__(self,parent,controler):
        super().__init__(parent)
        self.controler = controler
        self.setFixedSize(550,250)
        # widgets
        self.label_titre = QLabel("<b>Automatiser entrée/sortie</b>")
        self.label_erreur = QLabel("")
        self.label_somme = QLabel("Somme:")
        self.label_categorie = QLabel("Catégorie:")
        self.label_entreprise = QLabel("Bénef/Emet:")
        self.label_commentaire = QLabel("Commentaire:")
        self.label_debut = QLabel("Début:")
        self.label_fin = QLabel("Fin:")
        self.label_echeance = QLabel("Echéance:")
        self.label_echM = QLabel("M:")
        self.label_echJ = QLabel("J:")
        self.text_somme = QLineEdit()
        self.text_somme.setValidator(QDoubleValidator())
        self.text_categorie = QComboBox()
        self.text_categorie.addItems(self.controler.get_categorie_list())
        self.text_entreprise = QLineEdit()
        self.text_commentaire = QLineEdit()
        self.text_debut = QDateTimeEdit(QDate.currentDate())
        self.text_debut.setDisplayFormat("dd/MM/yyyy")
        self.text_fin = QDateTimeEdit(QDate.currentDate())
        self.text_fin.setDisplayFormat("dd/MM/yyyy")
        self.text_echM = QSpinBox()
        self.text_echJ = QSpinBox()
        self.button_valider = QPushButton("Valider")
        self.button_valider.setMinimumWidth(200)
        self.button_annuler = QPushButton("Annuler")
        self.button_annuler.setMaximumWidth(100)
        self.button_annuler.setStyleSheet('font: bold')
        # layouts
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.label_echM)
        layoutH.setAlignment(self.label_echM,Qt.AlignRight)
        layoutH.addWidget(self.text_echM)
        layoutH.addWidget(self.label_echJ)
        layoutH.setAlignment(self.label_echJ,Qt.AlignRight)
        layoutH.addWidget(self.text_echJ)
        layoutG = QGridLayout()
        layoutG.addWidget(self.label_titre,0,0,1,4)
        layoutG.setAlignment(self.label_titre,Qt.AlignCenter)
        layoutG.addWidget(self.label_somme,1,0)
        layoutG.setAlignment(self.label_somme,Qt.AlignRight)
        layoutG.addWidget(self.text_somme,1,1)
        layoutG.addWidget(self.label_debut,1,2)
        layoutG.setAlignment(self.label_debut,Qt.AlignRight)
        layoutG.addWidget(self.text_debut,1,3)
        layoutG.setAlignment(self.text_debut,Qt.AlignCenter)
        layoutG.addWidget(self.label_categorie,2,0)
        layoutG.setAlignment(self.label_categorie,Qt.AlignRight)
        layoutG.addWidget(self.text_categorie,2,1)
        layoutG.addWidget(self.label_echeance,2,2)
        layoutG.setAlignment(self.label_echeance,Qt.AlignRight)
        layoutG.addLayout(layoutH,2,3)
        layoutG.addWidget(self.label_entreprise,3,0)
        layoutG.setAlignment(self.label_entreprise,Qt.AlignRight)
        layoutG.addWidget(self.text_entreprise,3,1)
        layoutG.addWidget(self.label_fin,3,2)
        layoutG.setAlignment(self.label_fin,Qt.AlignRight)
        layoutG.addWidget(self.text_fin,3,3)
        layoutG.setAlignment(self.text_fin,Qt.AlignCenter)
        layoutG.addWidget(self.label_commentaire,4,0)
        layoutG.setAlignment(self.label_commentaire,Qt.AlignRight)
        layoutG.addWidget(self.text_commentaire,4,1,1,3)
        layoutG.addWidget(self.label_erreur,5,0)
        layoutG.addWidget(self.button_valider,5,0,1,4)
        layoutG.setAlignment(self.button_valider,Qt.AlignCenter)
        layoutG.addWidget(self.button_annuler,5,3)
        layoutG.setAlignment(self.button_annuler,Qt.AlignRight)
        self.setLayout(layoutG)
        # connecter les boutons/ signals
        self.button_valider.clicked.connect(self.click_valider)
        self.button_annuler.clicked.connect(self.click_annuler)
        self.text_debut.dateTimeChanged.connect(self.date_debut_changed)
        self.text_fin.dateTimeChanged.connect(self.date_fin_changed)
    
    def click_valider(self):
        debut = self.text_debut.dateTime().toString("dd/MM/yyyy")
        fin = self.text_fin.dateTime().toString("dd/MM/yyyy")
        ech = "{:02d}/{:02d}".format(self.text_echJ.value(),self.text_echM.value())
        if self.controler.ajouter_virement_auto(debut,
                                                fin,
                                                ech,
                                                self.text_somme.text(),
                                                self.text_categorie.currentText(),
                                                self.text_commentaire.text(),
                                                self.text_entreprise.text()):
            self.close()
        else:
            self.label_erreur.setText(
                    "<b><p style='color:red;'>Erreur")
    
    def click_annuler(self):
        self.close()
        
    def date_debut_changed(self,date):
        self.text_fin.setMinimumDateTime(date)
        
    def date_fin_changed(self,date):
        self.text_debut.setMaximumDateTime(date)
        
        
class VirementCompte(QWidget):
    def __init__(self,parent,controler):
        super().__init__(parent)
        self.controler = controler
        self.setFixedSize(750,220)
        # widgets
        self.label_titre = QLabel("<b>Virement entre compte</b>")
        self.label_erreur = QLabel("")
        self.label_debiteur = QLabel("<b>Débiteur</b>")
        self.label_compte1 = QLabel("Compte:")
        self.label_commentaire1 = QLabel("Commentaire:")
        self.label_montant = QLabel("Montant:")
        self.label_date = QLabel("Date:")
        self.label_categorie = QLabel("Catégorie:")
        self.label_beneficieur = QLabel("<b>Bénéficieur</b>")
        self.label_compte2 = QLabel("Compte:")
        self.label_commentaire2 = QLabel("Commentaire:")
        self.text_compte1 = QComboBox()
        self.text_compte1.addItems([c.name for c in controler.liste_comptes])
        self.text_compte1.setCurrentText(self.controler.compte.name)
        self.text_commentaire1 = QLineEdit()
        self.text_montant = QLineEdit()
        valid = QDoubleValidator()
        valid.setBottom(0)
        self.text_montant.setValidator(valid)
        self.text_date = QDateEdit(QDate.currentDate())
        self.text_date.setMaximumDate(QDate.currentDate())
        self.text_categorie = QComboBox()
        self.text_categorie.addItems(self.controler.get_categorie_list())
        self.text_compte2 = QComboBox()
        self.text_compte2.addItems([c.name for c in controler.liste_comptes])
        self.text_commentaire2 = QLineEdit()
        self.button_valider = QPushButton("Valider")
        self.button_annuler = QPushButton("Annuler")
        self.button_annuler.setStyleSheet('font: bold')
        # layouts
        layoutG = QGridLayout()
        layoutG.addWidget(self.label_titre,0,0,1,6)
        layoutG.setAlignment(self.label_titre,Qt.AlignCenter)
        layoutG.addWidget(self.label_debiteur,1,0,1,2)
        layoutG.setAlignment(self.label_debiteur,Qt.AlignCenter)
        layoutG.addWidget(self.label_beneficieur,1,4,1,2)
        layoutG.setAlignment(self.label_beneficieur,Qt.AlignCenter)
        layoutG.addWidget(self.label_compte1,2,0)
        layoutG.setAlignment(self.label_compte1, Qt.AlignRight)
        layoutG.addWidget(self.text_compte1,2,1)
        layoutG.addWidget(self.label_montant,2,2)
        layoutG.setAlignment(self.label_montant, Qt.AlignRight)
        layoutG.addWidget(self.text_montant,2,3)
        layoutG.addWidget(self.label_compte2,2,4)
        layoutG.setAlignment(self.label_compte2, Qt.AlignRight)
        layoutG.addWidget(self.text_compte2,2,5)
        layoutG.addWidget(self.label_commentaire1,3,0,1,2)
        layoutG.setAlignment(self.label_commentaire1,Qt.AlignCenter | Qt.AlignBottom)
        layoutG.addWidget(self.label_date,3,2)
        layoutG.setAlignment(self.label_date, Qt.AlignRight)
        layoutG.addWidget(self.text_date,3,3)
        layoutG.addWidget(self.label_commentaire2,3,4,1,2)
        layoutG.setAlignment(self.label_commentaire2,Qt.AlignCenter | Qt.AlignBottom)
        layoutG.addWidget(self.text_commentaire1,4,0,1,2)
        layoutG.addWidget(self.label_categorie,4,2)
        layoutG.addWidget(self.text_categorie,4,3)
        layoutG.addWidget(self.text_commentaire2,4,4,1,2)
        layoutG.addWidget(self.label_erreur,5,0)
        layoutG.addWidget(self.button_valider,5,2,1,2)
        layoutG.addWidget(self.button_annuler,5,5)
        layoutG.setAlignment(self.button_annuler,Qt.AlignRight)
        layoutG.setColumnStretch(0,1)
        layoutG.setColumnStretch(1,2)
        layoutG.setColumnStretch(2,1)
        layoutG.setColumnStretch(3,2)
        layoutG.setColumnStretch(4,1)
        layoutG.setColumnStretch(5,2)
        self.setLayout(layoutG)
        # connecter les boutons
        self.button_valider.clicked.connect(self.click_valider)
        self.button_annuler.clicked.connect(self.click_annuler)
        
    def click_valider(self):
        if self.controler.ajouter_virement(self.text_compte1.currentIndex(),
                                           self.text_compte2.currentIndex(),
                                           self.text_montant.text(),
                                           self.text_categorie.currentText(),
                                           self.text_date.date(),
                                           self.text_commentaire1.text(),
                                           self.text_commentaire2.text()):
            self.close()
        else:
            self.label_erreur.setText(
                    "<b><p style='color:red;'>Erreur")
    
    def click_annuler(self):
        self.close()


########################################################################################################################
# Widget contenant toutes les informations du compte selectionné
class InformationWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
        self.setMaximumWidth(700)
        # widgets
        # haut
        self.graph1 = TabGraph1(self,controler)
        #self.tab = QTabWidget()
        #self.tab.setStyle(QStyleFactory.create('Fusion'))
        #self.tab.addTab(self.graph1,'Récap. Général')
        #self.tab.addTab(self.graph2,'Récap. Catégorie')
        # bas
        self.label_titre = QLabel("<b>HISTORIQUE</b>")
        self.label_trier = QLabel("<i>Trier par:</i>")
        self.tri_categorie = QComboBox()
        self.tri_categorie.addItems(["Date","Montant","Catégorie"])
        self.tri_categorie.setMaximumWidth(150)
        self.historique_depense = HistoriqueDepenses(self,self.controler)
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.historique_depense)
        # layouts
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.label_titre,1,Qt.AlignLeft | Qt.AlignBottom)
        layoutH.addWidget(self.label_trier,3,Qt.AlignRight | Qt.AlignBottom)
        layoutH.addWidget(self.tri_categorie,1,Qt.AlignLeft)
        layoutV = QVBoxLayout()
        layoutV.addWidget(self.graph1)
        layoutV.addLayout(layoutH)
        layoutV.addWidget(self.scroll)
        layoutV.setStretchFactor(self.graph1,1)
        layoutV.setStretchFactor(self.scroll,1)
        layoutV.setContentsMargins(5,5,5,5)
        layoutV.setSpacing(2)
        self.setLayout(layoutV)

    def refresh(self):
        pass
    
# Widget avec les informations textes     
class HistoriqueDepenses(QWidget):
    def __init__(self,parent, controler):
        super().__init__(parent)
        self.parent = parent
        self.controler = controler
        self.controler.addClient(self)
        # widgets
        self.cell_init = CellDepense(self,None,'','','','')
        self.list_cell = []
        # layouts
        self.layoutV = QVBoxLayout()
        self.layoutV.addWidget(self.cell_init)
        self.layoutV.setContentsMargins(0,0,0,0)
        self.layoutV.setSpacing(0)
        self.setLayout(self.layoutV)
        # connecter signals
        self.parent.tri_categorie.currentIndexChanged.connect(self.refresh)
        
    def refresh(self):
        self.controler.trier_depense_general(self.parent.tri_categorie.currentIndex())
        if (self.controler.compte) and (self.controler.compte.depenses):
            for i in reversed(range(self.layoutV.count())): 
                self.layoutV.itemAt(i).widget().setParent(None)
            for d in self.controler.compte.depenses:
                cell = CellDepense(self,d.somme,d.date.strftime('%d/%m/%Y'),
                                   d.categorie,d.entreprise,d.commentaire)
                self.layoutV.addWidget(cell)
            self.resize(self.width(),60*self.layoutV.count())
        else:
            for i in reversed(range(self.layoutV.count())): 
                self.layoutV.itemAt(i).widget().setParent(None)
            self.layoutV.addWidget(self.cell_init)
            self.resize(self.width(),60*self.layoutV.count())
 
            
class CellDepense(QFrame):
    def __init__(self, parent, montant, date, categorie, entreprise, com):
        super().__init__(parent)
        self.setFixedSize(650,60)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(2)
        # widgets
        self.label_date = QLabel("<b>Date:</b> {}".format(date))
        self.label_categorie = QLabel("<b>Catégorie:</b> {}".format(categorie))
        self.label_commentaire = QLabel("<b>Commentaire:</b> <i>{}</i>".format(com))
        self.label_montant = QLabel("<b>Montant:</b>")
        self.label_entreprise = QLabel("<b>Bénéficiare:</b>")
        if (montant is not None) and (montant > 0):
            self.label_montant.setText("<b>Montant:</b> <FONT color='green'>{:,.2f} €".
                                       format(montant))
            self.label_entreprise.setText("<b>Emetteur:</b> {}".format(entreprise))
        elif (montant is not None) and (montant <= 0):
            self.label_montant.setText("<b>Montant:</b> <FONT color='red'>{:,.2f} €".
                                       format(montant))
            self.label_entreprise.setText("<b>Bénéficiaire:</b> {}".format(entreprise))
        # layouts
        layoutG = QGridLayout()
        layoutG.addWidget(self.label_montant,0,0)
        layoutG.setAlignment(self.label_montant, Qt.AlignLeft)
        layoutG.addWidget(self.label_entreprise,0,1)
        layoutG.setAlignment(self.label_entreprise, Qt.AlignLeft)
        layoutG.addWidget(self.label_date,1,0)
        layoutG.setAlignment(self.label_date, Qt.AlignLeft)
        layoutG.addWidget(self.label_categorie,1,1)
        layoutG.setAlignment(self.label_categorie, Qt.AlignLeft)
        layoutG.addWidget(self.label_commentaire,2,0,1,2)
        layoutG.setAlignment(self.label_commentaire, Qt.AlignLeft)
        layoutG.setColumnStretch(0,1)
        layoutG.setColumnStretch(1,1)
        layoutG.setContentsMargins(2,2,2,2)
        layoutG.setSpacing(0)
        self.setLayout(layoutG)


class TabGraph1(QWidget):
    def __init__(self,parent, controler):
        super().__init__(parent)
        self.parent = parent
        self.controler = controler
        self.controler.addClient(self)
        # widgets
        self.fig = plt.figure()
        self.fig.subplots_adjust(left=0.07,right=0.95,bottom=0.09,top=0.9)
        self.fig.set_facecolor((0.886,0.886,0.886))
        self.ax1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.label_deb = QLabel("Début:")
        self.label_fin = QLabel("Fin:")
        self.date_deb = QDateEdit(QDate.currentDate())
        self.date_fin = QDateEdit(QDate.currentDate())
        self.date_fin.setMaximumDate(QDate.currentDate())
        # layouts
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.label_deb)
        layoutH.addWidget(self.date_deb)
        layoutH.addWidget(self.label_fin)
        layoutH.addWidget(self.date_fin)
        layoutH.setSpacing(0)
        layoutV = QVBoxLayout()
        layoutV.addLayout(layoutH)
        layoutV.setAlignment(layoutH, Qt.AlignCenter)
        layoutV.addWidget(self.canvas)
        layoutV.setContentsMargins(0,0,0,0)
        layoutV.setSpacing(0)
        self.setLayout(layoutV)
        # connecter signal
        self.date_deb.dateChanged.connect(self.date_debut_changed)
        self.date_fin.dateChanged.connect(self.date_fin_changed)
        
    def date_debut_changed(self, date):
        self.date_fin.setMinimumDate(date)
        self.draw_graph()
        
    def date_fin_changed(self, date):
        self.date_deb.setMaximumDate(date)
        self.draw_graph()
        
    def draw_graph(self):
        x,y = self.controler.historique_graph1(self.date_deb.date().toString("dd/MM/yyyy"),
                                               self.date_fin.date().toString("dd/MM/yyyy"))
        self.ax1.cla()
        self.ax1.plot(x,[0 for i in range(len(y))], '-.r', linewidth=2)
        self.ax1.plot(x,y, '-g', linewidth=4)
        self.ax1.plot(x,[mean(y) for i in range(len(y))], '-b', linewidth=1)
        self.ax1.xaxis.set_ticks(range(0,len(x),int(len(x)/7)+1))
        self.ax1.xaxis.set_tick_params(labelsize = 6)
        self.ax1.yaxis.set_tick_params(labelsize = 6)
        self.ax1.set_ylabel('Euros',fontsize=8)
        self.ax1.set_title('Evolution du compte dans le temps',fontsize=8)
        self.ax1.margins(0,0.08)
        self.canvas.draw()
        
    
    def refresh(self):
        date_ini = QDate.fromString(self.controler.date_init_graph1(),"dd/MM/yyyy")
        self.date_deb.setMinimumDate(date_ini)
        self.date_deb.setDate(date_ini)
        self.date_fin.setDate(QDate.currentDate())
        self.draw_graph()
        

########################################################################################################################
#################################################### TAB: Budget #######################################################
########################################################################################################################
class Budget_tab(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.setMinimumSize(900, 500)

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
        self.label_date_fin = QLabel("Date de fin:")
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
        self.figure.set_facecolor((0.886,0.886,0.886))
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
        self.figure.set_facecolor((0.886,0.886,0.886))
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
