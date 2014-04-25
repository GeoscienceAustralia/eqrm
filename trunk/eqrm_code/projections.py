"""
 Title: projections.py

  Author:  Duncan Gray, duncan.gray@ga.gov.au

  Description: Converting from lats and longs to x and y and visa versa.

  Version: $Revision: 920 $
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-04-01 16:27:50 +1100 (Wed, 01 Apr 2009) $
  PLEASE NOTE you need to be very careful using these functions outside
  of EQRM.  In EQRM the x axis runs along the rupture trace. the y axis
  is perpendicular to the rupture trace. please see the images of the
  orientation and dimension of the rupture plane in both 3D and a 2D
  in the eqrm manual.

  Copyright 2007 by Geoscience Australia
"""

from scipy import cos, sin, arccos

PI_DIV_180 = 0.017453292519943295

# FIXME This should not be a class.  It should be two functions.


class _Projection(object):

    """
    Strange class.
    Seems to hold two functions.

    """

    def __init__(self, ll_to_xy, xy_to_ll, R=6367.0):
        """
        This class is instanciated at the end of this file
        azimuthal_orthographic=Projection(azimuthal_orthographic_ll_to_xy,\
                                  azimuthal_orthographic_xy_to_ll)
        """
        self.ll_to_xy = ll_to_xy
        self.xy_to_ll = xy_to_ll
        self.R = R

    def angular_to_cartesian(self, lat, lon, lat0, lon0, azimuth=0):
        return self.ll_to_xy(lat, lon, lat0, lon0, azimuth, self.R)

    def cartesian_to_angular(self, x, y, lat0, lon0, azimuth=0):
        return self.xy_to_ll(x, y, lat0, lon0, azimuth, self.R)


def __rotate_frame_back(x, y, azimuth):
    return __rotate_frame(x, y, -azimuth)


def __rotate_frame(x, y, azimuth):
    """
    as per p28 of eqrm manual

    This rotates the coordinate system round azimuth
    """
    c = cos(azimuth * PI_DIV_180)
    s = sin(azimuth * PI_DIV_180)
    x_rotate = +c * x + s * y
    y_rotate = -s * x + c * y
    return x_rotate, y_rotate


def azimuthal_orthographic_ll_to_xy(lat, lon, lat0, lon0, azimuth=0, R=6367.0):
    """
    lat,lon = point for conversion to x,y
    lat0,lon0 = origin of coordinate system

    assumes that longitude increases towards the east
    PLEASE NOTE you need to be very careful using these functions outside
    of EQRM.  In EQRM the x axis runs along the rupture trace. the y axis
    is perpendicular to the rupture trace.
    """
    x = R * PI_DIV_180 * (lat - lat0)
    y = R * PI_DIV_180 * (lon - lon0) * cos(lat * PI_DIV_180)
    x, y = __rotate_frame(x, y, azimuth)
    return x, y


def azimuthal_orthographic_xy_to_ll(x, y, lat0, lon0, azimuth=0, R=6367.0):
    """
    x,y = point for conversion to lat,lon
    lat0,lon0 = origin of coordinate system

    assumes that longitude increases towards the east
    PLEASE NOTE you need to be very careful using these functions outside
    of EQRM.  In EQRM the x axis runs along the rupture trace. the y axis
    is perpendicular to the rupture trace.
    """
    # x = site x, y = site x
    # lat0 = origin (event latitude), lon0 = origin (event longitude)
    # assumes that longitude increases towards the east
    x, y = __rotate_frame_back(x, y, azimuth)
    lat = x / (R * PI_DIV_180) + lat0
    lon = y / (R * PI_DIV_180) / cos(lat0 * PI_DIV_180) + lon0
    return lat, lon

azimuthal_orthographic = _Projection(azimuthal_orthographic_ll_to_xy,
                                     azimuthal_orthographic_xy_to_ll)
###################
# END OF FUNCTIONS#
###################

"""No functions past this step will be included in the table"""
__local_functions = locals().copy()  # all the functions in the local namespace
# Note that this is a copy, otherwise __local_functions would point to itself

projections = {}
for name in __local_functions.keys():
    # for all functions in the local namespace
    obj = __local_functions[name]
    if not name == 'Projection':
        if isinstance(obj, _Projection):
            projections[name] = obj
