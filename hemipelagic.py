import numpy as np
import sys
from sun import sun

# HEMIPELAGIC operator accounting for sedimentation from hemipelagic sediments
def hemipelagic(field,par, dt):

    if field.t == 0:
        z_b_new = field.z_b + dt * par.v_hemi
    else: 
        I = sun(field,par)
        z_b_new = field.z_b + dt* par.v_hemi - (I)

    
    
    
    # final update:
    newfield = field
    newfield.z_b = z_b_new
    return newfield
