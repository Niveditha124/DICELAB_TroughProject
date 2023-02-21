function flux = fluxLHLL(field,grad,par,dt);
%FLUXLHLL Approximate Riemann solver of Harten, Lax and Van Leer (1983) with lateralised momentum flux

% extrapolations left and right (in face-centred variables):
[m n] = size(field.x);
dx = field.x(1,2) - field.x(1,1);
h_m = field.z_m - field.z_b;

h_ml = h_m(:,1:n-1) + 0.5*grad.dh_m(:,1:n-1); 
h_mr = h_m(:,2:n) - 0.5*grad.dh_m(:,2:n);
mu = h_m.*field.c_m;
mu_l = mu(:,1:n-1) + 0.5*grad.dmu(:,1:n-1); 
mu_r = mu(:,2:n) - 0.5*grad.dmu(:,2:n);
kh = h_m.*field.k_m;
kh_l = kh(:,1:n-1) + 0.5*grad.dkh(:,1:n-1); 
kh_r = kh(:,2:n) - 0.5*grad.dkh(:,2:n);
z_bl = field.z_b(:,1:n-1) + 0.5*grad.dz_b(:,1:n-1); 
z_br = field.z_b(:,2:n) - 0.5*grad.dz_b(:,2:n);
q_m = h_m.*field.u;
q_ml = q_m(:,1:n-1) + 0.5*grad.dqx_m(:,1:n-1);
q_mr = q_m(:,2:n) - 0.5*grad.dqx_m(:,2:n);
qy_m = h_m.*field.v;
qy_ml = qy_m(:,1:n-1) + 0.5*grad.dqy_m(:,1:n-1);
qy_mr = qy_m(:,2:n) - 0.5*grad.dqy_m(:,2:n);


% positivity constraint on mu and kh
mu_l = max( mu_l , 0 );
mu_r = max( mu_r , 0 );
kh_l = max( kh_l , 0 );
kh_r = max( kh_r , 0 );

% retrieve primitive variables:
z_ml = z_bl + h_ml; z_mr = z_br + h_mr;
u_l = (h_ml>=par.h_min) .* q_ml ./ max( h_ml , par.h_min );
u_r = (h_mr>=par.h_min) .* q_mr ./ max( h_mr , par.h_min );
v_l = (h_ml>=par.h_min) .* qy_ml ./ max( h_ml , par.h_min );
v_r = (h_mr>=par.h_min) .* qy_mr ./ max( h_mr , par.h_min );
c_ml = (h_ml>=par.h_min) .* mu_l ./ max( h_ml , par.h_min );
c_mr = (h_mr>=par.h_min) .* mu_r ./ max( h_mr , par.h_min );
k_ml = (h_ml>=par.h_min) .* kh_l ./ max( h_ml , par.h_min );
k_mr = (h_mr>=par.h_min) .* kh_r ./ max( h_mr , par.h_min );
% left and right fluxes:
sig_l = h_ml.*u_l.^2 + 0.5*par.g*par.R*(c_ml.*h_ml.^2);
sig_r = h_mr.*u_r.^2 + 0.5*par.g*par.R*(c_mr.*h_mr.^2);

% wavespeeds:
h_l = max( z_ml - z_bl , 0 );
SLl = min( u_l - (par.g*par.R*h_l.*c_ml).^0.5 , 0 );
SRl = max( u_l + (par.g*par.R*h_l.*c_ml).^0.5 , 0 );
h_r = max( z_mr - z_br , 0 );
SLr = min( u_r - (par.g*par.R*h_r.*c_mr).^0.5 , 0 );
SRr = max( u_r + (par.g*par.R*h_r.*c_mr).^0.5 , 0 );

% extreme wave speeds:
SL = min( min( SLl , SLr ) , 0 );
SR = max( max( SRl , SRr ) , 0 );
prod = 1./ max( SR - SL , (par.g*par.h_min)^0.5 );

% canonical HLL statement for discharge:
q_m_star = ( SR.*q_ml - SL.*q_mr + SL.*SR.*(z_mr-z_ml) ).* prod;

% anti-emptying constraint:
q_m_star_min = -h_mr*dx/dt;
q_m_star_max =  h_ml*dx/dt;
q_m_star = min( max( q_m_star_min , q_m_star ) , q_m_star_max );

% canonical HLL statement for momentum:
sig_star = ( SR.*sig_l - SL.*sig_r + SL.*SR.*(q_mr-q_ml) ).* prod;

% momentum flux lateralisation:      
Cmhm_mean = 0.5*(c_ml.*h_ml+c_mr.*h_mr);
sig_starl = sig_star - prod .* SL .* par.R*par.g.*Cmhm_mean.*(z_br-z_bl);
sig_starr = sig_star - prod .* SR .* par.R*par.g.*Cmhm_mean.*(z_br-z_bl);

% exceptions at internal reflecting boundaries:
% SHOULD STILL CHECK THAT
e = ( ( (par.g*z_ml+0.5*u_l.^2) < par.g*z_br ) & ( h_mr < par.h_min ) );
q_m_star = (~e).*q_m_star;
sig_starl = (~e).*sig_starl + e.*( sig_l - 2*SL.*SR.*q_ml.*prod );
sig_starr = (~e).*sig_starr;

e = ( ( (par.g*z_mr+0.5*u_r.^2) < par.g*z_ml ) & ( h_ml < par.h_min ) );
q_m_star = (~e).*q_m_star;
sig_starl = (~e).*sig_starl;
sig_starr = (~e).*sig_starr + e.*( sig_r + 2*SL.*SR.*q_mr.*prod );

% upwind momentum cross-flux:
sigCross_star = ( (q_m_star>0).* v_l + (~(q_m_star>0)).* v_r ) .* (q_m_star);

% upwind concentration flux:
mu_star = ( (q_m_star>0).* c_ml + (~(q_m_star>0)).* c_mr ) .* (q_m_star);

% upwind turbulent kinetic energy flux:
kh_star = ( (q_m_star>0).* k_ml + (~(q_m_star>0)).* k_mr ) .* (q_m_star);

% anti-emptying constraint:
mu_star_min = -h_mr.*c_mr*dx/dt;
mu_star_max =  h_ml.*c_ml*dx/dt;
mu_star = min( max( mu_star_min , mu_star ) , mu_star_max );
kh_star_min = -h_mr.*k_mr*dx/dt;
kh_star_max =  h_ml.*k_ml*dx/dt;
kh_star = min( max( kh_star_min , kh_star ) , kh_star_max );


% final assignement:
flux.q_m = q_m_star;
flux.sig_l = sig_starl;
flux.sig_r = sig_starr;
flux.sigCross = sigCross_star;
flux.mu = mu_star;
flux.kh = kh_star;
flux.z_ml = z_ml;
flux.z_mr = z_mr;
flux.z_bl = z_bl;
flux.z_br = z_br;
%flux.c_ml = c_ml;
%flux.c_mr = c_mr;
