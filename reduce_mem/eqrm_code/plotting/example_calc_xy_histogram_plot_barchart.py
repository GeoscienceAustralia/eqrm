#!/usr/bin/env python

"""
An example of calculating a histogram and plotting it.

Copyright 2007 by Geoscience Australia

"""


import os
import sys
import tempfile
import shutil
import scipy

import eqrm_code.plotting.calc_xy_histogram as cxh
import eqrm_code.plotting.plot_barchart as pb


def example_calc_histogram_plot_barchart(datafile, output_file=None):
    """An example of calulating a histogram and then plotting the result.
    
    datafile    the path to the file to plot
    output_file path to the graph picture file to produce

    """

    data = cxh.calc_xy_histogram(datafile, bins=50)
    pb.plot_barchart(data, output_file=output_file,
                     title='example_calc_histogram_plot_barchart',
                     xlabel='IQ', ylabel='frequency',
                     xrange=None, yrange=None, grid=True,
                     show_graph=True, annotate=[])


if __name__ == '__main__':
    # make a temporary directory and file
    tmpdir = tempfile.mkdtemp(prefix='example_calc_histogram_plot_barchart')
    datafile = os.path.join(tmpdir, 'data.txt')

    # generate a normal curve centred 100, sigma 15, save in file
    mu = 100
    sigma = 15
    x = mu + sigma*scipy.random.randn(10000)
    scipy.savetxt(datafile, x)

    # call the example
    output_file = 'example_calc_histogram_plot_barchart.png'
    example_calc_histogram_plot_barchart(datafile, output_file=output_file)

    # remove temp directory
    shutil.rmtree(tmpdir)

