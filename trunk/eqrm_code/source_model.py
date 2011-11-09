"""
 Title: sites.py
 
  Author:  Peter Row, peter.row@ga.gov.au
           
  Description: Classes to represent earthquake source models
 
  Version: $Revision: 1644 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-04-27 16:59:30 +1000 (Tue, 27 Apr 2010) $
  
  Copyright 2007 by Geoscience Australia
"""
from scipy import zeros, where, arange, asarray

from eqrm_code.recurrence_functions import calc_event_activity
from eqrm_code.polygon_class import polygon_object
from eqrm_code.xml_interface import Xml_Interface
from eqrm_code.ground_motion_calculator import \
     Multiple_ground_motion_calculator
from eqrm_code import parse_in_parameters


    
class Source_Model(object):
    """
    This is now a wrapper for a loop over self.sources.
    
    sources is a list of Source/EventZone instances.
    
    FIXME DSG: Let's push this classes methods back. - It does have
    an extra attribute magnitude_type though
    
    """
    def __init__(self, sources, magnitude_type='Mw'):
        self._sources = sources
        #print "sources in __init__", sources
        self._magnitude_type = magnitude_type
        self._max_num_atten_models = None

    def __len__(self):
        return len(self._sources)

    def __getitem__(self,key):
        return self._sources[key]
    
    
    def __repr__(self):
        n='\n'
        s = 'Source_Model:'+n
        s = s+'# of sources = '+ \
            str(len(self._sources))+n
        s = s+'sources = '+str(self._sources)+n
        s = s+'magnitude_type = '+str(self._magnitude_type)+n
        return s

    def set_attenuation(self, atten_models, atten_model_weights):
        """
        Set the models and weights to be the same for all sources
        atten_model_weights must sum to 1.0.
        """
        
        for source in self:
            source.set_atten_models_and_weights(atten_models,
                                                atten_model_weights)

            
    def add_event_type_atts_to_sources(self, event_control_file):
        """
        Given an xml event control file, add attributes from the file
        to the source models.
        """
        
        # get list of ETC objects from XML file
        etc_list = event_control_from_xml(event_control_file)

        for source in self:
            # find event in ETC list matching SOURCE event_type
            for etc in etc_list:
                if etc.event_type == source.event_type:
                    break
            else:
                msg = ("Didn't find event_type '%s' in XML file '%s'"
                   % (source.event_type, event_control_file))
                raise Exception(msg)
            # attach appropriate ETC attributes to Source object
            source.fault_type = etc.fault_type
            source.atten_models = etc.branch_models
            source.atten_model_weights = etc.branch_weights
            source.scaling = etc.scaling_dict


    def calculate_recurrence(self, event_set, event_activity):
        """
        Calculate the normalized recurrence of the event set.

        weight is the weight assigned to the respective models in
        event_set.source_models.

        This function is used by analysis
        """
        for szp in self._sources:
            if szp.get_event_set_indexes() is None:
                szp.determine_event_set_indexes(event_set)
                
        event_activity_matrix = calc_event_activity(
            event_set,
            self._sources)
        
        event_activity.set_event_activity(event_activity_matrix)

    def set_ground_motion_calcs(self, periods):
        """
        Given the attenuation periods of interest, set the
        ground motion calculators for each region.
        """
        for source in self._sources:
            source.set_ground_motion_calcs(periods)

    def get_max_num_atten_models(self):
        """
        Return the maximum number of ground motion models across all sources.
        """
        assert hasattr(self._sources[0], 'atten_model_weights')
        if self._max_num_atten_models is None:
            
            max_num_models = 1
            for source in self._sources:
                if len(source.atten_model_weights) > max_num_models:
                    max_num_models = len(source.atten_model_weights)
            self._max_num_atten_models = max_num_models

            
        return self._max_num_atten_models
        
    def is_consistant(num_events):
        """
        See if the event indexes in this source model are all unique
        and that every event is covered by this source model.

        Do we really need this?
        """
        pass

    def sources_of_event_set(self, event_length):
        """
        Return a list the length of the event_set with values being
        the Source the event came from.  Return None if the event has
        no Source (currently this should not be possible).
        """
        sources = [None] * event_length
        for source in self._sources:
            for event_ind in source.get_event_set_indexes():
                sources[event_ind] = source
        return sources
        
    
        

        
    @classmethod
    def create_scenario_source_model(cls, num_events):
        # FIXME this is highlighting that source is being used for two
        # activities
        # calculating an event activity and associating an event with
        # a ground motion model.  So split this class into two classes sometime
        if False:
            source = Source((RecurrenceModel(None, None, None, None),),
                            generation_min_mag=None,
                            name='scenario',
                            event_type=None)
        else:
            source = EventZone(name='scenario')
        source.set_event_set_indexes(arange(0, num_events))
        source_model = cls([source])
            
        return source_model

