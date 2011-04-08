"""
Reflect changes in the set data .py file format in all of the set data .py
files in the sandpit.
Do this by loading up and overwriting all of the set data .py files.


"""

from eqrm_code.eqrm_filesystem import eqrm_path, demo_path, \
     Implementation_Path, mini_scenario_Path, scenario_scenarios_path, \
     mini_scenario_scenarios_path
from eqrm_code.parse_in_parameters import find_set_data_py_files, \
     old_set_data_py_2_new_set_data_py

def rewrite_set_data_py(path=None):
    """
    Reflect changes in the set data .py file format in all of the set data .py
    files in a directory and its sub directories.
    Do this by loading up and overwriting all of the set data .py files.

    parameters
      path: set data .py files in this directory will be rewritten

    DESIGN NOTE:  This way of rewriting the data set does not work
    in all cases, since
    parameters with functional values are evaluated.
    e.g. set.input_dir = set.eqrm_data_home() is evaluated.
    """
    if path is None:
        path = eqrm_path

    set_data_files = find_set_data_py_files(path)
    #print "set_data_files", set_data_files
    for file in set_data_files:
        old_set_data_py_2_new_set_data_py(file)
        

#-------------------------------------------------------------
if __name__ == "__main__":
    #rewrite_set_data_py(path=demo_path)
    #rewrite_set_data_py(path=Implementation_Path)
    #rewrite_set_data_py(path=scenario_scenarios_path)
    rewrite_set_data_py(path=mini_scenario_Path)
