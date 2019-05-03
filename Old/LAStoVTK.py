from laspy.file import File
import numpy as np



inFile = File("essai.laz", mode='r')

I = inFile.Classification == 2 # extrait les points représentant le sol (classe 2)

points = np.c_[inFile.X, inFile.Y, inFile.Z][I]

inFile.close()
