import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=modelo user=claire")
cur = conn.cursor()

#create tables
cur.execute("DROP TABLE OBJ")
cur.execute("DROP TABLE XML")
cur.execute("DROP TABLE reference")

conn.commit()

cur.close()
conn.close()