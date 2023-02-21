function newfield = friction(field,par,dt)
%FRICTION frictional operator accounting for shear stress between between turbidity current and bed
%
% Note: assumes that h is invariant

% obtain norm and direction vectors:
vel = ( field.u.^2 + field.v.^2 ).^0.5;
ix = (vel>(par.g*par.h_min)^0.5).* field.u./max(vel,(par.g*par.h_min)^0.5);
iy = (vel>(par.g*par.h_min)^0.5).* field.v./max(vel,(par.g*par.h_min)^0.5);

% layer depths:
h = field.z_m - field.z_b;
% solve for U and K (assumes h is invariant)
% start with explicit solution
vel_new = vel - dt*par.alpha.*field.k_m./max(h,par.h_min);
K_new = max( 0 , field.k_m./(1-par.alpha*dt.*vel_new./max(h,par.h_min)));
% iterate by looping 10 times on vel and K updates
for i=1:10
    vel_new = vel - dt*par.alpha.*K_new./max(h,par.h_min);
    K_new = max( 0 , field.k_m./(1-par.alpha*dt.*vel_new./max(h,par.h_min)));
end;

% final update
% redecompose velocity into x and y components and update field
% (special assignment needed to avoid zeroing small velocities)
newfield = field;
newfield.u = field.u + ix.*( vel_new - vel ); 
newfield.v = field.v + iy.*( vel_new - vel ); 

newfield.k_m = K_new;
