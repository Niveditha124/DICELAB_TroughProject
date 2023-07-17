# GEOTURBID
#
# Shallow-Water code for turbidity currents
# based on Parker et al 4-eq model
# two-dimensional, single turbid layer, second-order version
#
# Prepared by Benoit Spinewine (spinewine@gmail.com)

# initialisation:
import numpy as np
import os
from createFluxY import createFluxY



import init1D
from initMonterrey import initMonterrey
import initpar
import initrun
from bc_1D import bc_1D
from fieldplot import fieldplot
from fluxLHLL import fluxLHLL
from fluxLHLL_2 import fluxLHLL_2
from gradientVL import gradientVL
from hyperbolic import hyperbolic
from mirror import mirror
from relax import relax
from tag2str import tag2str
from timestep import timestep

import sys

dispflag = 0
t_end = 3600*1000
dt_output = 3600
n = 200
o = 1
geostaticflag = 0
par = initpar
# field = init1D.field(n, par) # input file
field = initMonterrey(n, par)
field_0 = field
field_prev = field
# disk output and screen display parameters
# t0 = (par.h0/par.g)^0.5;]
t_output = np.arange(0, t_end + dt_output, dt_output)
i_output = 1
# prepare graphics:
# figure;

os.system('cls')
file_path = "hyperbolicOutput.txt"
if os.path.exists(file_path):
    os.remove(file_path)
    print("File deleted successfully.")
else:
    print("File does not exist.")

file_path = "fluxLHLLOutput.txt"
if os.path.exists(file_path):
    os.remove(file_path)
    print("File deleted successfully.")
else:
    print("File does not exist.")

# main loop:
firstTimeStep = 1
# continue previous run
# load field_202;
# i_output = 203;
# firstTimeStep = 0;
iter = 1
flux_x = None


while field.t < t_end:
    
    print("\n\n", 'Iteration ', iter, ': ')
    iterStr = "Iteration " + str(iter) + ": \n\n"
    f = open("hyperbolicOutput.txt", "a")
    f.write(iterStr)
    f.close()

    f = open("fluxLHLLOutput.txt", "a")
    f.write(iterStr)
    f.close()

    
    
    if np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1)))):
        dt = timestep(field, par)
        if firstTimeStep:
            dt = min(dt, 0.1)
            firstTimeStep = 0
        # disp(['t = ' num2str(field.t) ' [sec]']); # time display
    # empty outflowing pit
    field.z_b[field.z_r == - 1000] = field.z_r[field.z_r == - 1000]
    field.z_m[field.z_r == - 1000] = field.z_r[field.z_r == - 1000]

    field.u[field.z_r == - 1000] = 0
    field.v[field.z_r == - 1000] = 0
    field.c_m[field.z_r == - 1000] = 0
    field.k_m[field.z_r == - 1000] = 0
    
    # screen display:
    if np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1)))):
        if dispflag == 1:
            print('im in the insane if')
            fieldplot(field, field_0, field_prev, par, dt)
            #            pause;
    
    # disk output:
    if np.logical_and((np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1))))),
                      (np.logical_and((i_output <= len(t_output)), ((field.t + dt) > t_output[i_output])))):
        # eval(np.array(['save field_', tag2str(i_output - 1), ' field field_0 field_prev dt']))
        # eval('save field_', tag2str(i_output - 1), np.array['field field_0 field_prev dt'])
        fieldplot(field, field_0, field_prev, par, dt)
        #         eval(['print -djpeg95 view_' tag2str(i_output-1)]);
        #         saveas(gcf,['view_' tag2str(i_output-1)],'fig');
        i_output = i_output + 1
    
    
    # book-keeping
    field_prev = field
    # half-step relaxation operator:
    if np.logical_and((o == 2), (iter % 2 == 1)):
        field = relax(field, par, 0.5 * dt, geostaticflag)
    # extend field left and right:   
    
    field_x = mirror(field)


    #    field_y = mirror(swapfield(field));
    # computation of in-cell gradients:
    # note: cell slopes are NOT recomputed for the second step of the predictor-corrector
    if np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1)))):
        grad_x = gradientVL(field_x, par, o)
        #        grad_y = gradientVL(field_y,par,o);
    # fluxing scheme (LHLL):
    # Original --> flux_x = fluxLHLL_2('x', field_x, grad_x, par, dt) # grad_x can be undefined but maybe we don't care?

    # WORKS
    flux_x = fluxLHLL(field_x, grad_x, par, dt)


    # print('\n', flux_x.sig_l[0][0], flux_x.sig_l[0][1])

    # impose BC at upstream inflow section
    # WORKS
    flux_x = bc_1D(flux_x, field_x, par)



    #    flux_y = swapflux(fluxLHLL(field_y,grad_y,par,dt));
    # 1D default:
    # Original flux_y line of code
    # flux_y = fluxLHLL_2('y', field_x, grad_x, par, dt) # this is because we have to instantiate flux_y
    
    flux_y = createFluxY(field)

    # print("ln 106 ", flux_x.q_m.shape)
    # flux_y.q_m = np.zeros((2, field_x.x.shape[1]))
    # # print("ln 108 ", flux_x.q_m.shape)
    # flux_y.sig_l = np.zeros((2, len(field.x)))
    # flux_y.sig_r = np.zeros((2, len(field.x)))
    # flux_y.sigCross = np.zeros((2, len(field.x)))
    # flux_y.mu = np.zeros((2, len(field.x)))
    # flux_y.kh = np.zeros((2, len(field.x)))
    # declare 2,203 array of 1's; multiply whole thing by field.z_m
            # this doesn't seem to be used anywhere
    # flux_y.z_ml = np.transpose(np.array([1, 1])) * field.z_m
    # flux_y.z_mr = np.transpose(np.array([1, 1])) * field.z_m
    # flux_y.z_bl = np.transpose(np.array([1, 1])) * field.z_b
    # flux_y.z_br = np.transpose(np.array([1, 1])) * field.z_b
    # hyperbolic operator:

    if o == 1:
        # 1st order forward Euler:
        # print("flux_x qm", flux_x.q_m.shape)
        # print('Before Hyperbolic')
        # print(field.z_m[0][:5])
        # WORKS - if we comment out relax, everything in hyperbolic 
        # (and subsequently everything else used by hyperbolic) works as it should
        field = hyperbolic(field, flux_x, flux_y, par, dt)  
        # relaxation operator:
        # field = relax(field, par, dt, geostaticflag)
        print('Midway - z_m')
        print(field.z_m[0][:20])
        # time update:
        field.t = field.t + dt

    else:
        if o == 2:
            # 2nd order predictor-corrector (Alcrudo & Garcia-Navarro 1993):
            if iter % 2 == 1:
                # book-keeping of previous field:
                field_prev = field
                # predictor step:
                field = hyperbolic(field, flux_x, flux_y, par, 0.5 * dt)
            else:
                # corrector step:
                field = hyperbolic(field_prev, flux_x, flux_y, par, dt)
                # half-step relaxation operator:
                field = relax(field, par, 0.5 * dt, geostaticflag)
                # time update:
                field.t = field.t + dt
    
    iter = iter + 1
    if iter == 20:
        break


