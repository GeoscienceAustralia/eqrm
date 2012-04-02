function harness_plot_singlesite_hzd(root_eqrm_dir)
%datadir = strcat(root_eqrm_dir, '\resources\data')
demodir = strcat(root_eqrm_dir, '\demo\output\prob_haz')

% From README-getting-started.txt 
% 6. POSTPROCESSING 1) Ground Motion Scenario
cd(demodir) 
Convert_Py2Mat_Hazard(demodir ,'THE_PARAM_T.txt')
[tmp]=plot_singlesite_hzd([demodir,'\newc_db_hzd.mat'], ...
    'UniformHzd',[151.65,-33.15;151.5,-32.9; 151.6,-33], ...
    [500 2500],'lin','rock','single');

% The jpg of this was manually saved.
end