#!/usr/bin/env python

"""
Description: A python replacement for the calc_pml.m function.
 
Version: $Revision: 1133 $  
ModifiedBy: $Author: dgray $
ModifiedDate: $Date: 2009-09-16 17:34:02 +1000 (Wed, 16 Sep 2009) $

Copyright 2007 by Geoscience Australia

"""


import os
import time
import numpy as num

import calc_annloss


def calc_pml(saved_ecloss, saved_ecbval2, nu):
    """Compute the probable maximum loss (PML) curve for a standard
    probabilistic EQRM risk run.

    Inputs:
    saved_ecloss   2D array containing the damage estimates in dollars for
                   each building, multiplied by the survey factor. Note that 
                   the matrix has one row for each simulated event and one
                   column for each building.
    saved_ecbval2  1D row array containing the value of each building,
                   multiplied by the survey factor.
    nu             1D column array the event activity of each of the simulated
                   events.

    Returns:
    pml_data       (nx3) array containing the PML curve. The first column
                   contains the probability of exceedance (in one year) values,
                   the second column contains the direct financial losses
                   for each of the probabilities of exceedance and the third 
                   column contains the financial losses as a percentage of the 
                   total building value.
    """

    # get total building value
    TotalBVal2 = num.sum(saved_ecbval2)
    AggEcLoss = num.sum(saved_ecloss, axis=0) # sum rows

    # Define return periods of interest and return *rates*
    return_periods = num.logspace(1, 6, 25)
    rtrn_rte = 1./return_periods

    # only 1 element on left gets first of returned tuple only?
    (trghzd_agg, _, _) = calc_annloss.acquire_riskval(AggEcLoss, nu, rtrn_rte)

    ProbExceedSmall = 1-num.exp(-rtrn_rte)
    
    return [ProbExceedSmall, trghzd_agg, trghzd_agg/TotalBVal2*100]
