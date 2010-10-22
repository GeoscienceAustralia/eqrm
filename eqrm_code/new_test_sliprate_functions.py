import os
import sys

import unittest

from scipy import exp, log, array, sum, allclose, r_, random, cumsum
import matplotlib.pylab as plt
from numpy import arange,exp

from eqrm_code.event_set import Event_Set
from eqrm_code.source_model import Source_Model, Source_Zone        
from eqrm_code.recurrence_functions import *
from eqrm_code.conversions import *

class Test_Sliprate_functions(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    
    def test_sliprate_functions(self):
        max_magnitude = 7.0
        prob_min_mag_cutoff = 4.0
        slip_rate_mm=2.0
        area_kms= float(30*10)
        prob_number_of_mag_sample_bins=200
        b = 1.
        bin_centroids = make_bins(prob_min_mag_cutoff,max_magnitude,
                                  prob_number_of_mag_sample_bins)
        event_bins=r_[0:prob_number_of_mag_sample_bins]
        event_bins=sorted(event_bins)
        (width,length)=Wells_and_Coppersmith_94("normal", bin_centroids, 15, 30)
        
        lon1=144
        lat1=(0,45,60,85)
        
        for i in range(4):
            print "azimuth of line from (", lat1[i],"," ,lon1,") to \
            (" ,lat1[i]+1,"," ,lon1+1,") =" , obsolete_calc_azimuth2(lat1[i], \
            lon1, lat1[i]+1, lon1+1)
        #print "azimuth 3: ",calc_azimuth3(lat1, lon1, lat2, lon2)
        
        print "Params: \n \
        max_magnitude = ",max_magnitude, "\n \
        prob_min_mag_cutoff = ",prob_min_mag_cutoff," \n \
        slip_rate_mm=  ",slip_rate_mm, "\n \
        area_kms= ",area_kms," \n \
        prob_number_of_mag_sample_bins= ",prob_number_of_mag_sample_bins," \n \
        b = ",b
        
        A_min= calc_A_min_from_slip_rate_GR(b,prob_min_mag_cutoff,
                                            max_magnitude,
                                            slip_rate_mm,area_kms)
        print "\nA_min from slip rate GR: ", A_min 
        A_minCharacteristic= calc_A_min_from_slip_rate_Characteristic(b,
                                                                      prob_min_mag_cutoff,
                                                                      max_magnitude,
                                                                      slip_rate_mm,
                                                                      area_kms)
        print "\nA_min from -slip rate Characteristic: ", A_minCharacteristic 
        print "\n bin centroids(magnitudes): ",bin_centroids
        pdfs= calc_activities_from_slip_rate_Characteristic(bin_centroids, b, 
                                                              prob_min_mag_cutoff, 
                                                              max_magnitude)
        #print "\npdfs  from -slip rate Characteristic: ", pdfs
        print "calc_A_min_from_slip_rate(b,mMin,mMax,slip_rate_mm,recurr_dist,\
                              lat1,lon1,lat2,lon2,depth_top,depth_bottom,dip ",\
                              (calc_A_min_from_slip_rate(b,prob_min_mag_cutoff,\
                                                         max_magnitude,slip_rate_mm,
                                                         'characteristic',
                                                        0,144.5,0,144.8,10,15,30))


        event_activity_source = array(
                [(A_minCharacteristic*pdfs[z]/(sum(where(
                event_bins == z, 1,0)))) for z in event_bins])
        #print "\nevent activity: ", event_activity_source
        print "\nsum event activity: ", sum(event_activity_source)
        
        t = arange(0.01, 20.0, 0.01)
        plt.figure()
        plt.semilogy(t, exp(-t/5.0))
        plt.title('Characteristic PDF')
        plt.xlabel('magnitude')
        plt.ylabel('probability')
        plt.plot(bin_centroids[0:-1],pdfs[0:-1])
        plt.ylim(0.00,0.04)
        plt.xlim(4,7)
        plt.savefig('pdf_characteristic.png')

        plt.figure()
        plt.semilogy(t, exp(-t/5.0))
        plt.title('Characteristic Event Activity')
        plt.xlabel('magnitude')
        plt.ylabel('events/year')
        plt.plot(bin_centroids[0:-1],event_activity_source[0:-1])
        plt.ylim(0.00,0.001)
        plt.xlim(4,7)
        plt.savefig('characteristic_event_activity.png')
        
        plt.figure()
        plt.semilogy(t, exp(-t/5.0))
        event_activity_source=event_activity_source[::-1]
        bin_centroids=bin_centroids[::-1]
        cumulative_event_activity= cumsum(event_activity_source)
        plt.title('Cumulative Characteristic Event Activity')
        plt.xlabel('magnitude')
        print " (max = " , max(cumulative_event_activity), ")"
        plt.ylabel('cumulative events/year')
        plt.plot(bin_centroids[0:-1],cumulative_event_activity[:-1])
        plt.ylim(0.00,0.04)
        plt.xlim(4,7)
        plt.savefig('Cumulative_chrctrstc_event_activity.png')
        

       
        

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Sliprate_functions,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
