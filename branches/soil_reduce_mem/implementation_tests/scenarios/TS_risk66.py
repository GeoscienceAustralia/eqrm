"""
  EQRM parameter file
  All input files are first searched for in the input_dir, then in the
  resources/data directory, which is part of EQRM.

 All distances are in kilometers.
 Acceleration values are in g.
 Angles, latitude and longitude are in decimal degrees.

 If a field is not used, set the value to None.

 Scenario - set a atten_threshold_distance low enough that some events are no
            longer applicable to the site_indexes
"""

from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user
from os.path import join


# Operation Mode
run_type = "risk_csm" 
is_scenario = False
site_tag = "risk66" 
site_db_tag = "" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
input_dir = join('.', 'implementation_tests', 'input', 'checking')
output_dir = join('.', 'implementation_tests', 'current', 'TS_risk66')
use_site_indexes = False
zone_source_tag = ""
event_control_tag = "use" 

# Scenario input

# Probabilistic input


# Attenuation
atten_collapse_Sa_of_atten_models = False
atten_variability_method = None
atten_periods = [0.0, 0.2, 1.0]
atten_threshold_distance = 222.
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2000000
atten_smooth_spectral_acceleration = None

# Amplification
use_amplification = False
amp_variability_method = None
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
loss_regional_cost_index_multiplier = 1.0
loss_aus_contents = 0

# Save
save_total_financial_loss = True
save_building_loss = True
save_contents_loss = True


# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
