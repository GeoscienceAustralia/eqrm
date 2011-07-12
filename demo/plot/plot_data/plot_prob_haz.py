"""
  EQRM parameter file
All input files are first searched for in the input_dir,then in the
resources/data directory, which is part of EQRM.

All distances are in kilometers.
Acceleration values are in g.
Angles, latitude and longitude are in decimal degrees.

If a field is not used, set the value to None.


"""

from os.path import join
from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user


# Operation Mode
run_type = "hazard" 
is_scenario = False
max_width = 15
site_tag = "newc" 
site_db_tag = "" 
return_periods = [100, 500, 7500, 10000.0]
input_dir = join('.', 'input')
output_dir = join('.', 'output', 'plot_prob_haz')
use_site_indexes = False
fault_source_tag = "no_fault" 

# Scenario input

# Probabilistic input
prob_number_of_events_in_zones = [5000, 1000, 1000, 3000, 1000, 1000]

# Attenuation
atten_models = ['Sadigh_97']
atten_model_weights = [1]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = 2
atten_periods = [0.0, 0.29999999999999999, 1.0]
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
# Delete all variables that are not EQRM attributes variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
