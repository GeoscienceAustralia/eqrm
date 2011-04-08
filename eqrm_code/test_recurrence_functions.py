import os
import sys

import unittest

from scipy import exp, log, array, sum, allclose, r_


from eqrm_code.event_set import Event_Set
from eqrm_code.source_model import Source_Model, Source_Zone        
from eqrm_code.recurrence_functions import *

class Test_Recurrence_functions(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_m2grpdfb(self):
        

        m = array([4,6])
        b = 1./4.
        m0 = 2.
        mmax = 10.
    
        beta = b *log(10)
        fm_temp = beta*exp(-1*beta*(m-m0))/(1-exp(-1*beta*(mmax-m0)))

        s = 0
        for i in range(len(fm_temp)):
            s+=fm_temp[i]
            pdf=fm_temp/s

        fmcalc = m2grpdfb(b,m,m0,mmax)
        self.assert_(allclose(pdf,fmcalc))
    
    def test_make_bins(self):
        min_magnitude = 0
        max_magnitude = 6
        num_bins = 3
        bins = make_bins(min_magnitude, max_magnitude, num_bins,
                         'bounded_gutenberg_richter')
        
        #print "bins", bins
        self.assert_(allclose(array([1.,3.,5.]),bins))
        
    def test_grscale(self):
        m = 3.
        b = 1.
        m0 = 1.
        mmax = 2.
        # gives a grscale of -.1
        
        beta = b *log(10)
        
        tmp = exp(-1*beta*(mmax-m0))
        test = (exp(-1*beta*(m-m0))-tmp)/(1-tmp)
        self.assertEqual(test, grscale(b,mmax,m,m0))     


    def test_calc_A_min_from_slip_rate_GR(self):
        max_magnitude = 7.0
        mMin = 4.0
        slip_rate_mm=2.0
        area_kms= float(30*10)
        
        b = 1.
        A_min= calc_A_min_from_slip_rate_GR(b, mMin,
                                            max_magnitude,
                                            slip_rate_mm, area_kms)
        self.assert_(allclose(A_min,0.225843709057))
        
    def test_make_bins2(self):
        max_magnitude = 7.0
        min_magnitude = 4.0
        num_of_mag_sample_bins = 4
        magnitudes = array([5,5.25,5.5,5.75,6,6.25,6.5,6.75,7])
        mag_bin_centroids = make_bins(min_magnitude, max_magnitude,
                                      num_of_mag_sample_bins,
                                      'characteristic')
        event_bins = assign_event_bins(magnitudes, min_magnitude, 
                                      max_magnitude, num_of_mag_sample_bins,
              recurrence_model_dist = 'characteristic')
#        print 'event_bins ',event_bins
        
    def test_calc_A_min_from_slip_rate_Characteristic(self):
        max_magnitude = 7.0
        mMin = 4.0
        slip_rate_mm = 2.0
        area_kms = float(30*10)        
        b = 1.
        A_min = calc_A_min_from_slip_rate_Characteristic(b, 
                                                         mMin,
                                                         max_magnitude,
                                                         slip_rate_mm,
                                                         area_kms)
        self.assert_(allclose(A_min,0.0253104984335))

    def test_calc_activities_Characteristic(self):
        max_magnitude = 7.0
        min_magnitude = 4.0
        slip_rate_mm = 2.0
        area_kms = float(30*10)
        prob_number_of_mag_sample_bins = 10
        b = 1.
        bin_centroids = make_bins(min_magnitude, max_magnitude,
                                  prob_number_of_mag_sample_bins,
                                  'characteristic')
        event_bins = r_[0:10]
        event_bins = sorted(event_bins)
    
        A_minCharacteristic = calc_A_min_from_slip_rate_Characteristic(
            b, min_magnitude,
            max_magnitude,
            slip_rate_mm, area_kms)
        
        pdfs = calc_activities_Characteristic(bin_centroids, b, 
                                              min_magnitude, 
                                              max_magnitude,
                                              prob_number_of_mag_sample_bins)
        
        event_activity_source = array(
                [(A_minCharacteristic*pdfs[z]/(sum(where(
                event_bins == z, 1,0)))) for z in event_bins])
        
        self.assert_(allclose(event_activity_source,[1.07157089e-02,
                                                     6.02588592e-03,
                                                     3.38860467e-03,
                                                     1.90555244e-03,
                                                     1.07157089e-03,
                                                     6.02588592e-04,
                                                     3.38860467e-04,
                                                     1.90555244e-04,
                                                     1.07157089e-04,
                                                     6.02588592e-05]))

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Recurrence_functions,'test')
    #suite = unittest.makeSuite(Test_Recurrence_functions,'test_calc_event_activity')
    runner = unittest.TextTestRunner()
    runner.run(suite)
