"""Regression testing framework
This module will search for scripts in the same directory named
test_*.py.  Each such script should be a test suite that tests a
module through PyUnit. This script will aggregate all
found test suites into one big test suite and run them all at once.
"""

# Author: Mark Pilgrim
# Modified by Duncan Gray and Ole Nielsen

import unittest
import os
import sys
from os.path import join
from scipy import seterr

# let's test if the eqrm_code module is accessable

try:
    from eqrm_code import util
except ImportError:
    print "Python cannot import eqrm_code module."
    print "Check you have followed all steps of its installation."
    print "os.environ['PYTHONPATH']", os.environ['PYTHONPATH']
    import sys; sys.exit(1)

from eqrm_code.ANUGA_utilities import log

log.console_logging_level = log.ERROR
log.file_logging_level = log.ERROR
log.default_to_console = False
log.debug('Starting up the log file, so warnings are suppressed.')

#List files that should be excluded from the testing process.
#E.g. if they are known to fail and under development

EXCLUDE_FILES = []

if sys.platform == 'win32':
    EXCLUDE_FILES.append('test_event_set_npy.py')

#exclude_files = ['test_check_scenarios.py',
 #                'test_eqrm_audit_wrapper.py'] #['test_exceedance_curves.py']
# Removing test_sparse.py and test_cg_solve.py since they want to compile.

EXCLUDE_DIRS = ['.svn', 'plotting']

def get_test_files(path):   
    """
    Args:
      path: The directory to look for files
    Return:
      test_files: The names of all the test files (test_*.py) in path
        and its subdirectories.
      subdirectories: All subdirectories in path, except EXCLUDE_DIRS,
        as absolute paths.
    """
    try:
        files = os.listdir(path)
    except:
        files = []
    files.append(path)
    
    #Check sub directories
    test_files = []
    
    #Exclude dirs
    files = [x for x in files if x not in EXCLUDE_DIRS]
    subdirectories = []
    for file in files:
        absolute_filename = path + os.sep + file
        if os.path.isdir(absolute_filename):
            subdirectories.append(absolute_filename)
            #print  file + ',', 
            more_test_files, more_subdirectories = get_test_files(
                absolute_filename)
            test_files += more_test_files
            subdirectories += more_subdirectories
        elif file.startswith('test_') and file.endswith('.py'):
            test_files.append(file)
        else:
            pass
    return test_files, subdirectories



def regressionTest(path=None):    
    """
    Args:
      path: The directory to look for files.
        Assumed to be eqrm_code.
    Return:
      suite: The test suit to use with the unit tests
      moduleNames: The names of all the modules.  This
        can be used to import all the modules. Used
        in do_coverage.
    """
    
    if path is None:
        path = util.determine_eqrm_path()
        
    print
    if False: # I never really looked at this info
        print "The following directories will be skipped over;"
        for dir in EXCLUDE_DIRS:
            print dir, 
            print "\n"
    
    #print 'Recursing into;'
    test_files, subdirectories = get_test_files(path)
    files = [x for x in test_files if not x == 'test_all.py']
    print 'Testing path %s:' %path
    if False: # I never really looked at this info
        print
        print 'Files tested;'
        #print_files = []
        for file in files:
            #print_files += file + ' '
            print file + ',',
        print
    print
    if globals().has_key('EXCLUDE_FILES'):
        for file in EXCLUDE_FILES:
            print 'WARNING: File '+ file + ' to be excluded from testing'
            try:    
                files.remove(file)
            except ValueError, e:
                msg = 'File "%s" was not found in test suite.\n' %file
                msg += 'Original error is "%s"\n' %e
                msg += 'Perhaps it should be removed from exclude list?' 
                raise Exception, msg

    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)
    #print "moduleNames", moduleNames
    # Note, if there are duplicate file names, from different directories
    # only one of them will be used.
    # Add directorys to the sys. path, 
    # so the load works.
    for file in subdirectories:
        sys.path.append(file)
    sys.path.append(path)
    modules = map(__import__, moduleNames)
    #sys.path.remove(path)
    # Fix up the system path
    for file in subdirectories:
        sys.path.remove(file)
    load = unittest.defaultTestLoader.loadTestsFromModule
    testCaseClasses = map(load, modules)
    return unittest.TestSuite(testCaseClasses), moduleNames

def main(path=None):
    """
    Test that all the unit tests are passing.
    Args:
      path: The python_eqrm directory
    """

    # issue warning if DISPLAY variable not defined.
    # individual tests check this and return OK if display wrong.
    import sys
    if sys.platform != 'win32':
        try:
            display = os.environ['DISPLAY']
        except KeyError:
            print("\nWARNING: The plotting test suites will not be run since "
                  "the X environment is not set up.\n"
                  "         You must do 'ssh -X <machine>' to run these tests.")

    suite, moduleNames = regressionTest(path=path)
    runner = unittest.TextTestRunner() # verbosity=2
    test_result = runner.run(suite)
    
    # moduleNames is used for do_coverage
    # test_result is used in distribution.py
    return moduleNames, test_result



if __name__ == '__main__':
    """
    Note, the parameter is currently obsolete
    The eqrm_code directory that will be tested can be passed in as
    a parameter.  This is usefull to test one sandpit from another
    sandpit.  Used in distribution.py
    """
    from os import access, F_OK
    import sys
    
    seterr(all='warn')

    if len(sys.argv) > 1 and access(sys.argv[1],F_OK):
        path = sys.argv[1]
        path = None
    else:
        path = None
    _, test_result = main(path=path)
    try:
        c_errors_failures = len(test_result.errors) + len(test_result.failures)
    except:
        print "WARNING TEST RESULTS UNKNOWN"
        c_errors_failures = 1
    sys.exit(c_errors_failures) 

