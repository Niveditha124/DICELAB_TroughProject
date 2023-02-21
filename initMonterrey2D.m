function field = initMonterrey2D(n,par)
%INITFIELD initialise flow field
%
% n = number of cells per unit block length

% initialise flow domain:
x0 = 0;
Lx = 22000; % 1 m
y0 = -2500;
Ly = 5000; % 1 m
dx = Lx/n;
dy=dx;
x = (x0-0.5*dx):dx:(x0+Lx+0.5*dx);
y = (y0-0.5*dy):dy:(y0+Ly+0.5*dy);
field.x = ones(length(y),1) * x;
field.y = y' * ones(1,length(x));

% top of turbid layer:
field.z_m = ones( size(field.x) )*-1000;%.001;
% field.z_m(field.x<0) = 0.75;

% turbid concentration
field.c_m = ones( size(field.x) )*0;%.0001;
% field.c_m(field.x<0) = 0.2;

% turbulent kinetic energy
field.k_m = ones( size(field.x) )*0;%.0001;

% rigid channel bottom under sediment bed:
field.z_r = ones( size(field.x) )*-2000; % default
field.z_r(field.x>21000) = -1000;

% sediment bed level:
field.z_b = ones( size(field.x) )*-1000; % default
% known points for interpolation
xx = [-1e99 0 6000 21000 21001 1e99];
zz = [0 0 -78  -123  -1000 -1000];
field.z_b = ones(length(field.x(:,1)),1) * interp1(xx,zz,field.x(1,:));
% rigid rim around domain:
field.z_r([1 end],:) = 1000;
field.z_r(:,[1 end]) = 1000;

% upstream inflow section
y_inflow = [-250 250];
% upstream inflow section
field.U_up = 3.5;
field.H_up = 20;
field.C_up = 0.01;
field.Q_up = field.H_up*field.U_up;
field.K_up = par.CfStar/par.alpha*field.U_up^2; % assume turbulence is fully developed at inflow
field.iy_inflow = find((field.y(:,1)>=y_inflow(1))&(field.y(:,1)<=y_inflow(2)));
n_inflow = length(field.iy_inflow);
% remove rim at inflow
field.z_r(field.iy_inflow,1) = field.z_r(field.iy_inflow,2);
% incise initial channel
field.z_b(field.iy_inflow,:) = field.z_b(field.iy_inflow,:)-40;


% z-ordering condition:
field.z_b = max( field.z_b , field.z_r );
field.z_m = max( field.z_m , field.z_b );

% velocities:
field.u = zeros( size(field.x) );
field.v = zeros( size(field.x) );

% time:
% -----
field.t = 0;
