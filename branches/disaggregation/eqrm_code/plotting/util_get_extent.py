#!/usr/bin/env python

"""
Get extent of lat+lon data in a file or data object.

Returns (ll_lat, ll_lon, ur_lat, ur_lon)
where ll_lat is the lower left corner latitude
      ll_lon is the lower left corner longitude
      ur_lat is the upper right corner latitude
      ur_lon is the upper right cornet longitude

"""


import re
import scipy
import numpy as num


# get regular expression to parse line delimited by whitespace or commas
SplitPattern = re.compile(' +| *, *')

# the default margin percentage
DefaultMargin = 5


def get_extent(datafile, margin=None, filter=None):
    """Get extent of data in a file.

    datafile is the path to the file containing
             many lat+lon points, one per line.
             If not a string, is assumed to be a data list of the form:
             [[lon, lat, value, ...], ...].
    margin   a percentage value giving the margin to apply to the extent
             default is 5%
    filter   is an optional function to return (lat, lon) from each line of the
             file.  If not supplied, CSV file is assumed, first two fields are
             latitude then longitude.

    Returns a tuple: (ll_lat, ll_lon, ur_lat, ur_lon)
             
    """

# TODO: remove file input

    # set the margin percentage
    if margin is None:
        margin = DefaultMargin
        
    # if user didn't supply a filter, use our own
    if filter is None:
        # define a default filter and use it
        def default_filter(line):
            """Get (lon, lat) from line of data.

            line  is a list of field strings

            Return fields 0 and 1.
            """
            
            return (float(line[0]), float(line[1]))

        filter = default_filter

    # start the result values    
    ll_lon = 361.
    ll_lat = 91.
    ur_lon = -361.
    ur_lat = -91.

    if isinstance(datafile, basestring):
        # now grovel through file, remembering max extent values
        for line in file(datafile):
            # ignore blank or comment lines
            line = line.strip()
            if line == '' or line[0] in '%#':
                continue

            # get lon+lat from line, check max extent values
            (lon, lat) = filter(SplitPattern.split(line))
            
            ll_lon = min(ll_lon, lon)
            ur_lon = max(ur_lon, lon)
            ll_lat = min(ll_lat, lat)
            ur_lat = max(ur_lat, lat)
    else:
        datafile = num.array(datafile)
        ll_lon = num.min(datafile[:,0])
        ur_lon = num.max(datafile[:,0])
        ll_lat = num.min(datafile[:,1])
        ur_lat = num.max(datafile[:,1])

    # apply the margin
    x_margin = abs(ur_lon - ll_lon) * margin/100.0
    y_margin = abs(ur_lat - ll_lat) * margin/100.0

    ll_lon -= x_margin
    ur_lon += x_margin
    ll_lat -= y_margin
    ur_lat += y_margin

    return (ll_lat, ll_lon, ur_lat, ur_lon)
