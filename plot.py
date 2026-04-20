#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import sys

try:
    import addcopyfighandler
except ImportError:
    pass

# Load data
col1 = []
col2 = []
col3 = []

sys.argv = sys.argv[1:]

savefig = False
label = None
trim = False
trim_amount = None
file_name_arg = None

plot_mode = "loop"

while sys.argv:
	if sys.argv[0] == "--savefig":
		savefig = True
	if sys.argv[0] == "--label":
		label = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--file" or sys.argv[0] == "-f":
		file_name_arg = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--time" or sys.argv[0] == "-t":
		plot_mode = "time"
	if sys.argv[0] == "--total":
		plot_mode = "total_magnetization"
	if sys.argv[0] == "--avg_mag":
		plot_mode = "average_magnetization"
	if sys.argv[0] == "--susceptibility" or sys.argv[0] == "-s":
		plot_mode = "susceptibility"
	if sys.argv[0] == "--trim":
		trim = True
		if len(sys.argv) > 1:
		    if "--" not in sys.argv[1]:
			    trim_amount = int(sys.argv[1])
			    sys.argv = sys.argv[1:]
		
	sys.argv = sys.argv[1:]
	
if(plot_mode == "loop" or plot_mode == "time" or plot_mode == "total_magnetization"):
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
	
	#Trim
	if trim:
	    if trim_amount == None:
	        #Delete 1/5 of the data: Initial branch
	        trim_amount = int(len(col1)/5)
	else:
	    trim_amount = 0
	
	col1 = col1[trim_amount:]
	col2 = np.array(col2[trim_amount:])
	col3 = np.array(col3[trim_amount:])
	
	# Compute global Y limits across columns 2 and 3
	y_min = min(min(col2), min(col3))
	y_max = max(max(col2), max(col3))

	# Add padding (10%)
	padding = 0.1 * (y_max - y_min)
	y_min_padded = y_min - padding
	y_max_padded = y_max + padding
	#y_min_padded = -3000
	#y_max_padded = 3000

	# Create figure with 2 horizontal subplots
	plt.figure(figsize=(10, 4))
	plt.suptitle(label)

	markers = 'None' if len(col1) > 100 else 'o'

	# Plot 1: Column 1 vs Column 2
	plt.subplot(1, 2, 1)
	plt.plot(col1, col2, marker = markers)
	plt.xlabel("Column 1")
	plt.ylabel("Column 2")
	plt.title("Column 1 vs Column 2")
	plt.ylim(y_min_padded, y_max_padded)
	plt.grid(True)

	# Plot 2: Column 1 vs Column 3
	plt.subplot(1, 2, 2)
	plt.plot(col1, col3, marker = markers)
	plt.xlabel("Column 1")
	plt.ylabel("Column 3")
	plt.title("Column 1 vs Column 3")
	plt.ylim(y_min_padded, y_max_padded)
	plt.grid(True)

	plt.tight_layout()

if(plot_mode == "time"):
	plt.close()
	plt.figure(figsize=(10, 4))
	plt.suptitle(label)
	
	plt.subplot(1, 2, 1)
	plt.plot(col2)
	plt.ylim(y_min_padded, y_max_padded)
	plt.grid(True)
	
	plt.subplot(1, 2, 2)
	plt.plot(col3)
	plt.ylim(y_min_padded, y_max_padded)
	plt.grid(True)
	
	plt.tight_layout()

if(plot_mode == "total_magnetization"):
	plt.cla()
	
	plt.subplot(1, 2, 1)
	plt.plot(col1, col2)
	plt.xlabel("h")
	plt.ylabel("M")
	plt.title("Magnetization")
	plt.ylim(y_min_padded, y_max_padded)
	plt.grid(True)
	
	plt.subplot(1, 2, 1)
	plt.plot(col1, col3)
	
	# Plot total magnetization
	plt.subplot(1, 2, 2)
	total_m = [i+j for i,j in zip(col2,col3)]
	plt.plot(col1, total_m)
	plt.xlabel("h")
	plt.ylabel("M")
	plt.title("Total magnetization")
#	plt.ylim(y_min_padded, y_max_padded)
	plt.grid(True)

if(plot_mode == "susceptibility"):
	if(file_name_arg == None):
		file_name = "susceptibility.txt"
	else:
		file_name = file_name_arg
		
	x = []
	y1 = []
	y2 = []
	
	with open(file_name, "r") as f:
		for line in f:
		    parts = line.strip().split()
		    if len(parts) == 3:
		        a, b, c = map(float, parts)
		        x.append(a)
		        y1.append(b)
		        y2.append(c)
	
	# get sorting indices from x
	idx = np.argsort(x)
	
	# reorder both arrays
	x = np.array(x)[idx]
	y1 = np.array(y1)[idx]
	y2 = np.array(y2)[idx]
	
	plt.close()
	plt.figure(figsize=(10, 4))
	plt.suptitle(label)
	
	plt.subplot(1, 2, 1)
#	plt.xlabel("N")
	plt.ylabel("<M>")
#	plt.ylim([-, 1.1])
	plt.plot(x, y1, marker = "o", linestyle='-')
	plt.grid(True)
	
	plt.subplot(1, 2, 2)
#	plt.xlabel("N")
	plt.ylabel("X")
	plt.plot(x, y2, marker = "o", linestyle='None')
	plt.grid(True)
	
	plt.tight_layout()
	
if(savefig):
	plt.savefig('plot.png')
else:
	plt.show()

