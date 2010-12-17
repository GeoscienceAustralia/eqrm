import os
import sys
import unittest
import tempfile

from os.path import join, split
import types

from eqrm_code.generation_polygon import *

class Test_Generation_polygon(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

     
    def test_polygons_from_xml_horspool(self):
        
        handle, file_name = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        sample = """<source_model_zone magnitude_type="Mw">
  <zone 
  area = "5054.035" 
  name = "bad zone"
  event_type = "crustal fault">
    
    <geometry 
       azimuth= "45" 
       delta_azimuth= "5" 
       dip= "35"
       delta_dip = "5"
       depth_top_seismogenic = "7"
       depth_bottom_seismogenic = "15.60364655">
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
      A_min= "0.568" 
      b = "1">
      <event_generation 
      generation_min_mag = "3.3"
	  number_of_mag_sample_bins = "15" 
	  number_of_events = "1000" />
    </recurrence_model>
    
    <ground_motion_models 
       fault_type = "normal" 
       ground_motion_selection = "crustal fault" />   
  </zone>
</source_model_zone>
"""
        handle.write(sample)
        handle.close()


        dip= 35
        delta_dip = 5
        prob_min_mag_cutoff = 1.0
        azi=[45]
        dazi=[5]
        fault_dip=[60]
        fault_width=12
        prob_min_mag_cutoff=2.1
        
        generation_polygons, magnitude_type = polygons_from_xml(
            file_name,
            prob_min_mag_cutoff=prob_min_mag_cutoff)
        os.remove(file_name)
        boundary = [(151.1500, -32.4000), 
                    (152.1700, -32.7500),
                    (151.4300, -33.4500),
                    (151.1500, -32.4000)]
        exclude = None # This is not tested
                       #[(151.1500, -32.4000),
                       #(152.1700, -32.7500),
                       #(151.4300, -33.4500)]
        depth_top_seismogenic_dist = {'distribution':'constant',
                            'mean':7}
        depth_bottom_seismogenic_dist = {'distribution':'constant',
                            'mean':15.60364655}
        azimuth = {'distribution':'uniform',
                       'minimum':float(azi[0])-float(dazi[0]),
                       'maximum': float(azi[0])+float(dazi[0])}
        dip = {'distribution':'uniform',
               'minimum':float(dip)-float(delta_dip),
               'maximum': float(dip)+float(delta_dip)}
        magnitude = {'distribution':'uniform',
                         'minimum':3.4,
                         'maximum': '5.4'}
        polygon_name = 'bad zone'
        polygon_event_type = "crustal fault"
        number_of_events = 1000
        number_of_mag_sample_bins = 15
        actual_gp = Generation_Polygon(
            boundary,
            depth_top_seismogenic_dist,
            azimuth,dip,
            magnitude,
            depth_bottom_seismogenic_dist,
            polygon_name,
            polygon_event_type,
            number_of_events,
            exclude)
        
        #print "source_zone_polygon.polygon_object", szp._linestring
        calc_gp = generation_polygons[0]
        self.failUnless(magnitude_type=="Mw",
            'Failed!')
        self.failUnless(calc_gp._linestring==actual_gp._linestring,
            'Failed!')
        self.failUnless(calc_gp.depth_bottom_seismogenic_dist ==
                        depth_bottom_seismogenic_dist,'Failed!')
        
        self.failUnless(calc_gp.depth_top_seismogenic_dist==depth_top_seismogenic_dist,
            'Failed!')
        self.failUnless(calc_gp.azimuth==azimuth,
            'Failed!')
        self.failUnless(calc_gp.dip==dip,
            'Failed!')
        self.failUnless(calc_gp.magnitude==magnitude,
            'Failed!')
        self.failUnless(calc_gp.number_of_events==number_of_events,
            'Failed!')
        self.failUnless(calc_gp.polygon_name=="bad zone",
            'Failed!')

    def test_xml_fault_generators(self):
        def dump_fault(fault):
            """Helper function to dump info from FSG object."""

            for attr in dir(fault):
                if attr[0] != '_' and attr != 'name_type_map':
                    val = eval('fault.%s' % attr)
                    if isinstance(val, dict):
                        print('    %s=%s' % (attr, str(val)))
                    elif isinstance(val, types.MethodType):
                        pass
                    else:
                        print('    %s=%s (%s)' % (attr, str(val), type(val)))

        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<source_model_fault magnitude_type="Mw">',
                            '  <fault name="big fault" event_type="crustal fault">',
                            '    <geometry dip="30" out_of_dip_theta="0"',
                            '              delta_theta="0"',
                            '              depth_top_seismogenic="0"',
                            '              depth_bottom_seismogenic="15"',
                            '              slab_width="0">',
                            '      <trace>',
                            '        <start lat="-17.5" lon="110.0" />',
                            '        <end lat="-17.0" lon="110.0" />',
                            '      </trace>',
                            '    </geometry>',
                            '    <recurrence_model distribution="bounded_gutenberg_richter"',
                            '                      recurrence_min_mag="4.0"',
                            '                      recurrence_max_mag="7.0"',
                            '                      slip_rate="2.0" b="1">',
                            '      <event_generation generation_min_mag="4.0"',
                            '                        number_of_mag_sample_bins="15"',
                            '                        number_of_events="1500" />',
                            '    </recurrence_model>',
                            '  </fault>',
                            '  <fault name="small fault" event_type="crustal fault">',
                            '    <geometry dip="90" out_of_dip_theta="10"',
                            '              delta_theta="5"',
                            '              depth_top_seismogenic="10"',
                            '              depth_bottom_seismogenic="50"',
                            '              slab_width="10">',
                            '      <trace>',
                            '        <start lat="-17.0" lon="120.0" />',
                            '        <end lat="-17.0" lon="120.5" />',
                            '      </trace>',
                            '    </geometry>',
                            '    <recurrence_model distribution="characteristic"',
                            '                      recurrence_min_mag="4.5"',
                            '                      recurrence_max_mag="7.5"',
                            '                      slip_rate="3.0" b="2">',
                            '      <event_generation generation_min_mag="4.0"',
                            '                        number_of_mag_sample_bins="15"',
                            '                        number_of_events="1500" />',
                            '    </recurrence_model>',
                            '  </fault>',
                            '  <fault name="sumba intraplate" event_type="intraplate">',
                            '    <geometry dip="20" out_of_dip_theta="90"',
                            '              delta_theta="20"',
                            '              depth_top_seismogenic="10"',
                            '              depth_bottom_seismogenic="100"',
                            '              slab_width="20">',
                            '      <trace>',
                            '        <start lat="-0.5" lon="115.0" />',
                            '        <end lat="0.5" lon=" 116.0" />',
                            '      </trace>',
                            '    </geometry>',
                            '    <recurrence_model distribution="bounded_gutenberg_richter"',
                            '                      recurrence_min_mag="4.2"',
                            '                      recurrence_max_mag="7.2"',
                            '                      A_min="0.58" b="1">',
                            '      <event_generation generation_min_mag="4.0"',
                            '                        number_of_mag_sample_bins="15"',
                            '                        number_of_events="3000" />',
                            '    </recurrence_model>',
                            '  </fault>',
                            '</source_model_fault>'])

        handle.write(sample)
        handle.close()

        (faults, magtype) = xml_fault_generators(file_name)
        os.remove(file_name)
