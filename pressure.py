import numpy as np
import sys
import math

class pressure:
    
    def __init__(self, field):
        p0 = 600; H = 11000
        h = field.z_m - field.z_b
        
        self.p = p0*math.e**(-field.z_b/H)
       
