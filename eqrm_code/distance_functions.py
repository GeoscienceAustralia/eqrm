"""
Title: distance_functions.py

Author:  Peter Row, peter.row@ga.gov.au


Description: A group of functions that all calculate different
distance measurements.  The interface for each function is the same,
consisting of the following parameters:

  lat_sites        array of site latitudes
  lon_sites        array of site longitudes
  lat_events       array of event latitudes
  lon_events       array of event longitudes
  lengths          array of event lengths (km)
  azimuths         array of trace headings (start -> end)
  widths           array of event widths (km)
  dips             array of event dips
  depths           array of event depths
  depths_to_top    array of depths to the top of each events rupture plane
  projection       ??
  trace_start_lat  array of trace start latitudes
  trace_start_lon  array of trace start longitudes
  rupture_centroid_x    array of the x of the rupture centroid in local coordinates
                        the start of the trace is the origin of the local coords
  rupture_centroid_y    array of the y of the rupture centroid in local coordinates
                        the start of the trace is the origin of the local coords

These functions are built into a dictionary.

Version: $Revision: 1360 $
ModifiedBy: $Author: dgray $
ModifiedDate: $Date: 2009-12-08 17:41:02 +1100 (Tue, 08 Dec 2009) $

Copyright 2007 by Geoscience Australia
"""

from scipy import newaxis, sqrt, pi, cos, sin, where, reshape, arctan, sign
from scipy import tan, arcsin, arccos, zeros

from .projections import azimuthal_orthographic_ll_to_xy as ll2xy

csc = lambda x: 1 / sin(x)
sec = lambda x: 1 / cos(x)
cot = lambda x: 1 / tan(x)

# constant used to convert degrees to radians: rad = deg * DegreesToRadians
DegreesToRadians = pi / 180.0

DISTANCE_LIMIT = 0.000001
#DISTANCE_LIMIT = 1.0


def As_The_Cockey_Flies(lat0, lon0, lat, lon):
    # Algorithm from GA website
    # Uses spherical geometry (rather than a projection)
    # to calculate epicentral distance
    lat = lat[:, newaxis]
    lon = lon[:, newaxis]
    L1 = lat0 * (pi / 180)
    L2 = lat * (pi / 180)
    DG = (lon - lon0) * (pi / 180)
    D = 1.852 * 60 * 180 / pi * \
        arccos(sin(L1) * sin(L2) + cos(L1) * cos(L2) * cos(DG))
    return D


def Hypocentral(
        lat_sites, lon_sites, lat_events, lon_events, lengths, azimuths,
        widths, dips, depths, depths_to_top, projection, trace_start_lat,
        trace_start_lon, rupture_centroid_x, rupture_centroid_y):
    # Increase the rank of lat_sites to (num_sites,1)
    # Now (lat_sites+lat_events).shape = (num_sites,num_events)
    lat_sites = lat_sites[:, newaxis]
    lon_sites = lon_sites[:, newaxis]

    # get the coordinates of the site, with events as the origin.
    (site_x, site_y) = projection.\
        angular_to_cartesian(lat_sites, lon_sites,
                             lat_events, lon_events, azimuths)

    return sqrt(site_x * site_x + site_y * site_y + depths * depths)


def Obsolete_Mendez_hypocentral(
        lat_sites, lon_sites, lat_events, lon_events, lengths,
        azimuths, widths, dips, depths, depths_to_top, projection,
        trace_start_lat, trace_start_lon, rupture_centroid_x,
        rupture_centroid_y):
    # Increase the rank of lat_sites to (num_sites,1)
    # Now (lat_sites+lat_events).shape = (num_sites,num_events)
    lat_sites = lat_sites[:, newaxis]
    lon_sites = lon_sites[:, newaxis]

    # find vector from site to event_centroid
    # using the same values as Matlab
    x0 = rupture_centroid_x
    y0 = rupture_centroid_y

    (x, y) = projection.angular_to_cartesian(lat_sites, lon_sites,
                                             trace_start_lat, trace_start_lon,
                                             azimuths)

    return sqrt((x - x0) ** 2 + (y - y0) ** 2 + depths * depths)


def Epicentral(lat_sites, lon_sites, lat_events, lon_events, lengths, azimuths,
               widths, dips, depths, depths_to_top, projection, trace_start_lat,
               trace_start_lon, rupture_centroid_x, rupture_centroid_y):
    lat_sites = lat_sites[:, newaxis]
    lon_sites = lon_sites[:, newaxis]

    # get the coordinates of the site, with events as the origin.
    (site_x, site_y) = projection.\
        angular_to_cartesian(lat_sites, lon_sites,
                             lat_events, lon_events, azimuths)

    return sqrt(site_x * site_x + site_y * site_y)


