"""
 Title: sites.py
 
  Author:  Peter Row, peter.row@ga.gov.au
           
  Description: Classes to represent earthquake source models
 
  Version: $Revision: 1644 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-04-27 16:59:30 +1000 (Tue, 27 Apr 2010) $
  
  Copyright 2007 by Geoscience Australia
"""
from scipy import zeros, where

from eqrm_code.recurrence_functions import calc_event_activity
from eqrm_code.polygon_class import polygon_object
from eqrm_code.xml_interface import Xml_Interface



class Source_Models(object):
    """
    Class to handle multiple Source Models.

    Code can currently only handle one Source Model
    """
    def __init__(self,prob_min_mag_cutoff, weight,
                              number_of_mag_sample_bins, *filenames):
        #print "prob_min_mag_cutoff", prob_min_mag_cutoff
        #print "weight", weight
        #print "*filenames", filenames
        self.weight = weight
        source_models=[]
        for fid_sourcepolys in filenames:
            source_model=source_model_from_xml(fid_sourcepolys.name,
                                               prob_min_mag_cutoff,
                                               number_of_mag_sample_bins)
            source_models.append(source_model)
        self.source_models=source_models
        
        assert len(self.weight) == len(self.source_models)
        
    def __len__(self):
        return len(self.source_models)

    def __getitem__(self,key):
        return self.source_models[key]
    
    def calculate_recurrence(self, event_set, prob_number_of_mag_sample_bins,
                             event_activity):
        """
        Calculate the normalized recurrence of the event set.

        weight is the weight assigned to the respective models in
        event_set.source_models.

        This function is used by analysis
        """
        #print "event_set", event_set
        source_models = self.source_models

        for szp in source_models[0]:
            if szp.event_set_indexes is None:
                szp.determine_event_set_indexes(event_set)
                
        event_activity_matrix = calc_event_activity(
            event_set,
            source_models[0],
            prob_number_of_mag_sample_bins)
        # Assuming only 1 source model
        event_activity.set_event_activity(event_activity_matrix)
        
    
    def stratify_source_models_obsolete(self,independent_polygons = None):
        """
        Stratify self.source_models.
        
        independent_polygons defaults to self.self.generation_polygons -
        the usual case.
        
        Stratifies the sources, so that the source polygons are
        independent, and do no source polygon crosses into more than
        one independent polygon.
        """
        if independent_polygons is None:
            from polygon_class import get_independent_polygons_obsolete \
                 as independent
            independent_polygons = independent(self.generation_polygons)
            if not len(independent_polygons) == len(self.generation_polygons):
                logging.info( \
                    'Had to make the generation_polygons independent!!!')

        for i in range(len(self.source_models)):
            source_model = self.source_models[i]
            source_model = source_model.stratified(independent_polygons)
            self.source_models[i] = source_model


class Source_Model(object):
    """
    This is now a wrapper for a loop over self.source_zone_polygons.
    
    source_zone_polygons is a list of Source_Zone_Polygon instances.
    
    FIXME DSG: Let's push this classes methods back. - It does have
    an extra attribute magnitude_type though
    
    """
    def __init__(self, source_zone_polygons,magnitude_type):
        self._source_zone_polygons = source_zone_polygons
        #print "source_zone_polygons in __init__", source_zone_polygons
        self._magnitude_type=magnitude_type

    def __len__(self):
        return len(self._source_zone_polygons)

    def __getitem__(self,key):
        return self._source_zone_polygons[key]
    
    def __repr__(self):
        n='\n'
        s = 'Source_Model:'+n
        s = s+'# of source_zone_polygons = '+ \
            str(len(self._source_zone_polygons))+n
        s = s+'source_zone_polygons = '+str(self._source_zone_polygons)+n
        s = s+'magnitude_type = '+str(self._magnitude_type)+n
        return s

    def set_attenuation(self, atten_models, atten_model_weights):
        """

        atten_model_weights must sum to 1.0.
        """
        
        for poly_zone in self:
            poly_zone.set_atten_models_and_weights(atten_models,
                                                   atten_model_weights)
            
