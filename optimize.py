#!/usr/bin/env python3

import subprocess
import numpy as np
from scipy.optimize import minimize, basinhopping
import sys

#PARAMETERS-------------

column = None

#------------------------

#Argument parsing
while sys.argv:
    if sys.argv[0] == "--column":
        column = int(sys.argv[1])
        sys.argv = sys.argv[1:]
        
    sys.argv = sys.argv[1:]

def run_line(line):
        comm = line.split(" ")    
        subprocess.run(comm, check=True)

def f(x):
    y = 0.105798-3.3437*x
    return y

def run_simulation(params):
    if(len(params)==1):
        x = params[0]
        y = f(x)
    else:
        x, y = params
    
    print(f"\nRunning simulation with x={round(x,3)}")
    
#    run_line(f"./fieldgen.py --rate {y} --range 2.5")
    run_line(f'./ising_model --J_ij={{{x},0.0,0.0}} --D_i={{{y},0.0}} --out=monitor')
#    run_line(f'./sweep.sh {x} {y}')
#    run_line(f'./average.py')

def compute_error():
    error = []
    if column == None:
        for i in [1, 2]:
            result = subprocess.run(["./error.py","--column", f"{i}"], check=True, capture_output = True)
            error.append(float(result.stdout))
        
        print(f"Error = {{1: {error[0]},  2: {error[1]}}}")
        error = np.mean(error)
        print(f"Mean error = {error}")
    else:
        result = subprocess.run(["./error.py","--column", f"{column}"], check=True, capture_output = True)
        error = float(result.stdout)
        print(f"Error = {error}")    
    
    return error

def objective(params):
    run_simulation(params)
    return compute_error()

initial_guess = [0.0734375, -0.31816406]
bnds = [(0,0.2), (-0.5, 0)]
tol = 1e-2

result = minimize(objective, initial_guess, bounds=bnds, method = 'Nelder-Mead', tol=tol)

print("Best parameters:", result.x)
print("Minimum error:", result.fun)

run_simulation(result.x)
if column == None:
    run_line(f'./error.py --column 1 --show')
    run_line(f'./error.py --column 2 --show')
else:
    run_line(f'./error.py --column {column} --show')
