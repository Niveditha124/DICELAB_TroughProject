import numpy as np

def friction(field, par, dt):

    # ix = (vel>(par.g*par.h_min)^0.5) .* (field.u./max(vel,(par.g*par.h_min)^0.5));
    vel = (( field.u ** 2 ) + (field.v ** 2)) ** 0.5
    rs = np.maximum(vel, (par.g * par.h_min) ** 0.5)
    rs = field.u / rs
    ls = (vel > ((par.g * par.h_min) ** 0.5)).astype(int)
    ix = ls * rs
    ix = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.u / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))
    iy = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.v / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))
    h = field.z_m - field.z_b
    vel_new = vel - (dt * par.alpha * (field.k_m / np.maximum(h, par.h_min)))
    K_new = np.maximum(0, (field.k_m / (1 - (par.alpha * (dt * (vel_new / np.maximum(h, par.h_min)))))))

    for i in range(10):
        vel_new = vel - (dt * par.alpha * (K_new / np.maximum(h, par.h_min)))
        K_new = np.maximum(0, (field.k_m / (1 - (par.alpha * (dt * (vel_new / np.maximum(h, par.h_min)))))))

    returnValue = field
    returnValue.u = field.u + (ix * (vel_new - vel))
    returnValue.v = field.v + (iy * (vel_new - vel))
    returnValue.k_m = K_new
    
    return returnValue