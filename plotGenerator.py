import math
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import seaborn as sns
import matplotlib 


past_x = []
past_y = []
colors = []

def generate_flowprofile(field, field_0, filepath):
        '''Function generates the flow profile graph to predetermined directory. Change directory in this method directly'''

        

        x1 = field.x[0]
        y1 = field_0.z_b[0]
        x2 = field.x[0]
        y2 = field.z_b[0]
        x3 = field.x[0]
        y3 = field.z_m[0]

        # -------------------------------------------------     FLOW PROFILE GRAPH       ------------------------------------------------- #
        idx = np.argmax(x1 >= 1000)
        plt.plot(x1[idx:], y1[idx:], color=(0.7, 0.7, 0.7))
        plt.plot(x2[idx:], y2[idx:], color='r')
        if field.f == 1:
            plt.plot(x3[idx:], y3[idx:], color='b')
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.xlabel('field.x (m)')
        plt.ylabel('(m)')
        title = 'flow profile, t = ' + str(math.floor(field.t/3600))
        plt.title(title)
        '''if field.h == 0 & field.f == 0:
            plt.text(1, 1, "hemi & flow off", transform=plt.gca().transAxes,ha='right', va='top')
        if field.h == 0 & field.f == 1:
            plt.text(1, 1, "hemi off, flow on", transform=plt.gca().transAxes,ha='right', va='top')
        if field.h == 1 & field.f == 1:
            plt.text(1, 1, "hemi & flow on", transform=plt.gca().transAxes,ha='right', va='top')
        if field.h == 1 & field.f == 0:
            plt.text(1, 1, "hemi on, flow off", transform=plt.gca().transAxes,ha='right', va='top')'''

        # Save the plot as a PNG image
        #plt.xlim(1000,40000)
        #plt.ylim(-300, 2500)
        #plt.ylim(-500,250)
        plt.savefig(filepath)
        plt.close()  # Close the figure to clear it for the next run

def generate_flowprofilecontour(field, field_0, filepath):
    x = field.x[0]          
    y = field.z_b[0]        
    y2 = field.z_m[0]       
    if field.f == 0: 
        nu2d = np.ones((field.s,field.s))
    else:
        nu2d = field.nu2d       

    global past_x, past_y, colors
    past_x.append(x)
    past_y.append(y)

    sns.set_theme(style="whitegrid", context="talk")
    plt.figure(figsize=(18, 10))
    cmap = matplotlib.colormaps.get_cmap('RdGy')


    for i in range(len(past_x)):
        if i == len(past_x) - 1:
            color = cmap(np.random.rand())
            colors.append(color)
        else:
            color = colors[i]
            y_clipped = np.minimum(past_y[i], y)
            sns.lineplot(x=past_x[i], y=y_clipped, linewidth=3,
                         color=color, alpha=0.7)

    J = nu2d.shape[0]                     
    frac = np.linspace(0, 1, J)[:, None]   
    Ygrid = y + frac * (y2 - y)           
    Xgrid = np.tile(x[None, :], (J, 1))    


    mask = (Ygrid < y) | (Ygrid > y2)      
    nu_masked = np.ma.masked_where(mask, nu2d)

    contour = plt.contourf(Xgrid, Ygrid, nu_masked,
                           cmap='GnBu', levels=50)
    cbar = plt.colorbar(contour)
    cbar.set_label('flow density (nu)')

    sns.lineplot(x=x, y=y2, color='b', linewidth=2.5, label='Flow Surface')
    sns.lineplot(x=x, y=y, color='black', linewidth=3, label='Bed Elevation')

    plt.xlabel('field.x (m)')
    plt.ylabel('(m)')
    #plt.ylim(-0, 900)
    #plt.xlim(0, 20000)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()






def generate_iacbchanges(field, field_prev, field_0, dt, filepath):
    '''Function generates the instant and cumulative bed changes graph to predetermined directory. Change directory in this method directly'''

    plt.title('Instant and cumul. bed changes')
    plot1 = (field.z_b - field_prev.z_b) / dt
    plot2 = field.z_b - field_0.z_b
    plt.plot(field.x[0], plot1[0], color='blue', label='Left Y-axis')
    plt.xlabel('field.x (m)')
    plt.ylabel('', color='blue')
    plt.tick_params(axis='y', colors='blue')
    ax2 = plt.twinx()
    ax2.plot(field.x[0], plot2[0], color='red', label='Right Y-axis')
    ax2.set_ylabel('', color='red')
    ax2.tick_params(axis='y', colors='red')
    plt.savefig(filepath)
    plt.close()  # Close the figure to clear it for the next run


def generate_kfrprofile(field, par, filepath):
    '''Function generates the K and Fr profiles graph to predetermined directory. Change directory in this method directly'''

    plt.title('K and Fr profiles')
    plt.plot(field.x[0], field.k_m[0], color='blue', label='Left Y-axis')
    plt.xlabel('field.x (m)')
    plt.ylabel('K (J/Kg)', color='blue')
    plt.tick_params(axis='y', colors='blue')
    ax2 = plt.twinx()
    # (h) calculates current flow depth/thickness
    # calculates the depth of each layer (h) by subtracting the bottom elevation (z_b) from the midpoint elevation (z_m)
    h = field.z_m - field.z_b
    # the Richardson number (Ri) is a dimensionless number used to predict the likelihood of turbulence within the fluid flow of these turbidity currents
    # the np.maximum() function ensures Richardson number is non-negative, and negates the possibilty of undefined behavior
    Ri = par.R * par.g * field.c_m * h / np.maximum(field.u**2, (par.g * par.h_min))
    # Froude Number, perdicts the transition from supercritical flow (Fr>1) to subcritical folw (Fr<1)
    Fr = np.sqrt(1.0 / np.maximum(Ri, 1e-10))
    ax2.plot(field.x[0], Fr[0], color='red', label='Right Y-axis')
    ax2.set_ylabel('Fr', color='red')
    ax2.tick_params(axis='y', colors='red')
    plt.savefig(filepath)
    plt.close()  # Close the figure to clear it for the next run



def generate_ucprofile(field, filepath):
    '''Function generates the U and C profiles graph to predetermined directory. Change directory in this method directly'''

    plt.title('U and C profiles')
    plt.plot(field.x[0], field.u[0], color='blue', label='Left Y-axis')
    plt.xlabel('field.x (m)')
    plt.ylabel('field.u (m/s)', color='blue')
    plt.tick_params(axis='y', colors='blue')
    ax2 = plt.twinx()
    ax2.plot(field.x[0], field.c_m[0], color='red', label='Right Y-axis')
    ax2.set_ylabel('field.c_m', color='red')
    ax2.tick_params(axis='y', colors='red')
    plt.savefig(filepath)
    plt.close()  # Close the figure to clear it for the next run
