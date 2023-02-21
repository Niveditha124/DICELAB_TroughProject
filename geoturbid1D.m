%GEOTURBID
%
% Shallow-Water code for turbidity currents
% based on Parker et al 4-eq model
% two-dimensional, single turbid layer, second-order version
% 
% Prepared by Benoit Spinewine (spinewine@gmail.com)

% initialisation:
run = initrun; % run parameters
n = run.n; % discretisation
o = run.o; % order of the scheme (1 or 2)
par = initpar; % material and numerical parameters
field = initMonterrey(n,par); % flow field (including time t)
field_0 = field;
field_prev = field;

% disk output and screen display parameters:
%t0 = (par.h0/par.g)^0.5;
t_end = run.t_end; 
dt_output = run.dt_output;
t_output = 0:dt_output:t_end;
i_output = 1;

% prepare graphics:
%figure;

% main loop:
firstTimeStep = 1;
% continue previous run
% load field_202;
% i_output = 203;
% firstTimeStep = 0;
iter = 1; % for predictor-corrector
while field.t<t_end
    if (o==1) | ((o==2)&(rem(iter,2)==1))
        dt = timestep(field,par); % timestep evaluation
        if firstTimeStep; dt = min(dt,0.1); firstTimeStep = 0; end;
        %disp(['t = ' num2str(field.t) ' [sec]']); % time display
    end;
    % empty outflowing pit
    field.z_b(field.z_r==-1000) = field.z_r(field.z_r==-1000);
    field.z_m(field.z_r==-1000) = field.z_r(field.z_r==-1000);
    field.u(field.z_r==-1000) = 0;
    field.v(field.z_r==-1000) = 0;
    field.c_m(field.z_r==-1000) = 0;
    field.k_m(field.z_r==-1000) = 0;
    % screen display:
    if ( (o==1) | ((o==2)&(rem(iter,2)==1)) )
        if run.dispflag == 1
           fieldplot(field,field_0,field_prev,par,dt);
%            pause;
        end;
    end;
    % disk output:
    if ( (o==1) | ((o==2)&(rem(iter,2)==1)) ) ...
       & ( (i_output<=length(t_output))&((field.t+dt)>t_output(i_output)) )
        eval(['save field_' tag2str(i_output-1) ' field field_0 field_prev dt']);
        fieldplot(field,field_0,field_prev,par,dt);
%         eval(['print -djpeg95 view_' tag2str(i_output-1)]);
%         saveas(gcf,['view_' tag2str(i_output-1)],'fig');
        i_output = i_output + 1;
    end;
    % book-keeping
    field_prev = field;
    % half-step relaxation operator:
    if (o==2)&(rem(iter,2)==1)
        field = relax(field,par,0.5*dt,run.geostaticflag);
    end;
    % extend field left and right:
    field_x = mirror(field);
%    field_y = mirror(swapfield(field));
    % computation of in-cell gradients:
    % note: cell slopes are NOT recomputed for the second step of the predictor-corrector    
    if ( (o==1) | ((o==2)&(rem(iter,2)==1)) ) 
        grad_x = gradientVL(field_x,par,o);
%        grad_y = gradientVL(field_y,par,o);
    end;
    % fluxing scheme (LHLL):
    flux_x = fluxLHLL(field_x,grad_x,par,dt);
    % impose BC at upstream inflow section
    flux_x = bc_1D(flux_x,field,par);
%    flux_y = swapflux(fluxLHLL(field_y,grad_y,par,dt));
    % 1D default:
    flux_y.q_m = zeros(2,length(field.x));
    flux_y.sig_l = zeros(2,length(field.x));
    flux_y.sig_r = zeros(2,length(field.x));
    flux_y.sigCross = zeros(2,length(field.x));
    flux_y.mu = zeros(2,length(field.x));
    flux_y.kh = zeros(2,length(field.x));
    flux_y.z_ml = [1 1]' * field.z_m;
    flux_y.z_mr = [1 1]' * field.z_m;
    flux_y.z_bl = [1 1]' * field.z_b;
    flux_y.z_br = [1 1]' * field.z_b;

    % hyperbolic operator:
    if (o==1)
        % 1st order forward Euler:
        field = hyperbolic(field,flux_x,flux_y,par,dt);
        % relaxation operator:
         field = relax(field,par,dt,run.geostaticflag);
        % time update:
        field.t = field.t + dt;
    elseif (o==2)
        % 2nd order predictor-corrector (Alcrudo & Garcia-Navarro 1993):
        if (rem(iter,2)==1)
            % book-keeping of previous field:
            field_prev = field;
            % predictor step:
            field = hyperbolic(field,flux_x,flux_y,par,0.5*dt);
        else
            % corrector step:
            field = hyperbolic(field_prev,flux_x,flux_y,par,dt);
            % half-step relaxation operator:
             field = relax(field,par,0.5*dt,run.geostaticflag);
            % time update:
            field.t = field.t + dt;
        end;
    end;
    iter = iter + 1;    
end;
