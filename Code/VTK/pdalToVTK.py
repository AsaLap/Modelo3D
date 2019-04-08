#!/usr/bin/python

from vtk import *
import csv

points = vtkPoints()


with open('petitEssai.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    i = 0
    for row in spamreader:
        if (row[8]== '2.000') :
            points.InsertNextPoint(i,int(float(row[0])),int(float(row[1])))
            i = i+1
print (i)

profile = vtkPolyData()
profile.SetPoints(points)

delny = vtkDelaunay3D()
delny.SetInputData(profile)
delny.SetTolerance(0.01)
delny.SetAlpha(0.2)
delny.BoundingTriangulationOff()

# Shrink the result to help see it better.
shrink = vtkShrinkFilter()
shrink.SetInputConnection(delny.GetOutputPort())
shrink.SetShrinkFactor(0.9)

map = vtkDataSetMapper()
map.SetInputConnection(shrink.GetOutputPort())

triangulation = vtkActor()
triangulation.SetMapper(map)
triangulation.GetProperty().SetColor(1, 0, 0)

# Create graphics stuff
ren = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
ren.AddActor(triangulation)
ren.SetBackground(1, 1, 1)
renWin.SetSize(250, 250)
renWin.Render()

cam1 = ren.GetActiveCamera()
cam1.Zoom(1.5)

iren.Initialize()
renWin.Render()
iren.Start()