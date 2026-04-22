#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys
try:
    import addcopyfighandler
except ImportError:
    pass

#PARAMETERS-------------

normTailWindow = 2
column = 1
show = False
mode = "half_loop"
trim = False
trim_amount = 0
savefig = False
label = None
norm_mode = "tail"

#------------------------

#Argument parsing
while sys.argv:
	if sys.argv[0] == "--savefig":
		savefig = True
	if sys.argv[0] == "--show":
		show = True
	if sys.argv[0] == "--label":
		label = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--column":
		column = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--mode":
		mode = sys.argv[1]
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--norm":
		norm_mode = sys.argv[1]
		sys.argv = sys.argv[1:]
		if len(sys.argv) > 1:
			if "--" not in sys.argv[1]:
				normTailWindow = int(sys.argv[1])
				sys.argv = sys.argv[1:]
	if sys.argv[0] == "--norm_tail":
		normTailWindow = int(sys.argv[1])
		sys.argv = sys.argv[1:]
	if sys.argv[0] == "--trim":
		trim = True
		if len(sys.argv) > 1:
			if "--" not in sys.argv[1]:
				trim_amount = int(sys.argv[1])
				sys.argv = sys.argv[1:]
		
	sys.argv = sys.argv[1:]

#Sort by first n-row an np.data1
def sortnp(a, n):
	return a[a[:, n].argsort()]

fileNames = [f'./data/down_{column}.txt', f'./data/up_{column}.txt']
simFile = 'output.txt'

data = []
for fileName in fileNames:
	data.append(np.loadtxt(fileName, skiprows=0))

simRawData = []
simRawData = np.loadtxt(simFile, skiprows=0)
simRawData = np.array([simRawData[:,0], simRawData[:,column]]).T

#Trim
if trim:
	trimmed_simData=simRawData[trim_amount:]

	simRawData=np.array(trimmed_simData)

if(mode == "half_loop"):
	simData = np.array([sortnp(simRawData, 0)])
	data = [data[0]]
else:
	branch = int(len(simRawData)/5)
	simData = np.array([sortnp(simRawData[branch:3*branch],0),sortnp(simRawData[3*branch:5*branch],0)])

#Trim data to sim
for entry in simData:
	low_bound=np.min(entry, axis=0)
	high_bound=np.max(entry, axis=0)

for i in range(len(data)):
		data[i] = np.array([[x, y] for x, y in data[i] if low_bound[0] < x < high_bound[0]])

#Data normalization	
if(norm_mode == "tail"):
	normLimits = []
	normLimits.append(np.mean([np.mean(d[:,1][0:normTailWindow]) for d in data]))
	normLimits.append(np.mean([np.mean(d[:,1][-normTailWindow]) for d in data]))

	normLowLim = min(normLimits)
	normHiLim = max(normLimits)
	
if(norm_mode == "range"):
	normLowLim = min(data[0][:,1])
	normHiLim = max(data[0][:,1])

normFactor = (normHiLim-normLowLim)/2
offset = 1-normHiLim/normFactor
for i in range(len(data)):
	data[i]=np.array([data[i][:,0],data[i][:,1]/normFactor+offset]).T

plt.figure()
error = []
for i in range(len(simData)):
	x = data[i][:,0]
	y = data[i][:,1]
	
	x_sim = simData[i][:,0]
	y_sim = simData[i][:,1]

	#Smoothing
#	y_smooth = savgol_filter(y, 15, 3)
#	y_sim_smooth = savgol_filter(y_sim, 25, 3)
	

	#Sim data interpolation to experimental
	simData_interp = np.interp(x, x_sim, y_sim)
	
	#Sim normalization
	if(norm_mode == "tail")	:
		normLimits = []
		normLimits.append(np.mean(simData_interp[0:normTailWindow]))
		normLimits.append(np.mean(simData_interp[-normTailWindow]))
		
		normLowLim = min(normLimits)
		normHiLim = max(normLimits)
		
	if(norm_mode == "range"):	
		normLowLim = min(simData_interp)
		normHiLim = max(simData_interp)	
	
	normFactor = (normHiLim-normLowLim)/2
	offset = 1-normHiLim/normFactor
	simData_interp = np.array(simData_interp/normFactor+offset)

	error_list = np.abs(np.subtract(y,simData_interp)/(abs(x*1)+1))
	error.append(error_list.mean())

	plt.plot(x, y, color="tab:blue", label='Data')
	plt.plot(x, error_list, color="tab:red", label='Error')
#	plt.plot(x_sim,y_sim, color="tab:orange", label='Sim')
	plt.plot(x,simData_interp, color="tab:orange", label='Sim')

plt.grid(True)
plt.title(label)
plt.legend()

print(np.mean(error))

if(savefig):
	plt.savefig('plot.png')
	
if(show):
	plt.show()
