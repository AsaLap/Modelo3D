from vtk import *

i= 0
j=0
k=-12

points = []

while i < 10 :
    while j < 10 :
        point = []
        point.append(i)
        point.append(j)
        point.append(k)
        points.append(point)
        j=j+1
        k=k+1
    j = 0
    i = i+1
def support()
    zMin = 1000000
    xMin = 1000000
    yMin = 1000000
    xMax = -1000000
    yMax = -1000000

    for point in points :
        if point[2] < zMin :
            zMin = point[2]
        if point[0] <xMin :
            xMin = point[0]
            xMiny = point[1]
        if point[0] > xMax :
            xMax = point[0]
            xMaxy = point[1]
        if point[1] <yMin :
            yMin = point[1]
            yMinx = point[0]
        if point[1] > yMax :
            yMax = point[1]
            yMaxx = point[0]
    res = [zMin, xMin, yMin, xMiny, xMaxy, yMin, yMinx, yMax, yMaxx]
    return res
bord1 = []
bord2 = []
bord3 = []
bord4 = []
for point in points :
    if point[1] >= xMiny and point[1] <= xMaxy :
        bord1.append(point)
    if point[0] >= yMinx and point[0] <= yMaxx :
        bord2.append(point)
    if point[0] >= xMin and point[0]<= yMinx:
        if point[1]>=yMin and point[1]<=xMiny:
            bord3.append(point)
    if point[0]<=xMax and point[0]>=yMaxx :
        if point[1]<=yMax and point[1]>=xMaxy:
            bord4.append(point)

print (bord4)

