#!/usr/bin/env python

"""Test the calc_annloss.py module."""

import os
import unittest
import random
import tempfile
import shutil
import scipy

import eqrm_code.plotting.calc_annloss as ca


class TestCalcAnnloss(unittest.TestCase):
   
    def test_small_checkable(self):       
        # See documentation/annualised_loss_calc.xls
        # for the calculations of the expected values.
        
        saved_ecloss = [[2000.0,    5.0],
                        [  10.0, 2001.0]]

        saved_ecbval2 = [2020.0, 2030.0]

        nu = [0.01, 0.001]
        
        expected_ann_loss = scipy.array([19.95996, 0.4928386])

        expected_cum_ann_loss = scipy.array([
            [1000, 90.909090],
            [19.95996, 0.0],
            [0.4928386, 0.0]])
        # call function
        (ann_loss,
         cum_ann_loss) = ca.calc_annloss(saved_ecloss, saved_ecbval2, nu)
        
        #print('expected_ann_loss=%s' % str(expected_ann_loss))
        #print('ann_loss=%s' % str(ann_loss))
        #print('cum_ann_loss=%s' % str(cum_ann_loss))
        
        # test return values
        self.failUnless(scipy.allclose(ann_loss, expected_ann_loss))
        self.failUnless(scipy.allclose(cum_ann_loss, expected_cum_ann_loss))

    def test_integrate_backwards(self):
        # square, 2 high, 2 long.
        # area of 4
        x = scipy.array([2,2])
        y = scipy.array([2,0])
        area = ca.integrate_backwards(x, y)
        self.failUnless(scipy.allclose(area[0], 4.0))

    def test_integrate_backwards_more(self):
        # square, 2 high, 2 long.
        # area of 4
        x = scipy.array([2,2,2])
        y = scipy.array([2,1,0])
        area = ca.integrate_backwards(x, y)
        self.failUnless(scipy.allclose(area[0], 4.0))
        
    def test_integrate_backwardsII(self):
        # triangle, 2 high, 2 long.
        # area of 2
        x = scipy.array([2,4])
        y = scipy.array([2,0])
        area = ca.integrate_backwards(x, y)
        
        self.failUnlessEqual(area[0], 6.0)
         
    def test_integrate_backwardsIII(self):
        # triangle, 2 high, 2 long.
        # on top of a square, 2 high and 2 long
        # area of 2
        x = scipy.array([2,4])
        y = scipy.array([2,0])
        area = ca.integrate_backwards(x, y)
        self.failUnlessEqual(area[0], 6.0)
        
    def test_integrate_backwards4(self):
        # Create more of a curve
        
        x = scipy.array([0,1,3,7])
        y = scipy.array([5, 3, 1, 0])
        area = ca.integrate_backwards(x, y)
        self.failUnlessEqual(list(area),
                             list([10., 9., 5., 0.]))

    def test_acquire_riskval(self):
        # create function input values.
        # values are from MatLab execution of acquire_riskval.m
        # with 'format long e' controlling display precision.

        x_ordinals = [3.6033316e+002,
                      1.1156048e+004,
                      5.1433916e+003,
                      1.1240941e+005,
                      7.4479859e+004,
                                   0,
                                   0,
                      2.3688128e+005,
                      6.9814475e+005,
                      1.1022014e+004,
                                   0,
                                   0]

        y_values = [4.630686287680000e-003,
                    1.060828942660000e-002,
                    5.316739231220000e-003,
                    4.033159153080000e-003,
                    3.059464090050000e-003,
                    1.267327623180000e-001,
                    4.828586998700000e-002,
                    4.916231738260000e-004,
                    1.801492034580000e-004,
                    5.811644129970000e-004,
                    1.804422031540000e-002,
                    1.336441244060000e-002]
        target_ordinals = [0.0]

        expected_target_values = [6.981447500000000e+005]

        expected_sorted_x_ordinals = [6.9814475e+005,
                                      2.3688128e+005,
                                      1.1240941e+005,
                                      7.4479859e+004,
                                      1.1156048e+004,
                                      1.1022014e+004,
                                      5.1433916e+003,
                                      3.6033316e+002,
                                                   0,
                                                   0,
                                                   0,
                                                   0]
        expected_cum_sorted_y_values = [1.801492034580000e-004,
                                        6.717723772840000e-004,
                                        4.704931530364000e-003,
                                        7.764395620414000e-003,
                                        1.837268504701400e-002,
                                        1.895384946001100e-002,
                                        2.427058869123100e-002,
                                        2.890127497891100e-002,
                                        1.556340372969110e-001,
                                        2.039199072839110e-001,
                                        2.219641275993110e-001,
                                        2.353285400399110e-001]

        # call function
        (target_values, sorted_x_ordinals, cum_sorted_y_values) = \
                        ca.acquire_riskval(x_ordinals,
                                        y_values,
                                        target_ordinals)

        # test return values
        self.failUnless(scipy.allclose(target_values, expected_target_values))
        self.failUnlessEqual(list(sorted_x_ordinals),
                             list(expected_sorted_x_ordinals))
        self.failUnless(scipy.allclose(cum_sorted_y_values,
                                     expected_cum_sorted_y_values))
        
    def test_calc_annloss_deagg_grid(self):
        # See documentation/annualised_loss_calc.xls
        # for the calculations of the expected values.

        lat = scipy.array([-25, -24])
        lon = scipy.array([130, 132])
        total_building_loss = scipy.array([[2000.0,    5.0],
                                           [  10.0, 2001.0]])

        total_building_value = scipy.array([2020.0, 2030.0])

        event_activity = scipy.array([0.01, 0.001])
        bins = (1,2)
        percent_ann_loss, lat_lon, _, _ = ca.calc_annloss_deagg_grid(
            lat,
            lon,
            total_building_loss,
            total_building_value,
            event_activity,
            bins=bins)
        
        expected_loss = scipy.array([[0.049233, 0.491135]])
        expected_lat_lon = scipy.array([[-24.5,130.5],[-24.5,131.5]])
        #print "percent_ann_loss", percent_ann_loss
        #print "expected_loss", expected_loss
        self.failUnless(scipy.allclose(percent_ann_loss, expected_loss))
        self.failUnless(scipy.allclose(lat_lon, expected_lat_lon))
    

if __name__ == '__main__':
    suite = unittest.makeSuite(TestCalcAnnloss,'test')
    #suite = unittest.makeSuite(TestCalcAnnloss,'test_calc_annloss_deagg_grid')
    #suite = unittest.makeSuite(TestCalcAnnloss,'test_small_checkable')
    runner = unittest.TextTestRunner()
    runner.run(suite)
