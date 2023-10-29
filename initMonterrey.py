import init1D
import numpy as np

def initMonterrey(n,par):
    #INITFIELD initialise flow field
    #
    # n = number of cells per unit block length

    # initialise flow domain:
    x0 = 0 # (x0) defines the initial x-coordinate 
    Lx = 22000 # (Lx) repersents the length of the flow domain (1 m)
    y0 = 0 # (y0) defines the initial y-coordinate 
    Ly = 0.5 # (Ly) computes the total width of the flow domain (1 m) 
    dx = Lx/n # (dx) computes the grid spacing based off the sum of all reach lengths (Lx) and number of cells (n)
    dy=dx
    
    # creating field object
    field = init1D.field(n, par) # input file

    # creating an array of (x) values
    #x = (x0-0.5*dx):dx:(x0+Lx+0.5*dx)
    x = np.arange((x0-0.5*dx), (x0+Lx+0.5*dx) + 1, dx) # +1 to match MATLAB results
    
    # creating a (y) array with a single value of (1)
    y = np.ones((1,1))
    #  setting field (x) and (y) attributes using the above arrays to define the grid
    field.x = np.ones((1,1)) * x # field.x = np.ones(lengt(y), 1) * x
    field.y = y * np.ones((1, len(x)))

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
    field.z_r[field.x > 21000] = -1000 # field.z_r(field.x>21000) = -1000
    
  
    # sediment bed level:
    field.z_b = np.ones(field.x.shape) * -1000  # default
    # known points for interpolation
    xx = [-1e99, 0, 6000, 21000, 21001, 1e99]
    zz = [0, 0, -78,  -123,  -1000, -1000]
    field.z_b = np.interp(field.x, xx, zz)
    # setting the rigid rim around the domain (downstream only) to (1000):
    field.z_r[-1][-1] = 1000

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
    
    return field


