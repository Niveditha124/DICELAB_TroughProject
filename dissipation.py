import numpy as np

def dissipation (field, par, dt):
    # DISSIPATION operator accounting for dissipation of K
    # supposes h&U&C are invariants

    # (vel) calculates the norm of the velcocity vector at each point in the flow field, where (u) and (v) are the horizontal and vertical components
    vel = ( field.u ** 2 + field.v ** 2 ) ** 0.5
    # (h) calculates current flow depth/thickness
    h = field.z_m - field.z_b
    # (Ri) calculates the explicit Richardson number, a dimensionless parameter used to predict turbulence within the flow
    Ri = par.R * par.g * field.c_m * h / np.maximum(vel ** 2,(par.g * par.h_min))
    # the np.maximum() function ensures Richardson number is non-negative, and negates the possibilty of undefined behavior
    Ri = np.maximum(Ri, 0) 
    # (ew) calculates the dimensionless coefficient governing the entrainment of ambient water into the current
    ew = 0.00153 / (0.0204 + Ri)
    # (Beta) calculates the dissipation of turbulent kinetic energy due to the ever-increasing values of the sediment entertainment coefficent (es) 
    # turbulennt energy is lost and dissipated due to it's energy being consumed in increasing the potential energy of the sediment being entrained
    Beta = (0.5 * ew * (1 - Ri - 2 * par.CfStar / par.alpha) + par.CfStar) / ((par.CfStar/par.alpha) ** 1.5)
    
    # solves for update of turbulent kientic energy (K), (assumes h is invariant)
    # start with explicit solution
    C1 = Beta / np.maximum(h, par.h_min)
    K_new = np.maximum(field.k_m - dt * (C1 * field.k_m ** 1.5), 0)
    # iterate by looping 10 times
    for i in range(10):
        dKdt_new = -C1 * K_new ** 1.5
        K_new = np.maximum(field.k_m + dt * dKdt_new, 0)

    # final update
    newfield = field
    newfield.k_m = K_new
    return newfield