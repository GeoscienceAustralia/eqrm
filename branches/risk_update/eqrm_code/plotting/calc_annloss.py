#!/usr/bin/env python

"""
Description: A python module to calculate Anevent_activityal Loss Deaggregated Distance
             and Magnitude data.
 
Copyright 2007 by Geoscience Australia

"""


import os
import time
import numpy as num
import scipy

from eqrm_code.plotting import utilities


def calc_annloss(loss_matrix, bldg_values, event_activity):
    """Computes the annualised loss from a standard probabilistic EQRM risk run.

    INPUTS:
    loss_matrix    Contains the loss estimates in dollars for each building
                   multiplied by the survey factor. Note that the matrix has one
                   row for each event and one column for each building (MxN).
    bldg_values    Contains the value of each building multiplied by the survey
                   factor (1xN).
    event_activity the activity of each of the simulated events (Mx1).

    Returns a tuple (ann_loss, cum_ann_loss) where:
    ann_loss       is a tuple (ann_$, ann_pct) where:
                       ann_$   is the annualised loss in dollars
                       ann_pct is the annualised loss as a percentage
                                  of the total building value
    cum_ann_loss   is a tuple (return, dollars, percent) where:
                       return  is the return period
                       dollars is the cumulative annual loss in dollars
                       percent is the cumulative annual loss as % of
                                  total building value
                          
    """

    # get the total building value for the region
    tot_bldg_values = num.sum(bldg_values)

    # reorder the loss values and activity
    # and get the cumulative activity values
    loss_by_actitivy = num.sum(loss_matrix, axis=1)
    (trghzd_agg, sort_loss_activity,
     cum_event_activity) = acquire_riskval(loss_by_actitivy,
                                              event_activity, 0)
    #print "sort_loss_activity", sort_loss_activity
    #print "cum_event_activity", cum_event_activity

    # convert recurrence rates to prob. of exceedance in 1 year
    prob_exceed = 1 - num.exp(-cum_event_activity)
    #print "prob_exceed", prob_exceed
    
    tmp_ann_loss = integrate_backwards(sort_loss_activity, prob_exceed)

    ann_loss = num.array([tmp_ann_loss[0], tmp_ann_loss[0]/tot_bldg_values*100])

    return_period = 1.0/ cum_event_activity
    #assert scipy.allclose(retrn_per1, retrn_period)
    cum_ann_loss = num.array([return_period, tmp_ann_loss,
                              tmp_ann_loss/tot_bldg_values*100])

    return (ann_loss, cum_ann_loss)

def integrate_backwards(x_array, y_array):
    """
    Given x_array and y_array values, calculate the backwards cumulative
    area under the y axis of the curve.
    
    preconditions;
    x is sorted, ascending.
    y is sorted, ascending.
    x and y values are positive    
    x and y are vectors.

    return:
      Vector[0] is the area under the y axis of the curve.
      if n is the last index of the vector
      vector[n-i] is the area under the y-axis from y_array[0]
      to y_array[i], so
      vector[n] is 0.
    """
     
    n = len(y_array)
    tmp_ann_loss = num.zeros(n)
    #print "range(n-2, -1, -1)", range(n-2, -1, -1)
    for s in range(n-2, -1, -1):
        height = abs(y_array[s+1] - y_array[s])
        tri_width = abs(x_array[s+1] - x_array[s])
        rect_width = min(x_array[s+1], x_array[s])
        tri_area = 0.5 * tri_width * height
        rect_area = height * rect_width
        tmp_ann_loss[s] = tmp_ann_loss[s+1] + tri_area + rect_area
    return tmp_ann_loss   
 
