import numpy as np

def timestep(field, par):
    # TIMESTEP compute time step according to the Courant condition
    # cel = ( par.g * max( field.z_m - field.z_b , par.h_min ) ).^0.5;
    # cel = (np.multiply(par.R * par.g * field.c_m, np.maximum(field.z_m - field.z_b, par.h_min)) ** 0.5)
    
    temp = np.maximum(field.z_m - field.z_b, par.h_min)
    temp2 = par.R * par.g 
    
    cel = np.sqrt(temp * temp2 * field.c_m)
    vel = np.sqrt(field.u**2 + field.v**2)

    sm = vel + cel
    speed_max = np.max(sm)
        #maximum of a maximum = get max of an array
    dx = field.x[0, 1] - field.x[0, 0]
    dy = dx
    dl = min(dx, dy)

    if speed_max == 0:
        dt = 1
    else:
        dt = (par.courant * dl) / speed_max
        # speed max is zero, then all the arrays shit the bed.

    return dt
