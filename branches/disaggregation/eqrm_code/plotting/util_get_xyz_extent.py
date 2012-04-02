#!/usr/bin/env python

"""
Get extent of lon+lat data in an XYZ data object.
Object has form [[lon, lat, val], ...].

Returns (ll_lat, ll_lon, ur_lat, ur_lon)
where ll_lat is the lower left corner latitude
      ll_lon is the lower left corner longitude
      ur_lat is the upper right corner latitude
      ur_lon is the upper right corner longitude

"""


import re
import numpy as num


# the default margin percentage
DefaultMargin = 5


def get_extent(data, margin=None):
    """Get extent of data in a file.

    data     is the numpy array containing [[lon, lat, val, ...], ...].
    margin   a percentage value giving the margin to apply to the extent
             default is 5%

    Returns a tuple: (ll_lat, ll_lon, ur_lat, ur_lon)
             
    """

    # set the margin percentage
    if margin is None:
        margin = DefaultMargin
    
    # get lat/lon limits
    ll_lon = num.min(data[:,0])
    ur_lon = num.max(data[:,0])
    ll_lat = num.min(data[:,1])
    ur_lat = num.max(data[:,1])

    # apply the margin
    x_margin = abs(ur_lon - ll_lon) * margin/100.0
    y_margin = abs(ur_lat - ll_lat) * margin/100.0

    ll_lon -= x_margin
    ur_lon += x_margin
    ll_lat -= y_margin
    ur_lat += y_margin

    return (ll_lat, ll_lon, ur_lat, ur_lon)
