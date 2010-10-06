#!/usr/bin/env python
import os
import sys
import unittest

from scipy import allclose,asarray     
from xml.etree import ElementTree as ET #, getiterator

from eqrm_code.xml_interface import Xml_Interface

from eqrm_code.ANUGA_utilities import log
#print "log.console_logging_level", log.console_logging_level
#log.console_logging_level = log.ERROR

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


class Test_Xml_Interface(unittest.TestCase):
    def test_attributes(self):
        xml = build_xml()
        assert xml['Event'][0].attributes['magnitude_type']=='Mw'
        #print "xml['Event']", xml['Event']
        xml.unlink()
        
    def test_getting_polygons(self):
        xml = build_xml()
        assert  len(xml['polygon'])==2
        xml.unlink()
        #log.log("YEAH$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #log.log("IF YOU ARE GETTING THIS MESSAGE")
        #log.log("THE console_logging_level IS TOO LOW.")


    def test_getting_excludes(self):
        xml = build_xml()
        assert len(xml['polygon'][0]['exclude'])==0
        assert len(xml['polygon'][1]['exclude'])==2
        xml.unlink()


    def test_getting_array(self):
        xml = build_xml()
        exclude_array = xml['polygon'][1]['exclude'][0].array
        expected_exclude_array=[[-32.0,121],[-34,122],[-32,121]]
        assert allclose(asarray(exclude_array),asarray(expected_exclude_array))
        xml.unlink()

    def Xtest_build_zone_xml(self):
        # Looking into something different
        root = build_xml()

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Xml_Interface,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
       
