"""
  EQRM parameter file
  All input files are first searched for in the input_dir, then in the
  resources/data directory, which is part of EQRM.

 All distances are in kilometers.
 Acceleration values are in g.
 Angles, latitude and longitude are in decimal degrees.

 If a field is not used, set the value to None.

 Scenario - set a atten_threshold_distance low enough that some events are no
            longer applicable to the site_indexes
"""

from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user
from os.path import join


# Operation Mode
run_type = "hazard" 
is_scenario = False
site_tag = "haz51" 
site_db_tag = "" 
return_periods = [10, 50, 100, 200, 250, 500, 975, 1000, 2500, 5000, 10000]
input_dir = join('.', 'implementation_tests', 'input', 'checking')
output_dir = join('.', 'implementation_tests', 'current', 'TS_haz51')
use_site_indexes = False
zone_source_tag = ""
event_control_tag = "use" 

# Scenario input

# Probabilistic input
prob_number_of_events_in_zones = [10, 10]

# Attenuation
atten_collapse_Sa_of_atten_models = True #False
atten_variability_method = None
atten_periods = [0.0, 0.2, 1.0]
atten_threshold_distance = 222.6 # 1 deg = 111 km at equator
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2000000
atten_smooth_spectral_acceleration = None

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
save_motion = True


# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
