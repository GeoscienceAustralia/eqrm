"""
Read the multi run logs and predict the memory used.
"""

import os

from eqrm_code.ANUGA_utilities.log_analyser import build_log_info
from eqrm_code.parse_in_parameters import eqrm_data_home

from eqrm_code.estimator import estimate_mem_log_format
from eqrm_code.ANUGA_utilities.log import EVENTS_J, MAXGMPE_J, BLOCKSITES_J, \
    PARALLELSIZE_J, TOTALMEM_J, INITIAL_J, LOOPING_J, MEM_J, RECMOD_J

MB2B = 1048576.

def create_meta_log():
    path = os.path.join(eqrm_data_home(), 'test_national', 
                                    #      'memory_output') 
                                         'memory_output_risk')
    log_pairs = build_log_info(path) 
    #print "len(log_pairs)", len(log_pairs)

    log_pairs_estimate_mem(log_pairs)

    
    
def log_pairs_estimate_mem_old(log_pairs):
    """
    Given a list of dictionaries of log information estimate the memory
    used, in MB. Add the esimate to the log pairs.
    
    Comparing the old and new estimates after the first memory change.
    
    args;
    log_pairs 
    """
    for log_pair in log_pairs:
        print "---------------------"
        print log_pair["output_dir"]
        mem_b, new_mem_b = estimate_mem_log_format(log_pair)
        total_mem_b = sum(mem_b.itervalues())

        for key, value in mem_b.iteritems():
            print 'array % ' + key + ' ' + str(
                value/float(total_mem_b)*100.) + '%' 
        print "After change"
        total_new_mem_b = sum(new_mem_b.itervalues())
        for key, value in new_mem_b.iteritems():
            print 'new array % ' + key + ' ' + str(
                value/float(total_new_mem_b)*100.) + '%' 
        
        actual_mem_MB = log_pair[LOOPING_J + MEM_J] -\
            log_pair[INITIAL_J + MEM_J]
        print "actual_mem_MB",actual_mem_MB
        print "old estimate total_mem_MB", total_mem_b/MB2B
        print "new estimate total_mem_MB", total_new_mem_b/MB2B
        for key, value in log_pair.iteritems():
            if mem_b.has_key(key):
                estimate_b = mem_b[key]
                if not estimate_b == value:
                    print log_pair["output_dir"]
                    print "*********************"
                    print "key",key
                    print "estimate_elements", estimate_b/8
                    print "actual elements", value/8 
                    
#-------------------------------------------------------------
if __name__ == "__main__":
    create_meta_log()
