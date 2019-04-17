#!/usr/bin/python

#pour transformer des fichiers en csv :
#import pdal (à installer avec anaconda/miniconda, ne marche pas avec pip)
#pdal translate -i <fichierAImporter> -o <output.csv>

# FICHIERS ISSUS D'UN LIDAR : utiliser importLidarCSV() et pas importCSV()

from vtk import *
import csv
import time


beginning = time.time()
start = beginning

def importCSV(filename, delimiter, modulo) :
    points = vtkPoints()
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        print ("Import du fichier")
        i = 0
        j=0
        for row in reader:
            if (i != 0 and i%modulo==0) : #pour ne pas prendre en compte le header
                    points.InsertNextPoint(int(float(row[0])),int(float(row[1])), int(float(row[2])))
                    j=j+1
            i = i+1
    print ("Nombre de points importés  : ",j)
    return points

def importLidarCSV(filename, delimiter) :
    points = vtkPoints()
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        print ("Import du fichier")
        i = 0
        j=0
        for row in reader:
            if (i != 0 and row[8]=='2000') : #row[8] est la catégorie des points, 2.000 correspond au sol
                    points.InsertNextPoint(int(float(row[0])),int(float(row[1])), int(float(row[2])))
                    j=j+1
            i = i+1
    print ("Nombre de points importés  : ",j)
    return points

#triangulation

def delaunay2D(points) :
    profile = vtkPolyData()
    profile.SetPoints(points)
    delny = vtkDelaunay2D()
    delny.SetInputData(profile)
    return delny

def mapping(delny) :
    mapMesh = vtkPolyDataMapper()
    mapMesh.SetInputConnection(delny.GetOutputPort())
    meshActor = vtkActor()
    meshActor.SetMapper(mapMesh)
    meshActor.GetProperty().SetColor(.1, .2, .4)
    return meshActor

#rendering

def rendering(meshActor) :
    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(meshActor)
    ren.SetBackground(1, 1, 1)
    renWin.SetSize(250, 250)
    renWin.Render()
    cam1 = ren.GetActiveCamera()
    cam1.Zoom(1.5)

    iren.Initialize()
    renWin.Render()
    # iren.Start()
    return renWin

#export au format OBJ
def exportOBJ(renWin) :
    obj = vtkOBJExporter()
    obj.SetFilePrefix("essai")
    obj.SetRenderWindow(renWin)
    obj.Write()

if __name__=='__main__':
    modulo = 1000000
    print("Modulo : ",modulo)
    fichier = importCSV("essai.csv",",",modulo) # a remplacer par importLidarCSV si les données sont issues d'un fichier lidar
    print ("Import : ", time.time() -beginning)
    beginning = time.time()
    delny = delaunay2D(fichier)
    print ("Triangulation de Delaunay : ", time.time() -beginning)
    beginning = time.time()
    mapped = mapping(delny)
    print ("Mapping : ", time.time() -beginning)
    beginning = time.time()
    rendered = rendering(mapped)
    print ("Rendering : ", time.time() -beginning)
    beginning = time.time()
    exportOBJ(rendered)
    print ("Ecriture obj : ", time.time() -beginning)
    beginning = time.time()
    print ("Temps total : ",time.time()-start)
