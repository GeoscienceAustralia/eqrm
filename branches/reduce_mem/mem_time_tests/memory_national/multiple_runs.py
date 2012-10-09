"""
Run multipe EQRM simulations, to get time and memory metrics. 
"""

import subprocess 
import os

import eqrm_code.util
from eqrm_code import util
from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user, \
     ParameterData, create_parameter_data, eqrm_flags_to_control_file

from eqrm_code.analysis import main

class ListLengthError(Exception):
    pass
    
def create_base():
    sdp = ParameterData()
    
    # Operation Mode
    sdp.run_type = "hazard" 
    sdp.is_scenario = False
    sdp.site_tag = "bench"
    sdp.return_periods = [100.75, 200.0, 300.0, 400.0, 500.0, 
    600.0, 700.0, 800.0, 900]
    
    sdp.input_dir = os.path.join(eqrm_data_home(), 'test_national',
                      'memory_input')
    sdp.output_dir = os.path.join(eqrm_data_home(), 'test_national', 
                      'memory_output','trial_matrix')
    
    sdp.use_site_indexes = True #False 
    sdp.site_indexes = [1]
    sdp.event_control_tag = "use" 
    sdp.zone_source_tag = ""
    
    # Probabilistic input
    sdp.prob_number_of_events_in_zones = [1,1,1,1]
    
    # Attenuation
    sdp.atten_collapse_Sa_of_atten_models = True
    sdp.atten_variability_method = None
    sdp.atten_periods = [0.0, 0.2, 1.0]
    sdp.atten_threshold_distance = 400
    sdp.atten_override_RSA_shape = None
    sdp.atten_cutoff_max_spectral_displacement = False
    sdp.atten_pga_scaling_cutoff = 2
    sdp.atten_smooth_spectral_acceleration = None
    
    # Amplification
    sdp.use_amplification = False
    sdp.amp_variability_method = None
    sdp.amp_min_factor = 0.6
    sdp.amp_max_factor = 10000
    
    # Save
    sdp.save_hazard_map = True
    
    
    return sdp

def build_runs_list():
    runs = []
    num_sources = 4
    # The base run
    sdp = create_base()
    sdp.output_dir = os.path.join(eqrm_data_home(), 'test_national', 
                      'memory_output','trial_matrix')
    runs.append({"processes":1, "sdp":sdp})

    # Testing parallel
    sdp = create_base()
    sdp.output_dir = os.path.join(eqrm_data_home(), 'test_national', 
                      'memory_output','trial_parallel')
    sdp.site_indexes = [1, 2]
    #runs.append({"processes":2, "sdp":sdp})

    # increasing events, 2 sites
    for events in [1000, 10000, 100000]:
        sdp = create_base()
        sdp.output_dir = os.path.join(eqrm_data_home(), 'test_national', 
                                      'memory_output','events_' + str(events))
        events_source = events/num_sources
        sdp.prob_number_of_events_in_zones = [events_source]*num_sources
        sdp.site_indexes = [1, 2]
        runs.append({"processes":1, "sdp":sdp})

    
    # Testing all sites
    sdp = create_base()
    sdp.output_dir = os.path.join(eqrm_data_home(), 'test_national', 
                      'memory_output','trial_all_sites')
    sdp.use_site_indexes = False 
    #runs.append({"processes":2, "sdp":sdp})
    
    # increasing events, all sites
    for events in [1000, 10000]: #, 100000]:
        for proc in [1,2,4]:
            sdp = create_base()
            dir_name = 'sites_' + str(17277) + '_events_' + str(events) + \
                '_' + 'proc_'+ \
                str(proc)
            sdp.output_dir = os.path.join(eqrm_data_home(), 'test_national', 
                                          'memory_output',
                                          dir_name)
            events_source = events/num_sources
            sdp.prob_number_of_events_in_zones = [events_source]*num_sources
            sdp.use_site_indexes = False 
            #runs.append({"processes":proc, "sdp":sdp})

    return runs

def multi_run(runs):
    """
    Run several simulations
    
    Arg:
    runs - A list of dictionaries. 
        Dic; "processes"; The number of processes
             "sdp"; The event control file parameters
             
    """
    for run in runs:
        control_file = 'temp.py'
         # Build the base eqrm_flags.
        flags = create_parameter_data(run["sdp"])
        num_nodes = run["processes"]
        # Write an EQRM control file, then do an mpi run call
        eqrm_flags_to_control_file(control_file, flags)
        (cluster, _) = util.get_hostname()
    
        cmd = mpi_command(cluster, num_nodes, control_file)
        subprocess.call(cmd)
            
    
    
def mpi_command(cluster, num_procs, control_file):
    """
    Build the mpi command to execute the simulation in parallel.
    
    Args:
      cluster - The cluster name.
      num_procs - The number of processes to run the simulation on.
      control_file - The EQRM control file.
      machines_file - the mpi machines_file
    """

    if cluster == 'rhe-compute1':
        cmd = ['mpirun','-np',str(num_procs),
               '-x','PYTHONPATH','-x','EQRMDATAHOME',
               'python', control_file]
    elif cluster == 'alamba':
        cmd = ['mpirun','-np',str(num_procs),'-hostfile'
               , '/home/graydu/.machines_alamba', '-x','PYTHONPATH',
               '-x','EQRMDATAHOME',
               'python',control_file]
    else:
        cmd = ['mpirun','-np',str(num_procs),
               '-x','PYTHONPATH','-x','EQRMDATAHOME',
               'python', control_file]
    return cmd
    
def create_sites_list(num_sites, max_sites):
    """
    Create a list, representing site indexes.  Have the numbers spread out
    over the posible number of sites.  The list will be num_sites long.
    
    Args:
    num_sites - The number of sites in the list
    max_site_index - The maximum site index number.
    """
    
    step = max_site_index//num_sites
    if step == 0:
        whole_site_list = num_sites//max_site_index
        remainder = num_sites%max_site_index
        site_indexs = []
        for wsl in range(len(whole_site_list)):
            site_indexs.extend(range(1, ))
    return 
 

def output_dir_basic(**kwargs):
    return os.path.join('.', 'test_ev' + events)
       

def test_run():
    runs = build_runs_list()
    multi_run(runs)

#-------------------------------------------------------------
if __name__ == "__main__":
    test_run()
