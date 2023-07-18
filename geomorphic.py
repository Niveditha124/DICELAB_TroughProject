# ENTRAINMENT operator accounting for water entrainment at the top of turbidity current
# solved implicitly with backward Euler scheme (solution obtained
# interatively from the explicit estimate with a Newton scheme)
import numpy as np
import sys

def geomorphic(field, par, dt):
    # obtain norm and direction vectors
    vel = (field.u ** 2 + field.v ** 2) ** 0.5
    ix = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.u / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))
    iy = ((vel > ((par.g * par.h_min) ** 0.5)).astype(int)) * (field.v / (np.maximum(vel, (par.g * par.h_min) ** 0.5)))
    h = field.z_m - field.z_b

    
    # moving sediments
    CH = h * field.c_m
    # KH
    KH = h * field.k_m
    '''
    print('\n')
    print('par.alpha:', par.alpha)
    print('field.k_m:', field.k_m[0][0])
    print('par.vs:', par.vs)
    print('par.Rp:', par.Rp)
    print('par.g:', par.g)
    print('h: {:.6e}'.format(h[0][0]))
    '''
    
    # temp = (par.alpha * field.k_m) ** 0.5
    # Ze5 = temp / par.vs
    # Ze5 = Ze5 * (par.Rp ** 0.6)
    # temp2 = temp / par.g
    # temp2 = temp2 / np.maximum(h, par.h_min)
    # temp2 = temp2 ** 0.08
    # Ze5 = Ze5 * temp2
    # Ze5 = Ze5 ** 5

    '''
        inside = temp / par.g
        print('inside: %f\n', inside)
        inside = inside / max(h[0][0],par.h_min)
        print('inside: %f\n', inside)
        Ze5 = Ze5 * (inside ** 0.08)
        print('Ze5: %f\n', Ze5)
        Ze5 = Ze5 ** 5
        print('Ze5: %f\n', Ze5)
    '''

    '''
    # solve for CH
    # start with explicit estimate
    denom = ((par.vs * par.Rp * 0.6 * (((par.alpha * field.k_m) ** 0.5) / (par.g / np.maximum(h, par.h_min)))) ** 0.08)
    Ze5 = ((par.alpha * field.k_m) ** 0.5) / 1 # because we have to initialize the array to something that won't shit the bed, so we can reference it's index :)
    
    for each in denom:## checking where each 0 value is in the denominator, and where it is 0.0, using 1 as the denom instead so we don't have a division issue
        for index, item in enumerate(each):
            if item == 0.0: # if it was 0 before it remains the same
                Ze5[0][index] = (par.alpha * field.k_m[0][index]) ** 0.5 / 1
            else: # otherwise it changes to whatever the updated par and field values calculate out to
                Ze5[0][index] = ((((par.alpha * field.k_m[0][index]) ** 0.5) / (par.vs * par.Rp * 0.6 * ((par.alpha * field.k_m[0][index]) ** 0.5) / (par.g / np.maximum(h, par.h_min)))) ** 0.08) ** 5
    
    # iterate 10 times with Newton Scheme
    for x in range(10):
        denom2 = (par.vs * par.Rp * 0.6 * ((par.alpha * K_new) ** 0.5) / (par.g / np.maximum(h_new, par.h_min)) ** 0.08) ** 5
        for each in denom2:
            for index, item in enumerate(each):
                if item == 0.0:
                    Ze5[0][index] = (par.alpha * K_new[0][index]) ** 0.5 / 1
                else:
                    Ze5[0][index] = ((((par.alpha * K_new[0][index]) ** 0.5) / (par.vs * par.Rp * 0.6 * ((par.alpha * K_new[0][index]) ** 0.5) / (par.g / np.maximum(h_new, par.h_min)))) ** 0.08) ** 5
        E = np.maximum((par.p * (1.3 * 10 ** -7)) * par.vs * Ze5 / (1 + (1.3 * 10 ** -7) / 0.3 * Ze5), 0)
        D = np.maximum(par.vs * par.r0 * C_new, 0)
        CH_new = np.maximum(CH + dt * (E - D), 0)
        h_new = np.maximum(h + dt / par.c_b * (E - D), 0)
        C_new = np.maximum(CH_new / np.maximum(h_new, par.h_min), 0)
        KH_new = KH - dt * 0.5 * par.R * par.g * h_new * (E - D)
        K_new = np.maximum(0, KH_new / np.maximum(h_new, par.h_min))

    # ensure dissipation of K (should we do that? -- watf)
    K_new = np.minimum(field.k_m, K_new)
    
    
    
    '''
    Ze5 = ((par.alpha*field.k_m) ** 0.5 / par.vs * par.Rp ** 0.6 * ((par.alpha * field.k_m) ** 0.5 / par.g / np.maximum(h, par.h_min)) ** 0.08) ** 5

    # print('Ze5: {:.10e}'.format(Ze5[0][0]))
    E = np.maximum((par.p * (1.3 * 10 ** -7)) * par.vs * Ze5 / (1 + (1.3 * 10 ** -7) / 0.3 * Ze5), 0)
    D = np.maximum(par.vs * par.r0 * field.c_m, 0)
    CH_new = np.maximum(CH + dt * (E - D), 0)
    h_new = np.maximum(h + dt / par.c_b * (E - D), 0)
    C_new = np.maximum(CH_new / np.maximum(h_new, par.h_min), 0)
    KH_new = KH - dt * 0.5 * par.R * par.g * h_new * (E - D)
    K_new = np.maximum(0, KH_new / np.maximum(h_new, par.h_min))





    for i in range(10):
        # Ze5 = ((par.alpha*K_new).^0.5/par.vs.*par.Rp^0.6.*((par.alpha*K_new).^0.5./par.g./max(h_new,par.h_min)).^0.08).^5;
        Ze5 = ((par.alpha*K_new) ** 0.5 / par.vs * par.Rp ** 0.6 * ((par.alpha * K_new) ** 0.5 / par.g / np.maximum(h_new, par.h_min)) ** 0.08) ** 5
        # E = max( par.p*1.3e-7*par.vs*Ze5./(1+1.3e-7/0.3*Ze5) , 0 );
        E = np.maximum((par.p * (1.3 * 10 ** -7)) * par.vs * Ze5 / (1 + (1.3 * 10 ** -7) / 0.3 * Ze5), 0)
        # D = max( par.vs*par.r0*C_new , 0 );
        D = np.maximum(par.vs * par.r0 * C_new, 0)
        # CH_new = max(CH + dt*(E-D) , 0);
        CH_new = np.maximum(CH + dt * (E - D), 0)
        # h_new = max (h + dt/par.c_b*(E-D) , 0);
        h_new = np.maximum(h + dt / par.c_b * (E - D), 0)
        # C_new = max(CH_new./max(h_new,par.h_min) , 0);
        C_new = np.maximum(CH_new / np.maximum(h_new, par.h_min), 0)
        # KH_new = KH - dt*0.5*par.R*par.g.*h_new.*(E-D);
        KH_new = KH - dt * 0.5 * par.R * par.g * h_new * (E - D)
        # K_new = max(0 , KH_new./max(h_new,par.h_min));
        K_new = np.maximum(0, KH_new / np.maximum(h_new, par.h_min))

    
    # print('Values: ')
    # print('CH: {:.16f}'.format(CH[0][0]))

    # print('KH: {:.16f}'.format(KH[0][0]))

    # print('par.alpha:', par.alpha)
    # print('field.k_m:', field.k_m)
    # print('par.vs:', par.vs)
    # print('par.Rp:', par.Rp)
    # print('par.g:', par.g)
    # print('h:', h)
    # print('par.h_min:', par.h_min)

    # print('Ze5: {:.16f}'.format(Ze5[0][0]))

    # print('E: {:.16f}'.format(E[0][0]))

    # print('D: {:.16f}'.format(D[0][0]))

    # print('CH_new: {:.16f}'.format(CH_new[0][0]))

    # print('h_new: {:.16f}'.format(h_new[0][0]))

    # print('C_new: {:.16f}'.format(C_new[0][0]))

    # print('KH_new: {:.16f}'.format(KH_new[0][0]))

    # print('K_new: {:.16f}'.format(K_new[0][0]))
    

    # retrieve bed level change and impose limit. dzb is positive in case of deposition
    dzb = np.minimum((dt * (D - E) / par.c_b), ((field.z_m - field.z_b) * field.c_m / par.c_b))
    dzb = np.maximum(dzb, field.z_r - field.z_b)  # dzb is positive in case of deposition

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
    newfield.c_m = np.minimum(np.maximum(CH_new / np.maximum(h_new, par.h_min), 0), 1)
    if (np.any(np.isnan(h_new))):
        print('h_new after has nans')
        sys.exit()
    indices = np.where(h_new < par.h_min)
    newfield.c_m[indices] = field.c_m[indices]

    newfield.k_m = np.maximum(KH_new / np.maximum(h_new, par.h_min), 0)

    # if h_new.all() < par.h_min:
    #     newfield.c_m = field.c_m
    # else:
    #     newfield.c_m = np.minimum(np.maximum(CH_new / np.maximum(h_new, par.h_min), 0), 1)
    # newfield.k_m = np.maximum(KH_new / np.maximum(h_new, par.h_min), 0)
    return newfield
    