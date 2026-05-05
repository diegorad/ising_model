#!/usr/bin/env python3

import numpy as np
import glob
import sys

#Defaults
avg_time = False
susceptibility = False
T = None
size = None
trim = False
trim_amount = None
bin_size = 0.1
file_name = "output.txt"
file_dir = "./run/run_0/output_serie"

mode = "files"

while sys.argv:
	if sys.argv[0] == "--mode":
		mode = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--file" or sys.argv[0] == "-f":
		file_name = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--dir":
		file_dir = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--time":
		mode = "time"
	if sys.argv[0] == "--susceptibility" or sys.argv[0] == "-s":
		mode = "susceptibility"
	if sys.argv[0] == "--stepped":
		mode = "stepped_loop"
	if sys.argv[0] == "--T":
		T = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--bin_size":
		bin_size = float(sys.argv[1])
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
	files = glob.glob(f"{file_dir}/*.txt")

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
	np.savetxt(f"{file_dir}/../averaged_output.txt", avg_data)

	print(f"Done! Saved in {file_dir}/../averaged_output.txt")

if(mode == "time"):
	data = np.loadtxt("output.txt")

	mean_col2 = np.mean(data[trim_amount:, 1])
	mean_col3 = np.mean(data[trim_amount:, 2])

	print(mean_col2, mean_col3)
	
if(mode == "susceptibility" and T != None and size != None):
	data = np.loadtxt(file_name)
	
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

if(mode == "bin"):
	data = np.loadtxt(file_name)
	
	#Trim
	if trim:
	    if trim_amount == None:
	        #Delete 1/5 of the data: Initial branch
	        trim_amount = int(len(data)/5)
	else:
	    trim_amount = 0
	
	previous_field = None
	current_field = None
		
	array = []
	for entry in data:
		current_field = entry[0]
		
		if(previous_field != None):
			if(abs(current_field - previous_field)<bin_size):
				array.append(entry)
			else:
				if(len(array)<=1):
					print(*entry)
				else:
					array = np.array(array)
					array_avg = np.mean(array, axis=0)
					print(*array_avg)
				
				previous_field = current_field
				array = []
		else:
			previous_field = current_field

if(mode == "stepped_loop"):
	data = np.loadtxt("output.txt")
	
	#Trim
	if trim:
	    if trim_amount == None:
	        #Delete 1/5 of the data: Initial branch
	        trim_amount = int(len(data)/5)
	else:
	    trim_amount = 0
	
	previous_field = None
	current_field = None
		
	array = []
	for entry in data:
		current_field = entry[0]
		
		if(previous_field != None):
			if(current_field == previous_field):
				array.append([entry[1], entry[2]])
			else:
				array = np.array(array)
				trim_amount = int(len(array)/5)
				M0 = array[trim_amount:, 0]
				M1 = array[trim_amount:, 1]
				
				M = [np.mean(M0), np.mean(M1)]
				
				print(previous_field, np.mean(M0), np.mean(M1))
				array = []
#				exit()
		
		previous_field = current_field
