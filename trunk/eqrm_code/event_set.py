"""
 Title: equivalent linear solver.py
  
  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, duncan.gray@ga.gov.au

  Description: Class for generating and storing sets of earthquake events
  

  Version: $Revision: 1665 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-05-09 00:07:41 +1000 (Sun, 09 May 2010) $

  Copyright 2007 by Geoscience Australia
"""
import copy
import xml.dom.minidom
import math
import scipy
import tempfile
import sys
import os, shutil

from scipy import asarray, transpose, array, r_, concatenate, sin, cos, pi, \
     ndarray, absolute, allclose, zeros, ones, float32, int32, float64, \
     int64, reshape, arange, append, radians, where, minimum, seterr
from numpy import random

from eqrm_code.ANUGA_utilities import log
from eqrm_code import conversions
from eqrm_code.conversions import calc_fault_area, calc_fault_width,\
    calc_fault_length, get_new_ll, azimuth_of_trace,\
    switch_coords, calc_max_width_in_slab
from eqrm_code.projections import projections
from eqrm_code.generation_polygon import polygons_from_xml
from eqrm_code.projections import azimuthal_orthographic_ll_to_xy as ll_to_xy
from eqrm_code.projections import azimuthal_orthographic_xy_to_ll as xy_to_ll
from eqrm_code.generation_polygon import xml_fault_generators
from eqrm_code.ANUGA_utilities import log as eqrmlog
from eqrm_code import source_model #import create_fault_sources
from eqrm_code import ground_motion_misc
from eqrm_code import scaling
from eqrm_code import file_store

# This specifies the dtypes used in  event set.
# This was investigated to save memory
# Float32 gives differnet results between windows and linux
# therefore let's not use it.
EVENT_FLOAT = float64 #float32
EVENT_INT = int64 #int32

