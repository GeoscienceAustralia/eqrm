import os
import sys

import unittest
import tempfile

from scipy import exp, log, array, sum, allclose, r_


from eqrm_code.event_set import Event_Set
from eqrm_code.source_model import Source_Model, Source_Zone, Source, \
    create_fault_sources
from eqrm_code.recurrence_functions import *

class Dummy_event_set:
    def __init__(self, Mw):
        self.Mw = Mw     
    
    def __len__(self):
        return len(self.Mw)
 
class Dummy:
    def __init__(self):
        pass

                  
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

    def test_grscaleB(self):
        m = 7.9
        b = 0.43429448190325176 # this makes beta = 1 
        mmin = 4.
        mmax = 8.
        
        beta = b *log(10)
        
        tmp = exp(-1*beta*(mmax-mmin))
        test = (exp(-1*beta*(m-mmin))-tmp)/(1-tmp)
        self.assertEqual(test, grscale(b,mmax,m,mmin))   
        

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
    
    
    ##  As far as I can tell you can regard this function as generating
    ##  events for testing.
        def make_bins(min_mag,max_magnitude,num_bins,
              recurrence_model_dist = 'bounded_gutenberg_richter'):
            if (recurrence_model_dist == 'characteristic'):
                m2=0.5
                m_c=max_magnitude-m2
                
                delta_mag = (m_c-min_mag)/(num_bins)
                bins = r_[min_mag+delta_mag/2:m_c-delta_mag/2:(num_bins)*1j]
                
                characteristic_bin = array([m_c+(m2/2)])
                bins = append(bins,characteristic_bin)
            else:
                delta_mag = (max_magnitude-min_mag)/num_bins
                bins = r_[min_mag+delta_mag/2:max_magnitude-delta_mag/2:num_bins*1j]
            #approximate the number of earthquakes in discrete (0.1 unit) bins
            return bins
    
    
        max_magnitude = 7.0
        min_magnitude = 4.0
        slip_rate_mm = 2.0
        area_kms = float(30*10)
        b = 1.
        prob_number_of_mag_sample_bins = 10
        bin_centroids = make_bins(min_magnitude, max_magnitude,
                                  prob_number_of_mag_sample_bins,
                                  'characteristic')
#        event_bins = r_[0:10]
#        event_bins = sorted(event_bins)
#    
        A_minCharacteristic = calc_A_min_from_slip_rate_Characteristic(
            b, min_magnitude,
            max_magnitude,
            slip_rate_mm, area_kms)
        
        pdfs = calc_activities_Characteristic(bin_centroids, b, 
                                              min_magnitude, 
                                              max_magnitude)
        
