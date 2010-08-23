import os
import sys
import unittest
from os.path import join
import tempfile

from scipy import array, allclose

from source_model import *
from source_model import Source_Zone_Polygon
from eqrm_code.event_set import Event_Set
from eqrm_code.util import reset_seed, determine_eqrm_path



#***************************************************************

class Test_Source_model(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_source_model_from_xml(self):
        
    
        handle, file_name = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        # I don't know what this is Lambda_Min="1.0"
        # But I added it so the tests would pass
        # Another example file at
        # Q:\python_eqrm\implementation_tests\input\newc_source_polygon.xml
        sample = """<Source_Model magnitude_type='Mw'>
    <polygon area='100'>
        <boundary>
-20 126.0
-21 126.5
-37 140
-20 126.0   
 </boundary>
        <recurrence distribution="sample" min_magnitude="5"  max_magnitude="8" A="2" Lambda_Min="0.5" b="1"></recurrence>
    </polygon>
    <polygon area='1000'>
        <boundary>
-10 100
-10 150
-40 150
-40 100
-10 100
        </boundary>
        <exclude>
-20 126.0
-21 126.5
-22 126.0
-23 125.5
-24 125.0
-25 125.5
-26 126.
-27 125.5
-28 125.
-29 124.5
-30 125.5
-31 125.6
-32 125.5
-33 125.
-34 124.5
-35 123.5
-36 127.5
-37 125.5
-37 140
-20 126.0   
        </exclude>
        <recurrence distribution="sample" min_magnitude="5"  max_magnitude="8" A="1" Lambda_Min="2.0"  b="1"></recurrence>
    </polygon>
</Source_Model>
"""
        handle.write(sample)
        handle.close()
        #handle = open(file_name, 'r')
        #print "handle.read()", handle.read()
        #handle.close()
        prob_min_mag_cutoff = 1.0
        source_model = source_model_from_xml(file_name,prob_min_mag_cutoff)
        os.remove(file_name)
        #print "source_model[1]", source_model[1]
        #print "source_model._source_zone_polygons", source_model._source_zone_polygons
        boundary = [(-20, 126.0), (-21, 126.5), (-37, 140), (-20, 126.0)]
        exclude = None
        min_magnitude = 5
        max_magnitude = 8
        b = 1
        Lambda_Min = 0.5
        szp = Source_Zone_Polygon(boundary,exclude,
                                  min_magnitude,max_magnitude,
                                  prob_min_mag_cutoff,
                                  Lambda_Min,b)
        #print "source_zone_polygon.polygon_object", szp._linestring
        result = source_model._source_zone_polygons[0]
        self.failUnless( result._linestring==szp._linestring,
            'Failed!')
        self.failUnless( result.min_magnitude==szp.min_magnitude,
            'Failed!')
        self.failUnless( result.max_magnitude==szp.max_magnitude,
            'Failed!')
        self.failUnless( result.b==szp.b,
            'Failed!')
        self.failUnless( result.Lambda_Min==szp.Lambda_Min,
            'Failed!')
        self.failUnless( result.prob_min_mag_cutoff==szp.prob_min_mag_cutoff,
            'Failed!')
        self.failUnless(source_model._magnitude_type=='Mw','Failed!')

    
    def test_source_model_from_xml_horspool(self):
        
        handle, file_name = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        sample = """<source_model_zone magnitude_type="Mw">
  <zone 
  area = "5054.035" 
  name = "bad zone">
    
    <geometry 
       azimuth= "6" 
       delta_azimuth= "2" 
       dip= "15"
       delta_dip = "5"
       depth_top_seismogenic = "7"
       depth_bottom_seismogenic = "30">
      <boundary>
	  151.1500 -32.4000  
	  152.1700 -32.7500
	  151.4300 -33.4500  
	  151.1500 -32.4000
      </boundary>
      <excludes>
	  151.1500 -32.4000    
	  152.1700 -32.7500   
	  151.4300 -33.4500 
      </excludes>
    </geometry>
    
    <recurrence_model
      distribution = "bounded_gutenberg_richter"
      recurrence_min_mag = "3.3" 
      recurrence_max_mag = "5.4" 
      lambda_min= "0.568" 
      b = "1">
      <event_generation 
      generation_min_mag = "3.3"
	  number_of_mag_sample_bins = "15" 
	  number_of_events = "1000" />
    </recurrence_model>
    
    <ground_motion_models 
       faulting_type = "normal" 
       ground_motion_selection = "crustal fault" />   
  </zone>
</source_model_zone>
"""
        handle.write(sample)
        handle.close()


        prob_min_mag_cutoff = 1.0
        source_model = source_model_from_xml(file_name,
                                             prob_min_mag_cutoff)
        os.remove(file_name)
        boundary = [(151.1500, -32.4000), 
                    (152.1700, -32.7500),
                    (151.4300, -33.4500),
                    (151.1500, -32.4000)]
        exclude = None # This is not tested
                       #[(151.1500, -32.4000),
                       #(152.1700, -32.7500),
                       #(151.4300, -33.4500)]
        min_magnitude = 3.3
        max_magnitude = 5.4
        b = 1
        Lambda_Min = 0.568
        szp = Source_Zone_Polygon(boundary,exclude,
                                  min_magnitude,max_magnitude,
                                  prob_min_mag_cutoff,
                                  Lambda_Min,b)
        #print "source_zone_polygon.polygon_object", szp._linestring
        result = source_model._source_zone_polygons[0]
        self.failUnless( result._linestring==szp._linestring,
            'Failed!')
        self.failUnless( result.min_magnitude==szp.min_magnitude,
            'Failed!')
        self.failUnless( result.max_magnitude==szp.max_magnitude,
            'Failed!')
        self.failUnless( result.b==szp.b,
            'Failed!')
        self.failUnless( result.Lambda_Min==szp.Lambda_Min,
            'Failed!')
        self.failUnless( result.prob_min_mag_cutoff==
                         szp.prob_min_mag_cutoff,
            'Failed!')
        self.failUnless(source_model._magnitude_type==
                        'Mw','Failed!')

    
    def test_Source_Zone_Polygon(self):
        prob_min_mag_cutoff = 1.0
        boundary = [(0, 0.0), (100., 0.0), (100., 100.0), (0., 100.0) ]
        exclude = [[(10., 10.0),  (20., 10.0),(20., 20.0),(10., 20.0)]]
        min_magnitude = 5
        max_magnitude = 8
        b = 1
        Lambda_Min = 0.5
        szp = Source_Zone_Polygon(boundary,exclude,
                                  min_magnitude,max_magnitude,
                                  prob_min_mag_cutoff,
                                  Lambda_Min,b)
        self.failUnless( boundary==szp._linestring,
            'Failed!')
        self.failUnless( exclude==szp._exclude,
            'Failed!')
        self.failUnless( min_magnitude==szp.min_magnitude,
            'Failed!')
        self.failUnless( max_magnitude==szp.max_magnitude,
            'Failed!')
        self.failUnless( b==szp.b,
            'Failed!')
        self.failUnless( Lambda_Min==szp.Lambda_Min,
            'Failed!')
        self.failUnless( prob_min_mag_cutoff==szp.prob_min_mag_cutoff,
            'Failed!')

        
    def test_Source_mini_check_gong(self):
        # Might start off hacky

        # this failed using the polygon contains point in shapely 1.03
        
        reset_seed(True)
        
        eqrm_dir = determine_eqrm_path()
        file_name = join(eqrm_dir, 'implementation_tests', 'input',
                             'newc_source_polygon.xml')
        #file_name = '../implementation_tests/input/newc_source_polygon.xml'
        fid_sourcepolys = open(file_name)
        
        prob_min_mag_cutoff = 4.5
        weight = [1.0]
        
        source_model = Source_Models(prob_min_mag_cutoff,
                                     weight,
                                     fid_sourcepolys)

        max_width = 15
        azi = [180, 180, 180, 180, 180, 180]
        prob_delta_azimuth_in_zones = [180, 180, 180, 180, 180, 180]
        dip = [35, 35, 35, 35, 35, 35]
        prob_min_mag_cutoff = 4.5
        prob_number_of_events_in_zones = [2, 1, 1, 2, 2, 2]
        prob_number_of_mag_sample_bins = 15
        
        events = Event_Set.generate_synthetic_events(
            fid_genpolys=fid_sourcepolys,
            fault_width=max_width,
            azi=azi,
            dazi=prob_delta_azimuth_in_zones,
            fault_dip=dip,
            prob_min_mag_cutoff=prob_min_mag_cutoff,
            override_xml=True,
            prob_number_of_events_in_zones=prob_number_of_events_in_zones)
        new_event_set = source_model.calculate_recurrence(events, prob_number_of_mag_sample_bins)
        event_activity = new_event_set.event_activity
        # Warning - this is just the results from running
        # calculate_recurrence at this version.
        # It is not independantly calculated to be correct
        actual =  [0.0058021,   0.01526108,  0.12673276,
                   0.23324915,  0.00144009,  0.00121821,
                   0.0062062,   0.00902211,  0.00554215,
                   0.0097141 ]
        self.failUnless( len(actual)==len(event_activity),
            'Failed!')
        # this fails using self.__contains_point_geo(point)
        self.assert_ (allclose(array(actual),event_activity))

        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Source_model,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
