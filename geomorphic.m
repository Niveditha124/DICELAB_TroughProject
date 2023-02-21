function newfield = geomorphic(field,par,dt)
%GEOMORPHIC operator accounting for bed erosion/deposition

% obtain norm and direction vectors:
vel = ( field.u.^2 + field.v.^2 ).^0.5;
ix = (vel>(par.g*par.h_min)^0.5).* field.u./max(vel,(par.g*par.h_min)^0.5);
iy = (vel>(par.g*par.h_min)^0.5).* field.v./max(vel,(par.g*par.h_min)^0.5);
% layer depths:
h = field.z_m - field.z_b;

% moving sediments
CH = h.*field.c_m;
%KH
KH = h.*field.k_m;

% SOLVE FOR CH
% start with explicit estimate
  Ze5 = ((par.alpha*field.k_m).^0.5/par.vs.*par.Rp^0.6.*((par.alpha*field.k_m).^0.5./par.g./max(h,par.h_min)).^0.08).^5;
  E = max( par.p*1.3e-7*par.vs*Ze5./(1+1.3e-7/0.3*Ze5) , 0 );
  D = max( par.vs*par.r0*field.c_m , 0 );
  CH_new = max(CH + dt*(E-D) , 0);
  h_new = max (h + dt/par.c_b*(E-D) , 0);
  C_new = max(CH_new./max(h_new,par.h_min) , 0);
  KH_new = KH - dt*0.5*par.R*par.g.*h_new.*(E-D);
  K_new = max(0 , KH_new./max(h_new,par.h_min));
% iterate 10 times with Newton scheme
if 1
for i = 1:10;
    Ze5 = ((par.alpha*K_new).^0.5/par.vs.*par.Rp^0.6.*((par.alpha*K_new).^0.5./par.g./max(h_new,par.h_min)).^0.08).^5;
    E = max( par.p*1.3e-7*par.vs*Ze5./(1+1.3e-7/0.3*Ze5) , 0 );
    D = max( par.vs*par.r0*C_new , 0 );
    CH_new = max(CH + dt*(E-D) , 0);
    h_new = max (h + dt/par.c_b*(E-D) , 0);
    C_new = max(CH_new./max(h_new,par.h_min) , 0);
    KH_new = KH - dt*0.5*par.R*par.g.*h_new.*(E-D);
    K_new = max(0 , KH_new./max(h_new,par.h_min));
end;
end;

% ensure dissipation of K (should we do that?)
% K_new = min(field.k_m, K_new);

% retrieve bed level change and impose limit. dzb is positive in case of deposition
dzb = min(dt.*(D-E)./par.c_b , (field.z_m-field.z_b).*field.c_m./par.c_b); % limited by deposition of all suspended sediments
dzb = max(dzb,field.z_r-field.z_b); % limit by rigid bottom

% retrieve all conservative variables from final bed level change
h_new = h-dzb;
CH_new = min(max(CH - dzb.*par.c_b , 0) , h_new) ;
KH_new = max(KH + 0.5*par.R*par.g.*h_new*par.c_b.*dzb , 0);

% Note 1: implication of erosion/deposition on momentum transfer to/from the
% bed is neglected.

% Note 2: Should we forbid a net gain in K in case of deposition?

% final update:
newfield = field;
newfield.z_b = field.z_b + dzb;
newfield.c_m = min ( max(CH_new./max(h_new,par.h_min) , 0) , 1);
newfield.c_m(h_new<par.h_min)=field.c_m(h_new<par.h_min); % do not change concentration where flow depth is about zero
newfield.k_m = max(KH_new./max(h_new,par.h_min) , 0);