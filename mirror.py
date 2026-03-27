import numpy as np
from init1D import field
from weedmark_ext import weedmark_ext


# CLEAN UP WHEN FUNCTIONAL
class newfield:
    # assigning properties from the original (field) object to the new class
    x = field.x 
    y = field.y
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
    s = field.s
    nu = field.nu
    nu2d = field.nu2d
    f = field.f
    h = field.h
    ls = field.ls
    rs = field.rs



def mirror(field):
    # MIRROR extend field left and right using mirror symmetry
    # creating new arrays by extending the original arrays using mirror symmetry
    m, n = field.x.shape # obtaining the shape of (field.x)
    dx = field.x[0, 1] - field.x[0, 0] # Calculating the grid spacing (dx)

    newfield.x = np.concatenate((field.x[:, 0][:, np.newaxis] - dx, field.x, field.x[:, -1][:, np.newaxis] + dx), axis=1)
    newfield.y = np.concatenate((field.y[:, 0][:, np.newaxis], field.y, field.y[:, -1][:, np.newaxis]), axis=1)
    newfield.z_m = np.concatenate((field.z_m[:, 0][:, np.newaxis], field.z_m, field.z_m[:, -1][:, np.newaxis]), axis=1)
    newfield.c_m = np.concatenate((field.c_m[:, 0][:, np.newaxis], field.c_m, field.c_m[:, -1][:, np.newaxis]), axis=1)
    newfield.k_m = np.concatenate((field.k_m[:, 0][:, np.newaxis], field.k_m, field.k_m[:, -1][:, np.newaxis]), axis=1)
    newfield.z_b = np.concatenate((field.z_b[:, 0][:, np.newaxis], field.z_b, field.z_b[:, -1][:, np.newaxis]), axis=1)
    newfield.z_r = np.concatenate((field.z_r[:, 0][:, np.newaxis], field.z_r, field.z_r[:, -1][:, np.newaxis]), axis=1)
    newfield.u = np.concatenate((field.u[:, 0][:, np.newaxis], field.u, field.u[:, -1][:, np.newaxis]), axis=1)
    newfield.v = np.concatenate((field.v[:, 0][:, np.newaxis], field.v, field.v[:, -1][:, np.newaxis]), axis=1)
    
    newfield.s = field.s
    newfield.nu = field.nu 
    newfield.nu2d = field.nu2d
    newfield.f = field.f
    newfield.h = field.h

    ########################## empty variables for testing
    newfield.ls = field.ls
    newfield.rs = field.rs
    ############################


    # Assigning properties which are not extended
    newfield.Q_up = field.Q_up
    newfield.H_up = field.H_up
    newfield.U_up = field.U_up
    newfield.C_up = field.C_up
    newfield.K_up = field.K_up

    # Returning the extended field
    newfield.t = field.t

    return newfield
