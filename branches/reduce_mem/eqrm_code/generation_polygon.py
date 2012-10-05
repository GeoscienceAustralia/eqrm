"""
 Title: generation_polygon.py
  
  Author:  Peter Row, peter.row@ga.gov.au

  Description: Polgon class and polygons_from_xml function.

  Version: $Revision: 1669 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-05-12 09:34:07 +1000 (Wed, 12 May 2010) $
"""

import os
import math
from scipy import where, asarray
import exceptions

from eqrm_code.distributions import distribution_functions
from eqrm_code.polygon import populate_polygon, populate_geo_coord_polygon
from eqrm_code.polygon_class import polygon_object
from eqrm_code.xml_interface import Xml_Interface
from eqrm_code.conversions import azimuth_of_trace
from eqrm_code.recurrence_functions import calc_A_min_from_slip_rate
from source_model import get_recurrence_elements, RecurrenceModel

class FileError(exceptions.Exception): pass

##############################################################################

class Generation_Polygon(polygon_object):
    def __init__(self,
                 boundary,
                 depth_top_seismogenic_dist,
                 azimuth,
                 dip,
                 magnitude,
                 depth_bottom_seismogenic_dist,
                 polygon_name,
                 polygon_event_type,
                 number_of_events,
                 exclude):
        """
        boundary is an array of polygon points
        exclude is an array of polygon points
        All other variables are dictionaries describing distributions
        """
        if exclude is None:
            exclude = []        
        polygon_object.__init__(self,boundary,exclude)
        self.depth_top_seismogenic_dist=depth_top_seismogenic_dist
        self.azimuth=azimuth
        self.dip=dip
        self.magnitude=magnitude
        self.depth_bottom_seismogenic_dist = depth_bottom_seismogenic_dist
        self.polygon_name = polygon_name
        self.polygon_event_type = polygon_event_type
        self.number_of_events = number_of_events 

    def populate_depth_top_seismogenic(self,n):
        return self.populate_distribution(self.depth_top_seismogenic_dist,n)

    def populate_depth_bottom_seismogenic(self,n):
        return self.populate_distribution(self.depth_bottom_seismogenic_dist,n)
    
    def populate_azimuth(self,n):
        return self.populate_distribution(self.azimuth,n)

    def populate_dip(self,n):
        return self.populate_distribution(self.dip,n)

    def populate_magnitude(self,n):
        return self.populate_distribution(self.magnitude,n)
    
    def populate_distribution(self,distribution_args,n):
        """
        Use the distribution specifed in pdf_dict to
        calculate an n-vector with the correct distribution.
        """

        local_distribution_args = distribution_args.copy()
        #Copy the pdf_dict, so that the original doesn't get mutated
        distribution_name = local_distribution_args.pop('distribution')
        #get the name of the desired distribution (deleting it from the dict)

        # Just used for depth_bottom_seismogenic_dist
        if distribution_name == None:
            return None
        
        distribution_function = distribution_functions[distribution_name]
        #get the distribution function from a table of functions

        return distribution_function(n=n,**local_distribution_args)
        #Using **dictionary as an argument "unpacks" the
        #dictionary into keyword arguments
        #Similar to unpacking tuples (ie range(*(1,5,2)) is same as [1,3,5])
        #see python tutorial s4.7.4

    def populate(self,number_of_points,seed=None,use_cache=False):
        polygon = self._linestring[:-1]
        exclude = [exclude[:-1] for exclude in self._exclude]
        
        points = populate_geo_coord_polygon(polygon, number_of_points, seed, exclude)

        if use_cache:
            for point in points:
                point = tuple(point)
                self._precomputed_points[point]=True
                
        return points


