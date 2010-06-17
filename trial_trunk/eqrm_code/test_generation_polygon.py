import os
import sys
import unittest
from os.path import join, split

from eqrm_code.generation_polygon import *

class Test_Generation_polygon(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_load_static_file(self):

        # Let's work-out the eqrm dir
        eqrm_dir, tail = split( __file__)
        # Since this is the eqrn_code dir and we want the python_eqrm dir
        eqrm_dir = join(eqrm_dir, "..", "test_resources")
        filename = join(eqrm_dir, "sample_event.xml")

        return
    # need to work on.
        generation_polygons,magnitude_type = polygons_from_xml(
            filename=filename,
            fault_width= 13
            )
        
    

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Generation_polygon,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
