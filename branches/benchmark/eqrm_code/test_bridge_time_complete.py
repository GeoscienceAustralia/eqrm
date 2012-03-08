#!/usr/bin/env python

"""Test the bridge state->time to completion code."""


import unittest
import bridge_time_complete as btc
import numpy as np

from eqrm_code import perf

class TestBridgeTimeComplete(unittest.TestCase):

    ######
    # test case to ensure bad state string is handled OK
    ######

    @perf.benchmark
    def test_bad_state(self):
        """Check that a bad state string gives RuntimeError."""

        states =  np.array([[[100]]])
        fp = np.array([0.1, 0.5, 0.9])
        self.failUnlessRaises(RuntimeError, btc.time_to_complete, fp, states)
        btc.reset_external_data()

    ######
    # test cases compared with published examples
    ######

    @perf.benchmark
    def test_Ken_example(self):
        # cases from Ken's recent paper:
        #     Bridge Seismic Vulnerability Modelling

        # none damage
        states =  np.array([[[0]]])
        fp = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
        expected_time = np.array([[[0, 0, 0, 0, 0, 0, 0, 0, 0]]])
        calc_time = btc.time_to_complete(fp, states)
        msg = ('states=\n%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (str(states), str(fp), str(expected_time), str(calc_time)))
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-2), msg)
        btc.reset_external_data()

        # slight damage
        states =  np.array([[[1]]])
        #fp = np.array([70, 100])
        fp = np.array([70])
        expected_time = np.array([[[1]]])
        calc_time = btc.time_to_complete(fp, states)
        msg = ('states=\n%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (str(states), str(fp), str(expected_time), str(calc_time)))
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-2), msg)
        btc.reset_external_data()

        # moderate damage
        states =  np.array([[[2]]])
        fp = np.array([30, 60, 95])
        expected_time = np.array([1, 3, 7])
        calc_time = btc.time_to_complete(fp, states)
        msg = ('states=\n%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (str(states), str(fp), str(expected_time), str(calc_time)))
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-1), msg)
        btc.reset_external_data()

        # extensive damage
        states =  np.array([[[3]]])
        fp = np.array([2, 5, 6, 15, 65])
        expected_time = np.array([1, 3, 7, 30, 90])
        calc_time = btc.time_to_complete(fp, states)
        msg = ('states=\n%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (str(states), str(fp), str(expected_time), str(calc_time)))
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-1), msg)
        btc.reset_external_data()

        # complete damage
        states =  np.array([[[4]]])
        fp = np.array([0, 2, 3, 10])
        expected_time = np.array([1, 4, 30, 90])
        calc_time = btc.time_to_complete(fp, states)
        msg = ('states=\n%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (str(states), str(fp), str(expected_time), str(calc_time)))
        # relaxed precision here since curve very flat at low FP
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-0), msg)
        btc.reset_external_data()

    ######
    # test more like the real world
    # really just ensuring multiple sites/events works
    ######
    @perf.benchmark
    def test_real_world(self):
        fp = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
        states = np.array([[[1],[0],[3]],
                           [[2],[1],[4]]])
        expected_time = np.array(
            [[[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0],
              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
              [22.0, 40.0, 53.0, 65.0, 75.0, 86.0, 98.0, 111.0, 129.0]],
             [[1.0, 1.0, 2.0, 2.0, 3.0, 4.0, 4.0, 5.0, 6.0],
              [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0],
              [90.0, 138.0, 173.0, 203.0, 230.0, 258.0, 288.0, 323.0, 371.0]]])
        calc_time = btc.time_to_complete(fp, states)
        msg = ('states=\n%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (str(states), str(fp), str(expected_time), str(calc_time)))
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-2), msg)
        btc.reset_external_data()

################################################################################

if __name__ == '__main__':
    unittest.main()

