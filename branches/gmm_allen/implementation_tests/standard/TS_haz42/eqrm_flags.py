"""
  EQRM parameter file
All input files are first searched for in the input_dir,then in the
resources/data directory, which is part of EQRM.

All distances are in kilometers.
Acceleration values are in g.
Angles, latitude and longitude are in decimal degrees.

If a field is not used, set the value to None.


"""

from os.path import join
from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user


# Operation Mode
run_type = "hazard" 
is_scenario = False
max_width = None
reset_seed_using_time = True
compress_output = False
site_tag = "newc" 
site_db_tag = "" 
return_periods = [10.0, 50.0, 100.0, 200.0, 250.0, 474.56, 500.0, 974.78999999999996, 1000.0, 2474.9000000000001, 2500.0, 5000.0, 7500.0, 10000.0]
input_dir = join('.', 'implementation_tests', 'input', '')
output_dir = join('.', 'implementation_tests', 'current', 'TS_haz42', '')
use_site_indexes = True
site_indexes = [2255, 11511, 10963, 686, 1026]
fault_source_tag = None
zone_source_tag = None
event_control_tag = "use" 

# Scenario input
scenario_azimuth = None
scenario_depth = None
scenario_latitude = None
scenario_longitude = None
scenario_magnitude = None
scenario_dip = None
scenario_number_of_events = None

# Probabilistic input
prob_azimuth_in_zones = None
prob_delta_azimuth_in_zones = None
prob_min_mag_cutoff = None
prob_number_of_mag_sample_bins = None
prob_number_of_events_in_zones = [1, 2, 1, 0, 0, 0]
prob_number_of_events_in_faults = None
prob_dip_in_zones = None

# Attenuation
atten_models = ['Allen_2012', 'AllenSEA06', 'Gaull_1990_WA', 'Toro_1997_midcontinent', 'Sadigh_97', 'Youngs_97_interface', 'Youngs_97_intraslab', 'Combo_Sadigh_Youngs_M8', 'Somerville09_Yilgarn', 'Somerville09_Non_Cratonic', 'Chiou08', 'Campbell08', 'Liang_2008', 'Campbell03', 'Atkinson06_hard_bedrock', 'Atkinson06_soil', 'Atkinson06_bc_boundary_bedrock', 'Zhao_2006_intraslab', 'Atkinson_2003_interface', 'Akkar_2010_crustal', 'Zhao_2006_interface', 'Atkinson_2003_intraslab']
atten_model_weights = [0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547, 0.04545454545454547]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = None
atten_periods = [0.0, 0.32000000000000001, 1.0]
atten_threshold_distance = 100
atten_spawn_bins = 1
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = None
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = True
amp_variability_method = None
amp_min_factor = 0.6
amp_max_factor = 10000

# Buildings
buildings_usage_classification = None
buildings_set_damping_Be_to_5_percent = None
bridges_functional_percentages = None

# Capacity Spectrum Method
csm_use_variability = None
csm_variability_method = 3
csm_standard_deviation = None
csm_damping_regimes = None
csm_damping_modify_Tav = None
csm_damping_use_smoothing = None
csm_hysteretic_damping = None
csm_SDcr_tolerance_percentage = None
csm_damping_max_iterations = None

# Loss
loss_min_pga = None
loss_regional_cost_index_multiplier = None
loss_aus_contents = None

# Save
save_hazard_map = True
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = False
save_prob_structural_damage = False
save_fatalities = False

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM attributes variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
