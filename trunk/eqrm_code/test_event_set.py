
import os
import sys
from random import uniform,seed
from time import time
import unittest
from os import sep
import types
import tempfile

from scipy import array, allclose, asarray, arange, sum

from xml_interface import Xml_Interface
from source_model import source_model_from_xml, Source_Model
import conversions

from eqrm_code.event_set import * #Event_Set, Pseudo_Event_Set


class Dummy:
    def __init__(self):
        pass
    def set_event_set_indexes(self,foo):
        pass
    
def event_from_csv_long():
    # Values tightly coupled with event_from_csv_short
    trace_start_lat = -38.15
    trace_start_lon = 146.5
   
    azimuth = 217
    dip = array([60.0])
    weight = 18
    event_activity = 0
    recurrence = weight*event_activity
    
    Mw = 6.9
    lat0 = -38.31
    lon0 = 146.3
    
    depth = array([6.5]) #FIXME it should not have to be an array
    rx = 25.3
    ry = 3.8
    
    length = 50.6
    width = 15

    event_set=Event_Set.create(depth=depth, rupture_centroid_lat=lat0,
                               rupture_centroid_lon=lon0, azimuth=azimuth,
                               dip=dip, ML=None, Mw=Mw, fault_width=15.0)

    event_set.trace_start_x = -rx
    event_set.trace_start_y = -ry
    event_set.trace_start_lat = trace_start_lat
    event_set.trace_start_lon = trace_start_lon
    event_set.recurrence = recurrence
    event_set.length = length
    event_set.width = width

    return event_set

def event_from_csv_short():
    # Values tightly coupled with event_from_csv_long
    azimuth = 217
    dip = array([60.])
    weight = 18
    event_activity = 0
    recurrence = weight*event_activity
    
    Mw = 6.9
    lat0 = -38.31
    lon0 = 146.3
    
    depth = array([6.5])
    
    event_set = Event_Set.create(depth=depth, rupture_centroid_lat=lat0,
                                 rupture_centroid_lon=lon0, fault_width=15.0,
                                 azimuth=azimuth, dip=dip, ML=None, Mw=Mw)
    event_set.recurrence = recurrence

    return event_set

def csv_to_array(csv_file):
    csv_file = open(csv_file)
    csv_array = array([[float(s) for s in line.split(',')]
                      for line in csv_file])
    csv_file.close()

    return csv_array

