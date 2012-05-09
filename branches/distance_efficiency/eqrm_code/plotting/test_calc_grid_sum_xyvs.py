#!/usr/bin/env python

'''Test the utility calc_grid_sum_xyvs module.'''

import os
import sys
import unittest
import random
import tempfile
import shutil
import scipy

import numpy as num
import calc_grid_sum_xyvs as cgsx


class TestCalcGridSumXyvs(unittest.TestCase):

    def test_simple(self):
        """Test of calc_grid_sum_xyvs()."""

        # simple 2x2 data points
        a = [[1.0,1.0,1,2],[1.0,2.0,1,2],[2.0,1.0,1,2],[2.0,2.0,1,2],
             [1.0,2.0,1,2],[1.0,1.0,1,2],[2.0,1.0,1,2],[1.0,1.0,1,2],
             [2.0,2.0,1,2],[1.0,2.0,1,2]]

        # expected result should be 2x2 array, coords [1.25,1.75] and
        # some values 2*, some 3*, 2 bins in each direction
        expected_array = scipy.array([[1.25, 1.25, 3. , 6.],
                                      [1.25, 1.75, 3. , 6.],
                                      [1.75, 1.25, 2. , 4.],
                                      [1.75, 1.75, 2. , 4.]])
        expected_bins = (2, 2)

        # call the function
        res = cgsx.calc_grid_sum_xyvs(a, bins=2)

        # as expected?
        (res_bins, res_array) = res
        self.failUnless(res_bins == expected_bins)
        self.failUnless(scipy.allclose(res_array, expected_array))

         
if __name__ == '__main__':
    unittest.main()
