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
is_scenario = True
max_width = 25
site_tag = "Depthtest" 
site_db_tag = "" 
return_periods = [500]
input_dir = join('.', 'input')
#output_dir = join('.', 'output', 'Adelaide_AB06_BC_M5_D1')
#output_dir = join('.', 'output', 'Adelaide_AB06_BC_M5_D7')
#output_dir = join('.', 'output', 'Adelaide_Sadigh_97_M5_D1')
#output_dir = join('.', 'output', 'Adelaide_Sadigh_97_M5_D7')
#output_dir = join('.', 'output', 'Adelaide_Toro97_M5_D1')
#output_dir = join('.', 'output', 'Adelaide_Toro97_M5_D7')
#output_dir = join('.', 'output', 'Adelaide_Somerville09_Non_Cratonic_M25_D1')
#output_dir = join('.', 'output', 'Adelaide_Somerville09_Non_Cratonic_M25_D7')
#output_dir = join('.', 'output', 'M3_Toro97_M25_D1')
#
output_dir = join('.', 'output', 'Depthtest_Somerville09_Non_Cratonic_M5_D1')
output_dir = join('.', 'output', 'Depthtest_Somerville09_Non_Cratonic_M5_D8')
output_dir = join('.', 'output', 'Depthtest_Chiou08_M5_D1')
output_dir = join('.', 'output', 'Depthtest_Chiou08_M5_D8')

use_site_indexes = False
site_indexes = [2997, 2657, 3004, 3500]
zone_source_tag = ""
event_control_tag = ""

# Scenario input
scenario_magnitude = 5.0
scenario_azimuth = 0
scenario_depth = 8.0
scenario_latitude = -25.0
scenario_longitude = 130.0
scenario_dip = 45
scenario_number_of_events = 1

# Probabilistic input

# Attenuation
atten_models = ['Atkinson06_bc_boundary_bedrock']
atten_models = ['Campbell08']
atten_models = ['Toro_1997_midcontinent']
atten_models = ['Depthtest_Somerville09_Non_Cratonic']
atten_models = ['Chiou08']
atten_model_weights = [1]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = 4
atten_periods = [0.0, 1.0, 2.0, 3.0, 4.0]
atten_threshold_distance = 400
atten_override_RSA_shape = None
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = None
atten_log_sigma_eq_weight = 0

# Amplification
use_amplification = False
amp_variability_method = None
amp_min_factor = 0.6
amp_max_factor = 10000

# Buildings

# Capacity Spectrum Method

# Loss

# Save
save_hazard_map = False
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = True
save_prob_structural_damage = None

file_array = False

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM attributes variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
