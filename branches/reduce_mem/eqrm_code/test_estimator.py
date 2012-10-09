
import unittest
import numpy
from eqrm_code.estimator import *

class Test_estimator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_estimator(self):
        
        events = 2
        atten_periods = 3
        return_periods = 5
        parallel_size = 7
        spawning = 11
        gmm_dimensions = 13
        rec_mod = 17
        save_total_financial_loss = True
        save_building_loss = True
        save_contents_loss = True
        save_hazard_map = True
        save_motion = True
        use_amplification = True
        loop_sites = 19
        item_size = 23

        results = estimate_mem(events, 
                               atten_periods, 
                               return_periods,
                               parallel_size,
                               spawning,
                               gmm_dimensions,
                               rec_mod,
                               save_total_financial_loss,
                               save_building_loss,
                               save_contents_loss,
                               save_hazard_map,
                               save_motion,
                               use_amplification,
                               loop_sites,
                               item_size)
        #print results
        # don't test this yet.


    def test_memory(self):
        mem_array = numpy.zeros([1000, 1000], dtype=float)
        self.assertEqual(mem_array.nbytes, 1000*1000*8)



################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_estimator, 'test')
    runner = unittest.TextTestRunner() #verbosity=2) #verbosity=2
    runner.run(suite)
