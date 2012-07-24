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
run_type = "risk_mmi" 
is_scenario = True
site_tag = "vuln04" 
site_db_tag = "" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
input_dir = join('.', 'implementation_tests', 'input', 'vulnerability')
output_dir = join('.', 'implementation_tests', 'current', 'TS_vuln04')
use_site_indexes = False
zone_source_tag = ""

# Scenario input
scenario_max_width = 15
scenario_azimuth = 340
scenario_depth = 11.5
scenario_latitude = -32.95
scenario_longitude = 151.61
scenario_magnitude = 7.2
scenario_dip = 35
scenario_number_of_events = 1

# Probabilistic input

# Attenuation
# This gives a large mean.  The SA is scaled back
atten_models = ['mean_10_sigma_1'] #'mean_1_sigma_0pt5'
atten_model_weights = [1.0]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = None
atten_periods = [1.0, 1.1, 1.2, 1.3]
atten_threshold_distance = 400
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
# This is what is really setting the SA
# 10/980. = 0.01020408163265306 
atten_pga_scaling_cutoff = 0.01020408163265306 
atten_smooth_spectral_acceleration = False
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = False
amp_variability_method = None
amp_min_factor = 0.6
amp_max_factor = 10000

# Buildings
buildings_usage_classification = "HAZUS" 

# Capacity Spectrum Method

# Loss

# Vulnerability
vulnerability_variability_method = None

# Save
save_hazard_map = False
save_total_financial_loss = False
save_building_loss = True
save_contents_loss = False
save_motion = True
save_prob_structural_damage = False

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    from eqrm_code.postprocessing import events_shaking_a_site
    main(locals())
    events_shaking_a_site(output_dir,
                          site_tag,
                          -33.1425,
                          151.5204,
                          1.0,
                          True)
