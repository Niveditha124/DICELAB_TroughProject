function newfield = knappBagnold(field,par,dt)
%knappBagnold operator
%
% supposes h&U&C are invariants

newfield = field;
% solve for K (assumes h is invariant)
newfield.k_m = max(field.k_m-dt*(par.R*par.g*par.vs*field.c_m) , 0);
