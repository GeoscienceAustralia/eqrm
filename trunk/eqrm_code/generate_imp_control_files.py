#!/usr/bin/env python

"""
Generate the eqrm control file that is used by the implementation tests.

"""
import os
import sys
import unittest
import tempfile

from xml.etree import ElementTree as ET #, getiterator

from eqrm_code.eqrm_filesystem import scenario_input_path



# design
 # read in the general input file
#  modify it based on the ground motion models needed


# read in the general input file
filename = os.path.join(scenario_input_path, 'newc_source_polygon.xml')
file = open(filename, "r")
tree = ET.parse(file)
elem = tree.getroot()
file.close()

filename_out = os.path.join(scenario_input_path, 'old_source_polygon.xml')
tree.write(filename_out)

# modify it based on the ground motion models needed
# write many input files.
