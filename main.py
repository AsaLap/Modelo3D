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


def get_one_or_two(prompt):
    """
        Fonction pratique permettant de vérifier l'input 1 ou 2 utilisateur.
        ARGS : le message d'input
        RETURN : le chiffre choisi
    """
    try:
        return int(input(prompt))
    except:
        print ("Choix non valide !")
        get_one_or_two(prompt)


def fic_input():
    lidar = False
    file = str(input("Quel fichier voulez-vous utiliser (chemin d'accès complet si pas dans le répertoire courant) : "))
    extension, run = test_format(file)
    if (not run):
        return
    elif (extension == "csv"):
        CSVFile = file
        #TODO Fonction d'input secure
        testLid = get_one_or_two("Est-ce que votre fichier provient d'une acquisition lidar ? (1 : Oui, 2 : Non) : ")
        if (testLid == 1):
            lidar = True
    else:
        CSVFile = converter(file,extension)
        if (extension == 'las' or extension == 'laz'):
            lidar = True
    return CSVFile,lidar


def file_to_run():
    """
        Fonction qui lance le traitement sur le fichier souhaité après
        vérification du format et conversion en CSV si nécessaire.
        ARGS : None
        RETURN : None
    """
    CSVFile,lidar = fic_input()
    socle = get_one_or_two("Voulez-vous ajouter un socle au traitement afin de l'imprimer en 3D par la suite ? (1 : Oui, 2 : Non) : ")
    modulo = int(input("modulo : "))
    bounds = PDALtoVTK.pipeline_VTK(CSVFile,lidar,socle,modulo)


def file_to_store():
    """
        Fonction qui sauvegarde le fichier sur la base données après
        vérification de son format et conversion en CSV si nécessaire
        ARGS : None
        RETURN : None
    """
    CSVFile,lidar = fic_input()
    planete = ""
    while (planete == ""):
        planete = str(input("De quelle planète ou astre s'agit-il ? : ")).replace("'"," ")
    commentaires = str(input("Avez-vous des commentaires à ajouter pour ce fichier ? : ")).replace("'"," ")
    entries = [str(lidar),planete,commentaires]
    BDDconnexion.set_file(CSVFile,entries,CSV_PATH,IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD,PORT_SSH,PORT_POSTGRES,BDD_USER,BDD_PASSWORD,DATABASE)


def run_process():
    """
        Fonction...
        ARGS :
        RETURN :
    """
    CSVFile,lidar,id = BDDconnexion.get_file(CSV_PATH,LOCAL_PATH,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE)
    file = LOCAL_PATH + CSVFile
    socle = get_one_or_two("Voulez-vous ajouter un socle au traitement afin de l'imprimer en 3D par la suite ? (1 : Oui, 2 : Non) : ")
    bounds = PDALtoVTK.pipeline_VTK(CSVFile,lidar,socle)
    query = "update csv set x_min = "+str(bounds[0])+", x_max = "+str(bounds[1])+", y_min = "+str(bounds[2])+", y_max = "+str(bounds[3])+", z_min = "+str(bounds[4])+", z_max = "+str(bounds[5])+" where id="+str(id)+";"
    print(query)
    BDDconnexion.make_query(query,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE)
    choix = get_one_or_two("Voulez-vous enregistrer le rendu OBJ dans la base de données ? (1 : Oui, 2 : Non) : ")
    if (choix == 1):
        OBJFile = CSVFile[:-3] + 'obj'
        print(OBJFile)
        entries = [str(id)]
        print(entries)
        BDDconnexion.set_file(OBJFile,entries,OBJ_PATH,IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD,PORT_SSH,PORT_POSTGRES,BDD_USER,BDD_PASSWORD,DATABASE)


def get_CSV_OBJ():
    """
        Fonction...
        ARGS :
        RETURN :
    """
    choix = get_one_or_two("CSV (1) ou OBJ (2) : ")
    if (choix == 1):
        BDDconnexion.get_file(CSV_PATH,LOCAL_PATH,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE)
    elif (choix == 2):
        BDDconnexion.get_file(OBJ_PATH,LOCAL_PATH,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE)
    else:
        print("Choix non valide, retour au menu !")


def viewOBJ_VTK():
    """
        Fonction permettant de passer d'un fichier OBJ (post-traitement) à une
        visualisation avec la bibliothèque VTK.
        ARGS : None
        RETURN : None
    """
    choix = get_one_or_two("Utiliser un fichier local (1) ou enregistré sur la base de données (2) : ")
    if (choix == 1):
        fic = str(input("Quel fichier voulez-vous utiliser (chemin d'accès complet si pas dans le répertoire courant) : "))
    elif (choix == 2):
        fic,lidar,id = BDDconnexion.get_file(OBJ_PATH,LOCAL_PATH,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE)
        fic = LOCAL_PATH + fic
    extension,go = test_format(fic)
    print(extension)
    if (go):
        PDALtoVTK.pipeline_VTK(fic,lidar,2)


