#!/usr/bin/env python
"""


"""
import os
import sys
import unittest
import tempfile

from xml.etree import ElementTree as ET #, getiterator

def build_xml():
    test_string = """<Event magnitude_type='Mw'>
    <polygon>
        <boundary>
-20 120
-30 120
-20 120
        </boundary>
        <depth distribution = "constant" mean = "10" ></depth>
    </polygon>
    <polygon>
        <boundary>
-30 121
-35 122
-30 135
-30 121
        </boundary>
        <exclude>
-32 121
-34 122
-32 121
        </exclude>
        <exclude>
-35 121
-36 122
-35 121
        </exclude>
        <depth distribution = "constant" mean = "5" ></depth>
    </polygon>
</Event>
"""
    xml=Xml_Interface(string = test_string)
    return xml


class Test_ElementTree(unittest.TestCase):

    def test_element_tree(self):
        from xml.etree import ElementTree
        #3$$$as ET #, getiterator
        from xml.etree.ElementTree import ElementTree, Element, SubElement, \
             dump

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
        
        tree = ElementTree(file=file_name)
        elem = tree.getroot()
        # works
        #dump(elem)
        for sub in elem: #.getiterator():
            pass
            #dump(sub)
        os.remove(file_name)

def build_zone_xml():
    test_string = """<source_model_zone magnitude_type="Mw">
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

    test_string = '<source_model_zone>yeah</source_model_zone>'

    element = ET.XML("<root><child>One</child><child>Two</child></root>")
    dump(element)
    for subelement in element:
        print subelement.text

    
       
    tree = None #ET.XML()

    return tree


        
        
        
 
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_ElementTree,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
       
