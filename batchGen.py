#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys

#PARAMETERS-------------

batch_type = None
start = None
stop = None

#------------------------

#Argument parsing
while sys.argv:
    if sys.argv[0] == "--type":
        batch_type = sys.argv[1]
        sys.argv = sys.argv[1:]
        
    sys.argv = sys.argv[1:]

if(batch_type == 'normal'):
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

if(batch_type == 'lin'):
	s = [i for i in range(1, 100, 1)]
	print(s)

#Export
with open("batch_values.dat", "w") as f:
    for val in s:
        f.write(f"{val}\n")
