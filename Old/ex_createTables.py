import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=modelo user=claire")
cur = conn.cursor()

#create tables
cur.execute("CREATE TABLE reference (id serial PRIMARY KEY, nom varchar(10), latMin float NOT NULL, longMin float NOT NULL, latMax float NOT NULL, LongMax float NOT NULL, dataOrigin varchar(10), form varchar(5) NOT NULL)")
cur.execute("CREATE TABLE XML (id int PRIMARY KEY REFERENCES reference (id), fichier oid)")
cur.execute("CREATE TABLE OBJ (id int PRIMARY KEY REFERENCES reference (id), fichier oid)")
conn.commit()

cur.close()
conn.close()



