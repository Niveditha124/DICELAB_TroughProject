import init1D
import numpy as np
import pandas as pd

def initMonterrey(n,par):
  
    
    # creating field object
    field = init1D.field(n, par) # input file

    # creating an array of (x) values
    file = pd.read_csv("R29-Region1_profile.csv")
    x_from_file = file["x-axis (meters)"].values
    s = len(x_from_file)    
    y = np.array([1])
    x= np.ones((len(y), 1)) * x_from_file
    y = np.transpose(y) * np.ones((1, x.size))
    z_b_from_file = file["y-axis (meters)"].values
    
    km_from_file = file["km (units)"].values
    zm_from_file = file["zm (meters)"].values
    cm_from_file = file["cm (units)"].values
    v_from_file = file["v (m/s)"].values
    u_from_file = file["u (m/s)"].values
    
    field.z_b = np.ones((len(y), 1)) * z_b_from_file
    field.k_m = np.ones((len(y), 1)) * km_from_file
    field.z_r = np.ones((x.shape[0], x.shape[1])) * - 9000
    field.z_m = np.ones((len(y), 1)) * zm_from_file
    field.c_m = np.ones((len(y), 1)) * cm_from_file
    field.u = np.ones((len(y), 1))  * u_from_file
    field.v = np.ones((len(y), 1)) * v_from_file
    
    field.x = x
    field.y = y
    
    field.s = s
    field.nu = np.ones((x.shape[0],x.shape[1]))*0
    field.nu2d = np.ones((x.shape[0],x.shape[1]))*0


    

    # upstream inflow section
    field.U_up = 3.5 # flow velocity
    field.H_up = 20 #20 # turbidity current depth/thickness
    field.C_up = 0.01 # the layer-averaged volume concentration of suspended sediment carried by the turbidity current
    field.Q_up = field.H_up * field.U_up # the volume transport rate of suspended sediment
    field.K_up = par.CfStar / par.alpha * field.U_up ** 2  # assume turbulence is fully developed at inflow



    

    
    
    # time:
    # -----
    field.t = 0
    field.f = 0
    field.h = 0

    
    return field