def Obsolete_Mendez_epicentral(
        lat_sites, lon_sites, lat_events, lon_events, lengths,
        azimuths, widths, dips, depths, depths_to_top, projection,
        trace_start_lat, trace_start_lon, rupture_centroid_x,
        rupture_centroid_y):
    lat_sites = lat_sites[:, newaxis]
    lon_sites = lon_sites[:, newaxis]

    # find vector from site to event_centroid
    # using the same values as Matlab
    x0 = rupture_centroid_x
    y0 = rupture_centroid_y

    (x, y) = projection.angular_to_cartesian(lat_sites, lon_sites,
                                             trace_start_lat, trace_start_lon,
                                             azimuths)

    # find vector from site to event_centroid
    # using the same values as Matlab
    return sqrt((x - x0) ** 2 + (y - y0) ** 2)


def Mendez_rupture(lat_sites, lon_sites, lat_events, lon_events, lengths,
                   azimuths, widths, dips, depths, depths_to_top, projection,
                   trace_start_lat, trace_start_lon, rupture_centroid_x,
                   rupture_centroid_y):
    lat_sites = lat_sites[:, newaxis]
    lon_sites = lon_sites[:, newaxis]

    rad = pi / 180
    cos_dip = cos(dips * rad)
    sin_dip = sin(dips * rad)

    x0 = rupture_centroid_x
    y0 = rupture_centroid_y

    (x, y) = projection.angular_to_cartesian(lat_sites, lon_sites,
                                             trace_start_lat, trace_start_lon,
                                             azimuths)

    # find vector from site to event_centroid
    # using the same values as Matlab
    return Mendez_Rupture_xy(cos_dip, sin_dip, lengths, widths, depths,
                             x0, y0, x, y)


def Obsolete_Rupture(
        lat_sites, lon_sites, lat_events, lon_events, lengths, azimuths,
        widths, dips, depths, depths_to_top, projection, trace_start_lat,
        trace_start_lon, rupture_centroid_x, rupture_centroid_y):
    lat_sites = lat_sites[:, newaxis]
    lon_sites = lon_sites[:, newaxis]

    rad = pi / 180
    cos_dip = cos(dips * rad)
    sin_dip = sin(dips * rad)

    # project lat,lon to local x,y
    (x, y) = projection.angular_to_cartesian(lat_sites, lon_sites,
                                             lat_events, lon_events,
                                             azimuths)

    # x, y are the sites location vectors in the local co-ord system
    return Obsolete_Rupture_xy(x, y, lengths, widths, cos_dip, sin_dip, depths)


def Mendez_Rupture_xy(cos_dip, sin_dip, lengths, widths, depths, x0, y0, x, y):

    # find the closest points to site on the infinite rupure plane
    y_closest = y * cos_dip * cos_dip
    z_closest = y * cos_dip * sin_dip
    x_closest = x.copy()

    z = 0

    # find the closest points to site on the bounded rupture plane
    # by truncating x_closest,y_closest,z_closest.
    xhi = ((x0 + lengths / 2) < x_closest)  # site 'North' of fault
    xlo = ((x0 - lengths / 2) > x_closest)  # site 'South' of fault

    x_closest = where(xhi, (x0 + lengths / 2), x_closest)
    x_closest = where(xlo, (x0 - lengths / 2), x_closest)

    yhi = ((y0 + widths * cos_dip / 2) < y_closest)  # site 'East' of fault
    ylo = ((y0 - widths * cos_dip / 2) > y_closest)  # site 'West' of fault

    y_closest = where(yhi, (y0 + widths * cos_dip / 2), y_closest)
    y_closest = where(ylo, (y0 - widths * cos_dip / 2), y_closest)

    # note: yes, we are correctly using yhi & ylo - see Distance.doc diagram
    # site closer to bottom edge
    z_closest = where(yhi, (depths + widths * sin_dip / 2), z_closest)
    # site closer to top edge
    z_closest = where(ylo, (depths - widths * sin_dip / 2), z_closest)

    rupture_distance = sqrt(
        (x_closest - x) ** 2 + (y_closest - y) ** 2 + (z_closest - z) ** 2)
    return where(rupture_distance < DISTANCE_LIMIT,
                 DISTANCE_LIMIT, rupture_distance)


def Obsolete_Rupture_xy(x, y, lengths, widths, cos_dip, sin_dip, depths):
    """
    x, y are the site locations on a 2D surface, referenced to a local
    co-ordinate system.  The mid point of the rupture or the mid point of the
    rupture trace is the origin and the direction of the rupture trace is
    the +ve x direction.
    """

    y_rup = y * cos_dip - depths * sin_dip
    z_rup = y * sin_dip + depths * cos_dip

    # rotate so y is on the plate
    # see Distances.doc
    (y, z) = (y_rup, z_rup)

    # work with absolute values
    x = abs(x)
    y = abs(y)

    l = lengths / 2
    w = widths / 2

    # if x is on the fault, set it to the edge (see next step)
    if l.shape == (1, 1):
        l = reshape(l, (1))
    x = where(x < l, l, x)

    if w.shape == (1, 1):
        w = reshape(w, (1))
    y = where(y < w, w, y)

    # take the distance from x to the edge of the fault
    x = x - l
    y = y - w

    rupture_distance = sqrt(x * x + y * y + z * z)

    return where(rupture_distance < DISTANCE_LIMIT,
                 DISTANCE_LIMIT, rupture_distance)


