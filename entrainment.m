function newfield = entrainment(field,par,dt)
%ENTRAINMENT operator accounting for water entrainment at the top of turbidity current
% solved implicitly with a backward Euler scheme (solution obtained
% iteratively from the explicit estimate with a Newton scheme)

% obtain norm and direction vectors:
vel = ( field.u.^2 + field.v.^2 ).^0.5;
% ix = (vel>(par.g*par.h_min)^0.5).* field.u./max(vel,(par.g*par.h_min)^0.5);
% iy = (vel>(par.g*par.h_min)^0.5).* field.v./max(vel,(par.g*par.h_min)^0.5);

% layer depth:
h = field.z_m - field.z_b;

% conserved momentum
MOM = h.*vel;
momx = h.*field.u;
momy = h.*field.v;
% conserved suspended sediments;
SS = h.*field.c_m;

% explicit Richardson number
Ri = par.R*par.g.*field.c_m.*h./max(vel.^2,(par.g*par.h_min));
Ri = max(Ri,0);
%if any(Ri<0); error('negative Ri'); end;

%SOLVE FOR H_NEW (Iterative Newton Scheme, loop 10 times)
% start with explicit estimate
h_new = h + dt.*(0.00153./(0.0204+Ri)).*vel;
C1 = 0.00153*MOM.^3;
C2 = 0.0204*MOM.^2;
C3 = par.R*par.g*SS;
% iterate 10 times with Newton scheme
for i = 1:10;
    warning off;
    dhdt_new = C1./(max(h_new,par.h_min).*(C2+C3.*max(h_new,par.h_min).^2));
    warning on;
    h_new = h + dt.*dhdt_new;
end;
h_new = max(h, h_new);

%retreive other variables from invariants
c_new = max(SS./max(h_new,par.h_min) , 0);
u_new = momx./max(h_new,par.h_min);
v_new = momy./max(h_new,par.h_min);
vel_new = ( u_new.^2 + v_new.^2 ).^0.5;
dhdt_new = (1/dt)*(h_new-h);

% solve for updated K
kh_new = max( h.*field.k_m + dt.*0.5.*dhdt_new.*(vel_new.^2-par.R*par.g.*SS) , 0);
k_new = kh_new./max(h_new,par.h_min);

% final update:
newfield = field;
newfield.u = u_new;
newfield.v = v_new;
newfield.z_m = field.z_b + h_new;
newfield.c_m = c_new;
newfield.k_m = k_new;