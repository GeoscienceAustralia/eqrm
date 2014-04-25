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
from scipy import array, log, newaxis, exp, logical_and


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
        line[title_index[title]] = title
    writer.writerow(line)

    # Write the values to a cvs file
    value_row_count = len(attributes[title_index.keys()[0]])
    for row_i in range(value_row_count):
        line = [None] * len(title_index)
        for title in title_index:
            line[title_index[title]] = attributes[title][row_i]
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
        seed(int(999 * random() + time()))


def get_weave_dir():
    """Get the weave output directory."""

    version = platform.python_version().split(".")
    python_tag = "python" + str(version[0]) + str(version[1])

    if sys.platform == 'win32' or sys.platform == 'win64':
        python_dir = python_tag + "_compiled"
        weave_path = os.path.join(tempfile.gettempdir(),
                                  os.environ["USERNAME"],
                                  python_dir)
    else:
        python_dir = "." + python_tag + "_compiled"
        weave_path = os.path.join(os.environ["HOME"], python_dir)
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
    if not access(input_dir, F_OK):
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
            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
            func(path)
        else:
            raise

    if access(folder, F_OK):
        shutil.rmtree(
            folder,
            ignore_errors=False,
            onerror=handleRemoveReadonly)
    mkdir(folder)


def find_period_indices(atten_periods, wanted_periods=[0.3, 1.0],
                        epsilon=1.0e-3):
    """Get the indices of the given periods in an atten periods array.

    atten_periods        1D array of atten_periods
    epsilon  acceptable 'slop' when comparing floats
    wanted_periods    The periods were index values into the atten_periods array
                      are wanted.

    Return a dictionary of wanted_periods to the indexes
    in the atten periods array.
    """
    periods_indexs = dict(zip(wanted_periods, [None] * len(wanted_periods)))

    for wanted_period in periods_indexs:
        for (i, period) in enumerate(atten_periods):
            if abs(period - wanted_period) <= epsilon:
                periods_indexs[wanted_period] = i
        if periods_indexs[wanted_period] is None:
            msg = "Can't find period %s in atten_periods %s\n" \
                % (str(wanted_period), str(atten_periods))
            raise RuntimeError(msg)
    return periods_indexs


def find_bridge_sa_indices(SA, epsilon=1.0e-3):
    """Get the indices of the 0.3 and 1.0 sec accelerations in an SA array.

    SA       spectral acceleration 1D array
    epsilon  acceptable 'slop' when comparing floats

    Return a tuple (SA0.3, SA1.0) of indices to the 0.3 & 1.0 sec accelerations.
    """
    wanted_period = find_period_indices(SA, wanted_periods=[0.3, 1.0],
                                        epsilon=epsilon)
    wanted_indexes = (wanted_period[0.3], wanted_period[1.0])

    return wanted_indexes


def convert_path_string_to_join(path):
    """
    This is to modify python scripts, changing r"./foo/bar" to
    'join('.','foo','bar')'

      Args:
        path: The string value to change to a join

      Returns:
        A join statement, as a string.
    """

    seps = ['/', '\\']
    out = multi_split(path, seps)
    # Taking out, since it is turning
    # '/nas/' to 'nas'
    #out = [x for x in out if x != '']
    if out[0] == '' and len(out) > 1:
        out.pop(0)
        out[0] = os.sep + out[0]
    # Don't make a drive reference point to a relative path
    if out[0][-1] == ':':
        out[0] += '\\\\'  # == '\\' escape characters!
    out = "', '".join(out)
    out = "join('" + out + "')"
    return out


def multi_split(split_this, seps):
    """
    Split a string based on multiple seperators.

    Args:
      split_this: the string to split.
      seps: A list of seperators.

    Returns:
     A list of strings.
    """
    results = [split_this]
    for seperator in seps:
        so_far, results = results, []
        for seq in so_far:
            results += seq.split(seperator)
    return results


def get_hostname():
    """Return (<host>, <domain>) for machine.

    For example, on the GA cyclone main node, return ('cyclone', 'agso.gov.au').
    """

    fd = os.popen('hostname')
    hostname = fd.read()
    fd.close()

    try:
        result = hostname.strip().split('.', 1)
        if len(result) < 2:
            result.append('')
    except:
        result = (hostname, '')

    return result


def string_array_equal(a1, a2):
    """Exists as np.array_equal does not work for strings. An implementation
    of the suggested fix from http://projects.scipy.org/numpy/ticket/2095"""
    return bool(logical_and.reduce((a1 == a2).ravel()))

##########################################################################

if __name__ == "__main__":
    compile_weave_functions()
