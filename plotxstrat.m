function plotxstrat(field,yStrat,color)

% crop out-of-domain regions of the field:
field = cropfield(field);
% set rim to NaN
field.x(field.z_b==1000)=NaN;
% set pits to NaN
field.x(field.z_b==-1000)=NaN;
% set flow with negligible concentration to NaN;
field.z_m(field.c_m<0.00001)=NaN;
% isolate a single long-profile transect
[bogus,iStrat]=min(abs(field.y(:,1)-yStrat));

% GENERAL PLOT PROPERTIES
ax=[5000 15000 -380 -220];
fontsize = 11;
fontweight='bold';
dar=[10 0.5 10];

% PREPARE PLOT
plot(field.x(iStrat,:),field.z_b(iStrat,:),'color',color*[1 0 0]);
set(gca,'fontsize',fontsize,'fontweight',fontweight);
title(['flow and bed transect long profiles at y = ' num2str(yStrat) '  m. Time t = ' num2str(round(field.t/3600)) ' h.']);
axis(ax);
set(gca,'dataAspectRatio',dar);
hold on;
plot(field.x(iStrat,:),field.z_m(iStrat,:),'color',color*[0 0 1]);
