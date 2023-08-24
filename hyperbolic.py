import numpy as np
import sys

def hyperbolic(field, flux_x, flux_y, par, dt):
    # HYPERBOLIC
    m, n = field.x.shape
    dx = field.x[0, 1] - field.x[0, 0]
    # dy = field.y(2,1) - field.y(1,1);
    dy = dx
    # z_m_new = field.z_m+ (dt / dx) * (flux_x.q_m(:,np.arange(1,n+1)) - flux_x.q_m(:,np.arange(2,n + 1+1))) + (dt /
    # dy) * (flux_y.q_m(np.arange(1,m+1),:) - flux_y.q_m(np.arange(2,m + 1+1),:))
    # asdf = field.z_m + (dt/dx) * (flux_x.q_m[:, (0, n+1)])
    # print(flux_x.q_m.shape)
    # print((flux_x.q_m[:, np.arange(0, n)]).shape)
    # print((field.z_m + (dt/dx)).shape)
    # a = field.z_m
    # print("a", a.shape)
    # b = np.multiply((dt/dx), (flux_x.q_m[1:, np.arange(0, n)]))
    # print("b", b.shape)
    # c = (flux_x.q_m[1:, np.arange(1, n+1)])
    # print("c", c.shape)
    # # d = (flux_x.q_m[:, np.arange(1, n+1)])
    #
    # e = np.multiply((dt / dy), flux_y.q_m[np.arange(0, m), 1:-1])
    # print("e", e.shape)
    # f = (flux_y.q_m[np.arange(1, m+1), 1:-1])
    # print("f", f.shape)

    # correct line
    # z_m_new = field.z_m + (dt / dx) * flux_x.q_m[:, np.arange(0, n)] - flux_x.q_m[:, np.arange(0, n)] - (dt / dy) * (flux_y.q_m[np.arange(1, m+1), :] - flux_y.q_m[np.arange(1, m + 1), :])
    ls = flux_x.q_m[:, 0:n] - flux_x.q_m[:, 1:n+1]
    rs = flux_y.q_m[0:m, :] - flux_y.q_m[1:m+1, :]
    z_m_new = field.z_m + ((dt / dx) * ls) + ((dt / dy) * rs)
    
    z_m_new = field.z_m + (dt/dx) * (flux_x.q_m[:, :n] - flux_x.q_m[:, 1:n+1]) + (dt/dy) * (flux_y.q_m[:m, :] - flux_y.q_m[1:m+1, :])

    '''
    print('Field Values:')
    print('dt/dx')
    print(dt/dx)
    print('dt/dy')
    print(dt/dy)

    # Print flux_x.q_m(:,1:n)
    print('flux_x.q_m[:,1:n]')
    print(flux_x.q_m[:, 0:n])

    # Print flux_x.q_m(:,2:n+1)
    print('flux_x.q_m[:,2:n+1]')
    print(flux_x.q_m[:, 1:n+1])

    # Print flux_y.q_m(1:m,:)
    print('flux_y.q_m[0:m, :]')
    print(flux_y.q_m[0:m, :])

    # Print flux_y.q_m(2:m+1,:)
    print('flux_y.q_m[1:m+1, :]')
    print(flux_y.q_m[1:m+1, :])

    '''
    
    #+ (dt/dy) * (flux_y.q_m[0:m, :] - flux_y.q_m[1:m+1, :])
    
    
    qm_x = np.multiply((field.z_m - field.z_b), field.u)

    # qm_x_new = qm_x + (dt / dx) * (flux_x.sig_r(:,np.arange(1,n+1)) - flux_x.sig_l(:,np.arange(2,n + 1+1))) + (dt /
    # dy) * (flux_y.sigCross(np.arange(1,m+1),:) - flux_y.sigCross(np.arange(2,m + 1+1),:)) + np.multiply((dt / dx) *
    # par.R * par.g * (np.multiply(field.c_m,(field.z_m - field.z_b))),(flux_x.z_br(:,np.arange(1,
    # n+1)) - flux_x.z_bl(:,np.arange(2,n + 1+1))))
    # qm_x_new = qm_x + (dt / dx) * flux_x.sig_r[:, (0, n + 1)] - flux_x.sig_l[:, (1, n + 2)] + (
    #         dt / dy) * flux_y.sigCross[(0, m + 1), :] - flux_y.sigCross[(1, m + 2), :] + np.multiply(
    #     (dt / dx) * par.R * par.g * (np.multiply(field.c_m(field.z_m - field.z_b))),
    #     (flux_x.z_br[:, (0, n + 1)] - flux_x.z_bl[:, (1, n + 2)]))
    '''
    a = np.multiply((dt / dx), (flux_x.sig_r[:, np.arange(1, n + 1)]))
    b = (flux_x.sig_l[:, np.arange(1, n + 1)])
    c = np.multiply((dt / dx), (flux_y.sigCross[np.arange(1, m + 1), :]))
    d = (flux_y.sigCross[np.arange(1, m + 1), :])
    e = ((dt / dx) * par.R * par.g)
    f = np.multiply(field.c_m, (field.z_m - field.z_b))
    g = (flux_x.z_br[:, np.arange(0, n)] - flux_x.z_bl[:, np.arange(0, n)])
    # print((qm_x + a - b + c - d + np.multiply(e, f) - g).shape)
    qm_x_new = qm_x + a - b + c - d + np.multiply(e, f) - g
    '''
    qm_x_new = qm_x + (dt/dx) * (flux_x.sig_r[:, :n] - flux_x.sig_l[:, 1:n+1]) \
                + (dt/dy) * (flux_y.sigCross[:m, :] - flux_y.sigCross[1:m+1, :]) \
                + (dt/dx) * par.R * par.g * (field.c_m * (field.z_m - field.z_b)) * (flux_x.z_br[:, :n] - flux_x.z_bl[:, 1:n+1])

    # qm_x_new = qm_x + np.multiply((dt/dx), (flux_x.sig_r[:, np.arange(0, n+1)])) - (flux_x.sig_l[:, np.arange(1, n+2)]) + np.multiply((dt/dx), (flux_y.sigCross[np.arange(0, m+1), :])) - (flux_y.sigCross[np.arange(1, m+2), :]) + ((dt / dx)*par.R*par.g)* (
    # np.multiply(field.c_m(field.z_m - field.z_b)), (flux_x.z_br[:, np.arange(0, n+1)] - flux_x.z_bl[:, np.arange(1, n+2)]))
    qm_y = np.multiply((field.z_m - field.z_b), field.v)
    # qm_y_new = qm_y + (dt / dx) * (flux_x.sigCross(:,np.arange(1,n+1)) - flux_x.sigCross(:,np.arange(2,n + 1+1))) +
    # (dt / dy) * (flux_y.sig_r(np.arange(1,m+1),:) - flux_y.sig_l(np.arange(2,m + 1+1),:)) + np.multiply((dt / dy) *
    # par.R * par.g * (np.multiply(field.c_m,(field.z_m - field.z_b))),(flux_y.z_br(np.arange(1,m+1),
    # :) - flux_y.z_bl(np.arange(2,m + 1+1),:)))

    two = np.multiply((dt / dx), (flux_x.sigCross[:, np.arange(0, n)]))
    three = flux_x.sigCross[:, np.arange(0, n)]
    four = np.multiply((dt / dy), flux_y.sig_r[np.arange(0, m), :-1])
    # print("sigl ", flux_y.sig_l[(0, 0), :].shape)
    # print("fluxy sigl", flux_y.sig_l.shape)
    # five = flux_y.sig_l[(0, m+1), :]
    five = flux_y.sig_l[np.arange(0, m), :-1]
    six = (dt / dx) * par.R * par.g
    six_1 = field.z_m - field.z_b
    seven = np.multiply(field.c_m, six_1)
    eight = np.multiply(seven, flux_y.z_br[np.arange(0, m), :])
    nine = flux_y.z_bl[np.arange(1, m+1), :]
    # qm_y_new = two - three + four - five + six * eight - nine

    qm_y_new = qm_y + (dt / dx) * (flux_x.sigCross[:, 0:n] - flux_x.sigCross[:, 1:n+1]) \
            + (dt / dy) * (flux_y.sig_r[0:m, :] - flux_y.sig_l[1:m+1, :]) \
            + (dt / dy) * par.R * par.g * (field.c_m * (field.z_m - field.z_b)) * (flux_y.z_br[0:m, :] - flux_y.z_bl[1:m+1, :])

    # qm_y_new = qm_y + (dt / dx) * flux_x.sigCross[:, (0, n + 1)] - flux_x.sigCross[:, (1, n + 2)] + (
    #         dt / dy) * flux_y.sig_r[(0, m + 1), :] - flux_y.sig_l[(1, m + 2), :] + np.multiply(
    #     (dt / dx) * par.R * par.g * (np.multiply(field.c_m(field.z_m - field.z_b))),
    #     (flux_y.z_br[(0, m + 1), :] - flux_y.z_bl[(1, m + 2), :]))
