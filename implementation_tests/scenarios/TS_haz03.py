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
site_tag = "newc" 
site_db_tag = "" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
input_dir = r".\implementation_tests\input/" 
output_dir = r".\implementation_tests\current\TS_haz03/" 
use_site_indexes = True
site_indexes = [2255, 11511, 10963, 686, 1026, 6597, 12382, 314, 2040, 3318, 9934, 12225, 10506, 9934, 2841, 10420, 10314, 10612, 10316, 10313, 11863, 11523, 9736, 11702, 11862, 2562, 5963, 4550, 6737, 5214]
zone_source_tag = "Atkinson_Boore_97" 
event_control_tag = "use" 

# Scenario input

# Probabilistic input

# Attenuation
atten_collapse_Sa_of_atten_models = True
atten_variability_method = 4
atten_periods = [0.0, 0.30303000000000002, 1.0]
atten_threshold_distance = 400
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = None
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = True
amp_variability_method = 4
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
