import numpy as np


def entrainment(field, par, dt):
    # normal and directional vectors
    vel = ((field.u ** 2) + (field.v ** 2)) ** 0.5

    ix = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.u / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))
    iy = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.v / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))


    # layer depth
    h = field.z_m - field.z_b


    # conserved momentum
    MOM = h * vel
    momx = h * field.u
    momy = h * field.v

    # conserved suspended sediments
    SS = h * field.c_m

    # explicit Richardson number
    Ri = par.R * par.g * field.c_m * h / np.maximum(vel**2, (par.g*par.h_min))
    Ri = par.R * par.g * field.c_m * h / np.maximum(vel**2, par.g * par.h_min)
    # VEL is fine, so it must be c_m
    Ri = np.maximum(Ri, 0)
    # acc derp af way of finding this
    for x in Ri:
        for i in x:
            if i < 0:
                print('negative Ri')

    h_new = h + dt * (0.00153/(0.0204 + Ri)) * vel


    C1 = 0.00153 * MOM ** 3
    C2 = 0.0204 * MOM ** 2
    C3 = par.R * par.g * SS


    for i in range(10):
        np.seterr(divide='ignore', invalid='ignore')
        dhdt_new = C1 / (np.maximum(h_new, par.h_min) * (C2+C3*np.maximum(h_new, par.h_min)**2))
        h_new = h + dt * dhdt_new
        np.seterr(divide='raise', invalid='raise')

    h_new[np.isnan(h_new)] = 0
    h_new = np.maximum(h, h_new)
    #retreive other variables from invariants
    c_new = np.maximum((SS/(np.maximum(h_new, par.h_min))), 0)
    u_new = momx / np.maximum(h_new, par.h_min)
    v_new = momy / np.maximum(h_new, par.h_min)
    vel_new = (u_new ** 2 + v_new ** 2)**0.5
    dhdt_new = (1 / dt) * (h_new - h)

     #solve for update K
    kh_new = np.maximum(h * field.k_m + dt * 0.5 * dhdt_new * (vel_new ** 2 - par.R * par.g * SS), 0)
    k_new = kh_new / np.maximum(h_new, par.h_min)

    #final update
    newfield = field
    newfield.u = u_new
    newfield.v = v_new
    newfield.z_m = field.z_b + h_new
    newfield.c_m = c_new
    newfield.k_m = k_new
    return newfield
