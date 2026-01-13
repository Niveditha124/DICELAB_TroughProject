from friction import friction
from entrainment import entrainment
from geomorphic import geomorphic
from knappBagnold import knappBagnold
from dissipation import dissipation
from hemipelagic import hemipelagic

def relax(field = None,par = None,dt = None, geostaticflag = None):
    #RELAX relaxation (source) operator
    if field.f == 1: 
        field = friction(field,par,dt)
        field = entrainment(field,par,dt)
        ield = geomorphic(field,par,dt)
        field = knappBagnold(field,par,dt)
        field = dissipation(field,par,dt)
    if field.h == 1:
        field = hemipelagic(field,par,dt)

    newfield = field
    return newfield
