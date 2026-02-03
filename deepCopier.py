import copy
import init1D

def deep_copy(field: init1D.field, newfield: init1D.field):
    n = field.n
    par = field.par
    
    newfield = init1D.field(n, par)
    
    newfield.x = copy.deepcopy(field.x)
    newfield.y = copy.deepcopy(field.y)
    newfield.z_m = copy.deepcopy(field.z_m)
    newfield.c_m = copy.deepcopy(field.c_m)
    newfield.k_m = copy.deepcopy(field.k_m)
    newfield.z_r = copy.deepcopy(field.z_r)
    newfield.z_b = copy.deepcopy(field.z_b)
    newfield.u = copy.deepcopy(field.u)
    newfield.v = copy.deepcopy(field.v)


    
    newfield.L = copy.deepcopy(field.L)
    newfield.S = copy.deepcopy(field.S)
    newfield.p = copy.deepcopy(field.p)


    newfield.n = copy.deepcopy(field.n)
    newfield.U_up = copy.deepcopy(field.U_up)
    newfield.H_up = copy.deepcopy(field.H_up)
    newfield.C_up = copy.deepcopy(field.C_up)
    newfield.Q_up = copy.deepcopy(field.Q_up)
    newfield.K_up = copy.deepcopy(field.K_up)
    newfield.t = copy.deepcopy(field.t)
    newfield.s = copy.deepcopy(field.s)
    newfield.nu = copy.deepcopy(field.nu)
    newfield.nu2d = copy.deepcopy(field.nu2d)
    newfield.f = copy.deepcopy(field.f)
    newfield.h = copy.deepcopy(field.h)
    
    return newfield

 
