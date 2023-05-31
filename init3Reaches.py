import init1D
import initpar
import numpy as np
from scipy.interpolate import interp1d

# TODO: Might need to round up values of field.z_b
# TODO: Temporary field object created inside init3Reaches function. Not sure where to get the field object
# Or if the original is created here oh well
    
def init3Reaches(n, par):
    #INITFIELD initialise flow field
    #
    # n = number of cells per unit block length

    field = init1D.field(n, par)

    L1 = 10000 # length of reach 1
    S1 = 0.01 # slope of reach 1
    p1 = 0 # amplitude of initial bed perturbation for reach 1
    L2 = 30000
    S2 = 0.003
    p2 = 1
    L3 = 10000
    S3 = 0
    p3 = 0

    field.S1 = S1
    field.S2 = S2
    field.S3 = S3
    field.L1 = L1
    field.L2 = L2
    field.L3 = L3
    field.pert1 = p1
    field.pert2 = p2
    field.pert3 = p3

    # initialise flow domain:
    x0 = -L1
    Lx = L1+L2+L3 # 1 m
    y0 = 0
    Ly = 0.5 # 1 m
    dx = Lx/n
    dy=dx
    x = np.arange((x0-0.5*dx), (x0+Lx+0.5*dx) + 1, dx) # +1 to match MATLAB results
    y = np.ones((1,1))

    field.x = np.ones((1,1)) * x
    field.y = y * np.ones((1,len(x)))

    isX1 = np.where((field.x > -field.L1) & (field.x < 0))[1]
    # Adding 1 to every element in the list for some reason they are all 1 less idk
    isX1 = [x+1 for x in isX1]
    isX1 = np.array(isX1) # converting back to ndarray

    isX2 = np.where((field.x > 0) & (field.x<field.L2))[1]
    isX2 = [x+1 for x in isX2]
    isX2 = np.array(isX2) # converting back to ndarray
    
    isX3 = np.where((field.x > field.L2) & (field.x < (field.L2 + field.L3)))[1]
    isX3 = [x+1 for x in isX3]
    isX3 = np.array(isX3) # converting back to ndarray


    # top of turbid layer:
    field.z_m = np.ones(field.x.shape ) * -1000 #.001
    # field.z_m(field.x<0) = 0.75

    # turbid concentration
    field.c_m = np.ones( field.x.shape ) * 0 #.0001
    # field.c_m(field.x<0) = 0.2

    # turbulent kinetic energy
    field.k_m = np.ones( field.x.shape ) * 0 #.0001

    # rigid channel bottom under sediment bed:
    field.z_r = np.ones( field.x.shape ) * -2000 # default
    # known points for interpolation
    # xx = [-1e10   0 1e10]
    # zz = [1e10*S1 0 -1e10*S1]
    # field.z_r = interp1(xx,zz,field.x)
    field.z_r[0][-3:] = -1000 # field.z_r(end-2:end) = -1000

    # sediment bed level:
    field.z_b = np.ones( field.x.shape ) *- 1000 # default
    
    # known points for interpolation
    xx = np.array([-L1, 0, L2, L2+L3])
    zz = np.array([L1*S1, 0, -L2*S2, -L2*S2-L3*S3])
    # field.z_b = np.interp(xx,zz,field.x[0])

    interp_func = interp1d(xx, zz, kind='linear', fill_value='extrapolate')
    field.z_b = interp_func(field.x)
    
    # field.z_b(end-2:end) = -1000
    field.z_b[0][-3:] = -1000
    
    
    # rigid rim around domain (downstream only):
    # field.z_r([end]) = 1000
    field.z_r[0][-1] = 1000
    
    #initial bed perturbations
    shape = field.z_b.shape
    for i in isX1:
        field.z_b[0][i] = np.float64(field.z_b[0][i] + ( np.random.rand() * p1 - p1 / 2))
    for i in isX2:
        field.z_b[0][i] = np.float64(field.z_b[0][i] + ( np.random.rand() * p2 - p2 / 2))
    for i in isX3:
        field.z_b[0][i] = np.float64(field.z_b[0][i] + ( np.random.rand() * p3 - p3 / 2))


    
    #field.z_b(isX1) = field.z_b(isX1) + ( rand(size(field.z_b(isX1)))*p1-p1/2 )
    #field.z_b(isX2) = field.z_b(isX2) + ( rand(size(field.z_b(isX2)))*p2-p2/2 )
    #field.z_b(isX3) = field.z_b(isX3) + ( rand(size(field.z_b(isX3)))*p3-p3/2 )

    # upstream inflow section
    field.H_up = 60
    field.C_up = 0.0015
    field.U_up = 1
    # field.Ri_up = 0.8
    # field.U_up = (par.R*par.g*field.C_up*field.H_up/field.Ri_up)^0.5
    field.Q_up = field.H_up * field.U_up
    field.K_up = par.CfStar / par.alpha * field.U_up ** 2 # assume turbulence is fully developed at inflow

    # z-ordering condition:
    field.z_b = np.maximum( field.z_b , field.z_r )
    field.z_m = np.maximum( field.z_m , field.z_b )

    # velocities:
    field.u = np.zeros( field.x.shape )
    field.v = np.zeros( field.x.shape )

    # time:
    # -----
    field.t = 0

    return field
    


