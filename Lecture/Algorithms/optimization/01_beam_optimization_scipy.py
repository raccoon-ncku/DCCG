"""
Lecture 09: Architectural Optimization
Example 01: Single Objective Optimization of a Cantilever Beam using Scipy

Problem Statement:
    Design a rectangular cantilever beam to minimize its weight (cross-sectional area)
    while ensuring the tip deflection does not exceed a specified limit.

Variables:
    b (width): 0.01m to 0.5m
    h (height): 0.01m to 0.5m

Objective:
    Minimize Area = b * h

Constraint:
    Deflection <= Max_Deflection
    (F * L^3) / (3 * E * I) <= 0.005
    where I = (b * h^3) / 12
"""

import numpy as np
from scipy.optimize import minimize

def beam_optimization():
    print("--- Structural Beam Optimization (Scipy) ---")
    
    # --- 1. Define Constants ---
    L = 2.0         # Length of beam (meters)
    F = 5000.0      # Point load at tip (Newtons) ~500kg
    E = 210e9       # Young's Modulus for Steel (Pascals)
    MAX_DEF = 0.005 # Maximum allowed deflection (meters) = 5mm

    # --- 2. Define Objective Function ---
    # We want to minimize Volume/Area: Area = width * height
    def objective(x):
        b, h = x
        return b * h

    # --- 3. Define Constraint Function ---
    # Scipy constraints are defined as C(x) >= 0
    # We want: MAX_DEF - deflection >= 0
    def deflection_constraint(x):
        b, h = x
        
        # Avoid division by zero if optimizer tries 0 or negative
        if b <= 1e-6 or h <= 1e-6: 
            return -1.0
            
        # Moment of Inertia for rectangle
        I = (b * h**3) / 12
        
        # Deflection formula for cantilever with point load at end
        deflection = (F * L**3) / (3 * E * I)
        
        return MAX_DEF - deflection

    # --- 4. Optimization Setup ---
    # Initial guess [width, height]
    x0 = [0.1, 0.1] 

    # Bounds for variables (min, max) in meters
    bounds = [(0.01, 0.5), (0.01, 0.5)]

    # Define constraints dictionary
    cons = {'type': 'ineq', 'fun': deflection_constraint}

    # --- 5. Run Optimization ---
    print(f"Optimizing for Load: {F}N, Max Deflection: {MAX_DEF}m")
    solution = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

    # --- 6. Output Results ---
    if solution.success:
        b_opt, h_opt = solution.x
        I_opt = (b_opt * h_opt**3) / 12
        def_opt = (F * L**3) / (3 * E * I_opt)
        
        print("\n✅ Optimization Successful!")
        print(f"Optimal Width  (b): {b_opt*1000:.2f} mm")
        print(f"Optimal Height (h): {h_opt*1000:.2f} mm")
        print(f"Resulting Area    : {b_opt * h_opt:.6f} m^2")
        print(f"Actual Deflection : {def_opt*1000:.4f} mm (Limit: {MAX_DEF*1000} mm)")
        
        # Check if constraint is active (binding)
        if abs(def_opt - MAX_DEF) < 1e-6:
            print("Constraint is ACTIVE (Design is at the limit).")
        else:
            print("Constraint is INACTIVE (Design is stiffer than required).")
            
    else:
        print("\n❌ Optimization Failed:", solution.message)

if __name__ == "__main__":
    beam_optimization()
