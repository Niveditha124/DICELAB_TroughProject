import numpy as np
from init1D import field
from weedmark_ext import weedmark_ext


# CLEAN UP WHEN FUNCTIONAL
class newfield:
    x = field.x
    y = field.y
    z_m = field.z_m
    c_m = field.c_m
    k_m = field.k_m
    z_b = field.z_b
    z_r = field.z_r
    u = field.u
    v = field.v
    Q_up = field.Q_up
    H_up = field.H_up
    U_up = field.U_up
    C_up = field.C_up
    K_up = field.K_up


# this is absolutely shagged :) <-- bruh
def mirror(field_x):
    # MIRROR extend field left and right using mirror symmetry
    m, n = field_x.x.shape
    dx = field_x.x[0, 1] - field_x.x[0, 0]
    # newfield.x = np.array([field_x.x[0, 0]-dx, field_x.x, field_x.x[0, n-1]+dx], dtype=object)
    # newfield.x = weedmark_ext(field_x.x)
    newfield.x = np.concatenate((field_x.x[:, 0][:, np.newaxis] - dx, field_x.x, field.x[:, -1][:, np.newaxis] + dx), axis=1)

    # newfield.y = np.array([field.y[0, 0], field.y, field.y[:, n - 1]], dtype=object)
    # newfield.y = weedmark_ext(field_x.y)
    newfield.y = np.concatenate((field_x.y[:, 0][:, np.newaxis], field_x.y, field_x.y[:, -1][:, np.newaxis]), axis=1)

    # newfield.z_m = np.array([field.z_m[0, 0], field.z_m, field.z_m[:, n - 1]], dtype=object)
    # newfield.z_m = weedmark_ext(field_x.z_m)
    # z_m is 1,204 exactly what it should be wrt matlab
    newfield.z_m = np.concatenate((field_x.z_m[:, 0][:, np.newaxis], field_x.z_m, field_x.z_m[:, -1][:, np.newaxis]), axis=1)

    # newfield.c_m = np.array([field.c_m[0, 0], field.c_m, field.c_m[:, n - 1]], dtype=object)
    # newfield.c_m = weedmark_ext(field_x.c_m)
    newfield.c_m = np.concatenate((field_x.c_m[:, 0][:, np.newaxis], field_x.c_m, field_x.c_m[:, -1][:, np.newaxis]), axis=1)

    # newfield.k_m = np.array([field.k_m[0, 0], field.k_m, field.k_m[:, n - 1]], dtype=object)
    # newfield.k_m = weedmark_ext(field_x.k_m)
    newfield.k_m = np.concatenate((field_x.k_m[:, 0][:, np.newaxis], field_x.k_m, field_x.k_m[:, -1][:, np.newaxis]), axis=1)

    # newfield.z_b = np.array([field.z_b[0, 0], field.z_b, field.z_b[:, n - 1]], dtype=object)
    # newfield.z_b = weedmark_ext(field_x.z_b)
    newfield.z_b = np.concatenate((field_x.z_b[:, 0][:, np.newaxis], field_x.z_b, field_x.z_b[:, -1][:, np.newaxis]), axis=1)

    # newfield.z_r = np.array([field.z_r[0, 0], field.z_r, field.z_r[:, n - 1]], dtype=object)
    # newfield.z_r = weedmark_ext(field_x.z_r)
    newfield.z_r = np.concatenate((field_x.z_r[:, 0][:, np.newaxis], field_x.z_r, field_x.z_r[:, -1][:, np.newaxis]), axis=1)

    # newfield.u = np.array([field.u[0, 0], field.u, field.u[:, n - 1]], dtype=object)
    # newfield.u = weedmark_ext(field_x.u)
    newfield.u = np.concatenate((field_x.u[:, 0][:, np.newaxis], field_x.u, field_x.u[:, -1][:, np.newaxis]), axis=1)

    # newfield.v = np.array([field.v[0, 0], field.v, field.v[:, n - 1]], dtype=object)
    # newfield.v = weedmark_ext(field_x.v)
    newfield.v = np.concatenate((field_x.v[:, 0][:, np.newaxis], field_x.v, field_x.v[:, -1][:, np.newaxis]), axis=1)
    
    # Not sure but screw it lets hard code it
    # Might need to change it later
    newfield.K_up = 0.05
    newfield.C_up = 0.0015

    return newfield
