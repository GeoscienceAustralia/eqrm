#!/usr/bin/env python

"""
A logging module that logs to the console and a logfile, and has a
configurable threshold loglevel for each of console and logfile output.

Use it this way:
    from eqrm_code.ANUGA_utilities import log

    # configure my logging
    log.console_logging_level = log.INFO
    log.file_logging_level = log.DEBUG
    log.log_filename = './my.log'

    # log away!
    log.debug('A message at DEBUG level')
    log.info('Another message, INFO level')

This has been designed to log for EQRM.  Using this code to log a program
that calls EQRM will result in chaos.  So don't.

Known Bugs
- If you call EQRM and then try to delete the log file a WindowsError will be
  raised, in Windows.  

This class uses the 'borg' pattern - there is never more than one instance
of log data.  See the URL for the basic idea used here: modules *are*
singletons!

<http://www.suttoncourtenay.org.uk/duncan/accu/pythonpatterns.html>

Until the first call to log() the user is free to play with the module data
to configure the logging.

Note that this module uses some features of the logging package that were
introduced in python2.5.  If running on earlier versions, the following
features are disabled:
    . Calling module name + line number
"""
"""
from http://plumberjack.blogspot.com/2009/09/python-logging-101.html
Levels

By default, there are five levels of importance associated with
logging events. Experience has shown that having more levels is
unhelpful, since the choice of which level to assign to an event
becomes subjective. The five levels are DEBUG, INFO, WARNING, ERROR
and CRITICAL. Their significance is described in the following table.

DEBUG Detailed information, of no interest when everything is working
well but invaluable when diagnosing problems.

INFO Affirmations that things are working as expected, e.g. "service
has started" or "indexing run complete". Often ignored.

WARNING There may be a problem in the near future, and this gives
advance warning of it. But the application is able to proceed
normally.

ERROR The application has been unable to proceed as expected, due to
the problem being logged.

CRITICAL This is a serious error, and some kind of application
meltdown might be imminent.

"""

import os
import sys
import traceback
import logging

DefaultConsoleLogLevel = logging.INFO
DefaultFileLogLevel = logging.DEBUG


################################################################################
# Module variables - only one copy of these, ever.
#
# The console logging level is set to a high level, like CRITICAL.  The logfile
# logging is set lower, between DEBUG and CRITICAL.  The idea is to log least to
# the console, but ensure that everything that goes to the console *will* also
# appear in the log file.  There is code to ensure log <= console levels.
#
# If console logging level is set to CRITICAL+1 then nothing will print on the
# console.
################################################################################

# flag variable to determine if logging set up or not
_setup = False

# logging level for the console
console_logging_level = DefaultConsoleLogLevel

# logging level for the logfile
file_logging_level = DefaultFileLogLevel

# If a log message does not have a level, set it to the console level
default_to_console = True

# The default name of the file to log to.
log_filename = os.path.join('.', 'EQRM.log')

# Log file handler
log_file_hdlr = None
console = None
logger = None

# set module variables so users don't have to do 'import logging'.
CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

# set _new_python to True if python version 2.5 or later
_new_python = (sys.version_info >= 0x02050000)      # 2.5.x.x
#_new_python = False  # To avoid conflicts, since shapely uses the logger,
# but mname is not defined in extras.

if _new_python:
    FMT = '%(asctime)s %(levelname)-8s %(mname)25s:%(lnum)-4d|%(message)s'
else:
    FMT = '%(asctime)s %(levelname)-8s |%(message)s'
    
##############################################################################
# Module code.
###############################################################################

#FIXME turn into a class

def log(msg, level=None):
    """Log a message at a particular loglevel.

    msg:    The message string to log.
    level:  The logging level to log with (defaults to console level)
            or just below console level, based on default_to_console.

    The first call to this method (by anybody) initializes logging and
    then logs the message.  Subsequent calls just log the message.
    """

    # if logging level not supplied, assume console level
    if level is None:
        if default_to_console is True:
            level = console_logging_level
        else:
            level = console_logging_level -1

    _initialise(level=level)
    
    # get caller information - look back for first module != <this module name>
    frames = traceback.extract_stack()
    frames.reverse()
    try:
        (_, mod_name) = __name__.rsplit('.', 1)
    except ValueError:
        mod_name = __name__
    for (fpath, lnum, mname, _) in frames:
        (fname, _) = os.path.basename(fpath).rsplit('.', 1)
        if fname != mod_name:
            break 
    
    if _new_python:
        logging.log(level, msg, extra={'mname': fname, 'lnum': lnum})
    else:
        # The problem with this is it goes to
        # the screen as well. Not so bad. Untill in imp testing it is checking
        # file names and line numbers.  
        #file_stamp = '%25s:%-4d' % (fname, lnum)
        #msg = file_stamp + '|' +msg
        logging.log(level, msg)


def set_log_file(new_log_filename, level=None):
    """
    Set up or change the location of the log file.
    """
    global log_filename
    
    log_filename = new_log_filename
    if _setup is False:
        _initialise(level=level)
    else:
        logger.removeHandler(log_file_hdlr)

        # This helps the tests to pass
        logger.removeHandler(console) 
        _add_console_handler(logger)
        _add_file_handler(logger)
        _start_msg(level=level)


def remove_file_handler():
    """
    Stop logging to a file.
    """
    logger.removeHandler(log_file_hdlr)


def remove_log_file():
    """
    If a log file is present, delete it.
    """
    
    try:
        os.remove(log_filename)
    except OSError: #WindowsError:
        pass

