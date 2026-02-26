import matplotlib.pyplot as plt
import numpy as np
import sys

mm = 1/25.4

#PARAMETERS-------------
plt.rcParams.update({'font.size': 7})

undersampling_factor = 1
normalize = False
show = True
normTailWindow = 4
trim = 0

xticks = None
yticks = None

xRange = None
yRange = None

figSize = (70*mm, 35*mm)
#------------------------

#Argument parsing
while sys.argv:
	if sys.argv[0] == "--normalize":
		normalize = True
	if sys.argv[0] == "--xRange":
		xRange = [float(sys.argv[1]), float(sys.argv[2])]
		sys.argv = sys.argv[2:]
	if sys.argv[0] == "--trim":
		trim = int(sys.argv[1])
		sys.argv = sys.argv[1:]
		
	sys.argv = sys.argv[1:]

data=np.loadtxt('output.txt', skiprows=0)
data = data[trim:]

##Undersampling
#interpolatedData = []
#x = data[400:].T[0]
#y = data[400:].T[1]

## sort by x
#idx = np.argsort(x)
#x = x[idx]
#y = y[idx]

#stepGrid = x[::undersampling_factor]
#interp = np.interp(stepGrid, x, y)
#interpolatedData.append(np.array([stepGrid, interp]).T)

#data = np.array(interpolatedData[0])

if normalize:
	normLowLim = min(data.T[1])
	normHiLim = max(data.T[1])

	normFactor = (normHiLim-normLowLim)/2
	offset = 1-normHiLim/normFactor
	data=np.array([data[:,0],data[:,1]/normFactor+offset]).T

#To be done
if(xRange != None):
	padding = (max(xRange)-min(xRange))*0.04
	for i in range(len(data)):
		data[i] = np.array([[x, y, z] for x, y, z in data[i] if min(xRange)+padding < x < max(xRange)-padding])

plt.figure(figsize=figSize)
if xticks:
	plt.xticks(xticks)
if yticks:
	plt.yticks(yticks)
if(xRange != None):
    plt.xlim(xRange)
if(yRange != None):
    plt.ylim(yRange)
plt.plot(data.T[0],data.T[1], color='#008080',linewidth=1, alpha=1, markersize=2.5)
#plt.plot(xUp,yUp, '-o', color='#008080',linewidth=1, alpha=1, markersize=2.5)
plt.grid(linewidth=0.567, color='0.9')
plt.savefig('hyst.svg')	
if(show):
	plt.show()
