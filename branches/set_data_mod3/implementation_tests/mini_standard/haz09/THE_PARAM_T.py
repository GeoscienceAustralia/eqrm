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
max_width = 15

# Scenario input
scenario_azimith = 340
scenario_depth = 11.5
scenario_latitude = -32.95
scenario_longitude = 151.61
scenario_magnitude = 5.6
scenario_number_of_events = 2

# Probabilistic input
prob_azimuth_in_zones = [180, 180, 180, 180, 180, 180]
prob_delta_azimuth_in_zones = [180, 180, 180, 180, 180, 180]
prob_min_mag_cutoff = 4.5
prob_number_of_mag_sample_bins = 15
prob_number_of_events_in_zones = [5, 2, 1, 3, 3, 1]
prob_dip_in_zones = [35, 35, 35, 35, 35, 35]

# Attenuation
atten_models = ['Toro_1997_midcontinent']
atten_model_weights = [1]
atten_aggregate_Sa_of_atten_models = True
atten_variability_method = None
atten_periods = [0.0, 0.30303000000000002, 1.0]
atten_threshold_distance = 400
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = None

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
csm_damping_modify_Tav = True
csm_damping_use_smoothing = True
csm_hysteretic_damping = None
csm_SDcr_tolerance_percentage = None
csm_damping_max_iterations = None

# Loss
loss_min_pga = None
loss_regional_cost_index_multiplier = None
loss_aus_contents = None

# Save
save_hazard_map = True
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = False
save_prob_structural_damage = None

# General
site_tag = "newc" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
site_indexes = [2255, 11511, 10963, 686, 1026]
site_db_tag = "" 
input_dir = r".\implementation_tests\input/" 
output_dir = r".\implementation_tests\mini_current\haz09/" 

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
