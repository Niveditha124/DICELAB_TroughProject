# ENTRAINMENT operator accounting for water entrainment at the top of turbidity current
# solved implicitly with backward Euler scheme (solution obtained
# interatively from the explicit estimate with a Newton scheme)
import numpy as np
import sys

def geomorphic(field, par, dt):
    # (vel) calculates the norm of the velcocity vector at each point in the flow field, where (u) and (v) are the horizontal and vertical components
    vel = (field.u ** 2 + field.v ** 2) ** 0.5

    # direction vectors (ix) and (iy), repersent the horizontal and vertical components of the flow velocity 
    ix = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.u / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))
    iy = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.v / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))

    # (h) calculates current flow depth/thickness
    h = field.z_m - field.z_b

    # (CH) calculates the amount of sediment being transported by the current 
    CH = h * field.c_m

    # (KH) calculates the turbulent kinetic energy within the current
    KH = h * field.k_m

    Ze5 = ((par.alpha*field.k_m) ** 0.5 / par.vs * par.Rp ** 0.6 * ((par.alpha * field.k_m) ** 0.5 / par.g / np.maximum(h, par.h_min)) ** 0.08) ** 5
    E = np.maximum((par.p * (1.3 * 10 ** -7)) * par.vs * Ze5 / (1 + (1.3 * 10 ** -7) / 0.3 * Ze5), 0)
    D = np.maximum(par.vs * par.r0 * field.c_m, 0)
    CH_new = np.maximum(CH + dt * (E - D), 0)
    h_new = np.maximum(h + dt / par.c_b * (E - D), 0)
    C_new = np.maximum(CH_new / np.maximum(h_new, par.h_min), 0)
    KH_new = KH - dt * 0.5 * par.R * par.g * h_new * (E - D)
    K_new = np.maximum(0, KH_new / np.maximum(h_new, par.h_min))
    
    for i in range(10):
    
        Ze5 = ((par.alpha*K_new) ** 0.5 / par.vs * par.Rp ** 0.6 * ((par.alpha * K_new) ** 0.5 / par.g / np.maximum(h_new, par.h_min)) ** 0.08) ** 5
        E = np.maximum((par.p * (1.3 * 10 ** -7)) * par.vs * Ze5 / (1 + (1.3 * 10 ** -7) / 0.3 * Ze5), 0)
        D = np.maximum(par.vs * par.r0 * C_new, 0)
        CH_new = np.maximum(CH + dt * (E - D), 0)
        h_new = np.maximum(h + dt / par.c_b * ((E - D)), 0)
        C_new = np.maximum(CH_new / np.maximum(h_new, par.h_min), 0)
        KH_new = KH - dt * 0.5 * par.R * par.g * h_new * (E - D)
        K_new = np.maximum(0, KH_new / np.maximum(h_new, par.h_min))


    # retrieve bed level change and impose limit. dzb is positive in case of deposition
    dzb = np.minimum((dt * ((D - E)*7) / par.c_b), ((field.z_m - field.z_b) * field.c_m / par.c_b)) #limited by deposition of all suspended sediments
    dzb = np.maximum(dzb, field.z_r - field.z_b) # limit by rigid bottom

    # retrieve all conservative variables from final bed level change
    h_new = h - dzb
    CH_new = np.minimum(np.maximum(CH - dzb * par.c_b, 0), h_new)
    KH_new = np.maximum(KH + 0.5 * par.R * par.g * h_new * par.c_b * dzb, 0)


    # note 1: implication of erosion/deposition on momentum transfer to/form the bed is neglected
    # note 2: should we forbid a net gain in K in case of deposition
    # K factor is an empirical measure of soil erodibility as affected by intrinsic soil properties
    # https://www.sciencedirect.com/topics/earth-and-planetary-sciences/revised-universal-soil-loss-equation\
   
    # final update
    newfield = field
    newfield.z_b = field.z_b + dzb
    newfield.c_m = np.minimum(np.maximum(CH_new / np.maximum(h_new, par.h_min), 0), 1) # do not change concentration where flow depth is about zero
    if (np.any(np.isnan(h_new))):
        print('h_new after has nans')
        sys.exit()
    indices = np.where(h_new < par.h_min)
    newfield.c_m[indices] = field.c_m[indices]

    newfield.k_m = np.maximum(KH_new / np.maximum(h_new, par.h_min), 0)

    return newfield
