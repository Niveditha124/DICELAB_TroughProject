import numpy as np

# FRICTION (frictional operator accounting for shear stress between between turbidity current and bed)
def friction(field, par, dt):

    # (vel) calculates the norm of the velcocity vector at each point in the flow field, where (u) and (v) are the horizontal and vertical components
    vel = (( field.u ** 2 ) + (field.v ** 2)) ** 0.5
    # rs = max(vel,(par.g*par.h_min)^0.5)
    rs = np.maximum(vel, (par.g * par.h_min) ** 0.5)
    # rs = (field.u./max(vel,(par.g*par.h_min)^0.5)) OR (field.u ./ vel)
    rs = field.u / rs
    # vel = (vel>(par.g*par.h_min)^0.5)
    ls = (vel > ((par.g * par.h_min) ** 0.5)).astype(int)
    # ix = ls .* rs
    ix = ls * rs
    # direction vectors (ix) and (iy), repersent the horizontal and vertical components of the flow velocity
    ix = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.u / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))
    iy = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.v / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))
    # (h) calculates current flow depth/thickness 
    # assumes that (h) is invariant
    h = field.z_m - field.z_b
    # solve for U and K 
    # start with explicit solution
    vel_new = vel - (dt * par.alpha * (field.k_m / np.maximum(h, par.h_min)))
    K_new = np.maximum(0, (field.k_m / (1 - (par.alpha * (dt * (vel_new / np.maximum(h, par.h_min)))))))
    
    # iterate by looping 10 times on (vel) and (K) updates
    for i in range(10):
        vel_new = vel - (dt * par.alpha * (K_new / np.maximum(h, par.h_min)))
        K_new = np.maximum(0, (field.k_m / (1 - (par.alpha * (dt * (vel_new / np.maximum(h, par.h_min)))))))
    # redecompose velocity into x and y components and update field
    # (special assignment needed to avoid zeroing small velocities)
    returnValue = field
    returnValue.u = field.u + (ix * (vel_new - vel))
    returnValue.v = field.v + (iy * (vel_new - vel))
    returnValue.k_m = K_new
    
    return returnValue