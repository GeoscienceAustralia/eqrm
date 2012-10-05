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
run_type = "bridge" 
is_scenario = True
site_tag = "newc" 
site_db_tag = "" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
input_dir = join('.', 'implementation_tests', 'input_bridges')
output_dir = join('.', 'implementation_tests', 'current', 'TS_bridge01')
use_site_indexes = True
site_indexes = [10, 11, 12]
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
scenario_number_of_events = 1

# Probabilistic input
prob_number_of_events_in_zones = [0, 0, 0, 0, 0, 1]

# Attenuation
atten_models = ['Toro_1997_midcontinent']
atten_model_weights = [1.0]
atten_collapse_Sa_of_atten_models = False
atten_variability_method = 4
atten_periods = [0.0, 0.17499999999999999, 0.29999999999999999, 0.80000000000000004, 1.0, 1.2, 1.3999999999999999, 1.6000000000000001, 1.8, 2.1000000000000001, 3.3999999999999999]
atten_threshold_distance = 400
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = False
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = True
amp_variability_method = 4
amp_min_factor = 0.6
amp_max_factor = 10000

# Buildings
bridges_functional_percentages = [25, 50, 75]

# Capacity Spectrum Method

# Loss

# Save
save_hazard_map = False
save_motion = False
save_prob_structural_damage = True

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
