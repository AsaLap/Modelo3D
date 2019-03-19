import vtk

lect = vtk.vtkBYUReader()
lect.SetGeometryFileName("cow.g")
lect.csv_Update()

donnees=lect.GetOutput()
print "donnees : ",donnees

print "nb de points = ",donnees.GetNumberOfPoints()
pt=donnees.GetPoint(2000)
print "point numero 2000 : ",pt

print "nb de cellules = ",donnees.GetNumberOfCells()
ce=donnees.GetCell(200)
print "cellule numero 200 : ",ce

bornes=donnees.GetBounds()
print "Bornes : ",bornes


mappeur=vtk.vtkPolyDataMapper()
mappeur.SetInputConnection(lect.GetOutputPort())

acteur=vtk.vtkActor()
acteur.SetMapper(mappeur)

ren=vtk.vtkRenderer()
ren.AddActor(acteur)

renWin=vtk.vtkRenderWindow()
renWin.AddRenderer(ren)

iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

iren.Initialize()
renWin.Render()

iren.Start()