class Source(object):
    """A class that combines fault source generator data with that from the 
    event type control file.

    The class is created with the FSG data, and the ETC data is added later.
    """

    def __init__(self, min_magnitude, max_magnitude, prob_min_mag_cutoff,
                 A_min, b, number_of_mag_sample_bins,
                 recurrence_model_distribution='bounded_gutenberg_richter'):
        """
        min_magnitude,max_magnitude,
        prob_min_mag_cutoff,A_min,b are floats
        
        #FIXME DSG-EQRM This class needs comments.
        What is prob_min_mag_cutoff?

        And where are it's methods? recurrence_functions might have 1.
        """

        self.min_magnitude = min_magnitude
        self.max_magnitude = max_magnitude
        self.prob_min_mag_cutoff = prob_min_mag_cutoff
        self.A_min = A_min
        self.b = b
        self.number_of_mag_sample_bins = number_of_mag_sample_bins
        self.recurrence_model_distribution = recurrence_model_distribution

        # indexes to the event sets in this source zone
        self.event_set_indexes = None

    def set_event_set_indexes(self, event_indexes):
        """Add event integer indices list as an attribute.

        The integers are indexes into an event set.
        """

        self.event_set_indexes = event_indexes

    def set_atten_models_and_weights(self, atten_models, atten_model_weights):
        """Add attenuation model and weight attribute lists.

        atten_models   list of ground motion models
        atten_weights  list of ground motion model weights

        Also ensure that the sum of weights is 1.0.
        """

        self.atten_models = atten_models
        self.atten_model_weights = atten_model_weights

        weight_sum = sum(atten_model_weights)
        if weight_sum != 1.0:
            msg = 'Model weights should sum to 1.0, got %f' %  weight_sum
            raise Exception(msg)

        
class Source_Zone_Polygon(Source, polygon_object):
    def __init__(self,boundary,exclude,
                 min_magnitude,max_magnitude,
                 prob_min_mag_cutoff,
                 A_min,b,
                 number_of_mag_sample_bins,
                 recurrence_model_distribution='bounded_gutenberg_richter'):
        """
        boundary is a list of points that forms a polygon
        exclude is a list of polygons (so a list of a list of points)
        min_magnitude,max_magnitude,
        prob_min_mag_cutoff,A_min,b are floats
        
        #FIXME DSG-EQRM This class needs comments.
        What is prob_min_mag_cutoff?

        And where are it's methods? recurrence_functions might have 1.
        """
        polygon_object.__init__(self,boundary,exclude)
        Source.__init__(self,min_magnitude,max_magnitude,
                 prob_min_mag_cutoff,
                 A_min,b,
                 number_of_mag_sample_bins,
                 recurrence_model_distribution)

    def determine_event_set_indexes(self, event_set):
        contains_point=[self.contains_point((lat,lon), use_cach=False) \
                        for lat,lon in zip(
        event_set.rupture_centroid_lat,
        event_set.rupture_centroid_lon)]
        poly_ind=where(contains_point)[0]
        
        self.set_event_set_indexes(poly_ind)
        
    def set_event_set_indexes(self, event_indexes):
        """
        Input an array of integers which represent the events in a zone source.
        The intergers are indexes into an event set.
        """
        self.event_set_indexes = event_indexes


    def set_atten_models_and_weights(self, atten_models,
                                     atten_model_weights):
        self.atten_models = atten_models
        self.atten_model_weights = atten_model_weights


def event_control_from_xml(filename):
    """Routine to read in event control data from an XML file and return a
    list of Event_Group objects containing the raw data.

    filename  is the path to the event control XML file
    """

    class Event_Group(object):
        """Class to hold event group data as attributes."""

        def __init__(self, filename, event_type, fault_type, branch_list, scaling_dict):
            """Construct an object from event group data.

            filename      name of file we are reading (for debug)
            event_type    a string describing the event type
            fault_type    a string describing the fault type
            branch_list   a list of dictionaries {'model': '...',
                                                  'weight': '0.5'}
            scaling_dict  a dictionary {'scaling_rule': '...',
                                        'scaling_event_type': '...'}

            The constructed object will have the following attributes:
                .event_type          - event type string
                .fault_type          - fault type string
                .branch_models       - list of branch models
                .branch_weights      - list of branch wrights
                .scaling_rule        - event scaling rule string
                .scaling_event_type  - event scaling type string
            """

            self.event_type = event_type
            self.fault_type = fault_type

            self.branch_models = []
            self.branch_weights = []
            for b in branch_list:
                self.branch_models.append(b['model'])
                weight = float(b['weight'])
                self.branch_weights.append(weight)
            if sum(self.branch_weights) != 1.0:
                msg = ("XML file %s: weights for event group '%s' should sum "
                       "to 1.0, got %.1f"
                       % (filename, event_type, sum(self.branch_weights)))
                raise Exception(msg)

            self.scaling_rule = scaling_dict['scaling_rule']
            self.scaling_event_type = scaling_dict.get('scaling_event_type',
                                                       'unspecified')

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

        # get <scaling> attributes
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

