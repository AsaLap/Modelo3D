import psycopg2

# Connect to an existing database
conn = psycopg2.connect("dbname=modelo user=claire")
cur = conn.cursor()

cur.execute("INSERT INTO reference (nom, latmin, longmin, latmax,longmax,dataOrigin, form) VALUES ('essai', 12, 12,12,12,'USGS','XML')")
conn.commit()

cur.close()
conn.close()