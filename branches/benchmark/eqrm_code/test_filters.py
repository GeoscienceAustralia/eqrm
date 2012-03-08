# -*- coding:utf-8 -*-
"""
Created on 12/01/2012

@author: Ben Cooper, ben.cooper@ga.gov.au
"""

import os
import tempfile
import unittest

from scipy import allclose, zeros, ones

from eqrm_code.filters import *

from eqrm_code.event_set import Event_Set
from eqrm_code.sites import Sites
from eqrm_code.source_model import Source_Model
from eqrm_code.test_event_set import DummyEventSet
    
from eqrm_code import perf
    
def create_source_model():
    """
    Create dummy source model.
    This needs to match the event_set created by create_event_set()
    """
    # create_event_set returns an event_set of size 2
    source_model = Source_Model.create_scenario_source_model(2)
    return source_model
    
def create_event_set():
    """
    Create dummy event set.
    Uses the same technique from test_event_set 
    (Test_Event_Set.test_scenario_event_II)
    """
    
    eqrm_flags = DummyEventSet()
    eqrm_flags.scenario_latitude = [-30., -32.]
    eqrm_flags.scenario_longitude = [150., -151.]
    eqrm_flags.scenario_azimuth = [340, 330]
    eqrm_flags.dip = [37, 30]
    eqrm_flags.scenario_magnitude = [8, 7.5]
    eqrm_flags.max_width = [15, 7]
    eqrm_flags.scenario_depth = [11.5, 11.0]
    eqrm_flags.scenario_number_of_events = 1
        
    event_set = Event_Set.create_scenario_events(
            rupture_centroid_lat=[eqrm_flags.scenario_latitude],
            rupture_centroid_lon=[eqrm_flags.scenario_longitude],
            azimuth=[eqrm_flags.scenario_azimuth],
            dip=[eqrm_flags.dip],
            Mw=[eqrm_flags.scenario_magnitude],
            fault_width=eqrm_flags.max_width,
            depth=[eqrm_flags.scenario_depth],
            scenario_number_of_events=eqrm_flags.scenario_number_of_events)
    
    return event_set


def create_site():
    """
    Create dummy site.
    Uses the same technique from test_sites
    (Test_Sites.test_read_from_file
    """
    # create dummy CSV file - this is bridges data, but sites should handle anything
    lat = [-35.352085]
    lon = [149.236994]
    clsf = ['HWB17']
    cat = ['BRIDGE']
    skew = [0]
    span = [2]
    cls = ['E']
    attribute_keys = ['BID', 'STRUCTURE_CLASSIFICATION']

    dummy_csv_data = ['BID,LONGITUDE,LATITUDE,STRUCTURE_CLASSIFICATION,'
                      'STRUCTURE_CATEGORY,SKEW,SPAN,SITE_CLASS',
                      '2,%.6f,%.6f,%s,%s,%s,%s,%s'
                          % (lon[0], lat[0], clsf[0], cat[0], skew[0], span[0], cls[0])]

    (handle, filename) = tempfile.mkstemp('.csv', 'test_sites_')
    os.close(handle)

    f = open(filename, 'wb')
    f.write('\n'.join(dummy_csv_data))
    f.close()

    # now read file - pass attribute_conversion as **kwargs data
    sites = Sites.from_csv(filename, BID=int, STRUCTURE_CLASSIFICATION=str)
    
    return sites
    
    
