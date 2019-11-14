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


# Widget contenent les boutons des actions disponible pour un compte    
class ActionWidget(QWidget):
    def __init__(self, parent, controler):
        super().__init__(parent)
        self.controler = controler
        self.controler.addClient(self)
        self.setMaximumWidth(200)
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
        
    def refresh(self):
        self.infocompte.setText("<b>{}</b><br/><i>{}</i><br/>{:.2f} €".
                                format(self.controler.compte.name,
                                       self.controler.compte.type,
                                       self.controler.compte.balance))
        pass


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
