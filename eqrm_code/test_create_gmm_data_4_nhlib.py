import os
#import sys
#import string
import unittest
import tempfile
import csv

import eqrm_code.create_gmm_data_4_nhlib as cgd


"""
Test 
"""

class Test_create_gmm_data_4_nhlib(unittest.TestCase):
    def test_write_gmm_data_file(self):
        if os.name == 'mac': 
            return
        (handle, file_name) = tempfile.mkstemp('.csv', 
                                               'test_create_gmm_data_4_nhlibt')
        os.close(handle)

        gmm = 'mean_10_sigma_1' #'Somerville09_Yilgarn'
        mag = ['rup_mag', [5, 7]]
        dist = ['Rupture', [1.,10.]]
        result_type = 'MEAN'
        periods = [0.0, 0.3, 0.7, 1.0]
        cgd.write_gmm_data_file(gmm, mag, dist, result_type,
                        periods, file_name)
        handle = open(file_name, 'rb')
        reader = csv.reader(handle,  delimiter=',', quoting=csv.QUOTE_NONE)
        row = reader.next()
        string_periods = [str(x) for x in periods[1:]]
        actual = [mag[0], dist[0], 'result_type', 'component_type'] + \
                 string_periods + ['pga'] 
        
        self.assertEqual(row, actual)
        
        # this isn't such a good ground model to use
        # since the coeffiecents/dist/mag values aren't tested
        # exp(10) = 22026.4657948
        # This isn't testing how pga is at the end.
        sa = ['22026.4657948'] * len(periods)
        
        for magi in mag[1]:
            for disti in dist[1]:
                row = reader.next()
                actual = [str(magi), str(disti), 'MEAN', 
                          'AVERAGE_HORIZONTAL'] + sa
                self.assertEqual(row, actual)

        handle.close()
        os.remove(file_name)
           

    def test_write_gmm_data_file_TOTAL_STDDEV(self):
        (handle, file_name) = tempfile.mkstemp('.csv', 
                                               'test_create_gmm_data_4_nhlibt')
        os.close(handle)

        gmm = 'mean_10_sigma_1' #'Somerville09_Yilgarn'
        mag = ['rup_mag', [5, 7]]
        dist = ['Rupture', [1.,10.]]
        result_type = 'TOTAL_STDDEV'
        periods = [0.0, 0.3, 0.7, 1.0]
        cgd.write_gmm_data_file(gmm, mag, dist, result_type,
                        periods, file_name)
        handle = open(file_name, 'rb')
        reader = csv.reader(handle,  delimiter=',', quoting=csv.QUOTE_NONE)
        row = reader.next()
        string_periods = [str(x) for x in periods[1:]]
        actual = [mag[0], dist[0], 'result_type', 'component_type'] + \
                 string_periods + ['pga'] 
        
        self.assertEqual(row, actual)
        
        # this isn't such a good ground model to use
        # since the coeffiecents/dist/mag values aren't tested
        # This isn't testing how pga is at the end.
        sa = ['1.0'] * len(periods)
        
        for magi in mag[1]:
            for disti in dist[1]:
                row = reader.next()
                actual = [str(magi), str(disti), 'TOTAL_STDDEV', 
                          'AVERAGE_HORIZONTAL'] + sa
                self.assertEqual(row, actual)

        handle.close()
        os.remove(file_name)
           
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_create_gmm_data_4_nhlib,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
