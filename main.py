#Fichier principal du projet Modelo3D

import BDDconnexion
import LAStoVTK
import OBJtoVTK
import pdalToVTK

def menu():
    choix = [
        'Ajouter un fichier source pour le traiter',
        'Ajouter un fichier source pour l\'enregistrer dans le base de données'',
        'Effectuer un traitement sur un fichier existant sur la base de données',
        'Visualiser un maillage pré-traité',
        'Récupérer un fichier au format OBJ (post-traitement)',
        'Faire une requête libre sur la base de données (dev)'
        ]
    choix = int(input(
    "Que souhaitez-vous faire :\n1 : Faire une requête sur la base de données (PostgreSQL)\n2 : "))

def requete():
    query = str(input("Veuillez entrer une requête SQL (SELECT...FROM...WHERE...) : "))
    res = BDDconnexion.connexion(query)
    return res

if __name__=='__main__':