#        event_activity_source = array(
#                [(A_minCharacteristic*pdfs[z]/(sum(where(
#                event_bins == z, 1,0)))) for z in event_bins])
        event_activity_source = array(A_minCharacteristic*pdfs)
        self.assert_(allclose(sum(event_activity_source),A_minCharacteristic))
        self.assert_(allclose(event_activity_source,[1.09104980e-02,
                                                     6.13542392e-03,
                                                     3.45020242e-03,
                                                     1.94019140e-03,
                                                     1.09104980e-03,
                                                     6.13542392e-04,
                                                     3.45020242e-04,
                                                     1.94019140e-04,
                                                     1.09104980e-04,
                                                     6.13542392e-05,
                                                     4.60091887e-04]))


    def test_calc_event_activity(self):
    
        # Create an event set
        Mw = [4.5, 5.5, 6.5, 7.5]
        Mw = [7.65, 7.75, 7.85, 7.95 ]
        event_set = Dummy_event_set(array(Mw))
        
        # Create a list of Sources  - eventually
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            ' <event_group event_type = "background">'
                            '  <GMPE fault_type = "normal">'
                            '     <branch model = "Toro" weight = "1.0"/>'
                            '  </GMPE>'
                            '  <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            ' </event_group>'
                            '</event_type_controlfile>'])
        handle.write(sample)
        handle.close()
        
        generation_min_mag = 7.6
        generation_min_mag = 4
        recurrence_min_mag = 4
        #recurrence_min_mag = 7.6
        actual_generation_min_mag = max(generation_min_mag, recurrence_min_mag)
        recurrence_max_mag = 8.0
        A_min = 10
        b = 1.4
        distribution = 'distribution'
        
        dummy = Dummy()
        dummy.magnitude_dist = {}
        dummy.magnitude_dist['minimum'] = actual_generation_min_mag
        dummy.magnitude_dist['maximum'] = recurrence_max_mag        
        dummy.generation_min_mag = generation_min_mag
        dummy.recurrence_max_mag  = recurrence_max_mag  
        dummy.recurrence_min_mag  = recurrence_min_mag  
        dummy.A_min = A_min
        dummy.b = b
        dummy.event_type = "background"
        dummy.name = 'name'
        dummy.distribution = 'bounded_gutenberg_richter'
        fsg_list = [dummy]
            
        magnitude_type = 'Mw'
        
        source_model = create_fault_sources(file_name, 
                                           fsg_list, 
                                           magnitude_type)
        for sm in source_model:
            sm.set_event_set_indexes( range(len(event_set)))
        event_activity_matrix = calc_event_activity(event_set, source_model)
        lamba = A_min * grscale(b, recurrence_max_mag, 
                                generation_min_mag, recurrence_min_mag)
        self.assert_(allclose(lamba, sum(event_activity_matrix)))
        

    def test_calc_event_activity_generation_min_mag(self):
    
        # Create an event set
        Mw = [7.65, 7.75, 7.85, 7.95 ]
        event_set = Dummy_event_set(array(Mw))
        
        # Create a list of Sources  - eventually
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            ' <event_group event_type = "background">'
                            '  <GMPE fault_type = "normal">'
                            '     <branch model = "Toro" weight = "1.0"/>'
                            '  </GMPE>'
                            '  <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            ' </event_group>'
                            '</event_type_controlfile>'])
        handle.write(sample)
        handle.close()
        
        generation_min_mag = 7.6
        recurrence_min_mag = 4
        #recurrence_min_mag = 7.6
        actual_generation_min_mag = max(generation_min_mag, recurrence_min_mag)
        recurrence_max_mag = 8.0
        A_min = 10
        b = 1.4
        distribution = 'distribution'
        
        dummy = Dummy()
        dummy.magnitude_dist = {}
        dummy.magnitude_dist['minimum'] = actual_generation_min_mag
        dummy.magnitude_dist['maximum'] = recurrence_max_mag        
        dummy.generation_min_mag = generation_min_mag
        dummy.recurrence_max_mag  = recurrence_max_mag  
        dummy.recurrence_min_mag  = recurrence_min_mag  
        dummy.A_min = A_min
        dummy.b = b
        dummy.event_type = "background"
        dummy.name = 'name'
        dummy.distribution = 'bounded_gutenberg_richter'
        fsg_list = [dummy]
            
        magnitude_type = 'Mw'
        
        source_model = create_fault_sources(file_name, 
                                           fsg_list, 
                                           magnitude_type)
        for sm in source_model:
            sm.set_event_set_indexes( range(len(event_set)))
        event_activity_matrix = calc_event_activity(event_set, source_model)
        lamba = A_min * grscale(b, recurrence_max_mag, 
                                generation_min_mag, recurrence_min_mag)
        
        self.assert_(allclose(lamba, sum(event_activity_matrix)))

        
    def test_calc_event_activity_summing(self):
    
        # Create an event set
        Mw = [4.5, 5.5, 6.5, 7.5]
        Mw = [7.65, 7.75, 7.85, 7.95 ]
        
        Mw = [4.5, 5.5, 6.5, 7.5]
        step = 0.1
        Mw = r_[4:8:step]
        #print "len(Mw)", len(Mw)
        event_set = Dummy_event_set(array(Mw))
        
        # Create a list of Sources  - eventually
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            ' <event_group event_type = "background">'
                            '  <GMPE fault_type = "normal">'
                            '     <branch model = "Toro" weight = "1.0"/>'
                            '  </GMPE>'
                            '  <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            ' </event_group>'
                            '</event_type_controlfile>'])
        handle.write(sample)
        handle.close()
        
        generation_min_mag = 4
        recurrence_min_mag = 4
        #recurrence_min_mag = 7.6
        actual_generation_min_mag = max(generation_min_mag, recurrence_min_mag)
        recurrence_max_mag = 8.0
        A_min = 10
        b = 1.4
        distribution = 'distribution'
        
        dummy = Dummy()
        dummy.magnitude_dist = {}
        dummy.magnitude_dist['minimum'] = actual_generation_min_mag
        dummy.magnitude_dist['maximum'] = recurrence_max_mag        
        dummy.generation_min_mag = generation_min_mag
        dummy.recurrence_max_mag  = recurrence_max_mag  
        dummy.recurrence_min_mag  = recurrence_min_mag  
        dummy.A_min = A_min
        dummy.b = b
        dummy.event_type = "background"
        dummy.name = 'name'
        dummy.distribution = 'bounded_gutenberg_richter'
        fsg_list = [dummy]
            
        magnitude_type = 'Mw'
        
        source_model = create_fault_sources(file_name, 
                                           fsg_list, 
                                           magnitude_type)
        for sm in source_model:
            sm.set_event_set_indexes( range(len(event_set)))
        event_activity_matrix = calc_event_activity(event_set, source_model)
        lamba = A_min * grscale(b, recurrence_max_mag, 
                                generation_min_mag, recurrence_min_mag)
        
        self.assert_(allclose(lamba, sum(event_activity_matrix)))

        

        
    
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Recurrence_functions,'test')
    #suite = unittest.makeSuite(Test_Recurrence_functions,'test_calc_event_activity_suss_summing')
    runner = unittest.TextTestRunner()
    runner.run(suite)
