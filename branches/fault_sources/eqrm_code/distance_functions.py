"""
 Title: distance_functions.py
  
  Author:  Peter Row, peter.row@ga.gov.au


  Description: A group of functions that all calculate different
  distance measurements.  The interface for each function is the same.

  This functions are built into a dictionary.


  Version: $Revision: 1360 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-12-08 17:41:02 +1100 (Tue, 08 Dec 2009) $
  
  Copyright 2007 by Geoscience Australia
"""

from scipy import newaxis, sqrt, pi, cos, sin, where, reshape

from projections import azimuthal_orthographic_ll_to_xy as ll2xy
 
    
def Hypocentral(lat_sites,lon_sites,lat_events,lon_events,
                lengths,azimuths,widths,dips,depths,
                projection,trace_start_lat,trace_start_lon,
                trace_start_x,trace_start_y):
    # Increase the rank of lat_sites to (num_sites,1)
    # Now (lat_sites+lat_events).shape = (num_sites,num_events)
    lat_sites=lat_sites[:,newaxis]
    lon_sites=lon_sites[:,newaxis]

    # get the coordinates of the site, with events as the origin.
    site_x,site_y=projection.angular_to_cartesian(lat_sites,lon_sites,
                                                  lat_events,lon_events,
                                                  azimuths)
    
    hypocentral_distance=sqrt(site_x*site_x+site_y*site_y+depths*depths)
    return hypocentral_distance

def Mendez_hypocentral(lat_sites,lon_sites,lat_events,lon_events,
                       lengths,azimuths,widths,dips,depths,
                       projection,trace_start_lat,trace_start_lon,
                       trace_start_x,trace_start_y):
    # Increase the rank of lat_sites to (num_sites,1)
    # Now (lat_sites+lat_events).shape = (num_sites,num_events)
    lat_sites=lat_sites[:,newaxis]
    lon_sites=lon_sites[:,newaxis]    
    
    # find vector from site to event_centroid
    # using the same values as Matlab
    x0=-trace_start_x
    y0=-trace_start_y
    
    x,y=projection.angular_to_cartesian(lat_sites,lon_sites,
                                        trace_start_lat,
                                        trace_start_lon,
                                        azimuths)

    distance=sqrt((x-x0)**2+(y-y0)**2+depths*depths)
    return distance

def Epicentral(lat_sites,lon_sites,lat_events,lon_events,
               lengths,azimuths,widths,dips,depths,
               projection,trace_start_lat,trace_start_lon,
               trace_start_x,trace_start_y):
    lat_sites=lat_sites[:,newaxis]
    lon_sites=lon_sites[:,newaxis]
    
    # get the coordinates of the site, with events as the origin.
    site_x,site_y=projection.angular_to_cartesian(lat_sites,lon_sites,
                                                  lat_events,lon_events,
                                                  azimuths)
    
    epicentral_distance=sqrt(site_x*site_x+site_y*site_y)
    return epicentral_distance

def Mendez_epicentral(lat_sites,lon_sites,lat_events,lon_events,
                      lengths,azimuths,widths,dips,depths,
                      projection,trace_start_lat,trace_start_lon,
                      trace_start_x,trace_start_y):
    lat_sites=lat_sites[:,newaxis]
    lon_sites=lon_sites[:,newaxis]
    
    # find vector from site to event_centroid
    # using the same values as Matlab
    x0=-trace_start_x
    y0=-trace_start_y
    
    x,y=projection.angular_to_cartesian(lat_sites,lon_sites,
                                        trace_start_lat,
                                        trace_start_lon,
                                        azimuths)
    # find vector from site to event_centroid
    # using the same values as Matlab
    return sqrt((x-x0)**2+(y-y0)**2)


def Mendez_rupture(lat_sites,lon_sites,lat_events,lon_events,lengths,
                   azimuths,widths,dips,depths,
                   projection,trace_start_lat,trace_start_lon,
                   trace_start_x,trace_start_y):
    
    lat_sites=lat_sites[:,newaxis]
    lon_sites=lon_sites[:,newaxis]
    
    rad=pi/180
    cos_dip=cos(dips*rad)
    sin_dip=sin(dips*rad)

    x0=-trace_start_x
    y0=-trace_start_y
    
    x,y=projection.angular_to_cartesian(lat_sites,lon_sites,
                                        trace_start_lat,
                                        trace_start_lon,
                                        azimuths)
    # find vector from site to event_centroid
    # using the same values as Matlab
    return Mendez_Rupture_xy(cos_dip,sin_dip,lengths,widths,depths,x0,y0,x,y)

def Rupture(lat_sites,lon_sites,lat_events,lon_events,lengths,azimuths,
            widths,dips,depths,
            projection,trace_start_lat,trace_start_lon,
            trace_start_x,trace_start_y):  
    lat_sites=lat_sites[:,newaxis]
    lon_sites=lon_sites[:,newaxis]
    
    rad=pi/180
    cos_dip=cos(dips*rad)
    sin_dip=sin(dips*rad)
    
    x,y=projection.angular_to_cartesian(lat_sites,lon_sites,
                                        lat_events,lon_events,
                                        azimuths)
    # project lat,lon to x,y
    return Rupture_xy(x,y,lengths,widths,cos_dip,sin_dip,depths)

