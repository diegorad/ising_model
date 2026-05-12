#!/usr/bin/env python3

import numpy as np
import sys
import matplotlib.pyplot as plt

threshold = 10
x_threshold = 1
rounding = 4
column = 1
show = False

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
    if sys.argv[0] == "--show":
        show = True
    
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

sign_list = np.sign(data[:,1])
data = [entry for entry in zip(data, sign_list)]

zeros = []
for i in range(len(data)-1):
	if data[i][1] != data[i+1][1]:
		zeros.append((data[i][0][0] + data[i+1][0][0])/2)
		
if(len(zeros) == 0):
	zero = -0.0
else:
	zero = np.mean(zeros)
	
print(round(zero,3))
exit()

x_lim=max(data[:, 0])

mask = np.abs(data[:, 0]) <= x_threshold
trim_data = data[mask]

near_zero = []
positives = None
negatives = None

while(len(near_zero) < 25):
	mask = np.abs(data[:, 0]) <= x_threshold
	trim_data = data[mask]
	near_zero = trim_data[np.abs(trim_data[:, 1]) <= threshold]
	
	sign_list = np.sign(near_zero[:,1])
	positives = len([i for i in sign_list if i == 1.])
	negatives = len([i for i in sign_list if i == -1.])
	print(positives, negatives)
	
	if x_threshold < x_lim:
		x_threshold = x_threshold + 0.1
	else:
		x_threshold = 0.1
		threshold = threshold + 1

x = near_zero[:,0]
y = near_zero[:,1]

#Linear fit and zero
coefficients = np.polyfit(x, y, 1)
p = np.poly1d(coefficients)

if(show):
	plt.figure()
	plt.scatter(x, y, label='Data Points')
	plt.plot(x, p(x), label='Linear Fit', color='red')
	plt.grid()
	plt.show()	
	
try:
	zero = p.r[0]
except:
	zero = -0.0
print(f"{round(zero, rounding)}")
