import numpy as np


class fluxx:
    def __init__(self, name):
        self.z_mr = None
        self.z_br = None
        self.z_bl = None
        self.z_ml = None
        self.mu = None
        self.sigCross = None
        self.sig_r = None
        self.sig_l = None
        self.x = None
        self.q_m = None
        self.kh = None
        self.name = name

    def which(self, x):
        s = (1, 203)
        t = (1, 204)
        self.x = x
        self.x = self.x + 1
        self.q_m = np.zeros(s)
        self.sig_l = np.zeros(s)
        self.sig_r = np.zeros(s)
        self.sigCross = np.zeros(s)
        self.mu = np.zeros(t)
        self.kh = np.zeros(s)
        self.z_ml = np.zeros(s)
        self.z_mr = np.zeros(s)
        self.z_bl = np.zeros(s)
        self.z_br = np.zeros(s)


def fluxLHLL_2(name, field, grad, par, dt):
    # FLUXLHLL Approximate Riemann solver of Harten, Lax and Van Leer (1983) with lateralised momentum flux
    # extrapolations left and right (in face-centred variables):
    flux_x = fluxx(name)
    flux_y = fluxx(name)

    m, n = field.x.shape
    dx = field.x[0, 1] - field.x[0, 0]
    h_m = field.z_m - field.z_b
    h_ml = np.full((1, 203), 0.5)
    h_mr = np.full((1, 203), 0.5)
    h_ml = ((h_ml[:, np.arange(0, n - 1)] + h_m[:, np.arange(0, n - 1)]) * grad.dh_m[:, np.arange(0, n - 1)])
    h_mr = (h_m[:, np.arange(1, n)] - (h_mr[:, np.arange(0, n - 1)]) * grad.dh_m[:, np.arange(1, n)])

    mu_l = np.full((1, 203), 0.5)
    mu_r = np.full((1, 203), 0.5)
    mu = np.multiply(h_m, field.c_m)  # shape is 1,204
    mu_l = ((mu_l[:, np.arange(0, n - 1)] + mu[:, np.arange(0, n - 1)]) * grad.dmu[:, np.arange(0, n - 1)])
    mu_r = (mu[:, np.arange(1, n)] - (mu_r[:, np.arange(0, n - 1)]) * grad.dmu[:, np.arange(1, n)])

    kh_l = np.full((1, 203), 0.5)
    kh_r = np.full((1, 203), 0.5)
    kh = np.multiply(h_m, field.k_m) # shape is 1,204
    kh_l = ((kh_l[:, np.arange(0, n - 1)] + kh[:, np.arange(0, n - 1)]) * grad.dkh[:, np.arange(0, n - 1)])
    kh_r = (kh[:, np.arange(1, n)] - (kh_r[:, np.arange(0, n - 1)]) * grad.dkh[:, np.arange(1, n)])

    z_bl = np.full((1, 203), 0.5)
    z_br = np.full((1, 203), 0.5)
    z_bl = ((z_bl[:, np.arange(0, n - 1)] + field.z_b[:, np.arange(0, n - 1)]) * grad.dz_b[:, np.arange(0, n - 1)])
    z_br = (field.z_b[:, np.arange(1, n)] - (z_br[:, np.arange(0, n - 1)]) * grad.dz_b[:, np.arange(1, n)])

    # print(h_m.shape, field.u.shape)
    # print("h m", h_m.shape)
    # print("field u", field.u.shape)
    q_m = np.multiply(h_m, field.u)
    # print("qm", q_m.shape)
    # print("flux lhll", print(q_m.shape))
    # print("q_m size here ", q_m.shape)
    q_ml = np.full((1, 203), 0.5)
    q_mr = np.full((1, 203), 0.5)
    q_ml = ((q_ml[:, np.arange(0, n - 1)] + q_m[:, np.arange(0, n - 1)]) * grad.dqx_m[:, np.arange(0, n - 1)])
    q_mr = (q_m[:, np.arange(1, n)] - (q_mr[:, np.arange(0, n - 1)]) * grad.dqx_m[:, np.arange(1, n)])

    qy_m = np.multiply(h_m, field.v)
    qy_ml = np.full((1, 203), 0.5)
    qy_mr = np.full((1, 203), 0.5)
    qy_ml = ((qy_ml[:, np.arange(0, n - 1)] + qy_m[:, np.arange(0, n - 1)]) * grad.dqy_m[:, np.arange(0, n - 1)])
    qy_mr = (qy_m[:, np.arange(1, n)] - (qy_mr[:, np.arange(0, n - 1)]) * grad.dqy_m[:, np.arange(1, n)])

    # positivity constraint on mu and kh
    mu_l = np.amax(mu_l, 0)
    mu_r = np.amax(mu_r, 0)
    kh_l = np.amax(kh_l, 0)
    kh_r = np.amax(kh_r, 0)
    # retrieve primitive variables:
    # print("z_bl ", z_bl)
    # print("h_ml", h_ml)
    z_ml = z_bl + h_ml
    z_mr = z_br + h_mr

    # print(type(par.h_min))
    u_l = np.multiply((h_ml >= par.h_min), q_ml)
    u_l = np.divide(u_l, np.maximum(h_ml, par.h_min))
    u_r = np.multiply((h_mr >= par.h_min), q_mr) / np.maximum(h_mr, par.h_min)
    v_l = np.multiply((h_ml >= par.h_min), qy_ml) / np.maximum(h_ml, par.h_min)
    v_r = np.multiply((h_mr >= par.h_min), qy_mr) / np.maximum(h_mr, par.h_min)
    c_ml = np.multiply((h_ml >= par.h_min), mu_l) / np.maximum(h_ml, par.h_min)
    c_mr = np.multiply((h_mr >= par.h_min), mu_r) / np.maximum(h_mr, par.h_min)
    k_ml = np.multiply((h_ml >= par.h_min), kh_l) / np.maximum(h_ml, par.h_min)
    k_mr = np.multiply((h_mr >= par.h_min), kh_r) / np.maximum(h_mr, par.h_min)

    print('Printing...\n\n')
    print('h_ml: ', h_ml.shape, h_ml)
    print('u_l: ', u_l.shape, u_l)
    print('c_ml: ', c_ml.shape, c_ml)

    temp_u_l = u_l ** 2
    temp_h_ml = h_ml ** 2
    np.seterr(all='ignore')

    # left and right fluxes:
    # sig_l = np.multiply(h_ml, u_l ** 2) + 0.5 * par.g * par.R * (np.multiply(c_ml, h_ml ** 2))
    # sig_l = (h_ml * (u_l ** 2)) + 0.5 * par.g * par.R * (c_ml * (h_ml ** 2))
    print('Printing shit: \n')
    print('dt: ', dt)
    print('c_ml: ', c_ml[0][0])
    print('temp_h_ml: ', temp_h_ml[0][0])
    test = np.multiply(c_ml[0][0], temp_h_ml[0][0])
    print('test is: ', test)
    
    sig_l = (c_ml * temp_h_ml)
    
    sig_r = np.multiply(h_mr, u_r ** 2) + 0.5 * par.g * par.R * (np.multiply(c_mr, h_mr ** 2))
    # wavespeeds:
    h_l = np.amax(z_ml - z_bl, 0)

    SLl = np.amin(u_l - (np.multiply(par.g * par.R * h_l, c_ml)) ** 0.5, 0)
    SRl = np.amax(u_l + (np.multiply(par.g * par.R * h_l, c_ml)) ** 0.5, 0)
    h_r = np.amax(z_mr - z_br, 0)
    SLr = np.amin(u_r - (np.multiply(par.g * par.R * h_r, c_mr)) ** 0.5, 0)
    SRr = np.amax(u_r + (np.multiply(par.g * par.R * h_r, c_mr)) ** 0.5, 0)
    # extreme wave speeds:
    SL = np.amin(np.minimum(SLl, SLr), 0)
    SR = np.amax(np.maximum(SRl, SRr), 0)
    prod = 1.0 / np.maximum(SR - SL, (par.g * par.h_min) ** 0.5)
    # canonical HLL statement for discharge:
    q_m_star = np.multiply(
        (np.multiply(SR, q_ml) - np.multiply(SL, q_mr) + np.multiply(np.multiply(SL, SR), (z_mr - z_ml))), prod)

    # anti-emptying constraint:
    q_m_star_min = - h_mr * dx / dt
    q_m_star_max = h_ml * dx / dt

    q_m_star = np.minimum(np.maximum(q_m_star_min, q_m_star), q_m_star_max)
    # canonical HLL statement for momentum:
    sig_star = np.multiply(
        (np.multiply(SR, sig_l) - np.multiply(SL, sig_r) + np.multiply(np.multiply(SL, SR), (q_mr - q_ml))), prod)
    # momentum flux lateralisation:
    Cmhm_mean = 0.5 * (np.multiply(c_ml, h_ml) + np.multiply(c_mr, h_mr))
    sig_starl = sig_star - np.multiply(np.multiply(np.multiply(np.multiply(prod, SL), par.R) * par.g, Cmhm_mean),
                                       (z_br - z_bl))
    sig_starr = sig_star - np.multiply(np.multiply(np.multiply(np.multiply(prod, SR), par.R) * par.g, Cmhm_mean),
                                       (z_br - z_bl))
    # exceptions at internal reflecting boundaries:
    # SHOULD STILL CHECK THAT

    e = (np.logical_and(((par.g * z_ml + 0.5 * u_l ** 2) < par.g * z_br), (h_mr < par.h_min)).all())
    q_m_star = np.multiply((not e), q_m_star)
    sig_starl = np.multiply((not e), sig_starl) + np.multiply(e, (
            sig_l - np.multiply(np.multiply(np.multiply(2 * SL, SR), q_ml), prod)))
    sig_starr = np.multiply((not e), sig_starr)
    e = (np.logical_and(((par.g * z_mr + 0.5 * u_r ** 2) < par.g * z_ml), (h_ml < par.h_min)).all())
    q_m_star = np.multiply((not e), q_m_star)
    sig_starl = np.multiply((not e), sig_starl)
    sig_starr = np.multiply((not e), sig_starr) + np.multiply(e, (
            sig_r + np.multiply(np.multiply(np.multiply(2 * SL, SR), q_mr), prod)))

    # upwind momentum cross-flux:
    sigCross_star = np.multiply((np.multiply((q_m_star.all() > 0), v_l) + np.multiply((not (q_m_star.all() > 0)), v_r)),
                                q_m_star.all())
    # upwind concentration flux:
    mu_star = np.multiply((np.multiply((q_m_star.all() > 0), c_ml) + np.multiply((not (q_m_star.all() > 0)), c_mr)),
                          q_m_star.all())
    # upwind turbulent kinetic energy flux:
    kh_star = np.multiply((np.multiply((q_m_star.all() > 0), k_ml) + np.multiply((not (q_m_star.all() > 0)), k_mr)),
                          q_m_star.all())
    # anti-emptying constraint:
    mu_star_min = np.multiply(- h_mr, c_mr) * dx / dt
    mu_star_max = np.multiply(h_ml, c_ml) * dx / dt
    mu_star = np.minimum(np.maximum(mu_star_min, mu_star), mu_star_max)
    kh_star_min = np.multiply(- h_mr, k_mr) * dx / dt
    kh_star_max = np.multiply(h_ml, k_ml) * dx / dt
    kh_star = np.minimum(np.maximum(kh_star_min, kh_star), kh_star_max)

    flux_x.q_m = q_m_star
    flux_x.sig_l = sig_starl
    flux_x.sig_r = sig_starr
    flux_x.sigCross = sigCross_star
    flux_x.mu = mu_star
    flux_x.kh = kh_star
    flux_x.z_ml = z_ml
    flux_x.z_mr = z_mr
    flux_x.z_bl = z_bl
    flux_x.z_br = z_br

    flux_y.q_m = np.zeros((2, field.x.shape[1]-2))
    flux_y.sig_l = sig_starl
    flux_y.sig_r = sig_starr
    flux_y.sigCross = np.zeros((2, len(field.x)))
    flux_y.mu = np.zeros((2, len(field.x)))
    flux_y.kh = np.zeros((2, len(field.x)))
    flux_y.z_br = np.zeros((2, len(field.x)))
    flux_y.z_bl = np.zeros((2, len(field.x)))

    if name == 'x':
        return flux_x
    else:
        return flux_y
