# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:46:29 2019

@author: nayab
"""

import functions_v3 as fc
import datetime as dt
import sys



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
        # Periode d'observation des depenses (2eme onglet)
        current_year=dt.datetime.today().year
        current_month=dt.datetime.today().month
        current_day=dt.datetime.today().day
        if current_month>1:
            if (current_day==31 or current_day==30 or current_day==29) and current_month-1==2:
                date_debut_default=dt.datetime(current_year,
                                                 current_month-1,28)
            elif current_day==31 and (current_month-1==4 or
                            current_month-1==6 or current_month-1==9
                            or current_month-1==11):
                date_debut_default=dt.datetime(current_year,
                                                 current_month-1,30)
            else:
                date_debut_default=dt.datetime(current_year,
                                                 current_month-1,current_day)

        else:
            date_debut_default=dt.datetime(current_year-1,
                                             12,
                                             current_day)
        self.periode_obs_dep=[date_debut_default,dt.datetime.today()]
        # Catégorie pour laquelle on affiche l'evolution des dépenses en fonction
        # du temps pour la deuxième onglet
        self.categorie_evolution=fc.categorie_list[0]
        # Chargement des données (clées, catégories, comptes)
        fc.lecture_key_document()
        fc.lecture_categorie_document()
        self.liste_comptes = fc.lecture_liste_compte()
        # Attribues
        try:
            self.compte = self.liste_comptes[0]
        except:
            self.compte = None

    def close(self):
        # Ecriture des données (clées, catégories, comptes)
        for c in self.liste_comptes:
            c.new_doc()
        fc.ecriture_categorie_document()
        fc.ecriture_key_document()

    def get_key_list(self):
        return fc.key_list

    def get_categorie_list(self):
        return fc.categorie_list

    def select_compte_from_index(self,index_select):
        self.compte = self.liste_comptes[index_select]
        fc.actualisation_depense_auto(self.compte)
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

    def ajouter_somme_compte(self,montant,entreprise,date,categorie,com):
        depense = fc.creation_depense(montant,entreprise,date,categorie,com)
        if depense is None:
            return 0
        else:
            fc.ajout_depense(self.compte,depense)
            self.refreshAll()
            return 1

    def ajouter_virement_auto(self,debut,fin,ech,montant,cat,com,ent):
        if fc.creation_depense_automatique(self.compte,debut,fin,ech,
                                           montant,cat,com,ent):
            fc.actualisation_depense_auto(self.compte)
            self.refreshAll()
            return 1
        else:
            return 0

    def ajouter_virement(self,index1,index2,montant,categorie,date,com1,com2):
        if fc.creation_virement(self.liste_comptes[index1],
                                self.liste_comptes[index2],
                                montant, categorie, date, com1, com2):
            self.refreshAll()
            return 1
        else:
            return 0

    def trier_depense_general(self,index):
        if (index == 0): # Date
            fc.tri_dep_date(self.compte)
        elif (index == 1): # Montant
            fc.tri_dep_montant(self.compte)
        elif (index == 2): # Categorie
            fc.tri_dep_categorie(self.compte)

    def date_init_graph1(self):
        return fc.find_init_date(self.compte)

    def historique_graph1(self, date_debut, date_fin):
        list_date, list_somme = fc.recup_list_historique(self.compte)
        return fc.list_historique_in_range(list_date, list_somme, date_debut, date_fin)

    def ajout_depense(self,somme,categorie,date,commentaire,entreprise):
        depense=fc.depense()
        depense.init_value(somme,categorie,date,commentaire,entreprise)
        fc.ajout_depense(self.compte,depense)
        self.refreshAll()

    def read_csv_depenses(self,path):
        fc.read_csv_depenses(self.compte,path[0])
        self.refreshAll()

    def ajout_budget(self,categorie,montant,frequence,debut):
        budget=fc.budget()
        budget.init_value(categorie,montant,frequence,debut)
        fc.ajout_budget(self.compte,budget)
        self.refreshAll()

    # Fonction pour trier des dépenses par date pour une catégorie donnée
    def trier_depenses(self,categorie):
        # categorie: nom de la catégorie (str)
        # periode: listes à deux élements (type datetime) avec le premier
        # élement la date de debut et le deuxième élement la date de fin
        depenses_triees=fc.trier_depenses_compte(self.compte,categorie)
        depenses_triees_periode=[]
        # Selection des dépenses qui rentrent dans la période souhaitée
        for i in depenses_triees:
            if i.date>=self.periode_obs_dep[0] and i.date<=self.periode_obs_dep[1]:
                depenses_triees_periode.append(i)
        # Calcul de la somme des dépenses pour la catégorie et période souhaitée
        somme=0
        for i in depenses_triees_periode:
            somme=i.somme+somme
        # Si depenses_triees_periode alors somme=0
        return(depenses_triees_periode,somme)

    def change_periode_obs_dep(self,date_debut,date_fin):
        self.periode_obs_dep=[date_debut,date_fin]
        self.refreshAll()

    # Fonction pour la deuxième onglet
    def choix_categorie_depenses(self,categorie):
        self.categorie_evolution=categorie
        self.refreshAll()

    def init(self):
        self.refreshAll("Initialisation du controleur")
