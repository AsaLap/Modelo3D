#!/usr/bin/python

from vtk import *
import csv
import time
import subprocess
import os
import re

beginning = time.time()
start = beginning

beginning = time.time()
def checkHeader(lidar, reader) :
    """
    Fonction demandant à l'utilisateur de vérifier que les champs à importer sont bien les bons
    ARGS : lidar : int indiquant si les données proviennent de la télédétection lidar ou pas (1 oui, 2 non)
           reader : objet reader du module import CSV
    RETURN : liste de int indiquant les index des champs à importer
    """
    header = next(reader)
    if (lidar == "oui") :
        importList = [0,1,2,8]
    else :
        importList = [0,1,2]
    print ("Veuillez vérifier les paramètres d'import du fichier")
    print ("En-tête : ")
    print(header)
    a = ["X :","Y :","Z :","Classification :"]
    print ("Les coordonnées utilisées seront : ")
    for i in range(0,3,1) :
        print (a[i], header[importList[i]])
    regEx = None
    while (regEx == None) :
        print ("OK ? (o/n) :")
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
        print ("OK ? (o/n) :")
        res = input()
        regEx = None
        regEx = re.search("[OoNn]", res)
        if (regEx == None) :
            print ("erreur de saisie")
    print ("Début du traitement. Veuillez patienter.")
    return importList

def importLidarCSV(filename,delimiter,modulo) :
    """
    Fonction permettant de d'importer les données d'un fichier CSV dans un objet vktPoints().
    Elle n'importe que les points correspondant à l'élévation du sol (classification = 2).
    Elle ne fonctionne que pour les fichiers issus de la télédétection Lidar.
    ARGS : filename : chaine de caracère contenant le nom du fichier
        delimiter : caractère séparant les champs du CSV
        modulo : int indiquant la résolution de la visualisation. ex : modulo = 10 -> 1 point sur 10 sera importer
    RETURN : points : objet vtkPoint contenant les coordonnées des points importés
             bounds : liste contenant [xmin,xmax,ymin, ymax,zmin,zmax]
    """
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
    print("Modulo : ",modulo)
    print ("Nombre de points importés  : ",j)
    bounds = points.GetBounds() #renvoie (xmin,xmax,ymin,ymax,zmin,zmax)
    return points, bounds

def importCSV(filename,delimiter,modulo) :
    """
    Fonction permettant d'importer les données d'un fichier CSV dans un objet vktPoints().
    Elle ne doit pas être utilisé pour les fichiers issus de la télédétection Lidar.
    ARGS : filename : chaîne de caractères contenant le nom du fichier
        delimiter : caractère séparant les champs du CSV
        modulo : int indiquant résolution de la visualisation. ex : modulo = 10 -> 1 point sur 10 sera importer
    RETURN : points : objet vtkPoint contenant les coordonnées des points importés
             bounds : liste de float contenant [xmin,xmax,ymin, ymax,zmin,zmax]
    """
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
    print("Modulo : ",modulo)
    print ("Nombre de points importés  : ",j)
    bounds = points.GetBounds() #renvoie (xmin,xmax,ymin,ymax,zmin,zmax)
    return points, bounds

def importOBJ(filename) :
    """
    Fonction permettant de d'importer les données d'un fichier OBJ dans un objet vtkPolyData.
    ARGS : filename : chaine de caractères indiquant le nom du fichier
        delimiter : caractère séparant les champs du CSV
    RETURN : points : objet vtkPolyData contenant la géométrie de l'objet (vertices,...)
             bounds : liste de float contenant [xmin,xmax,ymin, ymax,zmin,zmax]
    """
    importer = vtkOBJReader()
    importer.SetFileName(filename)
    bounds = importer.GetOutput().GetBounds()
    return importer, bounds

#triangulation
def delaunay2D(points) :
    """
    Triangule un objet vtkPoints selon la triangulation de Delaunay.
    ARGS : points : objet vtkPoint.
    RETURN : delny : objet vtkPolyData
    """
    profile = vtkPolyData()
    profile.SetPoints(points)
    delny = vtkDelaunay2D()
    delny.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE)
    delny.SetInputData(profile)
    delny.Update()
    return delny

def bordures(delny, bounds, hauteurSocle) :
    """
    Fonction permettant de créer les arêtes du socle
    ARGS : delny : objet vtkPolydata
              bounds : liste contenant [xmin,xmax,ymin, ymax,zmin,zmax]
              hauteurSocle : float contenant l'épaisseur du socle
    RETURN : points : objet vtkPoint contenant les coordonnées des points importés
             faceList : liste de vtkPoints. Chaque vtkPoint contient les coordonnées des points
             correspondant à une face du socle
    """

    #extraire les bordures du terrain
    edges = vtkFeatureEdges()
    edges.BoundaryEdgesOn()
    edges.FeatureEdgesOff()
    edges.ManifoldEdgesOff()
    edges.NonManifoldEdgesOff()
    edges.SetInputConnection(delny.GetOutputPort())
    edges.Update()
    print (edges.GetOutput())

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

