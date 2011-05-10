"""

Title: check_scenarios.py - Run the implementation scenarios then check
  the results in the current dir against the results in the standard
  directory.

  Also used to check the mini_scenarios, which is a subset of scenarios.
  It is used for a quick basic check.
  
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  CreationDate:  2007-08-20 

  Description:
  
   This script checks if the results in the 'current' dir are
   different from the results in the 'standard' dir.

   The results in 'standard' dir represent the correct results.

  To suppress the running the implementation scenarios, do;
  python check_scenarios.py no_run OR
  python check_scenarios.py n

  The THE_PARAM_T.txt files are skipped.

  Timings are also measured and stored in scenario_performance.asc.

  To reset the standard timings, delete the file 
  python_eqrm\implementation_tests\timing\standard*.asc

  This can be run in parallel, to test running parallel scenarios,
  rather than for speed.  For example;
  mpirun -np 4 -hostfile ~/.machines_cyclone python check_scenarios.py
  [Running this is parallel is now broken.]

  Note: Running the tests in parallel is a bit iffy, since some nodes
  can start checing if the tests pass before process 0 has produced
  the output.
  
  Version: $Revision: 1674 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-05-12 17:09:06 +1000 (Wed, 12 May 2010) $
  
  Copyright 2007 by Geoscience Australia
"""

import sys
import time
from os import sep, walk, listdir, path, remove
import socket
import csv
import os

from os.path import join, splitext, abspath

from scipy import asarray, allclose

from eqrm_code import analysis
from eqrm_code.get_version import get_version
from eqrm_code.parallel import Parallel
from eqrm_code import util
from eqrm_code.ANUGA_utilities import log
from eqrm_code import parse_in_parameters

log.console_logging_level = log.WARNING
log.default_to_console = False

eqrm_path = util.determine_eqrm_path()

IMP_DIR = join(eqrm_path, 'implementation_tests')
SCENARIO_DIR = join(IMP_DIR, 'scenarios')

STANDARD_DIR = join(IMP_DIR, 'standard')

CURRENT_DIR = join(IMP_DIR, 'current')

TIMING_DIR = join(IMP_DIR, 'timing')

STANDARD_STRING = "standard_timings_"
CURRENT_STRING = "current_timings_"
MINI_STANDARD_STRING = "mini_standard_timings_"
MINI_CURRENT_STRING = "mini_current_timings_"
FILE_EXTENTION = '.asc'

MINI_PAR_FILES = ['TS_haz38.py',
                  'TS_haz39.py',
                  'TS_risk63.py']
                  
PARALLEL_FILES = ['TS_haz05.py', 'TS_haz09.py', 'TS_haz12.py',
                  'TS_haz19.py',
                  'TS_risk20.py',
                  'TS_risk21.py', 'TS_risk22.py', 
                  'TS_risk32.py',
                  'TS_risk33.py', 'TS_risk34.py', 'TS_risk58.py',
                  'TS_risk60.py' ]
                  
class BadDirectoryStructure(Exception):
    pass
                  
def par_files(path='.', extension=".py", files=None):
    """ Find all the parameter data files in the scenario dir
    """
    if files is None:
        files = listdir(path)
        par_files = [x for x in files if x[-3:] == extension]
        
        # if this is being run is parallel,
        # only do the scenarios with no variability.
        para = Parallel()
        if para.is_parallel is True:
            if path is SCENARIO_DIR:
                par_files = PARALLEL_FILES
                print "WARNING: Running in parallel mode"
                print "Only scenarios with no randomness will be executed"
        #par_files = ['TS_haz20.py']
        #par_files = ['TS_risk60.py',''TS_haz20.py']
        par_files.sort()
        par_files.reverse()
    else:
        par_files = files
    return par_files

