

"""
Test logging and estimating memory use.
"""
import os
import shutil
import tempfile

import numpy

from eqrm_code.ANUGA_utilities.log_analyser import build_log_info
from eqrm_code import estimator
from eqrm_code.ANUGA_utilities import log
from eqrm_code.ANUGA_utilities import log_analyser

# from eqrm_code.ANUGA_utilities.log import EVENTS_J, MAXGMPE_J, BLOCKSITES_J, \
 #   PARALLELSIZE_J, TOTALMEM_J
# os.path.join('.', 'spike_estimator')
DIRPATH = tempfile.mkdtemp('spike_estimator')


def big_array(elements, dtype=float):

    # set up the logging
    log_filename = os.path.join(DIRPATH,
                                'log-0-' + str(elements) + '.txt')
    log.log_filename = log_filename
    log.remove_log_file()
    log.set_log_level('DEBUG')
    log.resource_usage(tag=log.INITIAL_J)
    array_mem = numpy.zeros([elements], dtype=dtype)
    log.resource_usage(tag=log.FINAL_J)
    dic = {"actual_mem MB": array_mem.nbytes / estimator.MB2B,
           "elements": elements}
    log.log_json(dic, log.DEBUG)


def big_arrays():
    for elements in [100000, 1000000, 10000000, 100000000]:
        big_array(elements)


def write_check():
    big_arrays()
    log_pairs = build_log_info(DIRPATH)
    for log_pair in log_pairs:
        logged_mem_mb = log_pair['final_memory MB'] - \
            log_pair['initial_memory MB']
        print '******************'
        print "logged_mem_mb", logged_mem_mb
        print "actual_mem MB", log_pair['actual_mem MB']
        if not logged_mem_mb == 0:
            print "diff %", ((logged_mem_mb - log_pair['actual_mem MB'])
                             / log_pair['actual_mem MB'] * 100.)

    shutil.rmtree(DIRPATH)


#-------------------------------------------------------------
if __name__ == "__main__":
    write_check()