def makeSocle(delny,bounds, hauteurSocle) :
    """
    Fonction permettant de trianguler les faces du socle
    ARGS : delny : objet vtkpolyData
           bounds : liste contenant [xmin,xmax,ymin, ymax,zmin,zmax]
           hauteurSocle : float contenant la l'épaisseur du socle
    RETURN : objet vtkPolyData contenant les 5 faces triangulées du socle
    """
    faceList = bordures(delny,bounds, hauteurSocle)
    socle = vtkAppendPolyData() #objet utilisé pour grouper les triangulations du socle en un seul objet
    for i in range (0,len(faceList),1) :
        delny = delaunay2D(faceList[i])
        socle.AddInputConnection(delny.GetOutputPort())
    return socle

def mapping(delny) :
    """
    Fonction permettant de faire le mapping d'un objet vtkPolyData
    ARGS : vtkPolyData
    RETURN : vtkActor
    """
    mapMesh = vtkPolyDataMapper()
    mapMesh.SetInputConnection(delny.GetOutputPort())
    meshActor = vtkActor()
    meshActor.SetMapper(mapMesh)
    meshActor.GetProperty().SetColor(.1, .2, .4)
    return meshActor

#rendering
def rendering(mapped) :
    """
    Fonction permettant de visualiser une liste de vtkActor
    ARGS : mapped : liste de vtkActor
    RETURN : renWin : fenêtre de visualisation vtkRenderWindow
    """
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

def exportOBJ(renWin, filename) :
    """
    Fonction permettant d'exporter au format Wavefront OBJ une fenêtre de visualisation
    ARGS : renWin : vtkRenderWindow
           filename : chaîne de caractères contenant le nom du fichier obj
    RETURN : None
    """
    obj = vtkOBJExporter()
    obj.SetFilePrefix(filename)
    obj.SetRenderWindow(renWin)
    obj.Write()

def pipeline_VTK(fic,lidar,socleChoix=2,modulo=1):
    """
    Fonction permettant de faire l'ensemble du traitement.
    ARGS :  fic : chaîne de caractère contenant le nom du fichier
            lidar : int indiquant si le fichier est isssu de la télédétection lidar
            socleChoix : int indiquant si le socle doit être créer ou pas
            modulo : int indiquant la résolution à prendre en compte
    RETURN : bounds : liste contenant [xmin,xmax,ymin, ymax,zmin,zmax]
    """
    beginning = time.time()
    start = beginning
    if (lidar) :
        fichier, bounds = importLidarCSV(fic,",",modulo)
    elif (fic[-3:] == "obj"):
        fichier, bounds = importOBJ(fic)
    else :
        fichier, bounds = importCSV(fic,",",modulo)
    print ("Import : ", time.time() -beginning)
    beginning = time.time()
    mapped = []
    if (fic[-3:] != 'obj'):
        delny = delaunay2D(fichier)
        print ("Triangulation de Delaunay : ", time.time() -beginning)
        beginning = time.time()
        mapped.append(mapping(delny))
        print ("Mapping : ", time.time() -beginning)
        beginning = time.time()
        if (socleChoix == 1) : #faire le socle si l'utilisateur l'a demandé
            print ("Par défaut, l'épaisseur du socle correspond à la moitié de la hauteur du terrain")
            regEx = None
            print ("Voulez-vous changer l'épaisseur? o/n")
            while (regEx == None) :
                choix = input()
                choix = choix.lower()
                regEx = re.search("[on]", choix)
                if (regEx == None) :
                    print ("erreur de saisie. Recommencez")
            if choix == 'o' :
                print ("Entrez la valeur choisie")
                hauteurSocle = input()
                a = 0
                while a == 0 :
                    a = 1
                    try :
                        hauteurSocle = float(hauteurSocle)
                        print (hauteurSocle)
                    except :
                        print ('erreur de saisie. Recommencez.')
                        a = 0
            if choix == 'n' :
                zmin = bounds[4]
                zmax = bounds[5]
                hauteurSocle = zmin -((zmax-zmin)/2)  
            socle = makeSocle(delny,bounds, hauteurSocle)
            mapped.append(mapping(socle))
            print ("Socle : ", time.time()- beginning)
            beginning = time.time()
    else:
        mapped.append(mapping(fichier))
    rendered = rendering(mapped)
    print ("Rendering : ", time.time() -beginning)
    beginning = time.time()
    exportOBJ(rendered, fic[-1:])
    print ("Ecriture obj : ", time.time() -beginning)
    print ("Temps total : ",time.time()-start)
    return bounds
