#!/usr/bin/env python

"""
Demonstration of using the generate_motion_csv function.

Copyright 2012 by Geoscience Australia

"""

from eqrm_code.postprocessing import generate_motion_csv

params = {'output_dir':     './output',
          'site_tag':       'newc',
          'is_bedrock':     True} 

print 'Running generate_motion_csv with parameters:'
print params

output_filenames = generate_motion_csv(params['output_dir'],
                                       params['site_tag'],
                                       params['is_bedrock'])

print 'Files written:' 
for file in output_filenames:
    print file