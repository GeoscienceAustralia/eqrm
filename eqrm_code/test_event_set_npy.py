"""
Run all Event_Set tests with numpy file storage method for arrays
"""
import tempfile, shutil
import unittest
from scipy import seterr, allclose, array

import eqrm_code.test_event_set as test_event_set
from eqrm_code import file_store
from eqrm_code.event_set import Event_Set, Event_Activity

from eqrm_code import perf

class Test_Event_Set_Npy(test_event_set.Test_Event_Set):
    
    def setUp(self):
        # Set up event_set module globals for this test
        file_store.SAVE_METHOD = 'npy'
        
        # Create a temporary directory for the data files
        self.data_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Remove the temporary data directory
        shutil.rmtree(self.data_dir)
        
    @perf.benchmark
    def test_event_set_load_save(self):
        # Create a dummy event set
        event_set1 = test_event_set.event_from_csv_long()
        
        # Save it to the temporary dir
        event_set1.save(self.data_dir)
        
        # Load the second event set from file
        event_set2 = Event_Set.load(self.data_dir)

        # Checking that event_set1.depth is not the same object
        # as event_set2.depth (as opposed to whether they are numerically
        # the same). 
        assert event_set1.depth is not event_set2.depth
        assert event_set1.rupture_centroid_x is not event_set2.rupture_centroid_x
        
        # Testing that the values were saved with good precision
        assert allclose(event_set1.depth,
                        event_set2.depth)
        assert allclose(event_set1.rupture_centroid_lat,
                        event_set2.rupture_centroid_lat)
        assert allclose(event_set1.rupture_centroid_lon,
                        event_set2.rupture_centroid_lon)
        assert allclose(event_set1.azimuth,
                        event_set2.azimuth)
        assert allclose(event_set1.dip,
                        event_set2.dip)
        assert allclose(event_set1.trace_start_lat,
                        event_set2.trace_start_lat,
                        atol=0.01)
        assert allclose(event_set1.trace_start_lon,
                        event_set2.trace_start_lon,
                        atol=0.01) 
        assert allclose(event_set1.dip,
                        event_set2.dip)

    @perf.benchmark
    def test_event_activity_load_save(self):
        # Event_Activity object based on Test_Event_Set.test_Event_Activity
        num_events = 3
        event_indexes = array([0,2])
        event_activities = array([[10, 20], [30, 40]])
        
        # Create a dummy event activity object
        ea1 = Event_Activity(num_events)
        ea1.set_event_activity(event_activities, event_indexes)
        
        # Save it to the temporary dir
        ea1.save(self.data_dir)
        
        # Load the second event activity object from file 
        ea2 = Event_Activity.load(num_events, self.data_dir)
        
        assert allclose(ea1.event_activity, ea2.event_activity)
        

if __name__ == "__main__":
    seterr(all='warn')
    suite = unittest.makeSuite(Test_Event_Set_Npy,'test')
    #suite = unittest.makeSuite(Test_Event_Set,'test_generate_synthetic_events_horspool')    
    runner = unittest.TextTestRunner() #verbosity=2
    runner.run(suite)
