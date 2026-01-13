# GEOTURBID
#
# Shallow-Water code for turbidity currents
# based on Parker et al 4-eq model
# two-dimensional, single turbid layer, second-order version

# Prepared by Benoit Spinewine (spinewine@gmail.com)

# field.x might be position, and not distance

# Create folder with timestamp for data

import os
import time
import sys
import numpy as np
from createFluxY import createFluxY
from deepCopier import deep_copy
import plotGenerator

import init1D
from initMonterrey import initMonterrey
import initpar
from bc_1D import bc_1D
from fieldplot import fieldplot
from fluxLHLL import fluxLHLL
from gradientVL import gradientVL
from hyperbolic import hyperbolic
from mirror import mirror
from relax import relax
from fieldIO import stringify_field, parse_field # parse_field implement later to parse in field text files
from timestep import timestep
from serializer import Serializer
import gifMaker


def store_data(folder_name):
    # Create and store your images in folder_name
    pass

if __name__ == "__main__":
    folder_name = 'my_folder_' + time.strftime("%Y_%m_%d_%H_%M_%S")
    folder_data = folder_name+'/data'
    folder_videos = folder_name+'/videos'
    folder_images = folder_name+'/images'
    folder_serialized = folder_name+'/serialized'

    videos_flowprofile = folder_videos + '/flowprofile'
    videos_iacbchanges = folder_videos + '/iacbchanges'
    videos_kfrprofile = folder_videos + '/kfrprofile'
    videos_ucprofile= folder_videos + '/ucprofile'
    videos_flowprofilecontour = folder_videos + '/flowprofilecontour'

    images_flowprofile = folder_images + '/flowprofile'
    images_iacbchanges = folder_images + '/iacbchanges'
    images_kfrprofile = folder_images + '/kfrprofile'
    images_ucprofile= folder_images + '/ucprofile'
    images_flowprofilecontour = folder_images + '/flowprofilecontour'

    os.mkdir(folder_name)
    os.mkdir(folder_data)
    os.mkdir(folder_videos)
    os.mkdir(folder_images)
    os.mkdir(folder_serialized)
    os.mkdir(videos_flowprofile)
    os.mkdir(videos_iacbchanges)
    os.mkdir(videos_kfrprofile)
    os.mkdir(videos_ucprofile)
    os.mkdir(videos_flowprofilecontour)
    os.mkdir(images_flowprofile)
    os.mkdir(images_iacbchanges)
    os.mkdir(images_kfrprofile)
    os.mkdir(images_ucprofile)
    os.mkdir(images_flowprofilecontour)
    store_data(folder_name)
    
#############################################################################
# User Inputs



UserInputFlag = input('\nDo you want to provide parameters? (if not, default parameters will be used) (y/n): ')
if UserInputFlag.strip().lower() == 'y':
    UserInputFlag = True
else:
    UserInputFlag = False


if UserInputFlag:
    # Gravity user input
    print('\nCurrent Gravity (g): ',  initpar.g)
    temp = None
    while temp is None:
        try:
            temp = float(input('Enter a float for Gravity (g): '))
        except ValueError:
            print("Error: Enter a valid number!".format(temp))
    initpar.g = (temp) # Makes new Gravity number 
    
    # Sediment Density user input
    print('\nCurrent Sediment Density (rho_S): ',  initpar.rho_S)
    temp = None
    while temp is None:
        try:
            temp = float(input('Enter a float for Sediment Density (rho_S): '))
        except ValueError:
            print("Error: Enter a valid number!".format(temp))
    initpar.rho_S = (temp) # Makes new Gravity number 
    
    # Fluid Density user input
    print('\nCurrent Water/Fluid Density (rho_W): ',  initpar.rho_W)
    temp = None
    while temp is None:
        try:
            temp = float(input('Enter a float for Water/Fluid Density (rho_W): '))
        except ValueError:
            print("Error: Enter a valid number!".format(temp))
    initpar.rho_W = (temp) # Makes new Gravity number 
    
    
