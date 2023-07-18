from friction import friction
from entrainment import entrainment
from geomorphic import geomorphic
from knappBagnold import knappBagnold
from dissipation import dissipation
from hemipelagic import hemipelagic
import sys
import numpy as np

def relax(field = None,par = None,dt = None, geostaticflag = None):
    #RELAX relaxation (source) operator
    
    # print('Midway - z_m')
    # print(field.z_m[0][:5])
    field = friction(field,par,dt)
    
    # print('Midway - z_m')
    # print(field.z_m[0][:5])

    field = entrainment(field,par,dt)
    # print('Midway - z_m')
    # print(field.z_m[0][:5])


    field = geomorphic(field,par,dt)
    # print('field.c_m inside2: {:.16f}'.format(field.c_m[0][0]))
    # print('Midway - z_m')
    # print(field.z_m[0][:5])

    field = knappBagnold(field,par,dt)
    # print('Midway - z_m')
    # print(field.z_m[0][:5])
    
    field = dissipation(field,par,dt)
    # print('Midway - z_m')
    # print(field.z_m[0][:5])
    
    field = hemipelagic(field,par,dt)

    # if ( geostaticflag == 1 )
#     field = geostatic(field,par);
# end;
    newfield = field
    return newfield