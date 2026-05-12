#!/usr/bin/env python3

import numpy as np
import sys

#PARAMETERS-------------

index = 1

#------------------------

#Argument parsing
while sys.argv:
    if sys.argv[0] == "--index":
        index = int(sys.argv[1])
        sys.argv = sys.argv[1:]    
        
    sys.argv = sys.argv[1:]

fileName = f"./run/run_{index}/zeros.txt"

data = np.loadtxt(fileName, skiprows=0)

error = []

targets = [[1.0, 0], [0.6, -0.48], [0.78, -0.2]]

for target in targets:  
	result = data[np.isclose(data[:, 0], target[0]), 1]
	error.append(abs(result - target[1]))

print(np.mean(error))