# Can be changed later somehow based on user's wants
plotCreationFlag = input('\nDo you want to generate plot images during this run? (y/n): ')
if plotCreationFlag.strip().lower() == 'y':
    plotCreationFlag = True
else:
    plotCreationFlag = False
    
#############################################################################
import pandas as pd
# creating an array of (x) values
intermittency = pd.read_csv("intermittency_v1.csv")
inter_time = intermittency["time (hours)"].values
flow = intermittency["flow (1/0)"].values
hemi = intermittency["hemipelagic (1/0)"].values
#################################################################################

titleCounter = 0
dispflag = 0
#t_end = 3600*1000
t_end = max(inter_time)
dt_output = 3600

n = 200
o = 1
geostaticflag = 0

# material and numerical parameters
par = initpar
field = initMonterrey(n, par)
field_0 = initMonterrey(n,par)
field_prev = initMonterrey(n,par)


t_output = np.arange(0, t_end + dt_output, dt_output)
i_output = 1

# main loop:
firstTimeStep = 1
iter = 1
flux_x = None


while field.t < t_end:          # Loops from begginning of field to end 

    idx = np.abs(inter_time - field.t).argmin()
    if flow[idx] == 0:
        field.f = 0
    else:
        field.f = 1
    if hemi[idx] == 0: 
        field.h = 0
    else: 
        field.h = 1

    print(f'Iteration: {iter}')

    if np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1)))):

        dt = timestep(field, par)           # timestep evaluation
        if firstTimeStep:
            dt = min(dt, 0.1)           
            firstTimeStep = 0
        # disp(['t = ' num2str(field.t) ' [sec]']); # time display
    # empty outflowing pit
    field.z_b[field.z_r == - 6000] = field.z_r[field.z_r == - 6000]
    field.z_m[field.z_r == - 6000] = field.z_r[field.z_r == - 6000]

    field.u[field.z_r == - 6000] = 0
    field.v[field.z_r == - 6000] = 0
    field.c_m[field.z_r == - 6000] = 0
    field.k_m[field.z_r == - 6000] = 0
    
    # screen display:
    if np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1)))):
        if dispflag == 1:
            print('im in the insane if')
            fieldplot(field, field_0, field_prev, par, dt)
            #            pause;
    
    # disk output:
    if np.logical_and((np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1))))),
                      (np.logical_and((i_output <= len(t_output)), ((field.t + dt) > t_output[i_output])))):
      
    
        # ---------------------------------------     Plots/Graphs and data file generation       --------------------------------------- #
        # Generate data for the plot - Data Trimming for graphs
        # For graph generation. I just don't want to outsource it as I am not sure if its pass by reference or by value
        field.x[field.z_b == 6000] = np.nan
        field.x[field.z_b == -6000] = np.nan

        if plotCreationFlag:

            #plotGenerator.generate_flowprofile(field, field_0, images_flowprofile + '/plot' + str(titleCounter) + '.png')
            #plotGenerator.generate_ucprofile(field, images_ucprofile + '/plot' + str(titleCounter) + '.png')
            #plotGenerator.generate_kfrprofile(field, par, images_kfrprofile + '/plot' + str(titleCounter) + '.png')
            #plotGenerator.generate_iacbchanges(field, field_prev, field_0, dt, images_iacbchanges + '/plot' + str(titleCounter) + '.png')
            plotGenerator.generate_flowprofilecontour(field, field_0, images_flowprofilecontour + '/plot' + str(titleCounter)+'.png')
        
        # Writing field data to file
        filename = folder_data + '/field' + str(titleCounter) + '.txt'
        # Output to data files
        stringify_field(filename, field)

        # Serialize data and store to file
        # Makes life easier when you want to read in the field objects later
        serializerObj = Serializer(field=field, field_0=field_0, field_prev=field_prev, par=par, dt=dt)
        serializerObj.encode(serializerObj, titleCounter, folder_serialized)
        # Incrementing title counter
        titleCounter = titleCounter + 1
        i_output = i_output + 1
    

    # book-keeping|
    field_prev = deep_copy(field, field_prev)

    if field.h == 1 and field.f == 0: 
        # half-step relaxation operator:
        if np.logical_and((o == 2), (iter % 2 == 1)):
            field = relax(field, par, 0.5 * dt, geostaticflag)

        # extend field left and right:   
        field_x = mirror(field)

        #hyperbolic operator:
        if o == 1:
            field = relax(field, par, dt, geostaticflag)
            # time update
            field.t = field.t + dt

        else:
            if o == 2:
                # 2nd order predictor-corrector (Alcrudo & Garcia-Navarro 1993):
                if iter % 2 == 1:
                    # book-keeping of previous field:
                    field_prev = deep_copy(field, field_prev)
                    # predictor step:
                    field = hyperbolic(field, flux_x, flux_y, par, 0.5 * dt)
                else:
                    # half-step relaxation operator:
                    field = relax(field, par, 0.5 * dt, geostaticflag)
                    # time update:
                    field.t = field.t + dt

    if field.f == 1:    
        # half-step relaxation operator:
        if np.logical_and((o == 2), (iter % 2 == 1)):
            field = relax(field, par, 0.5 * dt, geostaticflag)

        # extend field left and right:   
        field_x = mirror(field)

        # computation of in-cell gradients:
        # note: cell slopes are NOT recomputed for the second step of the predictor-corrector
        if np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1)))):
            grad_x = gradientVL(field_x, par, o)
       
        # fluxing scheme (LHLL):

        # Original --> flux_x = fluxLHLL_2('x', field_x, grad_x, par, dt) # grad_x can be undefined but maybe we don't care?

        # (magnitude of sediment flux across the Hydraulic jump in the horizontal direction of the flow)
        flux_x = fluxLHLL(field_x, grad_x, par, dt)


        # impose BC at upstream inflow section
        # WORKS
        flux_x = bc_1D(flux_x, field_x, par)

        # Original flux_y line of code    
        flux_y = createFluxY(field)
            
        #hyperbolic operator:
        if o == 1:
            # 1st order forward Euler:
            field = hyperbolic(field, flux_x, flux_y, par, dt)
            # relaxation operator:
            field = relax(field, par, dt, geostaticflag)
            # time update
            field.t = field.t + dt

        else:
            if o == 2:
                # 2nd order predictor-corrector (Alcrudo & Garcia-Navarro 1993):
                if iter % 2 == 1:
                    # book-keeping of previous field:
                    # field_prev = field
                    field_prev = deep_copy(field, field_prev)
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
    
    # 206516 # 406516
    if iter == 406516:
        
        break
    if titleCounter == 400: #102
        break


print(field.t)
############################# make gif
print("\nSimulation complete!")

'''png_folder_path = images_flowprofile
output_gif_path = videos_flowprofile + "/flowprofile.gif"
gifMaker.create_gif(png_folder_path, output_gif_path, duration=150)

png_folder_path = images_ucprofile
output_gif_path = videos_ucprofile + "/ucprofile.gif"
gifMaker.create_gif(png_folder_path, output_gif_path, duration=150)

png_folder_path = images_kfrprofile
output_gif_path = videos_kfrprofile + "/kfrprofile.gif"
gifMaker.create_gif(png_folder_path, output_gif_path, duration=150)

png_folder_path = images_iacbchanges
output_gif_path = videos_iacbchanges + "/iacbchanges.gif"
gifMaker.create_gif(png_folder_path, output_gif_path, duration=150)'''

png_folder_path = images_flowprofilecontour
output_gif_path = videos_flowprofilecontour + "/flowprofilecontour.gif"
gifMaker.create_gif(png_folder_path, output_gif_path, duration= 150)

print("GIFs saved!")