class EventZone(object):
    """A class that holds common information for a set of
    events. Currently this is the multiple gmm's associated with a set
    of events and their weights.
    
    The name of the zone, as well as the events in the zone are also known.
    """

    def __init__(self, name, 
                 event_set_indexes=None,
                 fault_type=None,
                 atten_models=None,
                 atten_model_weights=None,
                 scaling=None,
                 ground_motion_calculator=None):
        """
        """

        self.name = name
        
        # indexes to the event sets in this event zone
        self.event_set_indexes = event_set_indexes

        # The Att's that come from event type control file
        self.fault_type = fault_type
        self.atten_models = atten_models
        self.atten_model_weights = atten_model_weights
        self.scaling = scaling

        # A Multiple_ground_motion_calculator representing the
        # ground motion models
        self.ground_motion_calculator = None

    def set_event_set_indexes(self, event_indexes):
        """Add event integer indices list as an attribute.

        The integers are indexes into an event set.
        
        event_indexes  list of integers that are indexes into an event set.
        """

        self.event_set_indexes = asarray(event_indexes)

    def get_event_set_indexes(self):
        return self.event_set_indexes
        
    def set_atten_models_and_weights(self, atten_models, atten_model_weights):
        """Add attenuation model and weight attribute lists.

        atten_models   list of ground motion models
        atten_weights  list of ground motion model weights

        Also ensure that the sum of weights is 1.0.
        """

        self.atten_models = atten_models
        self.atten_model_weights = parse_in_parameters.check_sum_1_normalise(
            atten_model_weights)

    def set_ground_motion_calcs(self, periods):
        """
        """
        self.ground_motion_calculator = Multiple_ground_motion_calculator(
            self.atten_models,
            periods,
            self.atten_model_weights)
            
    def get_event_zone_instance(self):
        """
        Return an instance of EventZone.
        """
        return EventZone(name=self.name, 
                 event_set_indexes=self.event_set_indexes,
                 fault_type=self.fault_type,
                 atten_models=self.atten_models,
                 atten_model_weights=self.atten_model_weights,
                 scaling=self.scaling,
                 ground_motion_calculator=self.ground_motion_calculator)
        

class RecurrenceModel(object):
    def __init__(self,
                 recurrence_min_mag, recurrence_max_mag,
                 A_min, b,
                 distribution=None, weight=1.0):
        # Note __init__() arg names must match <recurrence_model>
        # attribute names so that RecurrenceModel(**attr_dict) works
        self.min_magnitude = float(recurrence_min_mag)
        self.max_magnitude = float(recurrence_max_mag)
        self.recurrence_model_distribution = distribution or 'bounded_gutenberg_richter'
        self.A_min = float(A_min)
        self.b = float(b)
        self.weight = float(weight)

    
class Source(EventZone):
    """A class that combines fault source generator data with that from the 
    event type control file.

    The class is created with the fault source generator data, and the
    event type control data is added later.
    """

    def __init__(self,
                 recurrence_model_seq,
                 generation_min_mag,
                 event_type,
                 name):
        """
        recurrence_model_seq: sequenec of RecurrenceModel()
        generation_min_mag - The minimum event generation specified
        by the user

        #FIXME DSG-EQRM This class needs comments.

        And where are it's methods? recurrence_functions might have 1.
        """

        self.recurrence_models = recurrence_model_seq

        # DJH FIXME handle weight - optional attr. If >1 RM, need weights on all, check total ~= 1
        # DJH FIXME store multiple RMs in model
        # FIXME write tests
            
        self.actual_min_mag_generation = max(generation_min_mag,
                                             min(m.min_magnitude for m in self.recurrence_models))
        self.event_type = event_type
        self.name = name
        super(Source, self).__init__(name)


