

"""
Test logging and estimating memory use.
"""
import os

import numpy

from eqrm_code.ANUGA_utilities import log

#from eqrm_code.ANUGA_utilities.log import EVENTS_J, MAXGMPE_J, BLOCKSITES_J, \
 #   PARALLELSIZE_J, TOTALMEM_J

def big_array():
    
    # set up the logging
    log_filename = os.path.join('.',
                                'log-0.txt')
    log.log_filename = log_filename
    log.remove_log_file()
    log.set_log_level('DEBUG')
    log.resource_usage(tag=log.INITIAL_J)
    



#-------------------------------------------------------------
if __name__ == "__main__":
    big_array()
