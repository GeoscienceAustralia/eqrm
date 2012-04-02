#!/usr/bin/env python

"""
A module to convert random geographic XYVV data into an XYZ form.
The Z value is computed from (V1/V2)*100, ie a percentage.

The input data object is a list of tuples (lon, lat, v1, v2).

Copyright 2007 by Geoscience Australia

"""


import scipy


def calc_xyvv_percentage(xyvv):
    """Convert an XYVV data object into an XYZ percentages object.
    
    xyvv      a list of tuples (x, y, v1, v2)

    Returns a list of tuples (x, y, (v1/v2)*100)

    """

    xyz = []
    for (x, y, v1, v2) in xyvv:
        if v1 < 1.0e-8:
            xyz.append((x, y, 0.0))
        else:
            xyz.append((x, y, (v1/v2)*100))

    return scipy.array(xyz)