#        # dump the FSG objects
#        for fault in faults:
#            print('-'*50)
#            print('%s:' % fault.name)
#            dump_fault(fault)

        msg = "Expected magnitude type 'Mw', got '%s'" % magtype
        self.failUnlessEqual(magtype, 'Mw')

        # check a few of the values, especially those calculated
        # 'big fault' first - must not assume it's the first
        for fault in faults:
            if fault.name == 'big fault':
                break
        else:
            msg = "Couldn't find 'big fault' fault!?"
            self.fail(msg)
        self.failUnlessEqual(fault.event_type, 'crustal fault')
        expected = {'distribution': 'constant', 'mean': 30.0}
        self.failUnlessEqual(fault.dip_dist, expected)
        
        expected = {'distribution': 'uniform', 'minimum': 0.0, 'maximum': 0.0}
        self.failUnlessEqual(fault.out_of_dip_theta_dist, expected)
        
        expected = {'distribution': 'constant', 'mean': 0.0}
        self.failUnlessEqual(fault.depth_top_seismogenic_dist, expected)
        
        expected = {'distribution': 'constant', 'mean': 15.0}
        self.failUnlessEqual(fault.depth_bottom_seismogenic_dist, expected)
        self.failUnlessEqual(fault.slab_width, 0.0)
        self.failUnlessEqual(fault.trace_start_lat, -17.5)
        self.failUnlessEqual(fault.trace_start_lon, 110.0)
        self.failUnlessEqual(fault.trace_end_lat, -17.0)
        self.failUnlessEqual(fault.trace_end_lon, 110.0)
        expected = {'distribution': 'constant', 'mean': 0.0}
        self.failUnlessEqual(fault.azimuth_dist, expected)
        self.failUnlessEqual(fault.distribution, 'bounded_gutenberg_richter')
        self.failUnlessEqual(fault.recurrence_min_mag, 4.0)
        self.failUnlessEqual(fault.recurrence_max_mag, 7.0)
        self.failUnlessEqual(fault.b, 1.0)
        # A_min not supplied above, should be there (converted from slip_rate)
        self.failUnless(not fault.A_min is None)
        self.failUnlessEqual(fault.generation_min_mag, 4.0)
        self.failUnlessEqual(fault.number_of_mag_sample_bins, 15)
        self.failUnlessEqual(fault.number_of_events, 1500)
        expected = {'distribution': 'uniform', 'minimum': 4.0, 'maximum': 7.0}
        self.failUnlessEqual(fault.magnitude_dist, expected)

        # a few spot values in 'sumba intraplate'
        for fault in faults:
            if fault.name == 'sumba intraplate':
                break
        else:
            msg = "Couldn't find 'sumba intraplate' fault!?"
            self.fail(msg)
        self.failUnlessEqual(fault.event_type, 'intraplate')
        expected = {'distribution': 'constant', 'mean': 20.0}
        self.failUnlessEqual(fault.dip_dist, expected)
        self.failUnlessEqual(fault.A_min, 0.58)
        self.failUnlessEqual(fault.number_of_events, 3000)
        
        #test for Fault_Source_Generator.populate_out_of_dip_theta
        fault.out_of_dip_theta_dist={'distribution': 'uniform', 'minimum': 83,
                                'maximum': 98}
        out_of_dip= fault.populate_out_of_dip_theta(100,90.0)
        (errorIndexes,) = where((out_of_dip > (175-90)) &
                                     (out_of_dip < (185-90)))
        
        self.failUnlessEqual(len(errorIndexes),0)
        
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Generation_polygon,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
