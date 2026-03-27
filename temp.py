import numpy as np
import sys

class temp:
    
    def __init__(self, field, pfield):
        t = np.ones((1, field.s))
        h = field.z_m - field.z_b

        self.t = pfield.p/(field.nu*287) #287 - specific ideal gas constant for air (J/kg*K)
        
    
