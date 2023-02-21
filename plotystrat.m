function plotystrat(field,xStrat,color)

% crop out-of-domain regions of the field:
field = cropfield(field);
% set rim to NaN
field.y(field.z_b==1000)=NaN;
field.z_m(field.z_b==1000)=NaN;
field.z_b(field.z_b==1000)=NaN;
% set pits to NaN
field.y(field.z_b==-1000)=NaN;
field.z_m(field.z_b==-1000)=NaN;
field.z_b(field.z_b==-1000)=NaN;
% set flow with negligible concentration to NaN;
field.z_m(field.c_m<0.00001)=NaN;
% isolate a single long-profile transect
[bogus,iStrat]=min(abs(field.x(round(end/2),:)-xStrat));

% GENERAL PLOT PROPERTIES
ax=[-5000 5000 -380 -220];
%ax=[-10000 10000 -1000 -1000];
fontsize = 11;
fontweight='bold';
dar=[10 0.5 10];

% PREPARE PLOT
plot(field.y(:,iStrat),field.z_b(:,iStrat),'color',color*[1 0 0]);
set(gca,'fontsize',fontsize,'fontweight',fontweight);
title(['flow and bed transect cross-profiles at x = ' num2str(xStrat) '  m. Time t = ' num2str(round(field.t/3600)) ' h.']);
% axis(ax);
set(gca,'dataAspectRatio',dar);
hold on;
plot(field.y(:,iStrat),field.z_m(:,iStrat),'color',color*[0 0 1]);
