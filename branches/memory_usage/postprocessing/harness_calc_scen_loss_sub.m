function harness_calc_scen_loss_sub(root_eqrm_dir) 
% produces a csv file with percentage building damage per suburb.

datadir = strcat(root_eqrm_dir, '\resources\data')
% 2) Damage Scenario with a single attenuation model
demodir = strcat(root_eqrm_dir, '\demo\output\scen_risk')
cd(demodir) 
 % convert EQRM outputs to MATLAB binary files (x2) 
Convert_Py2Mat_Risk(demodir,'THE_PARAM_T.txt',datadir)

% parameters that eventually get passed to the function
outputdir = strcat(root_eqrm_dir, '\postprocessing')
pre89_flag = 0
dollars89_flag = 0
med_flag = 0
ev = 50

[eqrm_param_T, ecloss_data,scenloss_sub_T] = wrap_risk_plots(1, ...
    'calc_scenloss_sub',outputdir, [demodir,'/matlab_setdata.mat'], ...
    [demodir,'/newc_db_savedecloss.mat'],{pre89_flag,dollars89_flag, ...
    med_flag, ev});

	
end