#     print('Making nu\n')
#     print('field.z_m')
#     print(field.z_m)
#     print('field.c_m')
#     print(field.c_m)
    nu = np.multiply((field.z_m - field.z_b), field.c_m)
#     print('nu')
#     print(nu)

#     print('field.z_m')
#     print(field.z_m[0][:5])
#     print('field.z_b')
#     print(field.z_b[0][:5])
#     print('field.c_m')
#     print(field.c_m[0][:5])
#     print('nu')
#     print(nu[0][:5])
    
    # nu_new = nu + (dt / dx) * (flux_x.mu(:,np.arange(1,n+1)) - flux_x.mu(:,np.arange(2,n + 1+1))) + (dt / dy) * (
    # flux_y.mu(np.arange(1,m+1),:) - flux_y.mu(np.arange(2,m + 1+1),:))

    # nu_new = nu + (dt / dx) * flux_x.mu[:, (0, n + 1)] - flux_x.mu[:, (1, n + 2)] + (dt / dy) * (
    #         flux_y.mu[(1, m + 1), :] - flux_y.mu[(1, m + 2), :])

    # nu_new = nu + (dt / dx) * flux_x.mu[:, np.arange(0, n)] - flux_x.mu[:, np.arange(1, n+1)] + (dt / dy) * (flux_y.mu[np.arange(0, m), :] - flux_y.mu[np.arange(1, m+1), :])
    
