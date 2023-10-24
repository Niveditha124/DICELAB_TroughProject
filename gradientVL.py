import numpy as np
import sys
from init1D import field
from weedmark_ext import weedmark_ext

# class definition for storing gradients
class grad:
    dh_m = np.zeros(field.x.shape)
    dmu = np.zeros(field.x.shape)
    dkh = np.zeros(field.x.shape)
    dz_b = np.zeros(field.x.shape)
    dqx_m = np.zeros(field.x.shape)
    dqy_m = np.zeros(field.x.shape)

# calculating the "minmod" of two input values (a) and (b)
def minmod(a, b):
    ab = np.multiply(a, b)
    c = np.multiply(ab > 0, (np.multiply(abs(a) < abs(b), a) + np.multiply(~(abs(a) < abs(b)), b)))
    return c

# GRADIENTVL Van Leer slope limiter
def gradientVL(field=None, par=None, o=0):
    # o = 0
    if o == 1:
       # reseting gradient variables back to to the condition (o = 1) 
        grad.dh_m = np.zeros(field.x.shape)
        grad.dmu = np.zeros(field.x.shape)
        grad.dkh = np.zeros(field.x.shape)
        grad.dz_b = np.zeros(field.x.shape)
        grad.dqx_m = np.zeros(field.x.shape)
        grad.dqy_m = np.zeros(field.x.shape)

    else:
        m, n = field.x.shape
        # obtain gradient variables:
        h_m = field.z_m - field.z_b
        z_b = field.z_b
        qx_m = np.multiply(h_m, field.u)
        qy_m = np.multiply(h_m, field.v)
        mu = np.multiply(h_m, field.c_m)
        kh = np.multiply(h_m, field.k_m)
        # extend variables left and right:
        h_me = weedmark_ext(h_m)
        mu_e = weedmark_ext(mu)
        kh_e = weedmark_ext(kh)
        z_be = weedmark_ext(z_b)
        qx_me = weedmark_ext(qx_m)
        qy_me = weedmark_ext(qy_m)
        # matrix multiplication
        grad.dh_m = minmod(h_me[:, np.arange(2, n + 2)] - h_me[:, np.arange(1, n + 1)],
                           h_me[:, np.arange(1, n + 1)] - h_me[:, np.arange(0, n)])
        grad.dmu = minmod(mu_e[:, np.arange(2, n + 2)] - mu_e[:, np.arange(1, n + 1)],
                          mu_e[:, np.arange(1, n + 1)] - mu_e[:, np.arange(0, n)])
        grad.dkh = minmod(kh_e[:, np.arange(2, n + 2)] - kh_e[:, np.arange(1, n + 1)],
                          kh_e[:, np.arange(1, n + 1)] - kh_e[:, np.arange(0, n)])
        grad.dz_b = minmod(z_be[:, np.arange(2, n + 2)] - z_be[:, np.arange(1, n + 1)],
                           z_be[:, np.arange(1, n + 1)] - z_be[:, np.arange(0, n)])
        grad.dqx_m = minmod(qx_me[:, np.arange(2, n + 2)] - qx_me[:, np.arange(1, n + 1)],
                            qx_me[:, np.arange(1, n + 1)] - qx_me[:, np.arange(0, n)])
        grad.dqy_m = minmod(qy_me[:, np.arange(2, n + 2)] - qy_me[:, np.arange(1, n + 1)],
                            qy_me[:, np.arange(1, n + 1)] - qy_me[:, np.arange(0, n)])

    return grad
