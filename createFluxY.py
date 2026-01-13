import numpy as np

class createFluxY:
    
    def __init__(self, field):
        s = (2, field.s)     
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

        s = field.s
        mu = np.ones((s+1, 1))

        y = np.array(range(s+1,0,-1))
        i = 0
        while i < s:
            mu[i][0] = abs(np.random.rand()*(y[i]/100))
            #mu[i][0] = (1- np.log(y[i]))
            #mu[i][0] = 5*(np.log(y[i]))
            #mu[i][0] = -np.exp(y[i])s
            i=i+1

        self.mu = mu