class Test_Event_Set(unittest.TestCase):

    def test_event_set_conformance(self):
        event_csv_name = "../test_resources/unit_test_event.csv"
        event_set1 = event_from_csv_long()
        event_set2 = event_from_csv_short()

        # Checking that event_set1.depth is not the same object
        # as event_set2.depth (as opposed to whether they are numerically
        # the same). 
        assert event_set1.depth is not event_set2.depth
        assert event_set1.trace_start_x is not event_set2.trace_start_x
        
        # Testing that the values were saved with good precision
        assert allclose(event_set1.depth,event_set2.depth)
        assert allclose(event_set1.rupture_centroid_lat,
                        event_set2.rupture_centroid_lat)
        assert allclose(event_set1.rupture_centroid_lon,
                        event_set2.rupture_centroid_lon)
        assert allclose(event_set1.azimuth,event_set2.azimuth)
        assert allclose(event_set1.dip,event_set2.dip)
        
        # Testing the values that were saved with val = 0.01*round(100*val)
        assert allclose(event_set1.recurrence,event_set2.recurrence)
        assert allclose(event_set1.trace_start_lat,event_set2.trace_start_lat,
                        atol=0.01)
        assert allclose(event_set1.trace_start_lon,event_set2.trace_start_lon,
                        atol=0.01) 
        assert allclose(event_set1.dip,event_set2.dip)

    def not_finished_test_event_from_file(self):
        (handle, file_name) = tempfile.mkstemp('_1.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        # I don't know what this is A_min="1.0"
        # But I added it so the tests would pass
        # Another example file at
        # Q:\python_eqrm\implementation_tests\input\newc_source_polygon.xml
        sample = """<Source_Model magnitude_type='Mw'>
<polygon area="5054.035">
  <boundary>-32.4000 151.1500 -32.7500 152.1700 -33.4500 151.4300 -32.4000 151.1500</boundary> 
  <recurrence distribution="bounded_gutenberg_richter" min_magnitude="3.3" max_magnitude="5.4" A_min="0.568" b="1" min_mag="4.5" depth="7" /> 
  </polygon>

</Source_Model>
"""

        handle.write(sample)
        handle.close()
        os.remove(file_name)

    def test_scenario_event(self):
        THE_PARAM_T = Dummy()
        THE_PARAM_T.scenario_latitude = -32.95
        THE_PARAM_T.scenario_longitude = 151.61
        THE_PARAM_T.scenario_azimuth = 340
        THE_PARAM_T.dip = 35
        THE_PARAM_T.scenario_magnitude = 8
        THE_PARAM_T.max_width = 15
        THE_PARAM_T.scenario_depth = 11.5
        THE_PARAM_T.scenario_number_of_events = 1
        
        event_set = Event_Set.create_scenario_events(
            rupture_centroid_lat=[THE_PARAM_T.scenario_latitude],
            rupture_centroid_lon=[THE_PARAM_T.scenario_longitude],
            azimuth=[THE_PARAM_T.scenario_azimuth],
            dip=[THE_PARAM_T.dip],
            Mw=[THE_PARAM_T.scenario_magnitude],
            fault_width=THE_PARAM_T.max_width,
            depth=[THE_PARAM_T.scenario_depth],
            scenario_number_of_events=THE_PARAM_T.scenario_number_of_events)

        #print "event_set.rupture_centroid_lat", event_set.rupture_centroid_lat
        answer = array(THE_PARAM_T.scenario_latitude)
        self.assert_(allclose(event_set.rupture_centroid_lat, answer))
        
        answer = array(THE_PARAM_T.scenario_longitude)
        self.assert_(allclose(event_set.rupture_centroid_lon, answer))
        
        answer = array(THE_PARAM_T.scenario_azimuth)
        self.assert_(allclose(event_set.azimuth, answer))
        
        answer = array(THE_PARAM_T.dip)
        self.assert_(allclose(event_set.dip, answer))
        
        answer = array(THE_PARAM_T.scenario_magnitude)
        self.assert_(allclose(event_set.Mw, answer))
        
        answer = array(THE_PARAM_T.max_width)
        self.assert_(allclose(event_set.fault_width, answer))
        
        answer = array(THE_PARAM_T.scenario_depth)
        self.assert_(allclose(event_set.depth, answer))
        
        self.assert_(THE_PARAM_T.scenario_number_of_events, len(event_set.Mw))

        area = array(conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.scenario_magnitude))
        self.assert_(allclose(event_set.area, area))

        width = array(conversions.modified_Wells_and_Coppersmith_94_width(
            THE_PARAM_T.dip,
            THE_PARAM_T.scenario_magnitude, area, THE_PARAM_T.max_width ))
        self.assert_ (allclose(event_set.width, width))
        
        answer = area/width 
        self.assert_(allclose(event_set.length, answer))
  
    def test_scenario_event_II(self):
        THE_PARAM_T = Dummy()
        THE_PARAM_T.scenario_latitude = [-30., -32.]
        THE_PARAM_T.scenario_longitude = [150., -151.]
        THE_PARAM_T.scenario_azimuth = [340, 330]
        THE_PARAM_T.dip = [37, 30]
        THE_PARAM_T.scenario_magnitude = [8, 7.5]
        THE_PARAM_T.max_width = [15, 7]
        THE_PARAM_T.scenario_depth = [11.5, 11.0]
        THE_PARAM_T.scenario_number_of_events = 1 # If this is 2 it fails
        
        event_set = Event_Set.create_scenario_events(
            rupture_centroid_lat=THE_PARAM_T.scenario_latitude,
            rupture_centroid_lon=THE_PARAM_T.scenario_longitude,
            azimuth=THE_PARAM_T.scenario_azimuth,
            dip=THE_PARAM_T.dip,
            Mw=THE_PARAM_T.scenario_magnitude,
            fault_width=THE_PARAM_T.max_width,
            depth=THE_PARAM_T.scenario_depth,
            scenario_number_of_events=THE_PARAM_T.scenario_number_of_events)
    
        answer = array(THE_PARAM_T.scenario_latitude)
        self.assert_(allclose(event_set.rupture_centroid_lat, answer))
        
        answer = array(THE_PARAM_T.scenario_longitude)
        self.assert_(allclose(event_set.rupture_centroid_lon, answer))
        
        answer = array(THE_PARAM_T.scenario_azimuth)
        self.assert_(allclose(event_set.azimuth, answer))
        
        answer = array(THE_PARAM_T.dip)
        self.assert_(allclose(event_set.dip, answer))
        
        answer = array(THE_PARAM_T.scenario_magnitude)
        self.assert_(allclose(event_set.Mw, answer))
        
        answer = array(THE_PARAM_T.max_width)
        self.assert_(allclose(event_set.fault_width, answer))
        
        answer = array(THE_PARAM_T.scenario_depth)
        self.assert_(allclose(event_set.depth, answer))
        
        self.assert_(THE_PARAM_T.scenario_number_of_events, len(event_set.Mw))

        area = array((conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.scenario_magnitude[0]),
            conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.scenario_magnitude[1])))
        self.assert_(allclose(event_set.area, area))

        width = array(conversions.modified_Wells_and_Coppersmith_94_width(
            THE_PARAM_T.dip, THE_PARAM_T.scenario_magnitude, area,
            THE_PARAM_T.max_width ))
        self.assert_(allclose(event_set.width, width))
        
        answer = area/width 
        self.assert_(allclose(event_set.length, answer))

    def test_scenario_event_III(self):
        
        THE_PARAM_T = Dummy()
        THE_PARAM_T.scenario_latitude = -32.95
        THE_PARAM_T.scenario_longitude = 151.61
        THE_PARAM_T.scenario_azimuth = 340
        THE_PARAM_T.dip = 35
        THE_PARAM_T.scenario_magnitude = 8
        THE_PARAM_T.max_width = 15
        THE_PARAM_T.scenario_depth = 11.5
        THE_PARAM_T.scenario_number_of_events = 2
        
        event_set = Event_Set.create_scenario_events(
            rupture_centroid_lat=[THE_PARAM_T.scenario_latitude],
            rupture_centroid_lon=[THE_PARAM_T.scenario_longitude],
            azimuth=[THE_PARAM_T.scenario_azimuth],
            dip=[THE_PARAM_T.dip],
            Mw=[THE_PARAM_T.scenario_magnitude],
            fault_width=THE_PARAM_T.max_width,
            depth=[THE_PARAM_T.scenario_depth],
            scenario_number_of_events=THE_PARAM_T.scenario_number_of_events)

        #print "event_set.rupture_centroid_lat", event_set.rupture_centroid_lat
        answer = array((THE_PARAM_T.scenario_latitude,
                        THE_PARAM_T.scenario_latitude))
        self.assert_ (allclose(event_set.rupture_centroid_lat, answer))
        
        answer = array((THE_PARAM_T.scenario_longitude,
                        THE_PARAM_T.scenario_longitude))
        self.assert_ (allclose(event_set.rupture_centroid_lon, answer))
        
        answer = array([THE_PARAM_T.scenario_azimuth,
                        THE_PARAM_T.scenario_azimuth])
        self.assert_ (allclose(event_set.azimuth, answer))
        
        answer = array([THE_PARAM_T.dip, THE_PARAM_T.dip])
        ###print "event_set.dip", event_set.dip
        self.assert_ (allclose(event_set.dip, answer))
        
        answer = array(THE_PARAM_T.scenario_magnitude)
        #print "answer", answer
        #print "event_set.Mw", event_set.Mw
        # in allclose [8 8] == 8
        self.assert_ (allclose(event_set.Mw, answer))
        
        answer = array(THE_PARAM_T.max_width)
        self.assert_ (allclose(event_set.fault_width, answer))
        
        answer = array(THE_PARAM_T.scenario_depth)
        self.assert_ (allclose(event_set.depth, answer))
        
        self.assert_ (THE_PARAM_T.scenario_number_of_events, len(event_set.Mw))

        area = array(conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.scenario_magnitude))
        self.assert_ (allclose(event_set.area, area))

        width = array(conversions.modified_Wells_and_Coppersmith_94_width(
            THE_PARAM_T.dip, THE_PARAM_T.scenario_magnitude,
            area, THE_PARAM_T.max_width ))
        self.assert_ (allclose(event_set.width, width))
        
        answer = area/width 
        self.assert_ (allclose(event_set.length, answer))


        self.assert_ (len(event_set.length)== \
                      THE_PARAM_T.scenario_number_of_events)
        
    def test_scenario_event_4(self):
        
        THE_PARAM_T = Dummy()
        THE_PARAM_T.scenario_latitude = [-30.]
        THE_PARAM_T.scenario_longitude = [150.]
        THE_PARAM_T.scenario_azimuth = [0]
        THE_PARAM_T.dip = [45]
        THE_PARAM_T.scenario_magnitude = [6.02]
        THE_PARAM_T.max_width = [5]
        THE_PARAM_T.scenario_depth = [7]
        THE_PARAM_T.scenario_number_of_events = 1 # If this is 2 it fails
        
        event_set = Event_Set.create_scenario_events(
            rupture_centroid_lat=THE_PARAM_T.scenario_latitude,
            rupture_centroid_lon=THE_PARAM_T.scenario_longitude,
            azimuth=THE_PARAM_T.scenario_azimuth,
            dip=THE_PARAM_T.dip,
            Mw=THE_PARAM_T.scenario_magnitude,
            fault_width=THE_PARAM_T.max_width,
            depth=THE_PARAM_T.scenario_depth,
            scenario_number_of_events=THE_PARAM_T.scenario_number_of_events)

    
        answer = array(THE_PARAM_T.max_width)
        self.assert_ (allclose(event_set.width, answer))
        
        area = array((conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.scenario_magnitude[0])))
        self.assert_ (allclose(100., area))
        self.assert_ (allclose(event_set.area, area))

        width = array(
            conversions.modified_Wells_and_Coppersmith_94_width(
            THE_PARAM_T.dip, THE_PARAM_T.scenario_magnitude,
            area, THE_PARAM_T.max_width ))
        self.assert_ (allclose(5., width))
        self.assert_ (allclose(event_set.width, width))
        
        self.assert_ (allclose(event_set.length, 20.))
        
        self.assert_ (allclose(event_set.trace_start_x, -10.))

        # Due to the 45 deg dip
        self.assert_ (allclose(event_set.trace_start_y, -event_set.depth))

        #event_set.trace_start_lat [-30.09]
        #event_set.trace_start_lon [ 149.93]
        #event_set.trace_end_lat [-29.91001134]
        #event_set.trace_end_lon [ 149.92726303]

        
        # Zone:   56 
        #Easting:  210590.347  Northing: 6677424.096 
        #Latitude:   -30  0 ' 0.00000 ''  Longitude: 150  0 ' 0.00000 ''
        
        # start
        # Easting:  203590.347
        # Northing: 6667424.096
        # Latitude:   -30 5 ' 18.39181 ''  Longitude: 149 55 ' 29.06358
        # -30.08
        # 149.92
        
        # End 
        # Easting:  203583.347
        # Northing: 6687424.096
        # Latitude:   -29 54 ' 29.55723 ''  Longitude: 149 55 ' 49.06877 ''
        # -29.90
        # 149.92

        self.assert_ (allclose(event_set.trace_start_lat, -30.08,0.001))
        self.assert_ (allclose(event_set.trace_start_lon, 149.9,0.001))
        
        self.assert_ (allclose(event_set.trace_end_lat, -29.9,0.001))
        self.assert_ (allclose(event_set.trace_end_lon, 149.9,0.001))
        
        repr = event_set.__repr__()
        repr_list = repr.split('\n')
        results = repr_list[1].split(':')
        self.assert_ (int(results[1]) == 1)
        results = repr_list[2].split(':')
        self.assert_ (float(results[1].strip('[]')) == \
                      THE_PARAM_T.scenario_latitude[0])
        results = repr_list[3].split(':')
        self.assert_ (float(results[1].strip('[]')) == \
                      THE_PARAM_T.scenario_longitude[0])
        results = repr_list[4].split(':')
        self.assert_ (float(results[1].strip('[]')) == \
                      THE_PARAM_T.scenario_magnitude [0])
        self.assert_ (len(event_set) == 1)
        
    def test_generate_synthetic_events(self):
        
        
        fault_width = 5
        azi = array([90])
        dazi = array([2])
        fault_dip = array([35.0])
        prob_min_mag_cutoff = 1.0
        override_xml = True
        prob_number_of_events_in_zones = array([1])
        handle, file_name = tempfile.mkstemp('_2.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')

        
        sample = """<source_model_zone magnitude_type='Mw'>
<zone area="5054.035" name = "tongs" event_type = "crustal fault">
<geometry
       azimuth= "6" 
       delta_azimuth= "2" 
       dip= "15"
       delta_dip = "5"
       depth_top_seismogenic = "7"
       depth_bottom_seismogenic = "30">
  <boundary>-32.000 151.00 -32.0 151.05 -32.05 151.05 -32.05 151.0</boundary> 
</geometry>
  <recurrence_model distribution = "bounded_gutenberg_richter"
      recurrence_min_mag = "3.3" 
      recurrence_max_mag = "5.4" 
      A_min= "0.568" 
      b = "1"> 
      <event_generation 
      generation_min_mag = "3.3"
	  number_of_mag_sample_bins = "15" 
	  number_of_events = "1000" />
    </recurrence_model>
  </zone>
</source_model_zone>
"""
        handle.write(sample)
        handle.close()
        # 1 zone therefore 1 source
        source = Dummy()
        source.scaling = {'scaling_rule':'modified_Wells_and_Coppersmith_94'}
        source_model = [source]


        (handle, et_file_name) = tempfile.mkstemp('_3.xml', __name__+'_')
        os.close(handle)
        et_handle = open(et_file_name,'w')

        sample = '\n'.join(
            ['<?xml version="1.0" encoding="UTF-8"?>',
             '<event_type_controlfile>'
             '  <event_group event_type = "crustal fault">'
             '    <GMPE fault_type = "more_crustal fault">'
             '      <branch model = "food" weight = "1.0"/>'
             '    </GMPE>'
             '    <scaling scaling_rule = "y" />'
             '  </event_group>'
             '  <event_group event_type = "eggs">'
             '    <GMPE fault_type = "more_eggs">'
             '      <branch model = "Camp" weight = "1.0"/>'
             '    </GMPE>'
             '    <scaling scaling_rule = "e" />'
             '  </event_group>'
             '</event_type_controlfile>'])

        et_handle.write(sample)
        et_handle.close()

        #file_name = os.path.join('..','implementation_tests','input','newc_source_polygon.xml')
        #return
        # need to fix
        events = Event_Set.generate_synthetic_events(
            file_name,
            prob_min_mag_cutoff,
            source_model,
            prob_number_of_events_in_zones=prob_number_of_events_in_zones)
