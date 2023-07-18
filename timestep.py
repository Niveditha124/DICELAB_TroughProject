import numpy as np
import sys

def timestep(field, par):
    # TIMESTEP compute time step according to the Courant condition
    # cel = ( par.g * max( field.z_m - field.z_b , par.h_min ) ).^0.5;
    # cel = (np.multiply(par.R * par.g * field.c_m, np.maximum(field.z_m - field.z_b, par.h_min)) ** 0.5)
    
    temp = np.maximum(field.z_m - field.z_b, par.h_min)
    temp2 = par.R * par.g 
    
    cel = np.sqrt(temp * temp2 * field.c_m)
    

    # print('par.R: ', par.R)
    # print('par.g: ', par.g)

    # print('field.z_m: ', field.z_m)
    # print('field.z_b: ', field.z_b)
    # print('par.h_min: ', par.h_min)

    # vel = (field.u ** 2 + field.v ** 2) ** 0.5
    vel = np.sqrt(field.u**2 + field.v**2)

    # print(vel)
    sm = vel + cel
    speed_max = np.max(sm)
        #maximum of a maximum = get max of an array
    dx = field.x[0, 1] - field.x[0, 0]
    # dy = field.y(2,1) - field.y(1,1);
    dy = dx
    dl = min(dx, dy)
    # dt = par.courant * dl / speed_max
    # np.seterr(divide='ignore', invalid='ignore')
    # print(speed_max)
    # print('par.courant: ', par.courant)
    # print('dl: ', dl)
    if speed_max == 0:
        dt = 1
    else:
        dt = (par.courant * dl) / speed_max
        # print(par.courant)
        # print(dl)

        # speed max is zero, then all the arrays shit the bed.

    return dt