class Event_Set(file_store.File_Store):
    def __init__(self, 
                 azimuth, 
                 dip, 
                 ML, 
                 Mw,
                 depth, 
                 depth_to_top, 
                 fault_type,
                 width, 
                 length, 
                 area, 
                 fault_width,
                 source_zone_id,
                 trace_start_lat, 
                 trace_start_lon,
                 trace_end_lat, 
                 trace_end_lon,
                 rupture_centroid_x, 
                 rupture_centroid_y,
                 rupture_centroid_lat, 
                 rupture_centroid_lon,
                 event_id=None,
                 dir=None):
        """
    A set of seismic events. Can be created  either directly or from an
    XML file which generates the events from eqrm_code.generation polygons.

    If you supply rupture_centroid, distances will be calcuated using
    rupture centroids. If you supply trace start, distances will use
    trace start. (#FIXME DSG-DSG  Check this)

    Do not use event_set as an iterator, I feel it is slow, since it
    creates a new instance of event set at each iteration
    
    azimuth               azimuths - scalar or n-vector, range [0:360)
    dip                   dips - scalar or n-vector, range (0:90)
                          # TODO ask Trev or Trev - maybe [0,90], or (0,90]??
    depth                 depths - scalar or n-vector, depth to event , km
                          range (0:large], ie [5,5,10,...]
    depth_top             depth to top of rupture - scalar or n-vector, km
    fault_type            index (0, 1 or 2) from the FaultTypeDictionary
                          above, depending on fault type key
    Mw                    moment magnitudes - scalar or n-vector
                          range (-large:+large) in practice ~(0:9)
    ML                    local magnitudes - scalar or n-vector
                          range (-large:+large) in practice ~(0:9)         
    rupture_centroid_lat  latitude of the rupture_centroid - scalar or n-vector
                          range (-90,90)
    rupture_centroid_lon  longitude of the rupture_centroid - scalor or
                          n-vector range unbounded.
                         

      
        can have:
          rupture_centroid_lat
          rupture_centroid_lon
        or        
          rupture_centroid_x
          rupture_centroid_y
          

    generation parameters
    ---------------------
    filename : generation polygons in target file 
               (see 'sample_event.xml')


        """
        super(Event_Set, self).__init__('event_set', dir)
        
        self.azimuth = azimuth
        self.dip = dip
        self.ML = ML
        self.Mw = Mw
        self.depth = depth
        self.depth_to_top = depth_to_top
        self.fault_type = fault_type
        self.width = width
        self.length = length
        self.area = area
        self.fault_width = fault_width
        self.source_zone_id = source_zone_id # Warning sometimes = to None
        self.trace_start_lat = trace_start_lat
        self.trace_start_lon = trace_start_lon
        self.trace_end_lat = trace_end_lat
        self.trace_end_lon = trace_end_lon
        self.rupture_centroid_x = rupture_centroid_x
        self.rupture_centroid_y = rupture_centroid_y
        self.rupture_centroid_lat = rupture_centroid_lat
        self.rupture_centroid_lon = rupture_centroid_lon
        if event_id is None and depth is not None:
           self.event_id = r_[0:len(self.depth)] # gives every event an id
        else:
            self.event_id = event_id
        self.check_arguments()
        

    def __del__(self):
        super(Event_Set, self).__del__()
    
    # PROPERTIES #
    # Define getters and setters for each attribute to exercise the 
    # file-based data structure
    azimuth = property(lambda self: self._get_file_array('azimuth'), 
                       lambda self, value: self._set_file_array('azimuth', value))
    
    dip = property(lambda self: self._get_file_array('dip'), 
                   lambda self, value: self._set_file_array('dip', value))
    
    ML = property(lambda self: self._get_file_array('ML'), 
                  lambda self, value: self._set_file_array('ML', value))
    
    Mw = property(lambda self: self._get_file_array('Mw'), 
                  lambda self, value: self._set_file_array('Mw', value))
    
    depth = property(lambda self: self._get_file_array('depth'), 
                     lambda self, value: self._set_file_array('depth', value))
    
    depth_to_top = property(lambda self: self._get_file_array('depth_to_top'), 
                            lambda self, value: self._set_file_array('depth_to_top', value))
    
    fault_type = property(lambda self: self._get_file_array('fault_type'), 
                          lambda self, value: self._set_file_array('fault_type', value))
    
    width = property(lambda self: self._get_file_array('width'), 
                     lambda self, value: self._set_file_array('width', value))
    
    length = property(lambda self: self._get_file_array('length'), 
                      lambda self, value: self._set_file_array('length', value))
    
    area = property(lambda self: self._get_file_array('area'), 
                    lambda self, value: self._set_file_array('area', value))
    
    fault_width = property(lambda self: self._get_file_array('fault_width'), 
                           lambda self, value: self._set_file_array('fault_width', value))
    
    source_zone_id = property(lambda self: self._get_file_array('source_zone_id'), 
                              lambda self, value: self._set_file_array('source_zone_id', value))
    
    trace_start_lat = property(lambda self: self._get_file_array('trace_start_lat'), 
                               lambda self, value: self._set_file_array('trace_start_lat', value))
    
    trace_start_lon = property(lambda self: self._get_file_array('trace_start_lon'), 
                               lambda self, value: self._set_file_array('trace_start_lon', value))
    
    trace_end_lat = property(lambda self: self._get_file_array('trace_end_lat'), 
                             lambda self, value: self._set_file_array('trace_end_lat', value))
    
    trace_end_lon = property(lambda self: self._get_file_array('trace_end_lon'), 
                             lambda self, value: self._set_file_array('trace_end_lon', value))
    
    rupture_centroid_x = property(lambda self: self._get_file_array('rupture_centroid_x'), 
                                  lambda self, value: self._set_file_array('rupture_centroid_x', value))
    
    rupture_centroid_y = property(lambda self: self._get_file_array('rupture_centroid_y'), 
                                  lambda self, value: self._set_file_array('rupture_centroid_y', value))
    
    rupture_centroid_lat = property(lambda self: self._get_file_array('rupture_centroid_lat'), 
                                    lambda self, value: self._set_file_array('rupture_centroid_lat', value))
    
    rupture_centroid_lon = property(lambda self: self._get_file_array('rupture_centroid_lon'), 
                                    lambda self, value: self._set_file_array('rupture_centroid_lon', value))
    
    event_id = property(lambda self: self._get_file_array('event_id'), 
                        lambda self, value: self._set_file_array('event_id', value))
    # END PROPERTIES #

    @classmethod
    def load(cls, load_dir, store_dir=None):
        """
        Return an Event_Set object from the .npy files stored in the specified
        directory
        """
        event_set = cls(azimuth=None,
                        dip=None,
                        ML=None,
                        Mw=None,
                        depth=None,
                        depth_to_top=None,
                        fault_type=None,
                        width=None,
                        length=None,
                        area=None,
                        fault_width=None,
                        source_zone_id=None,
                        trace_start_lat=None,
                        trace_start_lon=None,
                        trace_end_lat=None,
                        trace_end_lon=None,
                        rupture_centroid_x=None,
                        rupture_centroid_y=None,
                        rupture_centroid_lat=None,
                        rupture_centroid_lon=None,
                        dir=store_dir)
        event_set._load(load_dir)
        return event_set

    @classmethod
    def create(cls, 
               rupture_centroid_lat, 
               rupture_centroid_lon, 
               azimuth,
               dip=None, 
               ML=None, 
               Mw=None, 
               depth=None, 
               fault_width=None,
               depth_top_seismogenic=None, # Need for generate synthetic events
               depth_bottom_seismogenic=None,
               fault_type=None,
               area=None, 
               width=None, 
               length=None,
               dir=None):
        """generate a scenario event set or a synthetic event set.
        Args:
          rupture_centroid_lat: Latitude of rupture centriod
          rupture_centroid_lon: Longitude of rupture centriod
          azimuth: azimuth of event, degrees
          dip: dip of virtual faults, degrees
          ML or Mw: earthquake magnitude. analysis only uses Mw.
          depth: depth to event centroid, km
          fault_width: Maximum width along virtual fault, km
          depth_top_seismogenic: depth to the top of the seismmogenic region,
            km.
          
          Note, if you supply either ML or Mw, the other will be
          calculated. If you supply both, it is up to you to ensure that
          they are consitant. Note that most funtions in EQRM use Mw (ML
          based attenuation models being one exception).

        The degrees of freedom of this interface is not quite right.      

        Returns:
          An event set instance.
         
    FIXME DSG-EQRM scenario_number_of_events is actually how many times
    the scenario
    parameters will be repeated.  But __init__ fails if the parameters
    represent more than 1 event and scenario_number_of_events > 1.

        """
        

        # There is a diff between width and fault width.
        # Width is rupture/event width.
        # rupture width <= fault width

        # turn into arrays
        if depth is not None:
            depth = asarray(depth)
        if depth_top_seismogenic is not None:
            depth_top_seismogenic = asarray(depth_top_seismogenic)          
        if depth_bottom_seismogenic is not None:
            depth_bottom_seismogenic = asarray(depth_bottom_seismogenic)   
        if fault_width is not None:
            fault_width = asarray(fault_width)
        if width is not None:
            width = asarray(width)
        if length is not None:
            length = asarray(length)           
        rupture_centroid_lat = asarray(rupture_centroid_lat)
        rupture_centroid_lon = asarray(rupture_centroid_lon)
        azimuth = asarray(azimuth)
        dip = asarray(dip)    
        if ML is not None:
            ML = asarray(ML)
        if Mw is not None:
            Mw = asarray(Mw)
        # finish turning into arrays

        if Mw is None:
            Mw = conversions.Johnston_89_Mw(ML)
        if ML is None:
            ML = conversions.Johnston_01_ML(Mw)
                
        if fault_width is None and depth_bottom_seismogenic is not None \
                and depth_top_seismogenic is not None:
            fault_width = (depth_bottom_seismogenic \
                           - depth_top_seismogenic)/ \
                           sin(dip*pi/180.)
        
        if area is None:
            area = conversions.modified_Wells_and_Coppersmith_94_area(Mw)
                           
        if width is None:
            width = conversions.\
                modified_Wells_and_Coppersmith_94_width(dip, Mw, area,
                                                        fault_width)
        
        if length is None:
            length = area / width
        
        # Note: area used to determine length and width only
        # It is no longer needed after this point in time.
        
        if depth is None:
            depth = conversions.depth(depth_top_seismogenic,
                                      dip, Mw, fault_width)
            
        # calculate depth_to_top from depth, width, dip
        depth_to_top = conversions.calc_depth_to_top(depth, width, dip)

        # Default 'fault_type' to 'reverse'
        if fault_type is None:
            fault_type = ones(
                depth.shape, dtype=int) * \
                ground_motion_misc.FaultTypeDictionary['reverse']

        # Calculate the distance of the origin from the centroid
        rad = pi/180.
        x = length/2.
        y = depth*cos(dip*rad)/sin(dip*rad)

        rupture_centroid_x = x
        rupture_centroid_y = y

        (trace_start_lat,
         trace_start_lon) = xy_to_ll(-rupture_centroid_x,-rupture_centroid_y,
                                     rupture_centroid_lat,rupture_centroid_lon,
                                     azimuth)

        (trace_end_lat,
         trace_end_lon) = xy_to_ll(rupture_centroid_x,-rupture_centroid_y,
                                   rupture_centroid_lat,rupture_centroid_lon,
                                   azimuth)  

        # Create an Event_Set instance
        event_set = cls(azimuth,
                        dip,
                        ML,
                        Mw,
                        depth,
                        depth_to_top,
                        fault_type,
                        width,
                        length,
                        area,
                        fault_width,
                        None, #source_zone_id
                        trace_start_lat,
                        trace_start_lon,
                        trace_end_lat,
                        trace_end_lon,
                        rupture_centroid_x,
                        rupture_centroid_y,
                        rupture_centroid_lat,
                        rupture_centroid_lon,
                        dir=dir)
        return event_set
    
    
    @classmethod
    def create_scenario_events(cls, 
                               rupture_centroid_lat,
                               rupture_centroid_lon, 
                               azimuth,
                               dip, 
                               Mw, 
                               depth, 
                               scenario_number_of_events,
                               fault_width=None,
                               depth_top_seismogenic=None, 
                               depth_bottom_seismogenic=None,
                               width=None,
                               length=None,
                               store_dir=None):
        
        __len__ = '__len__'
        if scenario_number_of_events > 1:
            rupture_centroid_lat = concatenate(
                [rupture_centroid_lat for i in
                 xrange(scenario_number_of_events)])
            rupture_centroid_lon = concatenate(
                [rupture_centroid_lon for i in
                 xrange(scenario_number_of_events)])
            azimuth = concatenate(
                [azimuth for i in
                 xrange(scenario_number_of_events)])
            dip = concatenate([dip for i in xrange(
                scenario_number_of_events)])
            depth = concatenate([depth for i in
                                 xrange(scenario_number_of_events)])
            Mw = concatenate([Mw for i in xrange(
                scenario_number_of_events)])
            
            fault_width = concatenate([[fault_width] for i in 
                                       xrange(scenario_number_of_events)])
            if depth_top_seismogenic is not None:
                depth_top_seismogenic = concatenate(
                    [[depth_top_seismogenic] for i in
                     xrange(scenario_number_of_events)])
                
            # Note: as we need to test for NoneType width and length must be
            # passed into here as scalars and not vectors
            if width is not None:
                width = concatenate([[width] for i in 
                                     xrange(scenario_number_of_events)])
            if length is not None:
                length = concatenate([[length] for i in 
                                      xrange(scenario_number_of_events)])
        else:
            rupture_centroid_lat = asarray(rupture_centroid_lat)
            rupture_centroid_lon = asarray(rupture_centroid_lon)
            azimuth = asarray(azimuth)
            dip = asarray(dip)
            depth = asarray(depth)
            Mw = asarray(Mw)
            
            # Note: as we need to test for NoneType width and length must be
            # passed into here as scalars and not vectors
            if width is not None:
                width = asarray([width])
            if length is not None:
                length = asarray([length])
                
        event = Event_Set.create(rupture_centroid_lat=rupture_centroid_lat,
                                 rupture_centroid_lon=rupture_centroid_lon,
                                 azimuth=azimuth,
                                 dip=dip,
                                 Mw=Mw,
                                 depth=depth,
                                 fault_width=fault_width,
                                 depth_top_seismogenic=depth_top_seismogenic,
                                 depth_bottom_seismogenic=
                                 depth_bottom_seismogenic,
                                 width=width,
                                 length=length,
                                 dir=store_dir)
        return event
        

    @classmethod
    def generate_synthetic_events(cls, 
                                  fid_genpolys,
                                  source_model,
                                  prob_number_of_events_in_zones=None,
                                  store_dir=None):
        """Randomly generate the event_set parameters.

        Note: The rupture centroid are within the polygons.  The trace
        start and end can be outside of the polygon.  The trace is on
        the surface, the centroid is underground.
        
        Args:
          fid_genpolys: The full path name of the source polygon xml file
          source_model: Basically a list of sources.
          prob_number_of_events_in_zones: Vector whose elements represent
            the number of events for each generation.  Can be None.
            This overrides the info in the xml file.
          
        Returns: An event_set instance.
        
        Creates generation_polygons (from
        eqrm_code.generation_polygon.py) out of filename, then
        generate events in those polygons.
        
        prob_number_of_events_in_zones is a sequence of
        length number_of_polygons -
        polygon[i] will generate events_in_polygon[i]
        
        See populate, and populate_distribution from
        eqrm_code.generation_polygon.py:
    
    
        Notes:
        file (from filename) contains xml "generation polygons" example:
        <Source_Model magnitude_type="Mw">
        <polygon area="100">
        <boundary>-20 126.0 -21 126.5 -22 126.0 -20 126.0</boundary>
        <recurrence distribution="uniform" min_magnitude="5"
        max_magnitude="8"/> 
        </polygon>
        </Source_Model>
        
        Boundary is in lat,long pairs. First node is repeated.
        """      

        (generation_polygons,
             magnitude_type) = polygons_from_xml(fid_genpolys)
        num_polygons = len(generation_polygons)
        assert num_polygons == len(source_model)
        
        if prob_number_of_events_in_zones is None:
            prob_number_of_events_in_zones = zeros((len(generation_polygons)),
                                                   dtype=EVENT_INT)
            for i,gen_poly in enumerate(generation_polygons):
                prob_number_of_events_in_zones[i] = gen_poly.number_of_events
        
        
        #initialise new attributes
        num_events = sum(prob_number_of_events_in_zones)
                
        rupture_centroid_lat = zeros((num_events), dtype=EVENT_FLOAT)
        rupture_centroid_lon = zeros((num_events), dtype=EVENT_FLOAT)
        depth_top_seismogenic = zeros((num_events), dtype=EVENT_FLOAT)
        depth_bottom_seismogenic = zeros((num_events), dtype=EVENT_FLOAT)
        azimuth = zeros((num_events), dtype=EVENT_FLOAT)
        dip = zeros((num_events), dtype=EVENT_FLOAT)
        area = zeros((num_events), dtype=EVENT_FLOAT)
        width = zeros((num_events), dtype=EVENT_FLOAT)
        fault_width = zeros((num_events), dtype=EVENT_FLOAT)
        magnitude = zeros((num_events), dtype=EVENT_FLOAT)
        source_zone_id = zeros((num_events), dtype=EVENT_INT)
        
        start = 0
        for i, source in enumerate(source_model):
            
            eqrmlog.debug('Generating events for source %s of %s' % 
                          (i, len(source_model)))
            
            gp = generation_polygons[i]
            
            num = prob_number_of_events_in_zones[i]
            end = start + num
            
            range = arange(start, end)
            source.set_event_set_indexes(range)
            
            eqrmlog.debug('Number of events = %s, range = %s' % (num, range))
            
            if num == 0:
                continue
            
            #populate the polygons and attach the current polygons generated attributes
            depth_top_seismogenic[start:end] = gp.populate_depth_top_seismogenic(num)
            eqrmlog.debug('Memory: populate_depth_top_seismogenic created')
            eqrmlog.resource_usage()
            
            azimuth[start:end] = gp.populate_azimuth(num)
            eqrmlog.debug('Memory: populate_azimuth created')
            eqrmlog.resource_usage()
            
            dip[start:end] = gp.populate_dip(num)
            eqrmlog.debug('Memory: populate_dip created')
            eqrmlog.resource_usage()
            
            magnitude[start:end] = gp.populate_magnitude(num)
            eqrmlog.debug('Memory: populate_magnitude created')
            eqrmlog.resource_usage()
            
            depth_bottom_seismogenic[start:end] = gp.populate_depth_bottom_seismogenic(num)

            #FIXME DSG-EQRM the events will not to randomly placed,
            # Due to  lat, lon being spherical coords and popolate
            # working in x,y (flat 2D).
            (rupture_centroid_lat[start:end], 
             rupture_centroid_lon[start:end]) = array(gp.populate(num)).swapaxes(0, 1)
            
            eqrmlog.debug('Memory: lat,lon created')
            eqrmlog.resource_usage()      
            
            fault_width[start:end] = (depth_bottom_seismogenic[start:end] - \
                                      depth_top_seismogenic[start:end]) / \
                                        sin(dip[start:end]*pi/180.)
            area[start:end] = scaling.scaling_calc_rup_area(magnitude[start:end], 
                                                            source.scaling)
            #print "source.scaling", source.scaling
            #print "magnitude[start:end]", magnitude[start:end]
            #print "dip[start:end]", dip[start:end]
            #print "rup_area=area[start:end", area[start:end]
            #print "max_rup_width=fault_width[s:e]", fault_width[start:end]
            
            width[start:end] = scaling.scaling_calc_rup_width(magnitude[start:end], 
                                          source.scaling, 
                                          dip[start:end],
                                          rup_area=area[start:end], 
                                          max_rup_width=fault_width[start:end])
            eqrmlog.debug('Memory: event set lists have been combined')
            eqrmlog.resource_usage()

            
            # Does this mean source zone objects know nothing about
            # their id? Yes
            source_zone_id[start:end] = [i]*num
            
            
            start = end
            
        new_ML=None
        new_Mw=None
        if magnitude_type == 'ML':
            new_ML=magnitude
        elif magnitude_type == 'Mw':
            new_Mw=magnitude
        else:
            raise Exception('Magnitudes not set')
        event = Event_Set.create(rupture_centroid_lat=rupture_centroid_lat,
                                 rupture_centroid_lon=rupture_centroid_lon,
                                 azimuth=azimuth,
                                 dip=dip,
                                 ML=new_ML,
                                 Mw=new_Mw,
                                 depth_top_seismogenic=depth_top_seismogenic,
                                 depth_bottom_seismogenic=depth_bottom_seismogenic,
                                 fault_width=fault_width,
                                 area=area,
                                 width=width,
                                 dir=store_dir)
        event.source_zone_id = asarray(source_zone_id)
        eqrmlog.debug('Memory: finished generating events')
        eqrmlog.resource_usage()

        return event

    def save(self, dir=None):
        """
        Save the ndarray objects to the specified directory
        """
        self._save(dir)

    
    def scenario_setup(self):
        """
        
        setup event ids (for scenario simulations each id
        points to a new copy of the same event.
        These copies are necessary if Monte-Carlo techniques are used
        for things like ground motion and amplification etc.

        Attributes that are tacked onto an event_set instance.
        """
        # Moved from analysis        
        self.source_zone_id = array(0*self.depth+1) # create a vector of 1's


    def check_arguments(self):
        """
        Checks that all arguments are the same size (or scalar).
        Returns the length of the arguments.
        """

        arguments = {'depth': self.depth, 'azimuth': self.azimuth,
                     'dip': self.dip, 'ML': self.ML,
                     'Mw': self.Mw, 'length': self.length,
                     'rupture_centroid_lat': self.rupture_centroid_lat,
                     'rupture_centroid_lon': self.rupture_centroid_lon,
                     'event_id': self.event_id}

        n = 1     #initialise number of arguments to 1
        for key in arguments.keys():
            argument = arguments[key]
            if not argument is None:
                if not argument.size == 1:
                    if not (n==1 or n==argument.size):
                        msg = "Not all arguments are of equal size!"
                        msg+= "\nArguments size should be: "+str(n)
                        msg+= "\n"+key+" size = "+str(argument.size)
                        msg+= "\n Arguments = "+str(arguments.keys())
                        IOError( msg)
                    n = argument.size
        return n
    
    def introspect_attributes(self):
        """Return a list of all the event set attributes"""
        # FIXME could probbaly just use self.__dict__.keys(), 
        # or better yet self.__dict__.items() and change caller
        return [att for att in dir(self) if not callable(getattr(self, att))
                                         and not att[-2:] == '__'
                                         and not att[0] == '_']
    
    def introspect_attribute_values(self):
        """Puts all the attribute values of event set into a dictionary"""

        attributes = [att for att in dir(self)
                      if not callable(getattr(self, att))
                      and not att[-2:] == '__'
                      and not att[0] == '_']
        att_values = {}
        for att in attributes:
            att_values[att] = getattr(self, att)

        return att_values
    
    def __getitem__(self, key):
        """Get slice of this Event_Set.

        Returns a new Event_Set object containing the sliced data.
        Additional attributes aren't carried over. eg event_id.
        """
        
        # 'key' has to be an array.
        if isinstance(key, int):
            key = [key]

        # if key is None or key would slice whole of object, return self
        if key is None or (isinstance(key, ndarray) and
                           (key.shape == (len(self.depth),)) and
                           (key == r_[0:len(self.depth)]).all()):
            return self

        # special handling for some data
        if self.fault_width.shape == tuple():
            # Zero-rank or scalar. Broadcast to same shape as self.width
            fault_width = self.fault_width + 0*self.width
        else:
            fault_width = self.fault_width

        # some variables/array are set to None after the Event_set has
        # been saved, so this method now checks for None values.
        # We also don't want _arguments to be passed along
        # FIXME could probably just use args = self.__dict__.items()
        args = {}
        for att in self.introspect_attributes():
            if getattr(self, att) is None:
                args[att] = None
            else:
                args[att] = getattr(self, att)[key]
                
        # Keep the file_store data directory intact
        args['dir'] = self._dir
        
        return Event_Set(**args) # FIXME relies on arg/attr name correspondence
   
    def __len__(self):
        return len(self.rupture_centroid_lat)
    
    def __add__(self, other):
        atts=self.introspect_attributes()
        for att in atts:
            b=getattr(self, att)
            newValues=append(getattr(self, att),getattr(other, att))
            setattr(self,att,newValues)      
            c =getattr(self, att)
        return self

    def __repr__(self):
        return ('Event Set:\n'
                '     number of events:%d\n'
                ' rupture_centroid lat:%s\n'
                'rupture_centroid long:%s\n'
                '                   Mw:%s\n'
                % (self.check_arguments(), str(self.rupture_centroid_lat),
                   str(self.rupture_centroid_lon), str(self.Mw)))

    def get_Mw(self):
        pass
        
