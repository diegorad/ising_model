#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

mm = 1/25.4

#PARAMETERS-------------
plt.rcParams.update({'font.size': 7})

undersampling_factor = 1
undersampling = False
normalize = False
show = False
grid = False
normTailWindow = 4
trim = False
trim_amount = None
column = 1
scale = 1
file_name = "hyst"

xticks = None
yticks = None

xRange = None
yRange = None

figSize = (60*mm, 40*mm)
ticks_config = None
#------------------------

#Argument parsing
while sys.argv:
	if sys.argv[0] == "--xRange":
		xRange = [float(sys.argv[1]), float(sys.argv[2])]
		sys.argv = sys.argv[2:]
	if sys.argv[0] == "--yRange":
		yRange = [float(sys.argv[1]), float(sys.argv[2])]
		sys.argv = sys.argv[2:]
	if sys.argv[0] == "--trim":
		trim = True
		if "--" not in sys.argv[1]:
			trim_amount = int(sys.argv[1])
			sys.argv = sys.argv[1:]
	if sys.argv[0] == "--column":
		column = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--name":
		file_name = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--normalize":
		normalize = True
		normalize_column = column
		if "--" not in sys.argv[1]:
			normalize_column = int(sys.argv[1])
			sys.argv = sys.argv[1:]
	if sys.argv[0] == "--undersampling":
		undersampling = True
		undersampling_factor = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--show":
		show = True
	if sys.argv[0] == "--grid":
		grid = True
	if sys.argv[0] == "--ticks":
		ticks_config = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--scale":
		scale = float(sys.argv[1])
		sys.argv = sys.argv[1:]
		
	sys.argv = sys.argv[1:]

data=np.loadtxt('output.txt', skiprows=0)
#Trim
if trim_amount == None:
	#Delete 1/5 of the data: Initial branch
	trim_amount = int(len(data)/5)

data = data[trim_amount:]

##To be done
##Undersampling
#if(undersampling):
#	interpolatedData = []
#	
#	branch_lenght = int(len(data)/2)
#	for i in range(2):
#		x = data.T[0][i*branch_lenght: (i+1)*branch_lenght]
#		y1 = data.T[1][i*branch_lenght: (i+1)*branch_lenght]
#		y2 = data.T[2][i*branch_lenght: (i+1)*branch_lenght]
#		
#		# sort by x
#		idx = np.argsort(x)
#		x = x[idx]
#		y1 = y1[idx]
#		y2 = y2[idx]
#		
#		stepGrid = x[::undersampling_factor]
#		interp1 = np.interp(stepGrid, x, y1)
#		interp2 = np.interp(stepGrid, x, y2)
#		interpolatedData.append(np.array([stepGrid, interp1, interp2]).T)

#	data = np.concatenate((interpolatedData[0], interpolatedData[1]))

if normalize:
	normLowLim = min(data.T[normalize_column])
	normHiLim = max(data.T[normalize_column])

	normFactor = (normHiLim-normLowLim)/2
	offset = 1-normHiLim/normFactor
	data=np.array([data[:,0], data[:,1]/normFactor+offset, data[:,2]/normFactor+offset]).T

#if(xRange != None):
#	padding = (max(xRange)-min(xRange))*0.04
#	data = np.array([[x, y, z] for x, y, z in data if min(xRange)+padding < x < max(xRange)-padding])

plt.figure(figsize=figSize)
if xticks:
	plt.xticks(xticks)
if yticks:
	plt.yticks(yticks)
if(xRange != None):
    plt.xlim(xRange)
if(yRange != None):
    plt.ylim(yRange)
plt.plot(data.T[0], data.T[column]*scale, color='gray',linewidth=0.2/0.35278, alpha=1)
plt.grid(linewidth=0.567, color='0.9')
plt.grid(grid)

if(ticks_config != None):
	if(ticks_config == 'right'):
		plt.tick_params(axis='y', which='both', left=False, labelleft=False, right=True, labelright=True)
	elif(ticks_config == 'none'):
		plt.tick_params(axis='both', which='both', left=False, labelleft=False, right=False, labelright=False, bottom=False, labelbottom=False)
		plt.grid(False)
	else:
		print(f'--ticks {ticks_config} is not defined.')

plt.savefig(f'{file_name}.svg', transparent=True)	
if(show):
	plt.show()
