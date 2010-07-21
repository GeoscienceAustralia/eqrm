#!/usr/bin/env python

"""
A module to convert a random sampled XY.. object into a gridded XY.. object.

The input object is a list of tuples (x, y, ...) where the ... is ANY NUMBER
OF COLUMNS (ie, 1 or more).

The output object is a similar list of tuples with binned (x, y) values and
each of the value columns summed within the bin.

Copyright 2007 by Geoscience Australia

"""


import scipy


def make_xyz(grid, xedges, yedges):
    """Convert result of histogram2d() into an XYZ object.

    grid   gridded data
    xedges X edge coordinates from histogram2d()
    yedges Y edge coordinates from histogram2d()

    """

    xyz = []
    xedges = scipy.array(xedges)
    xedges = xedges[:-1] + (xedges[1] - xedges[0])/2
    yedges = scipy.array(yedges)
    yedges = yedges[:-1] + (yedges[1] - yedges[0])/2
    for (xi, x) in enumerate(xedges):
        for (yi, y) in enumerate(yedges):
            xyz.append([x, y, grid[xi,yi]])
    return scipy.array(xyz)


def calc_grid_sum_xyvs(xyvs, bins=100):
    """Convert an XYVs object into a gridded and summed XYVs object.
    
    xyvs      a list of tuples (x, y, ...)
    bins      the number of required bins, either <int> or [<int>, <int>]

    Returns a tuple ((bin_x, bin_y), xyz_data) where xyz_data is a binned
    version of the input object.  bin_? is bin count for the ? axis.

    """

    # convert to numpy array
    xyvs = scipy.array(xyvs)

    # figure out number of value columns
    num_columns = len(xyvs[0]) - 2
    if num_columns < 1:
        msg = 'calc_grid_sum_xyvs: xyvs object has no data columns'
        raise RuntimeError(msg)

    # get histogram with value1 column
    xyv1 = scipy.take(xyvs, (0,1,2), axis=1)
    (result, xedges, yedges) = scipy.histogram2d(xyv1[:,0], xyv1[:,1],
                                                 bins=bins, normed=False,
                                                 weights=xyv1[:,2])

    # create XYZ object
    result = make_xyz(result, xedges, yedges)

    # get number of bins for result
    # -1 since ?edges is numer of *edges*, we want bins
    bins_x = scipy.shape(xedges)[0] - 1
    bins_y = scipy.shape(yedges)[0] - 1

    # handle each extra value column seperately
    for i in range(num_columns-1):
        xyvn = scipy.take(xyvs, (0,1,i+3), axis=1)
        (binned_data, xedges, yedges) = scipy.histogram2d(xyvn[:,0], xyvn[:,1],
                                                          bins=bins, normed=False,
                                                        weights=xyvn[:,2])
        binned_data = make_xyz(binned_data, xedges, yedges)
        v_col = scipy.take(binned_data, (2,), axis=1)
        result = scipy.hstack((result, v_col))

    return ((bins_x, bins_y), result)


