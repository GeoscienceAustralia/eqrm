#!/usr/bin/env python

'''Test the plot_hexbin_map.py module.'''

import os
import sys
import unittest
import tempfile
import shutil
import scipy

import calc_load_data as cld
import plot_hexbin_map as phm


#DataFilename = 'lat_long_eloss.csv.SAVE'
DataFilename = 'lat_long_eloss.csv'

class TestHexbinPlot(unittest.TestCase):

    # do:
    #     python test_plot_hexbin_map.py TestHexbinPlot.show_small
    # to display graph
    def show_small(self):
        # don't test if DISPLAY environment variable undefined
        if sys.platform != 'win32':
            try:
                display = os.environ['DISPLAY']
            except KeyError:
                return

        self.test_real_world(show_graph=True)
        
    def test_real_world(self, show_graph=False):
        outputdir = tempfile.mkdtemp(prefix='test_plot_hexbin_map_')

        # get data from the file
        data = cld.calc_load_data(DataFilename, invert=True)

        value_scale = 1.0e3
        data[:,2] = data[:,2] / value_scale

        hexbin_args = {'gridsize': 100,
                       'reduce_C_function': scipy.sum,
                       'linewidth': 0.5,
                       'edgecolors': 'w',
                      }

        # test the plot routine
        output_file = os.path.join(outputdir, 'plot_hexbin_map.png')
        phm.plot_hexbin_map(data,
                            title='Test of plot_hexbin_map()\nsecond line',
                            output_file=output_file, 
                            cblabel='Dollar loss (x %d)' % int(value_scale),
                            cbformat='%.0f', colormap='hazmap',
                            show_graph=show_graph, grid=True,
                            np_posn='NW',
                            hexbin_args=hexbin_args)

        # ensure file expected was generated
        self.failUnless(os.path.isfile(output_file))

        # clean up
        shutil.rmtree(outputdir, ignore_errors=True)

         
if __name__ == '__main__':
    unittest.main()

