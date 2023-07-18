import numpy as np
import sys


class fluxx:
    s = (1, 203)
    t = (1, 204)
    q_m = np.zeros(s)
    sig_l = np.zeros(s)
    sig_r = np.zeros(s)
    sigCross = np.zeros(s)
    mu = np.zeros(t)
    kh = np.zeros(s)
    z_ml = np.zeros(s)
    z_mr = np.zeros(s)
    z_bl = np.zeros(s)
    z_br = np.zeros(s)
    
    def __init__ (self, q_m, sig_l, sig_r, sigCross, mu, kh, z_ml, z_mr, z_bl, z_br):
        self.q_m = q_m
        self.sig_l = sig_l
        self.sig_r = sig_r
        self.sigCross = sigCross
        self.mu = mu
        self.kh = kh
        self.z_ml = z_ml
        self.z_mr = z_mr
        self.z_bl = z_bl
        self.z_br = z_br













def fluxLHLL(field=None, grad=None, par=None, dt=None):
    # FLUXLHLL Approximate Riemann solver of Harten, Lax and Van Leer (1983) with lateralised momentum flux
    # extrapolations left and right (in face-centred variables):


    m, n = field.x.shape
    dx = field.x[0, 1] - field.x[0, 0]
    h_m = field.z_m - field.z_b

    h_ml = np.full((1, 203), 0.5)
    h_mr = np.full((1, 203), 0.5)
    # h_ml = ((h_ml[:, np.arange(0, n - 1)] + h_m[:, np.arange(0, n - 1)]) * grad.dh_m[:, np.arange(0, n - 1)])
    h_ml = h_m[:, :n-1] + 0.5 * grad.dh_m[:, :n-1]
    # print('h_ml')
    # print(h_ml)

    # h_mr = (h_m[:, np.arange(1, n)] - (h_mr[:, np.arange(0, n - 1)]) * grad.dh_m[:, np.arange(1, n)])
    h_mr = h_m[:, 1:] - 0.5 * grad.dh_m[:, 1:]

    mu_l = np.full((1, 203), 0.5)
    mu_r = np.full((1, 203), 0.5)
    mu = np.multiply(h_m, field.c_m)  # shape is 1,204
    # mu_l = ((mu_l[:, np.arange(0, n - 1)] + mu[:, np.arange(0, n - 1)]) * grad.dmu[:, np.arange(0, n - 1)])
    mu_l = mu[:, :n-1] + 0.5 * grad.dmu[:, :n-1]
    # mu_r = (mu[:, np.arange(1, n)] - (mu_r[:, np.arange(0, n - 1)]) * grad.dmu[:, np.arange(1, n)])
    mu_r = mu[:, 1:n] - 0.5 * grad.dmu[:, 1:n]
    kh = h_m * field.k_m
    kh_l = np.full((1, 203), 0.5)
    kh_r = np.full((1, 203), 0.5)
    # kh_l = ((kh_l[:, np.arange(0, n - 1)] + kh[:, np.arange(0, n - 1)]) * grad.dkh[:, np.arange(0, n - 1)])
    kh_l = kh[:, :n-1] + 0.5 * grad.dkh[:, :n-1]

    # kh_r = (kh[:, np.arange(1, n)] - (kh_r[:, np.arange(0, n - 1)]) * grad.dkh[:, np.arange(1, n)])
    kh_r = kh[:, 1:n] - 0.5 * grad.dkh[:, 1:n]

    # z_bl = np.full((1, 203), 0.5)
    s = (1, 203)
    z_bl = np.zeros(s)
    z_br = np.full((1, 203), 0.5)
    np.set_printoptions(suppress=True, formatter={'float': '{:0.6f}'.format})
    # z_bl = ((z_bl[:, np.arange(0, n - 1)] + field.z_b[:, np.arange(0, n - 1)]) * grad.dz_b[:, np.arange(0, n - 1)])
    z_bl = field.z_b[:, 0:n-1] + 0.5 * grad.dz_b[:, 0:n-1]
    
    # z_br = (field.z_b[:, np.arange(1, n)] - (z_br[:, np.arange(0, n - 1)]) * grad.dz_b[:, np.arange(1, n)])
    z_br = field.z_b[:, 1:] - 0.5 * grad.dz_b[:, 1:]

    q_m = np.multiply(h_m, field.u)
    # q_ml = np.full((1, 203), 0.5)
    # q_mr = np.full((1, 203), 0.5)
    # q_ml = ((q_ml[:, np.arange(0, n - 1)] + q_m[:, np.arange(0, n - 1)]) * grad.dqx_m[:, np.arange(0, n - 1)])
    # q_mr = (q_m[:, np.arange(1, n)] - (q_mr[:, np.arange(0, n - 1)]) * grad.dqx_m[:, np.arange(1, n)])

    q_ml = q_m[:, :n-1] + 0.5 * grad.dqx_m[:, :n-1]
    q_mr = q_m[:, 1:n] - 0.5 * grad.dqx_m[:, 1:n]
    qy_m = np.multiply(h_m, field.v)

    qy_ml = np.full((1, 203), 0.5)
    qy_mr = np.full((1, 203), 0.5)
    # qy_ml = ((qy_ml[:, np.arange(0, n - 1)] + qy_m[:, np.arange(0, n - 1)]) * grad.dqy_m[:, np.arange(0, n - 1)])
    qy_ml = qy_m[:, :n-1] + 0.5 * grad.dqy_m[:, :n-1]
    qy_mr = (qy_m[:, np.arange(1, n)] - (qy_mr[:, np.arange(0, n - 1)]) * grad.dqy_m[:, np.arange(1, n)])
    qy_mr = qy_m[:, 1:n] - 0.5 * grad.dqy_m[:, 1:n]


    
    '''
    f.write('dx')
    f.write(str(dx))

    f.write('\n')
    f.write('h_m')
    f.write(str(h_m[0][:5]))

    f.write('\n')
    f.write('h_ml')
    f.write(str(h_ml[0][:5]))

    f.write('\n')
    f.write('h_mr')
    f.write(str(h_mr[0][:5]))

    f.write('\n')
    f.write('mu')
    f.write(str(mu[0][:5]))

    f.write('\n')
    f.write('mu_l')
    f.write(str(mu_l[0][:5]))

    f.write('\n')
    f.write('mu_r')
    f.write(str(mu_r[0][:5]))

    f.write('\n')
    f.write('kh')
    f.write(str(kh[0][:5]))

    f.write('\n')
    f.write('kh_l')
    f.write(str(kh_l[0][:5]))

    f.write('\n')
    f.write('kh_r')
    f.write(str(kh_r[0][:5]))

    f.write('\n')
    f.write('z_bl')
    f.write(str(z_bl[0][:5]))

    f.write('\n')
    f.write('z_br')
    f.write(str(z_br[0][:5]))

    f.write('\n')
    f.write('q_m')
    f.write(str(q_m[0][:5]))

    f.write('\n')
    f.write('q_ml')
    f.write(str(q_ml[0][:5]))

    f.write('\n')
    f.write('q_mr')
    f.write(str(q_mr[0][:5]))

    f.write('\n')
    f.write('qy_m')
    f.write(str(qy_m[0][:5]))

    f.write('\n')
    f.write('qy_ml')
    f.write(str(qy_ml[0][:5]))

    f.write('\n')
    f.write('qy_mr')
    f.write(str(qy_mr[0][:5]))
    '''


    # ------------------------------ Idk it seems to work until here ------------------------------ #

    # positivity constraint on mu and kh
    # mu_l = np.amax(mu_l, 0)
    mu_l = np.maximum(mu_l, 0)
    # mu_r = np.amax(mu_r, 0)
    mu_r = np.maximum(mu_r, 0)
    # kh_l = np.amax(kh_l, 0)
    kh_l = np.maximum(kh_l, 0)
    # kh_r = np.amax(kh_r, 0)
    kh_r = np.maximum(kh_r, 0)

    # retrieve primitive variables:
    z_ml = z_bl + h_ml
    z_mr = z_br + h_mr
    
    # u_l = np.multiply((h_ml >= par.h_min), q_ml)
    # u_l = np.divide(u_l, np.maximum(h_ml, par.h_min))
    
    u_l = np.where(h_ml >= par.h_min, q_ml / np.maximum(h_ml, par.h_min), 0)
    u_r = np.multiply((h_mr >= par.h_min), q_mr) / np.maximum(h_mr, par.h_min)
    v_l = np.multiply((h_ml >= par.h_min), qy_ml) / np.maximum(h_ml, par.h_min)
    v_r = np.multiply((h_mr >= par.h_min), qy_mr) / np.maximum(h_mr, par.h_min)
    c_ml = np.multiply((h_ml >= par.h_min), mu_l) / np.maximum(h_ml, par.h_min)
    c_mr = np.multiply((h_mr >= par.h_min), mu_r) / np.maximum(h_mr, par.h_min)
    k_ml = np.multiply((h_ml >= par.h_min), kh_l) / np.maximum(h_ml, par.h_min)
    k_mr = np.multiply((h_mr >= par.h_min), kh_r) / np.maximum(h_mr, par.h_min)

    # left and right fluxes:
    sig_l = np.multiply(h_ml, u_l ** 2) + 0.5 * par.g * par.R * (np.multiply(c_ml, h_ml ** 2))
    sig_r = np.multiply(h_mr, u_r ** 2) + 0.5 * par.g * par.R * (np.multiply(c_mr, h_mr ** 2))
    # wavespeeds:
    h_l = np.maximum(z_ml - z_bl, 0)
    
    SLl = np.minimum(u_l - (np.multiply(par.g * par.R * h_l, c_ml)) ** 0.5, 0)

    SRl = np.maximum(u_l + (np.multiply(par.g * par.R * h_l, c_ml)) ** 0.5, 0)

    h_r = np.maximum(z_mr - z_br, 0)
    SLr = np.minimum(u_r - (np.multiply(par.g * par.R * h_r, c_mr)) ** 0.5, 0)
    SRr = np.maximum(u_r + (np.multiply(par.g * par.R * h_r, c_mr)) ** 0.5, 0)
    # extreme wave speeds:
    SL = np.minimum(np.minimum(SLl, SLr), 0)
    SR = np.maximum(np.maximum(SRl, SRr), 0)
    prod = 1.0 / np.maximum(SR - SL, (par.g * par.h_min) ** 0.5)

    '''
    f = open("fluxLHLLOutput.txt", "a")

    f.write('mu_l')
    f.write(str(mu_l[0][:5]))
    f.write('\n')

    f.write('mu_r')
    f.write(str(mu_r[0][:5]))
    f.write('\n')

    f.write('kh_l')
    f.write(str(kh_l[0][:5]))
    f.write('\n')

    f.write('kh_r')
    f.write(str(kh_r[0][:5]))
    f.write('\n')

    f.write('z_ml')
    f.write(str(z_ml[0][:5]))
    f.write('\n')

    f.write('z_mr')
    f.write(str(z_mr[0][:5]))
    f.write('\n')

    f.write('u_l')
    f.write(str(u_l[0][:5]))
    f.write('\n')

    f.write('u_r')
    f.write(str(u_r[0][:5]))
    f.write('\n')

    f.write('v_l')
    f.write(str(v_l[0][:5]))
    f.write('\n')

    f.write('v_r')
    f.write(str(v_r[0][:5]))
    f.write('\n')

    f.write('c_ml')
    f.write(str(c_ml[0][:5]))
    f.write('\n')

    f.write('c_mr')
    f.write(str(c_mr[0][:5]))
    f.write('\n')

    f.write('k_ml')
    f.write(str(k_ml[0][:5]))
    f.write('\n')

    f.write('k_mr')
    f.write(str(k_mr[0][:5]))
    f.write('\n')

    f.write('sig_l')
    f.write(str(sig_l[0][:5]))
    f.write('\n')

    f.write('sig_r')
    f.write(str(sig_r[0][:5]))
    f.write('\n')

    f.write('h_l')
    print('h_l type: ')
    f.write(str(h_l[0][:5]))
    f.write('\n')

    f.write('SLl')
    f.write(str(SLl[0][:5]))
    f.write('\n')

    f.write('SRl')
    f.write(str(SRl[0][:5]))
    f.write('\n')

    f.write('h_r')
    f.write(str(h_r[0][:5]))
    f.write('\n')

    f.write('SLr')
    f.write(str(SLr[0][:5]))
    f.write('\n')

    f.write('SRr')
    f.write(str(SRr[0][:5]))
    f.write('\n')

    f.write('SL')
    f.write(str(SL[0][:5]))
    f.write('\n')

    f.write('SR')
    f.write(str(SR[0][:5]))
    f.write('\n')

    f.write('prod')
    f.write(str(prod[0][:5]))
    f.write('\n')
    f.close()
    '''


    '''
    print('SRl')
    print(SRl)
    print('SRr')
    print(SRr)

    print('Flux Values: ')
    print("SR:")
    print(SR)
    print("SL:")
    print(SL)
    print("q_ml:")
    print(q_ml)
    print("q_mr:")
    print(q_mr)
    print("z_ml:")
    print(z_ml)
    print("z_mr:")
    print(z_mr)
    print("prod:")
    print(prod)
    '''


    # canonical HLL statement for discharge:
    q_m_star = np.multiply(
        (np.multiply(SR, q_ml) - np.multiply(SL, q_mr) + np.multiply(np.multiply(SL, SR), (z_mr - z_ml))), prod)

    # f.write('q_m_star')
    # f.write(str(q_m_star[0][:5]) + '\n')

    # anti-emptying constraint:
    q_m_star_min = - h_mr * dx / dt

    # f.write('q_m_star_min')
    # f.write(str(q_m_star_min[0][:5]) + '\n')

 

    q_m_star_max = h_ml * dx / dt

    # f.write('q_m_star_max')
    # f.write(str(q_m_star_max[0][:5]) + '\n')



    q_m_star = np.minimum(np.maximum(q_m_star_min, q_m_star), q_m_star_max)

    # f.write('q_m_star')
    # f.write(str(q_m_star[0][:5]) + '\n')

    # canonical HLL statement for momentum:
    sig_star = np.multiply(
        (np.multiply(SR, sig_l) - np.multiply(SL, sig_r) + np.multiply(np.multiply(SL, SR), (q_mr - q_ml))), prod)
    
    # f.write('sig_star')
    # f.write(str(sig_star[0][:5]) + '\n')


    
    # momentum flux lateralisation:
    Cmhm_mean = 0.5 * (np.multiply(c_ml, h_ml) + np.multiply(c_mr, h_mr))
    
    # f.write('Cmhm_mean')
    # f.write(str(Cmhm_mean[0][:5]) + '\n')

    sig_starl = sig_star - np.multiply(np.multiply(np.multiply(np.multiply(prod, SL), par.R) * par.g, Cmhm_mean),
                                       (z_br - z_bl))
    
    # f.write('sig_starl')
    # f.write(str(sig_starl[0][:5]) + '\n')
    

    sig_starr = sig_star - np.multiply(np.multiply(np.multiply(np.multiply(prod, SR), par.R) * par.g, Cmhm_mean),
                                       (z_br - z_bl))
    
    # f.write('sig_starr')
    # f.write(str(sig_starr[0][:5]) + '\n')


    # exceptions at internal reflecting boundaries:
    # SHOULD STILL CHECK THAT

    # e = (np.logical_and(((par.g * z_ml + 0.5 * u_l ** 2) < par.g * z_br), (h_mr < par.h_min)).all())
    e = ((par.g * z_ml + 0.5 * u_l**2) < par.g * z_br) & (h_mr < par.h_min)

    # f.write('e')
    # f.write(str(e) + '\n')

    # q_m_star = np.multiply((not e), q_m_star)
    q_m_star = np.multiply((~e), q_m_star)

    # f.write('q_m_star')
    # f.write(str(q_m_star[0][:5]) + '\n')
    
    # sig_starl = np.multiply((not e), sig_starl) + np.multiply(e, (sig_l - np.multiply(np.multiply(np.multiply(2 * SL, SR), q_ml), prod)))
    sig_starl = np.multiply((~e), sig_starl) + np.multiply(e, (sig_l - np.multiply(np.multiply(np.multiply(2 * SL, SR), q_ml), prod)))
    
    # f.write('sig_starl')
    # f.write(str(sig_starl[0][:5]) + '\n')
    
    # sig_starr = np.multiply((not e), sig_starr)
    sig_starr = np.multiply((~e), sig_starr)
    
    # f.write('sig_starr')
    # f.write(str(sig_starr[0][:5]) + '\n')
    
    # e = (np.logical_and(((par.g * z_mr + 0.5 * u_r ** 2) < par.g * z_ml), (h_ml < par.h_min)).all())
    e = ((par.g * z_mr + 0.5 * u_r**2) < par.g * z_ml) & (h_ml < par.h_min)

    # f.write('e')
    # f.write(str(e) + '\n')
    
    # q_m_star = np.multiply((not e), q_m_star)
    q_m_star = np.multiply((~e), q_m_star)
    
    # f.write('q_m_star')
    # f.write(str(q_m_star[0][:5]) + '\n')
    
    # sig_starl = np.multiply((not e), sig_starl)
    sig_starl = np.multiply((~e), sig_starl)
    
    # f.write('sig_starl')
    # f.write(str(sig_starl[0][:5]) + '\n')
    
    # sig_starr = np.multiply((not e), sig_starr) + np.multiply(e, (sig_r + np.multiply(np.multiply(np.multiply(2 * SL, SR), q_mr), prod)))
    sig_starr = np.multiply((~e), sig_starr) + np.multiply(e, (sig_r + np.multiply(np.multiply(np.multiply(2 * SL, SR), q_mr), prod)))


    # f.write('sig_starr')
    # f.write(str(sig_starr[0][:5]) + '\n')
    
    # upwind momentum cross-flux:
    # sigCross_star = np.multiply((np.multiply((q_m_star.all() > 0), v_l) + np.multiply((not (q_m_star.all() > 0)), v_r)), q_m_star.all())
    sigCross_star = np.multiply((np.multiply((q_m_star.all() > 0), v_l) + np.multiply((~(q_m_star.all() > 0)), v_r)), q_m_star.all())
    
    # f.write('sigCross_star')
    # f.write(str(sigCross_star[0][:5]) + '\n')
    
    # upwind concentration flux:
    # mu_star = np.multiply((np.multiply((q_m_star.all() > 0), c_ml) + np.multiply((not (q_m_star.all() > 0)), c_mr)), q_m_star.all())
    # mu_star = np.multiply((np.multiply((q_m_star.all() > 0), c_ml) + np.multiply((~(q_m_star.all() > 0)), c_mr)), q_m_star.all())
    mu_star = np.where(q_m_star > 0, c_ml, c_mr) * q_m_star

    # f.write('mu_star')
    # f.write(str(mu_star[0][:5]) + '\n')
    
    # upwind turbulent kinetic energy flux:
    # kh_star = np.multiply((np.multiply((q_m_star.all() > 0), k_ml) + np.multiply((not (q_m_star.all() > 0)), k_mr)), q_m_star.all())
    # kh_star = np.multiply((np.multiply((q_m_star.all() > 0), k_ml) + np.multiply((~(q_m_star.all() > 0)), k_mr)), q_m_star.all())
    kh_star = np.where(q_m_star > 0, k_ml, k_mr) * q_m_star

    # f.write('kh_star')
    # f.write(str(kh_star[0][:5]) + '\n')
    
    # anti-emptying constraint:
    mu_star_min = np.multiply(- h_mr, c_mr) * dx / dt
    # f.write('mu_star_min')
    # f.write(str(mu_star_min[0][:5]) + '\n')
    mu_star_max = np.multiply(h_ml, c_ml) * dx / dt
    # f.write('mu_star_max')
    # f.write(str(mu_star_max[0][:5]) + '\n')
    mu_star = np.minimum(np.maximum(mu_star_min, mu_star), mu_star_max)
    # f.write('mu_star')
    # f.write(str(mu_star[0][:5]) + '\n')
    kh_star_min = np.multiply(- h_mr, k_mr) * dx / dt
    # f.write('kh_star_min')
    # f.write(str(kh_star_min[0][:5]) + '\n')
    kh_star_max = np.multiply(h_ml, k_ml) * dx / dt
    # f.write('kh_star_max')
    # f.write(str(kh_star_max[0][:5]) + '\n')
    kh_star = np.minimum(np.maximum(kh_star_min, kh_star), kh_star_max)
    # f.write('kh_star')
    # f.write(str(kh_star[0][:5]) + '\n')

    # final assignment:
    fluxx.q_m = q_m_star
    fluxx.sig_l = sig_starl
    fluxx.sig_r = sig_starr
    fluxx.sigCross = sigCross_star
    fluxx.mu = mu_star
    fluxx.kh = kh_star
    fluxx.z_ml = z_ml
    fluxx.z_mr = z_mr
    fluxx.z_bl = z_bl
    fluxx.z_br = z_br
    # flux.c_ml = c_ml;
    # flux.c_mr = S


    return fluxx
    # print("here")
