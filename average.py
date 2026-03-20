#!/usr/bin/env python3

import numpy as np
import glob
import sys

#Defaults
avg_files = True
avg_time = False
susceptibility = False
T = None
size = None
trim = False
trim_amount = None

mode = "files"

while sys.argv:
	if sys.argv[0] == "--files":
		mode = "files"
	if sys.argv[0] == "--time":
		mode = "time"
	if sys.argv[0] == "--susceptibility" or sys.argv[0] == "-s":
		mode = "susceptibility"
	if sys.argv[0] == "--T":
		T = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--size":
		size = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--trim":
		trim = True
		if len(sys.argv) > 1:
		    if "--" not in sys.argv[1]:
			    trim_amount = int(sys.argv[1])
			    sys.argv = sys.argv[1:]
			    
	sys.argv = sys.argv[1:]

if(mode == "files"):
	# Get all files in the folder
	files = glob.glob("output_serie/*.txt")

	y1_all = []
	y2_all = []

	for f in files:
	    data = np.loadtxt(f)
	    x = data[:, 0]
	    y1_all.append(data[:, 1])
	    y2_all.append(data[:, 2])

	# Convert to arrays
	y1_all = np.array(y1_all)
	y2_all = np.array(y2_all)

	# Average across files
	y1_avg = np.mean(y1_all, axis=0)
	y2_avg = np.mean(y2_all, axis=0)

	# Save result
	avg_data = np.column_stack((x, y1_avg, y2_avg))
	np.savetxt("output.txt", avg_data)

	print("Done! Saved as output.txt")

if(mode == "time"):
	data = np.loadtxt("output.txt")

	mean_col2 = np.mean(data[trim_amount:, 1])
	mean_col3 = np.mean(data[trim_amount:, 2])

	print(mean_col2, mean_col3)
	
if(mode == "susceptibility" and T != None and size != None):
	data = np.loadtxt("output.txt")
	
	#Trim
	if trim:
	    if trim_amount == None:
	        #Delete 1/5 of the data: Initial branch
	        trim_amount = int(len(data)/5)
	else:
	    trim_amount = 0
	
	M0 = data[trim_amount:, 1]
	M1 = data[trim_amount:, 2]
	
	M = [(x + y)/pow(size,2) for x, y in zip(M0, M1)]
	
	print(np.mean(M), pow(size,2)/T * np.var(M))
