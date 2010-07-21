#!/usr/bin/env python

"""
A module to change all values in an XYZ object to numpy.nan.
This has the effect of ignoring those values when plotted.

Copyright 2007 by Geoscience Australia

"""


import scipy


def calc_ignore_xyz(data, ignore=None):
    """A function to take an XYZ data object of tuples (lon, lat, value)
    and change all values <= 'ignore' to numpy.nan.
    
    data      a file containing (lat, lon, val) values
    ignore    a value below which all values become a NaN

    Returns the original XYZ object with values <= ignore chend to a NaN.

    """

    # replace values <= 'ignore' with NaN
    if ignore is not None:
        data[:,2] = scipy.where(data[:,2] <= ignore, scipy.nan, data[:,2])

    return data


