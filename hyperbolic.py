import numpy as np

def hyperbolic(field, flux_x, flux_y, par, dt):
    # HYPERBOLIC
    m, n = field.x.shape
    dx = field.x[0, 1] - field.x[0, 0]
    dy = dx

    # correct line
    ls = flux_x.q_m[:, 0:n] - flux_x.q_m[:, 1:n+1]
    rs = flux_y.q_m[0:m, :] - flux_y.q_m[1:m+1, :]
    z_m_new = field.z_m + ((dt / dx) * ls) + ((dt / dy) * rs)
    
    z_m_new = field.z_m + (dt/dx) * (flux_x.q_m[:, :n] - flux_x.q_m[:, 1:n+1]) + (dt/dy) * (flux_y.q_m[:m, :] - flux_y.q_m[1:m+1, :])
    
    #+ (dt/dy) * (flux_y.q_m[0:m, :] - flux_y.q_m[1:m+1, :])
    
    
    qm_x = np.multiply((field.z_m - field.z_b), field.u)

    qm_x_new = qm_x + (dt/dx) * (flux_x.sig_r[:, :n] - flux_x.sig_l[:, 1:n+1]) \
                + (dt/dy) * (flux_y.sigCross[:m, :] - flux_y.sigCross[1:m+1, :]) \
                + (dt/dx) * par.R * par.g * (field.c_m * (field.z_m - field.z_b)) * (flux_x.z_br[:, :n] - flux_x.z_bl[:, 1:n+1])

    qm_y = np.multiply((field.z_m - field.z_b), field.v)

    two = np.multiply((dt / dx), (flux_x.sigCross[:, np.arange(0, n)]))
    three = flux_x.sigCross[:, np.arange(0, n)]
    four = np.multiply((dt / dy), flux_y.sig_r[np.arange(0, m), :-1])
    five = flux_y.sig_l[np.arange(0, m), :-1]
    six = (dt / dx) * par.R * par.g
    six_1 = field.z_m - field.z_b
    seven = np.multiply(field.c_m, six_1)
    eight = np.multiply(seven, flux_y.z_br[np.arange(0, m), :])
    nine = flux_y.z_bl[np.arange(1, m+1), :]

    qm_y_new = qm_y + (dt / dx) * (flux_x.sigCross[:, 0:n] - flux_x.sigCross[:, 1:n+1]) \
            + (dt / dy) * (flux_y.sig_r[0:m, :] - flux_y.sig_l[1:m+1, :]) \
            + (dt / dy) * par.R * par.g * (field.c_m * (field.z_m - field.z_b)) * (flux_y.z_br[0:m, :] - flux_y.z_bl[1:m+1, :])

    nu = np.multiply((field.z_m - field.z_b), field.c_m)
    nu_new = nu + (dt/dx) * (flux_x.mu[:, :n] - flux_x.mu[:, 1:n+1]) \
            + (dt/dy) * (flux_y.mu[:m, :] - flux_y.mu[1:m+1, :])
    

    kh = np.multiply((field.z_m - field.z_b), field.k_m)
    kh_new = kh + (dt/dx) * (flux_x.kh[:, :n] - flux_x.kh[:, 1:n+1]) \
            + (dt/dy) * (flux_y.kh[:m, :] - flux_y.kh[1:m+1, :])
    
    # z-ordering condition:
    z_m_new = np.maximum(z_m_new, field.z_b)

    # concentration update:
    c_m_new = np.where((z_m_new - field.z_b) > par.h_min, nu_new / np.maximum((z_m_new - field.z_b), par.h_min), field.c_m)

    # positivity condition
    c_m_new = np.maximum(c_m_new, 0)

    # turb kin energy update:
    k_m_new = ((z_m_new - field.z_b) > par.h_min) * kh_new / np.maximum((z_m_new - field.z_b), par.h_min) + ((z_m_new - field.z_b) <= par.h_min) * field.k_m

    # positivity condition
    k_m_new = np.maximum(k_m_new, 0)

    # velocity update
    u_new = ((z_m_new - field.z_b) >= par.h_min) * qm_x_new / np.maximum((z_m_new - field.z_b), par.h_min)
    v_new = ((z_m_new - field.z_b) >= par.h_min) * qm_y_new / np.maximum((z_m_new - field.z_b), par.h_min)

    # final update
    newfield = field
    newfield.z_m = z_m_new
    newfield.u = u_new
    newfield.v = v_new
    newfield.c_m = c_m_new
    newfield.k_m = k_m_new

    return newfield
