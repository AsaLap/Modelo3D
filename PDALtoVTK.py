#!/usr/bin/python

#pour transformer des fichiers en csv :
#import pdal (à installer avec anaconda/miniconda, ne marche pas avec pip)
#pdal translate -i <fichierAImporter> -o <output.csv>

# FICHIERS ISSUS D'UN LIDAR : utiliser importLidarCSV() et pas importCSV()

from vtk import *
import csv
import time
import subprocess
import os

from vtk import *
import csv
import time
import re
import subprocess
import os

beginning = time.time()
start = beginning

def initFile():
    file = input("Entrez le nom du fichier (sans l'extension): ")
    format= input("L'extension du fichier ? : ")
    finput=file+'.'+format
    if format=='csv':
        print("Vous utilisez importCSV")
        fichier,bounds = importCSV(finput,",",modulo)
    else:
        fileoutput=input("Quel nom voulez vous donnez a votre fichier en sortie: ")
        output=fileoutput+'.csv'
        print("Début de la conversion du fichier")
        subprocess.call(["pdal","translate","-i",finput,"-o",output])
        print("Fin de la conversion du fichier")
        print ("les gros fichiers peuvent être long a traiter. Indiquez une résolution")
        modulo = input()
        if format=='laz' or format=='las':
            print("Données lidar, seuls les points classifiés \"2\" (sol) seront utilisés)")
            fichier, bounds = importLidarCSV(output,",", modulo)
        else :
            fichier, bounds = importCSV(output,",", modulo)
    return fichier, bounds

beginning = time.time()
def checkHeader(lidar, reader) :
    header = next(reader)
    if (lidar == "oui") :
        importList = [0,1,2,8]
    else :
        importList = [0,1,2]
    print ("Veuillez vérifier les paramètres d'import du fichier")
    print ("en-tête du fichier")
    print(header)
    a = ["X :","Y :","Z :","Classification :"]
    print ("les coordonnées utilisées seront : ")
    for i in range(0,3,1) :
        print (a[i], header[importList[i]])
    regEx = None
    while (regEx == None) :
        print ("OK ? o/n")
        res = input()
        regEx = re.search("[OoNn]", res)
        if (regEx == None) :
            print ("erreur de saisie")
        else :
            res = res.lower()
    while (res == "n") :
        res = "o"
        regEx = None
        while (regEx == None) :
            print ("Entrez le numéro du champs à remplacer ?")
            for i in importList :
                print (i, header[i])
            res = input()
            regEx = re.search("[0-3]",res)
            if (regEx == None) :
                print ("erreur de saisie")
        regEx = None
        while (regEx == None) :
            print ("Entrer le numéro du champs dans le header (0 à",len(header),")")
            resChamps = input()
            regEx = re.search("[0-9]",resChamps)
            if (regEx == None ) :
                print ("erreur de saisie")
                continue
            resChamps = int(resChamps) #nécessaire pour la comparaison ligne suivante
            if (resChamps >= len(header)) :
                regEx == None
                print ("erreur de saisie")
        res = int(res)
        resChamps = int(resChamps)
        importList[res] = header[resChamps]
        for i in importList :
            print (a[i]," : ", header[importList[i]])
        print ("OK ? o/n")
        res = input()
        regEx = None
        regEx = re.search("[OoNn]", res)
        if (regEx == None) :
            print ("erreur de saisie")
    print ("début du traitement. Veuillez patienter.")
    return importList

def importLidarCSV(filename, delimiter, modulo = 0) :
    points = vtkPoints()
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        i = 0
        j = 0
        importList = checkHeader("oui",reader)
        for row in reader:
            if (row[importList[3]]=='2.000' and i%modulo == 0) : #row[importList[3]] est la catégorie des points, 2.000 correspond au sol
                points.InsertNextPoint(float(row[importList[0]]),float(row[importList[1]]),float(row[importList[2]]))
                j=j+1
            i = i+1
    print ("Nombre de points importés  : ",j)
    bounds = points.GetBounds() #renvoie (xmin,xmax,ymin,ymax,zmin,zmax)
    return points, bounds