class Source_Zone(Source, polygon_object):
    """
    Source_Zone adds boundary ploygon and exclude polygon to source,
    to describe the area of a Source.
    """
    def __init__(self,
                 boundary,
                 exclude,
                 recurrence_model_seq,
                 generation_min_mag,
                 event_type,
                 name):
        """
        boundary is a list of points that forms a polygon
        exclude is a list of polygons (so a list of a list of points)

        recurrence_model_seq: sequence of RecurrenceModel()
        
        #FIXME DSG-EQRM This class needs comments.

        And where are it's methods? recurrence_functions might have 1.
        """
        polygon_object.__init__(self, boundary, exclude)
        Source.__init__(self,
                        recurrence_model_seq,
                        generation_min_mag=generation_min_mag,
                        event_type=event_type,
                        name = name)
                 
                 
    def determine_event_set_indexes(self, event_set):
        contains_point=[self.contains_point((lat,lon), use_cach=False) 
                        for lat,lon in zip(
            event_set.rupture_centroid_lat,
            event_set.rupture_centroid_lon)]
        poly_ind=where(contains_point)[0]
        
        self.set_event_set_indexes(poly_ind)
        


def event_control_from_xml(filename):
    """Routine to read in event control data from an XML file and return a
    list of Event_Group objects containing the raw data.

    filename  is the path to the event control XML file
    """

    class Event_Group(object):
        """Class to hold event group data as attributes."""

        def __init__(self, filename, event_type, fault_type,
                     branch_list, scaling_dict):
            """Construct an object from event group data.

            filename      name of file we are reading (for debug)
            event_type    a string describing the event type
            fault_type    a string describing the fault type
            branch_list   a list of dictionaries {'model': '...',
                                                  'weight': '0.5'}
            scaling_dict  a dictionary {'scaling_rule': '...',
                                        'scaling_fault_type': '...'}

            The constructed object will have the following attributes:
                .event_type          - event type string
                .fault_type          - fault type string
                .branch_models       - list of branch models
                .branch_weights      - list of branch wrights
                .scaling_dict        - event scaling information
            """

            self.event_type = event_type
            self.fault_type = fault_type

            self.branch_models = []
            self.branch_weights = []
            for b in branch_list:
                self.branch_models.append(b['model'])
                weight = float(b['weight'])
                self.branch_weights.append(weight)
            self.branch_weights = asarray(self.branch_weights)
            msg = ("XML file %s: weights for event group '%s' should sum "
                       "to 1.0, got %.1f"
                       % (filename, event_type, sum(self.branch_weights)))
            self.branch_weights = parse_in_parameters.check_sum_1_normalise(
                self.branch_weights, msg)

            try:
                _ = scaling_dict['scaling_rule']
            except KeyError:
                msg = ("XML file %s: missing 'scaling_rule' attribute"
                       " in event group '%s'"
                       % (filename, event_type))
                raise Exception(msg)
            self.scaling_dict = scaling_dict

    # get XML doc and top-level tag object 
    try:
        doc = Xml_Interface(filename=filename)
    except Exception, e:
        msg = 'Malformed XML in file %s: %s' % (filename, str(e))
        raise Exception(msg)

    top_tag = doc['event_type_controlfile'][0]
    if len(doc['event_type_controlfile']) == 0:
        msg = ("XML file %s: expected 'event_type_controlfile' tag, got '%s'"
               % (filename, doc.xml_node.documentElement.nodeName))
        raise Exception(msg)

    # check that we have one or more 'event_group' tags
    event_groups = doc['event_group']
    if len(event_groups) == 0:
        msg = "XML file %s: expected one or more 'event_group' tags" % filename
        raise Exception(msg)

    # now cycle through 'event_group' tags
    eg_list = []
    for eg in event_groups:
        # get <event_group> attributes
        event_type = eg.attributes['event_type']

        # ensure only one <GMPE> tag and get attributes
        gmpe = eg['GMPE']
        if len(gmpe) != 1:
            msg = ("Badly formed XML in file %s: Expected exactly one "
                   "'GMPE' tag in event group '%s'"
                   % (filename, event_group))
            raise Exception(msg)
        gmpe = gmpe[0]
        fault_type = gmpe.attributes['fault_type']

        # check that we have one or more 'branch' tags under <GMPE>
        branches = gmpe['branch']
        if len(branches) == 0:
            msg = ("XML file %s: expected one or more 'branch' tags in event "
                   "group '%s'" % (filename, event_group))
            raise Exception(msg)

        branch_list = []
        for b in branches:
            branch_dict = b.attributes
            branch_list.append(branch_dict)

        # get <scaling> dictionary
        scaling = eg['scaling']
        if len(scaling) != 1:
            msg = ("Badly formed XML in file %s: Expected exactly one "
                   "'scaling' tag in event_group '%s'"
                   % (filename, event_group))
            raise Exception(msg)
        scaling = scaling[0]

        scaling_dict = scaling.attributes

        eg_obj = Event_Group(filename, event_type,
                             fault_type, branch_list, scaling_dict)
        eg_list.append(eg_obj)

    return eg_list


