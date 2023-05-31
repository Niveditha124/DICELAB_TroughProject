import init1D
import numpy as np

def initMonterrey(n,par):
    #INITFIELD initialise flow field
    #
    # n = number of cells per unit block length

    # initialise flow domain:
    x0 = 0
    Lx = 22000  # 1 m
    y0 = 0
    Ly = 0.5  # 1 m
    dx = Lx/n
    dy=dx
    
    field = init1D.field(n, par) # input file

    #x = (x0-0.5*dx):dx:(x0+Lx+0.5*dx)
    x = np.arange((x0-0.5*dx), (x0+Lx+0.5*dx) + 1, dx) # +1 to match MATLAB results
    y = np.ones((1,1))
    field.x = np.ones((1,1)) * x # field.x = np.ones(lengt(y), 1) * x
    field.y = y * np.ones((1, len(x)))

    # top of turbid layer:
    field.z_m = np.ones( field.x.shape ) * -1000 #.001
    # field.z_m(field.x<0) = 0.75

    # turbid concentration
    field.c_m = np.ones(field.x.shape)*0 #.0001
    # field.c_m(field.x<0) = 0.2

    # turbulent kinetic energy
    field.k_m = np.ones(field.x.shape)*0 #.0001

    # rigid channel bottom under sediment bed:
    field.z_r = np.ones(field.x.shape) * -2000  # default
    field.z_r[field.x > 21000] = -1000 # field.z_r(field.x>21000) = -1000
    
  
    # sediment bed level:
    field.z_b = np.ones(field.x.shape) * -1000  # default
    # known points for interpolation
    xx = [-1e99, 0, 6000, 21000, 21001, 1e99]
    zz = [0, 0, -78,  -123,  -1000, -1000]
    field.z_b = np.interp(field.x, xx, zz)
    # rigid rim around domain (downstream only):
    field.z_r[-1][-1] = 1000

    # z-ordering condition:
    field.z_b = np.maximum(field.z_b , field.z_r)
    field.z_m = np.maximum(field.z_m , field.z_b)
    print(field.z_m)

    # velocities:
    field.u = np.zeros(field.x.shape)
    field.v = np.zeros(field.x.shape)

    # upstream inflow section
    field.U_up = 3.5
    field.H_up = 20
    field.C_up = 0.01
    field.Q_up = field.H_up * field.U_up
    field.K_up = par.CfStar / par.alpha * field.U_up ** 2  # assume turbulence is fully developed at inflow
    # time:
    # -----
    field.t = 0
    
    return field


