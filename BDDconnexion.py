#coding: utf-8
import psycopg2
from sshtunnel import SSHTunnelForwarder
import paramiko
from scp import SCPClient

def ssh_Tunnel(IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD):
    """
        Fonction permettant de mettre en place un tunnel SSH afin de rediriger
        les ports locaux et distants pour faire des requêtes sur la base de
        données
        ARGS : None
        RETURN : Le tunnel
    """
    ###Connexion par tunnel SSH à la raspberry et redirection des ports en local
    try:
        ###Connexion en SSH
        tunnel = SSHTunnelForwarder(
        (IP_PUBLIQUE, PORT_SSH), #Remote server IP and SSH port
        ssh_username = USER,
        ssh_password = PASSWORD,
        remote_bind_address=(IP_LOCALE,PORT_POSTGRES), #PostgreSQL server IP and server port on remote machine
        local_bind_address=('localhost',PORT_POSTGRES)) #Redirection on a local machine port
        tunnel.start() #start ssh sever
        print ("Server connected via SSH")
        return tunnel
    except:
        print("SSH connection failed")
        tunnel.stop()
        return None

def make_query(query,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE):
    """
        Fonction permettant de faire des requêtes sur la base de données
        ARGS : la query de la requête SQL
        RETURN : une liste contenant les résultats de la requête
    """
    tunnel = ssh_Tunnel(IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD)
    try:
        conn = psycopg2.connect(
            database=DATABASE,
            user=BDD_USER,
            password=BDD_PASSWORD,
            host=tunnel.local_bind_host,
            port=tunnel.local_bind_port)
        curs = conn.cursor()
        print("Connected to BDD")
    except:
        print("BDD connection failed !")
        tunnel.stop()
    ###Query here !
    try:
        print("Requête en cours...")
        res = []
        print(query)
        curs.execute(query)
        res = curs.fetchall()
        conn.commit()
        curs.close()
        print("...requête terminée!")
    except:
        print("Query failed")
    finally:
        conn.close()
        tunnel.stop()
    return res


def ssh_connect(IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD):
    """
        Fonction permettant de mettre en place une connexion SSH pour le SCP
        ARGS : none
        RETURN : la connexion SSH
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=IP_PUBLIQUE,username=USER,password=PASSWORD)
        print("Connexion OK")
        return ssh
    except:
        print("SSH connection failed")
        return None


def set_file(inputFile,entries,hostPath,IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD,PORT_SSH,PORT_POSTGRES,BDD_USER,BDD_PASSWORD,DATABASE):
    """
        Fonction permettant de déposer un fichier sur le disque dur de la
        raspberry et d'ajouter son entrée dans la base de données.
        ARGS :
            inputFile : le fichier à déposer
            hostPath : le dossier dans lequel aller déposer ce fichier
            IP_PUBLIQUE : l'IP publique de la raspberry
            Autres : leur nom = leur utilité
        RETURN : None
    """
    ssh = ssh_connect(IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD) #Mise en place de la connexion
    ajout_bdd = False
    try:
        scp = SCPClient(ssh.get_transport())
        print("Transfert en cours...")
        scp.put(inputFile, remote_path = hostPath)
        print("...transfert terminé !")
        ajout_bdd = True
    except:
        print("SCP failed")
    finally:
        scp.close()
        ssh.close()
    if (ajout_bdd):
        try:
            print("Ajout à la base de données...")
            splitedFile = inputFile.split("/")
            file = splitedFile[-1] #Récupération du nom de fichier uniquement
            if (file[-3:]=="csv"):
                query = "INSERT INTO csv(nom,ex_lidar,planete,commentaires) VALUES ('"+file+"',"+entries[0]+",'"+entries[1]+"','"+entries[2]+"') RETURNING id;"
                make_query(query,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE)
            elif (file[-3:]=="obj"):
                query = "INSERT INTO obj(id,nom) VALUES ("+entries[0]+",'"+file+"');"
                make_query(query,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE)
            else:
                print("Le garbage n'est pas ajouté à la BDD")
        except:
            print("Ajout à la base données échoué")


#TODO : changer la fonction pour utiliser la BDD plutot qu'un 'ls' pour afficher les fichiers dispos
def get_file(hostPath,localPath,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE):
    """
        Fonction permettant de récupérer un fichier présent sur le disque dur
        de la raspberry et ses informations contenues dans la base de données.
        ARGS :
            hostPath : le chemin d'accès aux fichiers sur la raspberry
            localPath : le chemin local où télécharger ces fichiers
            IP_PUBLIQUE : l'IP publique de la raspberry
            Autres : leur nom = leur utilité
        RETURN : le nom du fichier choisi
    """
    # ssh = ssh_connect(IP_PUBLIQUE,IP_LOCALE,USER,PASSWORD) #Mise en place de la connexion
    # shellCom = 'ls '+ hostPath
    # stdin, stdout, stderr = ssh.exec_command(shellCom) #Envoie d'une commande "ls" pour afficher le contenu des répertoires
    # print("\nListe des fichiers "+hostPath[-3:]+" sur la BDD :")
    # print(stdout.read().decode('ascii')) #Affichage du résultat de "ls"
    # fic = str(input("Quel fichier voulez-vous récupérer ? (Il sera téléchargé dans le répertoire courant) : "))
    # hostPath += '/'+fic
    # print(hostPath)
    query = "SELECT id, nom, date_ajout FROM "+hostPath[-3:]+";"
    res = make_query(query,IP_PUBLIQUE,IP_LOCALE,PORT_SSH,PORT_POSTGRES,USER,PASSWORD,BDD_USER,BDD_PASSWORD,DATABASE)
    print(res)
    try:
        scp = SCPClient(ssh.get_transport())
        print("Téléchargement en cours...")
        scp.get(hostPath, local_path = localPath)
        print("...téléchargement terminé !")
    except:
        print("Le téléchargement a échoué!")
    finally:
        scp.close()
        ssh.close()
    return fic,lidar,id
