import numpy as np
from numpy import argwhere
from numpy import interp
from scipy.interpolate import interp1d


class field:
    p3 = 0
    p2 = 0
    p1 = 0
    L3 = 5000
    # L2 = 6000
    L2 = 15000
    # L1 = 6000
    L1 = 15000
    Lx = L1 + L2 + L3
    S3 = 0
    # S2 = 0.006
    S2 = 0.003
    # S1 = 0.013
    S1 = 0.003
    x0 = - L1
    n = 200
    dx = Lx / n
    dy = dx
    x = np.arange((x0 - 0.5 * dx), (x0 + Lx + 0.5 * dx) + dx, dx)
    y = [1]
    x = np.ones((len(y), 1)) * x
    y = np.transpose(y) * np.ones((1, x.size))
    y0 = 0
    Ly = 0.5
    k_m = np.ones((x.shape[0], x.shape[1])) * 0
    z_r = np.ones((x.shape[0], x.shape[1])) * - 2000
    z_b = np.ones((x.shape[0], x.shape[1])) * - 1000
    z_m = np.ones((x.shape[0], x.shape[1])) * - 1000
    c_m = np.ones((x.shape[0], x.shape[1])) * 0
    v = np.zeros((x.shape[0], x.shape[1]))
    u = np.zeros((x.shape[0], x.shape[1]))
    # z_r[-1, -1 - 2] = -1000
    z_r[0][-3:] = -1000 

    xx = np.array([- L1, 0, L2, L2 + L3])
    zz = np.array([L1 * S1, 0, - L2 * S2, - L2 * S2 - L3 * S3])
    set_interp = interp1d(xx, zz, kind='linear', fill_value='extrapolate')
    z_b = set_interp(x)
    # z_b[-1, -1 - 2] = -1000
    z_b[0][-3:] = -1000
    z_r[0][-1] = 1000
    isX1 = np.argwhere(np.logical_and((x[0] > -L1), (x[0] < 0)))
    isX2 = np.argwhere(np.logical_and((x[0] > 0), (x[0] < L2)))
    isX3 = np.argwhere(np.logical_and((x[0] > L2), (x[0] < (L2 + L3))))
    randno = np.random.random()
    for i in isX1:
        sX1 = i[0]
        sX1 = sX1 - 1
        z_b[0, sX1] = z_b[0, sX1] + (randno * p1 - p1 / 2)
    for i in isX2:
        sX2 = i[0]
        sX2 = sX2 - 1
        z_b[0, sX2] = z_b[0, sX2] + (randno * p2 - p2 / 2)
    for i in isX3:
        sX3 = i[0]
        sX3 = sX3 - 1
        z_b[0, sX3] = z_b[0, sX3] + (randno * p3 - p3 / 2)
    z_b = np.maximum(z_b, z_r)
    z_m = np.maximum(z_m, z_b)
    t = 0
    H_up = 60
    C_up = 0.333
    U_up = 1
    Q_up = H_up * U_up
    K_up = 0


    def __init__(self, n, par):
        self.L1 = 6000
        self.S1 = 0.013
        self.p1 = 0
        self.L2 = 6000
        self.S2 = 0.006
        self.p2 = 0
        self.L3 = 5000
        self.S3 = 0
        self.p3 = 0
        self.n = n
        self.par = par
        self.field = field
        self.x = field.x
        self.v = field.v
        self.u = field.u
        self.c_m = field.c_m
        self.z_b = field.z_b
        self.z_m = field.z_m
        self.k_m = field.k_m
        self.z_r = field.z_r
        self.Q_up = field.Q_up
        self.H_up = field.H_up
        self.C_up = field.C_up
        self.U_up = field.U_up
        self.K_up = field.K_up
        self.t = field.t

    def init1D(self, n, par):

        S1 = field.S1
        S2 = field.S2
        S3 = field.S3
        L1 = field.L1
        L2 = field.L2
        L3 = field.L3
        pert1 = field.p1
        pert2 = field.p2
        pert3 = field.p3
        # initialise flow domain:
        # x0 = - L1
        # Lx = L1 + L2 + L3
        # y0 = 0
        # Ly = 0.5
        # dx = Lx / field.n
        # dy = dx
        # x = np.arange((x0 - 0.5 * dx), (x0 + Lx + 0.5 * dx) + dx, dx)
        # y = [1]
        # field.x = np.ones((len(field.y), 1)) * field.x
        # field.y = np.transpose(field.y) * np.ones((1, len(field.x)))
        # isX1 = np.argwhere(np.logical_and((field.x[0] > -field.L1), (field.x[0] < 0)))
        # isX2 = np.argwhere(np.logical_and((field.x[0] > 0), (field.x[0] < field.L2)))
        # isX3 = np.argwhere(np.logical_and((field.x[0] > field.L2), (field.x[0] < (field.L2 + field.L3))))
        # top of turbid layer:
        # field.z_m = np.ones((field.x.shape[0], field.x.shape[1])) * - 1000

        # z_m(x<0) = 0.75;

        # turbid concentration
        # field.c_m = np.ones((field.x.shape[0], field.x.shape[1])) * 0

        # c_m(x<0) = 0.2;

        # turbulent kinetic energy
        # field.k_m = np.ones((field.x.shape[1], field.x.shape[1])) * 0

        # rigid channel bottom under sediment bed:
        # field.z_r = np.ones((field.x.shape[0], field.x.shape[1])) * - 2000

        # known points for interpolation
        # xx = [-1e10   0 1e10];
        # zz = [1e10*S1 0 -1e10*S1];
        # z_r = interp1(xx,zz,x);
        # field.z_r[-1, -1 - 2] = -1000
        # sediment bed level:
        # field.z_b = np.ones((field.x.shape[0], field.x.shape[1])) * - 1000
        # known points for interpolation
        # xx = np.array([- L1, 0, L2, L2 + L3])
        # zz = np.array([L1 * S1, 0, - L2 * S2, - L2 * S2 - L3 * S3])
        # set_interp = interp1d(xx, zz, kind='linear', fill_value='extrapolate')
        # field.z_b = set_interp(field.x)
        # field.z_b[-1, -1 - 2] = -1000
        # rigid rim around domain (downstream only):
        # field.z_r[-1, -1] = 1000
        # print(isX1.shape) # (71, 1)
        # print(z_b.shape) # (1, 202)

        # initial bed perturbations

        # upstream inflow section
        field.H_up = 60
        field.C_up = 0.0015
        field.U_up = 1
        # Ri_up = 0.8;
        # U_up = (par.R*par.g*C_up*H_up/Ri_up)^0.5;
        field.Q_up = field.H_up * field.U_up
        field.K_up = par.CfStar / par.alpha * field.U_up ** 2
        # z-ordering condition:
        # field.z_b = np.maximum(field.z_b, field.z_r)
        # field.z_m = np.maximum(field.z_m, field.z_b)
        # velocities:
        # field.u = np.zeros((field.x.shape[0], field.x.shape[1]))
        # field.v = np.zeros((field.x.shape[0], field.x.shape[1]))
        # time:
        # -----
        field.t = 0

