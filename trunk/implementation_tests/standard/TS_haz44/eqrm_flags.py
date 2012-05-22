"""
  EQRM parameter file
  All input files are first searched for in the input_dir, then in the
  resources/data directory, which is part of EQRM.

 All distances are in kilometers.
 Acceleration values are in g.
 Angles, latitude and longitude are in decimal degrees.

 If a field is not used, set the value to None.


"""

from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user
from os.path import join


# Operation Mode
run_type = "hazard" 
is_scenario = True
site_tag = "newc" 
site_db_tag = "" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
input_dir = join('.', 'implementation_tests', 'input')
output_dir = join('.', 'implementation_tests', 'current', 'TS_haz44')
use_site_indexes = True
site_indexes = [2997, 2657, 3004, 3500]
zone_source_tag = ""
event_control_tag = "use" 

# Scenario input
scenario_max_width = 15
scenario_azimuth = 340
scenario_depth = 11.5
scenario_latitude = -32.95
scenario_longitude = 151.61
scenario_magnitude = 7.2
scenario_dip = 35
scenario_number_of_events = 15
scenario_width = 20
scenario_length = 10

# Probabilistic input

# Attenuation
atten_models = ['Gaull_1990_WA']
atten_model_weights = [1]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = None
atten_periods = [0.0, 0.17544000000000001, 0.35088000000000003, 0.52632000000000001, 0.70174999999999998, 0.87719000000000003, 1.0526, 1.2281, 1.4035, 1.5789, 1.7544, 1.9298, 2.1053000000000002, 2.2806999999999999, 2.4561000000000002, 2.6316000000000002, 2.8069999999999999, 2.9824999999999999, 3.1579000000000002, 3.3332999999999999]
atten_threshold_distance = 400
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

# Capacity Spectrum Method
csm_use_variability = None
csm_variability_method = None
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
save_motion = True

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
