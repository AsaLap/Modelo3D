from vtk import *
import csv
import time

beginning = time.time()
def importLidarCSV(filename, delimiter) :
    points = vtkPoints()
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        print ("Import du fichier")
        i = 0
        j=0
        for row in reader:
            if (i != 0 and row[8]=='2.000') : #row[8] est la catégorie des points, 2.000 correspond au sol
                points.InsertNextPoint(float(row[0]),float(row[1]),float(row[2]))
                j=j+1
            i = i+1
    print ("Nombre de points importés  : ",j)
    bounds = points.GetBounds() #renvoie (xmin,xmax,ymin,ymax,zmin,zmax)
    return points, bounds

def importCSV(filename, delimiter) :
    points = vtkPoints()
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        print ("Import du fichier")
        i = 0
        j=0
        for row in reader:
            if (i != 0 and i%10000 == 0) : 
                points.InsertNextPoint(float(row[0]),float(row[1]), float(row[2]))
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
    ren.AddActor(mapped)
    ren.SetBackground(1, 1, 1)
    renWin.SetSize(250, 250)
    renWin.Render()
    cam1 = ren.GetActiveCamera()
    cam1.Zoom(1.5)

    iren.Initialize()
    renWin.Render()
    iren.Start()
    return renWin

def renderingSocle(mappedterrain,mappedSocle) :
    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    ren.AddActor(mappedterrain)
    ren.AddActor(mappedSocle)
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

modulo = 10000
filename = "tiff.csv"
socle = "oui"
print("Modulo : ",modulo)
terrain, bounds = importCSV(filename,",") # a remplacer par importLidarCSV si les données sont issues d'un fichier lidar
print ("Import : ", time.time() - beginning)
beginning = time.time()
delny = delaunay2D(terrain)
mappedterrain = mapping(delny)
print ("création terrain : ", time.time() - beginning)
beginning = time.time()
if (socle == "oui") :
    faceList = bordures(delny,bounds)
    socle = vtkAppendPolyData() #objet utilisé pour grouper les triangulations du socle en un seul objet
    for i in range (0,len(faceList)-1,1) :
        delny = delaunay2D(faceList[i])
        socle.AddInputConnection(delny.GetOutputPort())
    mappedSocle = mapping(socle)
    print ("triangulation + mappingSocle : ", time.time()- beginning)
    beginning = time.time()
    rendered = renderingSocle(mappedterrain,mappedSocle)
else :
    rendered = rendering(mappedterrain)
print ("rendering : ", time.time()- beginning)
beginning = time.time()
