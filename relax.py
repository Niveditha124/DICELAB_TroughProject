from friction import friction
from entrainment import entrainment
from geomorphic import geomorphic
from knappBagnold import knappBagnold
from dissipation import dissipation
from hemipelagic import hemipelagic
from pressure import pressure
from temp import temp
import initpar
import numpy as np
import sys

def relax(field = None,par = None,dt = None, geostaticflag = None):
    #RELAX relaxation (source) operator
    if field.f == 1: 
        #tfield = temp(field, initpar)

        #tfield = temp(field, pfield)

        pfield = pressure(field)
        field = friction(field,par,dt)
        field = entrainment(field, pfield, par,dt)
        field = geomorphic(field,par,dt)
        field = knappBagnold(field,par,dt)
        field = dissipation(field,par,dt)
        
    if field.h == 1:
        field = hemipelagic(field,par,dt)


    newfield = field
    
    newfield.ls = pfield.p

    
    return newfield