def Joyner_Boore_xy(lat_sites,
                    lon_sites,
                    lat_events,
                    lon_events,
                    lengths,
                    azimuths,
                    widths,
                    dips,
                    depths,
                    depths_to_top,
                    projection,
                    trace_start_lat,
                    trace_start_lon,
                    rupture_centroid_x,
                    rupture_centroid_y):
    """ #FIXME This code needs comments """

    lat_sites = lat_sites[:, newaxis]
    lon_sites = lon_sites[:, newaxis]

    rad = pi / 180
    cos_dip = cos(dips * rad)
    sin_dip = sin(dips * rad)

    x0 = rupture_centroid_x
    y0 = rupture_centroid_y

    (x, y) = ll2xy(lat_sites, lon_sites, trace_start_lat,
                   trace_start_lon, azimuths)

    # STARTING Matlab code:
    x = abs(x - x0)  # distance from x to rupture_centroid_x
    y = abs(y - y0)  # distance from y to rupture_centroid_y

    l = lengths / 2.0        # length from start/end to rupture_centroid_x
    w = cos_dip * widths / 2.0  # width from start/end to rupture_centroid_x

    if l.shape == (1, 1):
        l = reshape(l, (1))
    x = where(x < l, l, x)    # max(l, x)

    if w.shape == (1, 1):
        w = reshape(w, (1))
    y = where(y < w, w, y)    # max(w, y)

    x = x - l  # distance from x to edge of rupture plane
    y = y - w  # distance from y to edge of rupture plane

    return x, y


def Joyner_Boore(*args):
    """ #FIXME This code needs comments """

    x, y = Joyner_Boore_xy(*args)

    joyner_boore_distance = sqrt(x * x + y * y)
    return where(joyner_boore_distance < DISTANCE_LIMIT,
                 DISTANCE_LIMIT, joyner_boore_distance)


def Horizontal(lat_sites, lon_sites, lat_events, lon_events, lengths,
               azimuths, widths, dips, depths, depths_to_top, projection,
               trace_start_lat, trace_start_lon, rupture_centroid_x,
               rupture_centroid_y):
    """Distance function that calculates 'Rx'.

    Rx is the shortest horizontal distance (km) from a site to the line defined
    by extending the event fault trace to infinity.

                 ^ north
                /
               /\azimuth
        start 0======---+--------
               \        |
                \       |
                 \      |
                  \     | Rx
                   \    |
                    \   |
                     \  |
                      \ |
                       \|
                        .
                      site

    We get Rx by using ll2xy() to convert start/site positions to x and y
    in the coordinates relative to start and with axes shown in fig 3.1
    of the manual.  Rx is therefore the y value.
    """

    # get correct dimensionality
    lat_sites = lat_sites[:, newaxis]
    lon_sites = lon_sites[:, newaxis]

    # get x,y position of sites w.r.t. origin 'start'
    (_, Rx) = ll2xy(lat_sites, lon_sites, trace_start_lat,
                    trace_start_lon, azimuths)

    # limit distance to 1.0km minimum
    return where(abs(Rx) < DISTANCE_LIMIT,
                 sign(Rx) * DISTANCE_LIMIT, Rx)


def Kaklamanos_Ry(*args):
    """
    Calculation for Ry, the distance from the site to the surface projection of
    the ruptured area, measured parallel to the strike. It is essentially the y
    component of Rjb, which in the case of Joyner_Boore() is actually x
    (Fig. 5 Kaklamanos et al. (2011)
    """

    x, y = Joyner_Boore_xy(*args)

    # The x component of Joyner_Boore_xy is the y component that the
    # Kaklamanos et al. (2011) functions are after.
    Ry = x

    return Ry