#TODO
def view_Unity3D():
    """
        Fonction permettant de passer d'un fichier OBJ (post-traitement) à une
        visualisation avec la bibliothèque Unity3D.
        NB : Fonction non implémentée.
        ARGS : None
        RETURN : None
    """
    return null


def mode_libre():
    """
        Fonction permettant de taper des commande directement dans terminal.
        NB : Une seule fonction actuellement, pipeline_VTK().
        ARGS : None
        RETURN : None
    """
    libre = True
    fonctions = ["pipeline_VTK"]
    nbArgs = {"pipeline_VTK":[2,4]}
    helpFonctions = {"pipeline_VTK(fic,lidar,socleChoix,modulo)":{"fic":"Le fichier\
 à traiter (string)","lidar":"Si votre fichier provient d'une acquisition lidar\
 (True or False)","socleChoix":"Si vous souhaitez un socle, par défaut = 2,\
 (1 = Oui, 2 = Non)","modulo":"Si vous souhaitez accélérer le traitement en\
 divisant votre fichier, par défaut = 1 (valeur minimale)"}}
    print("\"help\" pour avoir de l'aide sur les fonctions disponibles en terminal, \"quit\" pour quitter")
    while(libre):
        entry = str(input())
        if (entry == "help"):
            for key in helpFonctions:
                print(key)
                for args in helpFonctions[key]:
                    print(args, ":", helpFonctions[key][args])
        elif (entry == "quit"):
            libre = False
        else:
            splited = entry.split("(")
            fonc = splited[0]
            splited.pop(0)
            splited = splited[0].replace(")","")
            arguments = splited.split(",")
            if (fonc in fonctions):
                if (len(arguments) < nbArgs[fonc][0] or len(arguments) > nbArgs[fonc][1]):
                    print("Trop ou pas assez d'arguments, "+str(nbArgs[fonc][0])+" argument(s) minimum et "+str(nbArgs[fonc][1])+" argument(s) maximum pour cette fonction.")
                else:
                    if (fonc == "pipeline_VTK"):
                        if (arguments[1] == "True"):
                            arguments[1] = True
                        else:
                            arguments[1] = False
                        print(arguments)
                        if (len(arguments) >= 3):
                            arguments[2] = int(arguments[2])
                        print(arguments)
                        if (len(arguments) == 4):
                            arguments[3] = int(arguments[3])
                        print("ok")
                        PDALtoVTK.pipeline_VTK(*arguments)
            else:
                print("Fonction non reconnue...")



def stock():
    choix = get_one_or_two("Vous voules récupérer (1) ou ajouter (2) un fichier ? : ")
    if (choix == 1):
        BDDconnexion.get_file(STOCK_PATH,LOCAL_PATH,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE)
    elif (choix == 2):
        stock = str(input("Veuillez donner le nom du fichier (avec extension) ainsi que son chemin s'il n'est pas dans le dossier courant : "))
        entries = []
        BDDconnexion.set_file(stock,entries,STOCK_PATH,IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD,PORT_SSH,PORT_POSTGRES,BDD_USER,BDD_PASSWORD,DATABASE)
    else:
        print("Choix non valide, retour au menu !")


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
            ['Récupérer un fichier au format CSV (pré traitement) ou OBJ (post traitement)', lambda : get_CSV_OBJ()],
            ['Visualiser un fichier OBJ via VTK', lambda : viewOBJ_VTK()],
            # ['Visualiser un maillage (post-traitement) via Unity3D', lambda : view()],
            ['Mode libre (Dev)', lambda : mode_libre()],
            ['Stockage', lambda : stock()],
            ['Quitter', lambda : quit()]
            ]
        for i in range(len(choix)):
            print(str(i+1) + " : " + choix[i][0])
        numChoix = int(input())
        if (numChoix <= len(choix)):
            try:
                choix[numChoix-1][1]() #Appel de la fonction contenue dans la liste à l'indice donné par l'utilisateur
            except:
                print("Echec de la fonction")
        else:
            print("Choix non valide !")


if __name__=='__main__':
    GoOn = True
    config,ALLOWED_FORMATS = read_config()

    ### Attribution des valeurs aux constantes via fichier de configuration ###
    CSV_PATH = config['PATH']['CSV_PATH']
    OBJ_PATH = config['PATH']['OBJ_PATH']
    LOCAL_PATH = config['PATH']['LOCAL_PATH']
    STOCK_PATH = config['PATH']['STOCK_PATH']
    IP_PUBLIQUE = config['SSH']['IP_PUBLIQUE']
    IP_LOCALE = config['SSH']['IP_LOCALE']
    PORT_SSH = int(config['SSH']['PORT_SSH'])
    PORT_POSTGRES = int(config['SSH']['PORT_POSTGRES'])
    USER = config['SSH']['USER']
    PASSWORD = config['SSH']['PASSWORD']
    BDD_USER = config['BDD']['BDD_USER']
    BDD_PASSWORD = config['BDD']['BDD_PASSWORD']
    DATABASE = config['BDD']['DATABASE']
    MODULO = int(config['PROCESS']['MODULO'])
    ###---###

    menu()
