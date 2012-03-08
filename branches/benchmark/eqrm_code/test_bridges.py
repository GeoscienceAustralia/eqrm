#!/usr/bin/env python

"""Testing for the bridges.py module."""


import os
import sys
import unittest
import tempfile
import scipy
import pprint

import bridges

from eqrm_code import perf


class Test_Bridges(unittest.TestCase):

    def setUp(self):
        """Create test file for testing."""

        self.pp = pprint.PrettyPrinter(indent=4, depth=10, width=80)

        self.lat = [-35.352085, -35.348677, -35.336884, -35.345209,
                    -35.340859, -35.301472, -35.293012, -35.320122]
        self.lon = [149.236994, 149.239383, 149.241625, 149.205986,
                    149.163037, 149.141364, 149.126767, 149.063810]
        self.clsf = ['HWB17', 'HWB17', 'HWB17', 'HWB22',
                      'HWB3', 'HWB17', 'HWB10', 'HWB28']
        self.cat = ['BRIDGE', 'BRIDGE', 'BRIDGE', 'BRIDGE',
                    'BRIDGE', 'BRIDGE', 'BRIDGE', 'BRIDGE']
        self.skew = [0, 32, 20, 4, 0, 0, 12, 0]
        self.span = [2, 3, 6, 2, 1, 1, 3, 3]
        self.cls = ['E', 'F', 'G', 'D', 'E', 'F', 'G', 'C']
        dummy_csv_data = ['BID,LONGITUDE,LATITUDE,STRUCTURE_CLASSIFICATION,'
                          'STRUCTURE_CATEGORY,SKEW,SPAN,SITE_CLASS',
                          '2,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (self.lon[0], self.lat[0], self.clsf[0],
                                 self.cat[0], self.skew[0], self.span[0],
                                 self.cls[0]),
                          '3,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (self.lon[1], self.lat[1], self.clsf[1],
                                 self.cat[1], self.skew[1], self.span[1],
                                 self.cls[1]),
                          '4,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (self.lon[2], self.lat[2], self.clsf[2],
                                 self.cat[2], self.skew[2], self.span[2],
                                 self.cls[2]),
                          '5,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (self.lon[3], self.lat[3], self.clsf[3],
                                 self.cat[3], self.skew[3], self.span[3],
                                 self.cls[3]),
                          '6,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (self.lon[4], self.lat[4], self.clsf[4],
                                 self.cat[4], self.skew[4], self.span[4],
                                 self.cls[4]),
                          '7,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (self.lon[5], self.lat[5], self.clsf[5],
                                 self.cat[5], self.skew[5], self.span[5],
                                 self.cls[5]),
                          '8,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (self.lon[6], self.lat[6], self.clsf[6],
                                 self.cat[6], self.skew[6], self.span[6],
                                 self.cls[6]),
                          '9,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (self.lon[7], self.lat[7], self.clsf[7],
                                 self.cat[7], self.skew[7], self.span[7],
                                 self.cls[7])]
        self.columns = {'BID': int,
                        'LONGITUDE': float,
                        'LATITUDE': float,
                        'STRUCTURE_CLASSIFICATION': str,
                        'STRUCTURE_CATEGORY': str,
                        'SKEW': float,
                        'SPAN': int,
                        'SITE_CLASS': str}

        (handle, self.file_name) = tempfile.mkstemp('.csv', 'test_bridges_')
        os.close(handle)

        f = open(self.file_name, 'wb')
        f.write('\n'.join(dummy_csv_data))
        f.close()

        self.def_indir = os.path.basename(self.file_name)

    def tearDown(self):
        """Remove the temporary file!"""

        os.remove(self.file_name)

    @perf.benchmark
    def test_load(self):
        """Test initial load of Bridges object."""

        b = bridges.Bridges.from_csv(self.file_name, **self.columns)

        actual = scipy.array(self.lat)
        b_lat_str = self.pp.pformat(b.latitude)
        actual_str = self.pp.pformat(actual)
        msg = ('b.latitude != actual\n'
               '(%s !=\n%s)'
               % (b_lat_str, actual_str))
        self.assert_(scipy.allclose(b.latitude, actual, 0.001), msg)

        actual = scipy.array(self.lon)
        b_lon_str = self.pp.pformat(b.longitude)
        actual_str = self.pp.pformat(actual)
        msg = ('b.longitude != actual\n'
               '(%s !=\n%s)'
               % (b_lon_str, actual_str))
        self.assert_(scipy.allclose(b.longitude, actual, 0.001))

        actual = scipy.array(['E', 'F', 'G', 'D', 'E', 'F', 'G', 'C'])
        for (att, act) in map(None, b.attributes['SITE_CLASS'], actual):
            msg = ('Expected attribute == actual (got %s == %s)'
                   % (str(att), str(act)))
            self.failUnlessEqual(att, act, msg)

        actual = scipy.array([0, 32, 20, 4, 0, 0, 12, 0])
        for (att, act) in map(None, b.attributes['SKEW'], actual):
            msg = ('Expected attribute == actual (got %s == %s)'
                   % (str(att), str(act)))
            self.failUnlessEqual(att, act, msg)

        actual = scipy.array([2, 3, 4, 5, 6, 7, 8, 9])
        for (att, act) in map(None, b.attributes['BID'], actual):
            msg = ('Expected attribute == actual (got %s == %s)'
                   % (str(att), str(act)))
            self.failUnlessEqual(att, act, msg)

    @perf.benchmark
    def test_get_item(self):
        """Test the __getitem__() method of Bridges object."""

        b = bridges.Bridges.from_csv(self.file_name, **self.columns)

        # test some indexing of a Bridges object
        for i in range(len(b.longitude)):
            i_msg = 'i=%d' % i

            slice = b[i]

            msg = ('%s: self.lon[i] (%s) != slice.longitude (%s)'
                   % (i_msg, str(self.lon[i]), str(slice.longitude)))
            self.failUnlessEqual(self.lon[i], slice.longitude, msg)

            msg = ('%s: self.lat[i] (%s) != slice.latitude (%s)'
                   % (i_msg, str(self.lat[i]), str(slice.latitude)))
            self.failUnlessEqual(self.lat[i], slice.latitude, msg)

            msg = ("%s: self.clsf[i] (%s) != "
                   "slice.attributes['STRUCTURE_CLASSIFICATION'] (%s)"
                   % (i_msg, str(self.clsf[i]),
                      str(slice.attributes['STRUCTURE_CLASSIFICATION'])))
            self.failUnlessEqual(self.clsf[i],
                                 slice.attributes['STRUCTURE_CLASSIFICATION'],
                                 msg)

            msg = ("%s: self.cat[i] (%s) != "
                   "slice.attributes['STRUCTURE_CATEGORY'] (%s)"
                   % (i_msg, str(self.cat[i]),
                      str(slice.attributes['STRUCTURE_CATEGORY'])))
            self.failUnlessEqual(self.cat[i],
                                 slice.attributes['STRUCTURE_CATEGORY'],
                                 msg)

            msg = ("%s: self.skew[i] (%s) != slice.attributes['SKEW'] (%s)"
                   % (i_msg, str(self.skew[i]), str(slice.attributes['SKEW'])))
            self.failUnlessEqual(self.skew[i], slice.attributes['SKEW'], msg)

            msg = ("%s: self.span[i] (%s) != slice.attributes['SPAN'] (%s)"
                   % (i_msg, str(self.span[i]), str(slice.attributes['SPAN'])))
            self.failUnlessEqual(self.span[i], slice.attributes['SPAN'], msg)

            msg = ("%s: self.cls[i] (%s) != slice.attributes['SITE_CLASS'] (%s)"
                   % (i_msg, str(self.cls[i]),
                      str(slice.attributes['SITE_CLASS'])))
            self.failUnlessEqual(self.cls[i],
                                 slice.attributes['SITE_CLASS'], msg)

################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Bridges,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)

