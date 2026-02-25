import numpy as np
import sys

threshold = 10
numberOfPoints = 1000
rounding = 4

# Load data
col1 = []
col2 = []
col3 = []

with open("output.txt", "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            a, b, c = map(float, parts)
            col1.append(a)
            col2.append(b)
            col3.append(c)
            
data = np.array([col1, col2]).T

numberOfPoints = len(data)

halfBranchLenght = int(numberOfPoints/4)

down = data[halfBranchLenght:3*halfBranchLenght]
down_near_zero = down[np.abs(down[:, 1]) <= threshold]

up = data[3*halfBranchLenght:numberOfPoints]
up_near_zero = up[np.abs(up[:, 1]) <= threshold]

down_zero = sum(down_near_zero.T[0])/len(down_near_zero.T[0])
up_zero = sum(up_near_zero.T[0])/len(up_near_zero.T[0])

print(f"Down={round(down_zero, rounding)}, Up={round(up_zero, rounding)}, diff={round(up_zero-abs(down_zero), rounding)}")
