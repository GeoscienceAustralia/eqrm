"""
"""

import unittest
import tempfile
from os import sep, path

from scipy import array, allclose, ones, e
from scipy.stats import norm

from eqrm_code.fatalities import *

from eqrm_code import perf

class Test_fatalities(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @perf.benchmark
    def test_forecast_fatality(self):
        # This test is bad, since I'm writing it based on the code.
        
        MMI = array([1,2,4., 10., 11.])
        population = ones(MMI.shape)       
        beta = 1.0
        theta = 10.0 * e**-2.0
        fatality = forecast_fatality(MMI, population, beta, theta)
        expected = array([0, 0, 0, norm.cdf(2.0), norm.cdf(2.0)])
        #print "expected", expected
        #print "fatality", fatality
        self.failUnless(allclose(expected, fatality))
        
        MMI = array([5.])
        pop_scaler = 5.0
        population = ones(MMI.shape) * pop_scaler      
        beta = 1.0
        theta = 5.0 * e**-2.0
        fatality = forecast_fatality(MMI, population, beta, theta)
        expected = array([pop_scaler * 1.0/beta*norm.cdf(2.0)])
        #print "expected", expected
        #print "fatality", fatality
        self.failUnless(allclose(expected, fatality))
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_fatalities,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
