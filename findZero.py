#!/usr/bin/env python3

import numpy as np
import sys

threshold = 10
x_threshold = 0.1
rounding = 4
column = 1

# Load data
col1 = []
col2 = []
col3 = []

file_name_arg = None

while sys.argv:
    if sys.argv[0] == "--file" or sys.argv[0] == "-f":
        file_name_arg = sys.argv[1]
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--column":
        column = int(sys.argv[1])
        sys.argv = sys.argv[1:]
    
    sys.argv = sys.argv[1:]

if(file_name_arg == None):
    file_name = "output.txt"
else:
    file_name = file_name_arg

with open(file_name, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            a, b, c = map(float, parts)
            col1.append(a)
            col2.append(b)
            col3.append(c)
        
data = [col1, col2, col3]
    
data = np.array([data[0], data[column]]).T

x_lim=max(data[:, 0])

mask = np.abs(data[:, 0]) <= x_threshold
trim_data = data[mask]

near_zero = trim_data[np.abs(trim_data[:, 1]) <= threshold]
while(len(near_zero) < 4):
	if x_threshold < x_lim:
		x_threshold = x_threshold + 0.1
	else:
		x_threshold = 0.1
		threshold = threshold + 1
	
	mask = np.abs(data[:, 0]) <= x_threshold
	trim_data = data[mask]
	near_zero = trim_data[np.abs(trim_data[:, 1]) <= threshold]
	
zero = sum(near_zero.T[0])/len(near_zero.T[0])

print(f"{round(zero, rounding)}")

#numberOfPoints = len(data)
#
#halfBranchLenght = int(numberOfPoints/5)
#
#down = data[halfBranchLenght:3*halfBranchLenght]
#down_near_zero = down[np.abs(down[:, 1]) <= threshold]
#while(len(down_near_zero) < 4):
#	threshold = threshold + 1
#	down_near_zero = down[np.abs(down[:, 1]) <= threshold]
#
#up = data[3*halfBranchLenght:numberOfPoints]
#up_near_zero = up[np.abs(up[:, 1]) <= threshold]
#
#down_zero = sum(down_near_zero.T[0])/len(down_near_zero.T[0])
#up_zero = sum(up_near_zero.T[0])/len(up_near_zero.T[0])
#
##print(f"Down={round(down_zero, rounding)}, Up={round(up_zero, rounding)}, diff={round(up_zero-abs(down_zero), rounding)}")
#print(f"{round(down_zero, rounding)} {round(up_zero, rounding)} {round(up_zero-abs(down_zero), rounding)}")