#         print "events.trace_start_lat", events.trace_start_lat
#         print " events.trace_start_lon", events.trace_start_lon
#         print "events.trace_end_lat", events.trace_end_lat
#         print "events.trace_end_lon", events.trace_end_lon
#         print "events.rupture_centroid_lat", events.rupture_centroid_lat
#         print "events.rupture_centroid_lon", events.rupture_centroid_lon
#         print "events.rupture_centroid_x", events.rupture_x
#         print "events.rupture_centroid_y", events.rupture_y
#         print "events.trace_start_x", events.trace_start_x
#         print " events.trace_start_y", events.trace_start_y
        self.assert_(events.rupture_centroid_lat <= -32.0)
        self.assert_(events.rupture_centroid_lat >= -32.05)
        self.assert_(events.rupture_centroid_lon <= 151.05)
        self.assert_(events.rupture_centroid_lon >= 151.0)
        
        os.remove(file_name)
        os.remove(et_file_name)


    def test_generate_synthetic_events_horspool(self):

        handle, file_name = tempfile.mkstemp('_4.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        sample = """<source_model_zone magnitude_type="Mw">
  <zone 
  area = "5054.035" 
  name = "bad zone"
  event_type = "crustal fault">
    
    <geometry 
       azimuth= "45" 
       delta_azimuth= "5" 
       dip= "35"
       delta_dip = "5"
       depth_top_seismogenic = "7"
       depth_bottom_seismogenic = "15.60364655">
      <boundary>
	  151.1500 -32.4000  
	  152.1700 -32.7500
	  151.4300 -33.4500  
	  151.1500 -32.4000
      </boundary>
      <excludes>
	  151.1500 -32.4000    
	  152.1700 -32.7500   
	  151.4300 -33.4500 
      </excludes>
    </geometry>
    
    <recurrence_model
      distribution = "bounded_gutenberg_richter"
      recurrence_min_mag = "3.4" 
      recurrence_max_mag = "5.4" 
      A_min= "0.568" 
      b = "1">
      <event_generation 
      generation_min_mag = "3.3"
	  number_of_mag_sample_bins = "15" 
	  number_of_events = "1" />
    </recurrence_model>
    
    <ground_motion_models 
       fault_type = "normal" 
       ground_motion_selection = "crustal fault" />   
  </zone>
   <zone 
  area = "5054.035" 
  name = "bad zone"
  event_type = "crustal fault">
    
    <geometry 
       azimuth= "45" 
       delta_azimuth= "5" 
       dip= "35"
       delta_dip = "5"
       depth_top_seismogenic = "7"
       depth_bottom_seismogenic = "15.60364655">
      <boundary>
	  151.1500 -32.4000  
	  152.1700 -32.7500
	  151.4300 -33.4500  
	  151.1500 -32.4000
      </boundary>
      <excludes>
	  151.1500 -32.4000    
	  152.1700 -32.7500   
	  151.4300 -33.4500 
      </excludes>
    </geometry>
    
    <recurrence_model
      distribution = "bounded_gutenberg_richter"
      recurrence_min_mag = "3.4" 
      recurrence_max_mag = "5.4" 
      A_min= "0.568" 
      b = "1">
      <event_generation 
      generation_min_mag = "3.3"
	  number_of_mag_sample_bins = "15" 
	  number_of_events = "2" />
    </recurrence_model>
    
    <ground_motion_models 
       fault_type = "normal" 
       ground_motion_selection = "crustal fault" />   
  </zone>
</source_model_zone>
"""
        handle.write(sample)
        handle.close()

        
        source = Dummy()
        source.scaling = {'scaling_rule':'modified_Wells_and_Coppersmith_94'}
        source_model = [source, source]

        fault_width = None
        azi = None
        dazi = None
        fault_dip = None
        override_xml = None
        prob_number_of_events_in_zones = None
        prob_min_mag_cutoff = 0.1
        
        
        events = Event_Set.generate_synthetic_events(
            file_name,
            prob_min_mag_cutoff,
            source_model,
            prob_number_of_events_in_zones=prob_number_of_events_in_zones)
        
        
        self.assert_(len(events)==3)
        
        os.remove(file_name)
        
    def test_event_set_subsetting(self):
        rupture_centroid_lat = [-33.351170370959323, -32.763381339789468]
        rupture_centroid_lon = [151.45946928787703, 151.77787395867014]
        azimuth = [162.8566392635347, 201.51805898897854]
        dip = [35.0, 35.0]
        #dip = None
        ML = None
        Mw = [5.0286463459649076, 4.6661943094693887]
        fault_width = [15.0, 15.0]
        #fault_width = None
        depth_top_seismogenic = [7.0, 7.0]

        set = Event_Set.create(
            rupture_centroid_lat,
            rupture_centroid_lon,
            azimuth,
            dip,
            ML,
            Mw,
            None, #depth,
            fault_width,
            depth_top_seismogenic=depth_top_seismogenic)
        set.source_zone_id = asarray([0,1]) #FIXME
        for i,event in enumerate(set):
            self.assert_(event.trace_start_lat == set.trace_start_lat[i])
            self.assert_(event.azimuth == set.azimuth[i])
            self.assert_(event.dip == set.dip[i])
            self.assert_(event.ML == set.ML[i])
            self.assert_(event.Mw == set.Mw[i])
            self.assert_(event.depth == set.depth[i])
            self.assert_(event.width == set.width[i])
            self.assert_(event.length == set.length[i])
            self.assert_(event.trace_start_lat == set.trace_start_lat[i])
            self.assert_(event.rupture_centroid_lat == set.rupture_centroid_lat[i])
            self.assert_(event.rupture_centroid_lon == set.rupture_centroid_lon[i])
            self.assert_(event.rupture_y == set.rupture_y[i])
            self.assert_(event.rupture_x == set.rupture_x[i])
            self.assert_(event.trace_start_y == set.trace_start_y[i])
            self.assert_(event.trace_start_x == set.trace_start_x[i])
            self.assert_(event.source_zone_id == set.source_zone_id[i])
            self.assert_(event.trace_end_lat == set.trace_end_lat[i])
            self.assert_(event.trace_end_lon == set.trace_end_lon[i])
           

        
        
    def test_Event_Activity(self):
        num_events = 3
        ea = Event_Activity(num_events)
        event_indexes = array([0,2])
        event_activities = array([10, 20])
        ea.set_event_activity(event_activities, event_indexes)
        self.assert_(allclose(ea.event_activity[0,0,0], 10))
        self.assert_(allclose(ea.event_activity[0,0,1], 0))
        self.assert_(allclose(ea.event_activity[0,0,2], 20))

        
    def test_Event_Activity_set_event_activity(self):
        num_events = 3
        ea = Event_Activity(num_events)
        event_activities = array([0, 10, 20])
        ea.set_event_activity(event_activities)
        self.assert_(allclose(ea.event_activity[0,0,0], 0))
        self.assert_(allclose(ea.event_activity[0,0,1], 10))
        self.assert_(allclose(ea.event_activity[0,0,2], 20))

        
    def test_Event_Activity_spawn(self):
        num_events = 3
        ea = Event_Activity(num_events)
        event_activities = array([1, 10, 100])
        ea.set_event_activity(event_activities)
        w = array([0.2, 0.8])
        ea.spawn(w)
        self.assert_(allclose(ea.event_activity[0,0,0], 0.2))
        self.assert_(allclose(ea.event_activity[0,0,1], 2))
        self.assert_(allclose(ea.event_activity[0,0,2], 20))
        self.assert_(allclose(ea.event_activity[1,0,0], 0.8))
        self.assert_(allclose(ea.event_activity[1,0,1], 8))
        self.assert_(allclose(ea.event_activity[1,0,2], 80))

        event = ea.event_activity.reshape(-1)
        # this should 'stack' so it goes [0,0 0,1 0,2 1,0 1,1 1,2]
        # with the numbers representing the indexes from the 2D array
        self.assert_(allclose(event[1], 2))
        self.assert_(allclose(event[4], 8))

        
    def test_Event_Activity_ground_motion_model_logic_split(self):      
        num_events = 6
        max_weights = 5
        ea = Event_Activity(num_events)
        indexes = arange(6)
        activity = indexes*10
        
        ea.set_event_activity(activity, indexes)
        atten_model_weights = [array([.4, .6]),array([.1, .4, .5])]
        a = Dummy()
        b = Dummy()
        source_model = [a, b]
        #event_set_indexes = [array([0,1,3]), array([2,4])]
        event_set_indexes = [[0,1,3], [2,4]]
        for sp, esi, amw in map(None, source_model, event_set_indexes,
                                atten_model_weights):
            sp.atten_model_weights = amw
            sp.event_set_indexes = esi
        source_model = Source_Model(source_model) 
            
        ea.ground_motion_model_logic_split(source_model, apply_weights=True)   
        self.assert_(allclose(sum(ea.event_activity), sum(activity)))
        self.assert_(allclose(ea.event_activity[0,0,3], 12.))
        self.assert_(allclose(ea.event_activity[0,0,4], 4.))


    def test_apply_spawn(self):      
        num_events = 6
        max_weights = 5
        ea = Event_Activity(num_events)
        indexes = arange(6)
        activity = indexes*10
        
        ea.set_event_activity(activity, indexes)
        atten_model_weights = [array([.4, .6]),array([.1, .4, .5])]
        a = Dummy()
        b = Dummy()
        source_model = [a, b]
        #event_set_indexes = [array([0,1,3]), array([2,4])]
        event_set_indexes = [[0,1,3], [2,4]]
        for sp, esi, amw in map(None, source_model, event_set_indexes,
                                atten_model_weights):
            sp.atten_model_weights = amw
            sp.event_set_indexes = esi
        source_model = Source_Model(source_model)    
        ea.ground_motion_model_logic_split(source_model, apply_weights=True)   
        self.assert_(allclose(sum(ea.event_activity), sum(activity)))
        self.assert_(allclose(ea.event_activity[0,0,3], 12.))
        self.assert_(allclose(ea.event_activity[0,0,4], 4.))
        
        w = array([0.25,
                   0.75])
        ea.spawn(w)
        self.assert_(allclose(ea.event_activity[0,0,3], 3.))
        self.assert_(allclose(ea.event_activity[1,0,3], 9.))
        self.assert_(allclose(ea.event_activity[0,0,4], 1.))
        self.assert_(allclose(ea.event_activity[1,0,4], 3.))
        
        self.assert_(allclose(ea.event_activity[0,1,1], 6./4.))
        self.assert_(allclose(ea.event_activity[1,1,1], 6.*0.75))
        
        event = ea.event_activity.reshape(-1)
        # this should 'stack' so it goes [0,0,0 0,0,1 0,2 1,0 1,1 1,2]
        # with the numbers representing the indexes from the 2D array
        self.assert_(allclose(event[3], 3))
        self.assert_(allclose(event[7], 6./4.))

        self.assert_(ea.get_num_spawn() == 2)
        self.assert_(allclose(ea.get_ea_event_dimsion_only(),
                              activity))
        
    def test_generate_synthetic_events_fault(self):
        def dump_src(etc):
            """Helper function to dump info from SRC object."""

            for attr in dir(src):
                if attr[0] != '_': # and attr != 'name_type_map':
                    val = eval('src.%s' % attr)
                    if isinstance(val, dict):
                        print('    %s=%s' % (attr, str(val)))
                    elif isinstance(val, types.MethodType):
                        pass
                    else:
                        print('    %s=%s (%s)' % (attr, str(val), type(val)))

        # create a test FSG file
        (handle, fault_xml_file) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(fault_xml_file,'w')
        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<source_model_fault magnitude_type="Mw">',
                            '  <fault name="big fault" event_type="crustal fault">',
                            '    <geometry dip="30" out_of_dip_theta="0"',
                            '              delta_theta="0"',
                            '              depth_top_seismogenic="0"',
                            '              depth_bottom_seismogenic="15"',
                            '              slab_width="0">',
                            '      <trace>',
                            '        <start lat="-17.5" lon="110.0" />',
                            '        <end lat="-17.0" lon="110.0" />',
                            '      </trace>',
                            '    </geometry>',
                            '    <recurrence_model distribution="bounded_gutenberg_richter"',
                            '                      recurrence_min_mag="4.0"',
                            '                      recurrence_max_mag="7.0"',
                            '                      slip_rate="2.0" b="1">',
                            '      <event_generation generation_min_mag="4.0"',
                            '                        number_of_mag_sample_bins="15"',
                            '                        number_of_events="1500" />',
                            '    </recurrence_model>',
                            '  </fault>',
                            '  <fault name="small fault" event_type="intraslab">',
                            '    <geometry dip="90" out_of_dip_theta="10"',
                            '              delta_theta="5"',
                            '              depth_top_seismogenic="10"',
                            '              depth_bottom_seismogenic="50"',
                            '              slab_width="10">',
                            '      <trace>',
                            '        <start lat="-17.0" lon="120.0" />',
                            '        <end lat="-17.0" lon="120.5" />',
                            '      </trace>',
                            '    </geometry>',
                            '    <recurrence_model distribution="characteristic"',
                            '                      recurrence_min_mag="4.5"',
                            '                      recurrence_max_mag="7.5"',
                            '                      slip_rate="3.0" b="2">',
                            '      <event_generation generation_min_mag="4.0"',
                            '                        number_of_mag_sample_bins="15"',
                            '                        number_of_events="1500" />',
                            '    </recurrence_model>',
                            '  </fault>',
                            '</source_model_fault>'])
        handle.write(sample)
        handle.close()

        # create a test ETC file
        (handle, event_control_file) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(event_control_file, 'w')
        sample = '\n'.join(['<?xml version="1.0" encoding="UTF-8"?>',
                            '<event_type_controlfile>'
                            '  <event_group event_type = "background">'
                            '    <GMPE fault_type = "normal">'
                            '      <branch model = "Toro_1997_midcontinent" weight = "0.3"/>'
                            '      <branch model = "Atkinson_Boore_97" weight = "0.4"/>'
                            '      <branch model = "Sadigh_97" weight = "0.3"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '  <event_group event_type = "crustal fault">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Campbell08" weight = "0.8"/>'
                            '      <branch model = "Boore08" weight = "0.2"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "reverse" />'
                            '  </event_group>'
                            '  <event_group event_type = "interface">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Zhao06_crustalinterface" weight = "0.5"/>'
                            '      <branch model = "Atkinson03_interface" weight = "0.5"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "reverse" />'
                            '  </event_group>'
                            '  <event_group event_type = "intraslab">'
                            '    <GMPE fault_type = "reverse">'
                            '      <branch model = "Zhao06_slab" weight = "0.5"/>'
                            '      <branch model = "Atkinson03_inslab" weight = "0.5"/>'
                            '    </GMPE>'
                            '    <scaling scaling_rule = "Wells_and_Coppersmith_94" scaling_fault_type = "unspecified" />'
                            '  </event_group>'
                            '</event_type_controlfile>'])
        handle.write(sample)
        handle.close()

        prob_min_mag_cutoff = 4.0
        prob_number_of_events_in_faults =[15,15]

        (event_set_zone, source_mod_zone) = generate_synthetic_events_fault(
            fault_xml_file,
            event_control_file,
            prob_min_mag_cutoff,
            prob_number_of_events_in_faults)
        
        prob_min_mag_cutoff = 3.0
        prob_number_of_events_in_faults =[10,10]
        (event_set_fault, source_mod_fault) = generate_synthetic_events_fault(
            fault_xml_file,
            event_control_file,
            prob_min_mag_cutoff,
            prob_number_of_events_in_faults)
        
        (event_set, source_mod)= merge_events_and_sources(
            event_set_zone,
            event_set_fault,
            source_mod_zone, 
            source_mod_fault
            )

        os.remove(fault_xml_file)
        os.remove(event_control_file)
        #event_activity = Event_Activity(len(event_set))
        #source_mod.calculate_recurrence(
         #   event_set,
          #  event_activity)
        
        #print event_set.__len__()

        #check event_set check sourcelist
        
        #calc event activity
        
        #check activities
#        # dump the SRC objects
#        for src in src_list:
#            print('-'*50)
#            print('%s:' % src.event_type)
#            dump_src(src)


    def test_merge_events_and_sources(self):
        para = array([0, 1., 2.])
        para_list = [para]*22
        events_zone = Event_Set(*para_list)
        para = array([3., 4., 5., 6.])
        para_list = [para]*22
        events_fault = Event_Set(*para_list)

        atten_model_weights = [array([.4, .6]),array([.1, .4, .5])]
        a = Dummy()
        b = Dummy()
        source_model = [a, b]
        event_set_indexes = [array([0]), array([1])]
        for sp, esi, amw in map(None, source_model, event_set_indexes,
                                atten_model_weights):
            sp.atten_model_weights = amw
            sp.event_set_indexes = esi
        source_zone = Source_Model(source_model)
        
        atten_model_weights = [array([.4, .6]),array([.1, .4, .5])]
        a = Dummy()
        b = Dummy()
        source_model = [a, b]
        event_set_indexes = [array([0,1]), array([2,3])]
        for sp, esi, amw in map(None, source_model, event_set_indexes,
                                atten_model_weights):
            sp.atten_model_weights = amw
            sp.event_set_indexes = esi
        source_fault = Source_Model(source_model)

        event_set_merged, source_model_merged = merge_events_and_sources(
            events_zone, events_fault,
            source_zone, source_fault)

        self.assert_(len(event_set_merged) == 7)
        answers = array([0, 1., 2., 3., 4., 5., 6.])
        self.assert_(allclose(event_set_merged.Mw, answers))
        source_answers = [array([0]), array([1]),
                          array([3,4]), array([5,6])]
        for smm, ans in map(None, source_model_merged, source_answers):
            self.assert_(allclose(
                smm.event_set_indexes, ans))
            
        
        
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Event_Set,'test')
    #suite = unittest.makeSuite(Test_Event_Set,'test_generate_synthetic_events')
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
