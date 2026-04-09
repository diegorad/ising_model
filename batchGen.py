#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 25, 20
s = np.random.normal(mu, sigma, 100)

s = [int(item) for item in s]

count, bins, ignored = plt.hist(s, 25, density=True)
plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
               np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
         linewidth=2, color='r')
plt.show()

s = [item for item in s if item > 5]

s = np.sort(s)

#Export
with open("batch_values.dat", "w") as f:
    for val in s:
        f.write(f"{int(val)}\n")
