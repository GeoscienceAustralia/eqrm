import os

from eqrm_code.check_scenarios import par_files, MINI_SCENARIO_DIR
from eqrm_code.parse_in_parameters import convert_par_to_py


def convert_imp(path=MINI_SCENARIO_DIR):
    par_file_list = par_files(path)
    for par_file in par_file_list:
        convert_par_to_py(os.path.join(path,par_file))
        

        
#-------------------------------------------------------------
if __name__ == "__main__":
    # A manual change - do two backslashes before risk57
    #risk57.py:set.output_dir = ".\implementation_tests\mini_current\\risk57/"
    # this is needed if this function is run in windows.
    #convert_imp(MINI_SCENARIO_DIR)
    #convert_imp(SCENARIO_DIR)
    #convert_imp('Q:\\trunk_branches\\trunk\\scenarios\\victoria\\melbourne')
    convert_imp('Q:\\trunk_branches\\trunk\\demo')