def merge_events_and_sources(event_set_zone, event_set_fault,
                              source_model_zone, source_model_fault):
    """
    Merge two event sets and two source models.
    The order of the events and sources passed in is important.
    Fault info is concatenated to the end of zone info.
    
    """
    # FIXME Keeping the event set separate from the source model is a
    # bad idea. If each source model had a reference to its own
    # events, none of this event_set_index bookkeeping would be
    # necessary.
    
    # add's event_set_fault to the end of event_set_zone
    source_model_zone_event_set_length = len(event_set_zone)
    event_set_merged = event_set_zone + event_set_fault
    # assumes event_set_fault is at the end of event_set_zone
    source_model_merged = _add_sources(source_model_zone,
                                      source_model_fault,
                                      source_model_zone_event_set_length)
   
    return event_set_merged, source_model_merged

def _add_sources(source_model_zone, source_model_fault,
                source_model_zone_event_set_length):
    """
    Need to know the length of the event set which must also be added.
    Increase the index on the other event set ids.
    """
    assert source_model_zone._magnitude_type == \
           source_model_fault._magnitude_type
    source_list = []
    for source in source_model_fault:
        # array add, adds the others_event_set_length to all the elements
        source.set_event_set_indexes((source.get_event_set_indexes() + \
                                  source_model_zone_event_set_length))
        source_list.append(source)
    
    # list add concatenates
    mergedSourceMod = source_model.Source_Model(
        source_model_zone._sources + source_list,
        source_model_zone._magnitude_type)
    
    return mergedSourceMod
    
