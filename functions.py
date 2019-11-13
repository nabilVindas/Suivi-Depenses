# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:46:31 2019

@author: nayab
"""

import sys
import pickle
import time
import datetime as dt

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
        self.date=date
        self.commentaire=commentaire
        self.entreprise=entreprise
        self.__key=f'D{round(time.time())}'


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
# =============================================================================

# =============================================================================
# Ajout depenses sur compte
def ajout_depense(compte,depense):
    compte.depenses.append(depense)
    compte.mise_a_jour_montant(depense.somme)
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

def virement(compte1,compte2,montant,commentaire):
    """ Virement du compte 1 vers le compte 2"""
    depense_compte1=depense()
    depense_compte2=depense()
    date=dt.datetime.now().strftime("%d/%m/%Y")
    depense_compte1.init_value(-montant,"virement",date,commentaire,compte2.name)
    depense_compte2.init_value(montant,"virement",date,commentaire,compte1.name)
    
    ajout_depense(compte1,depense_compte1)
    ajout_depense(compte2,depense_compte2)
    
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
        if dt.datetime.strptime(compte.depenses_auto[i].date,"%d/%m/%Y")<=dt.datetime.now():
            ajout_depense(compte,compte.depenses_auto[i])
            indices.append(i)
    k=0
    for i in indices:
        del(compte.depenses_auto[i-k])
        k=k+1
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
        if i.categorie==categorie:
            depenses_inter.append(i)
    depenses_inter.sort(key=lambda item:item.date)
    return(depenses_inter)
    
# =============================================================================

###########################################################################################################


def test():
    compte1=compte()
    compte1.init_value("test","type",500,credit=None,interest=None)
    depense1=depense()
    depense1.init_value(-100,"Loisirs","22/10/2019","commentaire","entreprise")
    ajout_depense(compte1,depense1)
    
    depense2=depense()
    depense2.init_value(-300,"Loisirs","25/10/2019","commentaire","entreprise")
    ajout_depense(compte1,depense2)
    
    compte1.new_doc()
    
    compte2=lecture(key_list[0])
#    print(compte2.balance, compte2.name)
    
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
    test2()