def Mendez_Rupture_xy(cos_dip,sin_dip,lengths,widths,depths,x0,y0,x,y):
    
    # find the closest points to site on the infinite rupure plane
    y_closest=y*cos_dip*cos_dip
    z_closest=y*cos_dip*sin_dip
    x_closest=x.copy()
    
    z=0

    # find the closest points to site on the bounded rupture plane
    # by truncating x_closest,y_closest,z_closest.
    
    xhi = ((x0+lengths/2)<x_closest) # site 'North' of fault
    xlo = ((x0-lengths/2)>x_closest) # site 'South' of fault
    
    x_closest = where(xhi,(x0+lengths/2),x_closest)
    x_closest = where(xlo,(x0-lengths/2),x_closest)
    
    yhi = ((y0+widths*cos_dip/2)<y_closest) # site 'East' of fault
    ylo = ((y0-widths*cos_dip/2)>y_closest) # site 'West' of fault
    
    y_closest = where(yhi,(y0+widths*cos_dip/2),y_closest)
    y_closest = where(ylo,(y0-widths*cos_dip/2),y_closest)
    
    # note: yes, we are correctly using yhi & ylo - see Distance.doc diagram
    # site closer to bottom edge
    z_closest = where(yhi,(depths+widths*sin_dip/2),z_closest)
    # site closer to top edge
    z_closest = where(ylo,(depths-widths*sin_dip/2),z_closest) 
    
    rupture_distance=sqrt((x_closest- x)**2+(y_closest-y)**2+(z_closest-z)**2)
    rupture_distance=where(rupture_distance<1,1,rupture_distance)
    return rupture_distance

def Rupture_xy(x,y,lengths,widths,cos_dip,sin_dip,depths):
    
    y_rup=(y*cos_dip-depths*sin_dip)
    z_rup=(y*sin_dip+depths*cos_dip)
    # rotate so y is on the plate
    # see Distances.doc
    y,z=y_rup,z_rup

    # work with absolute values
    x=abs(x)
    y=abs(y)

    l=lengths/2   
    w=widths/2
    # if x is on the fault, set it to the edge (see next step)
    if l.shape == (1,1):
        l = reshape(l,(1))
    x=where(x<l,l,x)

    if w.shape == (1,1):
        w = reshape(w,(1))    
    y=where(y<w,w,y)

    # take the distance from x to the edge of the fault
    x=x-l
    y=y-w
    
    rupture_distance=sqrt(x*x+y*y+z*z)
    rupture_distance=where(rupture_distance<1,1,rupture_distance)
    return rupture_distance

def Joyner_Boore(lat_sites,lon_sites,lat_events,lon_events,lengths,
                 azimuths,widths,dips,depths,
                 projection,trace_start_lat,trace_start_lon,
                 trace_start_x,trace_start_y):
    """
    #FIXME This code needs comments
    """
    import copy
    # Trying to avoid "ValueError: array dimensions must agree"
    # errors in the 'where' statement further on. 
#     lengths = copy.copy(lengths)
#     if lengths.shape == (1,1):
#         lengths.shape = (1)
#     widths = copy.copy(widths)
#     if widths.shape == (1,1):
#         widths.shape = (1)
    lat_sites=lat_sites[:,newaxis]
    lon_sites=lon_sites[:,newaxis]
    
    rad=pi/180
    cos_dip=cos(dips*rad)
    sin_dip=sin(dips*rad)
    
    x0=-trace_start_x
    y0=-trace_start_y
    
    x,y=ll2xy(lat_sites,lon_sites,trace_start_lat,trace_start_lon,azimuths)

    # STARTING Matlab code:
    
    x=abs(x-x0)
    y=abs(y-y0)
    
    l=lengths/2   
    w=cos_dip*widths/2
    if l.shape == (1,1):
        l = reshape(l,(1))
    x=where(x<l,l,x)

    if w.shape == (1,1):
        w = reshape(w,(1))    
    y=where(y<w,w,y)
    
    x=x-l
    y=y-w
    
    joyner_boore_distance=sqrt(x*x+y*y)
    
    joyner_boore_distance=where(joyner_boore_distance<1,1.0,
                                joyner_boore_distance)
    
    return joyner_boore_distance
###################
# END OF FUNCTIONS#
###################

"""No functions past this step will be included in the table"""
__local_functions = locals().copy() #all the functions in the local namespace
# Note that this is a copy, otherwise __local_functions would point to itself

distance_functions = {}
for function_name in __local_functions.keys():
    #for all functions in the local namespace
    
    if not function_name.startswith('_'): #If it's not private
        function = __local_functions[function_name]
        distance_functions[function_name]=function
