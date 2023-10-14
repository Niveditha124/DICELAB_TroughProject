import numpy as np
# ENTRAINMENT operator accounting for water entrainment at the top of turbidity current
# solved implicitly with a backward Euler scheme (solution obtained
# iteratively from the explicit estimate with a Newton scheme)

def entrainment(field, par, dt):
    # (vel) calculates the norm of the velcocity vector at each point in the flow field, where (u) and (v) are the horizontal and vertical components
    vel = ((field.u ** 2) + (field.v ** 2)) ** 0.5
    # direction vectors (ix) and (iy), repersent the horizontal and vertical components of the flow velocity
    ix = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.u / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))
    iy = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.v / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))


    # (h) calculates current flow depth/thickness
    h = field.z_m - field.z_b


    # conserved momentum, represents the quantity of motion in the flow
    MOM = h * vel # total momentum 
    momx = h * field.u # horizontal momentum component
    momy = h * field.v # vertical momentum component

    # (SS) conserved suspended sediments, total amount of suspended sediments within the flow as the current moves downhill
    SS = h * field.c_m

    # (Ri) calculates the explicit Richardson number, a dimensionless parameter used to predict turbulence within the flow
    Ri = par.R * par.g * field.c_m * h / np.maximum(vel**2, (par.g*par.h_min))
    Ri = par.R * par.g * field.c_m * h / np.maximum(vel**2, par.g * par.h_min)
    # VEL is fine, so it must be c_m
    # the np.maximum() function ensures Richardson number is non-negative, and negates the possibilty of undefined behavior
    Ri = np.maximum(Ri, 0)
    # acc derp af way of finding this
    for x in Ri:
        for i in x:
            if i < 0:
                print('negative Ri')

    # SOLVE FOR H_NEW (Iterative Newton Scheme, loop 10 times)
    # start with explicit estimate
    h_new = h + dt * (0.00153/(0.0204 + Ri)) * vel
    C1 = 0.00153 * MOM ** 3
    C2 = 0.0204 * MOM ** 2
    C3 = par.R * par.g * SS

    # iterate 10 times with Newton scheme
    for i in range(10):
        np.seterr(divide='ignore', invalid='ignore')
        dhdt_new = C1 / (np.maximum(h_new, par.h_min) * (C2+C3*np.maximum(h_new, par.h_min)**2))
        h_new = h + dt * dhdt_new
        np.seterr(divide='raise', invalid='raise')

    h_new[np.isnan(h_new)] = 0
    h_new = np.maximum(h, h_new)
    # retreive other variables from invariants
    c_new = np.maximum((SS/(np.maximum(h_new, par.h_min))), 0)
    u_new = momx / np.maximum(h_new, par.h_min)
    v_new = momy / np.maximum(h_new, par.h_min)
    vel_new = (u_new ** 2 + v_new ** 2)**0.5
    dhdt_new = (1 / dt) * (h_new - h)

    # solves for update of turbulent kientic energy (K)
    kh_new = np.maximum(h * field.k_m + dt * 0.5 * dhdt_new * (vel_new ** 2 - par.R * par.g * SS), 0)
    k_new = kh_new / np.maximum(h_new, par.h_min)

    # final update
    newfield = field
    newfield.u = u_new
    newfield.v = v_new
    newfield.z_m = field.z_b + h_new
    newfield.c_m = c_new
    newfield.k_m = k_new
    return newfield
