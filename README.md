# Ising model implemented in C
Implementation of the Ising model written in C along with tools to prepare the simulation and analyze the results. This implementation is aimed mainly towards the simulation of hysteresis loops of mixed-spin systems. It uses Glauber-Metropolis dynamics. It supports arbitrary spin values and includes a crystal field `D` term.

Energy of a spin $i$:

$E_i=-\sigma_i \sum_{j} J_{ij}\sigma_j-\sigma_i H-\sigma_i^2D$

Basic usage:

1) Generate the spin lattice with `netgen.py`
1) Generate a field routine with `fieldgen.py`
1) Run simulation over the defined field routine with `ising_model`	 
1) Plot result with `plot.py`
