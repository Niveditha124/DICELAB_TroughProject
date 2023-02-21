function newfield = hemipelagic(field,par,dt)
%HEMIPELAGIC operator accounting for sedimentation from hemipelagic sediments

z_b_new = field.z_b + dt*par.v_hemi;

% final update:
newfield = field;
newfield.z_b = z_b_new;