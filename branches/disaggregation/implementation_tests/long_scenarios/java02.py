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
is_scenario = False
site_tag = "java" 
return_periods = [500, 1000, 2500]
input_dir = join('.', 'implementation_tests', 'long_input')
output_dir = join('.', 'implementation_tests', 'long_current', 'java02')
use_site_indexes = True
site_indexes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
fault_source_tag = "div100_local_mag_min" 
zone_source_tag = "div100_local_mag_min"
event_control_tag = "" 

# Scenario input

# Probabilistic input

# Attenuation
atten_collapse_Sa_of_atten_models = True
atten_variability_method = 1
atten_periods = [0.0, 0.20000000000000001, 1.0]
atten_threshold_distance = 400
atten_spawn_bins = 5
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

# Capacity Spectrum Method

# Loss

# Save
save_hazard_map = True
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = False
save_prob_structural_damage = None

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
