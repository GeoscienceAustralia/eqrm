#!/bin/env python

"""
A module to compute time to complete bridge repairs to a FP given:
    . Functional Percentage (FP)
    . Bridge damage state (slight, moderate, extensive or complete)
    . Mean and sigma values for each damage state (read from file)
"""


import os
import scipy.stats
import numpy

from eqrm_code.util import determine_eqrm_path
import csv_interface as csvi
import eqrm_filesystem


# dictionary containing state -> mean+sigma values
# None means we have yet to load data from external file
MeanSigmaValues = None

# filename the above dictionary is filled from
MeanSigmaValuesCSVFile = 'bridge_state_mean_sigma.csv'

# path to directory for input files
DataFilePath = eqrm_filesystem.Resources_Data_Path


def time_to_complete(fp, state):
    """Return days to completion to given FP for a damage state.

    fp     array of required percentage functionality
    state  bridge damage state
 
    Return number of days as an integer array.
    """

    # make sure we have loaded external data
    # then get mean & sigma values matching the state
    if MeanSigmaValues is None:
        load_external_data()

    state = state.lower()		# ensure lower case
    try:
        (mean, sigma) = MeanSigmaValues[state]
    except KeyError:
        msg = "Bad bridge 'state' string: %s" % state
        raise RuntimeError(msg)

    # do the calculation (convert percentage to fraction first)
    fp_fraction = numpy.array(fp)/100.0
    result = scipy.stats.norm.ppf(fp_fraction, mean, sigma)

    # return integer results, clamped such that value < 1 become 1
    result = numpy.rint(result)		# integer values
    return numpy.where(result < 1, 1, result)


def load_external_data():
    """Load mean and sigma values from an external file."""

    global MeanSigmaValues

    eqrm_dir = determine_eqrm_path(__file__)
    path = os.path.join(eqrm_dir,
                        eqrm_filesystem.Resources_Data_Path,
                        MeanSigmaValuesCSVFile)
    MeanSigmaValues = csvi.csv2rowdict(path,
                                       columns=['State', 'Mean', 'Sigma'],
                                       convert={'Mean': float,
                                                'Sigma': float })


################################################################################

if __name__ == '__main__':
    fp = numpy.array([0.1, 0.5])
    state = 'slight'
    time_to_complete(fp, state)
