#coding : utf-8
#Fichier principal du projet Modelo3D

import BDDconnexion
import PDALtoVTK


def convertisseur(file,extension):
    return fileConvertie


def file_to_run():
    file = str(input("Quel fichier voulez-vous utiliser (chemin d'accès complet si pas dans le répertoire courant) : "))
    #Conversion du fichier si pas CSV
    test_format(file)


def run_process():
    fic = BDDconnexion.get_file('/media/pi/BDD_Data/Raw/CSV')
    PDALtoVTK.pipeline_VTK(fic,100000)
    return untruc


def test_format(file):
    splited_file = file.split('.')
    extension = (splited_file[len(splited_file)-1]).lower()
    if (extension not in ALLOWED_FORMATS):
        formats = " - ".join(ALLOWED_FORMATS)
        print("Le format de ce fichier (.", extension, ") n'est pas pris en charge, merci d'utiliser un format supporté : ", formats)
    else:
        hostPath = '/media/pi/BDD_Data/Raw/' + ALLOWED_FORMATS[extension]


def file_to_store():
    file = str(input("Veuillez donner le nom du fichier (avec extension) ainsi que son chemin s'il n'est pas dans le dossier courant : "))

    BDDconnexion.set_file(inputFile,hostPath)


def view_Unity3D():
    print(untruc)


def get_OBJ():
    print("Quel fichier voulez-vous récupérer ? (Il sera téléchargé dans votre répertoire courant)")
    BDDconnexion.get_file('/media/pi/BDD_Data/Output')


def requete():
    query = str(input("Veuillez entrer une requête SQL (SELECT...FROM...WHERE...) : "))
    res = BDDconnexion.make_query(query)
    for resultat in res:
        print(resultat)


def read_config():
    fic


def quit():
    global GoOn
    GoOn = False


def menu():
    while (GoOn):
        choix = [
            ['Utiliser un fichier source (local) pour le traiter', lambda : file_to_run()],
            ['Effectuer un traitement sur un fichier existant sur la base de données', lambda : run_process()],
            ['Ajouter un fichier source pour l\'enregistrer dans le base de données', lambda : file_to_store()],
            ['Visualiser un maillage (post-traitement) via Unity3D', lambda : view()],
            ['Récupérer un fichier au format OBJ (post-traitement)', lambda : get_OBJ()],
            ['Mode libre (Dev)', lambda : requete()],
            ['Quitter', lambda : quit()]
            ]
        for i in range(len(choix)):
            print(str(i+1) + " : " + choix[i][0])
        numChoix = int(input())
        try:
            choix[numChoix-1][1]() #Appel de la fonction contenue dans la liste à l'indice donné par l'utilisateur
        except:
            print("Echec de la fonction")


if __name__=='__main__':
    GoOn = True
    ALLOWED_FORMATS = ['las','laz','csv']
    menu()
