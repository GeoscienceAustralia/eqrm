"""
test_catalogue_reader.py
Test the catalogue reader script
"""

import sys,os
import unittest
import catalogue_reader
import datetime
#import tempfile
from earthquake_event import EarthquakeEvent, EventSet


class Test_catalogue_reader(unittest.TestCase):
 
    def setUp(self):
        pass
        
    def tearDown(self):
        pass     


    def test_catalogue_reader(self):

        ################################################################################
        # Test nordic format
        ################################################################################
        # Generate test data
        test_data = [' 1971 0126 2022 33.0 L   0.575 122.447192.0             5.3WCNV 5.2bNEI        1',
                     ' 1971 0308 1922 32.9 L   0.902 124.425171.0             5.0WCNV 4.9bNEI        1',
                     ' 1971 0326 1134 34.5 L  -0.628 121.688 36.0             6.2WCNV 4.9bNEI        1',
                     ' 1971 0326 2400 00.0 L  -0.628 121.688 36.0             6.2WCNV 4.9bNEI        1']

        test_event_list = [EarthquakeEvent(122.447, 0.575, 5.3, datetime.datetime(1971, 1, 26, 20, 22, 33, 0), depth = 192.0, mag_type = 'W'),
                           EarthquakeEvent(124.425, 0.902, 5.0, datetime.datetime(1971, 3, 8, 19, 22, 32, int(9e5)), depth = 171.0, mag_type = 'W'),
                           EarthquakeEvent(121.688, -0.628, 6.2, datetime.datetime(1971, 3, 26, 11, 34, 34, int(5e5)), depth = 36.0, mag_type = 'W'),
                           EarthquakeEvent(121.688, -0.628, 6.2, datetime.datetime(1971, 3, 26, 23, 59, 59, 999999), depth = 36.0, mag_type = 'W')]
        test_event_set = EventSet(test_event_list)

        
        # Write test file
        test_file = './test.nordic'
        f_out = open(test_file, 'w')
        for i in test_data:
            f_out.write(i + '\n')
        f_out.close()
        
        read_catalogue = catalogue_reader.CatalogueReader(test_file).EventSet

        i = 0
        for event in read_catalogue.catalogue_subset['all']:
            msg = event.lon, test_event_list[i].lon
            assert event.lon == test_event_list[i].lon, msg
            msg = event.lat, test_event_list[i].lat
            assert event.lat == test_event_list[i].lat, msg
            msg = event.magnitude, test_event_list[i].magnitude
            assert event.magnitude == test_event_list[i].magnitude, msg
            msg = event.time, test_event_list[i].time
            assert event.time == test_event_list[i].time, msg
            msg = event.depth, test_event_list[i].depth
            assert event.depth == test_event_list[i].depth, msg
            msg = event.mag_type, test_event_list[i].mag_type
            assert event.mag_type == test_event_list[i].mag_type, msg                 
            i+=1

        # remove test_file and data
        os.remove(test_file)
        del(read_catalogue)
        
        ################################################################################
        # Test Engdahl csv format
        ################################################################################
        test_data = ['Longitude,Latitude,Year,Month,Day,Magnitude,Depth,Hour,Minute',
                     '128.101,-7.404,1963,2,14,6.6,180,7,4',
                     '144.625,-4.9,1963,2,14,6.4,65.1,22,7',
                     '149.233,-6.057,1963,2,27,6.4,35,4,30']

        test_event_list = [EarthquakeEvent(128.101, -7.404, 6.6, datetime.datetime(1963, 2, 14, 7, 4), depth = 180.0),
                           EarthquakeEvent(144.625, -4.9, 6.4, datetime.datetime(1963, 2, 14, 22, 7), depth = 65.1),
                           EarthquakeEvent(149.233, -6.057, 6.4, datetime.datetime(1963, 2, 27, 4, 30), depth = 35.0)]
        test_event_set = EventSet(test_event_list)

        # Write test file
        test_file = './test.csv'
        f_out = open(test_file, 'w')
        for i in test_data:
            f_out.write(i + '\n')
        f_out.close()

        read_catalogue = catalogue_reader.CatalogueReader(test_file).EventSet

        i = 0
        for event in read_catalogue.catalogue_subset['all']:
            msg = event.lon, test_event_list[i].lon
            assert event.lon == test_event_list[i].lon, msg
            msg = event.lat, test_event_list[i].lat
            assert event.lat == test_event_list[i].lat, msg
            msg = event.magnitude, test_event_list[i].magnitude
            assert event.magnitude == test_event_list[i].magnitude, msg
            msg = event.time, test_event_list[i].time
            assert event.time == test_event_list[i].time, msg
            msg = event.depth, test_event_list[i].depth
            assert event.depth == test_event_list[i].depth, msg
            msg = event.mag_type, test_event_list[i].mag_type
            assert event.mag_type == test_event_list[i].mag_type, msg                 
            i+=1

        # remove test_file
        os.remove(test_file)

        
if __name__ == '__main__':
    suite = unittest.makeSuite(Test_catalogue_reader, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
