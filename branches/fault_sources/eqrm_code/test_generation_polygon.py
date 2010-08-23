import os
import sys
import unittest
import tempfile

from os.path import join, split

from eqrm_code.generation_polygon import *

class Test_Generation_polygon(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_polygons_from_xml(self):

        # Let's work-out the eqrm dir
        eqrm_dir, tail = split( __file__)
        # Since this is the eqrn_code dir and we want the python_eqrm dir
        eqrm_dir = join(eqrm_dir, "..", "test_resources")
        filename = join(eqrm_dir, "sample_event.xml")

        return
    # need to work on.
        generation_polygons,magnitude_type = polygons_from_xml(
            filename=filename,
            fault_width= 13
            )
     
    def test_polygons_from_xml_horspool(self):
        
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
      recurrence_min_mag = "3.4" 
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
        azi=[45]
        dazi=[5]
        fault_dip=[60]
        fault_width=12
        prob_min_mag_cutoff=2.1
        generation_polygons, magnitude_type = polygons_from_xml(
            file_name,
            azi=azi,
            dazi=dazi,
            fault_dip=fault_dip,
            fault_width=fault_width,
            prob_min_mag_cutoff=prob_min_mag_cutoff,
            override_xml=True)
        os.remove(file_name)
        boundary = [(151.1500, -32.4000), 
                    (152.1700, -32.7500),
                    (151.4300, -33.4500),
                    (151.1500, -32.4000)]
        exclude = None # This is not tested
                       #[(151.1500, -32.4000),
                       #(152.1700, -32.7500),
                       #(151.4300, -33.4500)]
        fault_depth_dist = {'distribution':'constant',
                            'mean':'7'}
        fault_width_dist = {'distribution':'constant',
                            'mean':fault_width}
        azimuth = {'distribution':'uniform',
                       'minimum':float(azi[0])-float(dazi[0]),
                       'maximum': float(azi[0])+float(dazi[0])}
        dip = {'distribution':'constant','mean':float(fault_dip[0])}
        magnitude = {'distribution':'uniform',
                         'minimum':3.4,
                         'maximum': '5.4'}
        actual_gp = Generation_Polygon(
            boundary,
            fault_depth_dist,
            fault_width_dist,
            azimuth,dip,
            magnitude,exclude)
        
        #print "source_zone_polygon.polygon_object", szp._linestring
        calc_gp = generation_polygons[0]
        self.failUnless( magnitude_type=="Mw",
            'Failed!')
        self.failUnless( calc_gp._linestring==actual_gp._linestring,
            'Failed!')
        self.failUnless( calc_gp.fault_width_dist==fault_width_dist,
            'Failed!')
        self.failUnless( calc_gp.fault_depth_dist==fault_depth_dist,
            'Failed!')
        self.failUnless( calc_gp.azimuth==azimuth,
            'Failed!')
        self.failUnless( calc_gp.dip==dip,
            'Failed!')
        self.failUnless( calc_gp.magnitude==magnitude,
            'Failed!')

       
    

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Generation_polygon,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
