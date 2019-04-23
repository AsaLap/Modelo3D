#coding : utf-8
#Fichier principal du projet Modelo3D

import BDDconnexion
# import OBJtoVTK
import PDALtoVTK

def requete():
    query = str(input("Veuillez entrer une requête SQL (SELECT...FROM...WHERE...) : "))
    res = BDDconnexion.connexion(query)
    return res

def quit():
    global GoOn
    GoOn = False

def menu():
    while (GoOn):
        choix = [
            ['Ajouter un fichier source pour le traiter',lambda : addFileToRun()],
            ['Ajouter un fichier source pour l\'enregistrer dans le base de données',lambda : addFileToStore()],
            ['Effectuer un traitement sur un fichier existant sur la base de données',lambda : runProcess()],
            ['Visualiser un maillage pré-traité',lambda : view()],
            ['Récupérer un fichier au format OBJ (post-traitement)',lambda : getOBJ()],
            ['Faire une requête libre sur la base de données (developpeurs uniquement)',lambda : requete()],
            ['Quitter', lambda : quit()]
            ]
        for i in range(len(choix)):
            print(str(i+1) + " : " + choix[i][0])
        numChoix = int(input())
        try:
            choix[numChoix-1][1]() #Appel de lafonction contenue dans la liste à l'indice donné par l'utilisateur
        except:
            print("Echec de la fonction")


if __name__=='__main__':
    GoOn = True
    menu()
