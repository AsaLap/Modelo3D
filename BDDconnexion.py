#coding: utf-8
import psycopg2
from sshtunnel import SSHTunnelForwarder
import paramiko
from scp import SCPClient

def make_query():
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
        curs.execute(query)
        res = curs.fetchall()
        conn.commit()
        curs.close()
        return res
    except:
        print("Query failed")

    # Close connections
    conn.close()
    # Stop the tunnel
    tunnel.stop()

def ssh_connect():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='81.185.93.239',username='pi',password='PiServer33')
        print("Connexion OK")
        return ssh
    except:
        print("SSH connection failed")

def set_file(inputFile,directory):
    dest = '/media/pi/BDD_Data/Raw/' + directory
    ssh = ssh_connect() #Mise en place de la connexion
    try:
        scp = SCPClient(ssh.get_transport())
        print("Transfert en cours...")
        scp.put(inputFile, remote_path = dest)
        print("...transfert terminé !")
    except:
        print("SCP failed")
    ssh.close()

def get_file():
    ssh = ssh_connect() #Mise en place de la connexion
    stdin, stdout, stderr = ssh.exec_command('ls /media/pi/BDD_Data/Raw/')
    for line in stdout.read().splitlines():
        print(line)
    ssh.close()
