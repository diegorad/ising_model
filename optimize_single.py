import subprocess
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar

def run_simulation(param):
    x = param

    subprocess.run([
        "./ising_model",
        f"--J_ij={{{x},0,0}}",
        f"--D_i={{0,0}}",
        "--out=monitor"
    ], check=True)

def compute_error():
    result = subprocess.run(["./error.py"], check=True, capture_output = True)
    error = float(result.stdout)
    print(error)
    return error

def objective(p):

    run_simulation(p)
    err = compute_error()

    print(f"p={p:.4f} error={err:.6f}")

    return err

result = minimize_scalar(objective, bounds=(0,3), method="bounded")

print("Best parameter:", result.x)
print("Minimum error:", result.fun)
