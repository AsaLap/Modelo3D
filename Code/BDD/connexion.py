#coding: utf-8
import psycopg2
from sshtunnel import SSHTunnelForwarder
import sys

###Connexion par tunnel SSH à la BDD
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

try:
    ###Connexion à la BDD
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

###Query ici !
try:
    query = "INSERT ..."
    curs.execute(query)
    conn.commit()
    curs.close()
except:
    print("Query failed")


# Close connections
conn.close()

# Stop the tunnel
tunnel.stop()
