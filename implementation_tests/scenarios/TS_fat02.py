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
run_type = "fatality"
is_scenario = False
site_tag = "java" 
site_db_tag = "" 
return_periods = [500, 1000, 2500]
input_dir = join('.', 'implementation_tests', 'input', 'java')
output_dir = join('.', 'implementation_tests', 'current', 'TS_fat02')
use_site_indexes = False
site_indexes = [1, 2, 3, 4, 5, 6, 7, 8]
fault_source_tag = ""
zone_source_tag = ""
event_control_tag = ""

# Scenario input

# Probabilistic input

# Attenuation
atten_collapse_Sa_of_atten_models = True
atten_variability_method = None
atten_periods = [1.0]
atten_threshold_distance = 400
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

# Capacity Spectrum Method

# Loss

# Fatalities
fatality_beta = 0.00000005
fatality_theta = .000005

# Save
save_hazard_map = True
save_fatalities = True

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