#     print('Making nu_new\n')
#     print('flux_x.mu')
#     print(flux_x.mu)
#     print('flux_y.mu')
#     print(flux_y.mu)
    nu_new = nu + (dt/dx) * (flux_x.mu[:, :n] - flux_x.mu[:, 1:n+1]) \
            + (dt/dy) * (flux_y.mu[:m, :] - flux_y.mu[1:m+1, :])
    

    kh = np.multiply((field.z_m - field.z_b), field.k_m)
    # kh_new = kh + (dt / dx) * (flux_x.kh(:,np.arange(1,n+1)) - flux_x.kh(:,np.arange(2,n + 1+1))) + (dt / dy) * (
    # flux_y.kh(np.arange(1,m+1),:) - flux_y.kh(np.arange(2,m + 1+1),:))
    # kh_new = kh + (dt / dx) * (flux_x.kh[:, (0, n + 1)] - flux_x.kh[:, (1, n + 2)]) + (dt / dy) * (
    #         flux_y.kh[(0, m + 1), :] - flux_y.kh[(1, m + 2), :])

    # kh_new = kh + (dt / dx) * flux_x.kh[:, np.arange(0, n)] - flux_x.kh[:, np.arange(1, n+1)] + (dt / dy) * (flux_y.kh[np.arange(0, m), :] - flux_y.kh[np.arange(1, m+1), :])
    kh_new = kh + (dt/dx) * (flux_x.kh[:, :n] - flux_x.kh[:, 1:n+1]) \
            + (dt/dy) * (flux_y.kh[:m, :] - flux_y.kh[1:m+1, :])
    
    # z-ordering condition:
    z_m_new = np.maximum(z_m_new, field.z_b)

    # concentration update:
    # c_m_new = np.multiply(((z_m_new - field.z_b) > par.h_min), nu_new) / np.maximum((z_m_new - field.z_b), par.h_min) + np.multiply(((z_m_new - field.z_b) <= par.h_min), field.c_m)
#     print('Making c_m_new\n')
#     print('z_m_new')
#     print(z_m_new[0][:5])
#     print('field.z_b')
#     print(field.z_b[0][:5])
#     print('nu_new')
#     print(nu_new[0][:5])
    c_m_new = np.where((z_m_new - field.z_b) > par.h_min, nu_new / np.maximum((z_m_new - field.z_b), par.h_min), field.c_m)

    # positivity condition
    c_m_new = np.maximum(c_m_new, 0)

#     print('c_m_new')
#     print(c_m_new[0][:5])

    # print("z_m_new:", z_m_new)
    # print("field.z_b:", field.z_b)
    # print("par.h_min:", par.h_min)
    # print("nu_new:", nu_new)
    # print("z_m_new:", z_m_new)
    # print("field.z_b:", field.z_b)
    # print("par.h_min:", par.h_min)
    # print("field.c_m:", field.c_m)
    
    
    # turb kin energy update:
    # k_m_new = np.multiply(((z_m_new - field.z_b) > par.h_min), kh_new) / np.maximum((z_m_new - field.z_b), par.h_min) + np.multiply(((z_m_new - field.z_b) <= par.h_min), field.k_m)
    k_m_new = ((z_m_new - field.z_b) > par.h_min) * kh_new / np.maximum((z_m_new - field.z_b), par.h_min) + ((z_m_new - field.z_b) <= par.h_min) * field.k_m

    # positivity condition
    k_m_new = np.maximum(k_m_new, 0)

    # velocity update
    # u_new = np.multiply(((z_m_new - field.z_b) >= par.h_min), qm_x_new) / np.maximum((z_m_new - field.z_b), par.h_min)
    u_new = ((z_m_new - field.z_b) >= par.h_min) * qm_x_new / np.maximum((z_m_new - field.z_b), par.h_min)

    # v_new = np.multiply(((z_m_new - field.z_b) >= par.h_min), qm_y_new) / np.maximum((z_m_new - field.z_b), par.h_min)
    v_new = ((z_m_new - field.z_b) >= par.h_min) * qm_y_new / np.maximum((z_m_new - field.z_b), par.h_min)

    # final update
    newfield = field
    newfield.z_m = z_m_new
    newfield.u = u_new
    newfield.v = v_new
    newfield.c_m = c_m_new
    newfield.k_m = k_m_new


    return newfield
