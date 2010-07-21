#!/usr/bin/env python

"""First attempt at a bridge-damage function.

This damage function takes a model string which determines the model to
use for damage estimation.  To add another model, do:
    . Add a new model string such as ModelFudge = 'FUDGE'
    . Add new model string into 'models'
    . Add another damage function called 'bridge_damage_FUDGE'
      (like bridge_damage_ModelLinear)
    . Add an entry into ModelFunctions - ModelFudge: bridge_damage_FUDGE

This function takes the Classification, DamageParams and EQCoefficients data
from external files.  Another option is to build that data into this module.
"""

import os
import string
import math
import warnings     # suppress deprecation warnings in scipy
warnings.simplefilter("ignore", DeprecationWarning)
import random
import scipy.stats
import numpy as num

from eqrm_code.util import determine_eqrm_path
import csv_interface as csvi
import eqrm_filesystem


# normalised composite log-normal standard deviation
# Mander JB, Basoz N, (1999) Seismic fragility curve theory for highway bridges.
# Optimizing Post-Earthquake Lifeline System Reliability - Proceedings of the
# 5th US Conference on Lifeline Earthquake Engineering, USA ASCE; 31-40.
Beta = 0.6

# Dictionaries containing algorithm data - filled 'lazily' on first call
ClassificationDamageParams = None
EQCoefficients = None

# filenames the above dictionaries are filled from
ClassificationDamageParamsCSVFile = 'bridge_classification_damage_params.csv'
EQCoefficientsCSVFile = 'bridge_k3d_coefficients.csv'

# directory path from base path to 'eqrm_code' to where data files reside
DataFilePath = eqrm_filesystem.Resources_Data_Path


######
# Default model used by this module.
######

ModelLinear = 'LINEAR'

################################################################################

def bridge_states(CLASS, sa_0_3, sa_1_0, skew, num_spans, model=None):
    """Top-level function to calculate bridge damage states.

    CLASS      bridge class - a string like 'hwb1'
    sa_0_3     1D array of spectral acceleration at the bridge, T=0.3s
    sa_1_0     1D array of spectral acceleration at the bridge, T=1.0s
    skew       bridge skew (degrees)
    num_spans  number of spans in the bridge
    model      the model to use when estimating damage (string)

    Returns a tuple (slight, moderate, extensive, complete) of state
    probabilities.  Each element is a 1D array of probabilities in the
    range [0.0, 1.0].
    """

    # assume default model if none supplied
    if model is None:
        model = ModelLinear

    # load data if necessary
    if ClassificationDamageParams is None or EQCoefficients is None:
        load_bridge_data()

    model = str(model).upper()
    model_func = ModelStateFunctions.get(model, invalid_model_func)

    return model_func(model, CLASS, sa_0_3, sa_1_0, skew, num_spans)

################################################################################
# Individual damage functions - called by top-level routine above
################################################################################

def bridge_states_ModelLinear(model, CLASS, sa_0_3, sa_1_0, skew, num_spans):
    """Calculate the bridge damage probability states for LINEAR model.

    model      the model to use when estimating damage (ignored)
    CLASS      bridge class - string like 'hwb1'
    sa_0_3     2D array of spectral acceleration at the bridge, T=0.3s
                  (numsites, numevents)
    sa_1_0     2D array of spectral acceleration at the bridge, T=1.0s
                  (numsites, numevents)
    skew       bridge skew (scalar)
    num_spans  number of spans in the bridge (scalar)

    Returns an Nx4 numpy array of state probabilities:
        [[slight, moderate, extensive, complete], ....]
    where the N axis is the events and 4 axis is state probabilities.
    """

    # convert user CLASS to uppercase, just in case
    uCLASS = CLASS.upper()

    # get classification and damage params for the bridge class
    try:
        (K3d, Ishape, a2, a3, a4, a5) = ClassificationDamageParams[uCLASS]
    except KeyError:
        msg = 'Bad bridge CLASS: %s' % CLASS
        raise RuntimeError(msg)

    # now calculate K3d value through the parameterised equation
    # if we get divide by zero, pretend num_spans = 2
    (A, B) = EQCoefficients[K3d]
    try:
        K3d_value = 1.0 + A/(num_spans - B)
    except ZeroDivisionError:
        K3d_value = 1.0 + A

    # calculate Kskew - convert degrees to radians
    Kskew = math.sqrt(math.sin(math.radians(90 - skew)))

    # using Sa values, calculate Kshape = 2.5 * (sa_1_0/sa_0_3)
    # adjust for Ishape value
    Kshape = 2.5 * (sa_1_0/sa_0_3)
    if Ishape == 0:
        Kshape = num.ones_like(sa_1_0)

    # now calculate the median fragility curve values for states 2 through 5
    A2 = Kshape * a2
    A3 = Kskew * K3d_value * a3
    A4 = Kskew * K3d_value * a4
    A5 = Kskew * K3d_value * a5

    # now get probability of exceedance for each damage state
    P_slight = scipy.stats.norm.cdf(num.log(sa_1_0/A2)/Beta)
    P_moderate = scipy.stats.norm.cdf(num.log(sa_1_0/A3)/Beta)
    P_extensive = scipy.stats.norm.cdf(num.log(sa_1_0/A4)/Beta)
    P_complete = scipy.stats.norm.cdf(num.log(sa_1_0/A5)/Beta)

    result = num.array((P_slight-P_moderate, P_moderate-P_extensive,
                        P_extensive-P_complete, P_complete))
    result = num.transpose(result, (1, 2, 0))

    return result

