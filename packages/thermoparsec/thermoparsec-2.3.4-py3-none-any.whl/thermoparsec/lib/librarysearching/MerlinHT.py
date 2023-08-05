from sys import argv
from scipy.sparse.linalg import lsqr
import numpy as np
from pyspark.mllib.linalg.distributed import CoordinateMatrix, MatrixEntry,BlockMatrix,RowMatrix
from pyspark.mllib.linalg import Matrix, Matrices,DenseVector,DenseMatrix

import pyspark
sc = pyspark.SparkContext(appName="Merlin Library Searching")
from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)

#Functions#########################################################################################
def GetMatrix(m):
    l = []
    for v in m:
        r = v[0]
        c = v[1]
        d = v[2]
        l.append(MatrixEntry(r,c,d))
    return l

def GetQMatrix(m):
    l = []
    row = 0
    for v in m:
        for i in range(len(v)):
            r = row
            c = i
            d = v[i]
            l.append(MatrixEntry(r,c,d))
        row = row + 1
    return l


#READ IN DATA#######################################################################################
#read matrix data from commandline
matrix = np.genfromtxt(argv[1], delimiter=",")

#read vector data from commandline
vector = np.genfromtxt(argv[2], delimiter=",")
####################################################################################################

# Create an RDD of coordinate entries.
A = GetMatrix(matrix)
entries = sc.parallelize(A)

# Create an CoordinateMatrix from an RDD of MatrixEntries.
cooMatrixA = CoordinateMatrix(entries)

#create block matrix
matA = cooMatrixA.toBlockMatrix()

#checking results print the matrix
print(matA.toLocalMatrix())

#create block matrix after matrix multiplication (square matrix)
ata = matA.transpose().multiply(matA);

#checking results print inner product
print(ata.toLocalMatrix())

#QR decomposition DEMO
#Convert it to an IndexRowMatrix whose rows are sparse vectors.
indexedRowmatrix = cooMatrixA.toIndexedRowMatrix()

#Drop its row indices.
rowMat = indexedRowmatrix.toRowMatrix()

#Compute QR################################################################################################
result = rowMat.tallSkinnyQR(True)
q = result.Q.rows.collect()

matrixQ = GetQMatrix(q)
qEntries = sc.parallelize(matrixQ)

# Create an CoordinateMatrix from an RDD of MatrixEntries.
cooMatrixQ = CoordinateMatrix(qEntries)

matQ = cooMatrixQ.toBlockMatrix()

q = matQ.toLocalMatrix()

# Create an RDD of coordinate entries.
b = GetMatrix(vector)
bEntries = sc.parallelize(b)
cooMatrixB =  CoordinateMatrix(bEntries)

#create block matrix
matB = cooMatrixB.toBlockMatrix()

#check results
b = matB.toLocalMatrix()

d = matQ.transpose().multiply(matB).toLocalMatrix()
r = result.R


#solve using gaussian elimination or least squares

