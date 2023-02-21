function newfield = cropfield(field)
%CROPFIELD remove rim around domain to obtain better view

[m n] = size(field.x);
newfield = field;
newfield.x = field.x(2:m-1,2:n-1);
newfield.y = field.y(2:m-1,2:n-1);
newfield.z_m = field.z_m(2:m-1,2:n-1);
newfield.z_b = field.z_b(2:m-1,2:n-1);
newfield.z_r = field.z_r(2:m-1,2:n-1);
newfield.u = field.u(2:m-1,2:n-1);
newfield.v = field.v(2:m-1,2:n-1);
newfield.c_m = field.c_m(2:m-1,2:n-1);
newfield.k_m = field.k_m(2:m-1,2:n-1);



