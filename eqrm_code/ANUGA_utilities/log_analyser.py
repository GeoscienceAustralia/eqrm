import sys
import os
import re
import csv
import ConfigParser
import StringIO

import datetime
import time

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        print "Import Error.  simplejson not installed."
        print "Install simplejson, or use Python2.6 or greater."
        import sys; sys.exit(1)

from eqrm_code.ANUGA_utilities.log import DELIMITER_J
from eqrm_code.ANUGA_utilities import log


OUTPUTFILE = 'timing.csv'
LOGFILETAG = 'log-0'
NCIEFILETAG = '.OU'
JOBIDNCI = 'JobId'

def analyse_log(path, output_file, log_file=LOGFILETAG):
    """
    Read all the logs and write a meta_log_csv file.

    args
    path - the directory to look for log files in.
    log_file - the standard logfile name.     
    """
    log_pairs = build_log_info(path, log_file)
    if log_pairs is not None:
        write_meta_log(log_pairs, output_file)

        
def merge_dicts(d1, d2, merge=lambda x,y:max(x,y)):
    """
    Merges two dictionaries, non-destructively, combining 
    values on duplicate keys as defined by the optional merge
    function.  The default behavior replaces the values in d1
    with corresponding values in d2.  (There is no other generally
    applicable merge strategy, but often you'll have homogeneous 
    types in your dicts, so specifying a merge technique can be 
    valuable.)

    by: rcreswick
    
    from: http://stackoverflow.com/questions/38987/
    how-can-i-merge-union-two-python-dictionaries-in-a-single-expression
    
    Examples:

    >>> d1
    {'a': 1, 'c': 3, 'b': 2}
    >>> merge(d1, d1)
    {'a': 1, 'c': 3, 'b': 2}
    >>> merge(d1, d1, lambda x,y: x+y)
    {'a': 2, 'c': 6, 'b': 4}

    """
    result = dict(d1)
    for k,v in d2.iteritems():
        if k in result:
            result[k] = merge(result[k], v)
        else:
            result[k] = v
    return result
   
   
def read_log_json(a_file):
    """
    Parse the json info in the log file and return a dictionary of the info
    if a value is found multiple times the maximum value is returned.
    """
    alog = {}
    for line in open(a_file):
        if line.find(DELIMITER_J)>-1:
            json_string = line.split(DELIMITER_J)[1]
            results = json.loads(json_string)
            if isinstance(results, dict):
                alog = merge_dicts(alog, results, 
                                   merge=lambda x,y:max(x,y))
            else:
                # raise error
                pass
    return alog
         
         
def build_log_info(path, log_file=LOGFILETAG):
    """
    Read 1 or more log files and collate the json dictionary 
    part of the log file into a list, with each element of the list
    being the results of a log file.
    
    The results of the log file will be a dictionary.
    The key will be a string, such as 'memory MB'
    The value will be the maximum value for that string in each log file.
    """
    
    log_pairs = []
    for (path, dirs, files) in os.walk(path):    
        for a_file in files:
            if log_file in a_file: 
                path_file = os.path.join(path, a_file)
                alog = read_log_json(path_file)
                if not alog == {}:
                    log_pairs.append(alog)
    return log_pairs
  
  
def write_meta_log(log_pairs, output_file):
    """Write the info from the log files to a file
    
    args
    log_pairs - a list of log dictionaries.
    """
    
    all_keys = {} # values aren't needed, but are there
    for log_p in log_pairs:
        all_keys.update(log_p)
                
    # sort the keys alphabetacally
    sorted_all_keys = sorted(all_keys.keys())
    han = open(output_file, 'w')
    writer = csv.DictWriter(han, delimiter=',', 
                            fieldnames=sorted_all_keys,
                            extrasaction='ignore')
    # Title 
    writer.writerow(dict(zip(sorted_all_keys, sorted_all_keys)))
    
    for pair in log_pairs:
        writer.writerow(pair)       
    han.close()
    
    
def add_nci_info2log(path, log_file_tag=LOGFILETAG, nci_file_tag=NCIEFILETAG):
    """
    Add info from an NCI .vu-pb.OU (standard out) file to a log file. 
    Assumes the log and nci file are in the same directory.

    """
    nci_log_pairs = find_nci_log_pairs(path, log_file_tag, nci_file_tag)
    for log_file, nci_file in nci_log_pairs:
        nci_dic = get_nci_value_pairs(nci_file)
        with open(log_file, "a") as myfile:
            myfile.write(DELIMITER_J + json.dumps(nci_dic))
        
    
