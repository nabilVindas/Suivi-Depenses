# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:46:23 2019

@author: nayab
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functions import *
from controler import Controler




# =============================================================================
# Fenetres Principal

class MainWindow(QMainWindow):
    def __init__(self, controler):
        super().__init__()
        self.setWindowTitle("Gestion du porte-monnaie")
        self.mainwidget = MainWidget(self, controler)
        self.setCentralWidget(self.mainwidget)
    

    
class MainWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.setMinimumSize(700, 500)
        # widgets
        self.actionwidget = ActionWidget(self,controler)
        self.informationwidget = InformationWidget(self,controler)
        layoutH = QHBoxLayout()
        layoutH.addWidget(self.actionwidget)
        layoutH.addWidget(self.informationwidget)
        self.setLayout(layoutH)

# =============================================================================
# Widget contenent les boutons des actions disponible pour un compte    
class ActionWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
        self.setMaximumWidth(200)
        # initialisation de la fenetre d'action
        self.fenetre = None
        self.ouvrir_select_compte()
        # widgets
        self.infocompte = QLabel("<b>Compte</b><br/><i>Type</i><br/>Montant")
        self.infocompte.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.infocompte.setLineWidth(3)
        self.infocompte.setFixedSize(180,60)
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
        layoutV.setAlignment(self.infocompte,Qt.AlignTop)
        layoutV.setAlignment(self.button_changercompte,Qt.AlignBottom)
        self.setLayout(layoutV)
        # connecter les boutons
        self.button_changercompte.clicked.connect(self.ouvrir_select_compte)
        self.button_supprimercompte.clicked.connect(self.ouvrir_supprime_compte)
        
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
        self.infocompte.setText("<b>{}</b><br/><i>{}</i><br/>{:,.2f} €".
                                format(self.controler.compte.name,
                                       self.controler.compte.type,
                                       self.controler.compte.balance))


class SelectCompte(QWidget):
    def __init__(self,parent,controler):
        super().__init__(parent)
        self.controler = controler
        self.setFixedSize(300,150)
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
        layoutV.setAlignment(self.button_new,Qt.AlignCenter)
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
        self.text_interet.setValidator(QDoubleValidator(0.0,100.0,2))
        self.button_creer = QPushButton("Créer")
        self.button_creer.setStyleSheet('font: bold')
        self.button_retour = QPushButton("Retour")
        # layouts
        layoutG = QGridLayout()
        layoutG.addWidget(self.titre2,0,0,1,2)
        layoutG.setAlignment(self.titre2,Qt.AlignCenter)
        layoutG.addWidget(self.label_nom,1,0)
        layoutG.setAlignment(self.label_nom,Qt.AlignRight)
        layoutG.addWidget(self.label_type,2,0)
        layoutG.setAlignment(self.label_type,Qt.AlignRight)
        layoutG.addWidget(self.label_montant,3,0)
        layoutG.setAlignment(self.label_montant,Qt.AlignRight)
        layoutG.addWidget(self.label_credit,5,0)
        layoutG.setAlignment(self.label_credit,Qt.AlignRight)
        layoutG.addWidget(self.label_interet,6,0)
        layoutG.setAlignment(self.label_interet,Qt.AlignRight)
        layoutG.addWidget(self.text_nom,1,1)
        layoutG.addWidget(self.text_type,2,1)
        layoutG.addWidget(self.text_montant,3,1)
        layoutG.addWidget(self.text_credit,5,1)
        layoutG.addWidget(self.text_interet,6,1)
        layoutG.addWidget(self.button_retour,7,0)
        layoutG.addWidget(self.button_creer,7,1)
        layoutG.addWidget(self.label_erreur,4,1)
        layoutG.setAlignment(self.button_creer,Qt.AlignCenter)
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
        self.setFixedSize(400,250)
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
        self.setFixedSize(300,150)
        self.layoutS.setCurrentIndex(0)


class SupprimeCompte(QWidget):
    def __init__(self,parent,controler,main_widget):
        super().__init__(parent)
        self.controler = controler
        self.main_widget = main_widget
        self.setFixedSize(250,100)
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
        layoutV.setAlignment(self.label,Qt.AlignCenter)
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
        

# =============================================================================
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
        
 
# =============================================================================
# Main app
        
def main():
    app = QApplication([])
    controler = Controler()
    win = MainWindow(controler)
    win.show()
    app.exec()
    controler.close()


if __name__ == '__main__':
    main()
