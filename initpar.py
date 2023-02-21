import math

# %   universal constants:
g = 3.698  # %[m/s^2] gravitational acceleration [9.81]
nu = 6.5e-7  # % water kinematic viscosity (m^2/s) [is 1e-6]

# %   material parameters:
rho_W = 23.97  # % [kg/m^3] 1000
rho_S = 916  # % [kg/m^3] 2650
rho_WS = 25.3  #
c_b = 0.7  # % [m^3/m^3] sediment concentration in static bed [0.50]
rho_w = rho_W  #
# %   R = (rho_S/rho_W)-1# % excess weight coefficient for the sediments = (rho_S-rho_w)/rho_w [-]
R = (rho_S - rho_WS) / rho_W  #
rPrime = R * c_b  # % excess weight coefficient for the bed load layer
r = 1 + rPrime  # % mult. coefficient accounting for bulk excess weight of the bed load layer
CfStar = 0.005  # % friction parameter
r0 = 1.2  # % multiplicative coefficient for deposition rate [2]
p = 0.07  #
alpha = 0.1  #
D = 20e-6  # % particle diameter 50e-6
Rp = (math.pow((R * g * D), 0.5) * D) / nu  # % Particle Reynolds number
# x = math.log10(Rp^2)
x = math.log10(math.pow(Rp, 2))
# y = -3.76715 + 1.92944*x - 0.09815*x^2 - 0.00575*x^3 + 0.00056*x^4 # what the fuck is this
y = -3.76715 + 1.92944 * x - math.pow(0.09815 * x, 2) - math.pow(0.00575 * x, 3) + math.pow(0.00056 * x, 4)
# Rf = ((10^y)/Rp)^(1/3)
Rf = math.pow(((math.pow(10, y)) / Rp), 1 / 3)
# vs = Rf*(R*g*D)^0.5# % particle fall velocity
vs = Rf * math.pow((R * g * D), 0.5)
v_hemi = 0 * 90e-6  # % rate of aggradation from hemipelagic sediments in-between turbidity current events 1e-5
# %   numerical parameters:
h0 = 300  # % typical depth [m] [10]
h_min = 0.0001 * h0  # % dry bed cutoff depth [m]
courant = 0.9  # % Courant number [-]
