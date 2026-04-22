#!/usr/bin/env python3

import subprocess
import numpy as np
from scipy.optimize import minimize, basinhopping
import sys

#PARAMETERS-------------

column = None
ext_val = None

#------------------------

#Argument parsing
while sys.argv:
    if sys.argv[0] == "--column":
        column = int(sys.argv[1])
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--ext_val":
        ext_val = float(sys.argv[1])
        sys.argv = sys.argv[1:]
        
    sys.argv = sys.argv[1:]

def run_line(line, capture_output=False):
        comm = line.split(" ")    
        result = subprocess.run(comm, check=True, capture_output=capture_output)
        return result

def f(x):
    y = -0.177599-2.15532*x
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
    
    y = f(ext_val)
    
#    run_line(f"./fieldgen.py --steps {y} --range 6")
    run_line(f'./ising_model --J_ij={{{ext_val},4.6,{x}}} --D_i={{{y},0.0}} --init=sat --out=none')
#    run_line(f'./sweep.sh {x} {y}')
#    run_line(f'./average.py')

def compute_error():
	error_proc = "./error.py --column {i} --mode half_loop --trim 100 --norm tail 20 --save"	
	
    error = []
    if column == None:
        for i in [1, 2]:
            result = run_line(f"./error.py --column {i} --mode half_loop --trim 100 --norm tail 20 --save", capture_output = True)
            error.append(float(result.stdout))
        
        print(f"Error = {{1: {error[0]},  2: {error[1]}}}")
        error = np.mean(error)
        print(f"Mean error = {error}")
    else:
        result = run_line(f"./error.py --column {column} --mode half_loop --trim 100 --norm tail 20 --save", capture_output = True)
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

initial_guess = [-2]
bnds = [(-4, 0)]
tol = 1e-2

normalized_guess = [transform(a, b) for a, b in zip(initial_guess, bnds)]

#result = minimize(objective, initial_guess, bounds=bnds, method = 'Nelder-Mead', tol=tol)
result = minimize(objective_scaled, normalized_guess, bounds=[(0, 1)], method = 'Nelder-Mead', tol=tol)

best_params = [detransform(a, b) for a, b in zip(result.x, bnds)]

print("Best parameters:", *best_params)
print("Minimum error:", result.fun)

#run_simulation(best_params)
#if column == None:
#    run_line(f'./error.py --column 1 --show')
#    run_line(f'./error.py --column 2 --show')
#else:
#    run_line(f'./error.py --column {column} --show')
