"""
earthquake_event.py
This is the earthquake event object.
Stores attributes of a particular earthquake event froma catalogue.
"""

import numpy as np
import datetime

class EarthquakeEvent(object):

    def __init__(self, lon, lat, magnitude, time, **kwargs):
        """
        lon, lat = latitude and longitude of earthquake
        magnitude = magnitude of event
        time = Datetime object. Can be
                incomplete but must have year.
        kwargs: other parameters:
            depth = depth of hypocenter
            magnitude_type = e.g. Mw, Ms, Mb 
        """

        # Get basic datadata
        self.lon = lon
        self.lat = lat
        self.magnitude = magnitude
        self.time = time

        # Get kwargs
        self.depth = kwargs.get('depth', None)
        self.mag_type = kwargs.get('mag_type', None)
        
        

class EventSet(object):

    def __init__(self, event_list):
        """
        Create object of list of EarthquakeEvent objects so that they can be manipulated,
        e.g. take a subset of the catalogue
        """
        #self.event_set = event_list
        self.catalogue_subset = {'all': event_list}
        self.magnitudes = {}
        self.times = {}
        self.depths= {}

    def create_subset(self, subset_name, **kwargs):
        """
        Method to create a subset of the catalogue based on arbitrary parameters
        kwargs (of the form parameter and value):
            
        """


        # Read kwargs
        self.max_mag = kwargs.get('max_mag', None)
        self.min_mag = kwargs.get('min_mag', None)
        self.max_lon = kwargs.get('max_lon', None)
        self.min_lon = kwargs.get('min_lon', None)
        self.max_lat = kwargs.get('max_lat', None)
        self.min_lat = kwargs.get('min_lat', None)
        self.max_depth = kwargs.get('max_depth', None)
        self.min_depth = kwargs.get('min_depth', None)
        self.max_time = kwargs.get('max_time', None)
        self.min_time = kwargs.get('min_time', None)
        self.mag_type = kwargs.get('mag_type', None)

        subset_name = subset_name

        # New list for catalogg subset

        catalogue_subset = []

        for event in self.catalogue_subset['all']:
            # Select magnitudes
            if self.max_mag is None:
                pass
            elif event.magnitude > self.max_mag:
                continue
            if self.min_mag is None:
                pass
            elif event.magnitude < self.min_mag:
                continue
            
            # Select locations
            if self.max_lon is None:
                pass
            elif event.lon > self.max_lon:
                continue            
            if self.min_lon is None:
                pass
            elif event.lon < self.min_lon:
                continue  
            if self.max_lat is None:
                pass
            elif event.lat > self.max_lat:
                continue          
            if self.min_lat is None:
                pass
            elif event.lat < self.min_lat:
                continue

            # Select depth
            if self.max_depth is None:
                pass
            elif event.depth > self.max_depth:
                continue          
            if self.min_depth is None:
                pass
            elif event.depth < self.min_depth:
                continue    

            # Select depth
            if self.max_depth is None:
                pass
            elif event.depth > self.max_depth:
                continue          
            if self.min_depth is None:
                pass
            elif event.depth < self.min_depth:
                continue

            # Select time
            if self.max_time is None:
                pass
            elif event.time > self.max_time:
                continue          
            if self.min_time is None:
                pass
            elif event.time < self.min_time:
                continue

            # Select magnitude type
            if self.mag_type is None:
                pass
            elif event.mag_type is None:
                print 'Magnitude types not specified, cannot select by this parameter'
                continue
            elif event.mag_type != self.mag_type:
                continue

            # If the event is within the required parameters,
            # append to the new event set
            catalogue_subset.append(event)
            self.catalogue_subset[subset_name] = catalogue_subset
        
    def get_magnitudes(self, subset_name='all'):
        """ Get numpy array of all magnitudes"""
        magnitudes = []
        for event in self.catalogue_subset[subset_name]:
            magnitudes.append(event.magnitude)
        self.magnitudes[subset_name] = np.array(magnitudes)

    def get_times(self, subset_name='all'):
        """ Get numpy array of all times"""
        times = []
        for event in self.catalogue_subset[subset_name]:
            times.append(event.time)
        self.times[subset_name] = np.array(times)

    def get_depths(self, subset_name='all'):
        """ Get numpy array of all magnitudes"""
        depths = []
        for event in self.catalogue_subset[subset_name]:
            depths.append(event.depth)
        self.depths[subset_name].depths = np.array(depths)
            


            
