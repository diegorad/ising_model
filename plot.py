import matplotlib.pyplot as plt
import numpy as np
import addcopyfighandler
import sys

# Load data
col1 = []
col2 = []
col3 = []

sys.argv = sys.argv[1:]

savefig = False
label = None
timePlot = False
total_magnetization = False
susceptibility = False

while sys.argv:
	if sys.argv[0] == "--savefig":
		savefig = True
	if sys.argv[0] == "--label":
		label = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--time":
		timePlot = True
	if sys.argv[0] == "--total":
		total_magnetization = True
	if sys.argv[0] == "--susceptibility":
		susceptibility = True
		
	sys.argv = sys.argv[1:]
if(susceptibility == False):
	with open("output.txt", "r") as f:
		for line in f:
		    parts = line.strip().split()
		    if len(parts) == 3:
		        a, b, c = map(float, parts)
		        col1.append(a)
		        col2.append(b)
		        col3.append(c)
	
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

	# Plot 1: Column 1 vs Column 2
	plt.subplot(1, 2, 1)
	plt.plot(col1, col2)
	plt.xlabel("Column 1")
	plt.ylabel("Column 2")
	plt.title("Column 1 vs Column 2")
	plt.ylim(y_min_padded, y_max_padded)
	plt.grid(True)

	# Plot 2: Column 1 vs Column 3
	plt.subplot(1, 2, 2)
	plt.plot(col1, col3)
	plt.xlabel("Column 1")
	plt.ylabel("Column 3")
	plt.title("Column 1 vs Column 3")
	plt.ylim(y_min_padded, y_max_padded)
	plt.grid(True)

	plt.tight_layout()

if(timePlot):
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

if(total_magnetization):
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

if(susceptibility):
	x = []
	y = []
	
	with open("susceptibility.txt", "r") as f:
		for line in f:
		    parts = line.strip().split()
		    if len(parts) == 2:
		        a, b = map(float, parts)
		        x.append(a)
		        y.append(b)
	
	# get sorting indices from x
	idx = np.argsort(x)
	
	# reorder both arrays
	x = np.array(x)[idx]
	y = np.array(y)[idx]

	plt.plot(x, y)
	plt.xlabel("T")
	plt.ylabel("X")
	plt.grid(True)
	
if(savefig):
	plt.savefig('plot.png')
else:
	plt.show()

