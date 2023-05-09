from friction import friction
from entrainment import entrainment
from geomorphic import geomorphic
def relax(field = None,par = None,dt = None, geostaticflag = None):
    #RELAX relaxation (source) operator
    
    field = friction(field,par,dt)
    field = entrainment(field,par,dt)
    field = geomorphic(field,par,dt)
    field = knappBagnold(field,par,dt)
    field = dissipation(field,par,dt)
    field = hemipelagic(field,par,dt)
    # if ( geostaticflag == 1 )
#     field = geostatic(field,par);
# end;
    newfield = field
    return newfield