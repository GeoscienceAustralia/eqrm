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
site_indexes = [1, 1001, 2001, 3001, 4001, 5001, 6001, 7001, 8001, 9001, 10001, 11001, 12001, 13001, 14001, 15001, 16001, 17001, 18001, 19001, 20001, 21001, 22001, 23001, 24001, 25001, 26001, 27001, 28001, 29001, 30001, 31001, 32001, 33001, 34001, 35001, 36001, 37001, 38001, 39001, 40001, 41001, 42001, 43001, 44001, 45001, 46001, 47001, 48001, 49001, 50001, 51001, 52001, 53001, 54001, 55001, 56001, 57001, 58001, 59001, 60001, 61001, 62001, 63001, 64001]
fault_source_tag = ""
zone_source_tag = ""
event_control_tag = ""

# Scenario input

# Probabilistic input

# Attenuation
atten_collapse_Sa_of_atten_models = True
atten_variability_method = 2
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
#fatality_beta = 0.00000005
#fatality_theta = .000005

# Save
save_hazard_map = False
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = False
save_prob_structural_damage = None
save_fatalities = True

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
