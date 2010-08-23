"""
 Title: generation_polygon.py
  
  Author:  Peter Row, peter.row@ga.gov.au

  Description: Polgon class and polygons_from_xml function.

  Version: $Revision: 1669 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-05-12 09:34:07 +1000 (Wed, 12 May 2010) $
"""

from eqrm_code.distributions import distribution_functions
from eqrm_code.polygon import populate_polygon
from eqrm_code.polygon_class import polygon_object
from eqrm_code.xml_interface import Xml_Interface

##############################################################################
class Generation_Polygon(polygon_object):
    def __init__(self,
                 boundary,
                 fault_depth_dist,
                 fault_width_dist,
                 azimuth,
                 dip,
                 magnitude,
                 exclude=None):
        if exclude is None:
            exclude = []        
        polygon_object.__init__(self,boundary,exclude)
        self.fault_width_dist=fault_width_dist
        self.fault_depth_dist=fault_depth_dist
        self.azimuth=azimuth
        self.dip=dip
        self.magnitude=magnitude

    def populate_fault_width(self,n):
        return self.populate_distribution(self.fault_width_dist,n)
    
    def populate_fault_depth(self,n):
        return self.populate_distribution(self.fault_depth_dist,n)

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

        distribution_function = distribution_functions[distribution_name]
        #get the distribution function from a table of functions

        return distribution_function(n=n,**local_distribution_args)
        #Using **dictionary as an argument "unpacks" the
        #dictionary into keyword arguments
        #Similar to unpacking tuples (ie range(*(1,5,2)) is same as [1,3,5])
        #see python tutorial s4.7.4

    def populate(self,number_of_points,seed=None):
        polygon = self._linestring[:-1]
        exclude = [exclude[:-1] for exclude in self._exclude]
        points=populate_polygon(polygon,number_of_points,seed,exclude)

        for point in points:
            point = tuple(point)
            self._precomputed_points[point]=True
        return points
    
def polygons_from_xml(filename,
                      azi=None,
                      dazi=None,
                      fault_dip=None,
                      fault_width=None,
                      prob_min_mag_cutoff=None,
                      override_xml=False):
    
    doc=Xml_Interface(filename=filename)
    if not doc['Source_Model'] == []:
        generation_polygons, magnitude_type = polygons_from_xml_row(
            doc, 
            azi,
            dazi,
            fault_dip,
            fault_width,
            prob_min_mag_cutoff,
            override_xml)
    else:
        generation_polygons, magnitude_type = polygons_from_xml_horspool(
            doc, 
            azi,
            dazi,
            fault_dip,
            fault_width,
            prob_min_mag_cutoff,
            override_xml)
    # Hacky checking code    
#     handle = open('.\implementation_tests\input/newc_source_polygon.xmlq')
#     #print "handle", handle
#     doc=Xml_Interface(filename=handle)
    
#     generation_polygons_h,magnitude_type_h = polygons_from_xml_horspool(
#         doc, 
#         azi,
#         dazi,
#         fault_dip,
#         fault_width,
#         prob_min_mag_cutoff,
#         override_xml)
#     assert magnitude_type == magnitude_type_h
    
#     for i in range(len(generation_polygons_h)):
#         assert generation_polygons[i]._linestring == generation_polygons_h[i]._linestring 

#         assert generation_polygons[i].fault_width_dist == generation_polygons_h[i].fault_width_dist
#         assert generation_polygons[i].fault_depth_dist == generation_polygons_h[i].fault_depth_dist
#         assert generation_polygons[i].azimuth == generation_polygons_h[i].azimuth
#         assert generation_polygons[i].dip == generation_polygons_h[i].dip
#         print "i", i
#         print "generation_polygons[i].magnitude",generation_polygons[i].magnitude 
#         print "generation_polygons_h[i].magnitude", generation_polygons_h[i].magnitude
#         assert generation_polygons[i].magnitude == generation_polygons_h[i].magnitude

    return generation_polygons, magnitude_type

