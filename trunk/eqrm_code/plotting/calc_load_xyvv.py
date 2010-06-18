#!/usr/bin/env python

"""
A module to load XYVV data into memory.

The data is expected to be in a file with lines like:
    lon lat value1 value2

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


# get regular expression to parse line delimited by whitespace or commas
SplitPattern = re.compile(' +| *, *')


def calc_load_xyvv(datafile, invert=False, filter=None, scale=None,
                   clip=None):
    """A function to take a file of data and create an XYVV data object.
    
    datafile  a file containing (lat, lon, val) values
    invert    used if 'filter' not supplied and an internal filter is used.
              if 'invert' is True, switch the order of lon/lat in data lines.
    filter    a function to extract (lon, lat, val) from one datafile line
              if not supplied an internal function is used
    scale     amount to scale the data (ie, divide)
    clip      if defined is a dictionary defining clip limits. Recognised
              keys in the dictionary are:
                 'high'     sets high limit above which values are clipped
                 'low'      sets low limit below which values are clipped
              At least one of the above keys must exist.
              The clipping is done before any scaling.

    Returns a list of tuples (lon, lat, val1, val2).

    """

    # if user didn't supply a data filter, use our own
    if filter is None:
        # define a default filter and use it
        if invert:
            def default_filter(line):
                return (float(line[1]), float(line[0]), float(line[2]),
                        float(line[3]))
        else:
            def default_filter(line):
                return (float(line[0]), float(line[1]), float(line[2]),
                        float(line[3]))

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

    return data


