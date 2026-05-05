#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys

#PARAMETERS-------------

mode = 'range'
steps = None
step = 1
start = None
stop = None
reverse = False
#------------------------

#Argument parsing
while sys.argv:
    if sys.argv[0] == "--mode":
        mode = sys.argv[1]
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--reverse":
        reverse = True
    if sys.argv[0] == "--steps":
        steps = int(sys.argv[1])
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--step":
        step = int(sys.argv[1])
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--start":
        start = float(sys.argv[1])
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--stop":
        stop = float(sys.argv[1])
        sys.argv = sys.argv[1:]
        
    sys.argv = sys.argv[1:]

if(mode == 'normal'):
	mu, sigma = 25, 1000
	s = np.random.normal(mu, sigma, 500)

	s = [int(item) for item in s]

	count, bins, ignored = plt.hist(s, 30, density=True)
	plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
		           np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
		     linewidth=2, color='r')
	plt.show()

	s = [int(item) for item in s if item > 4]

	s = np.sort(s)

if(mode == 'int_range'):
	s = [i for i in range(int(start), int(stop+step), step)]
	if(reverse):
		s.reverse()
	print(s)
	
if(mode == 'range'):
	s = np.linspace(start, stop, steps)
	if(reverse):
		s.reverse()
	print(s)

if mode == 'log_range':
    s = np.logspace(np.log10(start), np.log10(stop), steps)
    if reverse:
        s = s[::-1]
    print(s)

if(mode == 'function'):
	def N(n):
		result = 2500/n**2
		
		return result
	
	s = []
	for i in range(int(start), int(stop+step), step):
		print(i,int(N(i)))
		subList = [i for _ in range(int(N(i)))]
		s = s+subList
		
	if(reverse):
		s.reverse()
		
#	print(f"Batch lenght: {len(s)}")
#	print(s)
	
#Export
with open("batch_values.dat", "w") as f:
    for val in s:
        f.write(f"{val}\n")
