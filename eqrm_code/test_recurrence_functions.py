import os
import sys

import unittest

from scipy import exp, log, array, sum, allclose, r_


from eqrm_code.event_set import Event_Set
from eqrm_code.source_model import Source_Model, Source_Zone_Polygon        
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
        bins = make_bins(min_magnitude,max_magnitude,num_bins)
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
        prob_min_mag_cutoff = 4.0
        slip_rate_mm=2.0
        area_kms= float(30*10)
        
        b = 1.
        A_min= calc_A_min_from_slip_rate_GR(b,prob_min_mag_cutoff,
                                            max_magnitude,
                                            slip_rate_mm,area_kms)
        self.assert_(allclose(A_min,0.225843709057))

    def test_calc_A_min_from_slip_rate_Characteristic(self):
        max_magnitude = 7.0
        prob_min_mag_cutoff = 4.0
        slip_rate_mm=2.0
        area_kms= float(30*10)
        
        b = 1.
        A_min= calc_A_min_from_slip_rate_Characteristic(b,prob_min_mag_cutoff,
                                            max_magnitude,
                                            slip_rate_mm,area_kms)
        self.assert_(allclose(A_min,0.0253104984335))

    def test_calc_activities_from_slip_rate_Characteristic(self):
        max_magnitude = 7.0
        prob_min_mag_cutoff = 4.0
        slip_rate_mm=2.0
        area_kms= float(30*10)
        prob_number_of_mag_sample_bins=10
        b = 1.
        bin_centroids = make_bins(prob_min_mag_cutoff,max_magnitude,prob_number_of_mag_sample_bins)
        event_bins=r_[0:10]
        event_bins=sorted(event_bins)
    
        A_minCharacteristic= calc_A_min_from_slip_rate_Characteristic(b,prob_min_mag_cutoff,
                                            max_magnitude,
                                            slip_rate_mm,area_kms)
        
        pdfs= calc_activities_from_slip_rate_Characteristic(bin_centroids, b, 
                                                              prob_min_mag_cutoff, 
                                                              max_magnitude)
        
        event_activity_source = array(
                [(A_minCharacteristic*pdfs[z]/(sum(where(
                event_bins == z, 1,0)))) for z in event_bins])
        
        self.assert_(allclose(event_activity_source,[1.21328345e-02,   
                                                     6.08082174e-03,   
                                                     3.04763023e-03,   
                                                     1.52743336e-03,
                                                     7.65530102e-04,   
                                                     3.83673914e-04,   
                                                     1.92292468e-04,   
                                                     9.63745299e-05,
                                                     5.41953808e-04,   
                                                     5.41953808e-04]))
       
    # This test assumes events can be generated
    # outside of a source model
    # this is not the case right now
    def out_test_calc_event_activity(self):
        
        # Warning this test does not test all of the paths of
        # calc_event_activity.
        # Additionally, it is based on looking at the code and
        # seeing what it does, rather than based on an understanding
        # of what the function should really do.
        # additionally the weighting is not tested.

        l=116.6
        r=116.8
        hi=-31.6
        lo=-31.8
        square1 = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,l)]
        
        l=116.6
        r=116.8
        hi=-31.4
        lo=-31.6
        square2 = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,l)]

        min_magnitude = 0.9
        max_magnitude = 2.0
        prob_min_mag_cutoff = 1.0
        Lambda_Min = 1.
        b = 1.

        prob_number_of_mag_sample_bins = 10

        # Dependent, but hard coded.
        len_event_ind = 26
        event_bins =[0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5,
                     5, 5, 6, 6, 6, 7, 7, 8, 8, 8, 9, 9]

    
        szp1 = Source_Zone_Polygon(square1,[],
                                   min_magnitude,max_magnitude,
                                   prob_min_mag_cutoff,
                                   Lambda_Min,b,
                                   prob_number_of_mag_sample_bins)
        szp2 = Source_Zone_Polygon(square2,[],
                                   min_magnitude,max_magnitude,
                                   prob_min_mag_cutoff,
                                   Lambda_Min,b,
                                   prob_number_of_mag_sample_bins)
        sm = Source_Model([szp1], 'Is this used?')
        
        # The weight attribute is added to the instance in a real simulation
        # in event_set.calculate_recurrence
        weight = [1.0]
        sources = [sm]

        # Where is source_zone_id made in real examples?
        # It seems to be based on the source zone polygon..
        # but you can instanciate Event_set with no knowledge of
        # the source Model.
        # -31.801 means the last point are outside the polygon
        
        event_set = Event_Set.create(\
            rupture_centroid_lat=r_[-31.6:-31.801:30j],
            rupture_centroid_lon=r_[116.6:116.8:30j],
            Mw=r_[min_magnitude:max_magnitude-0.000001:30j],
            fault_width=r_[1.:2.:30j],
            depth=r_[1.:2.:30j],
            dip=r_[1.:2.:30j],
            azimuth=r_[1.:2.:30j]
            #source_zone_id=r_[0.0:0.0:30j]
            )
        event_set.source_zone_id = r_[0.0:0.0:30j]
        #print "len(event_set)", len(event_set)
        
        event_activity_matrix = calc_event_activity(event_set, sources,
                                            prob_number_of_mag_sample_bins,
                                            weight,
                                            )
        #print "len(new_event_set)", len(new_event_set)
        #print "event_set", event_set.Mw[3:29]
        #print "new_event_set", new_event_set.Mw
        self.assert_(allclose(event_set.Mw[3:29], new_event_set.Mw))
        self.assert_(allclose(event_set.rupture_centroid_lat[3:29],
                              new_event_set.rupture_centroid_lat))
        self.assert_(allclose(event_set.rupture_centroid_lat[3:29],
                              new_event_set.rupture_centroid_lat))
        #print " new_event_set.event_activity", new_event_set.event_activity

        A_mlow=grscale(b,max_magnitude,prob_min_mag_cutoff,min_magnitude)*Lambda_Min
        #print "A_mlow - test",  A_mlow
        #print "event_bins", event_bins
        bins = make_bins(prob_min_mag_cutoff,max_magnitude,prob_number_of_mag_sample_bins)
        grape=m2grpdfb(b,bins,prob_min_mag_cutoff,max_magnitude)
        #print "grape",grape
        #print "bins", bins
        event_activity=(prob_number_of_mag_sample_bins*A_mlow
                                *grape[event_bins]/len_event_ind)
        #print "event_activity - test", event_activity
        self.assert_(allclose(event_activity,
                              new_event_set.event_activity))

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Recurrence_functions,'test')
    #suite = unittest.makeSuite(Test_Recurrence_functions,'test_calc_event_activity')
    runner = unittest.TextTestRunner()
    runner.run(suite)
