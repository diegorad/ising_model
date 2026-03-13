#!/usr/bin/env python3

import subprocess
import numpy as np
from scipy.optimize import minimize, basinhopping


def run_line(line):
        comm = line.split(" ")    
        subprocess.run(comm, check=True)

def f(x):
    y = -0.734375+2.16667*x
    return y

def run_simulation(params):
    if(len(params)==1):
        x = params[0]
        y = f(x)
    else:
        x, y = params

    run_line(f"./fieldgen.py --rate {x} --range 2")
    run_line(f'./ising_model --J_ij={{2.625,0.0,0.0}} --D_i={{0.0,0.0}} --T 6 --out=monitor')
    print('')

def compute_error():
    result = subprocess.run(["./error.py"], check=True, capture_output = True)
    error = float(result.stdout)
    print(f"Error: {error}")
    return error

def objective(params):
    run_simulation(params)
    return compute_error()

initial_guess = [0.02]
bnds = [(0.005,0.02)]
tol = 1e-3

result = minimize(objective, initial_guess, bounds=bnds, method = 'Nelder-Mead', tol=tol)

print("Best parameters:", result.x)
print("Minimum error:", result.fun)

run_simulation(result.x)
run_line(f'./error.py --show')