def generate_synthetic_events_fault(fault_xml_file, 
                                    event_control_file,
                                    prob_number_of_events_in_faults=None,
                                    store_dir=None):
    """Create Source objects from XML files for faults and events.

    fault_xml_file                   path to the FSG XML file
    event_control_file               path to the ETC XML file
    prob_number_of_events_in_faults  ?
    """      

    log.info('generating events')
    
    (fsg_list, magnitude_type) = xml_fault_generators(fault_xml_file)

    source_mods = source_model.create_fault_sources(
        event_control_file, fsg_list,
        magnitude_type)
    
    if prob_number_of_events_in_faults is None:  
        prob_number_of_events_in_faults = zeros((len(source_mods)),
                                                   dtype=EVENT_INT)      
        for i,fault in enumerate(fsg_list):
            prob_number_of_events_in_faults[i] = fault.number_of_events
    
    assert len(prob_number_of_events_in_faults) == len(source_mods)
    assert len(fsg_list) == len(source_mods)
       
        
    num_events = sum(prob_number_of_events_in_faults)
    rupture_centroid_lat = zeros((num_events), dtype=EVENT_FLOAT)
    rupture_centroid_lon = zeros((num_events), dtype=EVENT_FLOAT)
    depth_top_seismogenic = zeros((num_events), dtype=EVENT_FLOAT)
    depth_bottom_seismogenic = zeros((num_events), dtype=EVENT_FLOAT)
    azimuth = zeros((num_events), dtype=EVENT_FLOAT)
    dip = zeros((num_events), dtype=EVENT_FLOAT)
    magnitude = zeros((num_events), dtype=EVENT_FLOAT)
    source_zone_id = zeros((num_events), dtype=EVENT_INT)
    fault_type = zeros((num_events), dtype=EVENT_INT)
    depth = zeros((num_events), dtype=EVENT_FLOAT)
    fault_w=zeros((num_events), dtype=EVENT_FLOAT)
    area =zeros((num_events), dtype=EVENT_FLOAT)
    width =zeros((num_events), dtype=EVENT_FLOAT)
    length =zeros((num_events), dtype=EVENT_FLOAT)
    trace_start_lat =zeros((num_events), dtype=EVENT_FLOAT)
    trace_start_lon =zeros((num_events), dtype=EVENT_FLOAT)
    trace_end_lat =zeros((num_events), dtype=EVENT_FLOAT)
    trace_end_lon =zeros((num_events), dtype=EVENT_FLOAT)
    rupture_centroid_x =zeros((num_events), dtype=EVENT_FLOAT)
    rupture_centroid_y =zeros((num_events), dtype=EVENT_FLOAT)
    
    start=0

    for i,fault in enumerate(fsg_list):
        
        #change to use index
        source = source_mods[i]
        num = prob_number_of_events_in_faults[i]
        if num == 0:
            continue
        end = start + num
        fault_dip = fault.dip_dist['mean']
        rupture_dip = fault_dip
        depth_top = fault.depth_top_seismogenic_dist['mean']
        depth_bottom = fault.depth_bottom_seismogenic_dist['mean']
        
        fault_magnitude = fault.populate_magnitude(num)
        slab_width = fault.slab_width  
        if slab_width > 0:
            out_of_dip_theta = fault.populate_out_of_dip_theta(num,fault_dip)
        else:
            out_of_dip_theta = None
        fault_width = calc_fault_width(depth_top, 
                                     depth_bottom,
                                     fault_dip)
        
        fault_length = calc_fault_length(fault.trace_start_lat,
                                       fault.trace_start_lon,
                                       fault.trace_end_lat,
                                       fault.trace_end_lon)
        
        fault_area = fault_width * fault_length
        magnitude[start:end] = fault_magnitude  
        fault_magnitude = asarray(fault_magnitude)
        
        # If slab_width >0 then the rupture width is limited so that it does not 
        # etxend out of the slab.
        
        
        rup_area = scaling.scaling_calc_rup_area(
            fault_magnitude, source.scaling)
        rup_width = scaling.scaling_calc_rup_width(
            fault_magnitude, source.scaling, fault_dip,
            rup_area=rup_area, max_rup_width=fault_width)
        if (slab_width > 0)and (out_of_dip_theta is not None):
            max_width_in_slab = calc_max_width_in_slab(
                out_of_dip_theta,
                slab_width,fault_width)
            rup_width = minimum(rup_width,max_width_in_slab)
            
        rup_length = minimum((rup_area/rup_width),fault_length)
        
        fault_azimuth = zeros((num), dtype=EVENT_FLOAT)
        fault_azimuth[0:num] = azimuth_of_trace(fault.trace_start_lat,
                                         fault.trace_start_lon,
                                         fault.trace_end_lat,
                                         fault.trace_end_lon)
        
       
        random_scalar = random.random_sample(size=num)
        Ds = (fault_length-rup_length) * random_scalar
        
        (r_start_lat,r_start_lon) = get_new_ll(fault.trace_start_lat,
                                                fault.trace_start_lon, 
                                                fault_azimuth, 
                                                Ds)
        
        #Not sure why we bother calculating this, doesn't seem to be used
        (r_end_lat,r_end_lon) = get_new_ll(r_start_lat,
                                               r_start_lon, 
                                               fault_azimuth, 
                                               rup_length)
        if (slab_width > 0)and (out_of_dip_theta is not None):
            rupture_dip = out_of_dip_theta + fault_dip
             #for all dips greater than 180; subtract 180
            k= where(rupture_dip>=180)
            rupture_dip[k] = rupture_dip[k]-180
               
            r_depth_min = depth_top + (0.5*rup_width) * sin(radians(rupture_dip))
            r_depth_max = depth_bottom - (0.5*rup_width) * \
                      sin(radians(rupture_dip))
        else:    
            r_depth_min = depth_top + (0.5*rup_width) * sin(radians(fault_dip))
            r_depth_max = depth_bottom - (0.5*rup_width) * \
                      sin(radians(fault_dip))

        
        random_scalar = random.random_sample(size=num)
        r_depth_centroid = (r_depth_max-r_depth_min) * random_scalar \
                           + r_depth_min
        
        r_depth_top = r_depth_centroid - ((0.5*rup_width) * 
                                           sin(radians(fault_dip)))
                         
        r_depth_bottom = r_depth_centroid + ((0.5*rup_width) * 
                                              sin(radians(fault_dip)))
        
        r_y_centroid=  r_depth_centroid * ((cos(radians(fault_dip)))/
                                           (sin(radians(fault_dip))))
        
        r_x_centroid= rup_length/2
        
        (r_centroid_lat,r_centroid_lon) = xy_to_ll(r_x_centroid,
                                                   r_y_centroid,
                                                   r_start_lat,
                                                   r_start_lon, 
                                                   fault_azimuth)
        r_x_start = 0
        r_y_start = r_y_centroid -(r_depth_centroid * 
                                      ((cos(radians(fault_dip)))/
                                      (sin(radians(fault_dip)))))
        
        
        if ((slab_width > 0)&(out_of_dip_theta is not None)):
            
            r_x_start = 0.0
            r_y_start = r_y_centroid -(r_depth_centroid * 
                                      ((cos(radians(rupture_dip)))/
                                      (sin(radians(rupture_dip)))))

            r_x_end = rup_length
            r_y_end = r_y_start
            (r_start_lat_temp,r_start_lon_temp) = xy_to_ll( r_x_start, r_y_start,
                                                  r_start_lat, r_start_lon, 
                                                  fault_azimuth, 
                                                  R=6367.0)
        
       
            (r_end_lat,r_end_lon) = xy_to_ll( r_x_end, r_y_end,
                                              r_start_lat, r_start_lon, 
                                                fault_azimuth, 
                                                R=6367.0)
           
            r_start_lat= r_start_lat_temp
            r_start_lon= r_start_lon_temp
            
            
           
             #Now flip the rupture trace for those events with dip >90 Degrees
            k= where(rupture_dip>90)
            fault_azimuth[k]=fault_azimuth[k]+180
            rupture_dip[k] = 180- rupture_dip[k]
            (r_start_lat[k],r_start_lon[k],r_end_lat[k],r_end_lon[k]) = \
                                   switch_coords(r_start_lat[k],r_start_lon[k],
                                                 r_end_lat[k],r_end_lon[k])
            k = where(fault_azimuth >= 360)
            fault_azimuth[k]=fault_azimuth[k]-360