def _initialise(level=None):
    
    global _setup, file_logging_level, logger

    # have we been setup?
    if not _setup:
        # sanity check the logging levels, require console >= file
        if file_logging_level > console_logging_level:
            file_logging_level = console_logging_level

        # setup the file logging system
        logger = logging.getLogger('')
        logger.setLevel(file_logging_level)

        _add_console_handler(logger)

        # catch exceptions
        sys.excepthook = _log_exception_hook

        # mark module as *setup*  Doing this after _add_file_handler
        # will result in a recursive loop
        _setup = True
        
        _add_file_handler(logger)
        _start_msg(level=level)
        

def _start_msg(level=None):
    """ tell the world how we are set up
    """
    
    start_msg = ("Logfile is '%s' with logging level of %s, "
                 "console logging level is %s"
                 % (log_filename,
                    logging.getLevelName(file_logging_level),
                    logging.getLevelName(console_logging_level)))
    log(start_msg, level=level)
    

def _add_console_handler(logger):
    """define a console handler which writes to sys.stdout
    """
    global console
    
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(console_logging_level)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)

    
def _add_file_handler(logger):
    """ define a handler which writes to the log file
    """
    global log_file_hdlr
    #print "log_filename",log_filename
    log_file_hdlr = logging.FileHandler(log_filename)
    log_file_hdlr.setLevel(file_logging_level)
    formatter = logging.Formatter(FMT)
    log_file_hdlr.setFormatter(formatter)
    logger.addHandler(log_file_hdlr)

    

def _log_exception_hook(type, value, tb):
    """Hook function to process uncaught exceptions.

    type:   Type of exception.
    value:  The exception data.
    tb:     Traceback object.

    This has the same interface as sys.excepthook().
    """

    msg = '\n' + ''.join(traceback.format_exception(type, value, tb))
    critical(msg)

    
################################################################################
# Shortcut routines to make for simpler user code.
################################################################################

def debug(msg=''):
    """Shortcut for log(DEBUG, msg)."""

    log(msg, logging.DEBUG)


def info(msg=''):
    """Shortcut for log(INFO, msg)."""

    log(msg, logging.INFO)


def warning(msg=''):
    """Shortcut for log(WARNING, msg)."""

    log(msg, logging.WARNING)


def error(msg=''):
    """Shortcut for log(ERROR, msg)."""

    log(msg, logging.ERROR)


def critical(msg=''):
    """Shortcut for log(CRITICAL, msg)."""

    log(msg, logging.CRITICAL)


def resource_usage(level=logging.DEBUG):
    """Log memory usage at given log level."""

    _scale = {'KB': 1024, 'MB': 1024*1024, 'GB': 1024*1024*1024,
              'kB': 1024, 'mB': 1024*1024, 'gB': 1024*1024*1024}

    if sys.platform != 'win32':
        _proc_status = '/proc/%d/status' % os.getpid()
        
        def _VmB(VmKey):
            """Get number of virtual bytes used."""

            # get pseudo file /proc/<pid>/status
            try:
                t = open(_proc_status)
                v = t.read()
                t.close()
            except IOError:
                return 0.0

            # get VmKey line, eg: 'VmRSS: 999 kB\n ...
            i = v.index(VmKey)
            v = v[i:].split(None, 3)
            if len(v) < 3:
                return 0.0

            # convert Vm value to bytes
            return float(v[1]) * _scale[v[2]]

        def memory(since=0.0):
            """Get virtual memory usage in bytes."""

            return _VmB('VmSize:') - since

        def resident(since=0.0):
            """Get resident memory usage in bytes."""

            return _VmB('VmRSS:') - since

        def stacksize(since=0.0):
            """Get stack size in bytes."""

            return _VmB('VmStk:') - since

        msg = ('Resource usage: memory=%.1fMB resident=%.1fMB stacksize=%.1fMB'
               % (memory()/_scale['MB'], resident()/_scale['MB'],
                  stacksize()/_scale['MB']))
        log(msg, level)
    else:
        # Windows code from: http://code.activestate.com/recipes/511491/
        try:
            import ctypes
            import _winreg
        except:
            log(level, 'Windows resource usage not available')
            return

        kernel32 = ctypes.windll.kernel32
        c_ulong = ctypes.c_ulong
        c_ulonglong = ctypes.c_ulonglong
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [('dwLength', c_ulong),
                        ('dwMemoryLoad', c_ulong),
                        ('ullTotalPhys', c_ulonglong),
                        ('ullAvailPhys', c_ulonglong),
                        ('ullTotalPageFile', c_ulonglong),
                        ('ullAvailPageFile', c_ulonglong),
                        ('ullTotalVirtual', c_ulonglong),
                        ('ullAvailVirtual', c_ulonglong),
                        ('ullAvailExtendedVirtual', c_ulonglong)
                       ]

        memoryStatusEx = MEMORYSTATUSEX()
        memoryStatusEx.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatusEx))

        msg = ('Resource usage: total memory=%.1fMB free memory=%.1fMB'
               % (memoryStatusEx.ullTotalPhys/_scale['MB'],
                  memoryStatusEx.ullAvailPhys/_scale['MB']))
        log(msg, level)


################################################################################

if __name__ == '__main__':
    critical('#' * 80)
    warning('Test of logging...')
    log('CRITICAL+1', CRITICAL+1)
    log('CRITICAL', CRITICAL)
    log('CRITICAL-1', CRITICAL-1)
    log('CRITICAL-2', CRITICAL-2)
    log('default - CRITICAL?')

    def test_it(num=100):
        if num > 0:
            test_it(num-1)
        else:
            resource_usage()

    import numpy as num
    
    a = num.zeros((1000,1000), num.float)

    info('sys.version_info=%s, _new_python=%s'
         % (str(sys.version_info), str(_new_python)))
    test_it()