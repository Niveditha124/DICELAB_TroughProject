import numpy as np
from init1D import field
from weedmark_ext import weedmark_ext


# CLEAN UP WHEN FUNCTIONAL
class newfield:
    # assigning properties from the original (field) object to the new class
    x = field.x 
    y = field.y
    s = field.s #shape of the x array
    z_m = field.z_m # elevation of the flow at a certain point??
    c_m = field.c_m # sediment concentration within the current
    k_m = field.k_m # turbulent kinetic energy within the flow
    z_b = field.z_b # sediment bed elevation??
    z_r = field.z_r # rigid channel bottom??
    # upstream inflow variables:
    u = field.u # velocity component along the horizontal direction
    v = field.v # velocity component along the vertical direction
    Q_up = field.Q_up # the volume transport rate of suspended sediment
    H_up = field.H_up # turbidity current depth/thickness
    U_up = field.U_up # flow velocity
    C_up = field.C_up # the layer-averaged volume concentration of suspended sediment carried by the turbidity current
    K_up = field.K_up # turbulent kinetic energy witihn the flow



def mirror(field):
    # MIRROR extend field left and right using mirror symmetry
    # creating new arrays by extending the original arrays using mirror symmetry
    m, n = field.x.shape # obtaining the shape of (field.x)
    dx = field.x[0, 1] - field.x[0, 0] # Calculating the grid spacing (dx)
    # newfield.x = np.array([field.x[0, 0]-dx, field.x, field.x[0, n-1]+dx], dtype=object)
    # newfield.x = weedmark_ext(field.x)
    newfield.x = np.concatenate((field.x[:, 0][:, np.newaxis] - dx, field.x, field.x[:, -1][:, np.newaxis] + dx), axis=1)

    # newfield.y = np.array([field.y[0, 0], field.y, field.y[:, n - 1]], dtype=object)
    # newfield.y = weedmark_ext(field.y)
    newfield.y = np.concatenate((field.y[:, 0][:, np.newaxis], field.y, field.y[:, -1][:, np.newaxis]), axis=1)

    # newfield.z_m = np.array([field.z_m[0, 0], field.z_m, field.z_m[:, n - 1]], dtype=object)
    # newfield.z_m = weedmark_ext(field.z_m)
    # z_m is 1,204 exactly what it should be wrt matlab
    newfield.z_m = np.concatenate((field.z_m[:, 0][:, np.newaxis], field.z_m, field.z_m[:, -1][:, np.newaxis]), axis=1)

    # newfield.c_m = np.array([field.c_m[0, 0], field.c_m, field.c_m[:, n - 1]], dtype=object)
    # newfield.c_m = weedmark_ext(field.c_m)
    newfield.c_m = np.concatenate((field.c_m[:, 0][:, np.newaxis], field.c_m, field.c_m[:, -1][:, np.newaxis]), axis=1)

    # newfield.k_m = np.array([field.k_m[0, 0], field.k_m, field.k_m[:, n - 1]], dtype=object)
    # newfield.k_m = weedmark_ext(field.k_m)
    newfield.k_m = np.concatenate((field.k_m[:, 0][:, np.newaxis], field.k_m, field.k_m[:, -1][:, np.newaxis]), axis=1)

    # newfield.z_b = np.array([field.z_b[0, 0], field.z_b, field.z_b[:, n - 1]], dtype=object)
    # newfield.z_b = weedmark_ext(field.z_b)
    newfield.z_b = np.concatenate((field.z_b[:, 0][:, np.newaxis], field.z_b, field.z_b[:, -1][:, np.newaxis]), axis=1)

    # newfield.z_r = np.array([field.z_r[0, 0], field.z_r, field.z_r[:, n - 1]], dtype=object)
    # newfield.z_r = weedmark_ext(field.z_r)
    newfield.z_r = np.concatenate((field.z_r[:, 0][:, np.newaxis], field.z_r, field.z_r[:, -1][:, np.newaxis]), axis=1)

    # newfield.u = np.array([field.u[0, 0], field.u, field.u[:, n - 1]], dtype=object)
    # newfield.u = weedmark_ext(field.u)
    newfield.u = np.concatenate((field.u[:, 0][:, np.newaxis], field.u, field.u[:, -1][:, np.newaxis]), axis=1)

    # newfield.v = np.array([field.v[0, 0], field.v, field.v[:, n - 1]], dtype=object)
    # newfield.v = weedmark_ext(field.v)
    newfield.v = np.concatenate((field.v[:, 0][:, np.newaxis], field.v, field.v[:, -1][:, np.newaxis]), axis=1)

    newfield.s = field.s
    
    # Assigning properties which are not extended
    newfield.Q_up = field.Q_up
    newfield.H_up = field.H_up
    newfield.U_up = field.U_up
    newfield.C_up = field.C_up
    newfield.K_up = field.K_up

    # Returning the extended field
    newfield.t = field.t

    return newfield
