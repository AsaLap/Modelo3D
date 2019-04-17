#coding : utf-8
#Fichier principal du projet Modelo3D

import BDDconnexion
# import OBJtoVTK
import PDALtoVTK

def menu():
    GoOn = True
    while (GoOn):
        choix = [
            'Ajouter un fichier source pour le traiter',
            'Ajouter un fichier source pour l\'enregistrer dans le base de données',
            'Effectuer un traitement sur un fichier existant sur la base de données',
            'Visualiser un maillage pré-traité',
            'Récupérer un fichier au format OBJ (post-traitement)',
            'Faire une requête libre sur la base de données (dev)',
            'Quitter'
            ]
        for i in range(len(choix)):
            print(str(i+1) + " : " + choix[i])
        choix = int(input())
        if (choix == 1):
            addFileToRun()
        elif (choix == 2):
            addFileToStore()
        elif (choix == 3):
            runProcess()
        elif (choix == 4):
            view()
        elif (choix == 5):
            getOBJ()
        elif (choix == 6):
            requete()
        elif (choix == 7):
            GoOn = False
        else:
            print("Demande non comprise")

def requete():
    query = str(input("Veuillez entrer une requête SQL (SELECT...FROM...WHERE...) : "))
    res = BDDconnexion.connexion(query)
    return res

if __name__=='__main__':
    menu()
