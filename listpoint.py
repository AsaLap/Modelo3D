from vtk import *
import csv



def importLidarCSV(filename, delimiter,modulo) :
    points = vtkPoints()
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar='|')
        print ("Import du fichier")
        i = 0
        j=0
        k=0
        for row in reader:
            if (k !=0 and row[8]=='2.000' and k%modulo==0) :
                zMinlist.append(int(float(row[2])))
            k=k+1
        zMin=min(zMinlist)
        for row in reader:
            if (i != 0 and row[8]=='2.000') : #row[8] est la catégorie des points, 2.000 correspond au sol
                    points.InsertNextPoint(int(float(row[0])),int(float(row[1])), int(float(row[2])))
                    j=j+1
            i = i+1
    print ("Nombre de points importés  : ",j)
    print (zMin)
    print (zMinlist)
    return points


def getCorner (points):
    for point in points :
        if point[2] < zMin :
            zMin = point[2]
        if point[0] <xMin :
            xMin = point[0]
        if point[0] > xMax :
            xMax = point[0]
        if point[1] <yMin :
            yMin = point[1]
        if point[1] > yMax :
            yMax = point[1]
    for point in points:
        if point[0] == xMax:
            xMaxlist.append(point[1])
        if point[0 ]== xMin:
            xMinlist.append(point[1])
        if point[1] == yMax:
            yMaxlist.append(point[0])
        if point[1] == yMin:
            yMinlist.append(point[0])
    xMaxy=max(xMaxlist)
    xMiny=min(xMinlist)
    yMaxx=min(yMaxlist)
    yMinx=max(yMinlist)


def getBorder():
    for point in points :
        if point[0] >= xMin and point[0]<= yMinx:
            if point[1]>=yMin and point[1]<=xMiny:
                bord1.append(point)
        if point[0] >= yMinx and point[0] <= xMax:
            if point[1]>=yMin and point[1]<= xMaxy:
                bord2.append(point)
        if point[0] <= xMax and point [0] >= yMaxx:
            if point[1]<= yMax and point[1] >= xMaxy:
                bord3.append(point)
        if point[0]<= yMaxx and point[0]>= xMin:
            if point[1]<= yMax and point[1]>= xMiny:
                bord4.append(point)


if __name__=='__main__':
    i= 0
    j=2
    k=-12

    points = []
    zMinlist=[]
    xMaxlist=[]
    xMinlist=[]
    yMaxlist=[]
    yMinlist=[]

    bord1 = []
    bord2 = []
    bord3 = []
    bord4 = []

    while i < 10 :
        while j < 12 :
            point = []
            point.append(i)
            point.append(j)
            point.append(k)
            points.append(point)
            j=j+1
            k=k+1
        j = 2
        i = i+1

    zMin = 1000000
    xMin = 1000000
    yMin = 1000000
    xMax = -1000000
    yMax = -1000000
    yMinx=0
    yMaxx=0
    xMiny=0
    xMaxy=0

    modulo = 1
    print("Modulo : ",modulo)
    fichier = importLidarCSV("essai.csv",",",modulo)
