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

def transform(initial_guess, bnds):
    a = (initial_guess-bnds[0])/(bnds[1] - bnds[0])
    return a

def detransform(x, bnds):
    a = (bnds[1]-bnds[0])*x+bnds[0]
    return a

def run_simulation(params):
    if(len(params)==1):
        x = params[0]
        y = f(x)
    else:
        x, y = params
    
    print(f"\nRunning simulation with x={[round(float(par),6) for par in params]}")
    
#    run_line(f"./fieldgen.py --steps {y} --range 6")
    run_line(f'./ising_model --J_ij={{0.234,0.0,0.0}} --D_i={{{x},0.0}} --out=monitor')
#    run_line(f'./sweep.sh {x} {y}')
#    run_line(f'./average.py')

def compute_error():
    error = []
    if column == None:
        for i in [1, 2]:
            result = subprocess.run(["./error_2.py","--column", f"{i}"], check=True, capture_output = True)
            error.append(float(result.stdout))
        
        print(f"Error = {{1: {error[0]},  2: {error[1]}}}")
        error = np.mean(error)
        print(f"Mean error = {error}")
    else:
        result = subprocess.run(["./error_2.py","--column", f"{column}"], check=True, capture_output = True)
        error = float(result.stdout)
        print(f"Error = {error}")    
    
    return error

def objective(params):
    run_simulation(params)
    return compute_error()
    
def objective_scaled(params):
	denormalized_params = [detransform(a, b) for a, b in zip(params, bnds)]
#	print(f"{params}: {denormalized_params}")
	run_simulation(denormalized_params)
	return compute_error()

initial_guess = [0.01]
bnds = [(0, 0.2)]
tol = 1e-2

normalized_guess = [transform(a, b) for a, b in zip(initial_guess, bnds)]

#result = minimize(objective, initial_guess, bounds=bnds, method = 'Nelder-Mead', tol=tol)
result = minimize(objective_scaled, normalized_guess, bounds=[(0, 1)], method = 'Nelder-Mead', tol=tol)

best_params = [detransform(a, b) for a, b in zip(result.x, bnds)]

print("Best parameters:", best_params)
print("Minimum error:", result.fun)

run_simulation(best_params)
if column == None:
    run_line(f'./error.py --column 1 --show')
    run_line(f'./error.py --column 2 --show')
else:
    run_line(f'./error.py --column {column} --show')
