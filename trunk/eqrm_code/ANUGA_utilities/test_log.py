#!/usr/bin/env python

import os
import sys
import unittest
import logging
from eqrm_code.ANUGA_utilities import log



class Test_Log(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        # The tests after this one should be quite.
        # Not too quite though, or exceptions are discarded.
        log.console_logging_level = log.ERROR
        
    # Problems with handles still present/ only closing at end of execution
    # 
#         logging.shutdown()
#         if os.path.exists(LOGFILE_NAME):
#             os.remove(LOGFILE_NAME)
#         self.f_open.close()
#         if os.path.exists(STDOUT_LOG_NAME):
#             os.remove(STDOUT_LOG_NAME)

    
    def FIXME_test_simple(self):

        current_default_to_console = log.default_to_console
        log.default_to_console = True
        LOGFILE_NAME = 'test.log'
        STDOUT_LOG_NAME = 'stdout.log'
        
        # Check that logging works in simple case.

        # just in case
        if os.path.exists(LOGFILE_NAME):
            os.remove(LOGFILE_NAME)
        if os.path.exists(STDOUT_LOG_NAME):
            os.remove(STDOUT_LOG_NAME)

        # set log module logfile name
        log.log_filename = LOGFILE_NAME

        # set logging levels for this test
        log.console_logging_level = logging.INFO
        log.file_logging_level = logging.DEBUG
        
        # vvvvv  WARNING - DO NOT REFORMAT THESE LINES!  vvvvv
        log_expect = '''2010-03-23 11:17:18,453 CRITICAL |Logfile is 'test.log' with logging level of DEBUG, console logging level is INFO
2010-03-23 11:17:18,469 DEBUG    |test at level DEBUG
2010-03-23 11:17:18,469 INFO     |test at level INFO'''

        stdout_expect = '''Logfile is 'test.log' with logging level of DEBUG, console logging level is INFO
test at level INFO'''
        # ^^^^^  WARNING - DO NOT REFORMAT THESE LINES!  ^^^^^

        # capture stdout to a file
        save_stdout = sys.stdout
        save_stderr = sys.stderr
        self.f_open = open(STDOUT_LOG_NAME, 'w')
        sys.stdout = sys.stderr = self.f_open

        #Initialise the logger
        log.set_log_file(LOGFILE_NAME)
                
        # do some logging
        log.debug('test at level DEBUG')
        #log.resource_usage(logging.INFO)
        log.info('test at level INFO')
        
        # put stdout/stderr back to normal
        sys.stderr = save_stderr
        sys.stdout = save_stdout

        # check logfile is as expected
        fd = open(LOGFILE_NAME, 'r')
        lines = fd.readlines()
        fd.close()

        result = strip_log(lines)
        expected = strip_log(log_expect.split('\n'))
        
        self.failUnlessEqual(result, expected)
        
        # check that captured stdout is as expected
        fd = open(STDOUT_LOG_NAME, 'r')
        lines = fd.readlines()
        fd.close()
        result = []
        for line in lines:
            l = line.strip('\n')
            result.append(l)
        expected = []
        for line in stdout_expect.split('\n'):
            expected.append(line)
        self.failUnlessEqual(result, expected)

        log.default_to_console = current_default_to_console

        
    def FIXME_test_set_log_file(self):
        # Since there are two tests,  set_log_file
        # is actually tested, though not be running twince in here.
        # The order the tests are done in does not matter
        
        current_default_to_console = log.default_to_console
        log.default_to_console = True
        
        LOGFILE_NAME = 'atest.log'
        STDOUT_LOG_NAME = 'cstdout.log'
        
        # just in case
        if os.path.exists(LOGFILE_NAME):
            os.remove(LOGFILE_NAME)
        if os.path.exists(STDOUT_LOG_NAME):
            os.remove(STDOUT_LOG_NAME)

        # set log module logfile name
        log.log_filename = LOGFILE_NAME

        # set logging levels for this test
        log.console_logging_level = logging.INFO
        log.file_logging_level = logging.DEBUG
        
        # vvvvv  WARNING - DO NOT REFORMAT THESE LINES!  vvvvv
        log_expect = '''2010-03-23 11:17:18,453 CRITICAL |Logfile is 'atest.log' with logging level of DEBUG, console logging level is INFO
2010-03-23 11:17:18,469 DEBUG    |test at level DEBUG
2010-03-23 11:17:18,469 INFO     |test at level INFO'''

        stdout_expect = '''Logfile is 'atest.log' with logging level of DEBUG, console logging level is INFO
test at level INFO'''
        # ^^^^^  WARNING - DO NOT REFORMAT THESE LINES!  ^^^^^

        # capture stdout to a file
        save_stdout = sys.stdout
        save_stderr = sys.stderr
        self.f_open = open(STDOUT_LOG_NAME, 'w')
        sys.stdout = sys.stderr = self.f_open

        #Initialise the logger
        log.set_log_file(LOGFILE_NAME)
        
        # do some logging
        log.debug('test at level DEBUG')
        #log.resource_usage(logging.INFO)
        log.info('test at level INFO')
        
        # put stdout/stderr back to normal
        sys.stderr = save_stderr
        sys.stdout = save_stdout
        

        # check logfile is as expected
        fd = open(LOGFILE_NAME, 'r')
        lines = fd.readlines()
        fd.close()

        result = strip_log(lines)
        expected = strip_log(log_expect.split('\n'))
        print "result",result
        print "expected", expected
        self.failUnlessEqual(result, expected)

        # check that captured stdout is as expected
        fd = open(STDOUT_LOG_NAME, 'r')
        lines = fd.readlines()
        fd.close()
        result = []
        for line in lines:
            l = line.strip('\n')
            result.append(l)
        expected = []
        for line in stdout_expect.split('\n'):
            expected.append(line)
        self.failUnlessEqual(result, expected)

        #log.close_log_file()

        log.default_to_console = current_default_to_console
        
def strip_log(lines):
    """
    Return a sub-set of the log file.  This subset is testable.
    Info that is not tested is dates, times, line numbers
    """
    out = []
    for line in lines:
        l = line.strip('\n')
        sub_l = l.split('|')
        # Jumping the time stamp 
        out.append(sub_l[1])
    return out
        
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Log, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
