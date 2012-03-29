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
site_tag = "newc" 
site_db_tag = "" 
return_periods = [10,25,50,100,200,500,1000,2000,5000,7500,10000]
input_dir = r".\input/" 
output_dir = r".\output\plot_prob_haz/" 
use_site_indexes = False
zone_source_tag = ""
event_control_tag = ""

# Scenario input

# Probabilistic input
prob_min_mag_cutoff = 4.5
prob_number_of_events_in_zones = [5000, 1000, 1000, 3000, 1000, 1000]

# Attenuation
atten_models = ['Sadigh_97']
atten_model_weights = [1]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = 2
atten_periods = [0.0, 0.01, 0.03, 0.05, 0.1, 0.2, 0.30303000000000002, 0.5, 0.75, 1.0]
atten_threshold_distance = 400
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = None
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = True
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

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
