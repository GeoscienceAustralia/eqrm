"""
 Title: util.py
 
  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, duncan.gray@ga.gov.au
           
  Description: A collection of low level functions that do not fit else where.
 
  Version: $Revision: 1692 $  
  ModifiedBy: $Author: rwilson $
  ModifiedDate: $Date: 2010-06-14 11:55:08 +1000 (Mon, 14 Jun 2010) $
  
  Copyright 2007 by Geoscience Australia
"""

import os
import sys
import csv
import exceptions
import platform
import tempfile
import shutil
import random
from subprocess import call
from copy import deepcopy
from os import remove, mkdir, access, F_OK, sep, path
from scipy import array, log, newaxis, exp


def determine_eqrm_path(file=__file__):
    """
    Workout a path string that describes the directory eqrm_code is in.
    """
    current_dir, tail = os.path.split(file)
    # Since this is the eqrm_code dir and we want the python_eqrm dir
    if current_dir == '':
        parrent_dir = '..'
    else:
        parrent_dir = os.path.join(current_dir, '..') 
    # eqrm_dir is relative, eg '..' when running demos
    # eqrm is absolute when running check scenarios Q:\python_eqrm

    return parrent_dir

def get_local_or_default(filename, default_input_dir, input_dir=None):
    """Look for a file in the input directory, then default input directory.

    filename           required file *name*, not path
    default_input_dir  the default input directory
    input_dir          the expected input directory

    Returns an open file handle.  Raises IOError if can't find file.
    """

    try:
        if input_dir is None:
            raise IOError
        path = os.path.join(input_dir, filename)
        fid = open(path)
    except IOError:
        try:
            path = os.path.join(default_input_dir, filename)
            fid = open(path)
        except IOError:
            msg = ('%s was not in input_dir or default_input_dir'
                   % filename)
            raise IOError(msg)

    return fid	

def dict2csv(filename, title_index, attributes):
    """Write a ',' separated CSV file (with header line) from a dictionary.
   
    filename     the path to the file to write
    title_index  a dictionary: {<column title>: [data, data, ...], ...}
    attributes   a dictionary: {<column_title>: <column_index>, ...}

    For example:
        title_index = {'A': ['A1', 'A2'], 'B': ['B1', 'B2']}
        attributes = {'B': 1, 'A': 0}
    creates a file:
        A,B
        A1,B1
        A2,B2
    """

    fd = open(filename, 'wb')
    writer = csv.writer(fd)
    
    # Write the header line
    line = [None] * len(title_index)
    for title in title_index:
        line[title_index[title]]= title
    writer.writerow(line)
        
    # Write the values to a cvs file
    value_row_count = len(attributes[title_index.keys()[0]])
    for row_i in range(value_row_count):
        line = [None] * len(title_index)
        for title in title_index:
            line[title_index[title]] =  attributes[title][row_i]
        writer.writerow(line)
    fd.close()

def reset_seed(use_determ_seed=False):
    """Set random seeds.

    use_determ_seed  True if we use a fixed seed (for testing)
    """
    
    from random import seed as pyseed
    from random import random
    from numpy.random import seed

    if use_determ_seed:
        # reset both seeds to a deterministic inital state
	pyseed(11)
	seed(10)
    else:
        from time import time 

	pyseed(int(time()))
	seed(int(999*random()+time()))

def get_weave_dir():
    """Get the weave output directory."""

    version = platform.python_version().split(".")
    python_tag = "python" + str(version[0]) + str(version[1])

    if sys.platform == 'linux2':
        python_dir = "." + python_tag + "_compiled"
        weave_path = os.path.join(os.environ["HOME"], python_dir)
    else:
        python_dir = python_tag + "_compiled"
        weave_path = os.path.join(tempfile.gettempdir(),
                                  os.environ["USERNAME"],
                                  python_dir)
    return weave_path

class WeaveIOError(exceptions.Exception):
    def __init__(self, errno=None, msg=None):
        msg = ("%s directory is full. Space is needed to compile files."
               % get_weave_dir())
        raise IOError(msg)

def run_call(command, dir=None, python_command='python'):
    """Run a command as a subprocess.  Results go to screen.

    command         The python code to run, relative to the eqrm_root directory.
    dir             The python_eqrm directory of the EQRM code being tested.
    python_command  If you don't want to use the standard python,
                    pass in the python to run. eg 'python2.4'

    Returns the exit status of the subprocess.  0 means OK (unix only?).
    """
    
    if dir is None:
        dir = determine_eqrm_path()
    dir = os.path.abspath(dir)   
    
    local_env = deepcopy(os.environ)
    local_env["PYTHONPATH"] = dir
    
    command_path = os.path.join(dir, command)
    retcode = call((python_command, command_path), env=local_env)
        
    return retcode

