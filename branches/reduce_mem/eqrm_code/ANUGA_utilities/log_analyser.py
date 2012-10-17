import sys
import os
import re
import csv


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
        for file in files:
            if log_file in file: 
                alog = {}
                for line in open(os.path.join(path,file)):
                    if line.find(DELIMITER_J)>-1:
                        json_string = line.split(DELIMITER_J)[1]
                        results = json.loads(json_string)
                        if isinstance(results, dict):
                            alog = merge_dicts(alog, results, 
                                               merge=lambda x,y:max(x,y))
                        else:
                            # raise error
                            pass
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

    
 
