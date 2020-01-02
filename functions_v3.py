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
            
    def __repr__(self):
        return("<compte>:\nname->{}\ntype->{}\nmontant->{}".format(
            self.name, self.type, self.balance))


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
        
    def __repr__(self):
        return("<depense>:\nmontant->{}\ncategorie->{}\ndate->{}".format(
            self.somme, self.categorie, self.date.strftime('%d/%m/%Y')))

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
        
    def __repr__(self):
        return("<budget>:\ncategorie->{}\nsomme->{}".format(
            self.categorie, self.somme))


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
        
    def __repr__(self):
        return("<donne_bourse>:\nnom->{}\ncapitaux->{}".format(
            self.nom, self.capitaux))

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
        new_depense = depense()
        new_depense.init_value(montant,categorie,date,
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
        virement(compte1,compte2,montant,categorie,date,com1,com2)
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

def test_final():
    global key_list
    nb_test = 0
    nb_test_succed = 0
    
    #Test 1: creation d'un compte
    nb_test += 1
    nom = "compte test"
    typ = "type test"
    montant = "500"
    credit = "Optionnel"
    interet = ""
    try:
        compte_test = creation_compte(nom,typ,montant,credit,interet)
        if ((compte_test.name == nom) &
            (compte_test.type == typ) &
            (compte_test.balance == float(montant)) &
            (compte_test.credit is None) &
            (compte_test.interest is None)):
            print("Test 1 (create an account): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 1 (create an account): FAILED <result>")
    except:
        print("Test 1 (create an account): FAILED <system>")
    
    #Test 2: lecture des comptes
    nb_test += 1
    try:
        compte_test.new_doc()
        list_comptes = lecture_liste_compte()
        compte_read = list_comptes[0]
        if(compte_test.get_key() == compte_read.get_key()):
            print("Test 2 (read an account): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 2 (read an account): FAILED <result>")
    except:
        print("Test 2 (read an account): FAILED <system>")
       
    #Test 3: supprimer comptes
    nb_test += 1
    try:
        key = compte_test.get_key()
        supprimer_compte(compte_test)
        if ((not(os.path.exists('{}.bin'.format(key))))&
            (not(key in key_list))):
            print("Test 3 (delete an account): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 3 (delete an account): FAILED <result>")
    except:
        print("Test 3 (delete an account): FAILED <system>")
    
    #Test 4: creation d'une depense
    nb_test += 1
    montant1 = "-100"
    entreprise = "entreprise test"
    date = "01/01/2001"
    categorie = categorie_list[2]
    commentaire = "commentaire test"
    try:
        depense_test = creation_depense(montant1, entreprise, date, categorie, commentaire)
        if((depense_test.somme == float(montant1)) &
           (depense_test.categorie == categorie) &
           (depense_test.date == dt.datetime.strptime(date,'%d/%m/%Y')) &
           (depense_test.commentaire == commentaire) &
           (depense_test.entreprise == entreprise)):
            print("Test 4 (create an expense): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 4 (create an expense): FAILED <result>")
    except:
        print("Test 4 (create an expense): FAILED <system>")
    
    #test 5: ajout dépense CSV
    nb_test += 1
    path = "test_depense.csv"
    with open(path,'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([montant1,categorie,date,commentaire,entreprise])
    try:
        read_csv_depenses(compte_test,path)
        depense_read = compte_test.depenses[0]
        if((depense_read.somme == float(montant1)) &
           (depense_read.categorie == categorie) &
           (depense_read.date == dt.datetime.strptime(date,'%d/%m/%Y')) &
           (depense_read.commentaire == commentaire) &
           (depense_read.entreprise == entreprise) &
           (compte_test.balance == float(montant)+float(montant1))):
            print("Test 5 (append an expense CSV): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 5 (append an expense CSV): FAILED <result>")
    except:
        print("Test 5 (append an expense CSV): FAILED <system>")
        
    #test 6: ajout d'un budget
    nb_test += 1
    categorie = categorie_list[2]
    montant2 = 1000
    frequence = "Jour"
    date = "01/01/2001"
    try:
        budget_test = budget()
        budget_test.init_value(categorie,montant2,frequence,date)
        ajout_budget(compte_test, budget_test)
        budget_read = compte_test.budgets[0]
        if((budget_read.categorie == categorie) &
           (budget_read.somme == montant2) &
           (budget_read.frequence == frequence) &
           (budget_read.debut == dt.datetime.strptime(date,'%d/%m/%Y'))):
            print("Test 6 (append a budget): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 6 (append a budget): FAILED <result>")
    except:
        print("Test 6 (append a budget): FAILED <system>")
    
    #test 7: lecture et ecriture key_list
    nb_test +=1
    lecture_key_document()          # Pour ne pas écraser
    key_list_copy = key_list        # les données
    key_list_test = ['CTEST']
    try:
        key_list = key_list_test
        ecriture_key_document()
        key_list = []
        lecture_key_document()
        if(key_list == key_list_test):
            print("Test 7 (read & write key document): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 7 (read & write key document): FAILED <result>")
    except:
        print("Test 7 (read & write key document): FAILED <system>")
    key_list = key_list_copy
    ecriture_key_document()
    key_list = []
    
    #test 8: ajout d'un virement
    nb_test += 1
    montant_virement = "100"
    montant_init1 = 600
    montant_init2 = 900
    categorie = categorie_list[1]
    date = "01/01/2001"
    com1 = "com1 test"
    com2 = "com2 test"
    try:
        compte1=compte()
        compte1.init_value("c1","t1",montant_init1)
        compte2=compte()
        compte2.init_value("c2","t2",montant_init2)
        creation_virement(compte1, compte2, montant_virement, categorie, date, com1, com2)
        if((compte1.balance == montant_init1-float(montant_virement)) &
           (compte2.balance == montant_init2+float(montant_virement))):
            print("Test 8 (append a transfer): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 8 (append a transfer): FAILED <result>")
    except:
        print("Test 8 (append a transfer): FAILED <system>")
    
    #test 9: ajout d'une depense automatique
    nb_test += 1
    TEST = 1
    debut = "01/01/2019"
    fin = "01/01/2021"
    ech = "00/01"
    montant3 = "100"
    cat = categorie_list[3]
    com = "commentaire test"
    ent = "entreprise test"
    try:
        compte_test=compte()
        compte_test.init_value("compte test", "type test",500)
        creation_depense_automatique(compte_test, debut, fin, ech, montant3, cat, com, ent)
        date = dt.datetime.strptime(debut,"%d/%m/%Y")
        for d in compte_test.depenses_auto:
            if((d.date == date) &
               (d.categorie == cat) &
               (d.somme == float(montant3))):
                TEST *= 1
            else:
                TEST *= 0
            date += relativedelta(months=1)
        if((TEST) & (date == dt.datetime.strptime(fin,"%d/%m/%Y"))):
            print("Test 9 (append a automatic transfer): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 9 (append a automatic transfer): FAILED <result>")
    except:
        print("Test 9 (append a automatic transfer): FAILED <system>")
    
    #test 10: actualisation des depenses automatique
    nb_test += 1
    TEST = 1
    try:
        actualisation_depense_auto(compte_test)
        for d in compte_test.depenses_auto:
            if(d.date > dt.datetime.now()):
                TEST *= 1
            else:
                TEST *= 0
        for d in compte_test.depenses:
            if(d.date <= dt.datetime.now()):
                TEST *= 1
            else:
                TEST *= 0
        if(TEST):
            print("Test 10 (update automatic transfers): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 10 (update automatic transfers): FAILED <result>")
    except:
        print("Test 10 (update automatic transfers): FAILED <system>")
        
    #test 11: trier des dépenses d'une catégorie
    nb_test += 1
    date = "01/01/2001"
    categorie1 = categorie_list[0]
    montant1 = 100
    categorie2 = categorie_list[1]
    montant2 = 200
    try:
        depense1=depense()
        depense1.init_value(montant1,categorie1,date,"","")
        depense2=depense()
        depense2.init_value(montant2,categorie2,date,"","")
        ajout_depense(compte_test,depense1)
        ajout_depense(compte_test,depense2)
        list_dep = trier_depenses_compte(compte_test,categorie1)
        if((len(list_dep) == 1) &
           (list_dep[0].date == dt.datetime.strptime(date,"%d/%m/%Y")) &
           (list_dep[0].somme == montant1) &
           (list_dep[0].categorie == categorie1)):
            print("Test 11 (select category expenses): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 11 (select category expenses): FAILED <result>")
    except:
        print("Test 11 (select category expenses): FAILED")
    
    #test 12: tri depense par date
    nb_test += 1
    montant1 = 100
    cat1 = categorie_list[1]
    date1 = "05/01/2001"
    montant2 = 50
    cat2 = categorie_list[2]
    date2 = "10/01/2001"
    montant3 = 150
    cat3 = categorie_list[3]
    date3 = "15/01/2001"
    try:
        compte_test=compte()
        compte_test.init_value("compte test", "type test",500)
        depense1=depense()
        depense1.init_value(montant1,cat1,date1,"","")
        ajout_depense(compte_test,depense1)
        depense2=depense()
        depense2.init_value(montant2,cat2,date2,"","")
        ajout_depense(compte_test,depense2)
        depense3=depense()
        depense3.init_value(montant3,cat3,date3,"","")
        ajout_depense(compte_test,depense3)
        tri_dep_date(compte_test)
        if((compte_test.depenses[0].date > compte_test.depenses[1].date) &
           (compte_test.depenses[1].date > compte_test.depenses[2].date)):
            print("Test 12 (sort expenses by date): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 12 (sort expenses by date): FAILED <result>")
    except:
        print("Test 12 (sort expenses by date): FAILED <system>")
    
    #test 13: tri depense par montant
    nb_test += 1
    try:
        tri_dep_montant(compte_test)
        if((compte_test.depenses[0].somme > compte_test.depenses[1].somme) &
           (compte_test.depenses[1].somme > compte_test.depenses[2].somme)):
            print("Test 13 (sort expenses by amount): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 13 (sort expenses by amount): FAILED <result>")
    except:
        print("Test 13 (sort expenses by amount): FAILED <system>")
        
    #test 14: tri depense par categorie
    nb_test += 1
    try:
        tri_dep_categorie(compte_test)
        if((compte_test.depenses[0].categorie < compte_test.depenses[1].categorie) &
           (compte_test.depenses[1].categorie < compte_test.depenses[2].categorie)):
            print("Test 14 (sort expenses by category): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 14 (sort expenses by category): FAILED <result>")
    except:
        print("Test 14 (sort expenses by category): FAILED")
    
    #test 15: Trouver la date de la première depense
    nb_test += 1
    date_init = (dt.datetime.strptime(date1,"%d/%m/%Y")-dt.timedelta(days=1)).strftime("%d/%m/%Y")
    try:
        date_find = find_init_date(compte_test)
        if(date_find == date_init):
            print("Test 15 (find first expense date): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 15 (find first expense date): FAILED <result>")
    except:
        print("Test 15 (find first expense date): FAILED <system>")
    
    #test 16: Trouver la liste de date et de somme
    nb_test += 1
    mi = 500
    cat = categorie_list[1]
    m1 = -100
    date1 = (dt.datetime.now()-dt.timedelta(days=3)).strftime("%d/%m/%Y")
    m2 = 200
    date2 = (dt.datetime.now()-dt.timedelta(days=1)).strftime("%d/%m/%Y")
    resultat_somme = [mi, mi+m1, mi+m1, mi+m1+m2, mi+m1+m2]
    resultat_date = [(dt.datetime.now()-dt.timedelta(days=4-i)).
                     strftime("%d/%m/%Y") for i in range(5)]
    try:
        compte_test=compte()
        compte_test.init_value("compte test", "type test",mi)
        depense1=depense()
        depense1.init_value(m1,cat,date1,"","")
        ajout_depense(compte_test,depense1)
        depense2=depense()
        depense2.init_value(m2,cat,date2,"","")
        ajout_depense(compte_test,depense2)
        (list_date,list_somme) = recup_list_historique(compte_test)
        if((list_date == resultat_date) & (list_somme == resultat_somme)):
            print("Test 16 (find amounts/date history): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 16 (find amounts/date history): FAILED <result>")
    except:
        print("Test 16 (find amounts/date history): FAILED <system>")
    
    
    #test 17: Recuperation des listes dans une période
    nb_test += 1
    debut = (dt.datetime.now()-dt.timedelta(days=3)).strftime("%d/%m/%Y")
    fin = (dt.datetime.now()-dt.timedelta(days=1)).strftime("%d/%m/%Y")
    resultat_somme = [mi+m1, mi+m1, mi+m1+m2]
    resultat_date = [(dt.datetime.now()-dt.timedelta(days=3-i)).
                     strftime("%d/%m/%Y") for i in range(3)]
    try:
        (list_date,list_somme) = list_historique_in_range(list_date, list_somme, debut, fin)
        if((list_date == resultat_date) & (list_somme == resultat_somme)):
            print("Test 17 (amounts/date history in range): SUCCED")
            nb_test_succed += 1
        else:
            print("Test 17 (amounts/date history in range): FAILED <result>")
    except:
        print("Test 17 (amounts/date history in range): FAILED <system>")
    
    #FIN DES TESTS
    print("\nTest End ({:.0f}% SUCCED):\nTest Number -> {}\nTest Succed -> {}".format(
        nb_test_succed*100/nb_test,nb_test, nb_test_succed))
    

if __name__=='__main__':
    #test()
    #test2()
    test_final()