def polygons_from_xml_row(doc,
                          azi=None,
                          dazi=None,
                          fault_dip=None,
                          fault_width=None,
                          prob_min_mag_cutoff=None,
                          override_xml=False):
    """
    
    azi, dazi and fault_dip are lists of length len(xml_polygons)

    Is the override_xml used so a list of events with no location can
    be turned into an event set? 

    Why are so many parameters passed in?
    override_xml:  Analysis uses True
    Returns a list of Generation_Polygon and magnitude_type

    Assumes only one source model
    """
    #FIXME implement;
    # azi=, dazi, fault_dip = can be a single value or a vector with
    # differnet elements
    #          for each source zone 
    generation_polygons=[]
    xml_polygons = doc['polygon']
    for i in range(len(xml_polygons)):
        xml_polygon=xml_polygons[i]
        boundary = xml_polygon['boundary'][0].array
        boundary.shape = -1, 2  # Had to add for a test. 
        try: fault_width_dist = xml_polygon['fault_width'][0].attributes
        except: pass
        try: fault_depth_dist = xml_polygon['fault_depth'][0].attributes
        except: pass
        try: dip = xml_polygon['dip'][0].attributes
        except: pass
        try: magnitude = xml_polygon['magnitude'][0].attributes   
        except: pass        
        try: azimuth = xml_polygon['azimuth'][0].attributes
        except: pass

        if override_xml:
            fault_depth=xml_polygon['recurrence'][0].attributes['depth']
            fault_depth_dist = {'distribution':'constant','mean':fault_depth}
            fault_width_dist = {'distribution':'constant','mean':fault_width}
            dip = {'distribution':'constant','mean':float(fault_dip[i])}
            
            min_magnitude=xml_polygon['recurrence'][0].attributes[
                'min_magnitude']
            min_mag=prob_min_mag_cutoff
            minmag=max(float(min_magnitude),
                       float(min_mag))
            maxmag=xml_polygon['recurrence'][0].attributes['max_magnitude']
            magnitude = {'distribution':'uniform',
                         'minimum':minmag,
                         'maximum': maxmag}
            azimuth = {'distribution':'uniform',
                       'minimum':float(azi[i])-float(dazi[i]),
                       'maximum': float(azi[i])+float(dazi[i])}
           
            
        exclude=[]
        for exclusion_zone in xml_polygon['exclude']:
            exclude.append(exclusion_zone.array)
        generation_polygon = Generation_Polygon(boundary,
                                                fault_depth_dist,
                                                fault_width_dist,
                                                azimuth,dip,
                                                magnitude,exclude)
        generation_polygons.append(generation_polygon)

    xml_Source_Model =doc['Source_Model'][0]
    magnitude_type=xml_Source_Model.attributes['magnitude_type']
    doc.unlink()

    return generation_polygons,magnitude_type

def polygons_from_xml_horspool(doc,
                               azi=None,
                               dazi=None,
                               fault_dip=None,
                               fault_width=None,
                               prob_min_mag_cutoff=None,
                               override_xml=False):
    """
    
    azi, dazi and fault_dip are lists of length len(xml_polygons)

    Is the override_xml used so a list of events with no location can
    be turned into an event set? 

    Why are so many parameters passed in?
    override_xml:  Analysis uses True
    Returns a list of Generation_Polygon and magnitude_type

    Assumes only one source model
    """
    
    xml_Source_Model =doc['source_model_zone'][0]
    magnitude_type=xml_Source_Model.attributes['magnitude_type']
    
    generation_polygons=[]
    xml_polygons = doc['zone']
    for i in range(len(xml_polygons)):
        xml_polygon=xml_polygons[i]
        geometry = xml_polygon['geometry'][0]
        geometry_atts = xml_polygon['geometry'][0].attributes 
        boundary = geometry['boundary'][0].array
        boundary.shape = -1, 2  # Had to add for a test. 
        try: dip = float(geometry_atts['dip'])
        except: pass     
        try: dip = float(geometry_atts['delta_dip'])
        except: pass

        if override_xml:
            #fault_depth = float(geometry_atts['depth_top_seismogenic'])
            fault_depth = geometry_atts['depth_top_seismogenic']
            fault_depth_dist = {'distribution':'constant','mean':fault_depth}
            fault_width_dist = {'distribution':'constant','mean':fault_width}
            dip = {'distribution':'constant','mean':float(fault_dip[i])}
            recurrence = xml_polygon['recurrence_model'][0]
            event_gen_atts = recurrence['event_generation'][0].attributes
            min_magnitude = event_gen_atts['generation_min_mag']
            recurrence_atts = recurrence.attributes
            min_magnitude = recurrence_atts['recurrence_min_mag']
            min_mag = prob_min_mag_cutoff
            minmag = max(float(min_magnitude),
                       float(min_mag))
            #maxmag = float(recurrence_atts['recurrence_max_mag'])
            maxmag = recurrence_atts['recurrence_max_mag']
            magnitude = {'distribution':'uniform',
                         'minimum':minmag,
                         'maximum': maxmag}
            azimuth = {'distribution':'uniform',
                       'minimum':float(azi[i])-float(dazi[i]),
                       'maximum': float(azi[i])+float(dazi[i])}
           
            
        exclude=[]
        for exclusion_zone in xml_polygon['excludes']:
            exclude.append(exclusion_zone.array)
        generation_polygon = Generation_Polygon(
            boundary,
            fault_depth_dist,
            fault_width_dist,
            azimuth,dip,
            magnitude,exclude)
        generation_polygons.append(generation_polygon)

    doc.unlink()

    return generation_polygons,magnitude_type
