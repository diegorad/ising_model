#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import sys

#PARAMETERS-------------

normTailWindow = 2
column = 1
show = False

#------------------------

#Argument parsing
while sys.argv:
    if sys.argv[0] == "--show":
        show = True
    if sys.argv[0] == "--column":
        column = int(sys.argv[1])
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
branch = int(len(simRawData)/5)
simRawData = np.array([simRawData[:,0], simRawData[:,column]]).T

simData = np.array([sortnp(simRawData[branch:3*branch],0),sortnp(simRawData[3*branch:5*branch],0)])

#Data normalization	
normLimits = []
normLimits.append(np.mean([np.mean(d[:,1][0:normTailWindow]) for d in data]))
normLimits.append(np.mean([np.mean(d[:,1][-normTailWindow]) for d in data]))

normLowLim = min(normLimits)
normHiLim = max(normLimits)
#normLowLim = min(data[0][:,1])
#normHiLim = max(data[0][:,1])

normFactor = (normHiLim-normLowLim)/2
offset = 1-normHiLim/normFactor
for i in range(len(data)):
	data[i]=np.array([data[i][:,0],data[i][:,1]/normFactor+offset]).T

#Sim normalization	
normLimits = []
normLimits.append(np.mean([np.mean(d[:,1][0:normTailWindow]) for d in simData]))
normLimits.append(np.mean([np.mean(d[:,1][-normTailWindow]) for d in simData]))
normLowLim = min(normLimits)
normHiLim = max(normLimits)

#y_smooth_sim = savgol_filter(simData[0][:,1], 25, 3)
#normLowLim = min(y_smooth_sim)
#normHiLim = max(y_smooth_sim)

normFactor = (normHiLim-normLowLim)/2
offset = 1-normHiLim/normFactor
for i in range(len(simData)):
	simData[i]=np.array([simData[i][:,0],simData[i][:,1]/normFactor+offset]).T

##Sim normalization
#normLowLim = min(simData.T[column])
#normHiLim = max(simData.T[column])
#
#normFactor = (normHiLim-normLowLim)/2
#offset = 1-normHiLim/normFactor
#simData=np.array([simData[:,0], simData[:,column]/normFactor+offset]).T


plt.figure()
error = []
for i in range(2):
    x = data[i][:,0]
    y = data[i][:,1]
    
    x_sim = simData[i][:,0]
    y_sim = simData[i][:,1]

    #Smoothing
    y_smooth = savgol_filter(y, 15, 3)
    y_sim_smooth = savgol_filter(y_sim, 25, 3)
    

    #Sim data interpolation to experimental
    simData_interp = np.interp(x, x_sim, y_sim_smooth)

    error.append(np.square(np.subtract(y_smooth,simData_interp)).mean())

#    plt.plot(x, y)
    plt.plot(x, y, color="tab:blue", label='Data')
    plt.plot(x_sim,y_sim, color="tab:orange", label='Sim')

print(np.mean(error))
plt.legend()
if(show):
    plt.show()
