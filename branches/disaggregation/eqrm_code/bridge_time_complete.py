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


# numpy array containing rows of completion times per FP value
# None means we have yet to load data from external file
# after loading, row 0->none, 1->slight, etc,
# values in each row match the given FP values
StateFPDays = None

# filename the above dictionary is filled from
MeanSigmaValuesCSVFile = 'bridge_state_mean_sigma.csv'

# path to directory for input files
DataFilePath = eqrm_filesystem.Resources_Data_Path


def time_to_complete(fp, states):
    """Return days to completion to given FP for a damage state.

    fp      1D array of required percentage functionality, shape (FP,)
            of integer values in range [0, 100]
    states  bridge damage states array with shape (S, E, ST) where
                S  is the number of sites
                E  is the number of events
                ST is the collapsed state integer of each bridge+event (1)
 
    Return float days as an array of shape (S, E, FP).
    """

    global StateFPDays

    # convert functional percentage to fraction
    fp_fraction = numpy.array(fp)/100.0

    # make sure we have loaded external data
    # then get days matching various FP values
    if StateFPDays is None:
        StateFPDays = load_external_data(fp_fraction)

    fp_dim = fp.shape
    states_dim = states.shape
    result_dim = (states_dim[0], states_dim[1], fp_dim[0])

    result = numpy.zeros(result_dim)
    try:
        result = result + StateFPDays[states[:,:,0]]
    except IndexError:
        msg = 'Bad state value in: %s' % str(states[:,:,0])
        raise RuntimeError(msg)

    return result


def load_external_data(fp):
    """Load mean and sigma values from an external file.

    Data is placed in a numpy array where row number is the state
    number and the columns are the ppf() function for each pf value

    That is, if the source data file contains:
        State,StateIndex,Mean,Sigma
        none,0,0.0,0.00001
        slight,1,0.6,0.6
        moderate,2,2.5,2.7
        extensive,3,75.0,42.0
        complete,4,230.0,110.0
    and the fp value is [10, 20] then the resulting array will be:
           fp(10) fp(20)
            vvv   vvv
        [[    0     0    ]	<- state 0 (none)
         [    1     1    ]	<- state 1 (slight)
         [    1     2    ]	<- state 2 (moderate)
         [   40    53    ]	<- state 3 (extensive)
         [  138   173    ]]	<- state 4 (complete)

    All 'none' state days will be 0 days.  All other states have values
    computed with ceil() and if less than 1 changed to 1.
    """

    eqrm_dir = determine_eqrm_path(__file__)
    path = os.path.join(eqrm_dir,
                        eqrm_filesystem.Resources_Data_Path,
                        MeanSigmaValuesCSVFile)
    dict = csvi.csv2rowdict(path,
                            columns=['StateIndex', 'Mean', 'Sigma'],
                            convert={'StateIndex': int,
                                     'Mean': float,
                                     'Sigma': float })

    data = []
    for i in range(5):
        (mean, sigma) = dict[str(i)]
        data.append(scipy.stats.norm.ppf(fp, mean, sigma))
    data = numpy.array(data)


    # 'normalise' results
    # if value < 0, convert to 1
    # if value < 1 and > 0, convert to 1
    result = data.clip(1.0, 99999999999.0)
    result = numpy.ceil(numpy.array(result))
    result[0,:] = 0.0		# force all 'none' times to 0

    return result


def reset_external_data():
    """Routine to set StateFPDays back to None.

    Forces a reload/recalc of StateFPDays data.
    USED ONLY FOR TESTING.
    """

    global StateFPDays

    StateFPDays = None


################################################################################

if __name__ == '__main__':
    fp = numpy.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
    #states = numpy.array([[[1],[0],[3]]])
    states = numpy.array([[[1],[0],[3]],
                          [[2],[1],[4]]])
    time_to_complete(fp, states)
