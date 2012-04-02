#!/usr/bin/env python

"""
Description: Place a north pointer annotation on a plot.
 
Copyright 2007 by Geoscience Australia

"""


import time

import matplotlib.pyplot as plt


def plot_northpointer(basemap, extent, posn):
    """
    Place a 'generated at ...' annotation on an open plot.

    basemap  the basemap to annotate
    extent   a tuple with plot extent data:
                 (ll_lat, ll_lon, ur_lat, ur_lon)
    posn     where to place the pointer, one of
                 'NE', 'SE', 'SW' or 'NW'
                 (case insensitive)

    """

    # unpack the extent values
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent

    # figure out annotation placement
    posn = posn.lower()
    if posn == 'ne':
        lon = ur_lon - (ur_lon-ll_lon)*3/100
        lat = ur_lat - (ur_lat-ll_lat)*10/100
    elif posn == 'se':
        lon = ur_lon - (ur_lon-ll_lon)*3/100
        lat = ll_lat + (ur_lat-ll_lat)*10/100
    elif posn == 'sw':
        lon = ll_lon + (ur_lon-ll_lon)*3/100
        lat = ll_lat + (ur_lat-ll_lat)*10/100
    elif posn == 'nw':
        lon = ll_lon + (ur_lon-ll_lon)*3/100
        lat = ur_lat - (ur_lat-ll_lat)*10/100
    else:
        raise RuntimeError('Bad scale placement: %s' % posn)

    # length of pointer arms is 4% of plot height
    length = (ur_lat-ll_lat)*4/100

    # other sizes depend on length
    cd_offset = length / 6
    p_w = length / 10
    p_lo = length / 10
    p_go = length / 4

    # draw top part, arm
    basemap.drawgreatcircle(lon, lat+cd_offset, lon, lat+cd_offset+length,
                            color='k', linewidth=1.0)

    # draw top part pointer
    basemap.drawgreatcircle(lon, lat+cd_offset+length,
                            lon-p_w, lat+cd_offset+length-p_lo,
                            color='k', linewidth=1.0)
    basemap.drawgreatcircle(lon-p_w, lat+cd_offset+length-p_lo,
                            lon, lat+cd_offset+length+p_lo+p_go,
                            color='k', linewidth=1.5)
    basemap.drawgreatcircle(lon, lat+cd_offset+length+p_lo+p_go,
                            lon+p_w, lat+cd_offset+length-p_lo,
                            color='k', linewidth=1.5)
    basemap.drawgreatcircle(lon+p_w, lat+cd_offset+length-p_lo,
                            lon, lat+cd_offset+length,
                            color='k', linewidth=1.0)

    # draw lower arm
    basemap.drawgreatcircle(lon, lat-cd_offset, lon, lat-length-cd_offset,
                            color='k', linewidth=1.0)

#    # draw a diamond in the middle
#    basemap.drawgreatcircle(lon, lat+cd_offset, lon-cd_offset, lat,
#                            color='k', linewidth=1.0)
#    basemap.drawgreatcircle(lon-cd_offset, lat, lon, lat-cd_offset,
#                            color='k', linewidth=1.0)
#    basemap.drawgreatcircle(lon, lat-cd_offset, lon+cd_offset, lat,
#                            color='k', linewidth=1.0)
#    basemap.drawgreatcircle(lon+cd_offset, lat, lon, lat+cd_offset,
#                            color='k', linewidth=1.0)

    # draw a large 'N' in the middle
    basemap.drawgreatcircle(lon-cd_offset/2, lat-cd_offset/2,
                            lon-cd_offset/2, lat+cd_offset/2,
                            color='k', linewidth=1.0)
    basemap.drawgreatcircle(lon-cd_offset/2, lat+cd_offset/2,
                            lon+cd_offset/2, lat-cd_offset/2,
                            color='k', linewidth=1.0)
    basemap.drawgreatcircle(lon+cd_offset/2, lat-cd_offset/2,
                            lon+cd_offset/2, lat+cd_offset/2,
                            color='k', linewidth=1.0)


