"""Relations between various earthquake parameters - Mw to length, etc.
 Title: conversions.py

  Author:  Peter Row, peter.row@ga.gov.au

  Description: Relations between various earthquake parameters - Mw to length,
  ML to Mw, etc.


  Version: $Revision: 995 $
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-06-30 11:51:34 +1000 (Tue, 30 Jun 2009) $

  Copyright 2007 by Geoscience Australia
"""

from scipy import (vectorize, sqrt, sin, minimum, pi, where, asarray,
                   exp, log, power)
import math

def Johnston_01_ML(Mw):
    """
    relationship developed by Arch Johnston, 1989

    coefficients per comms (01)
    """
    C1=0.473
    C2=0.145
    C3=3.45
    return (C1+(C1**2-4*C2*(C3-Mw))**0.5)/(2*C2)

def Johnston_89_Mw(ML):
    return 3.45-0.473*ML+0.145*(ML**2)

def Wells_and_Coppersmith_94_length(Mw):
    return 10.**(0.69*Mw - 3.22)

def modified_Wells_and_Coppersmith_94_area(Mw):
    return 10.**(Mw-4.02)

def modified_Wells_and_Coppersmith_94_width(dip,Mw,area,fault_width=15.0):
    #FIXME DSG-EQRM Does it make sence to have a default width value?
    # based on Wells_and_Coppersmith 94 with modification
    if Mw > 5.5:
        f=sqrt(sqrt(1+2*(Mw-5.5)*sin(dip*pi/180.)))**-1
    else: f=1.0
    if fault_width is not None:
        return minimum(f*sqrt(area),fault_width)
    else:
        return f*sqrt(area)

modified_Wells_and_Coppersmith_94_width = vectorize(
    modified_Wells_and_Coppersmith_94_width)

def depth(depth_top_seismogenic,dip,Mw,fault_width=None):
    """
    depth_top_seismogenic - depth to the top of the seismmogenic region, km.
    dip: dip of the seismmogenic region, degrees
    """
    if fault_width is None:
        fault_width = 15
    rad=pi/180

    f2=1+((Mw-4.0)/2)
    f2=where(f2<1,1,f2)
    f2=where(f2>2,2,f2)

    depth1=depth_top_seismogenic+f2/3*fault_width*sin(dip*rad)
    depth2=depth_top_seismogenic+fault_width*sin(dip*rad)-0.5*Mw*sin(dip*rad)
    depth=where(depth1<depth2,depth1,depth2)
    return depth

def calc_depth_to_top(depth, width, delta):
    """Given a fault details, get depth to rupture top.

    depth  depth to fault centroid (km)
    width  width of rupture (km)
    delta  fault dip angle (degrees)

    All three parameters are expected to be numpy arrays.

    Returns Rtor, depth to top of rupture (km)
    Rtor = depth - (width/2)*sin(delta)
    """

    # check dimensions of all three params the same
    try:
        msg = ('Expected depth.shape == width.shape, %s != %s'
               % (str(depth.shape), str(width.shape)))
    except AttributeError:
        raise AssertionError('calc_depth_to_top: expect numpy.array params')
    assert depth.shape == width.shape, msg

    try:
        msg = ('Expected depth.shape == delta.shape, %s != %s'
               % (str(depth.shape), str(delta.shape)))
    except AttributeError:
        raise AssertionError('calc_depth_to_top: expect numpy.array params')
    assert depth.shape == delta.shape, msg

    # convert dip angle in degrees to radians
    delta_rad = delta*math.pi/180.0

    # get and return Rtor
    return depth - (width/2)*sin(delta_rad)


# precalculate constants for convert_Vs30_to_Z10()
Ch_378_7_pow_8 = math.pow(378.7, 8)
Ch_3_82_div_8 = 3.82/8.0

def convert_Vs30_to_Z10(Vs30):
    """Convert a Vs30 value to an estimated V1.0 value.

    This function will handle both scalar and scipy array values of Z10.

    Formula taken from equation (1) of:
    Chiou.B.S.-J., Youngs R.R., 2008 An NGA Model for the Average Horizontal
    Component of Peak Ground Motion and Response Spectra,
    Earthquake Spectra 24, 173-215.
    """

    return exp(28.5 - Ch_3_82_div_8*log(power(Vs30, 8) + Ch_378_7_pow_8))


def convert_Z10_to_Z25(Z10):
    """Convert a Z1.0 value to a Z2.5 value.

    This function will handle both scalar and scipy array values of Z10.

    Formula taken from equation (6.3) of:
    Campbell-Bozorgnia NGA Ground Motion Relations for the Geometric Mean
    Horizontal Component of Peak and Spectral Ground Motion Parameters.
    Kenneth W. Campbell and Yousef Bozorgnia, PEER 2007/02.
    """

    return 0.519 + 3.595*Z10


def azimuth_of_trace(start_lat, start_lon, end_lat, end_lon):
    """Calculate a trace azimuth given start and end positions.

    start_lat  latitude of start point
    start_lon  longitude of start point
    end_lat    latitude of end point
    end_lon    longitude of end point

    Returns azimuth at start point in degrees, in range [0, 360).
    """

    dx = end_lon - start_lon
    dy = end_lat - start_lat
    azimuth = math.atan2(dx*math.cos(start_lat*math.pi/180.0), dy)*180.0/math.pi
    if azimuth < 0.0:
        azimuth += 360.0

    return azimuth

###################
# END OF FUNCTIONS#
###################

"""No functions past this step will be included in the table"""
__local_functions = locals().copy() #all the functions in the local namespace
# Note that this is a copy, otherwise __local_functions would point to itself

conversion_functions = {}
for function_name in __local_functions.keys():
    #for all functions in the local namespace

    if not function_name.startswith('__'): #If it's not private
        function = __local_functions[function_name]
        conversion_functions[function_name]=function
