"""

Title: EQRM imp_unit_coverage - unit and implementation test coverage.

Author: Duncan Gray (Duncan.Gray@ga.gov.au), etc

CreationDate: 2007

Description:

Writes annotated code files which shows which statements have been
executed by the unit tests and the implementation tests.  These files
are in the test-coverage directory.

The first column of each file shows if statements were executed in the
implementation tests.  The second column is for the unit tests.  >
means the line was executed.  ! means it was not.

So;
!>         sample_values=[]
means this line was not executed in the implementation tests,
but it was executed in the unit tests.

This script determines the coverage of the unit tests and the
implementation tests.  Information about both of these tests is sent
to screen. 

    NOTE: This code only works in Windows.
    It also needs coverage.py installed.
    
Constraints: See GPL license in the main directory

Version: 1.0 ($Revision: 974 $)
ModifiedBy:
    $Author: dgray $
    $Date: 2009-06-12 15:26:18 +1000 (Fri, 12 Jun 2009) $

"""

#Subversion keywords:
#
#$LastChangedDate: 2009-06-12 15:26:18 +1000 (Fri, 12 Jun 2009) $
#$LastChangedRevision: 974 $
#$LastChangedBy: dgray $

import coverage
import os, sys
from os import sep, listdir

import tempfile

coverage.erase()
coverage.start()

import eqrm_code.test_all

# run the unit tests and return a list of the unit test file names
os.chdir('eqrm_code')
module_names = eqrm_code.test_all.main()
coverage.stop()

# Remove the 'test' part of the unit test file names
print "module_names", module_names
removes = ['test_cadell_damage']
for ditch in removes:
    module_names.remove(ditch)
module_names = [ x[5:] for x in module_names]
# This is a hack, since all the files have to be in eqrm_code
code_dir = os.getcwd()
sys.path.append(code_dir)
modules = map(__import__, module_names)
sys.path.remove(code_dir)
coverage.report(modules)
unit_dir = tempfile.mkdtemp()
coverage.annotate(modules, directory=unit_dir)

os.chdir('..')

print "Getting differences in coverage? ",
print "The run with less coverage might use compiled code. Do a clean_all.py."
print "UNIT TEST COVERAGE FINISHED.  DOING IMPLEMENTATION TESTS"
#import sys; sys.exit()

# Run the implementation tests
coverage.erase()
coverage.start()

# This import causes problems.  Import this and it imports analysis
from eqrm_code.check_scenarios import run_scenarios

# run the imp tests and return a list of the unit test file names
IMP_DIR = '.'+sep+'implementation_tests'+sep
SCENARIO_DIR = IMP_DIR+'test'+sep
run_scenarios() #SCENARIO_DIR) # testing
coverage.stop()

# Remove the 'test' part of the unit test file names
#modules = map(__import__, module_names)

coverage.report(modules)
imp_dir = tempfile.mkdtemp()
coverage.annotate(modules, directory=imp_dir)

# delete the current combined annotate coverage results

# Combine the two annotated coverage files
out_dir = 'test_coverage'
files = listdir(imp_dir)
for file in files:
    imp = open(imp_dir+sep+file,'r')
    unit = open(unit_dir+sep+file,'r')
    out = open(out_dir+sep+file,'w')
    for imp_line, unit_line in map(None,imp,unit):
        out.write(str(imp_line[0])+str(unit_line))
    imp.close()
    unit.close()
    out.close()
    os.remove(imp_dir+sep+file)
    os.remove(unit_dir+sep+file)
os.rmdir(imp_dir)
os.rmdir(unit_dir)
