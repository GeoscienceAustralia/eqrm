"""
 Title: distances.py

  Author:  Peter Row, peter.row@ga.gov.au


  Description: Class to calculate distance.  Used in sites.

  Version: $Revision: 914 $
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-04-01 11:11:47 +1100 (Wed, 01 Apr 2009) $

  Copyright 2007 by Geoscience Australia
"""

# FIXME.  This looks like it can be optimised a lot.

from scipy import array

from .distance_functions import distance_functions

# def distance_limit(distance):
 #   """ Given an array of distances, set a lower limit.
  #  """


class Distances(object):

    def __init__(self,
                 site_latitude,
                 site_longitude,
                 rupture_centroids_lat,
                 rupture_centroids_lon,
                 lengths,
                 azimuths,
                 widths,
                 dips,
                 depths,
                 depths_to_top,
                 projection,
                 trace_start_lat=None,
                 trace_start_lon=None,
                 rupture_centroid_x=None,
                 rupture_centroid_y=None):

        self.distance_functions = distance_functions
        self.distance_cache = {}

        self.site_latitude = site_latitude
        self.site_longitude = site_longitude

        self.rupture_centroid_lat = rupture_centroids_lat
        self.rupture_centroid_lon = rupture_centroids_lon
        self.lengths = lengths
        self.azimuths = azimuths
        self.widths = widths
        self.dips = dips
        self.depths = depths
        self.depths_to_top = depths_to_top

        self.projection = projection

        # for backwards testing with matlab
        self.trace_start_lat = trace_start_lat
        self.trace_start_lon = trace_start_lon
        if self.trace_start_lat is not None:
            self.trace_start_lat = array(self.trace_start_lat)
        if self.trace_start_lon is not None:
            self.trace_start_lon = array(self.trace_start_lon)

        self.rupture_centroid_x = rupture_centroid_x
        self.rupture_centroid_y = rupture_centroid_y
        if self.rupture_centroid_x is not None:
            self.rupture_centroid_x = array(self.rupture_centroid_x)
        if self.rupture_centroid_y is not None:
            self.rupture_centroid_y = array(self.rupture_centroid_y)

    def __getattr__(self, distance_type):
        """self.Epicentral = self.distance['Epicentral']"""

        if distance_type not in self.distance_functions:
            raise AttributeError
        else:
            return self.distance(distance_type)

    def distance(self, distance_type):
        if distance_type not in self.distance_cache:
            self.distance_cache[distance_type] = self.raw_distances(
                site_latitude=self.site_latitude,
                site_longitude=self.site_longitude,
                rupture_centroid_lat=self.rupture_centroid_lat,
                rupture_centroid_lon=self.rupture_centroid_lon,
                lengths=self.lengths,
                azimuths=self.azimuths,
                widths=self.widths,
                dips=self.dips,
                depths=self.depths,
                depths_to_top=self.depths_to_top,
                projection=self.projection,
                distance_type=distance_type,
                trace_start_lat=self.trace_start_lat,
                trace_start_lon=self.trace_start_lon,
                rupture_centroid_x=self.rupture_centroid_x,
                rupture_centroid_y=self.rupture_centroid_y)
        return self.distance_cache[distance_type]

    def raw_distances(self,
                      site_latitude,
                      site_longitude,
                      rupture_centroid_lat,
                      rupture_centroid_lon,
                      lengths,
                      azimuths,
                      widths,
                      dips,
                      depths,
                      depths_to_top,
                      distance_type,
                      projection,
                      trace_start_lat=None,
                      trace_start_lon=None,
                      rupture_centroid_x=None,
                      rupture_centroid_y=None):
        """Calculate the distance from 'locations' to 'rupture_centroid'.

        A big array, not an array-like object
        """

        distance_function = self.distance_functions[distance_type]
        return distance_function(site_latitude,
                                 site_longitude,
                                 rupture_centroid_lat,
                                 rupture_centroid_lon,
                                 lengths, azimuths,
                                 widths,
                                 dips,
                                 depths,
                                 depths_to_top,
                                 projection,
                                 trace_start_lat,
                                 trace_start_lon,
                                 rupture_centroid_x,
                                 rupture_centroid_y)

    def __getitem__(self, key):
        """
        Take a slice by the event dimension
        """
        # TODO: Do we want to support slicing via site dimension?
        event = key

        site_latitude = self.site_latitude
        site_longitude = self.site_longitude
        rupture_centroid_lat = self.rupture_centroid_lat[event]
        rupture_centroid_lon = self.rupture_centroid_lon[event]
        lengths = self.lengths[event]
        azimuths = self.azimuths[event]
        widths = self.widths[event]
        dips = self.dips[event]
        depths = self.depths[event]
        depths_to_top = self.depths_to_top[event]

        projection = self.projection

        trace_start_lat = None
        trace_start_lon = None
        rupture_centroid_x = None
        rupture_centroid_y = None

        # for backwards testing with matlab
        if self.trace_start_lat is not None:
            trace_start_lat = self.trace_start_lat[event]
            trace_start_lon = self.trace_start_lon[event]
        if self.rupture_centroid_x is not None:
            rupture_centroid_x = self.rupture_centroid_x[event]
            rupture_centroid_y = self.rupture_centroid_y[event]

        distances = Distances(site_latitude,
                              site_longitude,
                              rupture_centroid_lat,
                              rupture_centroid_lon,
                              lengths,
                              azimuths,
                              widths,
                              dips,
                              depths,
                              depths_to_top,
                              projection,
                              trace_start_lat=trace_start_lat,
                              trace_start_lon=trace_start_lon,
                              rupture_centroid_x=rupture_centroid_x,
                              rupture_centroid_y=rupture_centroid_y)

        # Take a slice of the cached distances
        distance_cache = {}
        for dist_func, dist_cache in self.distance_cache.iteritems():
            distance_cache[dist_func] = dist_cache[:, event]
        distances.distance_cache = distance_cache

        return distances
