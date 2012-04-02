#!/usr/bin/env python

"""
Description: A python module to calculate Annual Loss Deaggregated Distance
             and Magnitude data.
 
Copyright 2007 by Geoscience Australia

"""


import os
import numpy as num

import calc_annloss


def calc_annloss_deagg_distmag(bldg_value, saved_ecloss, nu, saved_rjb,
                               aus_mag, momag_bin, R_bin, Zlim,
                               R_extend_flag=False):
    """Calculate the % of annualised loss disaggregated by mag and distance.

    It is the annualised loss disaggregated by mag and distance/ total
    annualised loss, as a percentage.

    Inputs:
    bldg_value      value of each building, dimensions(structure)
    saved_ecloss    building loss, dimensions(event, structure)
    nu              event activity, dimensions(event)
    saved_rjb       rjb distances array, dimensions(event, structure)
    aus_mag         earthquake magnitudes, dimensions(event)
    momag_bin       1xn array of bounds for moment magnitude bins e.g. 
                       momag_bin = [4.5:0.5:6.5];
                    Note that the value 0.0000000000001 is added to the last
                    entry in momag_bin to ensure that values corresponding to
                    momag_bin(-1) are captured i.e.
                        momag_bin = [4.5, 5.0, 5.5, 6.0, 6.5]
                    becomes
                        momag_bin = [4.5, 5.0, 5.5, 6.0, 6.5000000000001]
    R_bin           1xm list containing bounds for distance bins e.g. 
                       R_bin = [0:5:100];
                    Note that if R_extend_flag==1 R_bin is extended by one 
                    element as follows; R_bin(end+1) = 100000. This is done
                    to ensure that all values > R_bin(end) are included in the 
                    final R_bin. 
    R_extend_flag   Whether to extend the R_Bin last bin to catch overflow:
                       True  => extend R_bin (see R_bin)
                       False => do not extend R_bin
    Zlim            1x2 array of z-axis limits.

    Returns the normalised deaggregated loss, dimensions(mag_bin, dist_bin)

    """

    # convert all 'array' data to real arrays
    bldg_value = num.array(bldg_value)
    saved_ecloss = num.array(saved_ecloss)
    nu = num.array(nu)
    saved_rjb = num.array(saved_rjb)
    aus_mag = num.array(aus_mag)
    momag_bin = num.array(momag_bin)
    momag_bin = num.array(momag_bin)     # make sure we don't have a tuple

    # Verify the array shapes
    events = aus_mag.shape[0]
    structures = bldg_value.shape[0]
    assert saved_ecloss.shape == (events, structures)
    assert nu.shape == (events,)
    assert saved_rjb.shape == (events, structures)
    
    # get total building value
    tot_bldg_value = num.sum(bldg_value)

    # get annualised loss in $
    ((ann_loss, _), _) = calc_annloss.calc_annloss(saved_ecloss, bldg_value, nu)
    
    # Setup moment magnitude bins
    momag_bin[-1] = momag_bin[-1] + 0.0000000000001
    #momag_centroid = momag_bin[:-1] + num.diff(momag_bin)/2;
    #if len(momag_centroid) >= 3:
    #    momag_centroid[-1] = momag_bin[-2] + (momag_bin[-2] - momag_bin[-3])/2

    # Setup distance bins (doesn't necessarily need to be Joyner-Boore distance)
    Rjb_bin = R_bin[:]
    if R_extend_flag:
        Rjb_bin.append(10000)

    #Rjb_centroid = Rjb_bin[:-1] + num.diff(Rjb_bin)/2.0;
    #Rjb_centroid[-1] = Rjb_bin[-2] + (Rjb_bin[-2] - Rjb_bin[-3])/2.0

    mLength = len(momag_bin)
    RLength = len(Rjb_bin)

    # prepare result array for deaggregated annualised loss in $
    DeAggLoss = num.zeros((mLength-1, RLength-1))
    
    for i in range(1, mLength):
## TODO: convert to log()
##        print('Now aggregating loss for magnitude greater than '
##              '%.2f and less than %.2f' % (momag_bin[i-1], momag_bin[i]))
        
        aus_mag = num.array(aus_mag)
        # finding magnitudes in mag bin
        mInd = num.nonzero((momag_bin[i-1] <= aus_mag) ==
                           (aus_mag < momag_bin[i]))[0]
        subSaved_ecloss = num.take(saved_ecloss, mInd, axis=0)
        sliced_rjb = num.take(saved_rjb, mInd, axis=0)

        for j in range(1, RLength):
            LossMatrix = num.zeros(num.shape(subSaved_ecloss))
            
            ind = num.logical_and((Rjb_bin[j-1] <= sliced_rjb),
                                  (sliced_rjb < Rjb_bin[j])).nonzero()
            LossMatrix[ind] = subSaved_ecloss[ind]
            TempAggLoss = num.sum(LossMatrix, axis=1)
            [_, TempPercEcLoss, Tempcumnu_ecloss] = \
                         calc_annloss.acquire_riskval(
                TempAggLoss, nu[mInd], 0)
            
            # convert recurrence rates (cumsum(nu)) to
            # prob. of exceed in 1 year
            TempProbExceed = 1 - num.exp(-Tempcumnu_ecloss)
            TempIntPercEcLoss = calc_annloss.integrate_backwards(
                TempPercEcLoss, TempProbExceed)

            DeAggLoss[i-1, j-1] = TempIntPercEcLoss[0]

    # Normalise the Deaggregated loss by the annualised loss in $
    NormDeAggLoss = 100.0 * DeAggLoss / ann_loss;
    
    return NormDeAggLoss
