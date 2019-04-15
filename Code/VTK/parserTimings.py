with open("timings2.txt",'r') as fichier:
    raw = fichier.read()
raw = raw.replace("Modulo :  ","")
raw = raw.replace("Import du fichier\nNombre de points importés  :  ","")
raw = raw.replace("Import :  ","")
raw = raw.replace("Triangulation de Delaunay :  ","")
raw = raw.replace("Mapping :  ","")
raw = raw.replace("Rendering :  ","")
raw = raw.replace("Ecriture obj :  ","")
raw = raw.replace("Temps total :  ","")
raw = raw.split("\n\n")
for i in range(len(raw)):
    raw[i] = raw[i].replace("\n",",")
print(raw)
out = open("timings2.csv",'w')
out.write("Modulo,Nombre de points,Temps d'importation,Triangulation,Mapping,Rendering,Ecriture OBJ,Temps Total\n")
for i in raw:
    out.write(i)
    out.write("\n")