#        

         # Calculate the distance of the origin from the centroid
        #HACK
        rad = pi/180.
        x = rup_length/2.
        y = r_depth_centroid*cos(rupture_dip*rad)/sin(rupture_dip*rad)
        r_x_centroid = x
        r_y_centroid = y

        r_x_start = -x
        r_y_start = -y

        (r_start_lat,
         r_start_lon) = xy_to_ll(r_x_start,r_y_start,
                                     r_centroid_lat,r_centroid_lon,
                                     fault_azimuth)

        (r_end_lat,
         r_end_lon) = xy_to_ll(-r_x_start,r_y_start,
                                   r_centroid_lat,r_centroid_lon,
                                   fault_azimuth)  
          #FIXME DSG-EQRM the events will not to randomly placed,
            # Due to  lat, lon being spherical coords and popolate
            # working in x,y (flat 2D).
        #(lat, lon) = array(fault.populate(num)).swapaxes(0, 1) 
        eqrmlog.debug('Memory: lat,lon created')
        eqrmlog.resource_usage()
            
            #attach the current polygons generated attributes
        #if slab_width > 0:
      
            
        rupture_centroid_lat[start:end] = r_centroid_lat
        rupture_centroid_lon[start:end] = r_centroid_lon
            
        depth_top_seismogenic[start:end] = r_depth_top
        depth_bottom_seismogenic[start:end] = r_depth_bottom
        azimuth[start:end] = fault_azimuth
        fault_dip = fault.populate_dip(num)
        dip[start:end] = rupture_dip
        fault_type[start:end] = ground_motion_misc.FaultTypeDictionary[
            source.fault_type]
        depth[start:end] = r_depth_centroid
        fault_w[start:end] = fault_width
        area[start:end] = rup_width*rup_length
        width[start:end] = rup_width
        length[start:end] = rup_length
        trace_start_lat[start:end] = r_start_lat
        trace_start_lon[start:end] = r_start_lon
        trace_end_lat[start:end] = r_end_lat
        trace_end_lon[start:end] = r_end_lon
        rupture_centroid_x[start:end] = r_x_centroid
        rupture_centroid_y[start:end] = r_y_centroid
        #magnitude[start:end] = polygon_magnitude
            #print "magnitude.dtype.name", magnitude.dtype.name
        eqrmlog.debug('Memory: event set lists have been combined')
        eqrmlog.resource_usage()
        source.set_event_set_indexes(asarray(range(start,end),dtype=EVENT_INT))
        source_zone_id[start:end] = [i]*num
        start = end
    
    ML=None
    Mw=None
    if magnitude_type == 'ML':
        ML=magnitude
    elif magnitude_type == 'Mw':
        Mw=magnitude
    else:
        raise Exception('Magnitudes not set')
    if Mw is None:
        Mw = conversions.Johnston_89_Mw(ML)
    if ML is None:
        ML = conversions.Johnston_01_ML(Mw)
     #should use rupture_top
     # calculate depth_to_top from depth, width, dip
    #depth_to_top = conversions.calc_depth_to_top(depth, width, dip)
    #assert (depth_to_top == depth_top_seismogenic)
    event = Event_Set(azimuth,
                        dip,
                        ML,
                        Mw,
                        depth,
                        depth_top_seismogenic,
                        fault_type,
                        width,
                        length,
                        area,
                        fault_w,
                        None, #source_zone_id
                        trace_start_lat,
                        trace_start_lon,
                        trace_end_lat,
                        trace_end_lon,
                        rupture_centroid_x,
                        rupture_centroid_y,
                        rupture_centroid_lat,
                        rupture_centroid_lon,
                        dir=store_dir)

    event.source_zone_id = asarray(source_zone_id)
    
        #print "event.source_zone_id", event.source_zone_id
    eqrmlog.debug('Memory: finished generating events')
    eqrmlog.resource_usage()

    return event, source_mods


