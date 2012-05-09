#!/usr/bin/env python

"""
Description: A python module to calculate Annual Fatalities Deaggregated Distance
             and Magnitude data.
 

"""


import os
import numpy as num

import calc_annloss


def calc_annfatalities_deagg_distmag(saved_fatalities, nu, saved_rjb,
                               aus_mag, momag_bin, R_bin, Zlim,
                               R_extend_flag=False):
    """Calculate the % of annualised fatalities disaggregated by mag and distance.

    It is the annualised fatalities disaggregated by mag and distance/ total
    annualised fatalities, as a percentage.

    Inputs:
    saved_fatalities    fatalities, dimensions(event, structure)
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
    saved_fatalities = num.array(saved_fatalities)
    nu = num.array(nu)
    saved_rjb = num.array(saved_rjb)
    aus_mag = num.array(aus_mag)
    momag_bin = num.array(momag_bin)
    momag_bin = num.array(momag_bin)     # make sure we don't have a tuple

    # Verify the array shapes
    events = aus_mag.shape[0]
    assert nu.shape == (events,)
    
    
    # get total building value

    # get annualised loss in #
    (ann_fatalities, _) = calc_annloss.calc_annfatalities(saved_fatalities, nu)
    
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
    DeAggFatalities = num.zeros((mLength-1, RLength-1))
    
    for i in range(1, mLength):
## TODO: convert to log()
##        print('Now aggregating loss for magnitude greater than '
##              '%.2f and less than %.2f' % (momag_bin[i-1], momag_bin[i]))
        
        aus_mag = num.array(aus_mag)
        # finding magnitudes in mag bin
        #print aus_mag.shape
        mInd = num.nonzero((momag_bin[i-1] <= aus_mag) ==
                           (aus_mag < momag_bin[i]))[0]
        subSaved_fatalities = num.take(saved_fatalities, mInd, axis=0)
        #print saved_rjb.shape, mInd
        sliced_rjb = num.take(saved_rjb, mInd, axis=0)

        for j in range(1, RLength):
            FatalitiesMatrix = num.zeros(num.shape(subSaved_fatalities))
            
            ind = num.logical_and((Rjb_bin[j-1] <= sliced_rjb),
                                  (sliced_rjb < Rjb_bin[j])).nonzero()
            FatalitiesMatrix[ind] = subSaved_fatalities[ind]
            TempAggFatalities = num.sum(FatalitiesMatrix, axis=1)
            #print TempAggFatalities
            [_, TempPercFatalities, Tempcumnu_fatalities] = \
                         calc_annloss.acquire_riskval(
                TempAggFatalities, nu[mInd], 0)
            
            # convert recurrence rates (cumsum(nu)) to
            # prob. of exceed in 1 year
            TempProbExceed = 1 - num.exp(-Tempcumnu_fatalities)
            TempIntPercFatalities = calc_annloss.integrate_backwards(
                TempPercFatalities, TempProbExceed)

            #print DeAggFatalities.shape, TempIntPercFatalities.shape, TempPercFatalities
            
            if len(TempPercFatalities)>0:
                DeAggFatalities[i-1, j-1] = TempIntPercFatalities[0]
            else:
                DeAggFatalities[i-1, j-1] = 0

    # Normalise the Deaggregated loss by the annualised loss in $
    NormDeAggFatalities = 100.0 * DeAggFatalities / ann_fatalities;
    
    return NormDeAggFatalities

    