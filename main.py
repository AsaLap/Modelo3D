#coding : utf-8
#Fichier principal du projet Modelo3D

import BDDconnexion
import PDALtoVTK
import paramiko

def add_file_to_store():
    inputFile = str(input("Veuillez donner le nom du fichier (avec extension) ainsi que son chemin s'il n'est pas dans le dossier courant : "))
    splited_file = inputFile.split('.')
    extension = (splited_file[len(splited_file)-1]).lower()
    if (extension not in ALLOWED_FORMATS.keys()):
        formats = " - ".join(ALLOWED_FORMATS.keys())
        print("Le format de ce fichier (.", extension, ") n'est pas pris en charge, merci d'utiliser un format supporté : ", formats)
    else:
        # dest = '/media/pi/BDD_Data/Raw/' + ALLOWED_FORMATS[extension]
        directory = ALLOWED_FORMATS[extension]
        BDDconnexion.set_file(inputFile,directory)
        # ssh = BDDconnexion.ssh_connect() #Mise en place de la connexion
        # try:
        #     scp = SCPClient(ssh.get_transport())
        #     print("Transfert en cours...")
        #     scp.put(inputFile, remote_path = dest)
        #     print("...transfert terminé !")
        # except:
        #     print("SCP failed")
        # ssh.close()

def get_OBJ():
    ssh = BDDconnexion.ssh_connect() #Mise en place de la connexion
    print("Quel fichier voulez-vous récupérer ? ")
    stdin, stdout, stderr = ssh.exec_command('ls /media/pi/BDD_Data/Raw/*/')
    print(stdout.read().decode('ascii'))
    fic = str(input())
    scp = SCPClient(ssh.get_transport())
    scp.get('./', '/media/pi/BDD_Data/Raw/*/fic')
    ssh.close()

def requete():
    query = str(input("Veuillez entrer une requête SQL (SELECT...FROM...WHERE...) : "))
    res = BDDconnexion.make_query(query)
    print(res)

def quit():
    global GoOn
    GoOn = False

def menu():
    while (GoOn):
        choix = [
            ['Utiliser un fichier source (local) pour le traiter', lambda : file_to_run()],
            ['Ajouter un fichier source pour l\'enregistrer dans le base de données', lambda : add_file_to_store()],
            ['Effectuer un traitement sur un fichier existant sur la base de données', lambda : run_process()],
            ['Visualiser un maillage pré-traité', lambda : view()],
            ['Récupérer un fichier au format OBJ (post-traitement)', lambda : get_OBJ()],
            ['Faire une requête libre sur la base de données (developpeurs uniquement)', lambda : requete()],
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
    ALLOWED_FORMATS = {'las':'Lidar','laz':'LidarZip','csv':'CSV'}
    menu()