# dimensions
SPAWN_D = 0
GMMODEL_D = 1
RECMODEL_D = 2
EVENTS_D = 3
class Event_Activity(file_store.File_Store):
    """
    Class to manipulate the event activity value.
    Handles the logic of splitting based on spawning.
    
    The event activity is also split based on the attenuation models
    and recurrence models.  The weights in the list of sources are
    used to handle splitting between attenuation models, and
    recurrence model activity is split using the associated weights.

    Attributes:
    event_activity: probability that this event will occur is this
        year.  Takes into account;
        - The actual probability that a
        real event of the given magnitude will occur in a given year.
        - The number of synthetic events used.
        - spawning  (as a seperate dimension)
        - multiple ground motion models (as a seperate dimension)
        - multiple recurrence models (as a separate dimension)
    The dimensions of the event_activity are;
      (num_spawns, num_gm_models, num_recurrence_models, num_events)
    """
    def __init__(self, num_events, dir=None):
        """
        num_events is number of events
        """
        super(Event_Activity, self).__init__('event_activity', dir)
        
        self.event_activity = None
        self.num_events = num_events
        
    def __del__(self):
        super(Event_Activity, self).__del__()
         
    # PROPERTIES #
    # Define getters and setters for each attribute to exercise the 
    # file-based data structure
    event_activity = property(lambda self: self._get_file_array('event_activity'), 
                       lambda self, value: self._set_file_array('event_activity', value))
    # END PROPERTIES #
    
    @classmethod
    def load(cls, num_events, load_dir, store_dir=None):
        """
        Return an Event_Activity object from the .npy files stored in the specified
        directory
        """
        event_activity = cls(num_events, store_dir)
        event_activity._load(load_dir)
        return event_activity

    def save(self, dir=None):
        """
        Save the ndarray objects to the specified directory
        """
        self._save(dir)

    def set_scenario_event_activity(self):
        """
        Set the event activity for a scenario run.
       
        """
        event_indexes = arange(self.num_events)
        self.set_event_activity(ones(((1, self.num_events))), event_indexes)

        
    def set_event_activity(self, event_activities, event_indexes=None):
        """
        Assumes that spawning has not occured yet, or splitting due to 
        ground motion models.
        
        event_activities: result from calc_event_activity()
        event_indexes: the indexes of the events relating to the event
        activities
        """

        # Make sure spawning has not already occured.
        assert self.event_activity is None
        self.event_activity = zeros((1, # initial spawns
                                     1, # initial ground motion models
                                     event_activities.shape[0], # rec. models
                                     self.num_events),
                                    dtype=EVENT_FLOAT)
  
        if event_indexes == None:
            event_indexes = arange(self.num_events)
        assert len(event_indexes) == event_activities.shape[1]

        # Note: Arcane rules apply to array indexing using a mix of
        # tuples, integers and slices. See
        # http://docs.scipy.org/doc/numpy/reference/arrays.indexing.html#integer
        self.event_activity[0, 0, :, event_indexes] = event_activities.T


    def recurrence_model_count(self):
        """
        Returns the number of recurrence models.
        Only call this after .set_event_activity()
        """
        assert self.event_activity is not None
        return self.event_activity.shape[2]
        
        
    def spawn(self, weights):
        """
        Spawn the event activity.
        Do this after attenuation weighing.
        
        weights is a 1D array that sums to one.
        """
        # currently set up to only spawn once
        assert self.event_activity.shape[SPAWN_D] == 1
        wea_transposed = self.event_activity.T * weights
        self.event_activity = wea_transposed.T        

    def ground_motion_model_logic_split(self, source_model,
                                        apply_weights=True):
        """
        Given a source model, apply the attenuation weights to logically
        split the event activities.

        This must be called before any other splitting.
        This must only be called once.

        Source_model is a collection of Source's.
        """
        
        if apply_weights:
            assert self.event_activity.shape[SPAWN_D] == 1
            assert self.event_activity.shape[GMMODEL_D] == 1

            max_num_models = source_model.get_max_num_atten_models()
            
            new_event_activity = zeros((1,
                                        max_num_models,
                                        self.event_activity.shape[RECMODEL_D],
                                        self.num_events),
                                       dtype=EVENT_FLOAT)
            # this is so activities are not lost for events
            # which sources do not cover.
            new_event_activity[0, 0, :, :] = self.event_activity[0, 0, :, :]
            
            for szp in source_model:
                assert abs(sum(szp.atten_model_weights) - 1.0) < 0.01
                sub_activity = \
                    self.event_activity[0, 0, :, szp.get_event_set_indexes()]
                # sub_activity[event_index, rec_model_index] here due
                # to indexing event dim by sequence. See numpy
                # advanced indexing.
                
                # going from e.g. [0.2, 0.8] to [0.2, 0.8, 0.0]
                maxed_weights = zeros((max_num_models))
                maxed_weights[0:len(szp.atten_model_weights)] = \
                                                 szp.atten_model_weights

                activities = (sub_activity *
                              reshape(maxed_weights, (-1, 1, 1))).swapaxes(0,1)
                # activities[event_index, GM_model_index, rec_model_index]
                new_event_activity[0, :, :, szp.get_event_set_indexes()] = \
                    activities

            assert allclose(
                scipy.sum(new_event_activity, axis = GMMODEL_D),
                # self.event_activity.shape[GMMODEL_D] == 1 so we can compare directly
                self.event_activity)

            self.event_activity = new_event_activity


    def get_num_spawn(self):
        return self.event_activity.shape[SPAWN_D]

    
    def get_gmm_dimensions(self):
        """
        Get the ground motion model dimension length.
        This will be the max number of ground motion models across all
        sources if atten is not collapsed.
        WARNING, if attenuation is collapsed this will be 1.
        """
        return self.event_activity.shape[GMMODEL_D]

    def get_ea_event_dimsion_only(self):
        """
        Get the event activity collapsing the ground motion model, recurrence model
        and spawning dimensions.
        """
        return self.event_activity.reshape(-1, self.event_activity.shape[-1]).sum(axis=0)

