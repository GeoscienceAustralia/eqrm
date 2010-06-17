"""
Work out the coverage of the unit tests.
This has nothing to do with earthquakes.
It is a hacky software tool script.  It may not work with your system.

It does not work in linux. - No coverage module


NOTES DSG
Tried to move this into sw_dev_tools, but got stuck on  the map import line.
"""


# Note, the coverage package does not work in Linux
import coverage

coverage.erase()
coverage.start()

import test_all

# run the unit tests and return a list of the unit test file names
module_names, _ = test_all.main()
coverage.stop()

# Remove the 'test' part of the unit test file names
print "module_names", module_names
module_names = [x[5:] for x in module_names]
print "module_names", module_names
removes = ['latrobe_69_example', 'cadell_damage']
for ditch in removes:
    try:
        module_names.remove(ditch)
    except:
        pass
    
modules = map(__import__, module_names)

coverage.report(modules)
###coverage.annotate(modules, directory='C:\dump')
