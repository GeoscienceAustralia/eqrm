"""
Run multipe EQRM simulations, to get time and memory metrics.
"""

import subprocess
import os
import tempfile

from eqrm_code import util
from eqrm_code.parse_in_parameters import  \
    create_parameter_data, eqrm_flags_to_control_file

from eqrm_code.analysis import main


def multi_run(runs):
    """
    Run several simulations

    Arg:
    runs - A list of dictionaries.
        Dic; "processes"; The number of processes
             "sdp"; The event control file parameters, as attributes on an
                    object

    """
    for run in runs:
        # get a temporary file
        (handle, control_file) = tempfile.mkstemp(
            '.py', 'multi_run_generated_')
        os.close(handle)

         # Build the base eqrm_flags.
        flags = create_parameter_data(run["sdp"])
        num_nodes = run["processes"]
        # Write an EQRM control file, then do an mpi run call
        eqrm_flags_to_control_file(control_file, flags)
        (cluster, _) = util.get_hostname()

        cmd = mpi_command(cluster, num_nodes, control_file)
        subprocess.call(cmd)

        # clean up
        os.remove(control_file)


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
        cmd = ['mpirun', '-np', str(num_procs),
               '-x', 'PYTHONPATH', '-x', 'EQRMDATAHOME',
               'python', control_file]
    elif cluster == 'alamba':
        cmd = [
            'mpirun', '-np', str(num_procs), '-hostfile', '/home/graydu/.machines_alamba', '-x', 'PYTHONPATH',
            '-x', 'EQRMDATAHOME',
            'python', control_file]
    elif cluster == 'rhe-compute1':
        cmd = ['mpirun', '-np', str(num_procs),
               '-x', 'PYTHONPATH',
               '-x', 'EQRMDATAHOME',
               'python2.7', control_file]
    else:
        cmd = ['mpirun', '-np', str(num_procs),
               '-x', 'PYTHONPATH', '-x', 'EQRMDATAHOME',
               'python', control_file]
    return cmd


def create_sites_list(num_sites, sites_needed):
    """
    Create a list, representing site indexes.
    The list will be num_sites long.

    Args:
    num_sites - The number of sites in the csv file
    sites_needed - The number of sites needed for a simulation.
    """

    step = sites_needed // num_sites
    site_indexs = range(1, sites_needed % num_sites + 1)
    if step > 0:
        all_sites = range(1, num_sites + 1)
        for wsl in range(step):
            site_indexs.extend(all_sites)
    return site_indexs

#-------------------------------------------------------------
if __name__ == "__main__":
    pass
