"""
Run all Event_Set tests with numpy file storage method for arrays
"""
import unittest
from scipy import seterr

import eqrm_code.test_event_set as test_event_set
from eqrm_code import file_store

class Test_Event_Set_Npy(test_event_set.Test_Event_Set):
    
    def setUp(self):
        # Set up event_set module globals for this test
        file_store.SAVE_METHOD = 'npy'

if __name__ == "__main__":
    seterr(all='warn')
    suite = unittest.makeSuite(Test_Event_Set_Npy,'test')
    #suite = unittest.makeSuite(Test_Event_Set,'test_generate_synthetic_events_horspool')    
    runner = unittest.TextTestRunner() #verbosity=2
    runner.run(suite)
