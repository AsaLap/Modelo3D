#coding : utf-8
#Fichier principal du projet Modelo3D

import BDDconnexion
import PDALtoVTK
import configparser


def converter(file,extension):
    print("Conversion du fichier en CSV...")
    try:
        #TODO : conversion avec PDAL
        print("...conversion réussie !")
    except:
        print("...conversion échouée !")
    return fileConvertie


def test_format(file):
    """
        Fonction qui teste si le format du fichier entré est pris en charge
        ARGS : le fichier d'entrée
        RETURN : l'extension et un booléen d'acceptation ou non de l'extension
    """
    splitedFile = file.split('.')
    extension = (splitedFile[len(splitedFile)-1]).lower()
    if (extension not in ALLOWED_FORMATS):
        formats = " - ".join(ALLOWED_FORMATS)
        print("Le format de ce fichier (.", extension, ") n'est pas pris en charge, merci d'utiliser un format supporté : ", formats)
        return extension,False
    else:
        return extension,True


#Manque la fonction de conversion
def file_to_run():
    """
        Fonction qui lance le traitement après vérification du format et
        conversion si nécessaire, propose de sauvegarder le fichier sur la base
        de données
        ARGS : None
        RETURN : None
    """
    file = str(input("Quel fichier voulez-vous utiliser (chemin d'accès complet si pas dans le répertoire courant) : "))
    extension, run = test_format(file)
    if (not run):
        return
    elif (extension == "csv"):
        CSVFile = file
    else:
        CSVFile = converter(file,extension)
    PDALtoVTK.pipeline_VTK(CSVFile,100000)
    rep = int(input("Voulez-vous sauvegarder votre fichier d'entrée sur la base de données ? (1 : Oui, 2 : Non) : "))
    if (rep == 1):
        BDDconnexion.set_file(CSVFile,CSV_PATH,IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD,BDD_USER,BDD_PASSWORD)


#Manque la fonction de conversion
def file_to_store():
    """
        Fonction qui sauvegarde le fichier sur la base données après
        vérification de son format et conversion en CSV
        ARGS : None
        RETURN : None
    """
    file = str(input("Veuillez donner le nom du fichier (avec extension) ainsi que son chemin s'il n'est pas dans le dossier courant : "))
    extension, run = test_format(file)
    if (not run):
        return
    elif (extension == "csv"):
        CSVFile = file
    else:
        CSVFile = converter(file,extension)
    BDDconnexion.set_file(CSVFile,CSV_PATH,IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD,BDD_USER,BDD_PASSWORD)


def run_process():
    CSVFile = BDDconnexion.get_file(CSV_PATH,LOCAL_PATH,IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD)
    CSVFile = LOCAL_PATH + CSVFile
    PDALtoVTK.pipeline_VTK(CSVFile, 100000)
    return untruc


def view_Unity3D():
    print("untruc")


def get_OBJ():
    BDDconnexion.get_file(OBJ_PATH,LOCAL_PATH,IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD)


def mode_libre():
    #TODO : faire le parser pour le mode libre
    return


def read_config():
    config = configparser.ConfigParser()
    config.read('modelo.ini')
    ALLOWED_FORMATS = config['FORMATS']['ALLOWED_FORMATS'].split(',')
    return config,ALLOWED_FORMATS


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
    config,ALLOWED_FORMATS = read_config()
    ### Attribution des valeurs aux constantes ###
    CSV_PATH = config['PATH']['CSV_PATH']
    OBJ_PATH = config['PATH']['OBJ_PATH']
    LOCAL_PATH = config['PATH']['LOCAL_PATH']
    IP_PUBLIQUE = config['SSH']['IP_PUBLIQUE']
    IP_LOCALE = config['SSH']['IP_LOCALE']
    PORT_SSH = int(config['SSH']['PORT_SSH'])
    PORT_POSTGRES = int(config['SSH']['PORT_POSTGRES'])
    USER = config['SSH']['USER']
    PASSWORD = config['SSH']['PASSWORD']
    BDD_USER = config['BDD']['BDD_USER']
    BDD_PASSWORD = config['BDD']['BDD_PASSWORD']
    DATABASE = config['BDD']['DATABASE']
    menu()
