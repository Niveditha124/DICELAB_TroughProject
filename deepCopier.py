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
    
    # Integers should auto deep copy I think
    # newfield.L1 = copy.deepcopy(field.L1)
    # newfield.S1 = copy.deepcopy(field.S1)
    # newfield.p1 = copy.deepcopy(field.p1)
    # newfield.L2 = copy.deepcopy(field.L2)
    # newfield.S2 = copy.deepcopy(field.S2)
    # newfield.p2 = copy.deepcopy(field.p2)
    # newfield.L3 = copy.deepcopy(field.L3)
    # newfield.S3 = copy.deepcopy(field.S3)
    # newfield.p3 = copy.deepcopy(field.p3)
    
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
    
    return newfield

 