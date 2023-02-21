function newflux = swapflux(flux);

newflux.q_m = flux.q_m';
newflux.sig_l = flux.sig_l';
newflux.sig_r = flux.sig_r';
newflux.sigCross = flux.sigCross';
newflux.mu = flux.mu';
newflux.kh = flux.kh';
newflux.z_ml = flux.z_ml';
newflux.z_mr = flux.z_mr';
newflux.z_bl = flux.z_bl';
newflux.z_br = flux.z_br';
