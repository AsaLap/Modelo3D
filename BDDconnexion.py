#coding: utf-8
import psycopg2
from sshtunnel import SSHTunnelForwarder
import paramiko
from scp import SCPClient

def make_query(query):
    """
        Fonction permettant de faire des requêtes sur la base de données
        ARGS : la query de la requête SQL
        RETURN : une liste contenant les résultats de la requête
    """
    ###Connexion par tunnel SSH à la raspberry et redirection des ports en local
    try:
        ###Connexion en SSH
        tunnel = SSHTunnelForwarder(
        ('81.185.93.239', 22), #Remote server IP and SSH port
        ssh_username = "pi",
        ssh_password = "PiServer33",
        remote_bind_address=('192.168.0.20', 5432), #PostgreSQL server IP and server port on remote machine
        local_bind_address=('localhost',5432)) #Redirection on a local machine port
        tunnel.start() #start ssh sever
        print ("Server connected via SSH")
    except:
        print("SSH connection failed")

    ###Connexion à la BDD
    try:
        conn = psycopg2.connect(
            database='test',
            user='pi',
            password='PiServer33',
            host=tunnel.local_bind_host,
            port=tunnel.local_bind_port)
        curs = conn.cursor()
        print("Connected to BDD")
    except:
        print("BDD connection failed !")
        tunnel.stop()

    ###Query here !
    try:
        res = []
        print(query)
        curs.execute(query)
        res = curs.fetchall()
        conn.commit()
        curs.close()
    except:
        print("Query failed")

    # Close connections
    conn.close()
    # Stop the tunnel
    tunnel.stop()
    return res


def ssh_connect():
    """
        Fonction permettant de mettre en place une connexion SSH pour le SCP
        ARGS : none
        RETURN : la connexion SSH
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='81.185.93.239',username='pi',password='PiServer33')
        print("Connexion OK")
        return ssh
    except:
        print("SSH connection failed")
        return None


def set_file(inputFile,hostPath):
    """
        Fonction permettant de déposer un fichier sur le disque dur de la
        raspberry
        ARGS :
            inputFile : le fichier à déposer
            hostPath : le dossier dans lequel aller déposer ce fichier
        RETURN : none
    """
    ssh = ssh_connect() #Mise en place de la connexion
    try:
        scp = SCPClient(ssh.get_transport())
        print("Transfert en cours...")
        scp.put(inputFile, remote_path = hostPath)
        print("...transfert terminé !")
    except:
        print("SCP failed")
    scp.close()
    ssh.close()


def get_file(hostPath):
    """
        Fonction permettant de récupérer un fichier présent sur le disque dur
        de la raspberry
        ARGS : le/les dossier(s) dans lequel aller chercher ce fichier
        RETURN : le nom du fichier choisi
    """
    ssh = ssh_connect() #Mise en place de la connexion
    shellCom = 'ls '+ hostPath
    stdin, stdout, stderr = ssh.exec_command(shellCom) #Envoie d'une commande "ls" pour afficher le contenu des répertoires
    print(stdout.read().decode('ascii')) #Affichage du résultat de "ls"
    fic = str(input())
    hostPath += '/'+fic
    print(hostPath)
    localPath = './'
    try:
        scp = SCPClient(ssh.get_transport())
        print("Téléchargement en cours...")
        scp.get(hostPath, local_path = localPath)
        print("...téléchargement terminé !")
    except:
        print("Le téléchargement a échoué!")
    return fic
    scp.close()
    ssh.close()
