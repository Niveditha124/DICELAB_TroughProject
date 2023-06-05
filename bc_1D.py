from init1D import field


def bc_1D(flux=None, field=None, par=None):
    # impose upstream boundary condition in geoflood1D

    bcflux = flux
    # correct fluxes at upstream inflow section
    s = 0.0 * field.Q_up

    bcflux.q_m[0][0] = field.Q_up
    # bcflux.g_m(1) = s;  (apparently no change)
    bcflux.sig_r[0][0] = field.H_up * field.U_up ** 2 + 0.5 * par.g * par.R * (field.C_up * field.H_up ** 2)
    bcflux.mu[0][0] = field.C_up * field.Q_up
    bcflux.kh[0][0] = field.K_up * field.Q_up

    # K_up hardcoded in mirror.py
    
    return bcflux
