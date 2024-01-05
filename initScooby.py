'''
initScooby.py ™ © ®

Created by Armani Araujo
TM R All Rights Reserved.
Jk this is basically initMonterrey.py but better but let me have my thing ok

Listen. Don't change the name of this file. Let it be my last piece of work for this project.
I want to be remembered as you bring up the name of this file in a serious conversation, 
and have all the lab members stare at you in disbelief and confusion.

Love you! <3

# TODO: Check all field. variables coming out of initMonterrey and compare to initScooby

'''

import sys
import init1D
import numpy as np
import pandas as pd

def printField(field):
    # Print statements for each variable
    print("\nField.x:", field.x)
    print("\nField.y:", field.y)
    print("\nField.u:", field.u)
    print("\nField.v:", field.v)
    print("\nField.z_m:", field.z_m)
    print("\nField.z_r:", field.z_r)
    print("\nField.z_b:", field.z_b)
    print("\nField.c_m:", field.c_m)
    print("\nField.k_m:", field.k_m)
    
    with open('scoobyOutput.txt', 'w') as f:
        print("\nField.x:", field.x, file=f)
        print("\nField.y:", field.y, file=f)
        print("\nField.u:", field.u, file=f)
        print("\nField.v:", field.v, file=f)
        print("\nField.z_m:", field.z_m, file=f)
        print("\nField.z_r:", field.z_r, file=f)
        print("\nField.z_b:", field.z_b, file=f)
        print("\nField.c_m:", field.c_m, file=f)
        print("\nField.k_m:", field.k_m, file=f)

def parse_user_data(path):
    df = pd.read_csv(path, header=None, names=['Distance', 'Height'])
    x = df['Distance'].tolist()
    y = df['Height'].tolist()

    return [x],[y] # To match how data is returned in Monterrey (weird nested array shit)


def initScooby(n,par):
    
    # #INITFIELD initialise flow field
    # #
    # # n = number of cells per unit block length

    # # initialise flow domain:
    # x0 = 0 # (x0) defines the initial x-coordinate 
    # # Original
    # # Lx = 22000 # (Lx) repersents the length of the flow domain (1 m)
    # Lx = 5000
    
    # y0 = 0 # (y0) defines the initial y-coordinate 
    # Ly = 0.5 # (Ly) computes the total width of the flow domain (1 m) 
    
    # # Lx = length of the flow domain (1m)
    # # n = number of cells per unit block length

    # dx = Lx/n # (dx) computes the grid spacing based off the sum of all reach lengths (Lx) and number of cells (n)
    # dy=dx
    
    max_limit = 202
    # creating field object
    field = init1D.field(n, par) # input file

    # # creating an array of (x) values
    # #x = (x0-0.5*dx):dx:(x0+Lx+0.5*dx)
    # # TODO: HELP how does this always give us 202? Also what is the significance of it?
    # # Does it matter in the grand scheme?
    # a = (x0-0.5*dx)
    # b = (x0+Lx+0.5*dx) + 1
    # # Creating a list of items between the range of a to b, with steps dx
    # x = np.arange(a,b, dx)
    # print('a: ', a)
    # print('b: ', b)
    # print('dx: ', dx)
    # # x = np.arange((x0-0.5*dx), (x0+Lx+0.5*dx) + 1, dx) # +1 to match MATLAB results
    # print(x)
    # # sys.exit()
    

    # Creating our own x
    # TODO: Make x contain values from user
    # TODO: x/field.x contains x values, field.z_b contains y values
    x,z_b = parse_user_data('user_input.csv')

    # Assigning the parsed x, z_b values into field.
    field.x = np.array(x)
    field.z_b = np.array(z_b)
    

    # creating a 1 by 1 (y) array with a single value of (1)
    y = np.ones((1,1))
    #  setting field (x) and (y) attributes using the above arrays to define the grid
    # field.x = np.ones((1,1)) * x # field.x = np.ones(lengt(y), 1) * x
    field.y = y * np.ones((1, len(field.x[0]))) # shape of field.x and not x since in this code x is not a numpy array yet

    # setting the top of turbid layer to (-1000) for the whole grid:
    field.z_m = np.ones( field.x.shape ) * -1000 #.001
    # field.z_m(field.x<0) = 0.75

    # Setting the turbid concentration to (0) for the whole grid:
    field.c_m = np.ones(field.x.shape)*0 #.0001
    # field.c_m(field.x<0) = 0.2

    # setting the turbulent kinetic energy to (0) for the whole grid:
    field.k_m = np.ones(field.x.shape)*0 #.0001

    # setting the rigid channel bottom under sediment bed to (-2000) for the whole grid:
    field.z_r = np.ones(field.x.shape) * -2000  # default
    
    # setting (z_r) to (-1000) for (x) values greater than (21000):
    # field.z_r[field.x > 21000] = -1000 # field.z_r(field.x>21000) = -1000
    # Not really needed, but its fine we'll do our version anyways
    # TODO: We might not need to even do this. Ask Isaac
    field.z_r[field.x > 21000] = -1000
    
    
    
    # Needed before to initialize z_b, not needed anymore.
    # sediment bed level:
    # field.z_b = np.ones(field.x.shape) * -1000  # default
    # known points for interpolation
    # xx = [-1e99, 0, 6000, 21000, 21001, 1e99]
    # zz = [0, 0, -78,  -123,  -1000, -1000]
    # field.z_b = np.interp(field.x, xx, zz)
    # Not going to perform interpolation anymore since user will provide all points

    # setting the rigid rim around the domain (downstream only) to (1000):
    # TODO: Check if this is needed? Although it makes the last point of the graph go yeet up
    # field.z_r[-1][-1] = 1000
    
    
    
    # z-ordering condition:
    field.z_b = np.maximum(field.z_b , field.z_r)
    field.z_m = np.maximum(field.z_m , field.z_b)
    

    # velocities:
    field.u = np.zeros(field.x.shape)
    field.v = np.zeros(field.x.shape)

    # upstream inflow section
    field.U_up = 3.5 # flow velocity
    field.H_up = 20 # turbidity current depth/thickness
    field.C_up = 0.01 # the layer-averaged volume concentration of suspended sediment carried by the turbidity current
    field.Q_up = field.H_up * field.U_up # the volume transport rate of suspended sediment
    field.K_up = par.CfStar / par.alpha * field.U_up ** 2  # assume turbulence is fully developed at inflow
    
    # time:
    # -----
    field.t = 0
    printField(field)
    return field
