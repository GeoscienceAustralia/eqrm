#!/usr/bin/env python

"""Test the plot_annloss_deagg_distmag module.

This assumes that the demo code has been run.

"""

import os
import sys
import unittest
import random
import tempfile
import shutil
import scipy

import eqrm_code.plotting.calc_annloss_deagg_distmag as cadd
import eqrm_code.plotting.plot_annloss_deagg_distmag as padd


class TestPlotAnnlossDeaggDistmag(unittest.TestCase):

    # do:
    # python test_plot_annloss_deagg_distmag.py TestPlotAnnlossDeaggDistmag.show
    # to display graph
    def show(self):

        self.test_real_world_small(show_graph=True)
        
    def test_real_world_small(self, show_graph=False):
        # don't test if DISPLAY environment variable undefined
        if sys.platform != 'win32':
            try:
                display = os.environ['DISPLAY']
            except KeyError:
                return

        # create function input values.
        # values are from MatLab execution of calc_annloss.m
        # with 'format long e' controlling display precision
        # and a thinned data set.


        saved_ecloss = [[3.6033316e+002,              0,              0,              0],
                        [4.3791719e+003, 5.4416445e+003, 1.5130650e+002, 1.1839250e+003],
                        [4.3966499e+001, 4.6514600e+003, 4.4796530e+002,              0],
                        [3.2344959e+004, 7.7890422e+004,              0, 2.1740315e+003],
                        [3.7524958e+003, 8.5406250e+003, 2.0106344e+004, 4.2080391e+004],
                        [             0,              0,              0,              0],
                        [             0,              0,              0,              0],
                        [6.8155151e+003, 7.4778169e+003, 4.0293285e+004, 1.8229467e+005],
                        [4.7653789e+004, 5.7597363e+005, 4.2247324e+004, 3.2269982e+004],
                        [             0, 1.1022014e+004,              0,              0],
                        [             0,              0,              0,              0],
                        [             0,              0,              0,              0]]


        saved_ecbval2 = [1.657488601000000e+006, 1.297431077000000e+006,
                         1.559989253000000e+006, 7.915145563000001e+005]

        nu = [4.630686287680000e-003, 1.060828942660000e-002,
              5.316739231220000e-003, 4.033159153080000e-003,
              3.059464090050000e-003, 1.267327623180000e-001,
              4.828586998700000e-002, 4.916231738260000e-004,
              1.801492034580000e-004, 5.811644129970000e-004,
              1.804422031540000e-002, 1.336441244060000e-002]

        aus_mag = [5.028646345960000e+000, 4.666194309470000e+000,
                   4.960717775140000e+000, 5.066894448200000e+000,
                   5.213679185270000e+000, 4.750346609700000e+000,
                   5.137028659350000e+000, 5.846435787360000e+000,
                   6.332776147850000e+000, 5.831299749560000e+000,
                   5.704055389670000e+000, 5.678562864290000e+000]

      
        saved_rjb = [[4.7861000e+001, 5.3972000e+001, 4.7769001e+001, 5.2328999e+001],
                     [2.0844000e+001, 1.5184000e+001, 2.0931999e+001, 1.6514999e+001],
                     [4.1341999e+001, 4.7893002e+001, 4.1130001e+001, 4.6007000e+001],
                     [1.0091000e+001, 4.7954001e+000, 1.0547000e+001, 6.5434999e+000],
                     [1.1430000e+001, 7.0029001e+000, 1.1938000e+001, 8.7105999e+000],
                     [2.6070001e+002, 2.5430000e+002, 2.6089001e+002, 2.5610001e+002],
                     [1.8946001e+002, 1.9613000e+002, 1.8919000e+002, 1.9414999e+002],
                     [1.3391000e+001, 7.5120001e+000, 1.3538000e+001, 8.9108000e+000],
                     [1.4840000e+001, 1.1531000e+001, 1.4634000e+001, 1.2035000e+001],
                     [5.5563999e+001, 5.8155998e+001, 5.5868000e+001, 5.7826000e+001],
                     [2.1272000e+002, 2.0710001e+002, 2.1275999e+002, 2.0850000e+002],
                     [2.7423001e+002, 2.8089999e+002, 2.7397000e+002, 2.7894000e+002]]
 

        momag_bin = [4.500000000000000e+000, 5.000000000000000e+000,
                     5.500000000000000e+000, 6.000000000000000e+000,
                     6.500000000000000e+000]

        momag_labels = [4.500000000000000e+000, 5.000000000000000e+000,
                        5.500000000000000e+000, 6.000000000000000e+000,
                        6.500000000000000e+000]

        R_bin = [ 0,  5, 10, 15, 20, 25, 30, 35, 40, 45,
                 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

        Zlim = [0, 8]
        
        outputdir = tempfile.mkdtemp(prefix='test_calc_annloss_')


        expected_NormDeAggLoss = \
             scipy.array([[                     0,                      0,
                                                0, 9.953154884489259e-001,
                           6.805837966835917e-001,                      0,
                                                0,                      0,
                           1.478403601668658e-001, 1.397904170353129e+000,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0],
                          [1.026185781801060e+001, 6.351341814315093e+000,
                           8.029817774010610e+000,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0, 4.133484588328035e-002,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0],
                          [                     0, 3.155337893093759e+000,
                           7.832757193963517e-001,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0, 1.550199002799408e-001,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0],
                          [                     0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0,                      0,
                                                0]])

        # call function
        NormDeAggLoss = cadd.calc_annloss_deagg_distmag(saved_ecbval2, saved_ecloss,
                                                        nu, saved_rjb, aus_mag,
                                                        momag_bin, R_bin, Zlim,
                                                        R_extend_flag=True)

        # plot the data
        o_file = os.path.join(outputdir, 'test.png')
        padd.plot_annloss_deagg_distmag(NormDeAggLoss, momag_labels, R_bin, Zlim,
                               output_file=o_file,
                               title='test_plot_calc_annloss_deagg_distmag.py',
                               show_graph=show_graph, grid=False, annotate=[])

        # make sure output file was created
        self.failUnless(os.path.isfile(o_file))

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

         
if __name__ == '__main__':
    unittest.main()
