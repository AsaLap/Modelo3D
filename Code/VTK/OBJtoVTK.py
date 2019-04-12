from vtk import *
import time
beginning = time.time()


importer = vtkOBJReader()
importer.SetFileName("essai.obj")

mapMesh = vtkPolyDataMapper()
mapMesh.SetInputConnection(importer.GetOutputPort())
meshActor = vtkActor()
meshActor.SetMapper(mapMesh)
meshActor.GetProperty().SetColor(.1, .2, .4)



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

cam1 = ren.GetActiveCamera()
cam1.Zoom(1.5)

iren.Initialize()
renWin.Render()
iren.Start()