def run_scenarios(scenario_dir=SCENARIO_DIR, current_string=CURRENT_STRING,
                  extension='.py', files=None):  
    """
    Run all of the the scenario's in the scenario_dir.

    parameters:
      scenario_dir: The path to the directory of scenarios
      current_string: Used in the timing file name
      extension: The last three characters of the scenario files.
      Bad hack to represent the file extension of the scenarios.
      Currently .py or par.

    Write timings and svn info to a file.
    """
    timings = {}
    delimiter = ','
    ofile = 'imp_test_performance.asc'
    fd = open(ofile,'a')
    fd.write("version" + delimiter +
             "last_check_in_date" + delimiter +
             "modification_status" + delimiter +
             "scenario_file" + delimiter +
             "scenario_time" + "\n")
    files = par_files(scenario_dir, extension=extension, files=files)
    output_dirs = []
    for file in files:
        pull_path = join(scenario_dir, file)
        THE_PARAM_T = parse_in_parameters.create_parameter_data(pull_path)
        output_dirs.append(join(THE_PARAM_T['output_dir']))
        print "Running scenario", file
        #Initial time and memory
        t0 = time.clock()
        
        # Run the scenarios
        analysis.main(pull_path, True)
        root, ext = splitext(file)
        time_taken_sec = (time.clock()-t0)
        timings[root] = time_taken_sec
        version, date, modified = get_version()
        fd.write(str(version) + delimiter +
                 str(date) + delimiter +
                 str(modified) + delimiter +
                 str(file) + delimiter +
                 str(time_taken_sec) + "\n")
    fd.close()
    timings =  Scenario_times(timings, current_string=current_string)
    return timings, output_dirs
        
def file_diff(fileA, fileB):
    """
    returns false if the files are different, and the first lines that are
    different.

    returns
    is_same
    lineA
    lineB

    Maybe in the future do something different, such as also return how many
    lines, out of the total number of lines are different.
    """
    #print "fileB", fileB
    A = open(fileA)
    textA = A.read().splitlines()
    A.close()

    B = open(fileB)
    textB = B.read().splitlines()
    #textB = B.read().split('\n')
    B.close()

    for lineA, lineB in map(None, textA, textB):
        if not lineA == lineB:
            try:
                float_same = float_line_diff(lineA, lineB)
            except: #FIXME What is being caught? can it be caught sooner?
                float_same = False
            if lineA is not None and lineA.find(".input_dir") >= 0:
                # This line has linux/windows / \ differences
                # in THE_PARAM_T.py
                # So let's not care if it is different!
                return True, None, None
            if not float_same:
                return False, lineA, lineB
    return True, None, None

def float_line_diff(lineA, lineB,
                    relative_tolerance=1e-10):
    """
    relative_tolerance=1e-1 still gives a failed file in Linux
    
    If there is a difference in the lines in a file, it might
    be a relative difference.  Let's check.

    NOTE: This is currently being used when implementation testing, since
    the files are currently exactly the same.
    """
    
    # Seperate based on the delimiter
    # White space stripped from both ends, then delimted on
    lineA_list = lineA.split() 
    lineB_list = lineB.split()

    try:
        [float(i) for i in lineA_list]
    except:
        lineA_list = lineA.split(',')
        lineB_list = lineB.split(',')
        

    # Convert the strings to floats
    temp_line = []
    lineA = [float(i) for i in lineA_list]
    lineB = [float(i) for i in lineB_list]
    
    arrayA = asarray(lineA)
    arrayB = asarray(lineB)
    is_same = allclose(arrayA, arrayB, rtol=relative_tolerance)
    return is_same
    
def print_diff_results(diff_results):
    for diff_result in diff_results:
        print "======================================================================"
        print "File difference:", diff_result[0]
        print "----------------------------------------------------------------------"
        print "First line difference;"
        print "Standard line:", diff_result[1]
        print " Current line:", diff_result[2]
        print
     
     
