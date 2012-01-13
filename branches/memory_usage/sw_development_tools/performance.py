"""
Title: demo_batchmem.py

  Author:  Ben Cooper, ben.cooper@ga.gov.au

  Description: Runs a list of parameter files, gathering
  runtime stats and appending them to a csv file.

  Version: $Revision:  $
  ModifiedBy: $Author:  $
  ModifiedDate: $Date:  $

  Copyright 2012 by Geoscience Australia
"""

import time, datetime
from optparse import OptionParser

try:
    # import main (i.e. this is basically eqrm_analysis.py)
    from eqrm_code import analysis, perf
except:
    raise ImportError(
        'Please edit the PYTHONPATH ' + \
        'environmental variable to point to the python_eqrm directory.')

# SETUP - You must toggle these to suite your requirements
        
reset_seed = True     # True (to reset the seed) or
                        # False (to use time to set the seed).
                        
compress_output = False # True (to compress the output) or
                        # False (to save outputs as txt files) 

@perf.stats
def run_analysis(setdata=None):
    print 'STARTING PERFORMANCE TEST'

    print 'Setdata file name = ',setdata

    if setdata is not None:
        # loop over all the input parameter files
        #(i.e. loop over different simulations)
        print '============================\n============================'
        print 'Doing ', setdata
        
        # run the EQRM with the next input parameter file
        analysis.main(setdata,reset_seed,compress_output)
        
        print 'FINISH'
    
    print 'FINISH PERFORMANCE TEST'
    

if __name__ == '__main__':
    
    # Command line options
    parser = OptionParser()
    parser.add_option('-s', '--setdata', dest='setdata', help='Setdata file to use (if not specified a default batch will run')
    (options, args) = parser.parse_args()
    
    run_analysis(options.setdata)