####################################################################
from eqrm_code.source_model import source_model_from_xml, Source_Model
from eqrm_code.output_manager import save_event_set, get_source_file_handle

def generate_event_set(parallel, eqrm_flags):
    """
    Generate the event set, event activity and source model objects based on
    the parameters in eqrm_flags. Once completed call the save methods of these
    objects to store to file.
    """
    
    save_dir = os.path.join(eqrm_flags.data_dir, eqrm_flags.event_set_name)
    log.info('P%s: Generating event set and saving to %s' % (parallel.rank, save_dir))
    
    if eqrm_flags.is_scenario is True:
        # generate a scenario event set
        event_set = Event_Set.create_scenario_events(
            rupture_centroid_lat=[eqrm_flags.scenario_latitude],
            rupture_centroid_lon=[eqrm_flags.scenario_longitude],
            azimuth=[eqrm_flags.scenario_azimuth],
            dip=[eqrm_flags.scenario_dip],
            Mw=[eqrm_flags.scenario_magnitude],
            depth=[eqrm_flags.scenario_depth],
            fault_width=eqrm_flags.max_width,
            scenario_number_of_events=eqrm_flags.scenario_number_of_events,
            length=eqrm_flags.scenario_length,
            width=eqrm_flags.scenario_width,
            store_dir=eqrm_flags.data_array_storage)
        # Other rupture parameters are calculated by event_set object.
        # trace start is calculated from centroid and azimuth.
        # Rupture area, length, and width are calculated from Mw
        # using Wells and Coppersmith 94 (modified so rupture
        # width is less than fault_width).
        event_activity = Event_Activity(num_events=len(event_set), 
                                        dir=eqrm_flags.data_array_storage)
        event_activity.set_scenario_event_activity()
        event_set.scenario_setup()
        source_model = Source_Model.create_scenario_source_model(
            len(event_set))
        source_model.set_attenuation(eqrm_flags.atten_models,
                                          eqrm_flags.atten_model_weights)
    else:
        # (i.e. is_scenario is False) generate a probablistic event set
        # (using eqrm_flags.source_filename)
        # Once the event control file is 'fully operational'
        # remove the try.
        try:
            fid_event_types = get_source_file_handle(eqrm_flags,
                                                 source_file_type='event_type')
        except IOError, e:
            fid_event_types = None
            log.debug('No event typlecontrol XML file found')
            log.debug(e)
        try:
            fid_sourcepolys = get_source_file_handle(eqrm_flags, 
                                                     source_file_type='zone')
        except IOError, e:
            fid_sourcepolys = None
            log.debug('No zone source XML file found')
            log.debug(e)
      
        # tell event set which source models to calculate activity with
        if fid_sourcepolys is not None:
            source_model_zone = source_model_from_xml(
                fid_sourcepolys.name)
       
            if fid_event_types is not None:
                source_model_zone.add_event_type_atts_to_sources(
                    fid_event_types)

            if eqrm_flags.atten_models is not None and \
                eqrm_flags.atten_model_weights is not None:
                source_model_zone.set_attenuation(eqrm_flags.atten_models,
                                           eqrm_flags.atten_model_weights)
            log.debug('Memory: source_model_zone created')
            log.resource_usage()

            event_set_zone = Event_Set.generate_synthetic_events(
                fid_genpolys=fid_sourcepolys,
                source_model=source_model_zone,
                prob_number_of_events_in_zones=\
                eqrm_flags.prob_number_of_events_in_zones,
                store_dir=eqrm_flags.data_array_storage)

            log.debug('Memory: event_set_zone created')
            log.resource_usage()
        else:
            event_set_zone = None
            source_model_zone = None
        
        
        #generate event set and source_models for the fault sources
        
        try:
            fid_sourcefaults  = get_source_file_handle(
                eqrm_flags, source_file_type='fault')
        except IOError, e:
            fid_sourcefaults = None
            log.debug('No fault source XML file found')
            log.debug(e)
        if (fid_event_types is not None) and (fid_sourcefaults is not None):
            # fid_event_types.name since the zone code leaves
            # the handle at the end of the file. (I think)
            event_set_fault, source_model_fault = generate_synthetic_events_fault(
                fid_sourcefaults, 
                fid_event_types.name,
                eqrm_flags.prob_number_of_events_in_faults,
                store_dir=eqrm_flags.data_array_storage)
            
        else:
            event_set_fault = None
            source_model_fault = None
         
        # add the two event sets and source models together
        if event_set_fault is None: # assume no fault sources
            if event_set_zone is None:              
                msg = 'No fault source or zone source xml files'
                raise RuntimeError(msg)
            event_set = event_set_zone
            source_model = source_model_zone
        elif event_set_zone is None: # assume no zone sources
            event_set = event_set_fault
            source_model = source_model_fault
        else:
            # merge
            event_set, source_model = merge_events_and_sources(
                event_set_zone, event_set_fault,
                source_model_zone, source_model_fault)
                
        
        # event activity is calculated
        event_activity = Event_Activity(num_events=len(event_set), 
                                        dir=eqrm_flags.data_array_storage)
        source_model.calculate_recurrence(
            event_set,
            event_activity)
        log.debug('Memory: event activity has been calculated')
        log.resource_usage()
        
        # At this stage all the event generation has occured
        # So the Source classes should be 'downsized' to Event_Zones
    
    #  event_activity.event_activity[drop down to one dimension],
    event_activity.ground_motion_model_logic_split(
        source_model,
        not eqrm_flags.atten_collapse_Sa_of_atten_models)
        
    log.debug('Memory: Event activities split due to gmms.')
    log.resource_usage()
    
    # Add the ground motion models to the source
    source_model.set_ground_motion_calcs(eqrm_flags.atten_periods)
    
    # Save event set to standard output file
    save_event_set(eqrm_flags, event_set,
                   event_activity,
                   source_model,
                   compress=eqrm_flags.compress_output)
    event_set.area = None
    event_set.trace_end_lat = None
    event_set.trace_end_lon = None
    event_set.source_zone_id = None
    event_set.event_id = None
    
    # Save event_set, event_activity and source_model to data files
    event_set.save(save_dir)
    event_activity.save(save_dir)
    source_model.save(save_dir)
    
    return (event_set, event_activity, source_model)

