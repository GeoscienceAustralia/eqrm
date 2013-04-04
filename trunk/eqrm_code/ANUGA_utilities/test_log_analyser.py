#!/usr/bin/env python
#

# Warning, this will not update as the log format is updated.

import os
import unittest
import tempfile
import csv
import difflib
import shutil

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print "Import Error;  simplejson not installed."
        print "Install simplejson, or use Python2.6 or greater."
        import sys; sys.exit(1)
        
from log_analyser import analyse_log, merge_dicts, LOGFILETAG, add_nci_info2log, \
    newest_file_in_list, get_nci_value_pairs, colon_time2sec
    
from eqrm_code.ANUGA_utilities.log import DELIMITER_J

DUMMY_NCI_DATA = """
=============================================================================
                                     Resource usage:
                                       CPU time:              00:00:50
   JobId:      88518.vu-pbs            Elapsed time:          00:00:17
   Project:             w84            Requested time:        00:10:00
   Service Units:      0.04 
                                       Max physical memory:      433MB
                                       Max virtual memory:      1697MB
                                       Requested memory:       10000MB

                                       Number of cpus:               8

                                       Max jobfs disk use:       0.0GB
                                       Requested jobfs:          0.1GB
=============================================================================
"""

# CPU time:              00:00:55, not 50
DUMMY_NCI2_DATA = """
=============================================================================
                                     Resource usage:
                                       CPU time:              00:00:55
   JobId:      88518.vu-pbs            Elapsed time:          00:00:17
   Project:             w84            Requested time:        00:10:00
   Service Units:      0.04 
                                       Max physical memory:      433MB
                                       Max virtual memory:      1697MB
                                       Requested memory:       10000MB

                                       Number of cpus:               8

                                       Max jobfs disk use:       0.0GB
                                       Requested jobfs:          0.1GB
=============================================================================
"""
   
DUMMY_LOG_DATA = """
2013-04-02 13:40:57,720 DEBUG                     analysis:154 |Logfile is './half_sites_output/Bhalf_timing_p16_i0/log-0.txt' with logging level of DEBUG, console logging level is INFO
2013-04-02 13:40:57,737 INFO                      analysis:158 |Logfile is './half_sites_output/Bhalf_timing_p16_i0/log-0.txt' with logging level of DEBUG, console logging level is INFO
2013-04-02 13:40:57,743 INFO                      analysis:159 |JS*N{"parallel size": 16}
2013-04-02 13:41:02,719 DEBUG                     analysis:1099|Memory: calc_and_save_SA before return
2013-04-02 13:41:02,720 DEBUG                     analysis:1103|JS*N{"peak_resident MB": 55.9140625, "peak_memory MB": 501.5625, "peak_stacksize MB": 0.29296875}

"""     

DUMMY_LOG2_DATA = """
2013-04-02 13:40:57,720 DEBUG                     analysis:154 |Logfile is './half_sites_output/Bhalf_timing_p16_i0/log-0.txt' with logging level of DEBUG, console logging level is INFO
2013-04-02 13:40:57,737 INFO                      analysis:158 |Logfile is './half_sites_output/Bhalf_timing_p16_i0/log-0.txt' with logging level of DEBUG, console logging level is INFO
2013-04-02 13:40:57,743 INFO                      analysis:159 |JS*N{"parallel size": 16}
2013-04-02 13:41:02,719 DEBUG                     analysis:1099|Memory: calc_and_save_SA before return
2013-04-02 13:41:02,720 DEBUG                     analysis:1103|JS*N{"JobId": 55.9140625, "peak_memory MB": 501.5625, "peak_stacksize MB": 0.29296875}

"""     

class logAnalyserCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def assertMultiLineEqual(self, first, second, msg=None):
        """Assert that two multi-line strings are equal.

        If they aren't, show a nice diff.
        
        http://stackoverflow.com/questions/3942820/
        how-to-do-unit-testing-of-functions-writing-files-using-python-unittest
        """
        self.assertTrue(isinstance(first, str),
                'First argument is not a string')
        self.assertTrue(isinstance(second, str),
                'Second argument is not a string')

        if first != second:
            message = ''.join(difflib.ndiff(first.splitlines(True),
                                                second.splitlines(True)))
            if msg:
                message += " : " + msg
            self.fail("Multi-line strings are unequal:\n" + message)
            
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
        
        log_file_name = LOGFILETAG + '.txt'
        
        # Create a fake log file
        log_path_file1 = os.path.join(dir1, log_file_name)
        handle = file(log_path_file1, 'w')
        handle.write('yeah\n yeah\n ')
        handle.write('2012-01-23 13:20:10,147 INFO   general_mesh:202 |\n')
        made_up1 = {'a':1, 'f':2,
                    'e':3}
        made_up2 = {'d':4, 'c':5,
                    'b':6,
                    'a':7}
        for dic in [made_up1, made_up2]:
            handle.write(self.log_lines(dic))
        handle.close()
        
        # Create another fake log file
        log_path_file2 = os.path.join(dir2, log_file_name)
        handle = file(log_path_file2, 'w')
        handle.write('yeah\n yeah\n ')
        handle.write('2012-01-23 13:20:10,147 INFO   general_mesh:202 |\n')
        made_up1 = {'a':70, 'f':20,
                    'e':30}
        made_up2 = {'d':40, 
                    'b':60,
                    'a':10}
        # No 'startMemory' in this log file 
        for dic in [made_up1, made_up2]:
            handle.write(self.log_lines(dic))
        handle.close()

        # output file
        (handle, output_file) = tempfile.mkstemp('.csv',
        'log_analyser')
        os.close(handle)
        #output_file = 'yeah.csv'

        analyse_log(root_dir, output_file, log_file_name)
        
        actual = [['a', 'b',
                   'c', 'd',
                   'e', 'f'],
                  ['7', '6', '5', '4', '3', '2'],
                  ['70', '60', '', '40', '30', '20']]
        
        with open(output_file, 'rb') as f:
            results = []
            reader = csv.reader(f)
            for line in reader:
                results.append(line)
        self.assertEqual(actual[0], results[0])
        
        # The order of the log files is unknown
        if results[1][0] == '7':
            self.assertEqual(actual[1], results[1])
            self.assertEqual(actual[2], results[2])
        else:
            self.assertEqual(actual[1], results[2])
            self.assertEqual(actual[2], results[1])
            
       
        os.remove(output_file)
        os.remove(log_path_file1)
        os.remove(log_path_file2)
        os.rmdir(dir1)
        os.rmdir(dir2)
        os.rmdir(root_dir)

    def test_add_nci_info2log(self):
        test_dir = tempfile.mkdtemp()
        #print "test_dir", test_dir
        log_dir_a = os.path.join(test_dir, 'log_dir_a')
        os.mkdir(log_dir_a)
        log_dir_b = os.path.join(test_dir, 'log_dir_b')
        os.mkdir(log_dir_b)
        log_dir_c = os.path.join(test_dir, 'log_dir_c')
        os.mkdir(log_dir_c)
        log_dir_d = os.path.join(test_dir, 'log_dir_d')
        os.mkdir(log_dir_d)
        log_dir_e = os.path.join(test_dir, 'log_dir_e')
        os.mkdir(log_dir_e)
        
        # d Has a log file and two nci files
        filename = os.path.join(log_dir_d, '19089.vu-pb.OU')
        f = open(filename, 'wb')
        f.write(DUMMY_NCI_DATA)
        f.close()
        # the second file is created later
        
        log_d = os.path.join(log_dir_d, 'log-0.txt')
        f = open(log_d, 'wb')
        f.write(DUMMY_LOG_DATA)
        f.close()
        
        
        # a has log and nci file
        nci_a = os.path.join(log_dir_a, '19089.vu-pb.OU')
        f = open(nci_a, 'wb')
        f.write(DUMMY_NCI_DATA)
        f.close()
        
        log_a = os.path.join(log_dir_a, 'log-0.txt')
        f = open(log_a, 'wb')
        f.write(DUMMY_LOG_DATA)
        f.close()

        # b has log file
        log_b = os.path.join(log_dir_b, 'log-0.txt')
        f = open(log_b, 'wb')
        f.write(DUMMY_LOG_DATA)
        f.close()

        # c has nci file
        filename = os.path.join(log_dir_c, '19089.vu-pb.OU')
        f = open(filename, 'wb')
        f.write(DUMMY_NCI_DATA)
        f.close()
        
        # e has log with jobid in it and nci file
        filename = os.path.join(log_dir_e, '19089.vu-pb.OU')
        f = open(filename, 'wb')
        f.write(DUMMY_NCI_DATA)
        f.close()
        
        filename = os.path.join(log_dir_e, 'log-0.txt')
        f = open(filename, 'wb')
        f.write(DUMMY_LOG2_DATA)
        f.close()

        
        # d cont
        nci_d2 = os.path.join(log_dir_d, 'latest.vu-pb.OU')
        f = open(nci_d2, 'wb')
        f.write(DUMMY_NCI2_DATA)
        f.close()
        
        add_nci_info2log(test_dir)
        
        # a has log and nci file
        result = open(log_a).read()
        nci_dic = get_nci_value_pairs(nci_a)
        actual = DUMMY_LOG_DATA + DELIMITER_J + json.dumps(nci_dic)
        self.assertMultiLineEqual(result, actual)
        
        # b has log file only.  It isn't changed
        result = open(log_b).read()
        self.assertMultiLineEqual(result, DUMMY_LOG_DATA)
        
        # d has log and 2 nci files
        result = open(log_d).read()
        nci_dic = get_nci_value_pairs(nci_d2)
        actual = DUMMY_LOG_DATA + DELIMITER_J + json.dumps(nci_dic)
        self.assertMultiLineEqual(result, actual)
        
        # Let's do it again and see if it changes anything
        add_nci_info2log(test_dir)
        
        # a has log and nci file
        result = open(log_a).read()
        nci_dic = get_nci_value_pairs(nci_a)
        actual = DUMMY_LOG_DATA + DELIMITER_J + json.dumps(nci_dic)
        self.assertMultiLineEqual(result, actual)
        
        # b has log file only.  It isn't changed
        result = open(log_b).read()
        self.assertMultiLineEqual(result, DUMMY_LOG_DATA)
        
        # d has log and 2 nci files
        result = open(log_d).read()
        nci_dic = get_nci_value_pairs(nci_d2)
        actual = DUMMY_LOG_DATA + DELIMITER_J + json.dumps(nci_dic)
        self.assertMultiLineEqual(result, actual)
        
        shutil.rmtree(test_dir)
        
                
    def test_get_nci_value_pairs(self):
    
        DUMMY_NCI_DATA = """
=============================================================================
                                     Resource usage:
                                       CPU time:              00:00:50
   JobId:      88518.vu-pbs            Elapsed time:          00:00:17
   Project:             w84            Requested time:        00:10:00
   Service Units:      0.04 
                                       Max physical memory:      433MB
                                       Max virtual memory:      1697MB
                                       Requested memory:       10000MB

                                       Number of cpus:               8

                                       Max jobfs disk use:       0.0GB
                                       Requested jobfs:          0.1GB
=============================================================================
"""
        # get a temporary file
        (handle, filename) = tempfile.mkstemp('.vu-pb.OU','test_estimator')
        
        f = open(filename, 'wb')
        f.write(DUMMY_NCI_DATA)
        f.close()
        
        nci_dic = get_nci_value_pairs(filename)
        #print "nci_dic", nci_dic
        actual = {'CPU time (sec)':50, 'JobId':'88518.vu-pbs',
                  'Elapsed time (sec)':17, 'Project':'w84',
                  'Requested time (sec)':600, 'Service Units':0.04,
                  'Max physical memory (MB)':433,
                  'Max virtual memory (MB)':1697, 
                  'Requested memory (MB)':10000,
                  'Number of cpus':8, 'Max jobfs disk use (GB)':0.0,
                  'Requested jobfs (GB)':0.1}
        self.assertItemsEqual(nci_dic, actual)
        for key in actual:
            self.assertEqual(nci_dic[key], actual[key])
        os.remove(filename)  
        
               
    def test_get_nci_value_pairs2(self):
    
        DUMMY_NCI_DATA = """
=============================================================================
                                     Resource usage:
                                       CPU time:              01:00:32
   JobId:     109663.vu-pbs            Elapsed time:          01:00:51
   Project:             w84            Requested time:        00:10:00
   Service Units:      7.55 
                                       Max physical memory:       74MB
                                       Max virtual memory:       230MB
                                       Requested memory:        1000MB

                                       Max jobfs disk use:       0.0GB
                                       Requested jobfs:          0.1GB
=============================================================================
"""
        # get a temporary file
        (handle, filename) = tempfile.mkstemp('.vu-pb.OU','test_estimator')
        
        f = open(filename, 'wb')
        f.write(DUMMY_NCI_DATA)
        f.close()
        
        nci_dic = get_nci_value_pairs(filename)
        #print "nci_dic", nci_dic
        actual = {'CPU time (sec)':3632,
                  'JobId':'109663.vu-pbs',
                  'Elapsed time (sec)':3651, 
                  'Project':'w84',
                  'Requested time (sec)':600, 
                  'Service Units':7.55,
                  'Max physical memory (MB)':74,
                  'Max virtual memory (MB)':230, 
                  'Requested memory (MB)':1000,
                  'Max jobfs disk use (GB)':0.0,
                  'Requested jobfs (GB)':0.1}
        self.assertItemsEqual(nci_dic, actual)
        for key in actual:
            self.assertEqual(nci_dic[key], actual[key])
        os.remove(filename) 
        
    def test_colon_time2sec(self):
        self.assertEqual(colon_time2sec('00:01:04'), 64)
        self.assertEqual(colon_time2sec('01:01:04'), 3664)
        
    def slow_test_newest_file_in_list(self):
        # this test isn't done all the time, since it is slow.
    
        # get a temporary file
        (handle, filename1) = tempfile.mkstemp('.1','test_estimator')      
        f = open(filename1, 'wb')
        f.write('1')
        f.close()
        
        import time; time.sleep(1)
        # get a temporary file
        
        (handle, filename2) = tempfile.mkstemp('.2','test_estimator')       
        f = open(filename2, 'wb')
        f.write('2')
        f.close()
        
        latest = newest_file_in_list([filename1, filename2])
        self.assertEqual(latest, filename2)
        


################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(logAnalyserCase,'test')
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)
    
