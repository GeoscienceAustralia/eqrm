#!/usr/bin/env python

"""
Generate the eqrm control file that is used by the implementation tests.

"""
import os
import sys
import unittest
import tempfile

from xml.etree import ElementTree as ET #, getiterator
"""
design
- read in the general input file
- modify it based on the ground motion models needed
- write many input files.

"""
#import elementtree.ElementTree as ET

# build a tree structure
root = ET.Element("source_model_zone")
root.set('magnitude_type', "Mw")

head = ET.SubElement(root, "zone")
head.set('area', "5054.035")

title = ET.SubElement(head, "geometry")
title.text = "Page Title"

body = ET.SubElement(root, "body")
body.set("bgcolor", "#ffffff")

body.text = """
  -32.4000  151.1500    
  -32.7500  152.1700    
  -33.4500  151.4300    
  -32.4000  151.1500    
"""

# wrap it in an ElementTree instance, and save as XML
tree = ET.ElementTree(root)
tree.write("page.xhtml")

# given a generation instance and a source instance, can I write an XML file?
# I should be able to, but it will be a mess.

# Therefore let's stick to something simpler.

title = ['dip', 'delta_dip', 'azimuth', 'delta_azimuth', 'distribution',]
zone1 = []
