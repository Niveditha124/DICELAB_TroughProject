function par = initpar;

% universal constants:
par.g = 3.698; % [m/s^2] gravitational acceleration [9.81]
par.nu = 6.5e-7; % water kinematic viscosity (m^2/s) [is 1e-6]

% material parameters:
rho_W = 23.97; % [kg/m^3] 1000
rho_S = 916; % [kg/m^3] 2650
rho_WS = 25.3
par.c_b = 0.7; % [m^3/m^3] sediment concentration in static bed [0.50]
par.rho_w = rho_W;
%par.R = (rho_S/rho_W)-1; % excess weight coefficient for the sediments = (rho_S-rho_w)/rho_w [-]
par.R = (rho_S - rho_WS)/rho_W;
rPrime = par.R * par.c_b; % excess weight coefficient for the bed load layer
par.r = 1 + rPrime; % mult. coefficient accounting for bulk excess weight of the bed load layer
par.CfStar = 0.005; % friction parameter
par.r0 = 1.2; % multiplicative coefficient for deposition rate [2]
par.p = 0.07;
par.alpha = 0.1;
par.D = 20e-6 ; % particle diameter 50e-6
par.Rp = (par.R*par.g*par.D)^0.5*par.D/par.nu; % Particle Reynolds number
x = log10(par.Rp^2);
y = -3.76715 + 1.92944*x - 0.09815*x^2 - 0.00575*x^3 + 0.00056*x^4;
Rf = ((10^y)/par.Rp)^(1/3);
par.vs = Rf*(par.R*par.g*par.D)^0.5 % particle fall velocity
par.v_hemi = 0*90e-6; % rate of aggradation from hemipelagic sediments in-between turbidity current events 1e-5
% numerical parameters: 
par.h0 = 300; % typical depth [m] [10]
par.h_min = 0.0001 * par.h0; % dry bed cutoff depth [m]
par.courant = 0.9; % Courant number [-]
