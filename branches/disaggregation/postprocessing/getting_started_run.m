function getting_started_run(root_eqrm_dir)
% Let's test all the harnesses.
% This should be automatic, but who wants to learn Matlab?

harness_plot_singlesite_hzd(root_eqrm_dir)
harness_calc_scen_loss_sub(root_eqrm_dir)
harness_calc_scen_loss_stats(root_eqrm_dir)
harness_calc_annloss_deagg_sub(root_eqrm_dir) % produces csv
harness_calc_pml(root_eqrm_dir)
harness_calc_annloss_deagg_structural(root_eqrm_dir)
harness_calc_annloss_deagg_distmag(root_eqrm_dir)
harness_calc_annloss_deagg_btype(root_eqrm_dir)
harness_calc_annloss(root_eqrm_dir)
end