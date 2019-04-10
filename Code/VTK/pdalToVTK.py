#!/usr/bin/python

#pour transformer des fichiers en csv 
#import pdal (à installer avec anaconda/miniconda, ne marche pas avec pip)
#pdal translate -i <fichierAImporter> -o <output.csv>

from vtk import *
import csv
import time
 
points = vtkPoints()

beginning = time.time()

with open('essai.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    print ("import du fichier")
    i = 0
    j=0
    for row in spamreader:
        if (i != 0) : #pour ne pas prendre en compte le header
            #if (row[8]== '2.000') : #seulement pour les fichiers issus d'un lidar
                points.InsertNextPoint(int(float(row[0])),int(float(row[1])), int(float(row[2])))
                j=j+1
        i = i+1
print ("nombre de points importés  : ",j)
print(time.time() - beginning)
beginning = time.time()
#triangulation
profile = vtkPolyData()
profile.SetPoints(points)

delny = vtkDelaunay2D()
delny.SetInputData(profile)

mapMesh = vtkPolyDataMapper()
mapMesh.SetInputConnection(delny.GetOutputPort())
meshActor = vtkActor()
meshActor.SetMapper(mapMesh)
meshActor.GetProperty().SetColor(.1, .2, .4)
print("triangulation")
print(time.time() - beginning)
beginning = time.time()


#rendering
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

print("rendering")
print(time.time() - beginning)
beginning = time.time()

#export au format OBJ
obj = vtkOBJExporter()
obj.SetFilePrefix("essai")
obj.SetRenderWindow(renWin)
obj.Write()

print("écriture fichier")
print(time.time() - beginning)

cam1 = ren.GetActiveCamera()
cam1.Zoom(1.5)

iren.Initialize()
renWin.Render()
iren.Start()