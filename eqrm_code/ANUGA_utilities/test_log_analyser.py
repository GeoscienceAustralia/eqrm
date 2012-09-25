#!/usr/bin/env python
#

# Warning, this will not update as the log format is updated.

import os
import unittest
import tempfile
from log_analyser import analyse_log, merge_dicts, LOGFILE

from eqrm_code.ANUGA_utilities.log import DELIMITER_J

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print "Import Error;  simplejson not installed."
        print "Install simplejson, or use Python2.6 or greater."
        import sys; sys.exit(1)
        
class logAnalyserCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_merge_dicts(self):
        d1 = {'a':1, 'b':1}
        d2 = {'b':2, 'c':3}
        results = merge_dicts(d1, d2, merge=lambda x,y:max(x,y))
        self.assertEqual(results, {'a':1, 'b':2, 'c':3})
        results = merge_dicts(d1, d2, merge=lambda x,y:min(x,y))
        self.assertEqual(results, {'a':1, 'b':1, 'c':3})
        results = merge_dicts(d1, d2, merge=lambda x,y:x+y)
        self.assertEqual(results, {'a':1, 'b':3, 'c':3})
        
    
    def log_lines(self, dic):
        """ Create a dummy json log line"""        
        line = '2012-01-23 13:20:10,147 INFO   general_mesh:202 |'
        msg = line + DELIMITER_J + json.dumps(dic)+ '\n' 
        return msg

    def test_log(self):
        # create a dummy directory and log file
        root_dir = tempfile.mkdtemp('test_logAnalyser')
        dir1 = tempfile.mkdtemp(dir=root_dir)
        dir2 = tempfile.mkdtemp(dir=root_dir)
        
        log_file_name = LOGFILE
        
        # Create a fake log file
        log_path_file1 = os.path.join(dir1, log_file_name)
        handle = file(log_path_file1, 'w')
        handle.write('yeah\n yeah\n ')
        handle.write('2012-01-23 13:20:10,147 INFO   general_mesh:202 |\n')
        made_up1 = {'numTriangles':1, 'startMeshTime':2,
                    'finishMeshTime':3}
        made_up2 = {'finishTime':4, 'startMemory':5,
                    'finishMemory':6,
                    'numTriangles':3}
        for dic in [made_up1, made_up2]:
            handle.write(self.log_lines(dic))
        handle.close()
        
        # Create another fake log file
        log_path_file2 = os.path.join(dir2, log_file_name)
        handle = file(log_path_file2, 'w')
        handle.write('yeah\n yeah\n ')
        handle.write('2012-01-23 13:20:10,147 INFO   general_mesh:202 |\n')
        made_up1 = {'numTriangles':30, 'startMeshTime':20,
                    'finishMeshTime':30}
        made_up2 = {'finishTime':40, 
                    'finishMemory':60,
                    'numTriangles':10}
        # No 'startMemory' in this log file 
        for key, val in made_up2.iteritems():
            handle.write(self.log_lines(dic))
        handle.close()

        # output file
        (handle, output_file) = tempfile.mkstemp('.csv',
        'log_analyser')
        os.close(handle)
        output_file = 'yeah.csv'

        analyse_log(root_dir, output_file, log_file_name)
        
        #FIXME check these results
        
        os.remove(log_path_file1)
        os.remove(log_path_file2)
        os.rmdir(dir1)
        os.rmdir(dir2)
        os.rmdir(root_dir)




################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(logAnalyserCase,'test')
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)
    
