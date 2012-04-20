"""
  EQRM parameter file

  All input files are first searched for in the input_dir, then in the
  resources/data directory, which is part of EQRM.

 All distances are in kilometers.
 Acceleration values are in g.
 Angles, latitude and longitude are in decimal degrees.

 If a field is not used, set the value to None.


"""

from os import getenv
from os.path import join

# Operation Mode
run_type = "hazard" 
is_scenario = False
max_width = 20
site_tag = "nat" 
site_db_tag = ""
# General
#return_periods = [474.56, 500, 974.79, 2474.9, 2500]
return_periods = [100.0, 250.0, 474.56, 500.0, 974.79, 2474.9, 2500, 5000.0, 10000.0]
input_dir = join('.', 'input')
output_dir = join('/short', getenv('PROJECT'), 'output', 'national')
use_site_indexes = False
site_indexes = [1]
zone_source_tag = "bck"
event_control_tag = "use"


# Scenario input

# Probabilistic input
#prob_min_mag_cutoff = 4.5
#prob_number_of_events_in_zones = [600000,600000,200000,600000]
#prob_number_of_events_in_zones = [10,10,10,10]

# Attenuation
atten_collapse_Sa_of_atten_models = 1
atten_variability_method = 1
#atten_periods = [0.0]
#atten_periods = [0.0,0.2,1.0]
atten_periods = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
atten_threshold_distance = 400
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

# Capacity Spectrum Method

# Loss

# Save
save_hazard_map = True
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = False
save_prob_structural_damage = None

# If this file is executed the simulation will start
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals() )
