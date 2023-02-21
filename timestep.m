function dt = timestep(field,par)
%TIMESTEP compute time step according to the Courant condition

% cel = ( par.g * max( field.z_m - field.z_b , par.h_min ) ).^0.5;
cel = ( par.R*par.g * field.c_m.* max( field.z_m - field.z_b , par.h_min ) ).^0.5;
vel = (field.u.^2+field.v.^2).^0.5;
speed_max = max( max( vel + cel ) );
dx = field.x(1,2) - field.x(1,1);
%dy = field.y(2,1) - field.y(1,1);
dy = dx;
dl = min( dx , dy );
dt = par.courant * dl / speed_max;
