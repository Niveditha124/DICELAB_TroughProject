import numpy as np

# HEMIPELAGIC operator accounting for sedimentation from hemipelagic sediments
def hemipelagic(field,par, dt):
    z_b_new = field.z_b + dt * par.v_hemi
    
    # final update:
    newfield = field
    newfield.z_b = z_b_new
    return newfield