class Test_Filters(unittest.TestCase):
    
    def setUp(self):
        # Set up test sites object
        self.sites = create_site()
        #print "sites", self.sites
        #print "len(sites)=", len(self.sites)
        
        # Set up test event_set object
        self.event_set = create_event_set()
        #print "event_set", self.event_set
        #print "len(event_set)=", len(self.event_set)
        
        # Set up test source_model object
        self.source_model = create_source_model()
        
        # Set up dummy SA values - can be anything as long as we understand
        # what's being tested
        # SA dim (spawn, GMmodel, rec_model, site, event, period)
        # We only care about the affect to the sites and event_set dimensions
        # so everything else is just set to 1
        self.SA_zeros = zeros((1,
                               1,
                               1,
                               len(self.sites),
                               2, # len(event_set) returning 1?
                               1),
                              dtype=float)
        self.SA_ones = ones((1,
                             1,
                             1,
                             len(self.sites),
                             2, # len(event_set) returning 1?
                             1),
                            dtype=float)
        
        # so that apply_threshold_distance returns a soil_SA result
        self.use_amplification = True 
        
        
    def tearDown(self):
        # Run some analysis tearDown?
        pass
    
    @perf.benchmark
    def test_apply_threshold_distance_all(self):
        """
        Test apply_threshold_distance function for atten_threshold_distance 
        scenario where apply_threshold_distance sets the SA figures to zero
        """
        # Use the ones array for the initial SA figures
        bedrock_SA = self.SA_ones.copy()
        soil_SA = self.SA_ones.copy()
        
        # Set a low threshold distance
        # distances [[   337.69538742  27105.63126916]]
        atten_threshold_distance = 300
        
        # Run the threshold distance function
        apply_threshold_distance(bedrock_SA,
                                 soil_SA,
                                 self.sites,
                                 atten_threshold_distance,
                                 self.use_amplification,
                                 self.event_set)
        
        # This should produce all zeros
        assert allclose(bedrock_SA, self.SA_zeros)
        assert allclose(soil_SA, self.SA_zeros)
    
    @perf.benchmark
    def test_apply_threshold_distance_partial(self):
        """
        Test apply_threshold_distance function for atten_threshold_distance 
        scenario where apply_threshold_distance sets some SA figures to zero
        """
        # Use the ones array for the initial SA figures
        bedrock_SA = self.SA_ones.copy()
        soil_SA = self.SA_ones.copy()
        
        # Set a normal threshold distance
        #                event 0       event 1
        # distances [[   337.69538742  27105.63126916]]
        atten_threshold_distance = 400
        
        # Set up SA arrays that match the expected outcome, noting the distances
        # in the comment above
        site_inds = [0]
        event_inds = [1]
        bedrock_SA_expected = bedrock_SA.copy()
        bedrock_SA_expected[...,site_inds,event_inds,:] = 0
        soil_SA_expected = soil_SA.copy()
        soil_SA_expected[...,site_inds,event_inds,:] = 0
        
        # Run the threshold distance function
        apply_threshold_distance(bedrock_SA,
                                 soil_SA,
                                 self.sites,
                                 atten_threshold_distance,
                                 self.use_amplification,
                                 self.event_set)
        
        assert allclose(bedrock_SA, bedrock_SA_expected)
        assert allclose(soil_SA, soil_SA_expected)
    
    @perf.benchmark
    def test_apply_threshold_distance_none(self):
        """
        Test apply_threshold_distance function for atten_threshold_distance 
        scenario where apply_threshold_distance sets no SA figures to zero
        """
        # Use the ones array for the initial SA figures
        bedrock_SA = self.SA_ones.copy()
        soil_SA = self.SA_ones.copy()
        
        # Set a high threshold distance
        # distances [[   337.69538742  27105.63126916]]
        atten_threshold_distance = 30000
        
        # Run the threshold distance function
        apply_threshold_distance(bedrock_SA,
                                 soil_SA,
                                 self.sites,
                                 atten_threshold_distance,
                                 self.use_amplification,
                                 self.event_set)
        
        # This should produce all ones
        assert allclose(bedrock_SA, self.SA_ones)
        assert allclose(soil_SA, self.SA_ones)
        
    @perf.benchmark
    def test_source_model_threshold_distance_subset_all(self):
        """
        Test source_model_threshold_distance_subset function for 
        atten_threshold_distance scenario where the source_model_subset returned
        contains no events
        """
        # Set a low threshold distance
        #                event 0       event 1
        # distances [[   337.69538742  27105.63126916]]
        atten_threshold_distance = 300
        
        # Expected result - evcnt_set_indexes an empty array
        source_model_expected = create_source_model()
        for source in source_model_expected:
            source.set_event_set_indexes([])
        
        source_model_subset = source_model_threshold_distance_subset(self.sites,
                                                        self.event_set,
                                                        self.source_model,
                                                        atten_threshold_distance)
        
        for i, source in enumerate(source_model_subset):
            self.failUnless(allclose(source.event_set_indexes,
                                     source_model_expected[i].event_set_indexes))
    
    @perf.benchmark
    def test_source_model_threshold_distance_subset_partial(self):
        """
        Test source_model_threshold_distance_subset function for 
        atten_threshold_distance scenario where the source_model_subset returned
        contains a reduced set of events
        """
        # Set a normal threshold distance
        #                event 0       event 1
        # distances [[   337.69538742  27105.63126916]]
        atten_threshold_distance = 400
        
        # Expected result - event_set_indexes a subset according to distances in 
        # the above comment
        source_model_expected = create_source_model()
        for source in source_model_expected:
            event_inds = [0]
            source.set_event_set_indexes(event_inds)
        
        source_model_subset = source_model_threshold_distance_subset(self.sites,
                                                        self.event_set,
                                                        self.source_model,
                                                        atten_threshold_distance)
        
        for i, source in enumerate(source_model_subset):
            self.failUnless(allclose(source.event_set_indexes,
                                     source_model_expected[i].event_set_indexes))
    
    @perf.benchmark
    def test_source_model_threshold_distance_subset_none(self):
        """
        Test source_model_threshold_distance_subset function for 
        atten_threshold_distance scenario where the source_model_subset returned
        contains the original set of events
        """
        # Set a high threshold distance
        #                event 0       event 1
        # distances [[   337.69538742  27105.63126916]]
        atten_threshold_distance = 30000
        
        # Expected result - an unchanged source model
        source_model_expected = create_source_model()
        
        source_model_subset = source_model_threshold_distance_subset(self.sites,
                                                        self.event_set,
                                                        self.source_model,
                                                        atten_threshold_distance)
        
        for i, source in enumerate(source_model_subset):
            self.failUnless(allclose(source.event_set_indexes,
                                     source_model_expected[i].event_set_indexes))

#-------------------------------------------------------------    
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Filters,'test')
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)

    