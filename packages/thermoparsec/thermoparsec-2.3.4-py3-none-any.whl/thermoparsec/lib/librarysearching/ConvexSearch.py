import numpy as np
from scipy import linalg


def ConvexSpectralSearch(A, b, rho=0.00000001, threshold=0.001, iterations=1500):
    # A = A'* A
    a = np.transpose(A) * A
    # b = A' * b
    b = np.transpose(A) * b
    # identity matrix
    I = np.identity(len(a))

    # Inverse 'prime A' matrix
    Aprime = linalg.inv((a + rho * I))

    # Solution vectors
    u = np.zeros((len(b), 1))
    z = np.zeros((len(b), 1))
    x = np.zeros((len(b), 1))

    # RMS <- c()
    for i in range(0, iterations):
        x = Aprime * (b + rho * (z - u))
        for j in range(0, len(x)):
            temp = x[j] + u[j]
            if (temp > 0):
                z[j] = temp
            else:
                z[j] = 0
        for k in range(0, len(u)):
            u[k] = u[k] + (x[k] - z[k])
    return z


# Usage
# Ax = b least squares solution using matrix inversion
# example matrix (rows are mz and columns are scan )
A = np.mat('[1 1 1;1 2 3;1 3 6;1 5 14;1 17 2]')

# example experimental

b = [[2], [3], [4], [6], [18]]

# least squares solution
# x = linalg.inv(np.transpose(A)*A) * np.transpose(A) * b

print(A)
print(b)
r = ConvexSpectralSearch(A, b)
print(r)
