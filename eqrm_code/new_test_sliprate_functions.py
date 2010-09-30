import os
import sys

import unittest

from scipy import exp, log, array, sum, allclose, r_


from eqrm_code.event_set import Event_Set
from eqrm_code.source_model import Source_Model, Source_Zone_Polygon        
from eqrm_code.recurrence_functions import *

class Test_Sliprate_functions(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    
    def test_sliprate_functions(self):
        max_magnitude = 6.0
        prob_min_mag_cutoff = 1.0
        slip_rate=0.2
        area= float(3*10**12)
        prob_number_of_mag_sample_bins=10
        b = 1.
        bin_centroids = make_bins(prob_min_mag_cutoff,max_magnitude,prob_number_of_mag_sample_bins)
        event_bins=array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        
        print "Params: \n \
        max_magnitude = ",max_magnitude, "\n \
        prob_min_mag_cutoff = ",prob_min_mag_cutoff," \n \
        slip_rate=  ",slip_rate, "\n \
        area= ",area," \n \
        prob_number_of_mag_sample_bins= ",prob_number_of_mag_sample_bins," \n \
        b = ",b
        
        A_min= calc_A_min_from_slip_rate_GR(1,4,7,slip_rate,area)
        print "\nA_min from slip rate GR: ", A_min 
        A_minCharacteristic= calc_A_min_from_slip_rate_Characteristic(1,4,7,slip_rate,area)
        print "\nA_min from -slip rate Characteristic: ", A_minCharacteristic 
        
        pdfs= calc_activities_from_slip_rate_Characteristic(bin_centroids, b, 
                                                              prob_min_mag_cutoff, 
                                                              max_magnitude)
        print "\npdfs  from -slip rate Characteristic: ", pdfs
         
        event_activity_source = array(
                [(A_minCharacteristic*pdfs[z]/(sum(where(
                event_bins == z, 1,0)))) for z in event_bins])
        print "\nevent activity: ", event_activity_source
        print "\nsum event activity: ", sum(event_activity_source)
        
    
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Sliprate_functions,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
