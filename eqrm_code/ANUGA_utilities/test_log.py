#!/usr/bin/env python

from cStringIO import StringIO
import os
import sys
import unittest
import logging
from eqrm_code.ANUGA_utilities import log
import tempfile



class Test_Log(unittest.TestCase):
    def setUp(self):
        # Store current log values
        self.console_level_orig = log.console_logging_level
        self.file_level_orig = log.file_logging_level
        self.default_to_console_orig = log.default_to_console
        self.log_filename_orig = log.log_filename
        self.allow_level_override_orig = log.allow_level_override
        
        # Redirect stderr and stdout
        self.console = StringIO()
        sys.stdout = self.console
        
        # Temporary log file
        (handle, self.logfile) = tempfile.mkstemp('.log', 'test_log_')
        os.close(handle)
        
        # Initialise the new logger
        log.default_to_console = True
        log.allow_level_override = True
        log.set_log_file(self.logfile, log.file_logging_level)

    def tearDown(self):
        # Remove the temporary logfile
        log.remove_file_handler()
        log.remove_log_file()
        
        # Set everything back to the way it was
        log.default_to_console = self.default_to_console_orig
        log.allow_level_override = self.allow_level_override_orig
        log.set_log_level(logging.getLevelName(self.file_level_orig), 
                          logging.getLevelName(self.console_level_orig))
        log.set_log_file(self.log_filename_orig)
        
        # ..and stdout!
        sys.stdout = sys.__stdout__
        
    def logMessages(self):
        log.debug('test at level DEBUG')
        log.info('test at level INFO')
        log.warning('test at level WARNING')
        log.error('test at level ERROR')
        log.critical('test at level CRITICAL')
    
    def log_level_test(self, 
                       file_expected,
                       console_expected,
                       file_level,
                       console_level):
        
        log.set_log_level(file_level, console_level)
        
        self.logMessages()
        
        # Get file output
        f = open(self.logfile, 'r')
        lines = f.readlines()
        f.close()

        # The first line is the output message from
        # log.set_log_file(self.logfile, log.file_logging_level)
        # so we want the slice after this
        file_result = strip_log(lines)[1:]
        console_result = self.console.getvalue().strip().split('\n')[1:]
        
        file_expected = strip_log(file_expected.split('\n'))
        console_expected = console_expected.split('\n')
        
        self.assertEqual(file_result, file_expected)
        self.assertEqual(console_result, console_expected)
    
    def test_set_log_level(self):
        """
        Test standard operation of set_log_level
        """
        
        file_expected = '''|Logfile is '%s' with logging level of INFO, console logging level is ERROR
|test at level INFO
|test at level WARNING
|test at level ERROR
|test at level CRITICAL''' % self.logfile

        console_expected = '''test at level ERROR
test at level CRITICAL'''
        
        file_level = 'info'
        console_level = 'error'
        
        self.log_level_test(file_expected, 
                            console_expected, 
                            file_level, 
                            console_level)
        
        
    def test_set_log_level_no_console(self):
        """
        Test set_log_level where console level is set by default 
        (file level + increment)
        """
        file_expected = '''|Logfile is '%s' with logging level of DEBUG, console logging level is INFO
|test at level DEBUG
|test at level INFO
|test at level WARNING
|test at level ERROR
|test at level CRITICAL''' % self.logfile

        console_expected = '''test at level INFO
test at level WARNING
test at level ERROR
test at level CRITICAL'''
        
        file_level = 'debug'
        console_level = None
        
        self.log_level_test(file_expected, 
                            console_expected, 
                            file_level, 
                            console_level)
    
    def test_set_log_level_conflict(self):
        """
        Test set_log_level where console level < file level
        """
        file_expected = '''|Logfile is '%s' with logging level of INFO, console logging level is INFO
|test at level INFO
|test at level WARNING
|test at level ERROR
|test at level CRITICAL''' % self.logfile

        console_expected = '''test at level INFO
test at level WARNING
test at level ERROR
test at level CRITICAL'''
        
        file_level = 'error'
        console_level = 'info'
        
        self.log_level_test(file_expected, 
                            console_expected, 
                            file_level, 
                            console_level)
    
    def test_set_log_level_no_effect(self):
        """
        Test set_log_level where it is expected to have no effect. i.e.
        levels set programmatically elsewhere
        """
        log.allow_level_override = False
        log.console_logging_level = log.WARNING
        log.file_logging_level = log.INFO
        
        log.set_log_level(level='debug', console_level='critical')
        
        self.assertNotEqual(log.console_logging_level, log.CRITICAL)
        self.assertNotEqual(log.file_logging_level, log.DEBUG)
        
        
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
