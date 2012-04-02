
import logging

if False:
    LOG_FILENAME = 'ogging_example.out'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    
    logging.debug('This message should go to the log file')
    
    LOG_FILENAME = 'bogging_example.out'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    
    logging.debug('And This message should go to another log file')

    logger = logging.getLogger('myapp')
    hdlr = logging.FileHandler('myapp.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    
    logger.info('a log message')
    
    
    hdlr2 = logging.FileHandler('qmyapp.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr2.setFormatter(formatter)
    logger.addHandler(hdlr2)
    logger.removeHandler(hdlr)
    
    logger.info('a log message that goes to 2 files')
    
"""
Requirement
Get it going on one process first.
Only one log file per process.  The ouput of the log file can be changed.

Usage.
Init log in Analysis.  Use borg so it is only inited once per process.
Have a set log file  that changes where the output file name.

Have more levels?
Not yet.

"""

import os
import sys
import traceback
import logging

DefaultConsoleLogLevel = logging.INFO
DefaultFileLogLevel = logging.DEBUG

# logging level for the console
console_logging_level = DefaultConsoleLogLevel

# logging level for the logfile
file_logging_level = DefaultFileLogLevel

# set module variables so users don't have to do 'import logging'.
CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

global _setup

def initialise_logging(log_file_path=None):
    """
    """
    
    if not _setup:
        # sanity check the logging levels, require console >= file
        if file_logging_level > console_logging_level:
            file_logging_level = console_logging_level

        # define a console handler which writes to sys.stdout
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(console_logging_level)
        formatter = logging.Formatter('%(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

        # Add the logging of exceptions, see Rosses code.
        #FIXME
        
        # tell the world how we are set up
        start_msg = ("Logfile is '%s' with logging level of %s, "
                     "console logging level is %s"
                     % (log_filename,
                        logging.getLevelName(file_logging_level),
                        logging.getLevelName(console_logging_level)))
        
        # mark module as *setup*
        _setup = True

        
def log(msg, level=None):
