#!/usr/bin/env python

"""
A module to convert random geographic data into a gridded XYZ form.
Binned data is meaned within each bin.

The data is expected to be in a file with lines like:
    lon lat value

The values may be delimited by spaces or commas.

Copyright 2007 by Geoscience Australia

"""


import os
import sys
import re
import time
import tempfile
import shutil
import scipy
import numpy as num

import eqrm_code.plotting.util_get_extent as ge


# get regular expression to parse line delimited by whitespace or commas
SplitPattern = re.compile(' +| *, *')


def calc_mean_xyz(datafile, scale=None, bins=100, filter=None, invert=False,
                  clip=None):
    """Convert a file of (lon, lat, val) data to gridded XYZ data object.
    
    Take values at random x,y points and bin into summed values.

    datafile  a file containing (lon, lat, val) values
    scale     amount to scale the data (ie, divide)
    bins      number of bins in X and Y direction
                  if an int, # bins in X and Y direction
                  if [int, int] the X and Y bin counts may be different
    filter    a function to extract (lon, lat, val) from one datafile line
              if not supplied an internal function is used
    invert    if 'filter' not supplied, an internal filter is used.  if
              'invert' is True, switch the order of lat/lon in data lines.
    clip      if defined is a dictionary defining clip limits. Recognised
              keys in the dictionary are:
                 'high'     sets high limit above which values are clipped
                 'low'      sets low limit below which values are clipped
              At least one of the above keys must exist.
              The clipping is done before any scaling.

    Returns a tuple (bins, xyz) where bins is the number of bins in the X
    direction and xyz is a numpy array of XYZ data [[lon, lat, val], ...].

    Values that are 0 replaced with Nan.

    """

    # handle optional parameters
    try:
        bin_len = len(bins)
    except TypeError:
        bins_x = bins_y = bins
    else:
        try:
            (bins_x, bins_y) = bins
        except ValueError:
            raise RuntimeError("Bad 'bins' value, expected int or [int, int]")

    # if user didn't supply a data filter, use our own
    if filter is None:
        # define a default filter and use it
        if invert:
            def default_filter(line):
                return (float(line[1]), float(line[0]), float(line[2]))
        else:
            def default_filter(line):
                return (float(line[0]), float(line[1]), float(line[2]))

        filter = default_filter

    # get data into memory
    data = []
    for line in file(datafile):
        # ignore blank or comment lines
        line = line.strip()
        if line == '' or line[0] in '%#':
            continue

        # get lon+lat+value from line
        data.append(filter(SplitPattern.split(line)))
    data = scipy.array(data)

    # do clipping, if required
    if clip:
        low_clip = clip.get('low', None)
        high_clip = clip.get('high', None)

        if low_clip is None:
            low_clip = scipy.min(data[:,2])
        if high_clip is None:
            high_clip = scipy.max(data[:,2])

        data[:,2] = scipy.clip(data[:,2], low_clip, high_clip)

    # handle any scaling
    if scale:
        scale = int(scale)
        data[:,2] = data[:,2] / scale

#    # get extent of data (tight first, then with margin)
#    (tll_lat, tll_lon, tur_lat, tur_lon) = ge.get_extent(data, margin=0)
#    tr_opt = '-R%f/%f/%f/%f' % (tll_lon, tur_lon, tll_lat, tur_lat)
#
#    (ll_lat, ll_lon, ur_lat, ur_lon) = ge.get_extent(data)
#    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # now generate a binned dataset
    (sum_data, xedges, yedges) = num.histogram2d(data[:,0], data[:,1],
                                                 bins=bins, normed=False,
                                                 weights=data[:,2])

    (count_data, _, _) = num.histogram2d(data[:,0], data[:,1],
                                         bins=bins, normed=False)

    calc_mean = sum_data / count_data

    # create XYZ object
    # make sure X+Y is *centre* of each bin
    xyz = []
    xedges = scipy.array(xedges)
    xedges = xedges[:-1] + (xedges[1] - xedges[0])/2
    yedges = scipy.array(yedges)
    yedges = yedges[:-1] + (yedges[1] - yedges[0])/2
    for (xi, x) in enumerate(xedges):
        for (yi, y) in enumerate(yedges):
            xyz.append([x, y, calc_mean[xi,yi]])
    xyz = scipy.array(xyz)

    return (bins_x, xyz)


