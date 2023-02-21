function newfield = dissipation(field,par,dt)
%DISSIPATION operator accounting for dissipation of K
%
% supposes h&U&C are invariants

% obtain norm of velocity:
vel = ( field.u.^2 + field.v.^2 ).^0.5;
% layer depth:
h = field.z_m - field.z_b;
% Richardson number:
Ri = par.R*par.g.*field.c_m.*h./max(vel.^2,(par.g*par.h_min));
Ri = max(Ri,0);
% Water entrainment rate:
ew = 0.00153./(0.0204+Ri);
% Coefficient of K-dissipation
Beta = (0.5*ew.*(1-Ri-2*par.CfStar/par.alpha)+par.CfStar)/(par.CfStar/par.alpha)^1.5;

% solve for K (assumes h is invariant)
% start with explicit solution
C1 = Beta./max(h,par.h_min);
K_new = max(field.k_m-dt*(C1.*field.k_m.^1.5) , 0);
% iterate by looping 10 times
for i=1:10
    dKdt_new = -C1.*K_new.^1.5;
    K_new = max(field.k_m + dt*dKdt_new , 0);
end;

% final update
newfield = field;
newfield.k_m = K_new;