def colon_time2sec(colon_time):
    """
    Convert a time string like '00:01:04' to 64 seconds.
    
    http://stackoverflow.com/questions/10663720/
    converting-a-time-string-to-seconds-in-python
    """
    x = time.strptime(colon_time,'%H:%M:%S')
    delta = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,
                               seconds=x.tm_sec)
    return delta.total_seconds()

        
def get_nci_value_pairs(nci_e_file):
    """
    Parse the NCI output. Add units to the keys.  Remove the units
    from the values.
    
    Returns:
      A dictionary of NCI info, such as 'CPU time (sec)' and 'JobId', 
      with values.
      OR
      {} if it can't find the '=======================' to signify nci data.
    """
    f = open(nci_e_file, 'rU')
    nci_info = []
    reading = False
    for line in f.readlines():
        if '=======================' in line:
            if reading == False: 
                reading = True
            else:
                reading = False
        else:
            if reading:
                nci_info.append(line)
    #print "nci_info", nci_info
    if nci_info == []:
        # Not really an NCI file
        return {}
        
    nci_info.pop(0) # get rid of the  Resource usage: line   
    nci_dic = {}
    
    job_split = nci_info[1].split('JobId:')
    nci_dic['JobId'] = job_split[1][:26].strip()
    
    job_split = nci_info[2].split('Project:')
    nci_dic['Project'] = job_split[1][:26].strip()
    
    nci_mapping = [(0, 'CPU time:'), (1, 'Elapsed time:'), 
                   (2, 'Requested time:')] 
    for pair in nci_mapping:
        a_split = nci_info[pair[0]].split(pair[1])
        nci_dic[pair[1][:-1] + ' (sec)'] = colon_time2sec(a_split[1].strip())
        
    # from here on ':' can be used as a delimiter
    for line in nci_info[3:]:
        a_split = line.split(':')
        if len(a_split) > 1:
            value = a_split[1].strip()
            if value[-2:] == 'GB' or  value[-2:] == 'MB':
                unit = value[-2:]
                nci_dic[a_split[0].strip() + ' (' + unit + ')'] = \
                    float(value[:-2])
            else:
                nci_dic[a_split[0].strip()] = float(value)    
    return nci_dic
            
            
def newest_file_in_list(files):
    """
    Given a list of files return the most recent file
    """
    max_datetime = 0
    max_file = None
    for a_file in files:
        (_, _, _, _, _, _, _, _, mtime, ctime) = os.stat(a_file)
        if mtime > max_datetime:
            max_datetime = mtime
            max_file = a_file
    return max_file
    
    
def find_nci_log_pairs(path, log_file_tag, nci_file_tag):
    """
    Find nci and log files in the path sub directories.  Only return
    pairs where the log file has no 'JobId', so info is not added
    multiple times.
    
    Returns:
    A list of (log_file, nci_file) tuples.
    
    """
    dirs_with_logs = []
    for (path, dirs, files) in os.walk(path):
        for a_file in files:
            if log_file_tag in a_file: 
                dirs_with_logs.append([path, a_file])
    # assume one log file in each dir
    # multiple nci_files may be in a log dir
    nci_log_pairs = []
    for dir_with_log, log_file in dirs_with_logs:
        files_dirs = os.listdir(dir_with_log)
        nci_files = []
        log_file = os.path.join(dir_with_log, log_file)
        # If the log has a JobId associated with it assume the nci info has
        # already been added to the log
        log_dic = read_log_json(log_file)
        if JOBIDNCI in log_dic:
            # The nci info is already in the log file
            continue 
            
        for a_file in files_dirs:
            if nci_file_tag in a_file:
                nci_file = os.path.join(dir_with_log, a_file)
                nci_files.append(nci_file)
        if not nci_files == []:
            nci_file = newest_file_in_list(nci_files)
            nci_log_pairs.append((log_file, nci_file))
    return nci_log_pairs
 
####################################################
if __name__ == '__main__':
    """
    usage is;
    log_analyser [path] [outputFile]
    """
    
    if len(sys.argv) < 2:
        path = '.'
    else:
        path = sys.argv[1]
        
    if not os.path.exists(path):
        sys.exit('ERROR: path %s was not found!' % path)    
        
    if len(sys.argv) < 3:
        outputFile = defaultOutputFile
    else:
        outputFile = sys.argv[2]

    analyse_log(path, outputFile)
