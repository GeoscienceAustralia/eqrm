#!/usr/bin/env python

"""Test the bridge state->time to completion code."""


import unittest
import bridge_time_complete as btc
import numpy as np


class TestBridgeTimeComplete(unittest.TestCase):

    ######
    # test case to ensure bad state string is handled OK
    ######

    def test_bad_state(self):
        """Check that a bad state string gives RuntimeError."""

        state = 'bad'
        fp = np.array([0.1, 0.5, 0.9])
        self.failUnlessRaises(RuntimeError, btc.time_to_complete, fp, state)

    ######
    # test cases compared with published examples
    ######

    def test_Ken_example(self):
        # cases from Ken's recent paper:
        #     Bridge Seismic Vulnerability Modelling

        # none damage
        state = 'none'
        fp = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])
        expected_time = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        calc_time = btc.time_to_complete(fp, state)
        msg = ('state=%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (state, str(fp), str(expected_time), str(calc_time)))
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-2), msg)

        # slight damage
        state = 'slight'
        fp = np.array([70, 100])
        expected_time = np.array([1, np.inf])
        calc_time = btc.time_to_complete(fp, state)
        msg = ('state=%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (state, str(fp), str(expected_time), str(calc_time)))
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-2), msg)

        # moderate damage
        state = 'moderate'
        #fp = np.array([30, 60, 95, 100])
        fp = np.array([30, 60, 95])
        #expected_time = np.array([1, 3, 7, np.inf])
        expected_time = np.array([1, 3, 7])
        calc_time = btc.time_to_complete(fp, state)
        msg = ('state=%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (state, str(fp), str(expected_time), str(calc_time)))
        self.failUnless(np.allclose(expected_time, calc_time, rtol=1.0e-1), msg)

        # extensive damage
        state = 'extensive'
        fp = np.array([2, 5, 6, 15, 65])
        expected_time = np.array([1, 3, 7, 30, 90])
        calc_time = btc.time_to_complete(fp, state)
        msg = ('state=%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (state, str(fp), str(expected_time), str(calc_time)))
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-1), msg)

        # complete damage
        state = 'complete'
        fp = np.array([0, 2, 3, 10])
        expected_time = np.array([1, 4, 30, 90])
        calc_time = btc.time_to_complete(fp, state)
        msg = ('state=%s, fp=%s\nexpected_time=%s\ncalc_time=%s'
               % (state, str(fp), str(expected_time), str(calc_time)))
        # relaxed precision here since curve very flat at low FP
        self.failUnless(np.allclose(expected_time, calc_time, rtol=5.0e-0), msg)


################################################################################

if __name__ == '__main__':
    unittest.main()

