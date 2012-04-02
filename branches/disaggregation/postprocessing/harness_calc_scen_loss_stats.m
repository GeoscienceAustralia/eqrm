function harness_calc_scen_loss_stats(root_eqrm_dir)
% This produces 2 figures

datadir = strcat(root_eqrm_dir, '\resources\data')
% 2) Damage Scenario with a single attenuation model
demodir = strcat(root_eqrm_dir, '\demo\output\scen_risk')
cd(demodir) 
 % convert EQRM outputs to MATLAB binary files (x2) 
Convert_Py2Mat_Risk(demodir,'THE_PARAM_T.txt',datadir)

% parameters that eventually get passed to calc_scen_loss_stats
outputdir = strcat(root_eqrm_dir, '\postprocessing')
pre89_flag = 1
dollars89_flag = 1
resonly_flag = 1
finalprint_flag = 2
Xlim = [1,50]

 [eqrm_param_T, ecloss_data,scen_loss_stats,hf] = wrap_risk_plots(1,...
 'calc_scen_loss_stats',outputdir, [demodir,'/matlab_setdata.mat'],...
[demodir,'/newc_db_savedecloss.mat'],{pre89_flag,dollars89_flag, ...
resonly_flag,finalprint_flag,Xlim});

	
end