def invalid_model_func(model, *args):
    """Function called for unrecognized model string."""

    msg = 'Unrecognized bridge damage model: %s' % model
    raise RuntimeError(msg)

################################################################################
# Utility routines
################################################################################

# strings returned from interpret_damage_state()
DamageStateStrings = ('none', 'slight', 'moderate', 'extensive', 'complete')

def interpret_damage_state(state):
    """Convert a damage state integer into a state string."""

    return DamageStateStrings[state]


def choose_random_state(states, rand_value=None):
    """Choose a random state from a state array.

    states      is an array of shape (S, E, ST)
                    S  is the number of sites (N)
                    E  is the number of events (probably 1)
                    ST is the number of states for the bridge (4 in this case)
    rand_value  if not None, this is random value for all tuples ([0.0, 1.0])
                (TESTING *ONLY*)

    Choose a random state from each tuple, return an array of shape (S, E, 1),
    ie, return an array collapsed from 4 to 1 in the last dimension.
    """

    axis0 = states.shape[0]		# S
    axis1 = states.shape[1]		# E
    newshape = (axis0, axis1, 1)	# (S, E, 1)

    if rand_value is not None:
        rand_array = num.ones(newshape) * rand_value
    else:
        rand_array = num.random.rand(axis0,axis1,1)	# (S, E, 1)

    # create result vector, fill with -1 (get error indexing if not changed)
    result = num.ones(newshape, dtype=int) * -1		# (S, E, 1)

    # fill accum with 'none' probability
    accum = 1.0 - num.sum(states, axis=2)
    accum = num.reshape(accum, newshape)		# (S, E, 1)

    # handle 'none' damage state
    cols = num.where(accum >= rand_array)
    result[cols] = 0
    accum[cols] = -10.0		# shove accum way back, never see it again

    for i in xrange(4):
        delta = num.reshape(states[:,:,i], newshape)
        accum = accum + delta
        cols = num.where(accum >= rand_array)
        result[cols] = i + 1
        accum[cols] = -10.0	# shove accum way back, never see it again

    return result


def load_bridge_data():
    """Preload bridge damage data from external files."""

    global ClassificationDamageParams, EQCoefficients

    # check dictionaries - if empty, load from file
    if ClassificationDamageParams is None:
        eqrm_dir = determine_eqrm_path(__file__)
        path = os.path.join(eqrm_dir, DataFilePath,
                            ClassificationDamageParamsCSVFile)
        ClassificationDamageParams = csvi.csv2rowdict(path,
                                        columns=['CLASS', 'K3D', 'Ishape',
                                                 'Slight', 'Moderate',
                                                 'Extensive', 'Complete'],
                                        convert={'Ishape': int,
                                                 'Slight': float,
                                                 'Moderate': float,
                                                 'Extensive': float,
                                                 'Complete': float})
    if EQCoefficients is None:
        eqrm_dir = determine_eqrm_path(__file__)
        path = os.path.join(eqrm_dir, DataFilePath, EQCoefficientsCSVFile)
        EQCoefficients = csvi.csv2rowdict(path,
                                          columns=['Equation','A','B'],
                                          convert={'A': float, 'B': int})

######
# Dictionaries mapping model to bridge states function.
######

ModelStateFunctions = {ModelLinear: bridge_states_ModelLinear,
                      }


