function newfield = hyperbolic(field,flux_x,flux_y,par,dt)
%HYPERBOLIC

[m n] = size(field.x);
dx = field.x(1,2) - field.x(1,1);
%dy = field.y(2,1) - field.y(1,1);
dy = dx;
z_m_new = field.z_m + (dt/dx)*( flux_x.q_m(:,1:n) - flux_x.q_m(:,2:n+1) ) ...
                    + (dt/dy)*( flux_y.q_m(1:m,:) - flux_y.q_m(2:m+1,:) );

qm_x = (field.z_m-field.z_b) .* field.u;
qm_x_new = qm_x + (dt/dx)*( flux_x.sig_r(:,1:n) - flux_x.sig_l(:,2:n+1) ) ...
                + (dt/dy)*( flux_y.sigCross(1:m,:) - flux_y.sigCross(2:m+1,:) ) ...
                + (dt/dx)*par.R*par.g* (field.c_m.*(field.z_m-field.z_b)) .* ( flux_x.z_br(:,1:n) - flux_x.z_bl(:,2:n+1) );

qm_y = (field.z_m-field.z_b) .* field.v;
qm_y_new = qm_y + (dt/dx)*( flux_x.sigCross(:,1:n) - flux_x.sigCross(:,2:n+1) ) ...
                + (dt/dy)*( flux_y.sig_r(1:m,:) - flux_y.sig_l(2:m+1,:) ) ...
                + (dt/dy)*par.R*par.g* (field.c_m.*(field.z_m-field.z_b)) .* ( flux_y.z_br(1:m,:) - flux_y.z_bl(2:m+1,:) );

nu = (field.z_m-field.z_b).*field.c_m;
nu_new = nu + (dt/dx)*( flux_x.mu(:,1:n) - flux_x.mu(:,2:n+1) ) ...
            + (dt/dy)*( flux_y.mu(1:m,:) - flux_y.mu(2:m+1,:) );

kh = (field.z_m-field.z_b).*field.k_m;
kh_new = kh + (dt/dx)*( flux_x.kh(:,1:n) - flux_x.kh(:,2:n+1) ) ...
            + (dt/dy)*( flux_y.kh(1:m,:) - flux_y.kh(2:m+1,:) );

% z-ordering condition:
z_m_new = max( z_m_new , field.z_b );
% concentration update:
c_m_new = ((z_m_new-field.z_b)>par.h_min).*nu_new ./ max((z_m_new-field.z_b),par.h_min) + ((z_m_new-field.z_b)<=par.h_min).*field.c_m;
% positivity condition
c_m_new = max( c_m_new , 0 );
% turb kin energy update:
k_m_new = ((z_m_new-field.z_b)>par.h_min).*kh_new ./ max((z_m_new-field.z_b),par.h_min) + ((z_m_new-field.z_b)<=par.h_min).*field.k_m;
% positivity condition
k_m_new = max( k_m_new , 0 );
% velocity update
u_new = ((z_m_new-field.z_b)>=par.h_min) .* qm_x_new ./ max( (z_m_new-field.z_b) , par.h_min );
v_new = ((z_m_new-field.z_b)>=par.h_min) .* qm_y_new ./ max( (z_m_new-field.z_b) , par.h_min );

% final update
newfield = field;
newfield.z_m = z_m_new;
newfield.u = u_new;
newfield.v = v_new;
newfield.c_m = c_m_new;
newfield.k_m = k_m_new;