class Fault_Source_Generator(object):
    """Class encapsulating fault source data from the new-format XML files."""

    # Dictionary containing param name to type mapping.
    # Anything not here is assumed to be type 'str'.
    name_type_map = {'dip': float,
                     'out_of_dip_theta': float,
                     'delta_theta': float,
                     'depth_top_seismogenic': float,
                     'depth_bottom_seismogenic': float,
                     'slab_width': float,
                     'lat': float,
                     'lon': float,
                     'recurrence_min_mag': float,
                     'recurrence_max_mag': float,
                     'slip_rate': float,
                     'A_min': float,
                     'b': float,
                     'generation_min_mag': float,
                     'number_of_events': int,
                    }

    def __init__(self, 
                 filename, 
                 fault_name, 
                 fault_event_type,
                 geometry_dict, 
                 recurrence_models,
                 event_generation_dict):
        """Initialise a Fault_Source_Generator instance.

        fault_name             fault name
        fault_event_type       fault event type
        geometry_dict          dictionary of all <geometry> data
        recurrence_models      a list of dictionaries with <recurrence_model> data
        event_generation_dict  dictionary of all <event_generation> data

        The *_dict parameters contain exactly what was in the XML and must be
        checked for required data.  We ignore extra parameters.

        The returned object will have the following data attributes:
            .name
            .dip_dist
            .out_of_dip_theta_dist
            .depth_top_seismogenic_dist
            .depth_bottom_seismogenic_dist
            .slab_width
            .trace_start_lat
            .trace_start_lon
            .trace_end_lat
            .trace_end_lon
            .azimuth_dist
            .recurrence_models (a list of source_model.RecurrenceModel objects)
            .generation_min_mag
            .number_of_events
            .magnitude_dist
        """

        # save generic fault information
        self.name = fault_name
        self.event_type = fault_event_type

        # look in geometry_dict parameter - we expect:
        #    {'dip': <value>,                       # required
        #     'out_of_dip_theta': <value>,          # required
        #     'delta_theta': <value>,               # required
        #     'depth_top_seismogenic': value',      # required
        #     'depth_bottom_seismogenic': value',   # required
        #     'slab_width': <value>,                # required
        #     'trace': {'start': {'lon': <value>,   # required
        #                         'lat': <value>}   # required
        #               'end': {'lon': <value>,     # required
        #                       'lat': <value>}}    # required
        #     }
        dip = self.n2t(geometry_dict, 'dip')
        self.dip_dist = {'distribution': 'constant', 'mean': dip}
        out_of_dip_theta = self.n2t(geometry_dict, 'out_of_dip_theta')
        delta_theta = self.n2t(geometry_dict, 'delta_theta')
        self.out_of_dip_theta_dist = {
            'distribution': 'uniform', 
            'minimum': out_of_dip_theta - delta_theta,
            'maximum': out_of_dip_theta + delta_theta}
        depth_top = self.n2t(geometry_dict, 'depth_top_seismogenic')
        self.depth_top_seismogenic_dist = {'distribution': 'constant', 
                                           'mean': depth_top}
        depth_bottom = self.n2t(geometry_dict, 'depth_bottom_seismogenic')
        self.depth_bottom_seismogenic_dist = {'distribution': 'constant',
                                              'mean': depth_bottom}
        self.slab_width = self.n2t(geometry_dict, 'slab_width')

        # now unpack the <trace> dictionary
        trace = geometry_dict['trace']
        trace_point = trace['start']
        self.trace_start_lat = self.n2t(trace_point, 'lat')
        self.trace_start_lon = self.n2t(trace_point, 'lon')
        trace_point = trace['end']
        self.trace_end_lat = self.n2t(trace_point, 'lat')
        self.trace_end_lon = self.n2t(trace_point, 'lon')

        # calculate azimuth (in degrees)
        azimuth = azimuth_of_trace(self.trace_start_lat, self.trace_start_lon,
                                   self.trace_end_lat, self.trace_end_lon)
        self.azimuth_dist = {'distribution': 'constant', 'mean': azimuth}

        # recurrence_models -> a list of recurrence_model_dicts
        # we expect:
        #    {'distribution': <value>,
        #     'recurrence_min_mag': <value>,
        #     'recurrence_max_mag': <value>,
        #     'slip_rate': <value>,                        # optional
        #     'A_min': <value>,                            # optional
        #     'b': <value>,
        #     'event_generation': {'generation_min_mag': <value>,]
        #                          'number_of_events': <value>}}
        #     }
        #
        # Exactly one of 'slip_rate' and 'A_min' must exist.
        # All other parameters are required.
        self.recurrence_models = []
        for recurrence_model in recurrence_models:
            recurrence_model_dict = recurrence_model.attributes
            recurrence_min_mag =    self.n2t(recurrence_model_dict,
                                             'recurrence_min_mag')
            recurrence_max_mag =    self.n2t(recurrence_model_dict,
                                             'recurrence_max_mag')
            b =                     self.n2t(recurrence_model_dict, 
                                             'b')
            distribution =          self.n2t(recurrence_model_dict, 
                                             'distribution')
                
            # only save A_min, convert from slip_rate if required
            slip_rate =             self.n2t(recurrence_model_dict, 
                                             'slip_rate')
            A_min =                 self.n2t(recurrence_model_dict, 
                                             'A_min')
            
            if ((slip_rate and A_min) or (not slip_rate and not A_min)):
                msg = ("Badly formed XML in file %s: expected exactly one of "
                       "'slip_rate' and 'A_min' attributes in fault '%s'"
                       % (filename, fault_name))
                raise Exception(msg)
            
            if slip_rate:
                A_min = calc_A_min_from_slip_rate(b,
                                                  recurrence_min_mag,
                                                  recurrence_max_mag,
                                                  slip_rate,
                                                  distribution,
                                                  self.trace_start_lat,
                                                  self.trace_start_lon,
                                                  self.trace_end_lat,
                                                  self.trace_end_lon,
                                                  depth_top, 
                                                  depth_bottom,
                                                  dip)
            
            weight = self.n2t(recurrence_model_dict, 'weight')
            # Set to 100% if not there
            if weight is None:
                weight = 1.0
                
            self.recurrence_models.append(RecurrenceModel(recurrence_min_mag,
                                                          recurrence_max_mag,
                                                          A_min,
                                                          b,
                                                          distribution,
                                                          weight))
            
        self.generation_min_mag = self.n2t(event_generation_dict, 
                                           'generation_min_mag')
        
        self.number_of_events = self.n2t(event_generation_dict, 
                                         'number_of_events')
        
        minmag = min(rm.min_magnitude for rm in self.recurrence_models)
        maxmag = max(rm.max_magnitude for rm in self.recurrence_models)
        self.magnitude_dist = {'distribution': 'uniform',
                               'minimum': max(minmag, self.generation_min_mag),
                               'maximum': maxmag}
        

    def n2t(self, d, name):
        """Helper function to convert a named parameter to a typed value.

        d     data dictionary value with 'name' defined
        name  name of value in data dictionary 'd'

        self.name_type_map is the class global type mapping dictionary.

        If 'name' is not found in the data dictionary, assume a None value.
        If 'name' not found in type dictionary, assume 'str' type.
        """

        try:
            val = d[name]	# can only get KeyError exception here
            t = self.name_type_map.get(name, str)
            result = t(val)
        except KeyError:
            result = None

        return result

    def populate_depth_top_seismogenic(self,n):
        return self.populate_distribution(self.depth_top_seismogenic_dist,n)

    def populate_depth_bottom_seismogenic(self,n):
        return self.populate_distribution(self.depth_bottom_seismogenic_dist,n)
    
    def populate_azimuth(self,n):
        return self.populate_distribution(self.azimuth_dist,n)

    def populate_dip(self,n):
        return self.populate_distribution(self.dip_dist,n)

    def populate_out_of_dip_theta(self,n,dip):
        
        out_of_dip = asarray(self.populate_distribution(
                                            self.out_of_dip_theta_dist,n))
        
        
        (errorIndexes,) = where((out_of_dip > (175-dip)) &
                                     (out_of_dip < (185-dip)))
        
        if len(errorIndexes) > 0:
            for i in errorIndexes:
                blnBadNum =True
                count=0
                while blnBadNum:
                    newNum=self.populate_distribution(
                                                self.out_of_dip_theta_dist,1)
                    if ((newNum[0] <= (175-dip)) | (newNum[0] >= (185-dip))):
                        blnBadNum=False                        
                    count = count +1
                    if count>1000:
                        msg = "Bad out of dip theta range in fault \
                                     source file"
                        raise IOError(msg)
                out_of_dip[i]=newNum[0]
        (errorIndexes,) = where((out_of_dip > (175-dip)) &
                                     (out_of_dip < (185-dip)))
        
        if len(errorIndexes) > 0:
            msg = "Bad out of dip theta range in fault \
                                     source file"
            raise IOError(msg)
            
        return out_of_dip
    
    def populate_magnitude(self,n):
        return self.populate_distribution(self.magnitude_dist,n)
    
    def populate_range(self,n):
        dist= {'distribution': 'uniform', 'minimum': 0, 'maximum': 1}
        return self.populate_distribution(dist,n)
    
    def populate_distribution(self,distribution_args,n):
        """
        Use the distribution specifed in pdf_dict to
        calculate an n-vector with the correct distribution.
        """

        local_distribution_args = distribution_args.copy()
        #Copy the pdf_dict, so that the original doesn't get mutated
        distribution_name = local_distribution_args.pop('distribution')
        #get the name of the desired distribution (deleting it from the dict)

        # Just used for depth_bottom_seismogenic_dist
        if distribution_name == None:
            return None
        
        distribution_function = distribution_functions[distribution_name]
        #get the distribution function from a table of functions

        return distribution_function(n=n,**local_distribution_args)
        #Using **dictionary as an argument "unpacks" the
        #dictionary into keyword arguments
        #Similar to unpacking tuples (ie range(*(1,5,2)) is same as [1,3,5])
        #see python tutorial s4.7.4


