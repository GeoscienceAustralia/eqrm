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
run_type = "risk" 
is_scenario = False
max_width = 15
site_tag = "newc" 
site_db_tag = "" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
input_dir = r".\implementation_tests\input/" 
output_dir = r".\implementation_tests\current\TS_risk62/" 
use_site_indexes = True
site_indexes = [6067, 3129]
zone_source_tag = "TS_risk62" 
event_control_tag = "use" 

# Scenario input

# Probabilistic input
prob_number_of_events_in_zones = [1, 1]

# Attenuation
atten_collapse_Sa_of_atten_models = False
atten_variability_method = 4
atten_periods = [0.0, 0.17499999999999999, 0.29999999999999999, 0.80000000000000004, 1.0, 1.2, 1.3999999999999999, 1.6000000000000001, 1.8, 2.1000000000000001, 3.3999999999999999]
atten_threshold_distance = 400
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = False
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = True
amp_variability_method = 4
amp_min_factor = 0.6
amp_max_factor = 10000

# Buildings
buildings_usage_classification = "HAZUS" 
buildings_set_damping_Be_to_5_percent = False
bridges_functional_percentages = [25, 50, 75]

# Capacity Spectrum Method
csm_use_variability = False
csm_variability_method = None
csm_standard_deviation = 0.3
csm_damping_regimes = 0
csm_damping_modify_Tav = True
csm_damping_use_smoothing = True
csm_hysteretic_damping = "Error" 
csm_SDcr_tolerance_percentage = 1
csm_damping_max_iterations = 7

# Loss
loss_min_pga = 0.05
loss_regional_cost_index_multiplier = 1.4516
loss_aus_contents = 0

# Save
save_hazard_map = False
save_total_financial_loss = True
save_building_loss = False
save_contents_loss = False
save_motion = True
save_prob_structural_damage = True

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