def load_event_set(parallel, eqrm_flags):
    """
    Load the event set, event activity and source model objects from file as
    specified in eqrm_flags
    """
    
    load_dir = os.path.join(eqrm_flags.data_dir, eqrm_flags.event_set_name)
    log.info('P%s: Loading event set from %s' % (parallel.rank, load_dir))
    
    store_dir = eqrm_flags.data_array_storage
    
    event_set = Event_Set.load(load_dir, store_dir)
    event_activity = Event_Activity.load(len(event_set), load_dir, store_dir)
    source_model = Source_Model.load(load_dir)
    
    return (event_set, event_activity, source_model)

def create_event_set(eqrm_flags, parallel):
    """
    Implements the three modes as specified in eqrm_flags.event_set_handler
    'generate' - first node generates event set and saves to file
               - other nodes wait until first node is done
               - once first node is done, all nodes load the event set and return 
                 to the caller
    'save'     - first node generates event set and saves to file
               - any other nodes skipped
               - all nodes exit after completion
    'load'     - all nodes load the event set data from file and return to the 
                 caller
                 
    Other eqrm_flags used
    data_dir       - specifies the base directory for event set files
    event_set_name - a name for the event set generated
    
    These are used to construct the directory to save to and load from. i.e.
    the files are referenced in data_dir/event_set_name
    """
    
    mode = eqrm_flags.event_set_handler
    
    if parallel.rank == 0:
        log.info('event_set_handler = %s' % mode)
        log.info('event_set_name = %s' % eqrm_flags.event_set_name)
    
    # Wait for all nodes to be at this point to start
    parallel.barrier()
    
    if mode == 'load':
        
        (event_set,
         event_activity,
         source_model) = load_event_set(parallel, eqrm_flags)
        
    elif mode == 'generate':
            
        if parallel.rank == 0:
            (event_set,
             event_activity,
             source_model) = generate_event_set(parallel, eqrm_flags)
            # Let the workers know they can continue 
            parallel.notifyworkers(msg=parallel.load_event_set)
        else:
            log.info('P%s: Waiting for P0 to generate event set' % parallel.rank)
            parallel.waitfor(msg=parallel.load_event_set, source=0)
        
            (event_set,
             event_activity,
             source_model) = load_event_set(parallel, eqrm_flags)
         
    elif mode == 'save':
                
        if parallel.rank == 0:
            generate_event_set(parallel, eqrm_flags)
        else:
            log.warning('P%s: Saving the event set is not a parallel operation' 
                        % parallel.rank)
        
        log.info('P%s: Nothing else to do. Exiting.' % parallel.rank)
        
        parallel.finalize()
        sys.exit()
        
    else:
        raise ValueError('Got bad value for eqrm_flags.event_set_data_mode: %s'
                         % eqrm_flags.event_set_data_mode)
    
    log.info('P%s: Event set created. Number of events=%s' 
             % (parallel.rank, len(event_set.depth)))
    log.debug('Memory: Event Set created')
    log.resource_usage()
    
    return (event_set, event_activity, source_model)
        
####################################################################
# this will run if this is called from DOS prompt or double clicked
if __name__ == '__main__':
    event_num = 10  #00*1000
    eqrmlog.debug('Memory: before creating ' + str(event_num) + ' events')
    eqrmlog.resource_usage()
    event = Event_Set.create(
            rupture_centroid_lat=-33.7*ones((event_num,)),
            rupture_centroid_lon=151.3*ones((event_num,)),
            azimuth=162.6*ones((event_num,)),
            dip=35.*ones((event_num,)),
            Mw=5.*ones((event_num,)),
            fault_width=15.*ones((event_num,)),
            depth_top_seismogenic=7.*ones((event_num,))
            )
    eqrmlog.debug('Memory: after')
    eqrmlog.resource_usage()