def polygons_from_xml(filename):
    doc=Xml_Interface(filename=filename)
    if not doc['Source_Model'] == []:
        raise Exception('zone source file format incorrect.')
    else:
        generation_polygons, magnitude_type = polygons_from_xml_horspool(
            doc)
    # Hacky checking code
#     from eqrm_code.eqrm_filesystem import scenario_input_bridges_path
    
#     handle = open(os.path.join(scenario_input_bridges_path,
#                                'newc_source_polygon.xml'))
#     print "handle", handle
#     doc=Xml_Interface(filename=handle)
    
#     generation_polygons_r,magnitude_type_h = polygons_from_xml_row(
#         doc, 
#         azi,
#         dazi,
#         fault_dip,
#         fault_width,
#         override_xml)
#     assert magnitude_type == magnitude_type_h
    
#     for i in range(len(generation_polygons_r)):
#         assert generation_polygons[i]._linestring == generation_polygons_r[i]._linestring 

#         assert generation_polygons[i].depth_top_seismogenic_dist == generation_polygons_r[i].depth_top_seismogenic_dist
#         assert generation_polygons[i].azimuth == generation_polygons_r[i].azimuth
#         #print "generation_polygons[i].dip", generation_polygons[i].dip
#         #print "generation_polygons_r[i].dip", generation_polygons_r[i].dip
#         #generation_polygons[i].dip = generation_polygons_r[i].dip
#         #assert generation_polygons[i].dip == generation_polygons_r[i].dip
#         #print "i", i
#         #print "generation_polygons[i].magnitude",generation_polygons[i].magnitude 
#         #print "generation_polygons_r[i].magnitude", generation_polygons_r[i].magnitude
#         assert generation_polygons[i].magnitude == generation_polygons_r[i].magnitude

    return generation_polygons, magnitude_type


