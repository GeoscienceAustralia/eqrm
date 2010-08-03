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

from eqrm_code.ANUGA_utilities import log
import xml.dom.minidom

from scipy import asarray, transpose, array, r_, concatenate, sin, cos, pi, \
     ndarray, absolute, allclose, zeros, ones

from eqrm_code import conversions
from eqrm_code.projections import projections
from eqrm_code.generation_polygon import polygons_from_xml
from eqrm_code.projections import azimuthal_orthographic_ll_to_xy as ll_to_xy
from eqrm_code.projections import azimuthal_orthographic_xy_to_ll as xy_to_ll
from eqrm_code.ANUGA_utilities import log as eqrmlog

class Event_Set(object):
    def __init__(self,
                 azimuth,
                 dip,
                 ML,
                 Mw,
                 depth,
                 width,
                 length,
                 area,
                 fault_width,
                 source_zone_id,
                 trace_start_lat,
                 trace_start_lon,
                 trace_end_lat,
                 trace_end_lon,
                 trace_start_x,
                 trace_start_y,
                 rupture_x,
                 rupture_y,
                 rupture_centroid_lat,
                 rupture_centroid_lon):
        """
    A set of seismic events. Can be created  either directly or from an
    XML file which generates the events from eqrm_code.generation polygons.

    If you supply rupture_centroid, distances will be calcuated using
    rupture centroids. If you supply trace start, distances will use
    trace start. (#FIXME DSG-DSG  Check this)

    Do not use event_set as an iterator, I feel it is slow, since it
    creates a new instance of event set at each iteration
    
    Attributes:
      azimuth : azimuths - scalar or n-vector
              range : [0:360)
      dip : dips  - scalar or n-vector
              range : (0:90) #TODO ask Trev or Trev - maybe [0,90], or (0,90]??
      depth : depths - scalar or n-vector, depth to event , km
            range (0:large]
            ie [5,5,10,...]        
      Mw : moment magnitudes - scalar or n-vector
         range (-large:+large) in practice ~(0:9)              
      ML : local magnitudes - scalar or n-vector
         range (-large:+large) in practice ~(0:9)         
      rupture_centroid_lat : latitude of the ruptre_centroid
                           - scalar or n-vector
                           range (-90,90)
      rupture_centroid_lon : longitude of the rupture_centroid
                          - scalor or n-vector
                          range unbounded.
                          
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
        
        self.check_arguments() 


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
               fault_depth=None, # Need for generate synthetic events
               determ_number_of_events=1):
        """generate a deterministic event set or a synthetic event set.
        Args:
          rupture_centroid_lat: Latitude of rupture centriod
          rupture_centroid_lon: Longitude of rupture centriod
          azimuth: azimuth of event, degrees
          dip: dip of virtual faults, degrees
          ML or Mw: earthquake magnitude. analysis only uses Mw.
          depth: depth to event centroid, km
          fault_width: Maximum width along virtual fault, km
          fault_depth: depth to the top of the seismmogenic region, km.
          determ_number_of_events: Number of events
          
          Note, if you supply either ML or Mw, the other will be
          calculated. If you supply both, it is up to you to ensure that
          they are consitant. Note that most funtions in EQRM use Mw (ML
          based attenuation models being one exception).

        The degrees of freedom of this interface is not quite right.      

       Returns:
         An event set instance.
         
    FIXME DSG-EQRM determ_number_of_events is actually how many times
    the deterministic
    parameters will be repeated.  But __init__ fails if the parameters
    represent more than 1 event and determ_number_of_events > 1.

        """
#         print "rupture_centroid_lat", rupture_centroid_lat
#         print "rupture_centroid_lon", rupture_centroid_lon
#         print "azimuth", azimuth
#         print "dip", dip
#         print "Mw", Mw
#         print "fault_width", fault_width
#         print "fault_depth", fault_depth
        # concatenate vectors to match matlab's treatment of
        # determ_number_of_events
        __len__='__len__'
        if determ_number_of_events>1:
            if hasattr(rupture_centroid_lat,__len__):
                rupture_centroid_lat=concatenate(
                    [rupture_centroid_lat for i in \
                     range(determ_number_of_events)])
            if hasattr(rupture_centroid_lon,__len__):
                rupture_centroid_lon=concatenate(
                    [rupture_centroid_lon for i in \
                     range(determ_number_of_events)])
            if hasattr(azimuth,__len__):
                azimuth=concatenate([azimuth for i in \
                                     range(determ_number_of_events)])
            if hasattr(dip,__len__):
                dip=concatenate([dip for i in range(determ_number_of_events)])
            if hasattr(depth,__len__):
                depth=concatenate(
                    [depth for i in range(determ_number_of_events)])    
            if hasattr(ML,__len__):
                ML=concatenate([ML for i in range(determ_number_of_events)])
            if hasattr(Mw,__len__):
                Mw=concatenate([Mw for i in range(determ_number_of_events)])
            if fault_width is not None:
                fault_width=concatenate([[fault_width] for i in \
                                         range(determ_number_of_events)])
            if fault_depth is not None:
                fault_depth=concatenate([[fault_depth] for i in \
                                         range(determ_number_of_events)])

        # There is a diff between width and fault width.
        # Width is rupture width.
        # rupture width <= fault width

        # set_vectors
        if depth is not None:
            depth=asarray(depth)

        if fault_depth is not None:
            fault_depth = asarray(fault_depth)
            if fault_depth.shape==tuple():
                if depth is not None:
                    # FIXME: Fault_depth shaping is only conditionally occuring
                    fault_depth = fault_depth+0*depth #Shaping fault_depth
        if fault_width is not None:
            fault_width = asarray(fault_width)
            if fault_width.shape==tuple():
                if depth is not None:
                    # FIXME: Fault_width shaping is only conditionally occuring
                    fault_width = fault_width+0*depth #Shaping fault_depth
                    
        rupture_centroid_lat = asarray(rupture_centroid_lat)
        rupture_centroid_lon = asarray(rupture_centroid_lon)
        azimuth = asarray(azimuth)
        dip = asarray(dip)    
        if ML is not None:
            ML = asarray(ML)
        if Mw is not None:
            Mw = asarray(Mw)

        if Mw is None:
            Mw = conversions.Johnston_89_Mw(ML)
        if ML is None:
            ML = conversions.Johnston_01_ML(Mw)
        area = conversions.modified_Wells_and_Coppersmith_94_area(Mw)
        
        width = conversions.modified_Wells_and_Coppersmith_94_width(
            dip,Mw,area,fault_width)
        if depth is None:
            depth = conversions.depth(
                fault_depth,dip,Mw,fault_width)
            
        # ROSS calc depth_to_top

        # Add function conversions
        
        length = area/width

        # Calculate the distance of the origin from the centroid
        rad = pi/180.
        x = length/2.
        y = depth*cos(dip*rad)/sin(dip*rad)
        rupture_x = x
        rupture_y = y

        trace_start_x = -x
        trace_start_y = -y

        trace_start_lat,trace_start_lon = xy_to_ll(
            trace_start_x,trace_start_y,
            rupture_centroid_lat,rupture_centroid_lon,
            azimuth)

        trace_end_lat,trace_end_lon = xy_to_ll(
            -trace_start_x,trace_start_y,
            rupture_centroid_lat,rupture_centroid_lon,
            azimuth)  

        # Currently obsolete
        if rupture_centroid_lat is None:            
            assert rupture_centroid_lon is None
            lat,lon = xy_to_ll(
                rupture_x,rupture_y,
                trace_start_lat,trace_start_lon,
                azimuth)
            trace_start_lat = lat
            trace_start_lon = lon           

        # fault_depth can be None

        # Create an Event_Set instance
        event_set = cls(azimuth,
                        dip,
                        ML,
                        Mw,
                        depth,
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
    def generate_synthetic_events(cls,
                                  fid_genpolys,
                                  fault_width,
                                  azi,
                                  dazi,
                                  fault_dip,
                                  prob_min_mag_cutoff,
                                  override_xml,
                                  prob_number_of_events_in_zones=None):
        """Randomly generate the event_set parameters.

        Note: The rupture centroid are within the polygons.  The trace
        start and end can be outside of the polygon.  The trace is on
        the surface, the centroid is underground.
        
        Args:
          fid_genpolys: The full path name of the source polygon xml file
          fault_width: Maximum width along virtual fault, km
          azi: Predominant azimuth of events, degrees *
          dazi: Azimuth range of events (azi +/- dazi) *
          fault_dip: dip of virtual faults, degrees * 
          * = can be a single value or a vector with differnet elements
              for each source zone          
          prob_min_mag_cutoff: Mimimum magnitude below which hazard is not
            considered
          override_xml: Boolean means the above arguments override the
            arguments in the xml file.  Analysis uses True
          prob_number_of_events_in_zones: Vector whose elements represent
            the number of events for each generation.
          
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
        
        generation_polygons, magnitude_type = polygons_from_xml(
            fid_genpolys,
            azi,
            dazi,
            fault_dip,
            fault_width,
            prob_min_mag_cutoff,
            override_xml)
        num_polygons=len(generation_polygons)
        
        if prob_number_of_events_in_zones is None:
            prob_number_of_events_in_zones = 1
        prob_number_of_events_in_zones = asarray(
            prob_number_of_events_in_zones)
        if not prob_number_of_events_in_zones.shape or \
               prob_number_of_events_in_zones.shape[0] == 1:
            prob_number_of_events_in_zones = prob_number_of_events_in_zones \
                                             *asarray([1]*num_polygons)
        
        #initialise new attributes
        num_events = sum(prob_number_of_events_in_zones)
        
        rupture_centroid_lat = zeros((num_events))
        rupture_centroid_lon = zeros((num_events))
        fault_depth = zeros((num_events))
        fault_width = zeros((num_events))
        azimuth = zeros((num_events))
        dip = zeros((num_events))
        magnitude = zeros((num_events))
        source_zone_id = zeros((num_events))

        start = 0
        for i in range(num_polygons):
            gp = generation_polygons[i]
            #ep = event polygon
            num = prob_number_of_events_in_zones[i]
            if num == 0:
                continue
            #populate the polygons
            polygon_fault_width=gp.populate_fault_width(num)
            eqrmlog.debug('Memory: populate_fault_width created')
            eqrmlog.resource_usage()
            polygon_fault_depth=gp.populate_fault_depth(num)
            eqrmlog.debug('Memory: populate_fault_depth created')
            eqrmlog.resource_usage()
            polygon_azimuth=gp.populate_azimuth(num)
            eqrmlog.debug('Memory: populate_azimuth created')
            eqrmlog.resource_usage()
            polygon_dip=gp.populate_dip(num)
            eqrmlog.debug('Memory: populate_dip created')
            eqrmlog.resource_usage()
            polygon_magnitude=gp.populate_magnitude(num)
            eqrmlog.debug('Memory: populate_magnitude created')
            eqrmlog.resource_usage()

            #FIXME DSG-EQRM the events will not to randomly placed,
            # Due to  lat, lon being spherical coords and popolate
            # working in x,y (flat 2D).
            lat,lon = array(gp.populate(num)).swapaxes(0,1) 
            eqrmlog.debug('Memory: lat,lon created')
            eqrmlog.resource_usage()
            
            #attach the current polygons generated attributes
            end = start + num
            rupture_centroid_lat[start:end] = lat
            rupture_centroid_lon[start:end] = lon
            
            fault_depth[start:end] = polygon_fault_depth
            fault_width[start:end] = polygon_fault_width
            azimuth[start:end] = polygon_azimuth
            dip[start:end] = polygon_dip
            magnitude[start:end] = polygon_magnitude
            
            eqrmlog.debug('Memory: event set lists have been combined')
            eqrmlog.resource_usage()
            
            # Does this mean source zone objects know nothing about
            # their id?
            source_zone_id[start:end] = [i]*num
            start = end

        new_ML=None
        new_Mw=None
        if magnitude_type == 'ML': new_ML=magnitude
        elif magnitude_type == 'Mw': new_Mw=magnitude
        else:
            raise Exception('Magnitues not set')
        
        event = Event_Set.create(
            rupture_centroid_lat=rupture_centroid_lat,
            rupture_centroid_lon=rupture_centroid_lon,
            azimuth=azimuth,
            dip=dip,
            ML=new_ML,
            Mw=new_Mw,
            fault_width=fault_width,
            fault_depth=fault_depth
            )
        event.source_zone_id=asarray(source_zone_id)
        #print "event.source_zone_id", event.source_zone_id
        eqrmlog.debug('Memory: finished generating events')
        eqrmlog.resource_usage()
        return event


    def deterministic_setup(self):
        """
        make the event activity a vector
        
        setup event ids (for deterministic simulations each id
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
        
            
    def check_arguments(self):
        """
        Checks that all arguments are the same size (or scalar).
        Returns the length of the arguments.
        """
        arguments = {'depth':self.depth,'azimuth':self.azimuth,
                     'dip':self.dip,'ML':self.ML,
                     'Mw':self.Mw,'length':self.length,
                     'rupture_centroid_lat':self.rupture_centroid_lat,
                     'rupture_centroid_lon':self.rupture_centroid_lon,
                     'event_num':self.event_num}

        n = 1 #initialise number of arguments to 1
        for key in arguments.keys():
            argument = arguments[key]
            if not argument is None:
                if not argument.size == 1:
                    if not (n==1 or n==argument.size):
                        msg = "Not all arguments are of equal size!"
                        msg+= "\nArguments size should be: "+str(n)
                        msg+= "\n"+key+" size = "+str(argument.size)
                        msg+= "\n Arguments = "+str(arguments.keys())
                        raise msg
                    n = argument.size
        return n
    
    def introspect_attributes(self):
        """
        Return a list of all the event set attributes
        """
        attributes = [att for att in dir(self) if not callable(
            getattr(self, att)) and not att[-2:] == '__']
        return attributes
    
    def introspect_attribute_values(self):
        """
        Puts all the attribite values of event set into a dictionary
        """
        attributes = [att for att in dir(self) if not callable(
            getattr(self, att)) and not att[-2:] == '__']
        att_values = {}
        for att in attributes:
            att_values[att] = getattr(self, att)
        return att_values
    
    def __getitem__(self,key):
        # This is used when events are subsetted in recurrence functions.
        if isinstance(key,int):
            key=([key])
        if key==None or ((isinstance(key,ndarray)) and
                         (key.shape==(len(self.depth),)) and
                         (key==r_[0:len(self.depth)]).all()):
            return self
        else:
            #print "self.source_zone_id", self.source_zone_id #[key]
            #print "key", key
            #print "self.source_zone_id[key]", self.source_zone_id[key]
            if self.fault_width.shape==tuple():
                fault_width=self.fault_width+0*self.width
            else:
                fault_width=self.fault_width
            
            return Event_Set(      
                self.azimuth[key],
                self.dip[key],
                self.ML[key],
                self.Mw[key],
                self.depth[key],
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
                self.rupture_centroid_lon[key]
                )
        # self.source_zone_id[key] has to be an array.
        # eg array([0])
        # additional attributes aren't carried over. eg event_id, activity.
   
    def __len__(self):
        return len(self.rupture_centroid_lat)

    def __repr__(self):
        n='\n'
        s = 'Event Set:'+n
        s = s+'number of events :'+str(self.check_arguments())+n
        s = s+'rupture_centroid lat:'
        s = s+ str(self.rupture_centroid_lat)+n
        s = s+'rupture_centroid long:'
        s = s+ str(self.rupture_centroid_lon)+n
        s = s+'Mw:'
        s = s+ str(self.Mw)+n
        return s

    def __call__(self,*multi_multi_polygons_list):
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
        """
        Draw it once for every argument.
        
        The *arguments (any number) should be sequences of multi-polygons.

        I say multi-multi-polygons to highlight the fact that each argument is
        a sequence of multi-polygons, and each multi-polygon is a sequence of
        simple polygons (and simple exclusions).
        """
        
        import wx
        app = wx.PySimpleApp()
        try: recurrence = self.recurrence
        except: recurrence = None
        
        for i in range(len(multi_multi_polygons_list)):
            multi_multi_polygons=multi_multi_polygons_list[i]
            frame=MainWindow(None,i,'Stand alone module',\
                             self.rupture_start,self.rupture_end
                             ,multi_multi_polygons=multi_multi_polygons,\
                             recurrence = recurrence)
            
        app.MainLoop()
        

def _calc_attenuation_logic_split(GM_models, model_weights, 
                            event_activity, event_num):
    """
    event_activity has to be an array
    """
    model_weights = absolute(array(model_weights))

    new_event_num = []
    new_event_activity = []
    attenuation_ids = []
    attenuation_weights = []

    for attenuation_id, GM_model in enumerate(GM_models):
        new_event_num.extend(event_num)
        attenuation_ids.extend(attenuation_id+0*event_num)

        new_event_activity.extend(
            event_activity*model_weights[attenuation_id])
        attenuation_weights.extend(
            model_weights[attenuation_id]+0*event_num)
    #FIXME Why aren't these arrays?
    return new_event_activity, new_event_num, attenuation_ids, \
           attenuation_weights

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
        """
        Instanciate this using split_logic_tree.
        """
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

        
        # Puts all the attribite values of event set into a dictionary
        att_values = event_set_instance.introspect_attribute_values()
        try:
            del att_values['event_activity']
        except KeyError:
            pass
        try:
            del att_values['event_id'] # event_num
        except KeyError:
            pass
        try:
            del att_values['event_num']
        except KeyError:
            pass
        
        super(Pseudo_Event_Set, self).__init__(**att_values)
    """
    
    """
    def __len__(self):
        return len(self.index)
    
    def __getattribute__(self, key):
        """
        Override attribute calls, so 
        """
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
    def split_logic_tree(cls,
                         event_set_instance,
                         attenuation_models,
                         weights):
        """
        Create a pseudo_event instance.

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
        event_activity, event_num, attenuation_ids, attenuation_weights = \
                        _calc_attenuation_logic_split(
            attenuation_models,
            weights, 
            event_set_instance.event_activity,
            event_set_instance.event_num)
        
        # Assertions
        # event_num is an array of [event_ids] concatenated num att models
        # times.
        # event_activity is the
        # event_activity*model_weights[attenuation_id] for each psudo_event
        pseudo_event = cls(event_set_instance,
                           event_num,
                           event_activity,
                           attenuation_ids,
                           attenuation_weights)
        
        return pseudo_event

# this will run if this is called from DOS prompt or double clicked
if __name__ == '__main__':
    event_num = 10000000
    eqrmlog.debug('Memory: before creating ' + str(event_num) + ' events')
    eqrmlog.resource_usage()
    event = Event_Set.create(
            rupture_centroid_lat=-33.7*ones((event_num,)),
            rupture_centroid_lon=151.3*ones((event_num,)),
            azimuth=162.6*ones((event_num,)),
            dip=35.*ones((event_num,)),
            Mw=5.*ones((event_num,)),
            fault_width=15.*ones((event_num,)),
            fault_depth=7.*ones((event_num,))
            )
    eqrmlog.debug('Memory: after')
    eqrmlog.resource_usage()
