function newfield = mirror(field)
%MIRROR extend field left and right using mirror symmetry

[m n] = size(field.x);
dx = field.x(1,2) - field.x(1,1);
newfield = field;
newfield.x = [field.x(:,1)-dx field.x field.x(:,n)+dx];
newfield.y = [field.y(:,1) field.y field.y(:,n)];
newfield.z_m = [field.z_m(:,1) field.z_m field.z_m(:,n)];
newfield.c_m = [field.c_m(:,1) field.c_m field.c_m(:,n)];
newfield.k_m = [field.k_m(:,1) field.k_m field.k_m(:,n)];
newfield.z_b = [field.z_b(:,1) field.z_b field.z_b(:,n)];
newfield.z_r = [field.z_r(:,1) field.z_r field.z_r(:,n)];
newfield.u = [field.u(:,1) field.u field.u(:,n)];
newfield.v = [field.v(:,1) field.v field.v(:,n)];
