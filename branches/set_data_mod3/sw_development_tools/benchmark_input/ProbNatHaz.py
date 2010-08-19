"""
  EQRM parameter file

  All input files are first searched for in the input_dir, then in the
  resources/data directory, which is part of EQRM.

 All distances are in kilometers.
 Acceleration values are in g.
 Angles, latitude and longitude are in decimal degrees.

 If a field is not used, set the value to None.


"""

from eqrm_code.parse_in_parameters import Parameter_data
from os.path import join

sdp = Parameter_data()

# Operation Mode
sdp.run_type = "hazard" 
sdp.is_scenario = False
sdp.max_width = 15

# Scenario input
sdp.scenario_azimuth = 340
sdp.scenario_depth = 11.5
sdp.scenario_latitude = -32.95
sdp.scenario_longitude = 151.61
sdp.scenario_magnitude = 5.6
sdp.scenario_number_of_events = 167

# Probabilistic input
sdp.prob_azimuth_in_zones = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sdp.prob_delta_azimuth_in_zones = [180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]
sdp.prob_min_mag_cutoff = 4.5
sdp.prob_number_of_mag_sample_bins = 15
sdp.prob_number_of_events_in_zones = [2304, 6573, 28110, 42402, 1971, 12351, 7605, 14595, 6333, 9255, 13620, 2433, 6876, 2142, 855, 7002, 3984, 1677, 27390, 777, 5157, 2019, 2112, 2247, 8295, 2409, 7203, 342, 609450, 308736]
sdp.prob_number_of_events_in_zones = 30*[2334]
sdp.prob_dip_in_zones = [35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35]

# Attenuation
sdp.atten_models = ['Boore_08']
sdp.atten_model_weights = [1]
sdp.atten_collapse_Sa_of_atten_models = True
sdp.atten_use_variability = True
sdp.atten_variability_method = 2
sdp.atten_periods = [0.0, 0.30303, 1.0]
sdp.atten_threshold_distance = 400
sdp.atten_use_rescale_curve_from_pga = False
sdp.atten_override_RSA_shape = None
sdp.atten_cutoff_max_spectral_displacement = False
sdp.atten_pga_scaling_cutoff = 2
sdp.atten_smooth_spectral_acceleration = None
sdp.atten_log_sigma_eq_weight = 0

# Amplification
sdp.use_amplification = False
sdp.amp_use_variability = True
sdp.amp_variability_method = 2
sdp.amp_min_factor = 0.6
sdp.amp_max_factor = 10000

# Buildings
sdp.buildings_usage_classification = None
sdp.buildings_set_damping_Be_to_5_percent = None

# Capacity Spectrum Method
sdp.csm_use_variability = None
sdp.csm_variability_method = None
sdp.csm_standard_deviation = None
sdp.csm_damping_regimes = None
sdp.csm_damping_modify_Tav = True
sdp.csm_damping_use_smoothing = True
sdp.csm_use_hysteretic_damping = True
sdp.csm_hysteretic_damping = None
sdp.csm_SDcr_tolerance_percentage = None
sdp.csm_damping_max_iterations = None

# Loss
sdp.loss_min_pga = None
sdp.loss_regional_cost_index_multiplier = None
sdp.loss_aus_contents = None

# Save
sdp.save_hazard_map = True
sdp.save_total_financial_loss = False
sdp.save_building_loss = False
sdp.save_contents_loss = False
sdp.save_motion = False
sdp.save_prob_structural_damage = None

# General
sdp.site_tag = "nat" 
sdp.return_periods = [50, 475]
sdp.use_site_indexes = True #False
sdp.site_indexes = [1]
sdp.site_db_tag = "" 
sdp.input_dir = join(sdp.eqrm_data_home(), 'test_national',
                      'EQRM_input')
sdp.output_dir = join(sdp.eqrm_data_home(), 'test_national',
                      'EQRM_output','benchmark','events_'+ \
                  str(sum(sdp.prob_number_of_events_in_zones)) + '_' + \
                  'sites_1_' + \
                  sdp.get_time_user())

# If this file is executed the simulation will start
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(sdp)
