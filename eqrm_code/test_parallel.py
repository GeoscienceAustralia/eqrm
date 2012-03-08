
import os
import sys
import unittest

from eqrm_code.parallel import *

from eqrm_code import perf

class Test_Parallel(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @perf.benchmark
    def test_parallel_off(self):
        
        sites_len = 10
        sites = range(sites_len)
        parra = Parallel(is_parallel=False)
        parra.calc_lo_hi(sites_len)
        lo = parra.lo 
        hi = parra.hi
        #print "lo", lo
        #print "hi", hi
        self.assert_ (lo == 0) 
        self.assert_ (hi == sites_len) 
        
    @perf.benchmark
    def test_parallel_on(self):
        # This test can be run with
        # mpirun -hostfile ~/.machines.cyclone -c 2 python parallel_spike.py
        # if there is a path problem, try adding -x PYTHONPATH
        
        try:
            import pypar
        except ImportError:
            # can't do this test
            return
                
        sites_len = 10
        sites = range(sites_len)
        parra = Parallel(is_parallel=True)
        parra.calc_lo_hi(sites_len)
        lo = parra.lo 
        hi = parra.hi
        #print "lo", lo
        #print "hi", hi
        if parra.size == 1:
            self.assert_ (lo == 0) 
            self.assert_ (hi == sites_len)
        elif parra.size == 2:
            if parra.rank == 0:
                self.assert_ (lo == 0) 
                self.assert_ (hi == 5)
            else:
                self.assert_ (lo == 5) 
                self.assert_ (hi == 10)
    
    @perf.benchmark
    def test_parallel_on(self):
        # This test can be run with
        # mpirun -hostfile ~/.machines.cyclone -c 2 python parallel_spike.py
        # if there is a path problem, try adding -x PYTHONPATH
        
        try:
            import pypar
        except ImportError:
            # can't do this test
            return
                
        sites_len = 1
        sites = range(sites_len)
        parra = Parallel(is_parallel=True)
        parra.calc_lo_hi(sites_len)
        lo = parra.lo 
        hi = parra.hi
        #print "lo", lo
        #print "hi", hi
        if parra.size == 1:
            self.assert_ (lo == 0) 
            self.assert_ (hi == sites_len)
        elif parra.size == 2:
            if parra.rank == 0:
                self.assert_ (lo == 0) 
                self.assert_ (hi == 1)
            else:
                self.assert_ (lo == 1) 
                self.assert_ (hi == 1)
             
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Parallel,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
