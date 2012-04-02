#!/usr/bin/env python

'''Test the utility get_extent module.'''

import os
import sys
import unittest
import random
import tempfile
import shutil

import util_get_extent as ge


class TestGetExtent(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_NE(self):
        """Test of get_extent() for points in NE quadrant."""

        # generate some data
        outputdir = tempfile.mkdtemp(prefix='test_get_extent_')

        # data for NE quadrant and expected result
        test_file = 'quadrant_NE.txt'
        data_file = os.path.join(outputdir, test_file)
        fd = open(data_file, 'w')
        fd.write('''10.0,15.0       # lon, lat
10.0,25.0
20.0,15.0
20.0,25.0
''')
        fd.close()

        # (ll_lat, ll_lon, ur_lat, ur_lon)
        expected = (15.0, 10.0, 25.0, 20.0)

        # call get_extent()
        result = ge.get_extent(data_file, margin=0.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # now try same data with a 5.0 percent of the width margin
        # (ll_lat, ll_lon, ur_lat, ur_lon)
        margin = 5.0
        (ll_lat, ll_lon, ur_lat, ur_lon) = expected
        x_margin = abs(ur_lon - ll_lon) * margin/100.0
        y_margin = abs(ur_lat - ll_lat) * margin/100.0

        ll_lon -= x_margin
        ur_lon += x_margin
        ll_lat -= y_margin
        ur_lat += y_margin

        expected = (ll_lat, ll_lon, ur_lat, ur_lon)

        # call get_extent()
        result = ge.get_extent(data_file, margin=5.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

    def test_NW(self):
        """Test of get_extent() for points in NW quadrant."""

        # generate some data
        outputdir = tempfile.mkdtemp(prefix='test_get_extent_')

        # data for NW quadrant and expected result
        test_file = 'quadrant_NW.txt'
        data_file = os.path.join(outputdir, test_file)
        fd = open(data_file, 'w')
        fd.write('''-10.0,2.0       # lon, lat
-8.0,12.0
-4.0,1.0
-2.0,10.0
''')
        fd.close()

        # (ll_lat, ll_lon, ur_lat, ur_lon)
        expected = (1.0, -10.0, 12.0, -2.0)

        # call get_extent()
        result = ge.get_extent(data_file, margin=0.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # now try same data with a 5.0 percent of the width margin
        # (ll_lat, ll_lon, ur_lat, ur_lon)
        margin = 5.0
        (ll_lat, ll_lon, ur_lat, ur_lon) = expected
        x_margin = abs(ur_lon - ll_lon) * margin/100.0
        y_margin = abs(ur_lat - ll_lat) * margin/100.0

        ll_lon -= x_margin
        ur_lon += x_margin
        ll_lat -= y_margin
        ur_lat += y_margin

        expected = (ll_lat, ll_lon, ur_lat, ur_lon)

        # call get_extent()
        result = ge.get_extent(data_file, margin=5.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

    def test_SW(self):
        """Test of get_extent() for points in SW quadrant."""

        # generate some data
        outputdir = tempfile.mkdtemp(prefix='test_get_extent_')

        # data for NW quadrant and expected result
        test_file = 'quadrant_NW.txt'
        data_file = os.path.join(outputdir, test_file)
        fd = open(data_file, 'w')
        fd.write('''-13.0,-5.0       # lon, lat
-3.0,-5.0
-3.0,-10.0
-13.0,-10.0
''')
        fd.close()

        # (ll_lat, ll_lon, ur_lat, ur_lon)
        expected = (-10.0, -13.0, -5.0, -3.0)

        # call get_extent()
        result = ge.get_extent(data_file, margin=0.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # now try same data with a 5.0 percent of the width margin
        # (ll_lat, ll_lon, ur_lat, ur_lon)
        margin = 5.0
        (ll_lat, ll_lon, ur_lat, ur_lon) = expected
        x_margin = abs(ur_lon - ll_lon) * margin/100.0
        y_margin = abs(ur_lat - ll_lat) * margin/100.0

        ll_lon -= x_margin
        ur_lon += x_margin
        ll_lat -= y_margin
        ur_lat += y_margin

        expected = (ll_lat, ll_lon, ur_lat, ur_lon)

        # call get_extent()
        result = ge.get_extent(data_file, margin=5.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

    def test_SE(self):
        """Test of get_extent() for points in SE quadrant."""

        # generate some data
        outputdir = tempfile.mkdtemp(prefix='test_get_extent_')

        # data for NW quadrant and expected result
        test_file = 'quadrant_NW.txt'
        data_file = os.path.join(outputdir, test_file)
        fd = open(data_file, 'w')
        fd.write('''2.0,-1.0       # lon, lat
2.0,-4.0
3.0,-1.0
3.0,-4.0
''')
        fd.close()

        # (ll_lat, ll_lon, ur_lat, ur_lon)
        expected = (-4.0, 2.0, -1.0, 3.0)

        # call get_extent()
        result = ge.get_extent(data_file, margin=0.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # now try same data with a 5.0 percent of the width margin
        # (ll_lat, ll_lon, ur_lat, ur_lon)
        margin = 5.0
        (ll_lat, ll_lon, ur_lat, ur_lon) = expected
        x_margin = abs(ur_lon - ll_lon) * margin/100.0
        y_margin = abs(ur_lat - ll_lat) * margin/100.0

        ll_lon -= x_margin
        ur_lon += x_margin
        ll_lat -= y_margin
        ur_lat += y_margin

        expected = (ll_lat, ll_lon, ur_lat, ur_lon)

        # call get_extent()
        result = ge.get_extent(data_file, margin=5.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

    def test_NE_NW(self):
        """Test of get_extent() for points straddling NE+NW quadrants."""

        # generate some data
        outputdir = tempfile.mkdtemp(prefix='test_get_extent_')

        # data for NW quadrant and expected result
        test_file = 'quadrant_NW.txt'
        data_file = os.path.join(outputdir, test_file)
        fd = open(data_file, 'w')
        fd.write('''-10.0,10.0       # lon, lat
1.0,5.0
-1.0,20.0
10.0,15.0
''')
        fd.close()

        # (ll_lat, ll_lon, ur_lat, ur_lon)
        expected = (5.0, -10.0, 20.0, 10.0)

        # call get_extent()
        result = ge.get_extent(data_file, margin=0.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # now try same data with a 5.0 percent of the width margin
        # (ll_lat, ll_lon, ur_lat, ur_lon)
        margin = 5.0
        (ll_lat, ll_lon, ur_lat, ur_lon) = expected
        x_margin = abs(ur_lon - ll_lon) * margin/100.0
        y_margin = abs(ur_lat - ll_lat) * margin/100.0

        ll_lon -= x_margin
        ur_lon += x_margin
        ll_lat -= y_margin
        ur_lat += y_margin

        expected = (ll_lat, ll_lon, ur_lat, ur_lon)

        # call get_extent()
        result = ge.get_extent(data_file, margin=5.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

    def test_NW_SW(self):
        """Test of get_extent() for points straddling NW+SW quadrants."""

        # generate some data
        outputdir = tempfile.mkdtemp(prefix='test_get_extent_')

        # data for NW quadrant and expected result
        test_file = 'quadrant_NW.txt'
        data_file = os.path.join(outputdir, test_file)
        fd = open(data_file, 'w')
        fd.write('''-5.0,-7.0       # lon, lat
-4.0,1.0
-2.0,-3.0
-1.0,6.0
''')
        fd.close()

        # (ll_lat, ll_lon, ur_lat, ur_lon)
        expected = (-7.0, -5.0, 6.0, -1.0)

        # call get_extent()
        result = ge.get_extent(data_file, margin=0.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # now try same data with a 5.0 percent of the width margin
        # (ll_lat, ll_lon, ur_lat, ur_lon)
        margin = 5.0
        (ll_lat, ll_lon, ur_lat, ur_lon) = expected
        x_margin = abs(ur_lon - ll_lon) * margin/100.0
        y_margin = abs(ur_lat - ll_lat) * margin/100.0

        ll_lon -= x_margin
        ur_lon += x_margin
        ll_lat -= y_margin
        ur_lat += y_margin

        expected = (ll_lat, ll_lon, ur_lat, ur_lon)

        # call get_extent()
        result = ge.get_extent(data_file, margin=5.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

    def test_SW_SE(self):
        """Test of get_extent() for points straddling SW+SE quadrants."""

        # generate some data
        outputdir = tempfile.mkdtemp(prefix='test_get_extent_')

        # data for NW quadrant and expected result
        test_file = 'quadrant_NW.txt'
        data_file = os.path.join(outputdir, test_file)
        fd = open(data_file, 'w')
        fd.write('''-4.0,-5.0       # lon, lat
-1.0,-2.0
1.0,-6.0
3.0,-3.0
''')
        fd.close()

        # (ll_lat, ll_lon, ur_lat, ur_lon)
        expected = (-6.0, -4.0, -2.0, 3.0)

        # call get_extent()
        result = ge.get_extent(data_file, margin=0.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # now try same data with a 5.0 percent of the width margin
        # (ll_lat, ll_lon, ur_lat, ur_lon)
        margin = 5.0
        (ll_lat, ll_lon, ur_lat, ur_lon) = expected
        x_margin = abs(ur_lon - ll_lon) * margin/100.0
        y_margin = abs(ur_lat - ll_lat) * margin/100.0

        ll_lon -= x_margin
        ur_lon += x_margin
        ll_lat -= y_margin
        ur_lat += y_margin

        expected = (ll_lat, ll_lon, ur_lat, ur_lon)

        # call get_extent()
        result = ge.get_extent(data_file, margin=5.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

    def test_SE_NE(self):
        """Test of get_extent() for points straddling SE+NE quadrants."""

        # generate some data
        outputdir = tempfile.mkdtemp(prefix='test_get_extent_')

        # data for NW quadrant and expected result
        test_file = 'quadrant_NW.txt'
        data_file = os.path.join(outputdir, test_file)
        fd = open(data_file, 'w')
        fd.write('''2.0,1.0       # lon, lat
4.0,-4.0
5.0,3.0
7.0,0.5
''')
        fd.close()

        # (ll_lat, ll_lon, ur_lat, ur_lon)
        expected = (-4.0, 2.0, 3.0, 7.0)

        # call get_extent()
        result = ge.get_extent(data_file, margin=0.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # now try same data with a 5.0 percent of the width margin
        # (ll_lat, ll_lon, ur_lat, ur_lon)
        margin = 5.0
        (ll_lat, ll_lon, ur_lat, ur_lon) = expected
        x_margin = abs(ur_lon - ll_lon) * margin/100.0
        y_margin = abs(ur_lat - ll_lat) * margin/100.0

        ll_lon -= x_margin
        ur_lon += x_margin
        ll_lat -= y_margin
        ur_lat += y_margin

        expected = (ll_lat, ll_lon, ur_lat, ur_lon)

        # call get_extent()
        result = ge.get_extent(data_file, margin=5.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

    def test_centre(self):
        """Test of get_extent() for points straddling the origin."""

        # generate some data
        outputdir = tempfile.mkdtemp(prefix='test_get_extent_')

        # data for NW quadrant and expected result
        test_file = 'quadrant_NW.txt'
        data_file = os.path.join(outputdir, test_file)
        fd = open(data_file, 'w')
        fd.write('''-3.0,5.0       # lon, lat
-2.0,-5.0
3.0,6.0
4.0,-4.0
''')
        fd.close()

        # (ll_lat, ll_lon, ur_lat, ur_lon)
        expected = (-5.0, -3.0, 6.0, 4.0)

        # call get_extent()
        result = ge.get_extent(data_file, margin=0.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # now try same data with a 5.0 percent of the width margin
        # (ll_lat, ll_lon, ur_lat, ur_lon)
        margin = 5.0
        (ll_lat, ll_lon, ur_lat, ur_lon) = expected
        x_margin = abs(ur_lon - ll_lon) * margin/100.0
        y_margin = abs(ur_lat - ll_lat) * margin/100.0

        ll_lon -= x_margin
        ur_lon += x_margin
        ll_lat -= y_margin
        ur_lat += y_margin

        expected = (ll_lat, ll_lon, ur_lat, ur_lon)

        # call get_extent()
        result = ge.get_extent(data_file, margin=5.0)

        # ensure file expected was generated
        self.failUnless(result == expected)

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

         
if __name__ == '__main__':
    unittest.main()
