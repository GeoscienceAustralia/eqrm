#!/usr/bin/env python

"""
A function to get a placement string for a GMT map.
 
Copyright 2007 by Geoscience Australia

"""


import os
import sys
import re
import time
import tempfile
import shutil

import eqrm_code.plotting.plot_config as cfg
import eqrm_code.plotting.utilities as util


################################################################################
# Get a GMT raw placement string.
################################################################################

# dictionary to map place string to placement code
placement_dict = {'ne':  ('x=map_width_deg-width_deg/2.0-margin_x_deg;'
                          'y=map_height_deg-height_deg/2.0-margin_y_deg;'),
                  'se':  ('x=map_width_deg-width_deg/2.0-margin_x_deg;'
                          'y=height_deg/2.0+margin_y_deg;'),
                  'sw':  ('x=width_deg/2.0+margin_x_deg;'
                          'y=height_deg/2.0+margin_y_deg;'),
                  'nw':  ('x=width_deg/2.0+margin_x_deg;'
                          'y=map_height_deg-height_deg/2.0-margin_y_deg;'),
                  'cn':  ('x=map_width_deg/2.0;'
                          'y=map_height_deg-height_deg/2.0-margin_y_deg;'),
                  'ce':  ('x=map_width_deg-width_deg/2.0-margin_x_deg;'
                          'y=map_height_deg/2.0;'),
                  'cs':  ('x=map_width_deg/2.0;'
                          'y=height_deg/2.0+margin_y_deg;'),
                  'cw':  ('x=width_deg/2.0+margin_x_deg;'
                          'y=map_height_deg/2.0;'),
                  'c':   ('x=map_width_deg/2.0;'
                          'y=map_height_deg/2.0;'),
                  'ncn': ('x=map_width_deg/2.0;'
                          'y=map_height_deg+height_deg/2.0+margin_y_deg;'),
                  'nne': ('x=map_width_deg-width_deg/2.0-margin_x_deg;'
                          'y=map_height_deg+height_deg/2.0+margin_y_deg;'),
                  'ene': ('x=map_width_deg+width_deg/2.0+margin_x_deg;'
                          'y=map_height_deg-height_deg/2.0-margin_y_deg;'),
                  'ece': ('x=map_width_deg+width_deg/2.0+margin_x_deg;'
                          'y=map_height_deg/2.0;'),
                  'ese': ('x=map_width_deg+width_deg/2.0+margin_x_deg;'
                          'y=height_deg/2.0+margin_y_deg;'),
                  'sse': ('x=map_width_deg-width_deg/2.0-margin_x_deg;'
                          'y=-height_deg/2.0-margin_y_deg;'),
                  'scs': ('x=map_width_deg/2.0;'
                          'y=-height_deg/2.0-margin_y_deg;'),
                  'ssw': ('x=width_deg/2.0+margin_x_deg;'
                          'y=-height_deg/2.0-margin_y_deg;'),
                  'wsw': ('x=-width_deg/2.0-margin_x_deg;'
                          'y=height_deg/2.0+margin_y_deg;'),
                  'wcw': ('x=-width_deg/2.0-margin_x_deg;'
                          'y=map_height_deg/2.0;'),
                  'wnw': ('x=-width_deg/2.0-margin_x_deg;'
                          'y=map_height_deg-height_deg/2.0-margin_y_deg;'),
                  'nnw': ('x=width_deg/2.0+margin_x_deg;'
                          'y=map_height_deg+height_deg/2.0+margin_y_deg;'),
                 }


def get_placement(place, extent, width=0.0, height=0.0, margin=0.04):
    """Calculate the placement for an object.

    place    where the object is to be place, either a string:
                 'NW', 'NE', 'SE', 'SW', 'CN', 'CE', etc
             or a tuple (lon, lat)
    extent   the map extent (ll_lat, ll_lon, ur_lat, ur_lon)
    width    width of object being placed in centimetres
    height   height of object being placed in centimetres
    margin   margin (fraction of width/height) (default=2%)

    All measurements are assumed to be decimal degrees.

    The returned position is assumed to be the centre of the object.

    Returns a tuple (lon, lat).

    """

    # if place is a tuple, just return it
    if isinstance(place, tuple):
        return place

    # otherwise, unpack the extent and get map width+height in degrees
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    map_width_deg = (ur_lon - ll_lon)
    map_height_deg = (ur_lat - ll_lat)

    # and margins in degrees (from percentages)
    margin_x_deg = map_width_deg * margin
    margin_y_deg = map_height_deg * margin

    # convert object width/height from centimetres to degrees
    (width_deg, height_deg) = util.convert_cm_lonlat(width, height, extent)
    width_deg -= ll_lon
    height_deg -= ll_lat

    # convert place to lower case, get code
    l_place = place.lower()
    try:
        val_str = placement_dict[l_place]
    except KeyError:
        raise RuntimeError("Unrecognised place string: '%s'" % place)

    # evaluate the code, this gets X/Y as degrees from lower left origin
    exec(val_str)

    # convert to absolute degrees
    x = ll_lon + x
    y = ll_lat + y

    return (x, y)