def add_directories(root_directory, directories):
    """Create a nested sub-directory path.

    root_directory  base of the created directory path
    directories     iterable of sub-directories to create under 'root_directory'

    Returns the final ('leaf') directory of the created sub-directory path.
    eg:
        add_directories('tom', ['dick', 'harry'])
    returns 'tom/dick/harry'.
    """

    dir = root_directory
    for new_dir in directories:
        dir = os.path.join(dir, new_dir)
        if not access(dir, F_OK):
            mkdir(dir)

    return dir

def add_last_directory(input_dir):
    #input_dir = os.path.abspath(input_dir)
    head, tail = os.path.split(input_dir)
    if tail == "":
        head, tail = os.path.split(head)
    if not access(input_dir,F_OK):
            mkdir(input_dir)
    return dir

def del_files_dirs_in_dir(folder):
    """
    Delete all the files and folders in a folder.

    If the folder is not present, make the last directory of the folder.
    """
    
    def handleRemoveReadonly(func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
            func(path)
        else:
            raise
    
    if access(folder,F_OK):
        shutil.rmtree(folder, ignore_errors=False, onerror=handleRemoveReadonly)
    mkdir(folder)


# def obsolete_compile_weave_functions():
# 	"""
# 	See if all of the weave code can compile.  If not, throw an IOError.
#         This is to catch if the compiled weave code cannot be written.
#         This happens if a users drive is full.

#         This is a bit hacky, since when new weave code is added it has
#         to be added here as well.  And I have to find all the current
#         weave code...
# 	"""

#         from ground_motion_interface import gound_motion_init
#         from eqrm_code.regolith_amplification_model import \
#              Regolith_amplification_model
#         from eqrm_code.ground_motion_distribution import \
#              Log_normal_distribution
#         from eqrm_code.capacity_spectrum_functions import calculate_capacity, \
#              calculate_updated_demand

#         # ground motion interface weaves
#         distance = array([[[8.6602540]]])
#         mag = array([[[8.0]]])
#         coefficient = array([1,2,3,4,5,6,5])
#         coefficient.shape = (-1, 1, 1, 1)
#         sigma_coefficient = coefficient
        
#         distribution = gound_motion_init[
#             'Toro_1997_midcontinent'][0]        
#         log_mean,log_sigma = distribution(
#             mag=mag,
#             distance=distance,
#             coefficient=coefficient,
#             sigma_coefficient=sigma_coefficient)
        
#         distribution = gound_motion_init[
#             'Atkinson_Boore_97'][0]
#         coefficient = array([1,2,3,4])
#         coefficient.shape = (-1, 1, 1, 1)
#         sigma_coefficient = array([1])
#         sigma_coefficient.shape = (-1, 1, 1, 1)       
#         log_mean,log_sigma = distribution(
#             mag=mag,
#             distance=distance,
#             coefficient=coefficient,
#             sigma_coefficient=sigma_coefficient)

#         distribution = gound_motion_init[
#             'Sadigh_97'][0]
#         coefficient = array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
#         coefficient.shape = (-1, 1, 1, 1)
#         sigma_coefficient = array([1,2,3])
#         sigma_coefficient.shape = (-1, 1, 1, 1)       
#         log_mean,log_sigma = distribution(
#             mag=mag,
#             distance=distance,
#             coefficient=coefficient,
#             sigma_coefficient=sigma_coefficient)
        
#         # regolith amplification model weave
#         pga=array((0.05,0.1))
#         moment_magnitude=array((4.5,5.5,6.5))
#         periods=array((0.0,0.01))

#         log_ampC=array((((0.36327,0.36327+1),(0.33203,0.33203+1),
#                          (0.29231,0.29231+1)),
#                         ((0.36298,0.36298+1),(0.34226,0.34226+1),
#                          (0.31896,0.31896+1)))).swapaxes(0,1)

#         log_ampD=array((((0.74521,0.74521),(0.78958,0.78958),
#                          (0.80831,0.80831)),
#                         ((0.61605,0.61605),(0.66287,0.66287),
#                          (0.69683,0.69683)))).swapaxes(0,1)

#         log_stdC=array((((0.26331,0.26331),(0.25138,0.25138),
#                          (0.23645,0.23645)),
#                         ((0.26153,0.26153),(0.2527,0.2527),
#                          (0.24392,0.24392)))).swapaxes(0,1)

#         log_stdD=array((((0.18982,0.18982),(0.17712,0.17712),
#                          (0.16832,0.16832)),
#                         ((0.20337,0.20337),(0.19081,0.19081),
#                          (0.18001,0.18001)))).swapaxes(0,1)

#         log_amplifications={'CD':log_ampC,'D':log_ampD}
#         log_stds={'CD':log_stdC,'D':log_stdD}
        
#         regolith_amp_distribution = Log_normal_distribution(
#             1,
#             1,
#             num_psudo_events=2,
#             num_sites_per_site_loop=5)
        
#         amp_model=Regolith_amplification_model(
#             pga,moment_magnitude,periods,
#             log_amplifications,log_stds,
#             distribution_instance=regolith_amp_distribution)
        
#         log_ground_motion=log(array([[[0.05,0.1],[0.1,0.1]],
#                                      [[0.05,0.05],[0.05,0.1]]]))
#         # add periods dimension
#         log_ground_motion=log_ground_motion[...,newaxis] 
#         # 2 spawnings
#         site_classes=array(('CD','D'))
#         Mw=array((4.5,6.5))
#         event_periods=array([0,0.01])

#         dist= amp_model.distribution(exp(log_ground_motion),
#                                      site_classes,
#                                      Mw,event_periods)
        
#         # capacity_spectrum_functions weaves
#         # calculate_capacity, hitting 2 weaves
#         surface_displacement=array([0,1])        
#         surface_displacement.shape=1,2,-1                
        
#         Ay,Dy,Au,Du=(0.13417,2.9975,0.26833,41.964)
#         aa,bb,cc,kappa=(-0.3647,0.33362,0.26833,0.001)
#         capacity_parameters=Dy,Ay,Du,Au,aa,bb,cc       
#         capacity_parameters=array(capacity_parameters)[:,newaxis,newaxis,newaxis]
#         capacity=calculate_capacity(surface_displacement,capacity_parameters)
        
#         surface_displacement.shape=1,1,-1 
#         capacity=calculate_capacity(surface_displacement,capacity_parameters)

#         # calculate_updated_demand, hitting 2 weaves
#         SA=array([0.342010,0.763370,0.653840,0.530630,0.44294,
#                   0.38397,0.34452,0.321240,0.302940,0.276640,
#                   0.248310,0.15958,0.11005,0.080179,0.055094,
#                   0.039724,0.029105,0.021409,0.015748])
#         SA.shape=1,1,-1

#         SD=array([0,1.895,6.4923,11.855,17.593,23.829,
#                   30.789,39.074,48.129,55.625,61.64,
#                   89.128,109.27,124.4,123.09,120.8,
#                   115.6,107.62,97.732])
#         SD.shape=1,1,-1
        
#         TAV=array([[0.46795]])
#         TVD=array([[12.589]])
        
#         periods=array([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,
#                      1.5,2,2.5,3,3.5,4,4.5,5])

#         Ra = array([1.1804142])
#         Rv = array([1.13213065])
#         Rd = array([1.1044449])
#         TAV=TAV*(Ra/Rv)
#         Ra.shape=1,1,1
#         Rv.shape=1,1,1
#         Rd.shape=1,1,1
        
#         SAnew,SDnew=calculate_updated_demand(
#             periods,SA,SD,Ra,Rv,Rd,TAV,TVD)

#         # second weave
#         periods=array([0])
#         num_periods = len(periods)
#         num_sites = 1
#         num_events = 2
#         SA = array([0.342010,0.763370])
#         SA.shape = num_sites, num_events, num_periods
        
#         SD = array([0,1.895])
#         SD.shape = num_sites, num_events, num_periods
#         TAV = array([0.48, 0.48])
#         TAV.shape = num_sites, num_events
#         TVD = array([12.48, 12.48])
#         TVD.shape = num_sites, num_events
#         Ra = array([1.1804142,1 ])
#         Rv = array([1.13213065, 1])
#         Rd = array([1.1044449, 1])
#         Ra.shape = num_sites, num_events,-1
#         Rv.shape = num_sites, num_events,-1
#         Rd.shape = num_sites, num_events,-1

        
#         SAnew,SDnew = calculate_updated_demand(
#             periods,SA,SD,Ra,Rv,Rd,TAV,TVD)
#         print "*******************************"
#         print "fin"
#         print "*******************************"
        
################################################################################

if __name__ == "__main__":
    compile_weave_functions()
