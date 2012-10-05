#!/usr/bin/env python

"""
Demonstration of using the events_shaking_a_site function.

Copyright 2012 by Geoscience Australia

"""

from eqrm_code.postprocessing import events_shaking_a_site

params = {'output_dir':     './output',
          'site_tag':       'newc',
          'site_lat':       -30,
          'site_lon':       150,
          'atten_period':   1.0,
          'is_bedrock':     True} 

print 'Running events_shaking_a_site with parameters:'
print params

output_filename = events_shaking_a_site(params['output_dir'],
                                        params['site_tag'],
                                        params['site_lat'],
                                        params['site_lon'],
                                        params['atten_period'],
                                        params['is_bedrock'])

print 'File written to %s' % output_filename 