function grad = gradientVL(field,par,o)
%GRADIENTVL Van Leer slope limiter 

if (o==1)
    grad.dh_m = zeros(size(field.x));
    grad.dmu = zeros(size(field.x));
    grad.dkh = zeros(size(field.x));
    grad.dz_b = zeros(size(field.x));
    grad.dqx_m = zeros(size(field.x));
    grad.dqy_m = zeros(size(field.x));
else
    [m n] = size(field.x);
    % obtain gradient variables:
    h_m = field.z_m - field.z_b;
    z_b = field.z_b;
    qx_m = h_m.*field.u;
    qy_m = h_m.*field.v;
    mu = h_m.*field.c_m;
    kh = h_m.*field.k_m;
    % extend variables left and right:
    h_me = [h_m(:,1) h_m h_m(:,n)];
    mu_e = [mu(:,1) mu mu(:,n)];
    kh_e = [kh(:,1) kh kh(:,n)];
    z_be = [z_b(:,1) z_b z_b(:,n)];
    qx_me = [qx_m(:,1) qx_m qx_m(:,n)];
    qy_me = [qy_m(:,1) qy_m qy_m(:,n)];
    % minmod operations (see Nujic 1995):
    grad.dh_m = minmod( h_me(:,3:n+2) - h_me(:,2:n+1) , h_me(:,2:n+1) - h_me(:,1:n) );
    grad.dmu = minmod( mu_e(:,3:n+2) - mu_e(:,2:n+1) , mu_e(:,2:n+1) - mu_e(:,1:n) );
    grad.dkh = minmod( kh_e(:,3:n+2) - kh_e(:,2:n+1) , kh_e(:,2:n+1) - kh_e(:,1:n) );
    grad.dz_b = minmod( z_be(:,3:n+2) - z_be(:,2:n+1) , z_be(:,2:n+1) - z_be(:,1:n) );
    grad.dqx_m = minmod( qx_me(:,3:n+2) - qx_me(:,2:n+1) , qx_me(:,2:n+1) - qx_me(:,1:n) );
    grad.dqy_m = minmod( qy_me(:,3:n+2) - qy_me(:,2:n+1) , qy_me(:,2:n+1) - qy_me(:,1:n) );
end;
