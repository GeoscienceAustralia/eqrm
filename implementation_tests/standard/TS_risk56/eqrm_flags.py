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
run_type = "risk_csm" 
is_scenario = False
site_tag = "newc" 
site_db_tag = "" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
input_dir = join('.', 'implementation_tests', 'input')
output_dir = join('.', 'implementation_tests', 'current', 'TS_risk56')
use_site_indexes = True
site_indexes = [3541, 3541, 2773, 2773, 4547, 4547, 4080, 5570, 964, 933, 2249, 2249, 2194, 2194, 1766, 2196, 2158, 1674, 2291, 2233, 394, 4982, 5461, 3831, 60, 5966, 2633, 2281, 3059, 1707, 6012, 5284, 1726, 3300, 2979, 2406, 3729, 2353, 2252, 2252, 2342, 2342, 2398, 2187, 4962, 4962, 2219, 2219, 2253, 2367, 5338, 299, 1244, 3571, 1281, 2306, 6238, 2363, 1408, 6284, 6235, 6292, 1750, 1684, 4006, 4135, 1676, 3674, 3875, 17, 6267, 5360, 6268, 6240, 3228, 2383, 468, 71, 2317, 2183, 2694, 5237, 665, 401, 659, 3472, 4126, 2653, 1446, 3845, 1902, 6294, 567, 2222, 4659, 4951, 291, 2372]
zone_source_tag = "3_mods_TAS" 
event_control_tag = "use" 

# Scenario input

# Probabilistic input
prob_number_of_events_in_zones = [5, 1, 1, 3, 1, 1]

# Attenuation
atten_collapse_Sa_of_atten_models = False
atten_variability_method = 4
atten_periods = [0.0, 1.0526, 3.0]
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

# Capacity Spectrum Method
csm_use_variability = False
csm_variability_method = None
csm_standard_deviation = 0.3
csm_damping_regimes = 0
csm_damping_modify_Tav = True
csm_damping_use_smoothing = True
csm_hysteretic_damping = "trapezoidal" 
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
save_motion = False
save_prob_structural_damage = False

file_array = False

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
