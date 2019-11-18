# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:46:29 2019

@author: nayab
"""

import functions as fc



class ControlerBase:
    def __init__(self):
        self.clients = list()
        self.message = ""

    def addClient(self, client):
        self.clients.append(client)

    def refreshAll(self, message=None):
        self.message = message
        for client in self.clients:
            client.refresh()
            

class Controler(ControlerBase):
    def __init__(self):
        super().__init__()
        # Chargement des données (clées, catégories, comptes)
        fc.lecture_key_document()
        fc.lecture_categorie_document()
        self.liste_comptes = fc.lecture_liste_compte()
        # Attribues
        self.compte = None
        
    def close(self):
        # Ecriture des données (clées, catégories, comptes)
        for c in self.liste_comptes:
            c.new_doc()
        fc.ecriture_categorie_document()
        fc.ecriture_key_document()
        
    def select_compte_from_index(self,index_select):
        self.compte = self.liste_comptes[index_select]
        self.refreshAll()
        
    def nouveau_compte(self,nom,typ,montant,credit,interet):
        compte = fc.creation_compte(nom,typ,montant,credit,interet)
        if compte is None:
            return 0
        else:
            self.compte = compte
            self.liste_comptes.append(compte)
            self.refreshAll()
            return 1
        
    def delete_compte(self):
        fc.supprimer_compte(self.compte)
        self.liste_comptes.remove(self.compte)
        self.compte = None