def check_dir_names(dir_list, current_dir):
    """
    Given a list of directory paths this function returns a list of
     last directory names, and checks that these directories are in the
    current_dir.
    eg dir_list = ['./implementation_tests/current/TS_haz38/', 
    './implementation_tests/current/TS_haz39/', 
    './implementation_tests/current/TS_risk63/']
    current_dir = './implementation_tests/current'
        Returns    ['TS_haz38', 'TS_haz39', 'TS_risk63']
        
    parameters
    dir_list - a list of directory paths.
    current_dir - a directory path.
    """
    last_dir = []
    for path in dir_list:
        path, folder = os.path.split(path)
        if folder == "":
            path, folder = os.path.split(path)        
        last_dir.append(folder)
        if not os.path.abspath(path) == os.path.abspath(current_dir):
            msg = "os.path.abspath(path)", os.path.abspath(path)
            msg += "does not equal os.path.abspath(current_dir)", \
                os.path.abspath(current_dir)
            raise BadDirectoryStructure(msg)
    #print "last_dir", last_dir
    return last_dir
    
def check_scenarios(standard_dir=STANDARD_DIR, current_dir=CURRENT_DIR,
                    scenario_dirs=None):
    """
    Go into each results dir from the current and standard dirs
    And in each dir check that all the files are the same
    
    """
    # Create a list of the directories the test results are in.
    if scenario_dirs is None:
        scenario_dirs = listdir(standard_dir)
    else:
        scenario_dirs = check_dir_names(scenario_dirs, current_dir)
        
    missing_current_files = []
    diff_results = [] # the dir and name of the different file, and the
                      # lines that are different
    files_checked = 0
    diff_files = 0
    #print "scenario_dirs", scenario_dirs
    try:
        scenario_dirs.remove('.svn')
    except:
        pass
    for dir in scenario_dirs:
        result_files = listdir(join(standard_dir, dir))
        result_files = [x for x in result_files if not x[-4:] == '.lic']
        result_files = [x for x in result_files if not x[0] == '.']
        result_files = [x for x in result_files if not x[0:3] == 'log']
        
        #print "result_files", result_files
        try:
            result_files.remove('.svn')
        except:
            pass
        try:
            result_files.remove('THE_PARAM_T.pyc')
        except:
            pass
        try:
            result_files.remove('THE_PARAM_T.txt')
        except:
            pass
        try:
            result_files.remove('log.txt')
        except:
            pass
        for file in result_files:
            current_file = join(current_dir, dir, file)
            #print "current_file", current_file
            if not path.exists(current_file):
                missing_current_files.append(current_file)
                continue
            standard_file = join(standard_dir, dir, file)
            print ".", # To show something is happening
            is_same, lineA, lineB = file_diff(standard_file,
                                                          current_file)
            #remove(current_file)
            files_checked += 1
            if not is_same:
                print "F",
                diff_results.append((join(dir, file), lineA, lineB))
                diff_files += 1
    print ;  print
    for file in missing_current_files:
        print "Missing file:", file
    print_diff_results(diff_results)
    print "%i files missing." %(len(missing_current_files))
    print "Checked %i files. %i failed." %(files_checked, diff_files)
    return len(missing_current_files) + diff_files
 
