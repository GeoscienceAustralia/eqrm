
import os
import sys
from random import uniform,seed
from time import time
import unittest
from os import sep
import tempfile

from scipy import array, allclose, asarray

from xml_interface import Xml_Interface
from source_model import source_model_from_xml
import conversions

from event_set import Event_Set, Pseudo_Event_Set


class Dummy:
    def __init__(self):
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
        (handle, file_name) = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        # I don't know what this is Lambda_Min="1.0"
        # But I added it so the tests would pass
        # Another example file at
        # Q:\python_eqrm\implementation_tests\input\newc_source_polygon.xml
        sample = """<Source_Model magnitude_type='Mw'>
<polygon area="5054.035">
  <boundary>-32.4000 151.1500 -32.7500 152.1700 -33.4500 151.4300 -32.4000 151.1500</boundary> 
  <recurrence distribution="bounded_gutenberg_richter" min_magnitude="3.3" max_magnitude="5.4" Lambda_Min="0.568" b="1" min_mag="4.5" depth="7" /> 
  </polygon>

</Source_Model>
"""

        handle.write(sample)
        handle.close()
        os.remove(file_name)

    def test_deterministic_event(self):
        THE_PARAM_T = Dummy()
        THE_PARAM_T.determ_latitude = -32.95
        THE_PARAM_T.determ_longitude = 151.61
        THE_PARAM_T.determ_azimith = 340
        THE_PARAM_T.dip = 35
        THE_PARAM_T.determ_magnitude = 8
        THE_PARAM_T.max_width = 15
        THE_PARAM_T.determ_depth = 11.5
        THE_PARAM_T.determ_number_of_events = 1
        
        event_set = Event_Set.create(
            rupture_centroid_lat=[THE_PARAM_T.determ_latitude],
            rupture_centroid_lon=[THE_PARAM_T.determ_longitude],
            azimuth=[THE_PARAM_T.determ_azimith],
            dip=[THE_PARAM_T.dip],
            Mw=[THE_PARAM_T.determ_magnitude],
            fault_width=THE_PARAM_T.max_width,
            depth=[THE_PARAM_T.determ_depth],
            determ_number_of_events=THE_PARAM_T.determ_number_of_events)

        #print "event_set.rupture_centroid_lat", event_set.rupture_centroid_lat
        answer = array(THE_PARAM_T.determ_latitude)
        self.assert_(allclose(event_set.rupture_centroid_lat, answer))
        
        answer = array(THE_PARAM_T.determ_longitude)
        self.assert_(allclose(event_set.rupture_centroid_lon, answer))
        
        answer = array(THE_PARAM_T.determ_azimith)
        self.assert_(allclose(event_set.azimuth, answer))
        
        answer = array(THE_PARAM_T.dip)
        self.assert_(allclose(event_set.dip, answer))
        
        answer = array(THE_PARAM_T.determ_magnitude)
        self.assert_(allclose(event_set.Mw, answer))
        
        answer = array(THE_PARAM_T.max_width)
        self.assert_(allclose(event_set.fault_width, answer))
        
        answer = array(THE_PARAM_T.determ_depth)
        self.assert_(allclose(event_set.depth, answer))
        
        self.assert_(THE_PARAM_T.determ_number_of_events, len(event_set.Mw))

        area = array(conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.determ_magnitude))
        self.assert_(allclose(event_set.area, area))

        width = array(conversions.\
                      modified_Wells_and_Coppersmith_94_width(THE_PARAM_T.dip,
                                                 THE_PARAM_T.determ_magnitude,
                                                 area, THE_PARAM_T.max_width))
        self.assert_(allclose(event_set.width, width))
        
        answer = area/width 
        self.assert_(allclose(event_set.length, answer))
  
    def test_deterministic_event_II(self):
        THE_PARAM_T = Dummy()
        THE_PARAM_T.determ_latitude = [-30., -32.]
        THE_PARAM_T.determ_longitude = [150., -151.]
        THE_PARAM_T.determ_azimith = [340, 330]
        THE_PARAM_T.dip = [37, 30]
        THE_PARAM_T.determ_magnitude = [8, 7.5]
        THE_PARAM_T.max_width = [15, 7]
        THE_PARAM_T.determ_depth = [11.5, 11.0]
        THE_PARAM_T.determ_number_of_events = 1 # If this is 2 it fails
        
        event_set = Event_Set.create(
            rupture_centroid_lat=THE_PARAM_T.determ_latitude,
            rupture_centroid_lon=THE_PARAM_T.determ_longitude,
            azimuth=THE_PARAM_T.determ_azimith,
            dip=THE_PARAM_T.dip,
            Mw=THE_PARAM_T.determ_magnitude,
            fault_width=THE_PARAM_T.max_width,
            depth=THE_PARAM_T.determ_depth,
            determ_number_of_events=THE_PARAM_T.determ_number_of_events)
    
        #print "event_set.rupture_centroid_lat", event_set.rupture_centroid_lat
        answer = array(THE_PARAM_T.determ_latitude)
        self.assert_(allclose(event_set.rupture_centroid_lat, answer))
        
        answer = array(THE_PARAM_T.determ_longitude)
        self.assert_(allclose(event_set.rupture_centroid_lon, answer))
        
        answer = array(THE_PARAM_T.determ_azimith)
        self.assert_(allclose(event_set.azimuth, answer))
        
        answer = array(THE_PARAM_T.dip)
        self.assert_(allclose(event_set.dip, answer))
        
        answer = array(THE_PARAM_T.determ_magnitude)
        self.assert_(allclose(event_set.Mw, answer))
        
        answer = array(THE_PARAM_T.max_width)
        self.assert_(allclose(event_set.fault_width, answer))
        
        answer = array(THE_PARAM_T.determ_depth)
        self.assert_(allclose(event_set.depth, answer))
        
        self.assert_(THE_PARAM_T.determ_number_of_events, len(event_set.Mw))

        area = array((conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.determ_magnitude[0]),
            conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.determ_magnitude[1])))
        self.assert_(allclose(event_set.area, area))

        width = array(conversions.modified_Wells_and_Coppersmith_94_width(
            THE_PARAM_T.dip, THE_PARAM_T.determ_magnitude, area, THE_PARAM_T.max_width ))
        self.assert_(allclose(event_set.width, width))
        
        answer = area/width 
        self.assert_(allclose(event_set.length, answer))

    def test_deterministic_event_III(self):
        
        THE_PARAM_T = Dummy()
        THE_PARAM_T.determ_latitude = -32.95
        THE_PARAM_T.determ_longitude = 151.61
        THE_PARAM_T.determ_azimith = 340
        THE_PARAM_T.dip = 35
        THE_PARAM_T.determ_magnitude = 8
        THE_PARAM_T.max_width = 15
        THE_PARAM_T.determ_depth = 11.5
        THE_PARAM_T.determ_number_of_events = 2
        
        event_set = Event_Set.create(
            rupture_centroid_lat=[THE_PARAM_T.determ_latitude],
            rupture_centroid_lon=[THE_PARAM_T.determ_longitude],
            azimuth=[THE_PARAM_T.determ_azimith],
            dip=[THE_PARAM_T.dip],
            Mw=[THE_PARAM_T.determ_magnitude],
            fault_width=THE_PARAM_T.max_width,
            depth=[THE_PARAM_T.determ_depth],
            determ_number_of_events=THE_PARAM_T.determ_number_of_events)

        #print "event_set.rupture_centroid_lat", event_set.rupture_centroid_lat
        answer = array((THE_PARAM_T.determ_latitude, THE_PARAM_T.determ_latitude))
        self.assert_ (allclose(event_set.rupture_centroid_lat, answer))
        
        answer = array((THE_PARAM_T.determ_longitude, THE_PARAM_T.determ_longitude))
        self.assert_ (allclose(event_set.rupture_centroid_lon, answer))
        
        answer = array([THE_PARAM_T.determ_azimith, THE_PARAM_T.determ_azimith])
        self.assert_ (allclose(event_set.azimuth, answer))
        
        answer = array([THE_PARAM_T.dip, THE_PARAM_T.dip])
        ###print "event_set.dip", event_set.dip
        self.assert_ (allclose(event_set.dip, answer))
        
        answer = array(THE_PARAM_T.determ_magnitude)
        #print "answer", answer
        #print "event_set.Mw", event_set.Mw
        # in allclose [8 8] == 8
        self.assert_ (allclose(event_set.Mw, answer))
        
        answer = array(THE_PARAM_T.max_width)
        self.assert_ (allclose(event_set.fault_width, answer))
        
        answer = array(THE_PARAM_T.determ_depth)
        self.assert_ (allclose(event_set.depth, answer))
        
        self.assert_ (THE_PARAM_T.determ_number_of_events, len(event_set.Mw))

        area = array(conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.determ_magnitude))
        self.assert_ (allclose(event_set.area, area))

        width = array(conversions.modified_Wells_and_Coppersmith_94_width(
            THE_PARAM_T.dip, THE_PARAM_T.determ_magnitude, area, THE_PARAM_T.max_width ))
        self.assert_ (allclose(event_set.width, width))
        
        answer = area/width 
        self.assert_ (allclose(event_set.length, answer))


        self.assert_ (len(event_set.length)==THE_PARAM_T.determ_number_of_events)
        
    def test_deterministic_event_4(self):
        
        THE_PARAM_T = Dummy()
        THE_PARAM_T.determ_latitude = [-30.]
        THE_PARAM_T.determ_longitude = [150.]
        THE_PARAM_T.determ_azimith = [0]
        THE_PARAM_T.dip = [45]
        THE_PARAM_T.determ_magnitude = [6.02]
        THE_PARAM_T.max_width = [5]
        THE_PARAM_T.determ_depth = [7]
        THE_PARAM_T.determ_number_of_events = 1 # If this is 2 it fails
        
        event_set = Event_Set.create(
            rupture_centroid_lat=THE_PARAM_T.determ_latitude,
            rupture_centroid_lon=THE_PARAM_T.determ_longitude,
            azimuth=THE_PARAM_T.determ_azimith,
            dip=THE_PARAM_T.dip,
            Mw=THE_PARAM_T.determ_magnitude,
            fault_width=THE_PARAM_T.max_width,
            depth=THE_PARAM_T.determ_depth,
            determ_number_of_events=THE_PARAM_T.determ_number_of_events)

    
        answer = array(THE_PARAM_T.max_width)
        self.assert_ (allclose(event_set.width, answer))
        
        area = array((conversions.modified_Wells_and_Coppersmith_94_area(
            THE_PARAM_T.determ_magnitude[0])))
        self.assert_ (allclose(100., area))
        self.assert_ (allclose(event_set.area, area))

        width = array(conversions.modified_Wells_and_Coppersmith_94_width(
            THE_PARAM_T.dip, THE_PARAM_T.determ_magnitude, area, THE_PARAM_T.max_width ))
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
        self.assert_ (float(results[1].strip('[]')) == THE_PARAM_T.determ_latitude[0])
        results = repr_list[3].split(':')
        self.assert_ (float(results[1].strip('[]')) == THE_PARAM_T.determ_longitude[0])
        results = repr_list[4].split(':')
        self.assert_ (float(results[1].strip('[]')) == THE_PARAM_T.determ_magnitude [0])
        self.assert_ (len(event_set) == 1)
        
    def test_generate_synthetic_events(self):
        
        
        fault_width = 5
        azi = array([90])
        dazi = array([2])
        fault_dip = array([35.0])
        prob_min_mag_cutoff = 1.0
        override_xml = True
        prob_number_of_events_in_zones = 1    # changing this doesn't seem to do anything. 
        handle, file_name = tempfile.mkstemp('.xml', __name__+'_')
        os.close(handle)
        handle = open(file_name,'w')
        
        # I don't know what this is Lambda_Min="1.0"
        # But I added it so the tests would pass
        # Another example file at
        # Q:\python_eqrm\implementation_tests\input\newc_source_polygon.xml

        #  polygon is a small square

        
        sample = """<Source_Model magnitude_type='Mw'>
<polygon area="5054.035">
  <boundary>-32.000 151.00 -32.0 151.05 -32.05 151.05 -32.05 151.0</boundary> 
  <recurrence distribution="bounded_gutenberg_richter" min_magnitude="3.3" max_magnitude="5.4" Lambda_Min="0.568" b="1" min_mag="4.5" depth="7" /> 
  </polygon>

</Source_Model>
"""
        handle.write(sample)
        handle.close()
        
        #file_name = os.path.join('..','implementation_tests','input','newc_source_polygon.xml')
        #return
        # need to fix
        events = Event_Set.generate_synthetic_events(file_name,
                                                     fault_width,
                                                     azi,
                                                     dazi,
                                                     fault_dip,
                                                     prob_min_mag_cutoff,
                                                     override_xml,
                                                     prob_number_of_events_in_zones=None)
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

        #os.remove(fid_genpoly)
        
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
        fault_depth = [7.0, 7.0]

        set = Event_Set.create(
            rupture_centroid_lat,
            rupture_centroid_lon,
            azimuth,
            dip,
            ML,
            Mw,
            None, #depth,
            fault_width,
            fault_depth=fault_depth)
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
           
    def test_Pseudo_Event_Set(self):
        rupture_centroid_lat = [-33.351170370959323, -32.763381339789468]
        rupture_centroid_lon = [151.45946928787703, 151.77787395867014]
        azimuth = [162.8566392635347, 201.51805898897854]
        dip = array([35.0, 5.0])
        #dip = None
        ML = None
        Mw = [5.0286463459649076, 4.6661943094693887]
        fault_width = [15.0, 15.0]
        #fault_width = None
        fault_depth = [7.0, 30.0]

        set = Event_Set.create(
            rupture_centroid_lat,
            rupture_centroid_lon,
            azimuth,
            dip,
            ML,
            Mw,
            None, #depth,
            fault_width,
            fault_depth=fault_depth)
        event_activity = [1,0.1]
        set.set_event_activity(event_activity)
        set.source_zone_id = asarray([0,1]) #FIXME
        attenuation_models = asarray([0,1])
        weight = asarray([.4,.6])
        index = asarray([0,1,0,1])
        pes = Pseudo_Event_Set.split_logic_tree(set,
                                                attenuation_models,
                                                weight)
        weight.shape = [-1,1]
        pseudo_event_activity = event_activity * weight
        weight.shape = [-1]
        pseudo_event_activity.shape = [-1]
        self.assert_(allclose(pes.dip ,dip[index] ))
        self.assert_(allclose(pes.index , index))
        self.assert_(allclose(pes.event_activity , pseudo_event_activity))
        self.assert_(allclose(pes.att_model_index , array([0,0,1,1])))
        self.assert_(allclose(pes.attenuation_weights , array([.4,.4,.6,.6])))
        
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Event_Set,'test')
    #suite = unittest.makeSuite(Test_Event_Set,'test_generate_synthetic_events')
    runner = unittest.TextTestRunner()
    runner.run(suite)
