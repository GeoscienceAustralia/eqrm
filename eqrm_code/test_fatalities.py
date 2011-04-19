"""
"""

import unittest
import tempfile
from os import sep, path

from scipy import array, allclose

from eqrm_code.fatalities import *

class Test_fatalities(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_forecast_fatality(self):
        # This test is bad, since I'm writing it based on the code.
        
        MMI = [1,2,4.,]
        population = ones(MMI)
        fatality = forecast_fatality(MMI, population, beta, theta)
        expected = array([0, 0, 0, ])
        #print "expected", expected
        self.failUnless(allclose(expected, fatality))
        
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_fatalities,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
