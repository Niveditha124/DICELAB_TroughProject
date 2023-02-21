function newfield = swapfield(field)
%SWAPFIELD transpose the entire flow field

% transpose all fields, swap x and y, and swap u and v:
newfield = field; % default
newfield.x = field.y';
newfield.y = field.x';
newfield.z_m = field.z_m';
newfield.c_m = field.c_m';
newfield.k_m = field.k_m';
newfield.z_b = field.z_b';
newfield.z_r = field.z_r';
newfield.u = field.v';
newfield.v = field.u';
