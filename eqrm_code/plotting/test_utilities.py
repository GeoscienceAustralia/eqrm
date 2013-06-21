#!/usr/bin/env python

"""Test the utilities module."""

import os
import sys
import re
import unittest
import tempfile
import shutil
import math
import scipy
import numpy as num

import utilities as util
import eqrm_code.eqrm_filesystem as ef


class TestUtilities(unittest.TestCase):

    def test_get_unique_key(self):
        # define a test dictionary
        test_dict = {'alpha': 1,
                     'beta': 2,
                     'gamma': 3,
                     'delta': 4,
                     'del': 5,
                     'd': 6}

        # first test, no match at all
        result = util.get_unique_key(test_dict, 'xyzzy')
        self.failUnless(result is None)

        # find given complete unique key
        result = util.get_unique_key(test_dict, 'alpha')
        self.failUnless(result == 'alpha')

        # find given short but unique key
        result = util.get_unique_key(test_dict, 'alph')
        self.failUnless(result == 'alpha')
        result = util.get_unique_key(test_dict, 'alp')
        self.failUnless(result == 'alpha')
        result = util.get_unique_key(test_dict, 'al')
        self.failUnless(result == 'alpha')
        result = util.get_unique_key(test_dict, 'a')
        self.failUnless(result == 'alpha')

        # make sure we don't match on non-unique query
        result = util.get_unique_key(test_dict, 'del')
        self.failUnless(result is None)

        # ensure we match on short unique query when other matching prefixes
        result = util.get_unique_key(test_dict, 'delt')
        self.failUnless(result == 'delta')

        # do match on 'last' key in dictionary (bug found)
        last_key = test_dict.keys()[-1]
        result = util.get_unique_key(test_dict, last_key)
        self.failUnless(result == last_key)

    def test_make_discrete_cpt(self):
        """
        Test the make_discrete_cpt() function that makes discrete CPT files.
        """

        # need a temporary working directory
        tmp_dir = tempfile.mkdtemp(prefix='test_utilities_')

        # simple test
        filename = os.path.join(tmp_dir, 'test.cpt')
        colourmap = util.get_colourmap('hazmap')
        seq = [0.0, 1.0, 2.0, 4.0, 8.0]
        if sys.platform == 'win32':
            expected = [
                ['0.00', '32', '255', '0', '1.00', '32', '255', '0'],
                ['1.00', '96', '255', '0', '2.00', '96', '255', '0'],
                ['2.00', '191', '255', '0', '4.00', '191', '255', '0'],
                ['4.00', '255', '128', '0', '8.00', '255', '128', '0'],
                ['B', '0', '255', '0'],
                ['F', '255', '0', '0'],
                ['N', '255', '255', '255']
            ]
        else:
            expected = [
                ['0.00', '32', '255', '0', '1.00', '32', '255', '0'],
                ['1.00', '96', '255', '0', '2.00', '96', '255', '0'],
                ['2.00', '191', '255', '0', '4.00', '191', '255', '0'],
                ['4.00', '255', '127', '0', '8.00', '255', '127', '0'],
                ['B', '0', '255', '0'],
                ['F', '255', '0', '0'],
                ['N', '255', '255', '255']
            ]

        util.make_discrete_cpt(filename, colourmap, seq)

        # check resultant file
        fd = open(filename, 'r')
        lines = fd.readlines()
        fd.close()

        split_pattern = re.compile('[ |\t]+')
        generated = []
        for l in lines:
            l = l.strip()
            if l[0] == '#':
                continue

            generated.append(split_pattern.split(l))

        # delete the temporary directory
        shutil.rmtree(tmp_dir)

        msg = 'expected=\n%s\ngenerated=\n%s' % (str(expected), str(generated))
        self.failUnless(expected == generated, msg)

    def test_make_discrete_cpt_from_seq(self):
        # need a temporary working directory
        tmp_dir = tempfile.mkdtemp(prefix='test_utilities_')

        # create very simple CPT file
        cpt_file = os.path.join(tmp_dir, 'test.dat')
        seq = [0, 1, 2]
        util.make_discrete_cpt_from_seq(cpt_file, seq)

        # check generated file against what we expect
        # first colour is 2/3 of way to middle yellow, etc
        expected = [['0.000000', '170', '255', '000', '1.000000', '170',
                     '255', '000'],
                    ['1.000000', '255', '171', '000', '2.000000', '255',
                     '171', '000'],
                    ['B', '0', '255', '0'],
                    ['F', '255', '0', '0'],
                    ['N', '-']]

        # get regular expression to parse line delimited by whitespace
        split_pattern = re.compile('[ |\t]+')

        fd = open(cpt_file, 'r')
        lines = fd.readlines()
        fd.close()

        generated = []
        for l in lines:
            l = l.strip()
            if l[0] == '#':
                continue

            generated.append(split_pattern.split(l))

        self.failUnless(expected == generated)

        # create another simple CPT file
        seq = [0, 1, 2, 3]
        util.make_discrete_cpt_from_seq(cpt_file, seq)

        # check generated file against what we expect
        # each colour range starts at 1/2 of red/green half
        expected = [['0.000000', '128', '255', '000', '1.000000', '128',
                     '255', '000'],
                    ['1.000000', '255', '255', '000', '2.000000', '255',
                     '255', '000'],
                    ['2.000000', '255', '127', '000', '3.000000', '255',
                     '127', '000'],
                    ['B', '0', '255', '0'],
                    ['F', '255', '0', '0'],
                    ['N', '-']]

        # get regular expression to parse line delimited by whitespace
        split_pattern = re.compile('[ |\t]+')

        fd = open(cpt_file, 'r')
        lines = fd.readlines()
        fd.close()

        generated = []
        for l in lines:
            l = l.strip()
            if l[0] == '#':
                continue

            generated.append(split_pattern.split(l))

        self.failUnless(expected == generated)

        # delete the temporary directory
        shutil.rmtree(tmp_dir)

    def test_get_xyz_bin_inc(self):
        # define small allowable difference
        places = 6      # number of decimal places
        epsilon = eval('1.0e-%d' % places)

        # first test, no discernible binning
        xyz = [(1, 2, 3), (2, 3, 4), (5, 1, 2)]
        inc = util.get_xyz_bin_inc(xyz, epsilon=epsilon)
        self.failUnless(inc is None)

        # first test, no discernible binning of scipy.array()
        xyz = scipy.array([(1, 2, 3), (2, 3, 4), (5, 1, 2)])
        inc = util.get_xyz_bin_inc(xyz, epsilon=epsilon)
        self.failUnless(inc is None)

        # now a test that should show data is binned (0.5, 0.6)
        xyz = [(1.0, 1.0, 0.0),
               (1.0, 1.6, 0.1),
               (1.0, 2.2, 0.2),
               (1.5, 1.0, 1.0),
               (1.5, 1.6, 1.1),
               (1.5, 2.2, 1.2),
               (2.0, 1.0, 2.0),
               (2.0, 1.6, 2.1),
               (2.0, 2.2, 2.2)]
        n = util.get_xyz_bin_inc(xyz, epsilon=epsilon)
        self.failIf(n is None)
        (x_num, y_num) = n
        self.failUnlessEqual(x_num, 3)
        self.failUnlessEqual(y_num, 3)

        # as above, but use scipy.array()
        xyz = scipy.array([(1.0, 1.0, 0.0),
                           (1.0, 1.6, 0.1),
                           (1.0, 2.2, 0.2),
                           (1.5, 1.0, 1.0),
                           (1.5, 1.6, 1.1),
                           (1.5, 2.2, 1.2),
                           (2.0, 1.0, 2.0),
                           (2.0, 1.6, 2.1),
                           (2.0, 2.2, 2.2)])
        n = util.get_xyz_bin_inc(xyz, epsilon=epsilon)
        self.failIf(n is None)
        (x_num, y_num) = n
        self.failUnlessEqual(x_num, 3)
        self.failUnlessEqual(y_num, 3)

        # again as above, but perturb one value by epsilon*10
        delta = epsilon*10
        xyz = scipy.array([(1.0, 1.0, 0.0),
                           (1.0, 1.6, 0.1),
                           (1.0+delta, 2.2, 0.2),
                           (1.5, 1.0, 1.0),
                           (1.5, 1.6, 1.1),
                           (1.5, 2.2, 1.2),
                           (2.0, 1.0, 2.0),
                           (2.0, 1.6, 2.1),
                           (2.0, 2.2, 2.2)])
        n = util.get_xyz_bin_inc(xyz)
        self.failUnless(n is None)

    def test_lat_width(self):
        """Run a few spot checks on util.lat_width()

        width_km = util.lat_width(width_deg, lat)

        Circumference of a spherical earth assumed to be 40075.0km.
        """

        # allowed small difference between expected and actual values
        epsilon = 1.0e-6

        # at equator, 1/4 of circumference
        width_deg = 90.0
        lat = 0.0
        expected_width_km = (40075.0 / 4.0)
        width_km = util.lat_width(width_deg, lat)
        self.failUnless(abs(width_km-expected_width_km) < epsilon)

        # at 45 latitude, 1/4 of circumference, cos(45) = 1/sqrt(2)
        width_deg = 90.0
        lat = 45.0
        expected_width_km = (40075.0 / 4.0) / math.sqrt(2.0)
        width_km = util.lat_width(width_deg, lat)
        self.failUnless(abs(width_km-expected_width_km) < epsilon)

        # at 60 latitude, 1/2 of circumference, cos(60) = 0.5
        width_deg = 180.0
        lat = 60.0
        expected_width_km = (40075.0 / 2.0) * 0.5
        width_km = util.lat_width(width_deg, lat)
        self.failUnless(abs(width_km-expected_width_km) < epsilon)

        # at 70 latitude, 1/2 of circumference, cos(70) = 0.3420201433
        width_deg = 180.0
        lat = 70.0
        expected_width_km = (40075.0 / 2.0) * 0.3420201433
        width_km = util.lat_width(width_deg, lat)
        self.failUnless(abs(width_km-expected_width_km) < epsilon)

        # at 30 latitude, 1/10 of circumference, cos(30) = 0.8660254037
        width_deg = 36.0
        lat = 30.0
        expected_width_km = (40075.0 / 10.0) * 0.8660254037
        width_km = util.lat_width(width_deg, lat)
        self.failUnless(abs(width_km-expected_width_km) < epsilon)

    def test_get_colourmap(self):
        """Test the get_colourmap() function."""

        # unrecognised colourmap name
        self.failUnlessRaises(RuntimeError, util.get_colourmap, 'xyzzy')

        # GMT builtin colormap names, case insensitive
        expected = 'cool'
        got = util.get_colourmap('cool')
        self.failUnlessEqual(got, expected)
        expected = 'cool'
        got = util.get_colourmap('COOL')
        self.failUnlessEqual(got, expected)

        # local name, case insensitive
        expected = 'hazmap.cpt'
        got = util.get_colourmap('hazmap')
        self.failUnlessEqual(os.path.basename(got), expected)
        expected = 'hazmap.cpt'
        got = util.get_colourmap('HazMap')
        self.failUnlessEqual(os.path.basename(got), expected)

    def test_bin_data(self):
        ######
        # First test is small grid, all points inside, one cell empty
        ######

        # define a small 2x3 grid
        gx = 0.0
        gy = 0.0
        gwidx = 1.0
        gwidy = 1.0
        gnumx = 3
        gnumy = 2

        # define points
        #      ^Y
        # 2.0  +-----+-----+-----+
        #      |  0  | 1   |    5|
        #      |     |     |  4  |
        #      |     |   2 |3    |
        # 1.0  +-----+-----+-----+
        #      | 6 7 |10   |     |
        #      |     |     |     |
        #      | 8 9 |     |     |
        # 0.0  +-----+-----+-----+->X
        #      0.0   1.0   2.0   3.0
        #
        # So expected python array (actually, lists of lists) will be:
        #      [[[6,7,8,9],[0]], [[10,11,12,13,14], ...]]
        lon = [0.5, 1.3, 1.7, 2.3, 2.5, 2.7, 0.3, 0.7, 0.3, 0.7, 1.3]
        lat = [1.5, 1.7, 1.3, 1.3, 1.5, 1.7, 0.7, 0.7, 0.3, 0.3, 0.7]

        # expected result for above data
        expected_res = [[{'index': [6, 7, 8, 9], 'mid_lat_lon': (0.5, 0.5)},
                         {'index': [0], 'mid_lat_lon': (1.5, 0.5)}],
                        [{'index': [10], 'mid_lat_lon': (0.5, 1.5)},
                         {'index': [1, 2], 'mid_lat_lon': (1.5, 1.5)}],
                        [{'index': [], 'mid_lat_lon': (0.5, 2.5)},
                         {'index': [3, 4, 5], 'mid_lat_lon': (1.5, 2.5)}]]

        res = util.bin_data(lat, lon, gx, gy, gwidx, gwidy, gnumx, gnumy)

        for expected, actual in map(None, expected_res, res):
            for expected_dic, act_dic in map(None, expected, actual):
                self.failUnlessEqual(expected_dic['index'], act_dic['index'])
                self.failUnless(scipy.allclose(
                    scipy.array(expected_dic['mid_lat_lon']),
                    act_dic['mid_lat_lon']))

    def test_bin_dataII(self):
        ######
        # Same as above, extra points OUTSIDE THE GRID
        ######

        # define a small 2x3 grid
        gx = 0.0
        gy = 0.0
        gwidx = 1.0
        gwidy = 1.0
        gnumx = 3
        gnumy = 2

        # define points
        # First point as above
        lon = [0.5]
        lat = [1.5]
        # but add extra points at all external edges and quadrants
        #
        # *        *        *
        #    +---+---+---+
        #    |   |   |   |
        # *  +---+---+---+  *
        #    |   |   |   |
        #    +---+---+---+
        #
        # *        *        *
        #
        lon.extend([-0.5, -0.5, -0.5, 1.5,  1.5, 3.5, 3.5, 3.5])
        lat.extend([1.0, 2.5, -0.5, 2.5, -0.5, 2.5, 1.0, -0.5])

        # expected result for above data
        expected_res = [
            [{'index': [], 'mid_lat_lon': scipy.array([0.5, 0.5])},
             {'index': [0], 'mid_lat_lon': scipy.array([1.5, 0.5])}],
            [{'index': [], 'mid_lat_lon': scipy.array([0.5, 1.5])},
             {'index': [], 'mid_lat_lon': scipy.array([1.5, 1.5])}],
            [{'index': [], 'mid_lat_lon': scipy.array([0.5, 2.5])},
             {'index': [], 'mid_lat_lon': scipy.array([1.5, 2.5])}]
        ]

        res = util.bin_data(lat, lon, gx, gy, gwidx, gwidy, gnumx, gnumy)

        for expected, actual in map(None, expected_res, res):
            for expected_dic, act_dic in map(None, expected, actual):
                self.failUnlessEqual(expected_dic['index'], act_dic['index'])
                self.failUnless(scipy.allclose(expected_dic['mid_lat_lon'],
                                               act_dic['mid_lat_lon']))

    def test_bin_extent(self):
        ######
        # Same data as first test, but calling bin_extent(), and bins=(3,2)
        ######

        lon = [0.5, 1.3, 1.7, 2.3, 2.5, 2.7, 0.3, 0.7, 0.3, 0.7, 1.3]
        lat = [1.5, 1.7, 1.3, 1.3, 1.5, 1.7, 0.7, 0.7, 0.3, 0.3, 0.7]
        bins = (2, 3)

        # expected result for above data
        # Not checking the mid cell values, since I couldn't be bothered
        # calcing them... so this isn't that good a test.
        expected_res = [[{'index': [6, 7, 8, 9], 'mid_lat_lon': (0.5, 0.5)},
                         {'index': [0], 'mid_lat_lon': (1.5, 0.5)}],
                        [{'index': [10], 'mid_lat_lon': (0.5, 1.5)},
                         {'index': [1, 2], 'mid_lat_lon': (1.5, 1.5)}],
                        [{'index': [], 'mid_lat_lon': (0.5, 2.5)},
                         {'index': [3, 4, 5], 'mid_lat_lon': (1.5, 2.5)}]]

        res = util.bin_extent(lat, lon, bins)
        for expected, actual in map(None, expected_res, res):
            for expected_dic, act_dic in map(None, expected, actual):
                self.failUnlessEqual(expected_dic['index'], act_dic['index'])

    def test_bin_extentII(self):

        # This will describe an extent
        lat = [-25, -24]
        lon = [130, 131]
        bins = (1, 1)

        res = util.bin_extent(lat, lon, bins)

        expected_res = [[{'index': [0, 1], 'mid_lat_lon': (-24.5, 130.5)}]]

        for expected, actual in map(None, expected_res, res):
            for expected_dic, act_dic in map(None, expected, actual):
                self.failUnlessEqual(expected_dic['index'], act_dic['index'])
                self.failUnless(scipy.allclose(
                    scipy.array(expected_dic['mid_lat_lon']),
                    act_dic['mid_lat_lon']))

    def test_bin_extentII(self):

        # This will describe an extent
        lat = [-25, -24]
        lon = [130, 132]
        bins = (1, 2)

        res = util.bin_extent(lat, lon, bins)

        expected_res = [[{'index': [0], 'mid_lat_lon': (-24.5, 130.5)}],
                        [{'index': [1], 'mid_lat_lon': (-24.5, 131.5)}]]

        for expected, actual in map(None, expected_res, res):
            for expected_dic, act_dic in map(None, expected, actual):
                self.failUnlessEqual(expected_dic['index'], act_dic['index'])
                self.failUnless(scipy.allclose(
                    scipy.array(expected_dic['mid_lat_lon']),
                    act_dic['mid_lat_lon']))

    def test_max_nan(self):
        """Test the NaN handling of max_nan()."""

        vector = num.array([[1, 2, num.nan], [4, 5, 6], [7, 8, 9]])
        expected = 9
        got = util.max_nan(vector[:, 2])
        self.failUnless(got == expected)

        vector = num.array([[1, 2, 3], [4, 5, num.nan], [7, 8, 9]])
        expected = 9
        got = util.max_nan(vector[:, 2])
        self.failUnless(got == expected)

        vector = num.array([[1, 2, 3], [4, 5, 6], [7, 8, num.nan]])
        expected = 6
        got = util.max_nan(vector[:, 2])
        self.failUnless(got == expected)

        # if ALL of coloumn 2 is NaN, expect NaN
        vector = num.array([[1, 2, num.nan], [4, 5, num.nan], [7, 8, num.nan]])
        got = util.max_nan(vector[:, 2])
        self.failUnless(num.isnan(got))

    def test_min_nan(self):
        """Test the NaN handling of min_nan()."""

        vector = num.array([[1, 2, num.nan], [4, 5, 6], [7, 8, 9]])
        expected = 6
        got = util.min_nan(vector[:, 2])
        self.failUnless(got == expected)

        vector = num.array([[1, 2, 3], [4, 5, num.nan], [7, 8, 9]])
        expected = 3
        got = util.min_nan(vector[:, 2])
        self.failUnless(got == expected)

        vector = num.array([[1, 2, 3], [4, 5, 6], [7, 8, num.nan]])
        expected = 3
        got = util.min_nan(vector[:, 2])
        self.failUnless(got == expected)

        # if ALL of coloumn 2 is NaN,  expect NaN
        vector = num.array([[1, 2, num.nan], [4, 5, num.nan], [7, 8, num.nan]])
        got = util.min_nan(vector[:, 2])
        self.failUnless(num.isnan(got))

    def test_get_scale_min_max_step(self):
        """Test saneness of the get_scale_min_max_step() function"""

        # easy start
        max_val = 1.0
        min_val = 0.0
        expect_start = 0.0
        expect_stop = 1.0
        expect_step = 0.2
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # now check increased range
        max_val = 10.0
        min_val = 0.0
        expect_start = 0.0
        expect_stop = 10.0
        expect_step = 0.5
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # previous example, slightly increased min_val and decreased max_val
        # (ie. move away from previous start/stop by LESS THAN step)
        # shouldn't change start/stop
        max_val = 9.8           # expect 10.0 stop value
        min_val = 0.3           # expect 0.0 stop value
        expect_start = 0.0
        expect_stop = 10.0
        expect_step = 0.5
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # previous previous example, slightly decreased min_val and increased
        # max_val (ie. move away from previous start/stop by LESS THAN step)
        # should change start/stop
        max_val = 10.1          # expect 10.5 stop value
        min_val = -0.2          # expect -0.5 stop value
        expect_start = -0.5
        expect_stop = 10.5
        expect_step = 0.5
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # now try a simple negative minimum
        max_val = 1.0
        min_val = -1.0
        expect_start = -1.0
        expect_stop = 1.0
        expect_step = 0.5
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # negative minimum, larger range
        max_val = 10.0
        min_val = -10.0
        expect_start = -10.0
        expect_stop = 10.0
        expect_step = 5.0
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # previous example, slightly increased min_val and decreased max_val
        # (ie. move away from previous start/stop by LESS THAN step)
        # shouldn't change start/stop
        max_val = 9.9
        min_val = -9.8
        expect_start = -10.0
        expect_stop = 10.0
        expect_step = 2.0
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # previous previous example, slightly decreased min_val and increased
        # max_val (ie. move away from previous start/stop by LESS THAN step)
        # should change start/stop
        max_val = 10.1
        min_val = -10.2
        expect_start = -15.0
        expect_stop = 15.0
        expect_step = 5.0
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # now try a negative minimum and maximum
        max_val = -1.0
        min_val = -2.0
        expect_start = -2.0
        expect_stop = -1.0
        expect_step = 0.2
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # now try a negative minimum and maximum
        max_val = -1.0
        min_val = -2.0
        expect_start = -2.0
        expect_stop = -1.0
        expect_step = 0.2
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # now try a negative minimum and maximum, larger range
        max_val = -10.0
        min_val = -20.0
        expect_start = -20.0
        expect_stop = -10.0
        expect_step = 0.5
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # previous example, slightly increased min_val and decreased max_val
        # (ie. move away from previous start/stop by LESS THAN step)
        # shouldn't change start/stop
        max_val = -10.2
        min_val = -19.7
        expect_start = -20.0
        expect_stop = -10.0
        expect_step = 0.5
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)

        # previous previous example, slightly decreased min_val and increased
        # max_val (ie. move away from previous start/stop by LESS THAN step)
        # should change start/stop
        max_val = -9.8
        min_val = -20.1
        expect_start = -20.5
        expect_stop = -9.5
        expect_step = 0.5
        res = util.get_scale_min_max_step(max_val, min_val)
        (start, stop, step) = res
        msg = ('get_scale_min_max_step(%f,%f) returned %s, expected %s'
               % (max_val, min_val, str(res),
                  str((expect_start, expect_stop, expect_step))))
        self.failUnless(expect_start == start, msg)
        self.failUnless(expect_stop == stop, msg)
        self.failUnless(expect_step == step, msg)


if __name__ == '__main__':
    suite = unittest.makeSuite(TestUtilities, 'test')
    #suite = unittest.makeSuite(TestUtilities, 'test_bin_dataII')
    runner = unittest.TextTestRunner()
    runner.run(suite)
