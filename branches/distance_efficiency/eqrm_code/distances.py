"""
 Title: distances.py

  Author:  Peter Row, peter.row@ga.gov.au


  Description: Class to calculate distance.  Used in sites.

  Version: $Revision: 914 $
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-04-01 11:11:47 +1100 (Wed, 01 Apr 2009) $

  Copyright 2007 by Geoscience Australia
"""

#FIXME.  This looks like it can be optimised a lot.

from scipy import array

from distance_functions import distance_functions

from eqrm_code import file_store

class Distances(file_store.File_Store):
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
        
        super(Distances, self).__init__('distances')

        self.distance_functions = distance_functions

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
    
    Epicentral = property(lambda self: self.__getattr__('Epicentral'),
                          lambda self, value: self._set_file_array('Epicentral', value))
    
    Hypocentral = property(lambda self: self.__getattr__('Hypocentral'),
                       lambda self, value: self._set_file_array('Hypocentral', value))
    
    Joyner_Boore = property(lambda self: self.__getattr__('Joyner_Boore'),
                            lambda self, value: self._set_file_array('Joyner_Boore', value))
    
    Rupture = property(lambda self: self.__getattr__('Rupture'),
                       lambda self, value: self._set_file_array('Rupture', value))
    
    Horizontal = property(lambda self: self.__getattr__('Horizontal'),
                          lambda self, value: self._set_file_array('Horizontal', value))
                
    def __del__(self):
        super(Distances, self).__del__()

    def __getattr__(self, distance_type):
        """self.Epicentral = self.distance['Epicentral'])"""
        if not self.distance_functions.has_key(distance_type):
            raise AttributeError
        else:
            return self.distance(distance_type)

    def calc_distance(self, distance_type):
        if not self.distance_functions.has_key(distance_type):
            raise AttributeError
        
        distance = self.raw_distances(
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
        
        self._set_file_array(distance_type, distance)

    def distance(self, distance_type):
        distance = self._get_file_array(distance_type)
        if distance is None:
            return self.raw_distances(
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
        else:
            return distance
        
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
        """
        Calculate the distance using the specified distance function
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
        try:
            site, event = key
        except:
            site, event = key, slice(None)

        site_latitude = self.site_latitude[site]
        site_longitude = self.site_longitude[site]
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
        
        # We don't want to have to recalculate these again
        # TODO: Can this be abstracted and generalised?
        if self.Epicentral is not None:
            distances.Epicentral = self.Epicentral[site, event]
        if self.Hypocentral is not None:
            distances.Hypocentral = self.Hypocentral[site, event]
        if self.Joyner_Boore is not None:
            distances.Joyner_Boore = self.Joyner_Boore[site, event]
        if self.Rupture is not None:
            distances.Rupture = self.Rupture[site, event]
        if self.Horizontal is not None:
            distances.Horizontal = self.Horizontal[site, event]
        
        
        return distances

