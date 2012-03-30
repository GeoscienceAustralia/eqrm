"""
Created on 11/01/2012

@author: Ben Cooper, ben.cooper@ga.gov.au

Decorators and functions to assist in gathering performance statistics

Adapted from the 'timeit' example shown by Dr. Graeme Cross at PyConAU 2011
https://bitbucket.org/gjcross/talks/history/PyCon_AU_2011/Decorators/Examples/timeit.py
"""

import csv
import os
import socket
import sys
import time, datetime
from functools import wraps
from eqrm_code.get_version import get_svn_revision_sandpit_linux
from eqrm_code.ANUGA_utilities import log

default_csv_file = 'perf.csv'

# From Python's libs/timeit.py
if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms, the best timer is time.time()
    default_timer = time.time
    
def timeit(func):
    '''Print how long the function took (in milliseconds)'''
    @wraps(func)
    def wrapper(*args, **kw):
        t0 = default_timer()
        result = func(*args, **kw)
        tdiff_msecs = 1000 * (default_timer() - t0)
        print "%s(%s) time = %0.2f msecs" % (func.__name__ , str(*args), tdiff_msecs)
        return result
    return wrapper

def stats(func):
    '''Gather some key performance statistics from the running function
    
    Output:
        - SVN revision
        - Start datetime
        - End datetime
        - Overall running time (secs)
        - Collection of resource_usage data points throughout application
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        # Timing
        t0 = default_timer()
        
        # Run the wrapped function
        result = func(*args, **kwargs)
        
        t1 = default_timer()
        tdiff = (t1 - t0)
        #print "STATS %s(%s) Time start %s" %(func.__name__, str(*args), datetime.datetime.fromtimestamp(t0).isoformat(' '))
        #print "STATS %s(%s) Time end %s" %(func.__name__, str(*args), datetime.datetime.fromtimestamp(t1).isoformat(' '))
        #print "STATS %s(%s) Running time=%s" % (func.__name__, str(*args), str(tdiff))
        
        # If the log file does not exist then analysis.main probably
        # exited with an error. No point in gathering stats at this stage
        if os.path.exists(log.log_filename):
        
            # Subversion revision
            commit, _, url = get_svn_revision_sandpit_linux()
            #print "STATS %s(%s) SVN version=%s date=%s modified=%s" % (func.__name__, str(*args), version, date, modified)
            
            # hostname from socket library
            hostname = socket.gethostname()
            
            # Log analysis
            memory_usage_locations = log_analysis()
            #print "STATS %s(%s) Output=%s" % (func.__name__, str(*args), memory_usage_locations)
            
            # Append to CSV file (use the current logfile output directory)
            # Note: analysis.main changes the value of log.log_filename per setdata file
            output_dir = os.path.dirname(log.log_filename)
            #print "STATS %s(%s) Output=%s" % (func.__name__, str(*args), output_dir)
            
            # Headers
            header_list = None
            if not os.path.exists(os.path.join(output_dir, default_csv_file)):
                header_list = ['revision', 'url', 'hostname', 'start', 'end', 'running time']
                header_list.extend([k for (k,v) in memory_usage_locations])
            
            # Data
            data_list = [commit,
                         url,
                         hostname,
                         datetime.datetime.fromtimestamp(t0).isoformat(' '),
                         datetime.datetime.fromtimestamp(t1).isoformat(' '),
                         str(tdiff)]
            data_list.extend([v for (k,v) in memory_usage_locations])
            
            fd = open(os.path.join(output_dir, default_csv_file), 'a')
            writer = csv.writer(fd)
            
            # Write the header if file does not already exist
            if header_list:
                writer.writerow(header_list)
                
            # Write the data
            writer.writerow(data_list)
            
            fd.close()
            
            print "STATS %s(%s) Wrote to performance file %s" % (func.__name__, str(*args), os.path.join(output_dir, default_csv_file))
        
        return result
    
    return wrapper

def log_analysis():
    '''log_analysis - analyses the current log and returns a tuple list containing
    - Memory usage 'event' key
    - Memory usage data value
    
    It makes the assumption that the current pattern for logging memory usage 
    is consistent. e.g.
    
    log.debug('Memory: event_set_zone created')
    log.resource_usage()
    
    This will produce lines in the log file that looks like
    2012-01-12 13:12:29,694 DEBUG                     analysis:228 |Memory: event_set_zone created
    2012-01-12 13:12:29,695 DEBUG                     analysis:229 |Resource usage: memory=1151.0MB resident=758.2MB stacksize=0.3MB
    
    What we want from this example is a tuple that looks like
    ('event_set_zone created', 'memory=1151.0MB resident=758.2MB stacksize=0.3MB')
    
    Where the 'event' key is the 'Memory:' log reference and the data value is the
    'Resource usage:' log reference.
    '''
    
    results = []
    
    # Only do this is the logfile exists
    if os.path.exists(log.log_filename):
        # 1. Determine logfile for the previous run
        # Note: analysis.main changes the value of log.log_filename per setdata file
        log.info('log_analysis - using log file %s' % log.log_filename)
        log_file = open(log.log_filename)
        
        # 2. Grab the Memory/Resource lines in a tuple
        for line in log_file:
            if line.find('Memory:') > -1:
                key_line = line
                value_line = log_file.next()
                
                # This assumes the current pattern will always be
                _, key = key_line.split('Memory: ', 1)
                _, value = value_line.split('Resource usage: ', 1)  
                
                # We want to preserve order so cannot use a dict        
                results.append((key.strip(), value.strip()))
        
        log_file.close()
    
    # 3. Return tuple array
    return results
