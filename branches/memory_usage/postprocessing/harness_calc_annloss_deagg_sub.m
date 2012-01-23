function harness_calc_annloss_deagg_sub(root_eqrm_dir)
% eg harness_calc_annloss_deagg_sub('Q:\trunk_branches\trunk')
% The output is the file sub_annlosses.csv, in the outputdir

datadir = strcat(root_eqrm_dir, '\resources\data')
demodir = strcat(root_eqrm_dir, '\demo\output\prob_risk')

% parameters that eventually get passed to the function
outputdir = strcat(root_eqrm_dir, '\postprocessing')

cd(demodir) 
 % convert EQRM outputs to MATLAB binary files (x2) 
Convert_Py2Mat_Risk(demodir,'THE_PARAM_T.txt',datadir)

% example 5
[eqrm_param_T, ecloss_data,annloss_deagg_sub_T] = wrap_risk_plots(1, ...
    'calc_annloss_deagg_sub', outputdir,  ...
    [demodir,'/matlab_setdata.mat'], ...
    [demodir,'/newc_db_savedecloss.mat']);

end