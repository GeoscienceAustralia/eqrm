"""
  EQRM parameter file
All input files are first searched for in the input_dir,then in the
resources/data directory, which is part of EQRM.

All distances are in kilometers.
Acceleration values are in g.
Angles, latitude and longitude are in decimal degrees.

If a field is not used, set the value to None.


"""

from os import getenv
from os.path import join
from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user


# Operation Mode
run_type = "risk_csm" 
is_scenario = True
reset_seed_using_time = True
compress_output = False
site_tag = "newc" 
site_db_tag = "" 
return_periods = [10.0, 50.0, 100.0, 200.0, 250.0, 474.56, 500.0, 974.79, 1000.0, 2474.9, 2500.0, 5000.0, 7500.0, 10000.0]
input_dir = join('.', 'input', '')
output_dir = join('.', 'output', 'scen_risk', '')
use_site_indexes = True
site_indexes = [3541, 3541, 2773, 2773, 4547, 4547, 4080, 5570, 964, 933, 2249, 2249, 2194, 2194, 1766, 2196, 2158, 1674, 2291, 2233, 394, 4982, 5461, 3831, 60, 5966, 2633, 2281, 3059, 1707, 6012, 5284, 1726, 3300, 2979, 2406, 3729, 2353, 2252, 2252, 2342, 2342, 2398, 2187, 4962, 4962, 2219, 2219, 2253, 2367, 5338, 299, 1244, 3571, 1281, 2306, 6238, 2363, 1408, 6284, 6235, 6292, 1750, 1684, 4006, 4135, 1676, 3674, 3875, 17, 6267, 5360, 6268, 6240, 3228, 2383, 468, 71, 2317, 2183, 2694, 5237, 665, 401, 659, 3472, 4126, 2653, 1446, 3845, 1902, 6294, 567, 2222, 4659, 4951, 291, 2372]
fault_source_tag = None
zone_source_tag = "" 
event_control_tag = "" 

# Scenario input
scenario_azimuth = 340
scenario_depth = 11.5
scenario_latitude = -32.95
scenario_longitude = 151.61
scenario_magnitude = 7.2
scenario_dip = 35
scenario_number_of_events = 1002
scenario_width = None
scenario_length = None
scenario_max_width = 15

# Probabilistic input
prob_azimuth_in_zones = None
prob_delta_azimuth_in_zones = None
prob_min_mag_cutoff = None
prob_number_of_mag_sample_bins = None
prob_number_of_events_in_zones = None
prob_number_of_events_in_faults = None
prob_dip_in_zones = None

# Attenuation
atten_models = ['Toro_1997_midcontinent']
atten_model_weights = [1]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = 2
atten_periods = [0.0, 0.17544, 0.35088, 0.52632, 0.70175, 0.87719, 1.0526, 1.2281, 1.4035, 1.5789, 1.7544, 1.9298, 2.1053, 2.2807, 2.4561, 2.6316, 2.807, 2.9825, 3.1579, 3.3333]
atten_threshold_distance = 400
atten_spawn_bins = 1
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = False
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = True
amp_variability_method = 2
amp_min_factor = 0.6
amp_max_factor = 10000

# Buildings
buildings_usage_classification = "HAZUS" 
buildings_set_damping_Be_to_5_percent = False
bridges_functional_percentages = None

# Capacity Spectrum Method
csm_use_variability = False
csm_variability_method = None
csm_standard_deviation = 0.3
csm_damping_regimes = 0
csm_damping_modify_Tav = True
csm_damping_use_smoothing = True
csm_hysteretic_damping = "curve" 
csm_SDcr_tolerance_percentage = 1
csm_damping_max_iterations = 7
building_classification_tag = "" 
damage_extent_tag = "" 

# Loss
loss_min_pga = 0.05
loss_regional_cost_index_multiplier = 1.4516
loss_aus_contents = 0

# Vulnerability
vulnerability_variability_method = 2

# Fatalities
fatality_beta = 0.17
fatality_theta = 14.05

# Save
save_hazard_map = False
save_total_financial_loss = True
save_building_loss = False
save_contents_loss = False
save_motion = False
save_prob_structural_damage = False
save_fatalities = False
event_set_handler = "generate" 
data_array_storage = join('.', 'output', 'scen_risk', '')
file_array = False
event_set_load_dir = None
file_log_level = "debug" 
console_log_level = "info" 
file_parallel_log_level = "warning" 
console_parallel_log_level = "warning" 

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM attributes variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
