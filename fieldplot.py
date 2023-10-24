import numpy as np
import matplotlib.pyplot as plt



def num2str(i):
    str_i = str(i)
    return str_i


def fieldplot(field=None, field_0=None, field_prev=None, par=None, dt=None):

    # crop out-of-domain regions of the field:
    # field = cropfield(field);
    # set rim to NaN
    field.x[field.z_b == 1000] = float("nan")
    # set pits to NaN
    field.x[field.z_b == - 1000] = float("nan")
    # set flow with negligible concentration to NaN;
    # field.z_m(field.c_m<0.0001)=NaN;

    # GENERAL PLOT PROPERTIES
    ax = np.array([0, 21000, - 200, 100])
    fontsize = 11
    fontweight = 'bold'
    # PLOT PROFILES
    if 1: # full sets of profiles
        # 1. flow profile
        plt.subplot(2, 2, 1)
        plt.plot(field.x, field.z_r, 'k', 'linewidth', 3)
        plt.plot(field.x, field_0.z_b, 'color', np.array([0.7, 0.7, 0.7]), 'linewidth', 3)
        plt.plot(field.x, field.z_b, 'r', 'linewidth', 3)
        plt.plot(field.x, field.z_m, 'b', 'linewidth', 3)
        # setattr(plt.gca, 'fontsize', fontsize, 'fontweight', fontweight)
        plt.gca('fontsize', fontsize, 'fontweight', fontweight)
        plt.title(np.array(['flow profile, t = ', num2str(int(np.floor(field.t / 3600))), ' h.']))
        plt.axis(ax)
        plt.grid(True)
        # 2. velocity profile & concentration profile
        plt.subplot(2, 2, 2)
        #   %   PLOTYY(X1,Y1,X2,Y2) plots Y1 versus X1 with y-axis labeling
        #   %   on the left and plots Y2 versus X2 with y-axis labeling on
        #   %   the right.
        fig, H1 = plt.subplots()
        H2 = H1.twinx()
        H1.plot(field.x, field.u)
        H2.plot(field.x, field.c_m)
        # subax, H1, H2 = plotyy(field.x, field.u, field.x, field.c_m)
        setattr(H1, 'linewidth', 3)
        setattr(H2, 'linewidth', 3)
        setattr(H1, 'fontsize', fontsize)
        setattr(H1, 'fontweight', fontweight)
        setattr(H2, 'fontsize', fontsize)
        setattr(H2, 'fontweight', fontweight)
        plt.title('\color{blue}U\color{black} and \color[rgb]{0 .5 0}C\color{black} profiles')
        setattr(H1, 'xlim', ax[np.arange(0, 2)])
        setattr(H2, 'xlim', ax[np.arange(0, 2)])
        setattr(H1, 'ylim', np.array([0, 4]))
        setattr(H2, 'ylim', np.array([0, 0.016]))
        setattr(H1, 'ytick', np.arange(0, 10 + 0.5, 0.5))
        setattr(H2, 'ytick', np.arange(0, 1 + 0.002, 0.002))
        plt.grid(True)
        # 3. turbulent kinetic energy profile and Froude profile
        plt.subplot(2, 2, 3)
        h = field.z_m - field.z_b
        Ri = np.multiply(np.multiply(par.R * par.g, field.c_m), h) / np.amax(field.u ** 2, (par.g * par.h_min))
        Fr = (1.0 / np.amax(Ri, 1e-10)) ** 0.5
        # subax, H1, H2 = plotyy(field.x, field.k_m, field.x, Fr)
        setattr(H1, 'linewidth', 3)
        setattr(H2, 'linewidth', 3)
        setattr(H1, 'fontsize', fontsize)
        setattr(H1, 'fontweight', fontweight)
        setattr(H2, 'fontsize', fontsize)
        setattr(H2, 'fontweight', fontweight)
        plt.title('\color{blue}K\color{black} and \color[rgb]{0 .5 0}Fr\color{black} profiles')
        setattr(H1, 'xlim', ax[np.arange(1, 2 + 1)])
        setattr(H2, 'xlim', ax[np.arange(1, 2 + 1)])
        setattr(H1, 'ylim', np.array([0, 1]))
        setattr(H1, 'ytick', np.arange(0, 1 + 0.1, 0.1))
        setattr(H2, 'ylim', np.array([0, 2]))
        setattr(H2, 'ytick', np.arange(0, 2 + 0.2, 0.2))
        plt.grid(True)
        # 4. instant and cumulative bed level changes
        plt.subplot(2, 2, 4)
        # subax, H1, H2 = plotyy(field.x, (field.z_b - field_prev.z_b) / dt, field.x, field.z_b - field_0.z_b)
        setattr(H1, 'linewidth', 3)
        setattr(H2, 'linewidth', 3)
        setattr(H1, 'fontsize', fontsize)
        setattr(H1, 'fontweight', fontweight)
        setattr(H2, 'fontsize', fontsize)
        setattr(H2, 'fontweight', fontweight)
        plt.title('\color{blue}Instant.\color{black} and \color[rgb]{0 .5 0}cumul.\color{black} bed changes')
        setattr(H1, 'xlim', ax[np.arange(0, 2)])
        setattr(H2, 'xlim', ax[np.arange(0, 2)])
        plt.grid(True)
    else:
        plt.hold(False)
        plt.plot(field.x, field.z_r, 'k')
        plt.hold(True)
        plt.plot(field.x, field.z_b, 'r')
        plt.plot(field.x, field.z_m, 'b')
        plt.title(np.array(['flow profile, t = ', num2str(int(np.floor(field.t))), ' s.']))
        setattr(gca, 'fontsize', fontsize, 'fontweight', fontweight)
        setattr(gca, 'fontsize', fontsize, 'fontweight', fontweight)
        plt.axis(ax)

    # setattr(ax(2),'ylim',[0 4],'ytick',0:0.5:4);

    plt.show()
