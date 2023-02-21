function fieldplot(field,field_0,field_prev,par,dt)

hold off; % to allow repeated plots in same figure

% crop out-of-domain regions of the field:
% field = cropfield(field);
% set rim to NaN
field.x(field.z_b==1000)=NaN;
% set pits to NaN
field.x(field.z_b==-1000)=NaN;
% set flow with negligible concentration to NaN;
% field.z_m(field.c_m<0.0001)=NaN;

% GENERAL PLOT PROPERTIES
ax=[0 21000 -200 100];
fontsize = 11;
fontweight='bold';

% PLOT PROFILES
if 1 % full sets of profiles

% 1. flow profile
subplot(2,2,1);
hold off;
plot(field.x,field.z_r,'k','linewidth',3);
hold on;
plot(field.x,field_0.z_b,'color',[0.7 0.7 0.7],'linewidth',3);
plot(field.x,field.z_b,'r','linewidth',3);
plot(field.x,field.z_m,'b','linewidth',3);
set(gca,'fontsize',fontsize,'fontweight',fontweight);
title(['flow profile, t = ' num2str(floor(field.t/3600)) ' h.']);
axis(ax);
grid on
% 2. velocity profile & concentration profile
subplot(2,2,2);
[subax,H1,H2] = plotyy(field.x,field.u,field.x,field.c_m);
set(H1,'linewidth',3);
set(H2,'linewidth',3);
set(subax(1),'fontsize',fontsize,'fontweight',fontweight);
set(subax(2),'fontsize',fontsize,'fontweight',fontweight);
title('\color{blue}U\color{black} and \color[rgb]{0 .5 0}C\color{black} profiles');
set(subax(1),'xlim',ax(1:2));
set(subax(2),'xlim',ax(1:2));
set(subax(1),'ylim',[0 4]);
set(subax(2),'ylim',[0 0.016]);
set(subax(1),'ytick',0:0.5:10);
set(subax(2),'ytick',0:0.002:1);
grid on
% 3. turbulent kinetic energy profile and Froude profile
subplot(2,2,3);
h = field.z_m - field.z_b;
Ri = par.R*par.g.*field.c_m.*h./max(field.u.^2,(par.g*par.h_min));
Fr = (1./max(Ri,1e-10)).^0.5;
[subax,H1,H2] = plotyy(field.x,field.k_m,field.x,Fr);
set(H1,'linewidth',3);
set(H2,'linewidth',3);
set(subax(1),'fontsize',fontsize,'fontweight',fontweight);
set(subax(2),'fontsize',fontsize,'fontweight',fontweight);
title('\color{blue}K\color{black} and \color[rgb]{0 .5 0}Fr\color{black} profiles');
set(subax(1),'xlim',ax(1:2));
set(subax(2),'xlim',ax(1:2));
set(subax(1),'ylim',[0 1]);
set(subax(1),'ytick',0:0.1:1);
set(subax(2),'ylim',[0 2]);
set(subax(2),'ytick',0:0.2:2);
grid on
% 4. instant and cumulative bed level changes
subplot(2,2,4);
[subax,H1,H2] = plotyy(field.x,(field.z_b-field_prev.z_b)/dt,field.x,field.z_b-field_0.z_b);
set(H1,'linewidth',3);
set(H2,'linewidth',3);
set(subax(1),'fontsize',fontsize,'fontweight',fontweight);
set(subax(2),'fontsize',fontsize,'fontweight',fontweight);
title('\color{blue}Instant.\color{black} and \color[rgb]{0 .5 0}cumul.\color{black} bed changes');
set(subax(1),'xlim',ax(1:2));
set(subax(2),'xlim',ax(1:2));
grid on

else
hold off;
plot(field.x,field.z_r,'k');
hold on;
plot(field.x,field.z_b,'r');
plot(field.x,field.z_m,'b');
title(['flow profile, t = ' num2str(floor(field.t)) ' s.']);
set(gca,'fontsize',fontsize,'fontweight',fontweight);
set(gca,'fontsize',fontsize,'fontweight',fontweight);
axis(ax);
end;

% set(ax(2),'ylim',[0 4],'ytick',0:0.5:4);

drawnow;