def importCSV(filename, delimiter,modulo) :
    points = vtkPoints()
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        importList = checkHeader("non", reader)
        i = 0
        j = 0
        for row in reader:
            if (i != 0 and i%modulo == 0) :
                points.InsertNextPoint(float(row[importList[0]]),float(row[importList[1]]),float(row[importList[2]]))
                j=j+1
            i = i+1
    print ("Nombre de points importés  : ",j)
    bounds = points.GetBounds() #renvoie (xmin,xmax,ymin,ymax,zmin,zmax)
    return points, bounds

#triangulation
def delaunay2D(points) :
    profile = vtkPolyData()
    profile.SetPoints(points)
    delny = vtkDelaunay2D()
    delny.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE)
    delny.SetInputData(profile)
    delny.Update()
    return delny

#ExtractEdges
def bordures(delny, bounds) :
#bounds renvoie (xmin,xmax,ymin,ymax,zmin,zmax)
    zmin = bounds[4]
    zmax = bounds[5]
    hauteurSocle = zmin -((zmax-zmin)/2)
    #extraire les bordures du terrain
    edges = vtkFeatureEdges()
    edges.BoundaryEdgesOn()
    edges.FeatureEdgesOff()
    edges.ManifoldEdgesOff()
    edges.NonManifoldEdgesOff()
    edges.SetInputConnection(delny.GetOutputPort())
    edges.Update()

    #Séparer les bordures en 4 cotés pour faire les faces.
    #On récupère les points qui sont dans des cylindres centrés sur le milieu de chaque coté

    #trouver les centres des cylindres
    xcenter = bounds[0] + (bounds[1]-bounds[0])/2
    ycenter = bounds[2] + (bounds[3]-bounds[2])/2
    center1 = [xcenter,bounds[2],0]
    center2 = [bounds[1],ycenter,0]
    center3 = [xcenter,bounds[3],0]
    center4 = [bounds[0],ycenter,0]

    #créer les cylindres (les vtkcylinder ont une hauteur infinie)
    cylinderList = []
    cylinder1 = vtkCylinder()
    cylinder1.SetCenter(center1)
    cylinder1.SetRadius((bounds[1]-bounds[0])/2)
    cylinder1.SetAxis(0,0,1)
    cylinderList.append(cylinder1)
    cylinder2 = vtkCylinder()
    cylinder2.SetCenter(center2)
    cylinder2.SetRadius((bounds[3]-bounds[2])/2)
    cylinder2.SetAxis(0,0,1)
    cylinderList.append(cylinder2)
    cylinder3 = vtkCylinder()
    cylinder3.SetCenter(center3)
    cylinder3.SetRadius((bounds[1]-bounds[0])/2)
    cylinder3.SetAxis(0,0,1)
    cylinderList.append(cylinder3)
    cylinder4 = vtkCylinder()
    cylinder4.SetCenter(center4)
    cylinder4.SetRadius((bounds[3]-bounds[2])/2)
    cylinder4.SetAxis(0,0,1)
    cylinderList.append(cylinder4)

    #faceList = liste contenant une liste vtkPoint de point par face du socle
    #faceList[0] = liste de points de la face inférieur du socle
    #faceList[1] à faceList[4] = liste de points pour chaque face verticale du socle
    faceList = []
    for i in range(0,4,1) :
        tmp = vtkPoints()
        faceList.append(tmp)

    for i in range (0,len(cylinderList),1) :
        bord = vtkExtractGeometry() #extrait les points contenus dans le cylindre
        bord.SetInputConnection(edges.GetOutputPort())
        bord.SetImplicitFunction(cylinderList[i])
        bord.ExtractBoundaryCellsOn()
        bord.Update()
        pointarray = bord.GetOutput().GetPoints() #accède aux points
        for j in range(0,pointarray.GetNumberOfPoints(),1) :
            tmp = pointarray.GetPoint(j)
            faceList[0].InsertNextPoint(tmp[0],tmp[1],hauteurSocle)
            faceList[i].InsertNextPoint(tmp[0],tmp[1],hauteurSocle)
            faceList[i].InsertNextPoint(tmp[0],tmp[1],tmp[2])
    return faceList

