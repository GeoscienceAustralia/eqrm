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
import numpy

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print "Import Error;  simplejson not installed."
        print "Install simplejson, or use Python2.6 or greater."
        import sys; sys.exit(1)
        
    

 




from eqrm_code.get_version import get_version

DefaultConsoleLogLevel = logging.INFO
DefaultFileLogLevel = logging.DEBUG


# Terms used in the json dictionary
IOWAIT_J = 'iowait %'
MEM_J = 'memory MB'
RESMEM_J = 'resident MB'
STACKSIZE_J = 'stacksize MB'
TOTALMEM_J = 'total memory MB'
FREEMEM_J = 'free memory MB'
SVNVERSION_J = 'SVN version'
SVNDATE_J = 'SVN date'
SVNMODIFIED_J = 'SVN modified'
HOSTNAME_J = 'host name'
PARALLELSIZE_J = 'Parallel size'
PLATFORM_J = 'System platform'
PRESITELOOP_J = 'time_pre_site_loop_fraction'
EVENTLOOPTIME_J = 'event_loop_time_seconds'
CLOCKTIMEOVERALL_J = 'clock_time_taken_overall_seconds'
WALLTIMEOVERALL_J = 'wall_time_taken_overall_seconds'


DELIMITER_J = 'JS*N'

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

# Log level override flag for set_log_level
allow_level_override = True

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
INCREMENT = 10 


# set _new_python to True if python version 2.5 or later
_new_python = (sys.version_info >= 0x02050000)      # 2.5.x.x
#_new_python = False  # To avoid conflicts, since shapely uses the logger,
# but mname is not defined in extras.

if _new_python:
    FMT = '%(asctime)s %(levelname)-8s %(mname)25s:%(lnum)-4d|%(message)s'
else:
    FMT = '%(asctime)s %(levelname)-8s |%(message)s'

def _proc_stat():
    if sys.platform != 'win32':
        try:
            stat_fd = open('/proc/stat')
            stat_buf = stat_fd.readlines()[0].split()
            stat_fd.close()
        except IOError:
            stat_buf = [0.0]*8
    else:
        stat_buf = [0.0]*8
    #  user, nice, syst, idle, wait, irq, sirq
    return ( float(stat_buf[1]), float(stat_buf[2]), 
          float(stat_buf[3]), float(stat_buf[4]),
          float(stat_buf[5]), float(stat_buf[6]),
          float(stat_buf[7]) )

user, nice, syst, idle, wait, irq, sirq = _proc_stat()
    
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
    
    # Reinitialise the log
    _reinitialise(level)

def set_log_level(level, console_level=None):
    """
    Set up or change log level.
    
    level == string representation of log level. i.e.
    
    'critical' = logging.CRITICAL 
    'error' = logging.ERROR 
    'warning' = logging.WARNING 
    'info' = logging.INFO 
    'debug' = logging.DEBUG 
    
    file_logging_level = level
    
    If console_level is None, console_logging_level becomes the next quietest.
    i.e.
    console_logging_level = level + 10 (increment between above levels)
    
    e.g.
    level = 'info', console_level = None
    file_logging_level = logging.INFO
    console_logging_level = logging.WARNING
    
    Note: If console_logging_level and file_logging_level have already been
    set outside this module, this will not do anything. e.g. check_scenarios.py
    """
    global console_logging_level, file_logging_level
    
    if allow_level_override:
        # File logging level
        numeric_level = getattr(logging, level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % level)
        file_logging_level = numeric_level
        
        # Console logging level
        if console_level is None:
            console_logging_level = numeric_level + INCREMENT
        else:
            numeric_console_level = getattr(logging, console_level.upper(),
             None)
            if not isinstance(numeric_console_level, int):
                raise ValueError('Invalid console log level: %s'\
                 % console_level)
            console_logging_level = numeric_console_level
        
        # sanity check the logging levels, require console >= file
        if file_logging_level > console_logging_level:
            file_logging_level = console_logging_level
        
        # Reinitialise the log
        _reinitialise(file_logging_level)

def _reinitialise(level=None):
    # Initialise (or reinitialise) the logs
    if _setup is False:
        _initialise(level=level)
    else:
        logger.removeHandler(log_file_hdlr)
        logger.removeHandler(console) 
        logger.setLevel(file_logging_level)
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

def log_json(dic, level):
    """
    Convert a dictionary to a log message with the end of the message
    using the JSON format.
    """
    msg = DELIMITER_J + json.dumps(dic)
    log(msg, level)
    

def resource_usage(level=logging.DEBUG):   
    iowait = _calc_io_wait()
    results = _calc_resource_usage_mem()
    results.update(iowait) # 
    log_json(results, level)
   
   
def log_svn(level=logging.INFO):  
    version, date, modified = get_version()
    svn_dic = {SVNVERSION_J:version,
               SVNDATE_J:date,
               SVNMODIFIED_J: modified}
    
    
def _eqrm_flags_simple(dic):
    """
     If the value is a list or array, change it to len(value) and 
     add '_len' to the key.
     This function returns a new dic object. 
    """
    res = {}
    for k, v in dic.iteritems():
        if isinstance(v, list) or isinstance(v, numpy.ndarray):
            res['len_' + str(k)] = len(v) 
        else:   
            res[k] = v
    return res
    
    
def log_eqrm_flags_simple(eqrm_flags, level=logging.DEBUG):
    """
    Add the EQRM flags to the log file.
    
    Some modifications are made to simplify the data being logged;
    If the value is a list, log len(value) and add '_len' to the key. 
    """
    simple_flags = _eqrm_flags_simple(eqrm_flags)
    log_json(simple_flags, level)
    
    

def _calc_io_wait():
    """
    Calc the io_wait percentage.

    WARNING: This result is based on what the CPU has been doing
    Since the last time this function was called, or when this module 
    was loaded, for the first function call.
    """
    
    # The results from the last call
    global user, nice, syst, idle, wait, irq, sirq

    user_n, nice_n, syst_n, idle_n, wait_n, irq_n, sirq_n = _proc_stat()

    user_d = user_n - user
    nice_d = nice_n - nice
    syst_d = syst_n - syst
    idle_d = idle_n - idle
    wait_d = wait_n - wait
    irq_d = irq_n - irq
    sirq_d = sirq_n - sirq
    
    cact = user_d + syst_d + nice_d 
    ctot = user_d + nice_d + syst_d + idle_d + wait_d + irq_d + sirq_d 

    user = user_n
    nice = nice_n
    syst = syst_n
    idle = idle_n
    wait = wait_n
    irq = irq_n
    sirq = sirq_n
    if ctot == 0.0:
        wcpu = None
    else:
        wcpu = wait_d/ctot*100
    return {IOWAIT_J: wcpu}
    

def _calc_resource_usage_mem():
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
        
        return {MEM_J:memory()/_scale['MB'], 
                RESMEM_J:resident()/_scale['MB'],
                STACKSIZE_J:stacksize()/_scale['MB']}
    else:
        # Windows code from: http://code.activestate.com/recipes/511491/
        try:
            import ctypes
            import _winreg
        except:
            return {}

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

        return {TOTALMEM_J:memoryStatusEx.ullTotalPhys/_scale['MB'],
         FREEMEM_J:memoryStatusEx.ullAvailPhys/_scale['MB']}


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
