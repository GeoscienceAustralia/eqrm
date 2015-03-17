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
is_scenario = True
reset_seed_using_time = True
compress_output = False
site_tag = "Depthtest" 
site_db_tag = "" 
return_periods = [500]
input_dir = join('.', 'input', '')
output_dir = join('.', 'output', '')
use_site_indexes = False
site_indexes = [2997, 2657, 3004, 3500]
fault_source_tag = None
zone_source_tag = "" 
event_control_tag = "" 

# Scenario input
scenario_azimuth = 0
scenario_depth = 8.0
scenario_latitude = 0.0
scenario_longitude = 130.0
scenario_magnitude = 5.0
scenario_dip = 45
scenario_number_of_events = 1
scenario_width = None
scenario_length = None
scenario_max_width = 25

# Probabilistic input
prob_azimuth_in_zones = None
prob_delta_azimuth_in_zones = None
prob_min_mag_cutoff = None
prob_number_of_mag_sample_bins = None
prob_number_of_events_in_zones = None
prob_number_of_events_in_faults = None
prob_dip_in_zones = None

# Attenuation
atten_models = ['Chiou08']
atten_model_weights = [1]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = 4
atten_periods = [0.0, 1.0, 2.0, 3.0, 4.0]
atten_threshold_distance = 400
atten_spawn_bins = 1
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = None
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = False
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
save_hazard_map = False
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = True
save_prob_structural_damage = None
save_fatalities = False
event_set_handler = "generate" 
data_array_storage = join('.', 'output', '')
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
