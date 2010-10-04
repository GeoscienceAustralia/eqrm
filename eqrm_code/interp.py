"""
 Title: interp.py
 
  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, duncan.gray@ga.gov.au
           
  Description: The inbuilt interpolation functions in scipy didn't
extrapolate, so this is used instead.

  Version: $Revision: 1398 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-12-22 14:16:39 +1100 (Tue, 22 Dec 2009) $
  
  Copyright 2007 by Geoscience Australia
"""

from scipy import asarray, newaxis, where

def interp(new_period, old_c, old_period, axis=0,
           extrapolate_high=True, extrapolate_low=True):
    """Interpolate old_c(old_period) to new_period
    Args:
      new_period: The period values that need new coefficient values.
      old_c: The known coefficient values, to use in the interpolation
        The dimension is often (structure, event, periods) - check this.
        The last dimension must be periods.
      old_period: The known period values, to use in the interpolation
      axis:
      extrapolate_high: If extrapolate_high is False, do not extrapolate
        higher than the old values, rather return the old_c value of the
        highest old_period.
      extrapolate_low:
        If extrapolate_low is False, do not extrapolate lower than the
        old values, rather return the old_c value of the lowest old_period.
    
    Values will be sorted by old_period, so old_period is ascending

    Returns:
      new_c: The new coefficient values, given the new period values
    """
    new_period=asarray(new_period)
    old_c=asarray(old_c)
    old_period=asarray(old_period)

    # if this assert fails, maybe you need to add an extra dimension,
    # with a value of 1, to an array.
    #print "interp old_c", old_c
    #print "interp old_c.shape", old_c.shape
    assert old_c.shape[-1] == old_period.shape[0]
    
    if not len(old_period)>1:
        raise TypeError, "Cannot interpolate 1 value!"
        # You simply cannot interp with one value
    #print "old_c.shape[axis]",  old_c.shape[axis]
    #print "len(old_period", len(old_period)
    if not old_c.shape[axis]==len(old_period):
        raise TypeError, "Bad vaules"

    # this will sort the 
    old_period_order=old_period.argsort()
    old_period=old_period.take(old_period_order)
    old_c=old_c.take(old_period_order,axis=axis)     

    # scipy interp is annoying
    new_period_index=old_period.searchsorted(new_period)
    # returns i such that old_period[i-1] < new_period <= old_period[i]
    # returns len(old_period) if old < new
    # returns 0 if new <= old
    if isinstance(new_period_index,int):
        new_period_index=asarray((new_period_index,))
        #must be a sequence
    
    too_high=(new_period_index==len(old_period))
    too_low=(new_period_index==0)
    new_period_index=new_period_index+too_low-too_high
    # getting the right bin doesn't matter so much as getting
    # a valid bin (ie 0 < new_period_index < len(old_period))
    c0=old_c.take(new_period_index-1,axis=axis)
    p0=old_period.take(new_period_index-1)
    dc=old_c.take(new_period_index,axis=axis)-c0
    dp=old_period.take(new_period_index)-p0
    new_c = c0+(new_period-p0)*dc/dp
    if not extrapolate_high:
        new_c=where(too_high,c0+dc,new_c)
    if not extrapolate_low:
        new_c=where(too_low,c0,new_c)
    return new_c