################################################################################
# Get a GMT psbasemap option string to draw a scale.
################################################################################

# ratio of scale width to map width
ScaleRatio = 1.0/10.0

# map place string to map width function call string
MapWidth = {'ne':  'util.lat_width(map_width_deg, ur_lat)',
            'se':  'util.lat_width(map_width_deg, ll_lat)',
            'sw':  'util.lat_width(map_width_deg, ll_lat)',
            'nw':  'util.lat_width(map_width_deg, ur_lat)',
            'cn':  'util.lat_width(map_width_deg, ur_lat)',
            'ce':  'util.lat_width(map_width_deg, centre_lat)',
            'cs':  'util.lat_width(map_width_deg, ll_lat)',
            'cw':  'util.lat_width(map_width_deg, centre_lat)',
            'c':   'util.lat_width(map_width_deg, centre_lat)',
            'ncn': 'util.lat_width(map_width_deg, ur_lat)',
            'nne': 'util.lat_width(map_width_deg, ur_lat)',
            'ene': 'util.lat_width(map_width_deg, ur_lat)',
            'ece': 'util.lat_width(map_width_deg, centre_lat)',
            'ese': 'util.lat_width(map_width_deg, ll_lat)',
            'sse': 'util.lat_width(map_width_deg, ll_lat)',
            'scs': 'util.lat_width(map_width_deg, ll_lat)',
            'ssw': 'util.lat_width(map_width_deg, ll_lat)',
            'wsw': 'util.lat_width(map_width_deg, ll_lat)',
            'wcw': 'util.lat_width(map_width_deg, centre_lat)',
            'wnw': 'util.lat_width(map_width_deg, ur_lat)',
            'nnw': 'util.lat_width(map_width_deg, ur_lat)',
           }

def get_scale_placement(place, extent):
    """Calculate the placement string for a scale.

    place   where the object is to be placed:
                'NW', 'NE', 'SE', 'SW', etc
             or
                a tuple (lon, lat, width)
    extent  the extent tuple (ll_lat, ll_lon, ur_lat, ur_lon)

    Returns a complete -L option string for psbasemap.

    """

    # unpack the extent
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent

    # get various measures of the map
    centre_lat = (ll_lat + ur_lat) / 2.0
    map_width_deg = (ur_lon - ll_lon)

    # if place arg is a string
    if isinstance(place, basestring):
        # get map width at centre lat
        map_width_km = util.lat_width(map_width_deg, centre_lat)

        # guess a realistic scale width in km, convert to degrees
        scale_width_km = int(int(map_width_km*ScaleRatio)/5) * 5
        if scale_width_km == 0:
            scale_width_km = 5
        scale_width_deg = map_width_deg*scale_width_km/map_width_km
        scale_height_deg = scale_width_deg/5.0

        # get lon/lat placement for the scale
        scale_place = get_placement(place, extent,
                                    width=scale_width_deg,
                                    height=scale_height_deg,
                                    margin=0.04)
        (scale_lon, scale_lat) = scale_place

        l_opt = ('-L%.3f/%.3f/%f/%dk+l+jt'
                 % (scale_lon, scale_lat, centre_lat, scale_width_km))
    else:
        # else it's a placement tuple (lon, lat, width)
        (lon, lat, width) = place
        l_opt = ('-L%.3f/%.3f/%f/%dk+l+jt'
                 % (lon, lat, centre_lat, width))


    return  l_opt


################################################################################
# Get a GMT psbasemap option string to draw a northpointer.
################################################################################

# ratio of northpointer size to map width
PointerRatio = 1.0/20.0


def get_northpointer_placement(place, extent):
    """Calculate the placement string for a northpointer.

    place   where the northpointer is to be placed, either:
                a placement string ('NW', 'NE', 'SE', 'SW', etc)
              or
                a tuple (lon, lat)
    extent  the extent tuple (ll_lat, ll_lon, ur_lat, ur_lon)

    Returns a complete -T option string for psbasemap.

    """

    # if place arg is a string
    if isinstance(place, basestring):
        # unpack the extent
        (ll_lat, ll_lon, ur_lat, ur_lon) = extent

        # get map width in degrees
        map_width_deg = (ur_lon - ll_lon)

        # get width+height of pointer in degrees
        pointer_width_deg = map_width_deg*PointerRatio
        pointer_height_deg = pointer_width_deg*5.5

        # get X/Y placement for the pointer
        pointer_place = get_placement(place, extent,
                                      width=pointer_width_deg,
                                      height=pointer_height_deg)
    else:
        pointer_place = place

    return  '"-T%.3f/%.3f/1.5c:w,e,s, :"' % pointer_place