def acquire_riskval(x_ordinals, y_values, target_ordinals):
    """Acquire risk values associated with target return periods.

    Inputs:
    x_ordinals      ordinals of interest (X values)
    y_values        values at the ordinal values (Y values)
    target_ordinals ordinal values for which target values are required

    Returns (target_values, sorted_x_ordinals, cum_sorted_y_values) where:
    target_values       interpolated values at target ordinals
    sorted_x_ordinals   sorted 'x_ordinals' (input arg)
    cum_sorted_y_values cumulative sorted target values
    """

    # tie x_ordinals and y_values arrays together, sort on x_ordinals
    # largest to smallest, then untie back to two arrays
    zip_sort = zip(x_ordinals, y_values)
    
    zip_sort.sort(reverse=True, key=lambda x: x[0])
    
    sorted_x_ordinals = [a for (a,b) in zip_sort]
    sorted_y_values = [b for (a,b) in zip_sort]

    # get cumulative sum of sorted values
    cum_sorted_y_values = num.cumsum(sorted_y_values)

    # get linear interpolation values at required ordinals
    target_values = num.interp(target_ordinals, cum_sorted_y_values,
                               sorted_x_ordinals)

    return (target_values, sorted_x_ordinals, cum_sorted_y_values)
   
def calc_annloss_deagg_grid(lat,
                            lon,
                            total_building_loss,
                            total_building_value,
                            event_activity, bins=100):
    """Calculate the annualised loss as a percentage of total value in the
    grid cell.

    Inputs:
    lat                    latitude, dimensions(event)
    lon                    longitude, dimensions(event)
    total_building_loss    building loss, dimensions(event, structure)
    total_building_value   value of each building, dimensions(structure)
    event_activity         event activity, dimensions(event)
    bins   an integer or (int, int) describing how the extent of
           the data in (lat, lon) is to be binned
           If one integer is supplied the extent determined from the
           point data (lat, lon) is binned that number of times in the
           X and Y direction.  If (M, N), the number of X bins is M, etc.

    return:  
      percent_ann_loss: the annulaised loss, as a percentage of total
        value for each grid cell, dimensions(grid cells)
      lat_lon: a tuple of (lat, lon) midpoints, giving the grid cell locations,
        dimensions(grid cells)
    """
    
    # Bin data
    cell_location = utilities.bin_extent(lat, lon, bins=bins)
    
    # get bin width and number of cells
    try:
        (gnumx, gnumy) = bins
    except TypeError:
        gnumx = gnumy = bins
    num_of_bins = gnumx * gnumy

    # Run annulised loss calc on binned data
    lat_lon = scipy.zeros((num_of_bins, 2))
    annualised_loss_in_cell = scipy.zeros(num_of_bins)
    sum_building_value_cell = scipy.zeros(num_of_bins)

    i = 0
    for row in cell_location:
        for cell in row:
            # calc the annualised loss for this cell.
            index = scipy.array(cell['index'])
#             print "total_building_value", total_building_value
#             print "index", index
#             print "total_building_value.shape", total_building_value.shape
#             print "index.shape", index.shape
#             Print "cell['mid_lat_lon']", cell['mid_lat_lon']
#             print "cell['mid_lat_lon'].shape", cell['mid_lat_lon'].shape
            lat_lon[i, :] = cell['mid_lat_lon']
            if len(index) >= 1:
#                 print "index", index
#                 print "total_building_loss.shape", total_building_loss.shape
#                 print " total_building_value.shape", total_building_value.shape
                total_building_value_cell = scipy.take(total_building_value,
                                                       index)
                total_building_loss_cell = scipy.take(total_building_loss,
                                                      index, axis=1)
                ((annualised_loss_in_cell[i], _), _) = calc_annloss(
                    total_building_loss_cell,
                    total_building_value_cell,
                    event_activity)
                sum_building_value_cell[i] = scipy.sum(
                    total_building_value_cell)
            else:
                annualised_loss_in_cell[i] = scipy.nan
                sum_building_value_cell[i] = scipy.nan
            i += 1           
    percent_ann_loss = 100.0 *  annualised_loss_in_cell/sum_building_value_cell
    
    return percent_ann_loss, lat_lon, gnumx, gnumy
            
