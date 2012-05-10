"""
 Title: nci_utils.py

  Author:  Ben Cooper, ben.cooper@ga.gov.au

  Description: A set of functions to assist in running EQRM at NCI

  Copyright 2012 by Geoscience Australia
"""

from datetime import timedelta
import os
from shutil import copytree, rmtree

from eqrm_code.ANUGA_utilities import log
from eqrm_code.event_set import create_event_set
from eqrm_code.parallel import Parallel
from eqrm_code.parse_in_parameters import create_parameter_data, \
                                          eqrm_flags_to_control_file

LIMIT_NODES = 64
LIMIT_MEMORY_MULTIPLIER = 4096 # 4 GB in MB, per node
LIMIT_JOBFS_MULTIPLIER = 1024 # 1 GB in MB, per node
LIMIT_WALLTIME_MULTIPLIER = lambda nodes: int(48*60*60/nodes**0.5) # NCI formula
LIMIT_MIN_MEMORY = 768

CONV_B2MB = lambda b: b/(1024*1024)

def create_nci_job(nodes, param_file):
    """
    Creates an NCI job package from the given parameter file and the number of
    nodes specified.
    """
    # Initial node number validation
    if nodes > 8 and nodes % 8 != 0:
        raise Exception('Nodes must be a multiple of 8 if greater than 8.')
    if nodes > LIMIT_NODES:
        raise Exception('The node limit is %s' % LIMIT_NODES)
        
    # Parse param_file to eqrm_flags
    eqrm_flags = create_parameter_data(param_file)
    
    # Some validation based on the event_set_handler value
    if eqrm_flags.event_set_handler is 'save':
        raise Exception('Please ensure that event_set_handler is load or generate')
    if eqrm_flags.event_set_handler is not 'load':
        log.info('')
        log.info('event_set_handler not load. Generating event set for NCI.')
        log.info('')
        
    
    # Calculate parameters required for job
    params = calc_params(eqrm_flags)
    req_memory = calc_memory(nodes, params)
    req_jobfs = calc_jobfs(nodes)
    req_walltime = calc_walltime(nodes)
    
    # Validation based on parameters
    msg = ''
    if req_memory > nodes * LIMIT_MEMORY_MULTIPLIER:
        msg = '%sRequired memory %sMB greater than limit %sMB.\n' % (msg,
                                                                     req_memory,
                                                nodes * LIMIT_MEMORY_MULTIPLIER)
    if req_jobfs > nodes * LIMIT_JOBFS_MULTIPLIER:
        msg = '%sRequired jobfs %sMB greater than limit %sMB\n' % (msg,
                                                                   req_jobfs,
                                                 nodes * LIMIT_JOBFS_MULTIPLIER)
    if req_walltime > LIMIT_WALLTIME_MULTIPLIER(nodes):
        msg = '%sRequired walltime %ssecs greater than limit %ssecs\n' % (msg,
                                                                   req_walltime,
                                               LIMIT_WALLTIME_MULTIPLIER(nodes))
    if len(msg) > 0:
        msg += 'Consider reducing the size of your simulation.'
        raise Exception(msg)
    
    # Create directory to package into
    nci_dir = os.path.join('.', 'nci_job')
    if os.path.exists(nci_dir):
        rmtree(nci_dir)
    os.makedirs(nci_dir)
    
    log.info('')
    log.info('Saving package to %s' % nci_dir)
    log.info('(replaces current directory if exists)')
    
    # Copy input, output and save data to the packaged directory
    input_dir = os.path.join(nci_dir, 'input')
    copytree(eqrm_flags.input_dir,input_dir)
    
    output_dir = os.path.join(nci_dir, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    save_dir = os.path.join(nci_dir, 'save')
    copytree(os.path.join(eqrm_flags.output_dir, 
                          '%s_event_set' % eqrm_flags.site_tag), save_dir)
    
    # Modify eqrm_flags directories for NCI
    eqrm_flags['input_dir'] = os.path.join('.', 'input')
    eqrm_flags['output_dir'] = os.path.join('.', 'output')
    eqrm_flags['data_array_storage'] = "getenv('PBS_JOBFS')"
    eqrm_flags['event_set_load_dir'] = os.path.join('.', 'save')
    
    # We always want a load job
    eqrm_flags['event_set_handler'] = "load"
    
    # Write new setdata file
    eqrm_flags_to_control_file(os.path.join(nci_dir, param_file), eqrm_flags)
    
    # Write NCI job file
    job_file = open(os.path.join(nci_dir, '%s_job' % param_file), 'w')
    job_file.write('#!/bin/bash\n')
    job_file.write('#PBS -wd\n')
    job_file.write('#PBS -q normal\n')
    job_file.write('#PBS -l ncpus=%s\n' % nodes)
    job_file.write('#PBS -l walltime=%s\n' % req_walltime)
    job_file.write('#PBS -l vmem=%sMB\n' % req_memory)
    job_file.write('#PBS -l jobfs=%sMB\n' % req_jobfs)
    job_file.write('\n')
    job_file.write('mpirun python %s\n' % param_file)
    job_file.close()
    
    log.info('')
    log.info('Now tar gzip %s and copy to NCI. e.g.' % nci_dir)
    log.info('tar czvf nci_job.tar.gz %s' % nci_dir)
    log.info('scp nci_job.tar.gz <username>@<nci_host>:/short/<project>/jobs/')
    log.info('')

def calc_params(eqrm_flags):
    """
    Calculate parameters used for the other calculations based on event set
    information.
    """
    parallel = Parallel(is_parallel=False)
    
    # TODO: Do we really need to load this in its entirety?
    (event_set, 
     event_activity, 
     source_model) = create_event_set(eqrm_flags, parallel)
    
    params = {}
    params['num_events'] = len(event_set)
    params['num_gmm_max'] = source_model.get_max_num_atten_models()
    params['num_spawn'] = eqrm_flags.atten_spawn_bins
    params['num_rm'] = event_activity.recurrence_model_count()
    params['num_periods'] = len(eqrm_flags.atten_periods)
    params['use_amplification'] = eqrm_flags.use_amplification
    params['collapse_gmm'] = eqrm_flags.atten_collapse_Sa_of_atten_models
    
    return params

def calc_memory(nodes, params):
    """
    Calculates the maximum amount of memory required for use at NCI based on
    some basic metrics. Returns amount in MB.
    
    num_events
    num_gmm_max
    num_spawn
    num_rm
    num_periods
    eqrm_flags.use_amplification
    eqrm_flags.collapse_atten_models
    
    Note: 20% is added to this to accommodate memory mapped objects and other 
    difficult to estimate items, and a min memory limit per node is also 
    applied. The idea is to be as accurate as possible while keeping the 
    complexity low.
    """
    
    num_events = params['num_events']
    num_gmm_max = params['num_gmm_max']
    num_spawn = params['num_spawn']
    num_rm = params['num_rm']
    num_periods = params['num_periods']
    use_amplification = params['use_amplification']
    collapse_gmm = params['collapse_gmm']
    
    # FIXME: calc_and_save_SA only works on a single site. When this is not the
    # case this will need to change
    num_sites = 1
    
    # Bedrock initially
    SA_temp_size = (num_sites *
                    num_events *
                    num_gmm_max *
                    num_spawn *
                    num_rm *
                    num_periods) * 8 # size in bytes of float64
    if use_amplification:
        # Soil is used
        SA_temp_size *= 2
    
    # Collapsed by attenuation models
    if collapse_gmm:
        num_gmm_collapsed = 1
    else:
        num_gmm_collapsed = num_gmm_max
    SA_temp_size_collapsed = (num_spawn *
                              num_gmm_collapsed *
                              num_rm *
                              num_sites *
                              num_events *
                              num_periods) * 8 # size in bytes of float64
    
    total_size_bytes = (SA_temp_size + SA_temp_size_collapsed) * 1.2
    
    return (LIMIT_MIN_MEMORY * nodes) + int(CONV_B2MB(total_size_bytes * nodes))

def calc_jobfs(nodes):
    """
    Returns amount of jobfs required in MB
    """
    return nodes * LIMIT_JOBFS_MULTIPLIER

def calc_walltime(nodes):
    """
    Returns max walltime in seconds according to how many nodes are given.
    TODO: revisit when statistics are better known.
    """
    return LIMIT_WALLTIME_MULTIPLIER(nodes)
