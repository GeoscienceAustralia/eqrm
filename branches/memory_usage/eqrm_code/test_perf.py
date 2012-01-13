# -*- coding:utf-8 -*-
"""
Created on 12/01/2012

@author: u78240
"""

import os
import scipy
import tempfile
import unittest

from perf import *

try:
    from eqrm_code.ANUGA_utilities import log
    log_imported = True
except ImportError:
    log_imported = False
    
class Test_Perf(unittest.TestCase):
    
    def setUp(self):
        self.log_text = """2012-01-12 13:08:26,177 INFO                      analysis:154 |Logfile is '/nas/gemd/georisk_models/earthquake/EQRM_data/memory_test/output_large_coverage/log-0.txt' with logging level of DEBUG, console logging level is INFO
2012-01-12 13:08:26,178 DEBUG                     analysis:155 |host name: compute-0-2.local
2012-01-12 13:08:26,334 DEBUG                     analysis:157 |SVN version: 1881M
2012-01-12 13:08:26,335 DEBUG                     analysis:158 |SVN date: None
2012-01-12 13:08:26,336 DEBUG                     analysis:159 |SVN modified: None
2012-01-12 13:08:26,337 DEBUG                     analysis:160 |Memory: Initial
2012-01-12 13:08:26,338 DEBUG                     analysis:161 |Resource usage: memory=420.6MB resident=30.9MB stacksize=0.3MB
2012-01-12 13:08:26,499 DEBUG                     analysis:219 |Memory: source_model_zone created
2012-01-12 13:08:26,500 DEBUG                     analysis:220 |Resource usage: memory=423.7MB resident=31.9MB stacksize=0.3MB
2012-01-12 13:08:26,502 INFO                     event_set:363 |generating events
2012-01-12 13:08:27,392 DEBUG                    event_set:408 |Memory: populate_depth_top_seismogenic created
2012-01-12 13:08:27,392 DEBUG                    event_set:409 |Resource usage: memory=584.0MB resident=191.6MB stacksize=0.3MB
2012-01-12 13:08:29,825 DEBUG                    event_set:411 |Memory: populate_azimuth created
2012-01-12 13:08:29,825 DEBUG                    event_set:412 |Resource usage: memory=641.2MB resident=241.5MB stacksize=0.3MB
"""
        
        # Create temp log file
        (self.handle, self.file_name) = tempfile.mkstemp('.csv', 'test_perf_')
        os.close(self.handle)
        
        f = open(self.file_name,"wb")
        f.write(self.log_text)
        f.close()

        self.log_list = [('Initial','memory=420.6MB resident=30.9MB stacksize=0.3MB'),
                         ('source_model_zone created', 'memory=423.7MB resident=31.9MB stacksize=0.3MB'),
                         ('populate_depth_top_seismogenic created', 'memory=584.0MB resident=191.6MB stacksize=0.3MB'),
                         ('populate_azimuth created', 'memory=641.2MB resident=241.5MB stacksize=0.3MB')]
        
    def tearDown(self):
        os.remove(self.file_name)
    
    def test_log_analysis(self):
        # Set log global to the temp file_name
        log.log_filename = self.file_name
        
        # Run log file through log_analysis
        result = log_analysis()
        
        # Assert that the result is the same as self.log_list
        self.assertEqual(result, self.log_list)
    
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Perf,'test')
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)

    