def create_fault_sources(event_control_file, fsg_list, magnitude_type):
    """Takes an FSG list and an event control file and creates a list
    of Source objects.

    event_control_file  path to an <event_type_controlfile> XML file
    fsg_list            list of Fault_Source_Generator objects

    Returns a source_model which is basically a list of Source objects
    containing attributes from each FSG object and attributes from the
    appropriate event in the event_control_file.
    
    """

    # for each FSG object, create a Source object from FSG and ETC attributes
    source_list = []
    for fsg in fsg_list:
        # create a Source object with some FSG attributes
        min_magnitude = fsg.magnitude_dist['minimum']
        max_magnitude = fsg.magnitude_dist['maximum']
        source = Source(
            (RecurrenceModel(
                    fsg.recurrence_min_mag,
                    fsg.recurrence_max_mag,
                    fsg.A_min,
                    fsg.b,
                    fsg.distribution),),
            fsg.generation_min_mag,
            fsg.event_type,
            fsg.name)

        # add new source to result list
        source_list.append(source)
        
    source_model = Source_Model(source_list, magnitude_type)
    source_model.add_event_type_atts_to_sources(event_control_file)
        
    return source_model


def get_recurrence_elements(xml_polygon):
    """
    xml_polygon: a DOM <zone> node

    Returns: sequence: DOM <'recurrence_model> nodes, DOM
    <event_generation> node
    """
    # Handles both the legacy XML schema, which allows one recurrence
    # model per zone, and the newer schema, which allows for multiple
    # recurrence models per zone. A document using the newer schema is
    # detected by looking for <event_generation> as an immediate child
    # of <zone>. The older style has <event_generation> as a child of a
    # single instance of <recurrence_model>

    event_gen_elements = xml_polygon['event_generation']
    recurrence_models =  xml_polygon['recurrence_model']
    # Both old and new styles can only have one <event_generation>
    # per zone, and must have at least one recurrence model
    assert len(event_gen_elements) == 1 and recurrence_models
    event_gen = event_gen_elements[0]
    assert (event_gen.xml_node.parentNode is xml_polygon.xml_node or
            len(recurrence_models)==1) # old style
    return recurrence_models, event_gen 


def source_model_from_xml(filename):
    doc=Xml_Interface(filename=filename)
    
    xml_source_model=doc['source_model_zone'][0]
    magnitude_type=xml_source_model.attributes['magnitude_type']
    
    source_zone_polygons=[]
    xml_polygons = doc['zone']
    for i, xml_polygon in enumerate(xml_polygons):
        try:
            polygon_name = xml_polygon.attributes['name']
        except KeyError:
            polygon_name = str(i)
        geometry = xml_polygon['geometry'][0]
        boundary = geometry['boundary'][0].array
        recurrence_models,  event_gen = get_recurrence_elements(xml_polygon)
        area = float(xml_polygon.attributes['area'])
        event_type = xml_polygon.attributes['event_type']

        generation_min_mag = float(event_gen.attributes[
            'generation_min_mag'])
        
        exclude=[]
        for exclusion_zone in xml_polygon['excludes']:
            exclude.append(exclusion_zone.array)
        #print 'LAMBDAMIN 1 ',A_min
        
        source_zone_polygon = Source_Zone(
            boundary,
            exclude,
            [RecurrenceModel(**rm.attributes)
             for rm in recurrence_models],
            generation_min_mag,
            event_type,
            polygon_name)
        source_zone_polygons.append(source_zone_polygon)
        
    doc.unlink()
    return Source_Model(source_zone_polygons,magnitude_type)