def xml_fault_generators(filename):
    """Read Horspool style XML.

    attributes:
      filename -  the path to the XML file to read

    Returns:
     a tuple (gen_objects, mag_type) where 'gen_objects' is a list of
    Fault_Source_Generator objects and 'mag_type' is the magnitude type string.
    """
   
    # get XML doc and top-level tag object 
    try:
        doc = Xml_Interface(filename=filename)
    except Exception, e:
        msg = 'Malformed XML in file %s: %s' % (filename, str(e))
        raise Exception(msg)

    top_tag = doc['source_model_fault'][0]
    if len(doc['source_model_fault']) == 0:
        msg = ("XML file %s: expected 'source_model_fault' tag, got '%s'"
               % (filename, doc.xml_node.documentElement.nodeName))
        raise Exception(msg)

    # get magnitude type attribute try:
    try:
        magnitude_type = top_tag.attributes['magnitude_type']
    except KeyError:
        magnitude_type = 'Mw'
    
    if  magnitude_type != 'Mw':
        msg = "XML Error: magnitude_type must be 'Mw'."
        raise FileError(msg)
        

    # check that we have one or more 'fault' tags
    faults = doc['fault']
    if len(faults) == 0:
        msg = "XML file %s: expected one or more 'fault' tags" % filename
        raise Exception(msg)
    
    # now cycle through 'fault' tags
    fsg_list = []
    for i, fault in enumerate(faults):
        # get <fault> attributes
        try:
            fault_name = fault.attributes['name']
        except KeyError:
            fault_name = 'fault_' + str(i)
        fault_event_type = fault.attributes['event_type']

        # now get <geometry> attributes/children
        geometry = fault['geometry']
        if len(geometry) != 1:
            msg = ("Badly formed XML in file %s: Expected exactly one "
                   "'geometry' tag in fault named '%s'"
                   % (filename, fault_name))
            raise Exception(msg)
        geometry = geometry[0]

        geometry_dict = geometry.attributes

        # get <trace> data from <geometry> tag
        trace = geometry['trace']
        if len(trace) != 1:
            msg = ("Badly formed XML in file %s: Expected exactly one 'trace' "
                   "tag in fault named '%s'"
                   % (filename, fault_name))
            raise Exception(msg)
        trace = trace[0]

        start = trace['start'][0]
        start_point = start.attributes
        end = trace['end'][0]
        end_point = end.attributes
        trace_dict = {'start': start_point, 'end': end_point}

        geometry_dict['trace'] = trace_dict

        # get <recurrence_model> attributes/children
        recurrence_models,  event_generation = get_recurrence_elements(fault)
        
        event_generation_dict = event_generation.attributes

        fault_obj = Fault_Source_Generator(filename, 
                                           fault_name,
                                           fault_event_type,
                                           geometry_dict,
                                           recurrence_models,
                                           event_generation_dict)
        fsg_list.append(fault_obj)

    return (fsg_list, magnitude_type)


