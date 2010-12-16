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

from scipy import asarray, transpose, array, r_, concatenate, sin, cos, pi, \
     ndarray, absolute, allclose, zeros, ones, float32, int32, float64, \
     int64, reshape, arange, append, radians, where, minimum
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

# This specifies the dtypes used in  event set.
# This was investigated to save memory
# Float32 gives differnet results between windows and linux
# therefore let's not use it.
EVENT_FLOAT = float64 #float32
EVENT_INT = int64 #int32


class Dummy:
    def __init__(self):
        pass

    
class Event_Set(object):
    def __init__(self, azimuth, dip, ML, Mw,
                 depth, depth_to_top, fault_type,
                 width, length, area, fault_width,
                 source_zone_id,
                 trace_start_lat, trace_start_lon,
                 trace_end_lat, trace_end_lon,
                 trace_start_x, trace_start_y,
                 rupture_x, rupture_y,
                 rupture_centroid_lat, rupture_centroid_lon,
                 event_activity=None):
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
                         
      event_activity: probability that this event will occur is this
        year.  Takes into account; - The actual probability that a
        real event of the given magnitude will occur in a given year.
        - The number of synthetic events used.  

      
        can have:
          rupture_centroid_lat
          rupture_centroid_lon
        or        
          rupture_x
          rupture_y
          

    generation parameters
    ---------------------
    filename : generation polygons in target file 
               (see 'sample_event.xml')


        """
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
        self.trace_start_x = trace_start_x
        self.trace_start_y = trace_start_y
        self.rupture_x = rupture_x
        self.rupture_y = rupture_y
        self.rupture_centroid_lat = rupture_centroid_lat
        self.rupture_centroid_lon = rupture_centroid_lon
        self.event_num = r_[0:len(self.depth)] # gives every event an id
        self.event_activity = event_activity
        self.check_arguments() 


    @classmethod
    def create(cls, rupture_centroid_lat, rupture_centroid_lon, azimuth,
               dip=None, ML=None, Mw=None, depth=None, fault_width=None,
               depth_top_seismogenic=None, # Need for generate synthetic events
               depth_bottom_seismogenic=None,
               fault_type=None,area=None, width=None, length=None):
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

    Should accept a fault type and use that instead of hardcoded 'reverse'.
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
            
        if area is None:
            area = conversions.modified_Wells_and_Coppersmith_94_area(Mw)
        #print "Mw", Mw
#        area_old = conversions.modified_Wells_and_Coppersmith_94_area(Mw)
#        assert allclose(area, area_old)
            
        # finish turning into arrays arrays
                
        if fault_width is None:
            fault_width = (depth_bottom_seismogenic \
                           - depth_top_seismogenic)/ \
                           sin(dip*math.pi/180.)
#         fault_width_old = (depth_bottom_seismogenic \
#                            - depth_top_seismogenic)/ \
#                            sin(dip*math.pi/180.)
#         assert allclose(fault_width, fault_width_old)
        if width is None:
            width = conversions.\
                modified_Wells_and_Coppersmith_94_width(dip, Mw, area,
                                                        fault_width)
#         print "dip", dip
#         print "Mw", Mw
#         print "area", area
#         print "fault_width", fault_width
#        Width_old = conversions.\
#                modified_Wells_and_Coppersmith_94_width(dip, Mw, area,
#                                                        fault_width)
#        print "width", width
#        print "width_old", width_old
#        assert allclose(width, width_old)
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

        # Add function conversions
        if length is None:
            length = area/width

        # Calculate the distance of the origin from the centroid
        rad = pi/180.
        x = length/2.
        y = depth*cos(dip*rad)/sin(dip*rad)
        rupture_x = x
        rupture_y = y

        trace_start_x = -x
        trace_start_y = -y

        (trace_start_lat,
         trace_start_lon) = xy_to_ll(trace_start_x,trace_start_y,
                                     rupture_centroid_lat,rupture_centroid_lon,
                                     azimuth)

        (trace_end_lat,
         trace_end_lon) = xy_to_ll(-trace_start_x,trace_start_y,
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
                        trace_start_x,
                        trace_start_y,
                        rupture_x,
                        rupture_y,
                        rupture_centroid_lat,
                        rupture_centroid_lon)
        return event_set
    
    
    @classmethod
    def create_scenario_events(cls, rupture_centroid_lat,
                               rupture_centroid_lon, azimuth,
                               dip, Mw, depth, 
                               scenario_number_of_events,
                               fault_width=None,
                               depth_top_seismogenic=None, 
                               depth_bottom_seismogenic=None):
        
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
        else:
            rupture_centroid_lat = asarray(rupture_centroid_lat)
            rupture_centroid_lon = asarray(rupture_centroid_lon)
            azimuth = asarray(azimuth)
            dip = asarray(dip)
            depth = asarray(depth)
            Mw = asarray(Mw)
                
        event = Event_Set.create(rupture_centroid_lat=rupture_centroid_lat,
                                 rupture_centroid_lon=rupture_centroid_lon,
                                 azimuth=azimuth,
                                 dip=dip,
                                 Mw=Mw,
                                 depth=depth,
                                 fault_width=fault_width,
                                 depth_top_seismogenic=depth_top_seismogenic,
                                 depth_bottom_seismogenic=
                                 depth_bottom_seismogenic)
        return event
        

    @classmethod
    def generate_synthetic_events(cls, fid_genpolys,
                                  prob_min_mag_cutoff,
                                  source_model,
                                  prob_number_of_events_in_zones=None):
        """Randomly generate the event_set parameters.

        Note: The rupture centroid are within the polygons.  The trace
        start and end can be outside of the polygon.  The trace is on
        the surface, the centroid is underground.
        
        Args:
          fid_genpolys: The full path name of the source polygon xml file
          prob_min_mag_cutoff: Mimimum magnitude below which hazard is not
            considered.
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

        log.info('generating events')
        
        (generation_polygons,
             magnitude_type) = polygons_from_xml(fid_genpolys,
                                                 prob_min_mag_cutoff)
        num_polygons = len(generation_polygons)
        assert num_polygons == len(source_model)
        
        if prob_number_of_events_in_zones is None:
            prob_number_of_events_in_zones = zeros((len(generation_polygons)),
                                                   dtype=EVENT_INT)
            for i,gen_poly in enumerate(generation_polygons):
                prob_number_of_events_in_zones[i] = gen_poly.number_of_events
            # The number of events is not specified in the control file
            # use the number of events in the xml file.
