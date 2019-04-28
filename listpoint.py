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
    return pointstri

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
    print("xMax : ",xMax,"xMaxy : ",xMaxy)
    print("yMax : ",yMax,"yMaxx : ",yMaxx)
    print("xMin : ",xMin,"xMiny : ",xMiny)
    print("yMin : ",yMin,"yMinx : ",yMinx)
    return (xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx)



def getBorder(pointstri, xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx):
    bord1 = vtkPoints()
    bord2 = vtkPoints()
    bord3 = vtkPoints()
    bord4 = vtkPoints()
    bordDown = vtkPoints()
    bord1py=[]
    bord1down=[]
    for point in pointstri :
        pointtmp=point.copy()
        pointtmp[2]=0
        print(point,pointtmp)
        if point[0] >= xMin and point[0]<= yMinx:
            if point[1]>=yMin and point[1]<=xMiny:
                bord1.InsertNextPoint(point)
                bord1.InsertNextPoint(pointtmp)
                bordDown.InsertNextPoint(pointtmp)
                bord1py.append(point)
                bord1down.append(pointtmp)
        if point[0] >= yMinx and point[0] <= xMax:
            if point[1]>=yMin and point[1]<= xMaxy:
                bord2.InsertNextPoint(point)
                bord2.InsertNextPoint(pointtmp)
                bordDown.InsertNextPoint(pointtmp)
        if point[0] <= xMax and point [0] >= yMaxx:
            if point[1]<= yMax and point[1] >= xMaxy:
                bord3.InsertNextPoint(point)
                bord3.InsertNextPoint(pointtmp)
                bordDown.InsertNextPoint(pointtmp)
        if point[0]<= yMaxx and point[0]>= xMin:
            if point[1]<= yMax and point[1]>= xMiny:
                bord4.InsertNextPoint(point)
                bord4.InsertNextPoint(pointtmp)
                bordDown.InsertNextPoint(pointtmp)
    print(bord1.GetNumberOfPoints())
    print(bord1py)
    print(bord1down[0],bord1down[1])
    return bordDown,bord1,bord2,bord3,bord4

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

#socle
def socle(bordDown,bord1,bord2,bord3,bord4) :
    delnyInf = delaunay2D(bordDown)
    mappedInf = mapping(delnyInf)

    #Création surfaces externes socle :
    delnyExt1 = delaunay2D(bord1)
    delnyExt1.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE) #pour que la triangulation se face dans le plan xz et pas xy
    delnyExt1.Update()
    delnyExt2 = delaunay2D(bord2)
    delnyExt2.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE) #pour que la triangulation se face dans le plan xz et pas xy
    delnyExt2.Update()
    delnyExt3 = delaunay2D(bord3)
    delnyExt3.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE) #pour que la triangulation se face dans le plan yz et pas xy
    delnyExt3.Update()
    delnyExt4 = delaunay2D(bord4)
    delnyExt4.SetProjectionPlaneMode(VTK_BEST_FITTING_PLANE) #pour que la triangulation se face dans le plan yz et pas xy
    delnyExt4.Update()

    mappedExt1 = mapping(delnyExt1)
    mappedExt2 = mapping(delnyExt2)
    mappedExt3 = mapping(delnyExt3)
    mappedExt4 = mapping(delnyExt4)

    return mappedExt1, mappedExt2, mappedExt3, mappedExt4, mappedInf

#rendering utiliser
def renderingSocle(mappedExt1, mappedExt2, mappedExt3,mappedExt4, mappedInf):
    ren = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(mappedInf)
    # ren.AddActor(mappedExt1)
    # ren.AddActor(mappedExt2)
    # ren.AddActor(mappedExt3)
    # ren.AddActor(mappedExt4)

    ren.SetBackground(1, 1, 1)
    renWin.SetSize(250, 250)
    cam1 = ren.GetActiveCamera()
    cam1.Zoom(1.5)

    iren.Initialize()
    renWin.Render()
    iren.Start()
    return renWin
#rendering

# def rendering(meshActor) :
#     ren = vtkRenderer()
#     renWin = vtkRenderWindow()
#     renWin.AddRenderer(ren)
#     iren = vtkRenderWindowInteractor()
#     iren.SetRenderWindow(renWin)
#
#     # Add the actors to the renderer, set the background and size
#     ren.AddActor(meshActor)
#     ren.SetBackground(1, 1, 1)
#     renWin.SetSize(250, 250)
#     renWin.Render()
#     cam1 = ren.GetActiveCamera()
#     cam1.Zoom(1.5)
#
#     iren.Initialize()
#     renWin.Render()
#     iren.Start()
#     return renWin

#export au format OBJ
def exportOBJ(renWin) :
    obj = vtkOBJExporter()
    obj.SetFilePrefix("essai")
    obj.SetRenderWindow(renWin)
    obj.Write()



if __name__=='__main__':
    i= 0
    j=2
    k=5
    heigth=0
    pointstri = []

    # while i <10:
    #     while j <12:
    #         point=[]
    #         point.append(i)
    #         point.append(j)
    #         point.append(k)
    #         pointstri.append(point)
    #         j=j+1
    #     j=2
    #     i=i+1
    # print(pointstri)


    zMinlist=[]
    xMaxlist=[]
    xMinlist=[]
    yMaxlist=[]
    yMinlist=[]


    zMin = 1000000000
    xMin = 1000000000
    yMin = 1000000000
    xMax = -1000000000
    yMax = -1000000000
    yMinx=0
    yMaxx=0
    xMiny=0
    xMaxy=0

    modulo = 5000
    print("Modulo : ",modulo)
    zMin = getzMin("essai.csv",",",modulo)
    fichier = importLidarCSV("essai.csv",",",modulo, zMin)
    xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx = getCorner(pointstri, xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx)
    bordDown,bord1,bord2,bord3,bord4 = getBorder(pointstri, xMin,xMax,yMin,yMax,xMaxy,xMiny,yMinx,yMaxx)
    print ("listeEcrite")
    face1,face2,face3,face4,faceInf = socle(bordDown,bord1,bord2,bord3,bord4)
    print ("socleMapped")
    rendered = renderingSocle(face1,face2,face3,face4,faceInf)
    # delny = delaunay2D(points)
    # print ("Triangulation de Delaunay")
    # mapped = mapping(delny)
    # print ("Mapping")
    # rendered = rendering(mapped)
