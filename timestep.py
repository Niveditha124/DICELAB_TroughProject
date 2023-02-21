import numpy as np


def timestep(field, par):
    # TIMESTEP compute time step according to the Courant condition
    # cel = ( par.g * max( field.z_m - field.z_b , par.h_min ) ).^0.5;

    cel = (np.multiply(par.R * par.g * field.c_m, np.maximum(field.z_m - field.z_b, par.h_min))) ** 0.5
    vel = (field.u ** 2 + field.v ** 2) ** 0.5
    # print(cel)
    # print(vel)
    speed_max = np.amax(np.amax(vel + cel))
    # print(speed_max)
    dx = field.x[0, 1] - field.x[0, 0]
    # dy = field.y(2,1) - field.y(1,1);
    dy = dx
    dl = min(dx, dy)
    # dt = par.courant * dl / speed_max
    np.seterr(divide='ignore', invalid='ignore')
    dt = np.divide((par.courant * dl), speed_max)
    return dt
