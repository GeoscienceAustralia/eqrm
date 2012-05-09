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

from eqrm_code import perf

# SETUP - You must toggle these to suite your requirements
        
reset_seed = True     # True (to reset the seed) or
                        # False (to use time to set the seed).
                        
compress_output = False # True (to compress the output) or
                        # False (to save outputs as txt files)

def run_batch():
    print 'STARTING BATCH PERFTEST'

    # list of input parameter files to use in the batch run
    run_names = [
        # probabilistic hazard, very few events (1 attenuation model)
        'setdata_ProbHaz.py',
        # scenario ground motion (1 attenuation model)
        'setdata_ScenGM.py',
        # scenario loss simulation (1 attenuation model)
        'setdata_ScenRisk.py',
        # sceario loss simulation
        #(multiple attenuation models - not collapsed)
        'setdata_ScenRisk2.py',
        # probabilistic hazard (1 attenuation model)
        'setdata_ProbHaz.py',
        # probablistic risk (1 attenuation model)
        'setdata_ProbRisk.py',    
        ]


    print 'Parameter file names = ',run_names

    for run in run_names:
        # loop over all the input parameter files
        #(i.e. loop over different simulations)
        print '============================\n============================'
        print 'Doing ', run
        
        run_analysis(setdata=run)
        
        
        print 'FINISH'
    
    print 'FINISH BATCH PERFTEST'

@perf.stats
def run_analysis(setdata=None):
    
    try:
        # import main (i.e. this is basically eqrm_analysis.py)
        from eqrm_code import analysis
    except:
        raise ImportError(
            'Please edit the PYTHONPATH ' + \
            'environmental variable to point to the python_eqrm directory.')
    
    if setdata is not None:
        # run the EQRM with the next input parameter file
        analysis.main(setdata,reset_seed,compress_output)
    

if __name__ == '__main__':
    run_batch()
