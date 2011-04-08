import os
import sys
import unittest
from os.path import join
import tempfile
import types

from scipy import array, allclose

from source_model import *
from source_model import Source_Zone
from eqrm_code.event_set import Event_Set
from eqrm_code.util import reset_seed, determine_eqrm_path



#***************************************************************

class Dummy:
    def __init__(self):
        pass
    
class Test_Source_model(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_source_model_from_xml(self):
        
        handle, file_name = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        sample = """<source_model_zone magnitude_type="Mw">
  <zone 
  area = "5054.035"  event_type = "TS_haz03" name="bake">
    
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
        source_model = source_model_from_xml(file_name)
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
        A_min = 0.568
        number_of_mag_sample_bins = 15
        event_type = 'fish'
        name = 'bake'
        generation_min_mag = 1.0
        szp = Source_Zone(boundary,exclude,
                          min_magnitude,max_magnitude,
                          generation_min_mag,
                          A_min,b,
                          number_of_mag_sample_bins,
                          event_type,
                          name)
        #print "source_zone_polygon.polygon_object", szp._linestring
        result = source_model._sources[0]
        self.failUnless(result._linestring==szp._linestring,
            'Failed!')
        self.failUnless(result.min_magnitude==szp.min_magnitude,
            'Failed!')
        self.failUnless(result.max_magnitude==szp.max_magnitude,
            'Failed!')
        self.failUnless(result.b==szp.b,
            'Failed!')
        self.failUnless(result.A_min==szp.A_min,
            'Failed!')
        self.failUnless(result.name == name,'Failed!')
        self.failUnless(szp.name == name,'Failed!')
        self.failUnless(source_model._magnitude_type == 'Mw','Failed!')
        self.failUnless(result.number_of_mag_sample_bins== 15,'Failed!')

    
    def test_Source_Zone(self):
        boundary = [(0, 0.0), (100., 0.0), (100., 100.0), (0., 100.0) ]
        exclude = [[(10., 10.0),  (20., 10.0),(20., 20.0),(10., 20.0)]]
        min_magnitude = 5
        max_magnitude = 8
        b = 1
        A_min = 0.5
        number_of_mag_sample_bins = 15
        event_type = 'fish'
        name = 'Source_Zone'
        generation_min_mag = 1.0
        szp = Source_Zone(boundary, exclude,
                          min_magnitude, max_magnitude,
                          generation_min_mag,
                          A_min, b,
                          number_of_mag_sample_bins, event_type,
                          name)
        self.failUnless(boundary==szp._linestring,
            'Failed!')
        self.failUnless(exclude==szp._exclude,
            'Failed!')
        self.failUnless(min_magnitude==szp.min_magnitude,
            'Failed!')
        self.failUnless(max_magnitude==szp.max_magnitude,
            'Failed!')
        self.failUnless(b==szp.b,
            'Failed!')
        self.failUnless(A_min==szp.A_min,
            'Failed!')
        self.failUnless(szp.number_of_mag_sample_bins== \
                        number_of_mag_sample_bins,'Failed!')

   
    def test_Source(self):
        def dump_etc(etc):
            """Helper function to dump info from EG object."""

            for attr in dir(etc):
                if attr[0] != '_': # and attr != 'name_type_map':
                    val = eval('etc.%s' % attr)
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
                            '<event_type_controlfile>'
                            '  <event_group event_type = "background">'
                            '    <GMPE fault_type = "normal">'
                            '      <branch model = "Toro_1997_midcontinent" weight = "0.3"/>'
                            '      <branch model = "Atkinson_Boore_97" weight = "0.4"/>'
                            '      <branch model = "Sadigh_97" weight = "0.3"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '  <event_group event_type = "crustal fault">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Campbell08" weight = "0.8"/>'
                            '      <branch model = "Boore08" weight = "0.2"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "reverse" />'
                            '  </event_group>'
                            '  <event_group event_type = "interface">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Zhao06_crustalinterface" weight = "0.5"/>'
                            '      <branch model = "Atkinson03_interface" weight = "0.5"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "reverse" />'
                            '  </event_group>'
                            '  <event_group event_type = "intraslab">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Zhao06_slab" weight = "0.5"/>'
                            '      <branch model = "Atkinson03_inslab" weight = "0.5"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '</event_type_controlfile>'])

        handle.write(sample)
        handle.close()

        etc_list = event_control_from_xml(file_name)

#        # dump the EG objects
#        for etc in etc_list:
#            print('-'*50)
#            print('%s:' % etc.event_type)
#            dump_etc(etc)

        for etc in etc_list:
            if etc.event_type == 'crustal fault':
                break
        else:
            msg = "Couldn't find 'crustal fault' <event_group>!?"
            self.fail(msg)
        self.failUnlessEqual(etc.fault_type, 'reverse')
        expected = ['Campbell08', 'Boore08']
        self.failUnlessEqual(etc.branch_models, expected)
        expected = [0.80000000000000004, 0.20000000000000001]
        self.failUnless(allclose(etc.branch_weights, expected))
        expected = {'scaling_rule': 'Wells_and_Coppersmith_94',
                    'scaling_fault_type': 'reverse'}
        self.failUnlessEqual(etc.scaling_dict,  expected)

        os.remove(file_name)

    def test_Source2(self):
        """Test various expected exceptions for XML errors."""

        # is badly-formed XML caught?
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            '</event_type_controlfileX>'])

        handle.write(sample)
        handle.close()

        self.failUnlessRaises(Exception, event_control_from_xml, (file_name,))

        os.remove(file_name)

        # missing <event_type_controlfile> tag
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfileX>'
                            '</event_type_controlfileX>'])

        handle.write(sample)
        handle.close()

        self.failUnlessRaises(Exception, event_control_from_xml, (file_name,))

        os.remove(file_name)

        # missing <event_group> tag
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            '  <event_groupX event_type = "background">'
                            '  </event_groupX>'
                            '</event_type_controlfile>'])

        handle.write(sample)
        handle.close()

        self.failUnlessRaises(Exception, event_control_from_xml, (file_name,))

        os.remove(file_name)

        # 0 occurrences of <GMPE> tag
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            '  <event_group event_type = "background">'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '</event_type_controlfile>'])

        handle.write(sample)
        handle.close()

        self.failUnlessRaises(Exception, event_control_from_xml, (file_name,))

        os.remove(file_name)

        # >1 occurrence of <GMPE> tag
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            '  <event_group event_type = "background">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Zhao06_slab" weight = "0.5"/>'
                            '      <branch model = "Atkinson03_inslab" weight = "0.5"/>'
                            '    </GMPE>'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Zhao06_slab" weight = "0.5"/>'
                            '      <branch model = "Atkinson03_inslab" weight = "0.5"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '</event_type_controlfile>'])

        handle.write(sample)
        handle.close()

        self.failUnlessRaises(Exception, event_control_from_xml, (file_name,))

        os.remove(file_name)

        # 0 occurrence of <branch> tag
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            '  <event_group event_type = "background">'
                            '    <GMPE fault_type = "reverse">'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '</event_type_controlfile>'])

        handle.write(sample)
        handle.close()

        self.failUnlessRaises(Exception, event_control_from_xml, (file_name,))

        os.remove(file_name)

        # sum of <branch weight> attributes != 1.0
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            '  <event_group event_type = "background">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Zhao06_slab" weight = "0.6"/>'
                            '      <branch model = "Atkinson03_inslab" weight = "0.5"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '</event_type_controlfile>'])

        handle.write(sample)
        handle.close()

        self.failUnlessRaises(Exception, event_control_from_xml, (file_name,))

        os.remove(file_name)

    def test_add_event_type_atts_to_sources(self):
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        sample = '\n'.join(
            ['<?xml version="1.0" encoding="UTF-8"?>',
             '<event_type_controlfile>'
             '  <event_group event_type = "ham">'
             '    <GMPE fault_type = "more_ham">'
             '      <branch model = "food" weight = "1.0"/>'
             '    </GMPE>'
             '    <scaling scaling_rule = "y" />'
             '  </event_group>'
             '  <event_group event_type = "eggs">'
             '    <GMPE fault_type = "more_eggs">'
             '      <branch model = "Camp" weight = "0.33"/>'
             '      <branch model = "Tongs" weight = ".66"/>'
             '    </GMPE>'
             '    <scaling scaling_rule = "e" />'
             '  </event_group>'
             '</event_type_controlfile>'])

        handle.write(sample)
        handle.close()

        
        event_type = ['ham', 'eggs', 'ham', 'eggs', 'eggs']
        dummy_list = []
        for name in event_type:
            d = Dummy()
            d.event_type = name
            dummy_list.append(d)
            source_mod = Source_Model(dummy_list, 'Mw')
        source_mod.add_event_type_atts_to_sources(file_name)

        for s in source_mod:
            if s.event_type == 'ham':
                self.failUnlessEqual(s.fault_type, "more_ham")
            else:
                self.failUnlessEqual(s.fault_type, "more_eggs")
            
        os.remove(file_name)
        max_num_atten_models = source_mod.get_max_num_atten_models()
        self.failUnlessEqual(max_num_atten_models, 2)
        
        
    def test_create_scenario_source_model(self):
        source_model = Source_Model.create_scenario_source_model(3)
        self.failUnless(allclose(source_model[0].event_set_indexes,
                                     array([0,1,2])))

    def test_sources_of_event_set(self):
        setups = [('5,3,2', [5,3,2]), ('6,4',[6, 4]), ('0,1',[0,1])]
        setups_dic = dict(setups)
        sources = []
        for setup in setups:
            d = Dummy()
            d.name = setup[0]
            d.event_set_indexes = setup[1]
            sources.append(d)
        sm = Source_Model(sources)
        sources_wrt_events = sm.sources_of_event_set(7)
        for i, source in enumerate(sources_wrt_events):
            key = source.name
            self.failUnless(setups_dic.has_key(key))
            self.failUnless(i in setups_dic[key])
            setups_dic[key].remove(i)
            
        
            
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Source_model,'test')
    #suite = unittest.makeSuite(Test_Source_model,'test_add_event_type_atts_to_sources')
    runner = unittest.TextTestRunner()
    runner.run(suite)