class Scenario_times(object):
    """ Class to handle the reading and writing of scenario time csv files.
    """
    def __init__(self,
                 timings_dic,
                 timing_dir=TIMING_DIR,
                 host=socket.gethostname(),
                 current_string=CURRENT_STRING):
        
        self.timings_dic = timings_dic      
        self.host =  host
        self.timing_dir = abspath(timing_dir)
        self.save(file_string=current_string)
        
        
    def save(self, file_string=CURRENT_STRING):
        """
        Save the timing file
        """
        file_name = self.timing_dir + sep + file_string + self.host \
                    + FILE_EXTENTION
        fd = open(file_name,'wb')
        writer = csv.writer(fd)
        
        #Write the title to a cvs file
        writer.writerow(['scenario','time_seconds'])

        # Write the values to a cvs file
        writer.writerows(self.timings_dic.items())
        
    def read_standard(self, file_string=STANDARD_STRING):
        file_name = self.timing_dir + sep + file_string + self.host \
                    + FILE_EXTENTION
        try:
            fd = file(file_name)
        except IOError:
            return None          

        reader = csv.reader(fd)
        titles = reader.next()

        standard_dic = {}
        for line in reader:
            # Lets not worry about extensions
            root, ext = splitext(line[0])
            standard_dic[root] = float(line[1])
        return standard_dic
        

    def compare_times(self, standard_string=STANDARD_STRING,
                      verbose=True):
        """
        Compare the current times against standard times

        If there are no standard times, then these times are written
        as standard times
        """
        if verbose:
            print "Compare timings (Wall clock, so processor activity can cause test failure)"
        standard = self.read_standard(standard_string)
        if standard is None:
            self.save(file_string=standard_string)
            results = None
            fail_dic = None
            if verbose: print "No standard time file.  Creating new file."
        else:
            results, fail_dic = self.compare_known_times(standard,verbose)
        return results, fail_dic

    def compare_known_times(self, standard, verbose=True):
        """
        Compare the current times against a standard.

        If the standard has timings that the current doesn't have, that's
        a fail

        If the standard and current timing keys do not match, write the
        current to file.
        
        """
        results = ''
        fail_dic = {}
        standard_keys = standard.keys()
        standard_keys.sort()
        for s_key in standard_keys:
            if self.timings_dic.has_key(s_key):
                if self.timings_dic[s_key] < standard[s_key]*1.2:
                    results +='.'
                    if verbose: print '.',
                else:
                    results +='F'
                    if verbose: print 'F',
                    fail_dic[s_key] = [standard[s_key],self.timings_dic[s_key]]
            else:
                results +='F'
                if verbose: print 'F',
                fail_dic[s_key] = [standard[s_key],-999.999]
        current = self.timings_dic.keys()
        current.sort()
        if not standard_keys == current:
            # The scenarios are not the same
            if verbose:
                print
                print 'WARNING: The scenario names have changed.'
                print 'Cannot compare all scenario times'
                print "standard_keys", standard_keys
                print "current", current
                print "Timing files are in the directory " + self.timing_dir
        if verbose:
            print
            print '--------------------------------'
            if len(fail_dic) == 0:
                print "Timings OK"
            else:
                print 'Failed Scenarios'
                for fail in fail_dic.items():
                    print "%s has standard of %f, current %f" %(fail[0],
                                                                fail[1][0],
                                                                fail[1][1])
                
        return results,fail_dic
        
            
    def delete(self, file_string=STANDARD_STRING):
        """
        fails silently
        """
        file_name = self.timing_dir + sep + file_string + self.host \
                    + FILE_EXTENTION
        try:
            remove(file_name)
        except:
            pass

        
def check_scenarios_main(scenario_dir=SCENARIO_DIR,
                         standard_dir=STANDARD_DIR,
                         standard_string=STANDARD_STRING,
                         current_dir=CURRENT_DIR,
                         current_string=CURRENT_STRING,
                         files=None): 
    
    try:
        import planning.is_sandpit
        check_times=True
    except:
        check_times=False
    if len(sys.argv) > 1 and sys.argv[1][0].upper() == 'N':
        check_times = False
        output_dirs = None
    else:
        para = Parallel()
        if para.is_parallel is True:
            check_times = False 
        scenario_times, output_dirs = run_scenarios(scenario_dir,
                                                    current_string,
                                                    extension='.py',
                                                    files=files)
    c_failed_missing_file = check_scenarios(standard_dir,
                                            current_dir,
                                            scenario_dirs=output_dirs)
    if check_times is True:
        scenario_times.compare_times(standard_string)
    return c_failed_missing_file

# Note, the constants are different
def mini_check_scenarios_main():
    c_failed_missing_file =check_scenarios_main(
        files=MINI_PAR_FILES)
    return c_failed_missing_file
        
#-------------------------------------------------------------
        
if __name__ == "__main__":
    import os    
    os.chdir('..')
    c_failed_missing_file = check_scenarios_main()
    sys.exit(c_failed_missing_file) 
