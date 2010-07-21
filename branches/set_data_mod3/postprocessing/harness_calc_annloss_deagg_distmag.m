function harness_calc_annloss_deagg_distmag(root_eqrm_dir)
% eg harness_calc_annloss_deagg_distmag('Q:\trunk_branches\trunk')

datadir = strcat(root_eqrm_dir, '\resources\data')
demodir = strcat(root_eqrm_dir, '\demo\output\prob_risk')

% parameters that eventually get passed to the function
outputdir = strcat(root_eqrm_dir, '\postprocessing')

cd(demodir) 
 % convert EQRM outputs to MATLAB binary files (x2) 
Convert_Py2Mat_Risk(demodir,'THE_PARAM_T.txt',datadir)

% example 5

[eqrm_param_T, ecloss_data,NormDeAggLoss, hf] = wrap_risk_plots(1, ...
    'calc_annloss_deagg_distmag',demodir, ...
    [demodir,'/matlab_setdata.mat'], ...
    [demodir,'/newc_db_savedecloss.mat'], ...
    {[4.5:0.5:6.5],[4.5:0.5:6.5],0:5:100, 1,1,[0,8]});

	
end