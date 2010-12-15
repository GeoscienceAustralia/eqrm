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
    def obtest_calc_new_rupture_trace_lower_slab(self):
        (low_trace_lat_s, low_trace_lon_s, low_trace_lat_e,low_trace_lon_e) = \
        calc_new_rupture_trace_lower_slab(35, 140, -10.338979, 112.433555, 
                                          -8.60524, 105.822974, 
                                          58)
        print ("low_trace_lat_s, low_trace_lon_s, low_trace_lat_e,low_trace_lon_e")
        print "Calculated loweer trace ",low_trace_lat_s, low_trace_lon_s, \
        low_trace_lat_e,low_trace_lon_e
        print("Jono's lower trace -9.35599, 112.691361, -7.622251,106.080779")
        
        azimuth_top =azimuth_of_trace(-10.338979, 112.433555, 
                                          -8.60524, 105.822974)
        
        print ("azimuth of new top trace", azimuth_top)
        
        azimuth =azimuth_of_trace(low_trace_lat_s, low_trace_lon_s, 
                                  low_trace_lat_e,low_trace_lon_e)
        
        print ("azimuth of new calc trace", azimuth)
        
        azimuth =azimuth_of_trace(-9.35599, 112.691361, 
                                  -7.622251,106.080779)
        
        print ("azimuth of new jono trace", azimuth)
        
        dist_start_traces = calc_ll_dist(-10.338979, 112.433555, low_trace_lat_s,
                                          low_trace_lon_s)
        dist_end_traces = calc_ll_dist(-8.60524, 105.822974, low_trace_lat_e,
                                          low_trace_lon_e)
        
        print ("Dist between the trace start of the top and lower slab ", 
                dist_start_traces)
        print ("Dist between the trace end of the top and lower slab ", 
                dist_end_traces)
        
        j_dist_start_traces = calc_ll_dist(-9.35599, 112.691361, low_trace_lat_s,
                                          low_trace_lon_s)
        j_dist_end_traces = calc_ll_dist(-7.622251, 106.080779, low_trace_lat_e,
                                          low_trace_lon_e)
        
        print ("Dist between the trace start of the lower slab (jono and calc)  ", 
                j_dist_start_traces)
        print ("Dist between the trace end of the lower slab (jono and calc)  ", 
                j_dist_end_traces)
        
        
        
    def test_sliprate_functions(self):
        max_magnitude = 7.0
        prob_min_mag_cutoff = 4.0
        slip_rate_mm=2.0
        area_kms= float(30*10)
        prob_number_of_mag_sample_bins=20
        num_events =1000
        magnitudes = r_[4.803:6.997:num_events*1j]
        print magnitudes
        
        b = 1.
       
        #hack changed to guten
        bin_centroids = make_bins(prob_min_mag_cutoff,max_magnitude,
                                  prob_number_of_mag_sample_bins,
                                 'characteristic')
        #event_bins=r_[0:num_events]
        #event_bins=sorted(event_bins)
       

       
        event_bins = assign_event_bins(magnitudes, prob_min_mag_cutoff,max_magnitude,
                                  prob_number_of_mag_sample_bins,
                                  'characteristic')
        
        #(width,length)=Wells_and_Coppersmith_94("normal", bin_centroids, 15, 30)
#        event_bins = array([int(i) for i in
#                                (event_set.Mw[event_ind]
#                                 -zone_mlow)/delta_mag])
#
#        
#        m2=0.5
#        m_c=max_magnitude-m2
#        k =where(event_set.Mw[event_ind]>=m_c)
#        event_bins[k]=num_of_mag_sample_bins-1
                
           
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
#        pdfs= calc_activities_Characteristic(bin_centroids, b, 
#                                                              prob_min_mag_cutoff, 
#                                                              max_magnitude)

        pdfs =calc_activities_Characteristic(bin_centroids, b, 
                                                              prob_min_mag_cutoff, 
                                                              max_magnitude,
                                            prob_number_of_mag_sample_bins)
        
                  
     
        #print "\npdfs  from -Characteristic: ", pdfs
        print "calc_A_min_from_slip_rate(b,mMin,mMax,slip_rate_mm,recurr_dist,\
                              lat1,lon1,lat2,lon2,depth_top,depth_bottom,dip ",\
                              (calc_A_min_from_slip_rate(b,prob_min_mag_cutoff,\
                                                         max_magnitude,slip_rate_mm,
                                                         'characteristic',
                                                        0,144.5,0,144.8,10,15,30))


        event_activity_source = array(
                [(A_minCharacteristic*pdfs[z]/(sum(where(
                event_bins == z, 1,0)))) for z in event_bins])
        
#        pdfs= calc_activities_Characteristic(magnitudes, b, 
#                                                              prob_min_mag_cutoff, 
#                                                              max_magnitude)
#        event_activity_source =A_minCharacteristic*pdfs
#        
        #print "\nevent activity: ", event_activity_source
        print "\nsum event activity: ", sum(event_activity_source)
        
        for i in range(len(magnitudes)):
            print magnitudes[i],", ", event_activity_source[i]
        
        print
        
        t = arange(0.01, 20.0, 0.01)
        plt.figure()
        plt.semilogy(t, exp(-t/5.0))
        plt.title('Characteristic PDF')
        plt.xlabel('magnitude')
        plt.ylabel('probability')
        plt.plot(bin_centroids[:],pdfs[:])
        plt.ylim(0.00,0.6)
        plt.xlim(4,7)
        plt.savefig('pdf_characteristic.png')

        plt.figure()
        plt.semilogy(t, exp(-t/5.0))
        plt.title('Characteristic Event Activity')
        plt.xlabel('magnitude')
        plt.ylabel('events/year')
        plt.plot(magnitudes[:],event_activity_source[:])
        plt.ylim(0.00,0.01)
        plt.xlim(4,7)
        plt.savefig('characteristic_event_activity.png')
        
        plt.figure()
        plt.semilogy(t, exp(-t/5.0))
        event_activity_source=event_activity_source[::-1]
        bin_centroids=magnitudes[::-1]
        cumulative_event_activity= cumsum(event_activity_source)
        plt.title('Cumulative Characteristic Event Activity')
        plt.xlabel('magnitude')
        print " (max = " , max(cumulative_event_activity), ")"
        plt.ylabel('cumulative events/year')
        plt.plot(bin_centroids[:],cumulative_event_activity[:])
        plt.ylim(0.00,0.04)
        plt.xlim(4,7)
        plt.savefig('Cumulative_chrctrstc_event_activity.png')
        

       
        

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Sliprate_functions,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