def create_fault_sources(event_control_file, fsg_list):
    """Takes an FSG list and an event controfile and creates a list
    of Source objects.

    event_control_file  path to an <event_type_controlfile> XML file
    fsg_list            list of Fault_Source_Generator objects

    
    """

    return source_list

def source_model_from_xml(filename,prob_min_mag_cutoff,
                              number_of_mag_sample_bins):
    doc=Xml_Interface(filename=filename)
    if not doc['Source_Model'] == []:
        source_model = source_model_from_xml_row(
            doc, prob_min_mag_cutoff,
            number_of_mag_sample_bins)
    else:
        source_model = source_model_from_xml_horspool(
            doc, prob_min_mag_cutoff)
    return source_model


def source_model_from_xml_row(doc, prob_min_mag_cutoff,
                              number_of_mag_sample_bins):
    xml_source_model=doc['Source_Model'][0]
    magnitude_type=xml_source_model.attributes['magnitude_type']
    
    source_zone_polygons=[]
    xml_polygons = doc['polygon']
    for xml_polygon in xml_polygons:
        boundary = xml_polygon['boundary'][0].array
        recurrence = xml_polygon['recurrence'][0].attributes
        
        min_magnitude=float(recurrence['min_magnitude'])
        max_magnitude=float(recurrence['max_magnitude'])
        #prob_min_mag_cutoff=float(recurrence['prob_min_mag_cutoff'])
        A_min=float(recurrence['A_min'])
        b=float(recurrence['b'])
        
        area = float(xml_polygon.attributes['area'])
        exclude=[]
        for exclusion_zone in xml_polygon['exclude']:
            exclude.append(exclusion_zone.array)
        #print 'LAMBDAMIN 1 ',A_min
        source_zone_polygon = Source_Zone_Polygon(boundary,exclude,
                                                  min_magnitude,max_magnitude,
                                                  prob_min_mag_cutoff,
                                                  A_min,b,
                                                  number_of_mag_sample_bins)
        source_zone_polygons.append(source_zone_polygon)
        
    doc.unlink()
    return Source_Model(source_zone_polygons,magnitude_type)


def source_model_from_xml_horspool(doc, prob_min_mag_cutoff):
    xml_source_model=doc['source_model_zone'][0]
    magnitude_type=xml_source_model.attributes['magnitude_type']
    
    source_zone_polygons=[]
    xml_polygons = doc['zone']
    for xml_polygon in xml_polygons:
        geometry = xml_polygon['geometry'][0]
        boundary = geometry['boundary'][0].array
        recurrence = xml_polygon['recurrence_model'][0].attributes
        
        min_magnitude=float(recurrence['recurrence_min_mag'])
        max_magnitude=float(recurrence['recurrence_max_mag'])
        #prob_min_mag_cutoff=float(recurrence['prob_min_mag_cutoff'])
        A_min=float(recurrence['A_min'])
        b=float(recurrence['b'])
        
        area = float(xml_polygon.attributes['area'])

        event_gen = xml_polygon['recurrence_model'][0]['event_generation']
        number_of_mag_sample_bins = int(event_gen[0].attributes[
            'number_of_mag_sample_bins'])
        
        exclude=[]
        for exclusion_zone in xml_polygon['excludes']:
            exclude.append(exclusion_zone.array)
        #print 'LAMBDAMIN 1 ',A_min
        
        source_zone_polygon = Source_Zone_Polygon(
            boundary,
            exclude,
            min_magnitude,
            max_magnitude,
            prob_min_mag_cutoff,
            A_min,b,
            number_of_mag_sample_bins)
        source_zone_polygons.append(source_zone_polygon)
        
    doc.unlink()
    return Source_Model(source_zone_polygons,magnitude_type)
