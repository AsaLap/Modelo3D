#Création surface inférieur socle :
delnyInf = delaunay2D(faceInf)
mappedInf = mapping(delnyInf)

#Création surfaces externes socle :
delnyExt1 = delaunay2D(faceArriere)
delnyExt1.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE) #pour que la triangulation se face dans le plan xz et pas xy
delnyExt1.Update()
delnyExt2 = delaunay2D(faceAvant)
delnyExt2.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE) #pour que la triangulation se face dans le plan xz et pas xy
delnyExt2.Update()
delnyExt3 = delaunay2D(faceGauche)
delnyExt3.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE) #pour que la triangulation se face dans le plan yz et pas xy
delnyExt3.Update()
delnyExt4 = delaunay2D(faceDroite)
delnyExt4.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE) #pour que la triangulation se face dans le plan yz et pas xy
delnyExt4.Update()

mappedExt1 = mapping1(delnyExt1)
mappedExt2 = mapping(delnyExt2)
mappedExt3 = mapping(delnyExt3)
mappedExt4 = mapping(delnyExt4)


#rendering

ren = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
ren.AddActor(mappedInf)
ren.AddActor(mappedExt1)
ren.AddActor(mappedExt2)
ren.AddActor(mappedExt3)
ren.AddActor(mappedExt4)

ren.SetBackground(1, 1, 1)
renWin.SetSize(250, 250)
cam1 = ren.GetActiveCamera()
cam1.Zoom(1.5)

iren.Initialize()
renWin.Render()
iren.Start()
