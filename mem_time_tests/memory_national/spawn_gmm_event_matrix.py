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
    sdp.max_width = 15
    sdp.site_tag = "bench"
    sdp.return_periods = [100.75, 200.0, 300.0, 400.0, 500.0, 
    600.0, 700.0, 800.0, 900]
    
    sdp.input_dir = os.path.join(eqrm_data_home(), 'test_national',
                      'memory_input')
    sdp.output_dir = os.path.join(eqrm_data_home(), 'test_national', 
                      'memory_output','trial_matrix')
    
    sdp.use_site_indexes = False 
    sdp.site_indexes = [1]
    sdp.event_control_tag = "use" 
    
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

def multi_run(base_control,
              nodes, 
              sites=None,
              max_site_index=None,
              input_dir=None,
              output_dir_funct=None,
              total_events=None, 
              #execute=True, 
              **kwargs):
    """
    Run several simulations
    
    Arg:
    base_control -  will have the initial paramters.
    input_dir_funct -  a function that can make the input_dir string, 
                       **kwargs is passed in.
    output_dir_funct -  a function that can make the output_dir string, 
                       **kwargs is passed in.
    nodes - a list of the number of nodes to run each simulation on.
            The first value is for the first simulation ect.
    sites - a list of number of sites to run each simulation on.
            The first value is for the first simulation ect.
            The sites chosen will be spread out.
    max_site_index - The number of sites in the site file.
    total_events - a list of the number of events to run each simulation on.
            The first value is for the first simulation ect.
    **kwargs - Each key is an eqrm control file attribute. The value is
            a lists of vaules to go into each simulation.
             The first value is for the first simulation ect.
    """
    control_file = 'temp.py'
    # Build the base eqrm_flags.
    flags = create_parameter_data(base_control)
    
    # First check that all the array sizes are correct
    runs = len(nodes)
    for k, v in kwargs.items():
        if not len(v) == runs:
            msg = k  + " list is length " + len(v) + "," + runs + \
                " was expected." 
            raise ListLengthError(msg)
     
    # Start Looping
    for i, num_nodes in enumerate(nodes):       
        
        new_flags = {}
        for k, v in kwargs.items():
            kwargs_column[k] = v[i]
            
        # Add the kwargs
        flags.update(new_flags)
        
        # Add the directories
        if output_dir_funct is not None:
            flags['output_dir'] = output_dir_funct(**flags)
        if input_dir is not None:
            flags['input_dir'] = input_dir   
        
        # Write an EQRM control file, then do an mpi run call
        eqrm_flags_to_control_file(control_file, flags)
        (cluster, _) = util.get_hostname()
    
        cmd = mpi_command(cluster, num_nodes, control_file)
        subprocess.call(cmd)
            
    
    
def mpi_command(cluster, num_procs, control_file, machines_file=None):
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
               'python', obj_file, output_dir, str(events)]
    elif cluster == 'alamba':
        cmd = ['mpirun','-np',str(num_procs),'-hostfile'
               , '/home/graydu/.machines_alamba', '-x','PYTHONPATH',
               '-x','EQRMDATAHOME',
               'python', obj_file, output_dir, str(events)]
    else:
        if machines_file is None:
            machines_file = os.path.join(os.getenv("HOME"), 
                                 '.machines_' + cluster)
            
            cmd = ['mpirun','-np',str(num_procs),'-hostfile'
                   , machines_file, '-x','PYTHONPATH','-x','EQRMDATAHOME',
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
    base = create_base()
    nodes = [1]
    kwargs = {}
    max_site_index = 17277
    sites = None
    events = 10
    
    flags = multi_run(base, 
                      nodes, 
                      sites=sites,
                      max_site_index=max_site_index, 
                      output_dir_funct=output_dir_basic, 
                      **kwargs)
    
#-------------------------------------------------------------
if __name__ == "__main__":
    test_run()
