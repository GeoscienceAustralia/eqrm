"""
  EQRM Control file
  All input files are first searched for in the input_dir, then in the
  resources/data directory, which is part of EQRM.

 All distances are in kilometers.
 Acceleration values are in g.
 Angles, latitude and longitude are in decimal degrees.

 If a field is not used, set the value to None.

 This control file is for the Java Tengah PSHA
 
 

"""

from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user
from os.path import join




# Operation Mode
run_type = "hazard" 
is_scenario = False
max_width = 15
site_tag = "java" 
site_db_tag = "" 
return_periods = [500,1000,2500]

input_dir = r"..\inputs\EQRM_inputs/" 
output_dir = r"." 
use_site_indexes = False
site_indexes = [1, 10, 100, 1000,1100]
zone_source_tag = "zonetag"
fault_source_tag = "faulttag"
event_control_tag = "eventag"

# Scenario input



# Probabilistic input
# prob_azimuth_in_zones = [10, 30, 70, 100, 150, 15]
# prob_delta_azimuth_in_zones = [5, 10, 20, 25, 50, 0]
prob_min_mag_cutoff = 5.0
# prob_number_of_mag_sample_bins = 15
# prob_number_of_events_in_zones = [5000, 1000, 1000, 3000, 1000, 1000]
# prob_dip_in_zones = [35, 40, 45, 50, 55, 60]

# Attenuation
#atten_models = ['Campbell08']
#atten_model_weights = [1]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = 1
atten_periods = [0.0, 0.2, 1.0]
atten_threshold_distance = 400
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = None
atten_log_sigma_eq_weight = 0
atten_spawn_bins = 5

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
