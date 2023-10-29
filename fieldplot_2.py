import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time


# converting a number to a string
def num2str(i):
    str_i = str(i)
    return str_i

# generating a field plot
def fieldplot_2(figure, ax, line1, test, field=None, field_0=None, field_prev=None, par=None, dt=None):

    # crop out-of-domain regions of the field:
    # field = cropfield(field);
    # set rim to NaN
    # field.x[field.z_b == 1000] = float("nan")
    field.x[field.z_b == 1000] = np.nan
    # set pits to NaN
    # field.x[field.z_b == - 1000] = float("nan")
    field.x[field.z_b == -1000] = np.nan
    # set flow with negligible concentration to NaN;
    # field.z_m(field.c_m<0.0001)=NaN;

    # GENERAL PLOT PROPERTIES
    ax = np.array([0, 21000, - 200, 100])
    fontsize = 11
    fontweight = 'bold'
    # PLOT PROFILES
    if 1:
        # 1. flow profile
        '''
        plt.subplot(2, 2, 1)
        plt.plot(field.x, field.z_r, 'k', linewidth=3)
        # setattr(plt.gca, 'fontsize', fontsize, 'fontweight', fontweight)
        plt.rcParams['font.size'] = 11
        plt.rcParams['font.weight'] = 'bold'
        # plt.title(np.array(['flow profile, t = ', num2str(int(np.floor(field.t / 3600))), ' h.']))
        plt.title('Hello world!')
        plt.axis(ax)
        plt.grid(True)
        '''
        line1.set_xdata(np.arange(1000000))
        line1.set_ydata(test)
        # updates the data of the plot line 
        figure.canvas.draw()
        figure.canvas.flush_events()
        time.sleep(0.1)
        
    else:
        # plotting the flow profile
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

