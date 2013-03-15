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
run_type = "hazard" 
is_scenario = False
reset_seed_using_time = True
compress_output = False
site_tag = "nat" 
site_db_tag = "" 
return_periods = [474.56, 500.0, 974.79, 2474.9, 2500.0]
input_dir = join('.', 'implementation_tests', 'long_input', '')
output_dir = join('.', 'implementation_tests', 'long_current', 'nat01', '')
use_site_indexes = False
site_indexes = [1]
fault_source_tag = None
zone_source_tag = "01" 
event_control_tag = "01" 

# Scenario input
scenario_azimuth = None
scenario_depth = None
scenario_latitude = None
scenario_longitude = None
scenario_magnitude = None
scenario_dip = None
scenario_number_of_events = None
scenario_width = None
scenario_length = None
scenario_max_width = None

# Probabilistic input
prob_azimuth_in_zones = None
prob_delta_azimuth_in_zones = None
prob_min_mag_cutoff = None
prob_number_of_mag_sample_bins = None
prob_number_of_events_in_zones = None
prob_number_of_events_in_faults = None
prob_dip_in_zones = None

# Attenuation
atten_models = None
atten_model_weights = None
atten_collapse_Sa_of_atten_models = 1
atten_variability_method = 1
atten_periods = [0.0, 0.2, 1.0]
atten_threshold_distance = 400
atten_spawn_bins = 1
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = False
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = False
amp_variability_method = 2
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
building_classification_tag = "" 
damage_extent_tag = "" 

# Loss
loss_min_pga = None
loss_regional_cost_index_multiplier = None
loss_aus_contents = None

# Vulnerability
vulnerability_variability_method = 2

# Fatalities
fatality_beta = 0.17
fatality_theta = 14.05

# Save
save_hazard_map = True
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = False
save_prob_structural_damage = None
save_fatalities = False
event_set_handler = "generate" 
data_array_storage = join('.', 'implementation_tests', 'long_current', 'nat01', '')
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
