#!/usr/bin/env python3

import subprocess
import numpy as np
from scipy.optimize import minimize, basinhopping
import sys

#PARAMETERS-------------

column = None
ext_val = None
index = None

#------------------------

#Argument parsing
while sys.argv:
    if sys.argv[0] == "--column":
        column = int(sys.argv[1])
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--ext_val":
        ext_val = float(sys.argv[1])
        sys.argv = sys.argv[1:]
    if sys.argv[0] == "--index":
        index = int(sys.argv[1])
        sys.argv = sys.argv[1:]
        
        
    sys.argv = sys.argv[1:]

def run_line(line, capture_output=False, stdout=None):
        comm = line.split(" ")    
        result = subprocess.run(comm, check=True, capture_output=capture_output, stdout=stdout)
        return result

def f(x):
    y = -0.528198-2.1852*x
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
    
#    aux_val = f(ext_val)
#    print(ext_val, aux_val)
    
#    run_line(f"./fieldgen.py --steps {y} --range 6")
    run_line(f'./ising_model --J_ij={{{ext_val},4.6,0}} --D_i={{{x},0.0}} --init=sat --out=none')
    #Bin points
    with open("output.tmp", "w") as file:
    	run_line(f'./average.py --mode bin --bin_size 0.01 --trim 250', stdout=file)
    run_line(f'mv output.tmp output.txt')

	#Run sweep
#    run_line(f'./sweep.sh {index} {x} {y} {ext_val}')

def compute_error():
#    error_proc = "./error.py --column {i} --mode half_loop --norm tail 10 --save"	
	
    error = []
    if column == None:
        for i in [1, 2]:
            result = run_line(f"./error.py --column {i} --mode half_loop --norm tail 10 --savefig", capture_output = True)
            error.append(float(result.stdout))
        
        print(f"Error = {{1: {error[0]},  2: {error[1]}}}")
        error = np.mean(error)
        print(f"Mean error = {error}")
    else:
        result = run_line(f"./error.py --dir data_Fe --mode half_loop --norm_sim False --scale_sim 0.0016 --norm_data False --scale_data 5.86", capture_output = True)
#        result = run_line(f"./error_zeros.py --index {index}", capture_output = True)
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

initial_guess = [0]
bnds = [(-5, 0)]
tol = 1e-2

normalized_guess = [transform(a, b) for a, b in zip(initial_guess, bnds)]

#result = minimize(objective, initial_guess, bounds=bnds, method = 'Nelder-Mead', tol=tol)
result = minimize(objective_scaled, normalized_guess, bounds=[(0, 1)], method = 'Nelder-Mead', tol=tol)

best_params = [detransform(a, b) for a, b in zip(result.x, bnds)]

print("Best parameters:", *best_params)
print("Minimum error:", result.fun)

with open("best_parameters.txt", "w") as f:
  print(*best_params, result.fun, file=f)

#run_simulation(best_params)
#if column == None:
#    run_line(f'./error.py --column 1 --show')
#    run_line(f'./error.py --column 2 --show')
#else:
#    run_line(f'./error.py --column {column} --show')
