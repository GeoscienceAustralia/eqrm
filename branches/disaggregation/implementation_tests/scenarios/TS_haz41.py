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
run_type = "hazard" 
is_scenario = False
site_tag = "newc" 
site_db_tag = "" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
input_dir = join('.', 'implementation_tests', 'input')
output_dir = join('.', 'implementation_tests', 'current', 'TS_haz41')
use_site_indexes = True
site_indexes = [2255, 11511, 10963, 686, 1026]
zone_source_tag = ""
event_control_tag = "use" 

# Scenario input

# Probabilistic input
prob_number_of_events_in_zones = [1, 2, 1, 0, 0, 0]

# Attenuation
atten_models = ['Allen', 'Allen_2012', 'Gaull_1990_WA', 'Toro_1997_midcontinent', 'Sadigh_97', 'Youngs_97_interface', 'Youngs_97_intraslab', 'Combo_Sadigh_Youngs_M8', 'Somerville09_Yilgarn', 'Somerville09_Non_Cratonic', 'Chiou08', 'Campbell08', 'Liang_2008', 'Campbell03', 'Atkinson06_hard_bedrock', 'Atkinson06_soil', 'Atkinson06_bc_boundary_bedrock', 'Zhao_2006_intraslab', 'Atkinson_2003_interface', 'Akkar_2010_crustal', 'Zhao_2006_interface', 'Atkinson_2003_intraslab']
atten_model_weights = [0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456, 0.045454545454545456]
atten_collapse_Sa_of_atten_models = True
atten_variability_method = None
atten_periods = [0.0, 0.30303000000000002, 1.0]
atten_threshold_distance = 100
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

# Capacity Spectrum Method

# Loss

# Save
save_hazard_map = True

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