def polygons_from_xml_horspool(doc):
    """
    
    Returns a list of Generation_Polygon and magnitude_type

    Assumes only one source model
    """
    xml_Source_Model = doc['source_model_zone'][0]
    try:
        magnitude_type = xml_Source_Model.attributes['magnitude_type']
    except KeyError:
        magnitude_type = 'Mw'
    
    if  magnitude_type != 'Mw':
        msg = "Badly formed XML: magnitude_type must be 'Mw'."
        raise FileError(msg)
        
    generation_polygons=[]
    xml_polygons = doc['zone']
    for i, xml_polygon in enumerate(xml_polygons):
        try:
            polygon_name = xml_polygon.attributes['name']
        except KeyError:
            polygon_name = 'zone_' + str(i)
        polygon_event_type = xml_polygon.attributes['event_type'] 
        geometry = xml_polygon['geometry'][0]
        geometry_atts = xml_polygon['geometry'][0].attributes 
        boundary = geometry['boundary'][0].array
        boundary.shape = -1, 2  # Had to add for a test.
        dip = float(geometry_atts['dip'])
        delta_dip = float(geometry_atts['delta_dip'])
        azi = float(geometry_atts['azimuth'])
        dazi = float(geometry_atts['delta_azimuth'])

        depth_top = float(geometry_atts['depth_top_seismogenic'])
        depth_bottom = float(geometry_atts['depth_bottom_seismogenic'])
        depth_top_seismogenic_dist = {'distribution':'constant',
                                      'mean':depth_top}
        depth_bottom_seismogenic_dist = {'distribution':'constant',
                                      'mean':depth_bottom}
        
        dip = {'distribution':'uniform',
               'minimum':dip - delta_dip,
               'maximum': dip + delta_dip}

        recurrence_models,  event_gen = get_recurrence_elements(xml_polygon)
        event_gen_atts = event_gen.attributes
        number_of_events = int(event_gen_atts['number_of_events'])
        minmag = min(float(rm.attributes['recurrence_min_mag']) for rm in recurrence_models)
        maxmag = max(float(rm.attributes['recurrence_max_mag']) for rm in recurrence_models)
        magnitude = {'distribution':'uniform',
                     'minimum': max(minmag,
                                    float(event_gen_atts['generation_min_mag'])),
                     'maximum': maxmag}
        # magnitude = None This fails, so this is used.             
        azimuth = {'distribution':'uniform',
                   'minimum':azi - dazi,
                   'maximum':azi + dazi}
        exclude = []
        for exclusion_zone in xml_polygon['excludes']:
            exclude.append(exclusion_zone.array)
        generation_polygon = Generation_Polygon(
            boundary,
            depth_top_seismogenic_dist,
            azimuth,
            dip,
            magnitude,
            depth_bottom_seismogenic_dist,
            polygon_name,
            polygon_event_type,
            number_of_events,
            exclude)
        generation_polygons.append(generation_polygon)

    doc.unlink()

    return generation_polygons,magnitude_type
