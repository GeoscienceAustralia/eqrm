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
is_deterministic = True
max_width = 15

# Deterministic input
determ_azimith = 340
determ_depth = 11.5
determ_latitude = -32.95
determ_longitude = 151.61
determ_magnitude = 5.6
determ_dip = 35
determ_number_of_events = 1


# Attenuation
atten_models = ['Toro_1997_midcontinent']
atten_model_weights = [1]
atten_aggregate_Sa_of_atten_models = True
atten_use_variability = False
atten_periods = [0.0, 0.17544000000000001, 0.35088000000000003, 0.52632000000000001, 0.70174999999999998, 0.87719000000000003, 1.0526, 1.2281, 1.4035, 1.5789, 1.7544, 1.9298, 2.1053000000000002, 2.2806999999999999, 2.4561000000000002, 2.6316000000000002, 2.8069999999999999, 2.9824999999999999, 3.1579000000000002, 3.3332999999999999]
atten_use_rescale_curve_from_pga = False
atten_cutoff_max_spectral_displacement = False
atten_pga_scaling_cutoff = 2
atten_smooth_spectral_acceleration = None

# Amplification
use_amplification = True
amp_use_variability = False

# Save
save_hazard_map = False
save_total_financial_loss = False
save_building_loss = False
save_contents_loss = False
save_motion = True
save_prob_structural_damage = None

# General
site_tag = "newc" 
return_periods = [10, 50, 100, 200, 250, 474.56, 500, 974.78999999999996, 1000, 2474.9000000000001, 2500, 5000, 7500, 10000]
use_site_indexes = True
site_indexes = [2997, 2657, 3004, 3500]
input_dir = r".\implementation_tests\input/" 
output_dir = r".\implementation_tests\current\TS_haz20/" 

# If this file is executed the simulation will start.
# Delete all variables that are not EQRM parameters variables. 
if __name__ == '__main__':
    from eqrm_code.analysis import main
    main(locals())
