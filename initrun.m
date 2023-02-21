function run = initrun
%INITRUN

run.dispflag = 0; % screen display turned on (= 1) or off (= 0)
run.t_end = 3600*1000; % time to end of simulation (in seconds) 10000
run.dt_output = 3600; % time interval between disk outputs (in seconds)
run.n = 200; % refinement of the discretisation
run.o = 1; % order of the scheme (= 1 or 2)
run.geostaticflag = 0;


