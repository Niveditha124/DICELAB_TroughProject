
import numpy as np
from scipy.interpolate import interp1d
import initpar
import pandas as pd

class field:
    

#taking cvs input for initial field properties
    file = pd.read_csv("Model_Input4.csv")
    x_from_file = file["x-axis (meters)"].values
    s = len(x_from_file)
    n = 200
    y = np.array([1])  
    x= np.ones((len(y), 1)) * x_from_file      
    y = np.transpose(y) * np.ones((1, x.size))
    z_b_from_file = file["y-axis (meters)"].values
    
    km_from_file = file["km (units)"].values #turbulent kinetic energy within the flow
    zm_from_file = file["zm (meters)"].values #elevation of the flow at a certain point??
    cm_from_file = file["cm (units)"].values  #sediment concentration within the current
    v_from_file = file["v (m/s)"].values #ertical velocity component 
    u_from_file = file["u (m/s)"].values #horizontal velocity component 
    
    z_b = np.ones((len(y), 1)) * z_b_from_file
    k_m = np.ones((len(y), 1)) * km_from_file
    z_r = np.ones((x.shape[0], x.shape[1])) * - 2000 #rigid channel bottom??
    z_m = np.ones((len(y), 1)) * zm_from_file
    c_m = np.ones((len(y), 1)) * cm_from_file
    u = np.ones((len(y), 1))  * u_from_file
    v = np.ones((len(y), 1)) * v_from_file

#############################################################
    t = 0
    H_up = 60 # turbidity current depth/thickness
    C_up = 0.333 # the layer-averaged volume concentration of suspended sediment carried by the turbidity current
    U_up = 1 # flow velocity
    Q_up = H_up * U_up # the volume transport rate of suspended sediment
    K_up = 0 # # turbulent kinetic energy witihn the flow 

    ### parameters we don't need ##############
    p = [0,0,0]
    L = [15000,2500, 5000]
    Lx = sum(L)
    S = [30,25,0]
    x0 = - L[0]
    dx = Lx / n; 
    dy = dx
    y0 = 0
    Ly = 0.5
    ##############################

    
    def __init__(self, n, par):

        self.n = n
        self.par = par
        self.field = field
        self.x = field.x
        self.u = field.u
        self.c_m = field.c_m
        self.z_b = field.z_b
        self.z_m = field.z_m
        self.k_m = field.k_m
        self.z_r = field.z_r
        self.Q_up = field.Q_up
        self.H_up = field.H_up
        self.C_up = field.C_up
        self.U_up = field.U_up
        self.K_up = field.K_up
        self.t = field.t
        self.x_from_file = field.x_from_file
        self.z_b_from_file = field.z_b_from_file
        self.s = field.s

        #############don't need
        self.L = [6000, 6000, 5000]
        self.S = [30, 25, 0]
        self.p = [0,0,0]
        ################

    def init1D(self, n, par):
        ###########don't need
        S = field.S
        L = field.L
        pert = field.p
        ###################

        field.H_up = 60
        field.C_up = 0.0015
  
        field.Q_up = field.H_up * field.U_up
        field.K_up = par.CfStar / par.alpha * field.U_up ** 2 # assume turbulence is fully developed at inflow
    
        field.t = 0
