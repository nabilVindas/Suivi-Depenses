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
        self.compte:compte = None
        
    def close(self):
        # Ecriture des données (clées, catégories, comptes)
        for c in self.liste_comptes:
            c.new_doc()
        fc.ecriture_categorie_document()
        fc.ecriture_key_document()
