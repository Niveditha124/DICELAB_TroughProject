import numpy as np

class createFluxY:
    
    def __init__(self, field):
        s = (2,202)
        self.q_m = np.zeros(s)
        self.sig_l = np.zeros(s)
        self.sig_r = np.zeros(s)
        self.sigCross = np.zeros(s)
        self.mu = np.zeros(s)
        self.kh = np.zeros(s)
        self.z_ml = np.array([[1], [1]]) * field.z_m
        self.z_mr = np.array([[1], [1]]) * field.z_m
        self.z_bl = np.array([[1], [1]]) * field.z_b
        self.z_br = np.array([[1], [1]]) * field.z_b

