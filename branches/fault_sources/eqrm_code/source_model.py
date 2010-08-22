"""
 Title: sites.py
 
  Author:  Peter Row, peter.row@ga.gov.au
           
  Description: Classes to represent earthquake source models
 
  Version: $Revision: 1644 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-04-27 16:59:30 +1000 (Tue, 27 Apr 2010) $
  
  Copyright 2007 by Geoscience Australia
"""
from scipy import zeros

from eqrm_code.recurrence_functions import calc_event_activity
from eqrm_code.polygon_class import polygon_object
from eqrm_code.xml_interface import Xml_Interface



class Source_Models(object):
    """
    Class to handle multiple Source Models.

    Code can currently only handle one Source Model
    """
    def __init__(self,prob_min_mag_cutoff, weight, *filenames):
        #print "prob_min_mag_cutoff", prob_min_mag_cutoff
        #print "weight", weight
        #print "*filenames", filenames
        self.weight = weight
        source_models=[]
        for fid_sourcepolys in filenames:
            source_model=source_model_from_xml(fid_sourcepolys.name,
                                               prob_min_mag_cutoff)
            source_models.append(source_model)
        self.source_models=source_models
        #print "self.source_models", self.source_models
        assert len(self.weight) == len(self.source_models)
        
    def __len__(self):
        return len(self.source_models)

    def __getitem__(self,key):
        return self.source_models[key]
    
    def calculate_recurrence(self, event_set, prob_number_of_mag_sample_bins):
        """
        Calculate the normalized recurrence of the event set.

        weight is the weight assigned to the respective models in
        event_set.source_models.

        This function is used by analysis
        """
        #print "event_set", event_set
        source_models = self.source_models

        new_event_set = calc_event_activity(event_set,
                                          source_models,
                                          prob_number_of_mag_sample_bins,
                                          self.weight)
        
        return new_event_set
    
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
    def __init__(self,source_zone_polygons,magnitude_type):
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


class Source_Zone_Polygon(polygon_object):
    def __init__(self,boundary,exclude,
                 min_magnitude,max_magnitude,
                 prob_min_mag_cutoff,
                 Lambda_Min,b):
        """
        boundary is a list of points that forms a polygon
        exclude is a list of polygons (so a list of a list of points)
        min_magnitude,max_magnitude,
        prob_min_mag_cutoff,Lambda_Min,b are floats
        
        #FIXME DSG-EQRM This class needs comments.
        What is prob_min_mag_cutoff?

        And where are it's methods? recurrence_functions might have 1.
        """
        polygon_object.__init__(self,boundary,exclude)
        self.min_magnitude=min_magnitude
        self.max_magnitude=max_magnitude
        self.prob_min_mag_cutoff=prob_min_mag_cutoff
        self.Lambda_Min=Lambda_Min
        self.b=b

    
def source_model_from_xml(filename,prob_min_mag_cutoff):
    doc=Xml_Interface(filename=filename)
    if not doc['Source_Model'] == []:
        source_model = source_model_from_xml_row(doc, prob_min_mag_cutoff)
    else:
        source_model = source_model_from_xml_horspool(doc, prob_min_mag_cutoff)
    return source_model


def source_model_from_xml_row(doc, prob_min_mag_cutoff):
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
        Lambda_Min=float(recurrence['Lambda_Min'])
        b=float(recurrence['b'])
        
        area = float(xml_polygon.attributes['area'])
        exclude=[]
        for exclusion_zone in xml_polygon['exclude']:
            exclude.append(exclusion_zone.array)
        #print 'LAMBDAMIN 1 ',Lambda_Min

        source_zone_polygon = Source_Zone_Polygon(boundary,exclude,
                                                  min_magnitude,max_magnitude,
                                                  prob_min_mag_cutoff,
                                                  Lambda_Min,b)
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
        Lambda_Min=float(recurrence['lambda_min'])
        b=float(recurrence['b'])
        
        area = float(xml_polygon.attributes['area'])
        exclude=[]
        for exclusion_zone in xml_polygon['excludes']:
            exclude.append(exclusion_zone.array)
        #print 'LAMBDAMIN 1 ',Lambda_Min

        source_zone_polygon = Source_Zone_Polygon(
            boundary,
            exclude,
            min_magnitude,
            max_magnitude,
            prob_min_mag_cutoff,
            Lambda_Min,b)
        source_zone_polygons.append(source_zone_polygon)
        
    doc.unlink()
    return Source_Model(source_zone_polygons,magnitude_type)
