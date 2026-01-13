import numpy as np
import sys

index = sys.argv[1]
threshold = 500
numberOfPoints = 1000

# Load data
col1 = []
col2 = []
col3 = []

with open("output.txt".format(index), "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            a, b, c = map(float, parts)
            col1.append(a)
            col2.append(b)
            col3.append(c)
            
data = np.array([col1, col3]).T

halfBranchLenght = int(numberOfPoints/5)

down = data[halfBranchLenght:3*halfBranchLenght]
down_zero = down[np.abs(down[:, 1]) <= threshold]

up = data[3*halfBranchLenght:numberOfPoints]
up_zero = up[np.abs(up[:, 1]) <= threshold]
print(round(sum(down_zero.T[0])/len(down_zero.T[0]),2), round(sum(up_zero.T[0])/len(up_zero.T[0]),2))
