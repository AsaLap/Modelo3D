from vtk import *
import csv


############################Ajout dans la liste####################
def getzMin(filename, delimiter,modulo) :
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        k=0
        for row in reader:
            if (k !=0 and row[8]=='2.000' and k%modulo==0) :
                zMinlist.append(int(float(row[2])))
            k=k+1
        zMin=min(zMinlist)
        print (zMin)
        return zMin



def importLidarCSV(filename, delimiter,modulo, zMin):
    pointsfirst = vtkPoints()
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        print ("Import du fichier")
        i = 0
        j=0
        for row in reader:
            if (i != 0 and row[8]=='2.000' and i%modulo==0) : #row[8] est la catégorie des points, 2.000 correspond au sol
                heigth=int(float(row[2]))-zMin
                #pointsfirst.InsertNextPoint(int(float(row[0])),int(float(row[1])),int(float(row[2])))
                point = []
                point.append(int(float(row[0])))
                point.append(int(float(row[1])))
                point.append(heigth)
                pointstri.append(point)
                j=j+1
            i = i+1
    print ("Nombre de points importés  : ",j)
    return pointsfirst

############################Récupération des bordures et des coins(coin)######################################

def getCorner (pointstri, xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx):
    for point in pointstri :
        if point[0] <xMin :
            xMin = point[0]
        if point[0] > xMax :
            xMax = point[0]
        if point[1] <yMin :
            yMin = point[1]
        if point[1] > yMax :
            yMax = point[1]
    for point in pointstri:
        if point[0] == xMax:
            xMaxlist.append(point[1])
        if point[0]== xMin:
            xMinlist.append(point[1])
        if point[1] == yMax:
            yMaxlist.append(point[0])
        if point[1] == yMin:
            yMinlist.append(point[0])

    xMaxy=max(xMaxlist)
    xMiny=min(xMinlist)
    yMaxx=min(yMaxlist)
    yMinx=max(yMinlist)
    print(xMax, xMaxy)
    print(yMax,yMaxx)
    print(xMin,xMiny)
    print(yMin,yMinx)


    return (xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx)



def getBorder(pointstri, xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx):
    points = vtkPoints()
    for point in pointstri :
        if point[0] >= xMin and point[0]<= yMinx:
            if point[1]>=yMin and point[1]<=xMiny:
                bordinit.append(point)
        if point[0] >= yMinx and point[0] <= xMax:
            if point[1]>=yMin and point[1]<= xMaxy:
                bordinit.append(point)
        if point[0] <= xMax and point [0] >= yMaxx:
            if point[1]<= yMax and point[1] >= xMaxy:
                bordinit.append(point)
        if point[0]<= yMaxx and point[0]>= xMin:
            if point[1]<= yMax and point[1]>= xMiny:
                bordinit.append(point)
    for point in bordinit:
        points.InsertNextPoint(point)
    print(len(bordinit))
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
    iren.Start()
    return renWin

#export au format OBJ
def exportOBJ(renWin) :
    obj = vtkOBJExporter()
    obj.SetFilePrefix("essai")
    obj.SetRenderWindow(renWin)
    obj.Write()



if __name__=='__main__':
    i= 0
    j=2
    k=-12
    heigth=0

    pointstri = []
    zMinlist=[]
    xMaxlist=[]
    xMinlist=[]
    yMaxlist=[]
    yMinlist=[]

    bordinit=[]
    bord1 = []
    bord2 = []
    bord3 = []
    bord4 = []
    bord1down=[]
    bord2down=[]
    bord3down=[]
    bord4down=[]


    zMin = 1000000000
    xMin = 1000000000
    yMin = 1000000000
    xMax = -1000000000
    yMax = -1000000000
    yMinx=0
    yMaxx=0
    xMiny=0
    xMaxy=0

    modulo = 2000
    print("Modulo : ",modulo)
    zMin = getzMin("essai.csv",",",modulo)
    fichier = importLidarCSV("essai.csv",",",modulo, zMin)
    xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx = getCorner(pointstri, xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx)
    getBorder(pointstri, xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx)
    delny = delaunay2D(fichier)
    print ("Triangulation de Delaunay")
    mapped = mapping(delny)
    print ("Mapping")
    rendered = rendering(mapped)
