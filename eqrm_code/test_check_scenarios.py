"""
"""

# FIXME This test imports check_scenarios, which imports analysis
# which imports everything.  

import unittest
import tempfile
from os import sep, path

from scipy import array, allclose

from eqrm_code.check_scenarios import *

class Test_check_scenarios(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_how_it_works(self):
        
        try:
            import pypar
        except ImportError:
            rank = 0
        else:
            rank = pypar.rank

        # This test can not be run in parallel.
        if rank == 0:
            timings = {'ben':9.79, 'carl':9.92}
            scenario = Scenario_times(timings, timing_dir='.') #, host='1988')
            scenario.delete()
            results, fail_dic = scenario.compare_times(verbose=False)
            self.assert_ (results is None)
            self.assert_ (fail_dic is None)
            results, fail_dic = scenario.compare_times(verbose=False)
            self.assert_ (fail_dic == {})
            self.assert_ (results == '..')
            
            timings = {'ben':10.00, 'carl':12.0, 'duncan':13.9}
            scenario2 = Scenario_times(timings, timing_dir='.') #, host='1988')
            
            # this will trigger writing the current file
            results, fail_dic = scenario2.compare_times(verbose=False)
            self.assert_ (results == '.F')
            self.assert_ (len(fail_dic) == 1)
            standard = array([9.92, 12.0])
            results = array(fail_dic['carl'])
            self.assert_ (allclose(results, standard))
            standard_dic = scenario.read_standard(file_string=CURRENT_STRING)
            self.assert_ (standard_dic.has_key('duncan'))
            
            scenario.delete(file_string=CURRENT_STRING)
            scenario.delete()
            scenario2.delete()
        else:
            pass
            #print "Test not running"
    
    def test_check_dir_names(self):    
        dir_list = ['./implementation_tests/current/TS_haz38/', 
                    './implementation_tests/current/TS_haz39/', 
                    './implementation_tests/current/TS_risk63/']
        standard_dir = './implementation_tests/current'
        results = check_dir_names(dir_list, standard_dir)
        actual = ['TS_haz38', 'TS_haz39', 'TS_risk63']
        self.assertEqual(results, actual)
        
    def test_check_dir_namesII(self):    
        dir_list = ['./implementation_tests/current/TS_haz38', 
                    './implementation_tests/current/TS_haz39', 
                    './implementation_tests/current/TS_risk63']
        standard_dir = './implementation_tests/current'
        results = check_dir_names(dir_list, standard_dir)
        actual = ['TS_haz38', 'TS_haz39', 'TS_risk63']
        self.assertEqual(results, actual)
        
    def test_check_dir_names3(self):    
        dir_list = ['./foo/TS_haz38', 
                    './implementation_tests/current/TS_haz39', 
                    './implementation_tests/current/TS_risk63']
        standard_dir = './implementation_tests/current'
        self.assertRaises(BadDirectoryStructure,
                          check_dir_names,dir_list, standard_dir)
        #results = check_dir_names(dir_list, standard_dir)
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_check_scenarios,'test')
    #suite = unittest.makeSuite(Test_check_scenarios,'test_check_dir_names3')
    runner = unittest.TextTestRunner()
    runner.run(suite)
