function bcflux = bc_1D(flux,field,par)
% impose upstream boundary condition in geoflood1D

bcflux = flux;
% correct fluxes at upstream inflow section
s = 0.*field.Q_up;  % scale factor incoming flux [0.1]

bcflux.q_m(1) = field.Q_up;
%bcflux.g_m(1) = s;  (apparently no change)
bcflux.sig_r(1) = field.H_up*field.U_up^2 + 0.5*par.g*par.R*(field.C_up*field.H_up^2);
bcflux.mu(1) = field.C_up*field.Q_up;
bcflux.kh(1) = field.K_up*field.Q_up;
