import init1D
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d 

def initMonterrey(n,par):
  
    
    # creating field object
    field = init1D.field(n, par) # input file

    # creating an array of (x) values
    file = pd.read_csv("R29-Region1_profile_base.csv")
    x_from_file = file["x-axis (meters)"].values
    s = len(x_from_file)    
    y = np.array([1])
    x= np.ones((len(y), 1)) * x_from_file
    y = np.transpose(y) * np.ones((1, x.size))
    z_b_from_file = (file["y-axis (meters)"].values)


    '''y = np.array([1])
    x = file.iloc[:, 0].values   # first column = x
    z = file.iloc[:, 1].values   # second column = elevation

    # Sort by x in case the data isn't ordered
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    z = z[sort_idx]

    # Create new x-axis with 100 m spacing
    x_new = np.arange(x.min(), x.max(), 100.0)

    # Interpolation function
    interp_func = interp1d(
        x, z,
        kind="linear",        # change to 'cubic' if you want smoother
        fill_value="extrapolate"
    )

    # Interpolated elevations
    z_new = interp_func(x_new)

    # Put into a new DataFrame
    df_interp = pd.DataFrame({
        "x_m": x_new,
        "elevation_m": z_new
    })


    x1 = df_interp["x_m"].values
    z_b1 = df_interp["elevation_m"].values

    x= np.ones((len(y), 1)) * x1
    y = np.transpose(y) * np.ones((1, x.size))
    field.z_b = np.ones((len(y), 1)) * z_b1
    field.k_m = np.ones((x.shape[0], x.shape[1])) * 0
    field.z_r = np.ones((x.shape[0], x.shape[1])) * - 9000
    field.z_m = np.ones((x.shape[0], x.shape[1])) * - 6000
    field.c_m = np.ones((x.shape[0], x.shape[1])) * 0
    field.u = np.ones((x.shape[0], x.shape[1])) * 0
    field.v = np.ones((x.shape[0], x.shape[1])) * 0
    s = len(x1)'''
    
    km_from_file = file["km (units)"].values
    zm_from_file = file["zm (meters)"].values
    cm_from_file = file["cm (units)"].values
    v_from_file = file["v (m/s)"].values
    u_from_file = file["u (m/s)"].values
    
    field.z_b = np.ones((len(y), 1)) * z_b_from_file
    field.k_m = np.ones((len(y), 1)) * km_from_file
    field.z_r = np.ones((x.shape[0], x.shape[1])) * -9000
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
    field.ls = np.ones((x.shape[0],x.shape[1]))  
    field.rs = np.ones((x.shape[0],x.shape[1]))  

    
    return field