def Kaklamanos_Rrup_prime(Rx, widths, dips, depths_to_top):
    """
    Calculation for the in-plane rupture distance based on 3 zones
    (Fig. 4 Kaklamanos et al. (2011)


    ~-----------Zone A--------->|<--Zone B-->|<--Zone C--~
    ____________________________|____________|____________
          ^     |              /            /   #####   ^
          |     |             /            /           /
          |     |            /            /   Ground _/
          |     |           /            /    Surface
          |     |          /            /
          |     |         /            /
          |     |        /            /
        depth   |       /            /
          |     |      /            /
          |     |     /            /
          |     |    /            /
          |     |   /            /
          |     |  /            /
          |     | /            /
       ___._____|/____        /
                / dip        /
               / #          /
              /   #        /
             /^    #      /
               \    #    /
             width   #  / 90 degrees
                 \    #/
                  \   /
                   . /
                    /
    """

    d = dips * pi / 180  # define dips in terms of radians
    Ztor = depths_to_top
    W = widths

    Rrup_p = zeros(Rx.shape)

    # Zone A
    Rrup_p = where(Rx < Ztor * tan(d),
                   sqrt(Rx ** 2 + Ztor ** 2),
                   Rrup_p)

    # Zone B
    Rrup_p = where((Rx >= Ztor * tan(d)) & (Rx <= Ztor * tan(d) + W * sec(d)),
                   Rx * sin(d) + Ztor * cos(d),
                   Rrup_p)

    # Zone C
    Rrup_p = where(Rx > Ztor * tan(d) + W * sec(d),
                   sqrt((Rx - W * cos(d)) ** 2 + (Ztor + W * sin(d)) ** 2),
                   Rrup_p)

    return Rrup_p


def Kaklamanos_Vertical_Rrup(Rjb, depths_to_top):
    return sqrt(Rjb ** 2 + depths_to_top ** 2)


def Kaklamanos_Non_Vertical_Rrup(lat_sites,
                                 lon_sites,
                                 lat_events,
                                 lon_events,
                                 lengths,
                                 azimuths,
                                 widths,
                                 dips,
                                 depths,
                                 depths_to_top,
                                 projection,
                                 trace_start_lat,
                                 trace_start_lon,
                                 rupture_centroid_x,
                                 rupture_centroid_y):

    # Calculate Rx
    Rx = Horizontal(lat_sites,
                    lon_sites,
                    lat_events,
                    lon_events,
                    lengths,
                    azimuths,
                    widths,
                    dips,
                    depths,
                    depths_to_top,
                    projection,
                    trace_start_lat,
                    trace_start_lon,
                    rupture_centroid_x,
                    rupture_centroid_y)

    # Calculate Rrup_inplane
    Rrup_prime = Kaklamanos_Rrup_prime(Rx, widths, dips, depths_to_top)

    # Calculate Ry
    Ry = Kaklamanos_Ry(lat_sites,
                       lon_sites,
                       lat_events,
                       lon_events,
                       lengths,
                       azimuths,
                       widths,
                       dips,
                       depths,
                       depths_to_top,
                       projection,
                       trace_start_lat,
                       trace_start_lon,
                       rupture_centroid_x,
                       rupture_centroid_y)

    Rrup = sqrt(Rrup_prime ** 2 + Ry ** 2)

    return Rrup


def Rupture(lat_sites,
            lon_sites,
            lat_events,
            lon_events,
            lengths,
            azimuths,
            widths,
            dips,
            depths,
            depths_to_top,
            projection,
            trace_start_lat,
            trace_start_lon,
            rupture_centroid_x,
            rupture_centroid_y):
    """
    Implementation of Rupture Distance as specified by
    Kaklamanos et al. (2011)
    """

    # Calculate Rjb
    Rjb = Joyner_Boore(lat_sites,
                       lon_sites,
                       lat_events,
                       lon_events,
                       lengths,
                       azimuths,
                       widths,
                       dips,
                       depths,
                       depths_to_top,
                       projection,
                       trace_start_lat,
                       trace_start_lon,
                       rupture_centroid_x,
                       rupture_centroid_y)

    Rrup_non_vertical = Kaklamanos_Non_Vertical_Rrup(lat_sites,
                                                     lon_sites,
                                                     lat_events,
                                                     lon_events,
                                                     lengths,
                                                     azimuths,
                                                     widths,
                                                     dips,
                                                     depths,
                                                     depths_to_top,
                                                     projection,
                                                     trace_start_lat,
                                                     trace_start_lon,
                                                     rupture_centroid_x,
                                                     rupture_centroid_y)

    Rrup_vertical = Kaklamanos_Vertical_Rrup(Rjb, depths_to_top)

    # Calculate Rrup
    Rrup = where(dips == 90.0, Rrup_vertical, Rrup_non_vertical)

    return where(Rrup < DISTANCE_LIMIT, DISTANCE_LIMIT, Rrup)


###################
# END OF FUNCTIONS#
###################

"""No functions past this step will be included in the table"""
__local_functions = locals().copy()  # all the functions in the local namespace
# Note that this is a copy, otherwise __local_functions would point to itself

distance_functions = {}
for function_name in __local_functions.keys():
    # for all functions in the local namespace
    # WARNING: This also includes all scipy functions, etc.
    if not function_name.startswith('_'):  # If it's not private
        function = __local_functions[function_name]
        distance_functions[function_name] = function