def makeSocle(delny,bounds) :
    faceList = bordures(delny,bounds)
    socle = vtkAppendPolyData() #objet utilisé pour grouper les triangulations du socle en un seul objet
    for i in range (0,len(faceList),1) :
        delny = delaunay2D(faceList[i])
        socle.AddInputConnection(delny.GetOutputPort())
    return socle

def mapping(delny) :
    mapMesh = vtkPolyDataMapper()
    mapMesh.SetInputConnection(delny.GetOutputPort())
    meshActor = vtkActor()
    meshActor.SetMapper(mapMesh)
    meshActor.GetProperty().SetColor(.1, .2, .4)
    return meshActor

#rendering
def rendering(mapped) :
    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    for i in mapped :
        ren.AddActor(i)
    ren.SetBackground(1, 1, 1)
    renWin.SetSize(250, 250)
    renWin.Render()
    cam1 = ren.GetActiveCamera()
    cam1.Zoom(1.5)
    iren.Initialize()
    renWin.Render()
    iren.Start()
    return renWin

#export au format OBJ
def exportOBJ(renWin) :
    obj = vtkOBJExporter()
    obj.SetFilePrefix("essai")
    obj.SetRenderWindow(renWin)
    obj.Write()

#La même chose que dans le main de ce fichier mais utilisable ailleurs car dans une fonction avec arguments
def pipeline_VTK(fic,lidar=False,modulo=1,socleChoix="non"):
    beginning = time.time()
    start = beginning
    print("Modulo : ",modulo)
    if (lidar) :
        fichier, bounds = importLidarCSV(fic,",",modulo)
    else :
        fichier, bounds = importCSV(fic,",",modulo)
    print ("Import : ", time.time() -beginning)
    beginning = time.time()
    delny = delaunay2D(fichier)
    print ("Triangulation de Delaunay : ", time.time() -beginning)
    beginning = time.time()
    mapped = []
    mapped.append(mapping(delny))
    print ("Mapping : ", time.time() -beginning)
    beginning = time.time()
    if (socleChoix == "oui") : #faire le socle si l'utilisateur l'a demandé
        socle = makeSocle(delny,bounds)
        mapped.append(mapping(socle))
        print ("triangulation + mappingSocle : ", time.time()- beginning)
        beginning = time.time()
    rendered = rendering(mapped)
    print ("Rendering : ", time.time() -beginning)
    beginning = time.time()
    exportOBJ(rendered)
    print ("Ecriture obj : ", time.time() -beginning)
    print ("Temps total : ",time.time()-start)

if __name__=='__main__':
    modulo = 1000
    print("Modulo : ",modulo)
    fichier, bounds = initFile() #bounds = liste contenant les min/max sur chaque axe
    socleChoix = "oui" #choisir si on veut dessiner le socle
    lidar = "non" #choisir entre importCSV et importLidarCSV
    print ("Import : ", time.time() -beginning)
    beginning = time.time()
    delny = delaunay2D(fichier)
    print ("Triangulation de Delaunay : ", time.time() -beginning)
    beginning = time.time()
    mapped = []
    mapped.append(mapping(delny))
    print ("Mapping : ", time.time() -beginning)
    beginning = time.time()
    if (socleChoix == "oui") : #faire le socle si l'utilisateur l'a demandé
        socle = makeSocle(delny,bounds)
        mapped.append(mapping(socle))
        print ("triangulation + mappingSocle : ", time.time()- beginning)
        beginning = time.time()
    rendered = rendering(mapped)
    print ("Rendering : ", time.time() -beginning)
    beginning = time.time()
    exportOBJ(rendered)
    print ("Ecriture obj : ", time.time() -beginning)
    beginning = time.time()
print ("Temps total : ",time.time()-start)
