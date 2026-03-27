import numpy as np
import pandas as pd
from decimal import Decimal

def sun(field,par):
    
    dx = np.diff(field.x)
    dy = np.diff(field.z_b)
    slope = np.degrees(np.acos(dy/dx))
    first = slope[0][0]
    slopes = np.insert(slope, 0, first)
    
    file = pd.read_csv("Solar_elevation.csv")
    sol = file["Sol (day)"].values
    elevation = file["Elevation (degrees)"].values

    

    if field.t < 86400:
        day = 1
    else:
        day = round(field.t/86400)

    idx = np.abs(elevation - day).argmin()

    e_slopes = (90 - slopes) + elevation[idx]
    I = (600*np.sin(np.radians(e_slopes)))*3e-11

    return I

 
