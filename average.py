import numpy as np
import glob
import sys

#Defaults
avg_files = True
avg_time = False
susceptibility = False
T = None

while sys.argv:
	if sys.argv[0] == "--files":
		avg_files = True
	if sys.argv[0] == "--time":
		avg_time = True
		avg_files = False
	if sys.argv[0] == "--susceptibility":
		susceptibility = True
		avg_files = False
	if sys.argv[0] == "--T":
		T = float(sys.argv[1])
		sys.argv = sys.argv[1:]
	sys.argv = sys.argv[1:]
	
if(avg_files):
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

if(avg_time):
	data = np.loadtxt("output.txt")

	mean_col2 = np.mean(data[1000:, 1])
	mean_col3 = np.mean(data[1000:, 2])

	print(mean_col2, mean_col3)
	
if(susceptibility and T != None):
	data = np.loadtxt("output.txt")
	
	M0 = data[100:, 1]
	M1 = data[100:, 2]
	
	M = [x + y for x, y in zip(M0, M1)]
	
	print(1/T * np.var(M))
