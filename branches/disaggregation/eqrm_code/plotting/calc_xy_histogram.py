#!/usr/bin/env python

"""
A module to convert random (x, y) data into a histogram form.

The data is expected to be in a file with lines like:
    xvalue yvalue

Copyright 2007 by Geoscience Australia

"""


import os
import sys
import re
import time
import tempfile
import shutil
import scipy


def calc_xy_histogram(datafile, scale=None, bins=10):
    """Takes scalar values from a file and generates an XY histogram object:
           [(X, Y), (X', Y'), ...]
    by calculating the frequency count for each bin Y.

    datafile  path to a file containing scalar values, one per line,
              or an array of already-loaded data
    scale     amount to scale the data (ie, divide)
    bins      If an int, it defines the number of equal-width bins in the given
              X range. If it is a sequence, it defines the bin edges, including
              the rightmost edge, allowing for non-uniform bin widths.

    Returns an array of rows of (x, y) where the y values are binned at value x.

    """

    # get data into memory
    if isinstance(datafile, basestring):
        #data = om.load_x_data(datafile)    # when we have it
        #data = scipy.array(data)
        data = scipy.loadtxt(datafile)
    else:
        # already loaded
        data = datafile

    # handle any scaling
    if scale:
        data /= scale

    # now generate histogrammed data
    (hist_data, xedges) = scipy.histogram(data, bins=bins, normed=False, new=True)

    # get array of bin centres
    bins = []
    for i in range(len(xedges)-1):
        bins.append(xedges[i] + (xedges[i+1] - xedges[i])/2.0)
    bins = scipy.array(bins)

    # return nx2 array of (x, y)
    return scipy.hstack((bins[:,scipy.newaxis], hist_data[:,scipy.newaxis]))


