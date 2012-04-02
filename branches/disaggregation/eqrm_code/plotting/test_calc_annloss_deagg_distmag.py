#!/usr/bin/env python

'''Test the calc_annloss_deagg_distmag.py module.'''

import os
import unittest
import random
import tempfile
import shutil
import scipy

import eqrm_code.plotting.calc_annloss_deagg_distmag as cadd


class TestCalcAnnlossDeaggDistmag(unittest.TestCase):


    def test_calc_annloss_deagg_distmag(self):
        # See documentation/annualised_loss_calc.xls
        # for the calculations of the expected values.
        # 
        bldg_value = scipy.array([2020, 2030])
        saved_ecloss = scipy.array([[2000, 5],[10, 2001]])
        nu = scipy.array([0.01, 0.001])
        saved_rjb = scipy.array([[5, 15],[5, 15]])
        aus_mag = scipy.array([6.2, 6.7])
        momag_labels = momag_bin = scipy.array([6.0,7.0])
        R_bin = [ 0, 10, 20]
        Zlim = None

        NormDeAggLoss = cadd.calc_annloss_deagg_distmag(
            bldg_value, saved_ecloss, nu, saved_rjb,
            aus_mag, momag_bin, R_bin, Zlim, R_extend_flag=False)
        #print "NormDeAggLoss.shape", NormDeAggLoss.shape
        #print "NormDeAggLoss", NormDeAggLoss
        expected_NormDeAggLoss = scipy.array([[4.9824877, 49.9501992]])
        
        # test return values
        self.failUnless(scipy.allclose(NormDeAggLoss, expected_NormDeAggLoss))

        
    def test_calc_annloss_deagg_distmagII(self):
        # See documentation/annualised_loss_calc.xls
        # for the calculations of the expected values.
        # 
        bldg_value = scipy.array([2020, 2030])
        saved_ecloss = scipy.array([[2000, 5],
                                    [10, 2001],
                                    [2000, 5],
                                    [10, 2001]])
        nu = scipy.array([0.01, 0.001, 0.01, 0.001])
        saved_rjb = scipy.array([[5, 15],[5, 15],[5, 15],[5, 15]])
        aus_mag = scipy.array([6.2, 6.7, 7.2, 7.7])
        momag_labels = momag_bin = scipy.array([6.0,7.0, 8.0])
        R_bin = [ 0, 10, 20]
        Zlim = None

        NormDeAggLoss = cadd.calc_annloss_deagg_distmag(
            bldg_value, saved_ecloss, nu, saved_rjb,
            aus_mag, momag_bin, R_bin, Zlim, R_extend_flag=False)
        #print "NormDeAggLoss", NormDeAggLoss
        expected_NormDeAggLoss = scipy.array([[2.387182086, 23.93186447],
                                              [2.387182086, 23.93186447]])
        
        # test return values
        self.failUnless(scipy.allclose(NormDeAggLoss, expected_NormDeAggLoss))
        
if __name__ == '__main__':
    suite = unittest.makeSuite(TestCalcAnnlossDeaggDistmag,'test')
    #suite = unittest.makeSuite(TestCalcAnnlossDeaggDistmag,'test_calc_annloss_deagg_distmag')
    runner = unittest.TextTestRunner()
    runner.run(suite)
