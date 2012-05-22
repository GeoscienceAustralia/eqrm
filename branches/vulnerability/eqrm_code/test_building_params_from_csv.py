import os
import sys
import unittest

#from scipy import allclose,array,info

#from csv_interface import Csv_interface
from eqrm_code.building_params_from_csv import *

class Test_Building_Params(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_building_parameters_values_FCB(self):
        pass
    
        #FIXME DSG-EQRM take out the assert and do this elsewhere, as a test
        #from scipy import allclose
        #assert allclose((structure_ratio+nsd_d_ratio+nsd_a_ratio),1.0)

        
    def test_building_params_from_csv_workshop_3(self):
        pass
        # Let's not test this stuff.
        # It's reading in files and the way it's done is not ideal.
        # Have the tests at a higher level - test_structure.
        #
        
    def investigate_building_params_from_csv_workshop_3(self):
        bp=building_params_from_csv('building_parameters_workshop_3')
        print "bp", bp
        for key, value in bp.iteritems():
            print "key", key
            try:
                print " value.shape", value.shape
            except:
                print " len(value)", len(value)
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Building_Params,'investigate')
    runner = unittest.TextTestRunner()
    runner.run(suite)
