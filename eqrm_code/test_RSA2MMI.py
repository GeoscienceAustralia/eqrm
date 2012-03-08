"""
"""

import unittest
import tempfile
from os import sep, path

from scipy import array, allclose

from eqrm_code.RSA2MMI import *
from eqrm_code import perf

class Test_RSA2MMI(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @perf.benchmark
    def test_RSA2MMI(self):
        # This test is bad, since I'm writing it based on the code.
        data = []   
        data.append(1.0/980.)
        # gives  C1 + C2*(log10(1.0))
        # = C1 + C2*0.
        # = C1 
        
        data.append(100.0/980.)
        # gives  C3 + C4*(log10(10.0))
        # = C3 + C4*2.
        
        data.append(10000000000000.0)
        # hits the max limit
        
        # the min limit can not be hit
        
        period = 1.0
        mmi = rsa2mmi_array(data, period)
        expected = array([3.23, 0.57 + 2*2.95, 10])
        #print "expected", expected
        #print "mmi", mmi
        self.failUnless(allclose(expected, mmi))
        
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_RSA2MMI,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
