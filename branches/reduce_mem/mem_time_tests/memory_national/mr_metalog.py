"""
Read the multi run logs and predict the memory used.
"""

import os

from eqrm_code.ANUGA_utilities.log_analyser import build_log_info #analyse_log, merge_dicts, LOGFILE
from eqrm_code.parse_in_parameters import eqrm_data_home

from eqrm_code.estimator import log_pairs_estimate_mem

def create_meta_log():
    path = os.path.join(eqrm_data_home(), 'test_national', 
                                          'memory_output') 
                                   #      'memory_output_too_much')
    log_pairs = build_log_info(path) 
    print "len(log_pairs)", len(log_pairs)

    log_pairs_estimate_mem(log_pairs)

#-------------------------------------------------------------
if __name__ == "__main__":
    create_meta_log()
