import numpy as np


def hyperbolic(field, flux_x, flux_y, par, dt):
    # HYPERBOLIC
    m, n = field.x.shape
    dx = field.x[0, 1] - field.x[0, 0]
    # dy = field.y(2,1) - field.y(1,1);
    dy = dx
    # z_m_new = field.z_m+ (dt / dx) * (flux_x.q_m(:,np.arange(1,n+1)) - flux_x.q_m(:,np.arange(2,n + 1+1))) + (dt /
    # dy) * (flux_y.q_m(np.arange(1,m+1),:) - flux_y.q_m(np.arange(2,m + 1+1),:))
    z_m_new = field.z_m + (dt / dx) * (flux_x.q_m[:, (0, n + 1)]) - flux_x.q_m[:, (1, n)] + (dt / dy) * flux_y.q_m[
                                                                                                        (0, m + 1),
                                                                                                        :] - flux_y.q_m[
                                                                                                             (1, m), :]
    qm_x = np.multiply((field.z_m - field.z_b), field.u)
    # qm_x_new = qm_x + (dt / dx) * (flux_x.sig_r(:,np.arange(1,n+1)) - flux_x.sig_l(:,np.arange(2,n + 1+1))) + (dt /
    # dy) * (flux_y.sigCross(np.arange(1,m+1),:) - flux_y.sigCross(np.arange(2,m + 1+1),:)) + np.multiply((dt / dx) *
    # par.R * par.g * (np.multiply(field.c_m,(field.z_m - field.z_b))),(flux_x.z_br(:,np.arange(1,
    # n+1)) - flux_x.z_bl(:,np.arange(2,n + 1+1))))
    qm_x_new = qm_x + (dt / dx) * flux_x.sig_r[:, (0, n + 1)] - flux_x.sig_l[:, (1, n + 2)] + (
            dt / dy) * flux_y.sigCross[(0, m + 1), :] - flux_y.sigCross[(1, m + 2), :] + np.multiply(
        (dt / dx) * par.R * par.g * (np.multiply(field.c_m(field.z_m - field.z_b))),
        (flux_x.z_br[:, (0, n + 1)] - flux_x.z_bl[:, (1, n + 2)]))
    qm_y = np.multiply((field.z_m - field.z_b), field.v)
    # qm_y_new = qm_y + (dt / dx) * (flux_x.sigCross(:,np.arange(1,n+1)) - flux_x.sigCross(:,np.arange(2,n + 1+1))) +
    # (dt / dy) * (flux_y.sig_r(np.arange(1,m+1),:) - flux_y.sig_l(np.arange(2,m + 1+1),:)) + np.multiply((dt / dy) *
    # par.R * par.g * (np.multiply(field.c_m,(field.z_m - field.z_b))),(flux_y.z_br(np.arange(1,m+1),
    # :) - flux_y.z_bl(np.arange(2,m + 1+1),:)))
    qm_y_new = qm_y + (dt / dx) * flux_x.sigCross[:, (0, n + 1)] - flux_x.sigCross[:, (1, n + 2)] + (
            dt / dy) * flux_y.sig_r[(0, m + 1), :] - flux_y.sig_l[(1, m + 2), :] + np.multiply(
        (dt / dx) * par.R * par.g * (np.multiply(field.c_m(field.z_m - field.z_b))),
        (flux_y.z_br[(0, m + 1), :] - flux_y.z_bl[(1, m + 2), :]))
    nu = np.multiply((field.z_m - field.z_b), field.c_m)
    # nu_new = nu + (dt / dx) * (flux_x.mu(:,np.arange(1,n+1)) - flux_x.mu(:,np.arange(2,n + 1+1))) + (dt / dy) * (
    # flux_y.mu(np.arange(1,m+1),:) - flux_y.mu(np.arange(2,m + 1+1),:))
    nu_new = nu + (dt / dx) * flux_x.mu[:, (0, n + 1)] - flux_x.mu[:, (1, n + 2)] + (dt / dy) * (
            flux_y.mu[(1, m + 1), :] - flux_y.mu[(1, m + 2), :])
    kh = np.multiply((field.z_m - field.z_b), field.k_m)
    # kh_new = kh + (dt / dx) * (flux_x.kh(:,np.arange(1,n+1)) - flux_x.kh(:,np.arange(2,n + 1+1))) + (dt / dy) * (
    # flux_y.kh(np.arange(1,m+1),:) - flux_y.kh(np.arange(2,m + 1+1),:))
    kh_new = kh + (dt / dx) * (flux_x.kh[:, (0, n + 1)] - flux_x.kh[:, (1, n + 2)]) + (dt / dy) * (
            flux_y.kh[(0, m + 1), :] - flux_y.kh[(1, m + 2), :])
    # z-ordering condition:
    z_m_new = np.amax(z_m_new, field.z_b)
    # concentration update:
    c_m_new = np.multiply(((z_m_new - field.z_b) > par.h_min), nu_new) / np.amax((z_m_new - field.z_b),
                                                                                 par.h_min) + np.multiply(
        ((z_m_new - field.z_b) <= par.h_min), field.c_m)
    # positivity condition
    c_m_new = np.amax(c_m_new, 0)
    # turb kin energy update:
    k_m_new = np.multiply(((z_m_new - field.z_b) > par.h_min), kh_new) / np.amax((z_m_new - field.z_b),
                                                                                 par.h_min) + np.multiply(
        ((z_m_new - field.z_b) <= par.h_min), field.k_m)
    # positivity condition
    k_m_new = np.amax(k_m_new, 0)
    # velocity update
    u_new = np.multiply(((z_m_new - field.z_b) >= par.h_min), qm_x_new) / np.amax((z_m_new - field.z_b), par.h_min)
    v_new = np.multiply(((z_m_new - field.z_b) >= par.h_min), qm_y_new) / np.amax((z_m_new - field.z_b), par.h_min)
    # final update
    newfield = field
    newfield.z_m = z_m_new
    newfield.u = u_new
    newfield.v = v_new
    newfield.c_m = c_m_new
    newfield.k_m = k_m_new
    return newfield
