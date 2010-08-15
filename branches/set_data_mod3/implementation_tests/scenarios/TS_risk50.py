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
is_scenario = True
max_width = 15
site_tag = "newc" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
use_site_indexes = True
site_indexes = [1684, 4006, 4135, 1676, 3674, 3875, 17, 6267, 5360, 6268, 6240, 3228, 2383, 468, 71, 2317, 2183, 2694, 5237, 665, 401, 659, 3472, 4126, 2653, 1446, 3845, 1902, 6294, 567, 2222, 4659, 4951, 291, 2372]
site_db_tag = "" 
input_dir = r".\implementation_tests\input/" 
output_dir = r".\implementation_tests\current\TS_risk50/" 

# Scenario input
scenario_azimith = 340
scenario_depth = 11.5
scenario_latitude = -32.95
scenario_longitude = 151.61
scenario_magnitude = 7.2
scenario_dip = 35
scenario_number_of_events = 2

# Probabilistic input
prob_azimuth_in_zones = 180
prob_delta_azimuth_in_zones = 180
prob_min_mag_cutoff = 4.5
prob_number_of_mag_sample_bins = 15
prob_number_of_events_in_zones = [5, 10, 10, 3, 10, 10]
prob_dip_in_zones = 35

# Attenuation
atten_models = ['Toro_1997_midcontinent', 'Atkinson_Boore_97', 'Sadigh_97']
atten_model_weights = [0.33333333333333331, 0.33333333333333331, 0.33333333333333331]
atten_aggregate_Sa_of_atten_models = True
atten_variability_method = 2
atten_periods = [0.0, 0.17544000000000001, 0.35088000000000003, 0.52632000000000001, 0.70174999999999998, 0.87719000000000003, 1.0526, 1.2281, 1.4035, 1.5789, 1.7544, 1.9298, 2.1053000000000002, 2.2806999999999999, 2.4561000000000002, 2.6316000000000002, 2.8069999999999999, 2.9824999999999999, 3.1579000000000002, 3.3332999999999999]
atten_threshold_distance = 400
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = False
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = True
amp_variability_method = 2
amp_min_factor = 0.6
amp_max_factor = 10000

# Buildings
buildings_usage_classification = "HAZUS" 
buildings_set_damping_Be_to_5_percent = False

# Capacity Spectrum Method
csm_use_variability = True
csm_variability_method = 3
csm_standard_deviation = 0.3
csm_damping_regimes = 0
csm_damping_modify_Tav = True
csm_damping_use_smoothing = True
csm_hysteretic_damping = "curve" 
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

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
