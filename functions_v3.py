# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:46:31 2019

@author: nayab
"""

import sys
import os
import pickle
import time
import datetime as dt
from dateutil.relativedelta import relativedelta
import csv

key_list=[]
categorie_list=["Salaire","Nourriture","Loisirs","Transport","Investissement","Utile"]

class compte:
    global key_list
    def __init__(self):
        self.__key=None
        self.name=None
        self.type=None
        self.balance=None
        self.depenses=[]
        self.credit=None
        self.interest=None
        self.depenses_auto=[]
        self.budgets=[]

    def get_key(self):
        return(self.__key)

    def new_doc(self):
        try:
            f=open(f'{self.__key}.bin','wb')
            pickle.dump(self,f,pickle.HIGHEST_PROTOCOL)
            f.close()
        except:
            print('Error: compte inconnu')

    def init_value(self,name,type_compte,balance,credit=None,interest=None):
        self.name=name
        self.type=type_compte
        self.balance=balance
        self.credit=credit
        self.interest=interest
        self.__key=f'C{round(time.time())}'
        key_list.append(self.__key)


    def mise_a_jour_montant(self,dep):
        try:
            self.balance=self.balance+dep
        except:
            print("Error: compte inconnu")


class depense:
    def __init__(self):
        self.somme=None
        self.categorie=None
        self.date=None
        self.commentaire=None
        self.entreprise=None
        self.__key=None

    def init_value(self,somme,categorie,date,commentaire,entreprise):
        self.somme=somme
        self.categorie=categorie
        try:
            self.date=dt.datetime.strptime(date,'%d/%m/%Y')
        except:
            self.date=dt.datetime.strptime(date,'%d/%m/%y')
        self.commentaire=commentaire
        self.entreprise=entreprise
        self.__key=f'D{round(time.time())}'

class budget:
    def __init__(self):
        self.categorie=None
        self.somme=None
        self.frequence=None
        self.debut=None

    def init_value(self,categorie:str, somme:float,frequence:str,debut:str):
        self.categorie=categorie
        self.somme=somme
        self.frequence=frequence
        self.debut=dt.datetime.strptime(debut,'%d/%m/%Y')

class donne_bourse:
    def __init__(self):
        self.nom=None
        self.ISIN=None
        self.symbole=None
        self.marche=None
        self.currency=None
        self.ouvert=None
        self.haut=None
        self.bas=None
        self.dernier=None
        self.last_date_time=None
        self.time_zone=None
        self.volume=None
        self.capitaux=None

    def init_value(self,nom,ISIN,symbole,marche,currency,ouvert,haut,bas,dernier,last_date_time,time_zone,volume,capitaux):
        self.nom=nom
        self.ISIN=ISIN
        self.symbole=symbole
        self.marche=marche
        self.currency=currency
        self.ouvert=ouvert
        self.haut=haut
        self.bas=bas
        self.dernier=dernier
        self.last_date_time=last_date_time
        self.time_zone=time_zone
        self.volume=volume
        self.capitaux=capitaux

# =============================================================================
# Lecture fichier compte
def lecture(key):
    f=open(f'{key}.bin','rb')
    compte_inter=pickle.load(f)
    f.close()
    return(compte_inter)

# Lecture de tous les comptes dans une liste
def lecture_liste_compte():
    global key_list
    list_comptes = []
    for key in key_list:
        list_comptes.append(lecture(key))
    return list_comptes

# Ecriture d'un compte à partir de chaine de caractère
def creation_compte(nom,typ,montant,credit,interet):
    if (nom is not '') and (typ is not '') and (montant is not ''):
        montant = float(montant)
        if (credit is '') or (credit == 'Optionnel'):
            credit = None
        else:
            credit = float(credit)
        if (interet is '') or (interet == 'Optionnel'):
            interet = None
        else:
            interet = float(interet)
        new_compte = compte()
        new_compte.init_value(nom,typ,montant,credit,interet)
        return new_compte
    else:
        return None

#Suppression d'un compte des données (fichier, clé)
def supprimer_compte(compte):
    global key_list
    key = compte.get_key()
    key_list.remove(key)
    os.remove('{}.bin'.format(key))


# =============================================================================

# =============================================================================
# Ajout depenses sur compte
def ajout_depense(compte,depense):
    compte.depenses.append(depense)
    compte.mise_a_jour_montant(depense.somme)

#Création d'une dépense à partir de chaine de caratère
def creation_depense(montant,entreprise,date,categorie,commentaire):
    if (montant is not '') and (entreprise is not ''):
        montant = float(montant)
        date_str = "{:02d}/{:02d}/{:04d}".format(date.day(),
                    date.month(),date.year())
        new_depense = depense()
        new_depense.init_value(montant,categorie,date_str,
                               commentaire,entreprise)
        return new_depense
    else:
        return None
# Fonction pour lire un fichier csv avec les depenses_auto
def read_csv_depenses(compte,path):
    with open(path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            depense_inter=depense()
            try:
                depense_inter.init_value(float(row[0]),row[1],row[2],row[3],row[4])
                ajout_depense(compte,depense_inter)
            except:
                pass

# Ajout budget sur compte
def ajout_budget(compte,budget):
    verification=0
    for i in range(len(compte.budgets)):
        if budget.categorie.capitalize()==compte.budgets[i].categorie.capitalize():
            compte.budgets[i].somme=budget.somme
            verification=1
            break
    if verification==0:
        compte.budgets.append(budget)
# =============================================================================

# =============================================================================
#  Lecture/ecriture documents avec les cles
def ecriture_key_document():
    global key_list
    f=open(f'key_list.bin','wb')
    pickle.dump(key_list,f,pickle.HIGHEST_PROTOCOL)
    f.close()

def lecture_key_document():
    global key_list
    f=open(f'key_list.bin','rb')
    key_list=pickle.load(f)
    f.close()

# =============================================================================



# =============================================================================
#  Virement

def virement(compte1,compte2,montant,categorie,date,com1,com2):
    """ Virement du compte 1 vers le compte 2"""
    depense_compte1=depense()
    depense_compte2=depense()
    depense_compte1.init_value(-montant,categorie,date,com1,compte2.name)
    depense_compte2.init_value(montant,categorie,date,com2,compte1.name)
    ajout_depense(compte1,depense_compte1)
    ajout_depense(compte2,depense_compte2)

# Création d'un virement à partir de chaine de caratère
def creation_virement(compte1,compte2,montant,categorie,date,com1,com2):
    if (montant is not ''):
        montant = float(montant)
        date_str = "{:02d}/{:02d}/{:04d}".format(date.day(),
                    date.month(),date.year())
        virement(compte1,compte2,montant,categorie,date_str,com1,com2)
        return 1
    else:
        return 0

# =============================================================================


# =============================================================================
#  Automatisation depenses
def depense_automatique(compte,date_debut,date_fin,echeance,montant,categorie, commentaire,entreprise):
    date_debut=dt.datetime.strptime(date_debut,"%d/%m/%Y")
    date_fin=dt.datetime.strptime(date_fin,"%d/%m/%Y")
    date=date_debut
    while date<date_fin:
        depense_inter=depense()
        depense_inter.init_value(montant,categorie,date.strftime("%d/%m/%Y"),commentaire,entreprise)
        compte.depenses_auto.append(depense_inter)
        date=date+echeance


def actualisation_depense_auto(compte):
    indices=[]
    for i in range(len(compte.depenses_auto)):
        if compte.depenses_auto[i].date<=dt.datetime.now():
            ajout_depense(compte,compte.depenses_auto[i])
            indices.append(i)
    k=0
    for i in indices:
        del(compte.depenses_auto[i-k])
        k=k+1

def creation_depense_automatique(compte,debut,fin,ech,montant,cat,com,ent):
    if (montant is not '') and (ent is not '') and (ech != '00/00'):
        list_ech = ech.split("/")
        ech = relativedelta(months=int(list_ech[1]),days=int(list_ech[0]))
        montant = float(montant)
        depense_automatique(compte,debut,fin,ech,montant,cat,com,ent)
        return 1
    else:
        return 0
# =============================================================================

# =============================================================================
# Categories

def ajout_categorie(categorie:str):
    global categorie_list
    categorie_list.append(categorie)

def ecriture_categorie_document():
    global categorie_list
    f=open(f'categorie_list.bin','wb')
    pickle.dump(categorie_list,f,pickle.HIGHEST_PROTOCOL)
    f.close()

def lecture_categorie_document():
    global categorie_list
    f=open(f'categorie_list.bin','rb')
    categorie_list=pickle.load(f)
    f.close()
# =============================================================================


# =============================================================================
#  Triage des depenses par catégorie
def trier_depenses_compte(compte,categorie):
    depenses_inter=[]
    for i in compte.depenses:
        try:
            if i.categorie==categorie:
                depenses_inter.append(i)
        except:
            pass
    try:
        depenses_inter.sort(key=lambda item:item.date)
    except:
        var_int=depense()
        var_int.init_value(0,categorie,"01/01/00",None,None)
        depenses_inter.append(var_int)

    return(depenses_inter)


# Tri par Date recent>ancien, puis Categorie
def tri_dep_date(compte):
    compte.depenses.sort(key=lambda item:item.categorie)
    compte.depenses.sort(key=lambda item:item.date,reverse=True)

# Tri par Montant +>-, puis Date
def tri_dep_montant(compte):
    compte.depenses.sort(key=lambda item:item.date,reverse=True)
    compte.depenses.sort(key=lambda item:item.somme,reverse=True)

# Tri par Categorie, puis Montant
def tri_dep_categorie(compte):
    compte.depenses.sort(key=lambda item:item.somme,reverse=True)
    compte.depenses.sort(key=lambda item:item.categorie)



# =============================================================================
# Traitement des données en graph


# Trouver la date de la première dépense (-1 jour pour un meilleur visuelle sur le graph)
def find_init_date(compte):
    init_date = dt.datetime.now()
    for dep in compte.depenses:
        # print(dep.date)
        if dep.date<=init_date:
            init_date = dep.date
    # sys.exit()
    init_date = init_date - dt.timedelta(days=1)
    return init_date.strftime("%d/%m/%Y")

# Récupération de la liste de montant et de la liste de date (str)
def recup_list_historique(compte):
    date = dt.datetime.now()
    date = dt.datetime(date.year,date.month,date.day)
    somme = compte.balance
    list_date = [date.strftime("%d/%m/%Y")]
    list_somme = [somme]
    tri_dep_date(compte)
    nb_dep = len(compte.depenses)
    i = 0
    while date <= compte.depenses[i].date:
        date = date + dt.timedelta(days=1)
    while (i != nb_dep):
        if (date == compte.depenses[i].date):
            somme = somme - compte.depenses[i].somme
            i = i+1
        else:
            date = date - dt.timedelta(days=1)
            list_date.append(date.strftime("%d/%m/%Y"))
            list_somme.append(somme)
    date = date - dt.timedelta(days=1)
    list_date.append(date.strftime("%d/%m/%Y"))
    list_somme.append(somme)
    list_date.reverse()
    list_somme.reverse()
    return (list_date,list_somme)


# Renvoie seulement la liste de montant et de date (str) dans la période selctionné (str)
def list_historique_in_range(list_date, list_somme, date_debut, date_fin):
    date_debut = dt.datetime.strptime(date_debut,"%d/%m/%Y")
    date_fin = dt.datetime.strptime(date_fin,"%d/%m/%Y")
    indices = []
    for i in range(len(list_date)):
        d = dt.datetime.strptime(list_date[i],"%d/%m/%Y")
        if (d<date_debut or d>date_fin):
            indices.append(i)
    k=0
    for i in indices:
        del(list_date[i-k])
        del(list_somme[i-k])
        k=k+1
    return (list_date,list_somme)


###########################################################################################################
# Fonction pour lire un fichier csv avec les données de bourse
def read_csv_bourse(compte,path):
    with open(path) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            bourse_inter=depense()
            try:
                bourse_inter.init_value(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12])
            except:
                pass


###########################################################################################################


def test():
    compte1=compte()
    compte1.init_value("test","type",500,credit=None,interest=None)

    # Ajout de 1 dépense dans chaque catégorie
    montant_depense=1500
    for i in categorie_list:
        depense1=depense()
        depense1.init_value(montant_depense,i,"22/10/2019","commentaire","entreprise")
        ajout_depense(compte1,depense1)
        if montant_depense==1500:
            montant_depense=-250
        else:
            montant_depense=montant_depense-50
        print(compte1.balance)

    # Ajout de une autre dépense dans chaque catégorie
    montant_depense=2000
    for i in categorie_list:
        depense1=depense()
        depense1.init_value(montant_depense,i,"25/10/2019","commentaire","entreprise")
        ajout_depense(compte1,depense1)
        if montant_depense==2000:
            montant_depense=-300
        else:
            montant_depense=montant_depense-50
        print(compte1.balance)

    # Ajout des budgets
    montant_budget=100;
    for i in categorie_list:
        budget1=budget()
        budget1.init_value(i,montant_budget,"Jour","21/11/2019")
        ajout_budget(compte1, budget1)
        if montant_budget<700:
            montant_budget=montant_budget+300
        else:
            montant_budget=montant_budget-600

    compte1.new_doc()

    compte2=lecture(key_list[0])
    print(compte2.balance, compte2.name)

    depense_automatique(compte1,"20/10/2019","20/11/2019",dt.timedelta(days=1),100,"categorie", "commentaire","entreprise")

    #########Lignes à écrire avant fermeture############
    compte1.new_doc()
    ecriture_key_document()
    ecriture_categorie_document()

def test2():
    #########Lignes à écrire après ouverture############
    lecture_key_document() # Ne pas oublier ouvrir le fichier dès qu'on lance le programme
    compte2=lecture(key_list[0])   # Une ligne pour chaque compte (boucle)
    lecture_categorie_document()
    ######## Tests ########
    print(key_list)
    print(categorie_list)
    print(compte2.balance, compte2.name)

    actualisation_depense_auto(compte2) # A lancer au debut du programme

#    compte1=compte()
#    compte1.init_value("test","type",500,credit=None,interest=None)
#
#    virement(compte1,compte2,200,"virement test")

    ppp=trier_depenses_compte(compte2,"Loisirs")
    print(ppp[1].date)

    print(compte2.balance, compte2.name)

    #########Lignes à écrire avant fermeture############
    compte2.new_doc()
    ecriture_key_document()
    ecriture_categorie_document()


if __name__=='__main__':
    test()
    # test2()
