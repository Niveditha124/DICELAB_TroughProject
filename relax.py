from friction import friction
from entrainment import entrainment
from geomorphic import geomorphic
from knappBagnold import knappBagnold
from dissipation import dissipation
from hemipelagic import hemipelagic

def relax(field = None,par = None,dt = None, geostaticflag = None):
    #RELAX relaxation (source) operator
    field = friction(field,par,dt)
    field = entrainment(field,par,dt)
    field = geomorphic(field,par,dt)
    field = knappBagnold(field,par,dt)
    field = dissipation(field,par,dt)
    field = hemipelagic(field,par,dt)

    newfield = field
    return newfield