#             prob_number_of_events_in_zones = 1
#         prob_number_of_events_in_zones = asarray(prob_number_of_events_in_zones)
#         if (not prob_number_of_events_in_zones.shape or
#             prob_number_of_events_in_zones.shape[0]) == 1:
#             prob_number_of_events_in_zones = prob_number_of_events_in_zones* \
#                                                 asarray([1]*num_polygons)
        
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
        
        #number_of_mag_sample_bins = zeros((num_events), dtype=EVENT_INT)

        #print "magnitude.dtype.name", magnitude.dtype.name
        start = 0
        for i, source in enumerate(source_model):
            gp = generation_polygons[i]
            
            num = prob_number_of_events_in_zones[i]
            end = start + num
            
            source.set_event_set_indexes(arange(start, end))
            
            if num == 0:
                continue

            #populate the polygons
            polygon_depth_top_seismogenic = gp.populate_depth_top_seismogenic(
                num)
            eqrmlog.debug('Memory: populate_depth_top_seismogenic created')
            eqrmlog.resource_usage()
            polygon_azimuth = gp.populate_azimuth(num)
            eqrmlog.debug('Memory: populate_azimuth created')
            eqrmlog.resource_usage()
            polygon_dip = gp.populate_dip(num)
            #rint "polygon_dip", polygon_dip
            eqrmlog.debug('Memory: populate_dip created')
            eqrmlog.resource_usage()
            polygon_magnitude = gp.populate_magnitude(num)
            eqrmlog.debug('Memory: populate_magnitude created')
            eqrmlog.resource_usage()
            polygon_depth_bottom = gp.populate_depth_bottom_seismogenic(num)

            #FIXME DSG-EQRM the events will not to randomly placed,
            # Due to  lat, lon being spherical coords and popolate
            # working in x,y (flat 2D).
            (lat, lon) = array(gp.populate(num)).swapaxes(0, 1) 
            eqrmlog.debug('Memory: lat,lon created')
            eqrmlog.resource_usage()
            
            #attach the current polygons generated attributes
            rupture_centroid_lat[start:end] = lat
            rupture_centroid_lon[start:end] = lon
            
            depth_top_seismogenic[start:end] = polygon_depth_top_seismogenic
            depth_bottom_seismogenic[start:end] = polygon_depth_bottom
            azimuth[start:end] = polygon_azimuth
            dip[start:end] = polygon_dip
            magnitude[start:end] = polygon_magnitude
            #number_of_mag_sample_bins[start:end] = mag_sample_bins
            #print "magnitude.dtype.name", magnitude.dtype.name
            fault_width[start:end] = (depth_bottom_seismogenic[start:end] \
                           - depth_top_seismogenic[start:end])/ \
                           sin(dip[start:end]*math.pi/180.)
            area[start:end] = scaling.scaling_calc_rup_area(
                magnitude[start:end], source.scaling)
            #print "source.scaling", source.scaling
            #print "magnitude[start:end]", magnitude[start:end]
            #print "dip[start:end]", dip[start:end]
            #print "rup_area=area[start:end", area[start:end]
            #print "max_rup_width=fault_width[start:end]", fault_width[start:end]
            width[start:end] = scaling.scaling_calc_rup_width(
                magnitude[start:end], source.scaling, dip[start:end],
                rup_area=area[start:end], max_rup_width=fault_width[start:end])
            eqrmlog.debug('Memory: event set lists have been combined')
            eqrmlog.resource_usage()

            
            # Does this mean source zone objects know nothing about
            # their id?
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
                                 depth_bottom_seismogenic=
                                 depth_bottom_seismogenic,
                                 fault_width=fault_width,
                                 area=area,
                                 width=width)
        event.source_zone_id = asarray(source_zone_id)
        eqrmlog.debug('Memory: finished generating events')
        eqrmlog.resource_usage()

        return event

    
    def scenario_setup(self):
        """make the event activity a vector
        
        setup event ids (for scenario simulations each id
        points to a new copy of the same event.
        These copies are necessary if Monte-Carlo techniques are used
        for things like ground motion and amplification etc.

        Attributes that are tacked onto an event_set instance.
        """
        # Moved from analysis        
        self.event_activity = array(0*self.depth+1) # create a vector of 1's
        self.source_zone_id = array(0*self.depth+1) # create a vector of 1's


    def set_event_activity(self, event_activity):
        """        
        Set event activity boiler plate code.  I'm doing this so I
        know when this is being set.        
        """
        self.event_activity = asarray(event_activity)

            
    def remove_events_with_no_activity(self):
        """        
        Set event activity boiler plate code.  I'm doing this so I
        know when this is being set.

        returns an event instance which is a subset of this event index.
          where all events with 0 event activity have been removed.
        """
        event_activity_index = where(event_set.event_activity!=0)
        return self[event_activity_index]

        
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
                     'event_num': self.event_num}

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

        return [att for att in dir(self) if not callable(getattr(self, att))
                                         and not att[-2:] == '__']
    
    def introspect_attribute_values(self):
        """Puts all the attribute values of event set into a dictionary"""

        attributes = [att for att in dir(self)
                      if not callable(getattr(self, att))
                      and not att[-2:] == '__']
        att_values = {}
        for att in attributes:
            att_values[att] = getattr(self, att)

        return att_values
    
    def __getitem__(self, key):
        """Get slice of this Event_Set.

        Returns a new Event_Set object containing the sliced data.
        Additional attributes aren't carried over. eg event_id, activity.
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
            fault_width = self.fault_width + 0*self.width
        else:
            fault_width = self.fault_width

        if self.event_activity == None:
            event_activity = None
        else:
            event_activity = self.event_activity[key] 

        # create and return a slice of the Event_Set data values
        return Event_Set(self.azimuth[key],
                         self.dip[key],
                         self.ML[key],
                         self.Mw[key],
                         self.depth[key],
                         self.depth_to_top[key],
                         self.fault_type[key],
                         self.width[key],
                         self.length[key],
                         self.area[key],
                         fault_width[key],
                         self.source_zone_id[key],
                         self.trace_start_lat[key],
                         self.trace_start_lon[key],
                         self.trace_end_lat[key],
                         self.trace_end_lon[key],
                         self.trace_start_x[key],
                         self.trace_start_y[key],
                         self.rupture_x[key],
                         self.rupture_y[key],
                         self.rupture_centroid_lat[key],
                         self.rupture_centroid_lon[key],
                         event_activity)
   
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

    def __call__(self, *multi_multi_polygons_list):
        """
        WARNING: not tested/ used.  probably broken.
        
        Calling event set will draw it once for every argument.
        
        The *arguments (any number) should be sequences of multi-polygons.

        I say multi-multi-polygons to highlight the fact that each argument is
        a sequence of multi-polygons, and each multi-polygon is a sequence of
        simple polygons (and simple exclusions).
        """

        self.draw(*multi_multi_polygons_list)

    def draw(self,*multi_multi_polygons_list):
        """Draw it once for every argument.
        
        The *arguments (any number) should be sequences of multi-polygons.

        I say multi-multi-polygons to highlight the fact that each argument is
        a sequence of multi-polygons, and each multi-polygon is a sequence of
        simple polygons (and simple exclusions).
        """
        
        import wx

        app = wx.PySimpleApp()
        try:
            recurrence = self.recurrence
        except:
            recurrence = None
        
        for i in xrange(len(multi_multi_polygons_list)):
            multi_multi_polygons = multi_multi_polygons_list[i]
            frame = MainWindow(None, i, 'Stand alone module',
                               self.rupture_start, self.rupture_end,
                               multi_multi_polygons=multi_multi_polygons,
                               recurrence=recurrence)
        app.MainLoop()
        

def _calc_attenuation_logic_split(GM_models, model_weights, 
                                  event_activity, event_num):
    """event_activity has to be an array"""

    model_weights = absolute(array(model_weights))

    new_event_num = []
    new_event_activity = []
    attenuation_ids = []
    attenuation_weights = []

    for attenuation_id, GM_model in enumerate(GM_models):
        new_event_num.extend(event_num)
        attenuation_ids.extend(attenuation_id+0*event_num)

        new_event_activity.extend(event_activity*model_weights[attenuation_id])
        attenuation_weights.extend( model_weights[attenuation_id]+0*event_num)

    #FIXME Why aren't these arrays?
    return (new_event_activity, new_event_num,
            attenuation_ids, attenuation_weights)
    
    
def merge_events_and_sources(event_set_zone, event_set_fault,
                              source_model_zone, source_model_fault):
    """
    Merge two event sets and two source models.
    The order of the events and sources passed in is important.
    Fault info is concatenated to the end of zone info.
    
    """
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
        source.event_set_indexes=(source.event_set_indexes + \
                                  source_model_zone_event_set_length)
        source_list.append(source)
    
    # list add concatenates
    mergedSourceMod = source_model.Source_Model(
        source_model_zone._sources + source_list,
        source_model_zone._magnitude_type)
    
    return mergedSourceMod
    
def generate_synthetic_events_fault(fault_xml_file, event_control_file,
                                    prob_min_mag_cutoff, 
                                    prob_number_of_events_in_faults=None):
    """Create Source objects from XML files for faults and events.

    fault_xml_file                   path to the FSG XML file
    event_control_file               path to the ETC XML file
    prob_min_mag_cutoff              min mag below which hazard not considered
    prob_number_of_events_in_faults  ?
    """      

    log.info('generating events')
    
    (fsg_list, magnitude_type) = xml_fault_generators(fault_xml_file, 
                                                      prob_min_mag_cutoff)

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
    trace_start_x =zeros((num_events), dtype=EVENT_FLOAT)
    trace_start_y =zeros((num_events), dtype=EVENT_FLOAT)
    rupture_x =zeros((num_events), dtype=EVENT_FLOAT)
    rupture_y =zeros((num_events), dtype=EVENT_FLOAT)
    
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
        trace_start_x[start:end] = r_x_start
        trace_start_y[start:end] = r_y_start
        rupture_x[start:end] = r_x_centroid
        rupture_y[start:end] = r_y_centroid
        #magnitude[start:end] = polygon_magnitude
            #number_of_mag_sample_bins[start:end] = mag_sample_bins
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
                        trace_start_x,
                        trace_start_y,
                        rupture_x,
                        rupture_y,
                        rupture_centroid_lat,
                        rupture_centroid_lon)

    event.source_zone_id = asarray(source_zone_id)
    
        #print "event.source_zone_id", event.source_zone_id
    eqrmlog.debug('Memory: finished generating events')
    eqrmlog.resource_usage()

    #return create_fault_sources(event_control_file, fsg_list)

    return event, source_mods
   
    
    
class Pseudo_Event_Set(Event_Set):
    """
    A pseudo event set is like an event set except it takes into account
    logic tree splits.

    The only logic tree split currently is if one or more attenuation
    models are used.

    Attributes:
      index: An array of indexes representing the event each
        pseudo event is representing.
      event_activity: The multiplier that must be applied to each pseudo
        event/ event to represent a real earthquake.
      att_model: The attenuation model associated with each pseudo event
      
    """
    
    def __init__(self, event_set_instance, index, event_activity,
                 att_model_index, attenuation_weights):
        """Instantiate this using split_logic_tree. """

        # Note this is hardcoding a speed/memory trade-of in favour of
        # saving memory.

        # Warning - the way the attributes from event_set are added
        # means that some idioms are very slow, such as;
        # for i in range(x): pseudo_event.depth[i]
        # this is much faster
        # depth = pseudo_event.depth; for i in range(x):depth[i]
        #
        # This might be a good reason to scrap overriding __getattribute__
        
        # WARNING, WHEN ADDING/CHANGING ATTRIBUTES __getattribute__
        # HAS TO BE MODIFIED.
        # These are the attributes that incexed directly,
        # rather than indexed indirectly into an event set instance.
        # This attribute converts a pseudo_event_index into a event_index
        # e.g. it looks like [0,1,2,0,1,2]
        self.index = asarray(index)
        self.event_activity = asarray(event_activity)

        # att_model_index - Not currently used (except for outputting to file)
        # Index into the GM_models array. e.g. 0 is the first model,
        # 1 the second.
        self.att_model_index = asarray(att_model_index)

        # if the att weights were (.8, .2) and there were 2 events
        # this is (.8, .8, .2, .2) it is used in exceedance curves.
        self.attenuation_weights = asarray(attenuation_weights)
        # WARNING, WHEN ADDING/CHANGING ATTRIBUTES __getattribute__
        # HAS TO BE MODIFIED.

        # WARNING att_model_index

        # Puts all the attribute values of event set into a dictionary
        att_values = event_set_instance.introspect_attribute_values()
        for a in ('event_activity', 'event_id', 'event_num'):
            try:
                del att_values[a]
            except KeyError:
                pass

        super(Pseudo_Event_Set, self).__init__(**att_values)

        # This overwrites the None value that can be set in event_set
        self.event_activity = asarray(event_activity)
        
    def __len__(self):
        return len(self.index)
    
    def __getattribute__(self, key):
        """Override attribute calls, so ..."""

        v = object.__getattribute__(self, key)
        _index = object.__getattribute__(self, 'index')
        if hasattr(v, '__get__'):
            return v.__get__(None, self) #[_index]

        if (key == 'event_activity' or
            key == 'index' or
            key == 'attenuation_weights' or
            key == 'att_model_index'):
            return v
        else:
            return v[_index]

    @classmethod
    def split_logic_tree(cls, event_set_instance, attenuation_models, weights):
        """Create a pseudo_event instance.

        parameters
          event_set_instance:
          attenuation_models: list of strings reprenting att mod' used.
            e.g.  ['Toro_1997_midcontinent', 'Atkinson_Boore_97', 'Sadigh_97']
            From the list in analysis.py (Yes, this is not good.);
            attenuation_models_dict={0:'Gaull_1990_WA',
                             1:'Toro_1997_midcontinent',
                             2:'Atkinson_Boore_97',
                             3:'Sadigh_97',
                             6:'Youngs_97',
                             7:'Combo_Sadigh_Youngs_M8'}
          weights: list of floats reprenting the weights for att models.
            e.g.  [-0.33333333 -0.33333333 -0.33333333]
        """

        #print "attenuation_models", attenuation_models
        #print "weights", weights
        (event_activity, event_num, attenuation_ids, attenuation_weights) = \
           _calc_attenuation_logic_split(attenuation_models, weights, 
                                         event_set_instance.event_activity,
                                         event_set_instance.event_num)
        # Assertions
        # event_num is an array of [event_ids] concatenated num att models
        # times.
        # event_activity is the
        # event_activity*model_weights[attenuation_id] for each psudo_event
        return cls(event_set_instance, event_num, event_activity,
                   attenuation_ids, attenuation_weights)

# dimensions
SPAWN_D = 0
GMMODEL = 1
EVENTS = 2
class Event_Activity(object):
    """
    Class to manipulate the event activity value.
    Handles the logic of splitting based on spawning.
    
    The event activity is NOT split based on the attenuation models.
    Use the weights in the list of sources to handle this.


    The dimensions of the event_activity are;
      (num_spawns, num_gm_models, num_events)
    """
    def __init__(self, num_events):
        """
        num_events is number of events
        """
        self.event_activity = zeros((1,1,num_events),
                                    dtype=EVENT_FLOAT)
        self.num_events = num_events
         

    def set_scenario_event_activity(self):
        event_indexes = arange(self.num_events)
        self.set_event_activity(ones((self.num_events)), event_indexes)

        
    def set_event_activity(self, event_activities, event_indexes=None):
        """

        Assumes that spawning has not occured yet.
        
        Parameters
        event_indexes - the indexes of the events relating to the
          event activities
          
        """

        # Make sure spawning has not already occured.
        assert self.event_activity.shape[SPAWN_D] == 1
        
        if event_indexes == None:
            event_indexes = arange(self.num_events)
        assert len(event_indexes) == len(event_activities)
        self.event_activity[0,0, event_indexes] = event_activities

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
        
        if apply_weights is False:
            pass
        else:
            assert self.event_activity.shape[SPAWN_D] == 1
            assert self.event_activity.shape[GMMODEL] == 1

            max_num_models = source_model.get_max_num_atten_models()
            new_event_activity = zeros((1, max_num_models,
                                        self.num_events),
                                       dtype=EVENT_FLOAT)
            # this is so activities are not lost for events
            # which sources do not cover.
            new_event_activity[0,0,:] = self.event_activity[0,0,:]
            
            for szp in source_model:
                assert sum(szp.atten_model_weights) == 1
                #self.event_activity[szp.event_set_indexes] =
                sub_activity = self.event_activity[0,0,szp.event_set_indexes]
                # going from e.g. [0.2, 0.8] to [0.2, 0.8, 0.0]
                maxed_weights = zeros((max_num_models))
                maxed_weights[0:len(szp.atten_model_weights)] = \
                                                 szp.atten_model_weights
                activities = sub_activity * reshape(maxed_weights, (-1,1))
                overwrite = new_event_activity[0,:,szp.event_set_indexes]
                new_event_activity[0,:,szp.event_set_indexes] = activities.T
            assert allclose(scipy.sum(new_event_activity, axis=GMMODEL),
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
        return self.event_activity.shape[GMMODEL]

    def get_ea_event_dimsion_only(self):
        """
        Get the event activity collapsing the ground motion model
        and spawning dimensions.
        """
        return scipy.sum(scipy.sum(self.event_activity, axis=SPAWN_D),
                         axis=(GMMODEL-1))  
        
        

    
class Obsolete_Event_Activity(object):
    """
    Class to manipulate the event activity value.
    Handles a lot of the logic splitting in EQRM.
    It assumes the logic splitting is done in a certain order.
    First the event activities are added, then they are logically
    spit based on the attenuation models.

    The next split is based on spawning.

    Only call the splitting method once.

    The dimensions of the event_activity are;
      (num_events, max_num_models, num_spawns)
    """
    def __init__(self, num_events, max_num_models=1, num_spawns=1):
        """
        num_events is number of events
        max_num_models is the maximum number of ground motion models
          for any source.
        num_spawns is the number of spawned events.
        """
        self.event_activity = zeros((num_events, max_num_models, num_spawns),
                                    dtype=EVENT_FLOAT)
        self.max_num_models = max_num_models
        self.num_events = num_events
        

    def set_scenario_event_activity(self):
        event_indexes = arange(self.num_events)
        self.set_event_activity(ones((self.num_events)), event_indexes)

        
    def set_event_activity(self, event_activities, event_indexes=None):
        """
        event_indexes - the indexes of the events relating to the
          event activities
        """
        if event_indexes == None:
            event_indexes = arange(self.num_events)
        assert len(event_indexes) == len(event_activities)
        self.event_activity[event_indexes, 0, 0] = event_activities

        
    def scenario_attenuation_logic_split(self, atten_model_weights):
        source_model = Dummy()
        source_model.event_set_indexes = arange((self.num_events))
        source_model.atten_model_weights = atten_model_weights       
        self.attenuation_logic_split([source_model])
    
    def attenuation_logic_split(self, source_model):
        """
        Given a source model, apply the attenuation weights to logically
        split the event activities.

        This must be called before any other splitting.
        This must only be called once.

        Source_model is a collection of Source's.
        """
        
        unsplit_event_activity = copy.copy(self.event_activity[:,0,0])
        
        for szp in source_model:
            assert sum(szp.atten_model_weights) == 1
            #self.event_activity[szp.event_set_indexes] =
            sub_activity = unsplit_event_activity[szp.event_set_indexes]
            # going from e.g. [0.2, 0.8] to [0.2, 0.8, 0.0]
            maxed_weights = zeros((self.max_num_models))
            maxed_weights[0:len(szp.atten_model_weights)] = \
                                                      szp.atten_model_weights
            activities = sub_activity * reshape(maxed_weights, (-1,1))
            self.event_activity[szp.event_set_indexes, :, 0] = activities.T

    def spawn(weights):
        """
        Spawn the event activity.
        
        weights is a ??D array that sums to one.

        Has to handle that the GM is interated over and that the
        weights are different for each event.
        
        Make len(weight) copies, in the 3rd dimension, of the current
        event activity, applying the weights.

        This value is set as the new event activity.
        
        """
        pass
    
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
