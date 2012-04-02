#!/usr/bin/env python

'''Test the plot_pml.py module.'''

import os
import sys
import unittest
import random
import tempfile
import shutil
import scipy

import plot_pml
import eqrm_code.util as util


class TestPlotPml(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    # do:
    # python test_plot_pml.py TestPlotPml.show_small
    # to display graph
    def show_small(self):
        # don't test if DISPLAY environment variable undefined
        if sys.platform != 'win32':
            try:
                display = os.environ['DISPLAY']
            except KeyError:
                return

        self.test_real_world_small(show_graph=True)
        
    def test_real_world_small(self, show_graph=False):
        # don't test if DISPLAY environment variable undefined
        if sys.platform != 'win32':
            try:
                display = os.environ['DISPLAY']
            except KeyError:
                return

        # create function input values.
        # values are from MatLab execution of calc_pml.m
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
        saved_ecbval2 = [1.657488601000000e+006,
                         1.297431077000000e+006,
                         1.559989253000000e+006,
                         7.915145563000001e+005]
        nu = [4.630686287680000e-003,
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
        
        outputdir = tempfile.mkdtemp(prefix='test_plot_pml_')

        expected_pml_curve=[scipy.array([9.516258196404048e-002, 6.001990726997575e-002, 3.758725213253833e-002,
                                         2.343477581582976e-002, 1.457079605966405e-002, 9.044030246264989e-003,
                                         5.607631459973006e-003, 3.474649972298738e-003, 2.152115561384393e-003,
                                         1.332632687555568e-003, 8.250636329376615e-004, 5.107664918124755e-004,
                                         3.161777712868963e-004, 1.957150234642713e-004, 1.211454271629053e-004,
                                         7.498660929694534e-005, 4.641481113543122e-005, 2.872943563536623e-005,
                                         1.778263598739560e-005, 1.100688113631065e-005, 6.812897482721958e-006,
                                         4.216956142943928e-006, 2.610153809201599e-006, 1.615596793347329e-006,
                                         9.999994999843054e-007]),
                            scipy.array([1.581815795898438e+002, 2.665191955566406e+002, 3.335764770507813e+002,
                                         5.759092285156250e+003, 3.321068750000000e+004, 6.659575781250000e+004,
                                         1.010225859375000e+005, 1.501917812500000e+005, 1.911231718750000e+005,
                                         2.164582968750000e+005, 2.321398750000000e+005, 3.878219687500000e+005,
                                         5.704695625000000e+005, 6.835221875000000e+005, 6.981447500000000e+005,
                                         6.981447500000000e+005, 6.981447500000000e+005, 6.981447500000000e+005,
                                         6.981447500000000e+005, 6.981447500000000e+005, 6.981447500000000e+005,
                                         6.981447500000000e+005, 6.981447500000000e+005, 6.981447500000000e+005,
                                         6.981447500000000e+005]),
                            scipy.array([2.980945263197025e-003, 5.022576810812553e-003, 6.286276959408505e-003,
                                         1.085305818304859e-001, 6.258582184306246e-001, 1.255002695730662e+000,
                                         1.903779187229967e+000, 2.830376836855518e+000, 3.601732359515218e+000,
                                         4.079174935680411e+000, 4.374695603462225e+000, 7.308537844334971e+000,
                                         1.075054721631848e+001, 1.288103350846180e+001, 1.315659693710628e+001,
                                         1.315659693710628e+001, 1.315659693710628e+001, 1.315659693710628e+001,
                                         1.315659693710628e+001, 1.315659693710628e+001, 1.315659693710628e+001,
                                         1.315659693710628e+001, 1.315659693710628e+001, 1.315659693710628e+001,
                                         1.315659693710628e+001])]

        # call function
        output_file = os.path.join(outputdir, 'test.eps')
        plot_pml.plot_pml(expected_pml_curve, title='Test plot_pml()',
                          output_file=output_file, grid=True,
                          show_graph=show_graph)

        # ensure file expected was generated
        self.failUnless(os.path.isfile(output_file))

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

         
if __name__ == '__main__':
    unittest.main()
