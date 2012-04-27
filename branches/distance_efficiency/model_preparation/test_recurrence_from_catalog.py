"""
test_catalogue_reader.py
Test the catalogue reader script

Jonathan Griffin
Australia-Indonesia Facility for Disaster Reduction
April 2012
"""

import sys,os
import unittest
import catalogue_reader
from recurrence_from_catalog import calc_recurrence
import datetime
import numpy
#import tempfile
from earthquake_event import EarthquakeEvent, EventSet


class Test_catalogue_reader(unittest.TestCase):
 
    def setUp(self):
        pass
        
    def tearDown(self):
        pass     


    def test_recurrence_from_catalog(self):
        # don't test if DISPLAY environment variable undefined
        if sys.platform != 'win32':
            try:
                display = os.environ['DISPLAY']
            except KeyError:
                return

        ###################################################################
        # Generate test data
        ###################################################################
        fours=numpy.ones(81683)*4.0
        fives=numpy.ones(21683)*5.0
        sixes=numpy.ones(1260)*6.0
        sevens=numpy.ones(98)*7.0
        eights=numpy.ones(7)*8.0
        nines=numpy.ones(1)*9.0
        magnitudes = numpy.concatenate([fours, fives, sixes, sevens, eights, nines])
        latitude = 0.0
        longitude = 0.0
        time=datetime.datetime(2010,1,1,0,0,0)
        event_list = []
        for magnitude in magnitudes:
            event = EarthquakeEvent(latitude, longitude, magnitude, time)
            event_list.append(event)
        # change year of first event to give a range of date
        event_list[0].time=datetime.datetime(2000,1,1,0,0,0)
        pass
        event_set = EventSet(event_list)

        ###################################################################
        # Expected results (generated manually)
        ###################################################################

        b_least_squares_test = -1.0454065177746481
        a_least_squares_test = 8.3695720382963614
        b_mle_test = 1.8542409163755169
        annual_num_eq_test = 10473.2


        ##################################################################
        # Test recurrence calulation
        #a, b, b_mle, annual_num_eq = calc_recurrence(event_set, min_mag=5.5, interval=0.5)
        a, b, b_mle, annual_num_eq = calc_recurrence(event_set, interval=1.0)

        msg = a_least_squares_test, a
        assert numpy.allclose(a_least_squares_test, a, rtol=1e-15), msg
        msg = b_least_squares_test, b
        assert numpy.allclose(b_least_squares_test, b, rtol=1e-15), msg
        msg = b_mle_test, b_mle
        assert numpy.allclose(b_mle_test, b_mle, rtol=1e-15), msg
        msg = annual_num_eq_test, annual_num_eq
        assert numpy.allclose(annual_num_eq_test, annual_num_eq, rtol=1e-15), msg        

if __name__ == '__main__':
    suite = unittest.makeSuite(Test_catalogue_reader, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
