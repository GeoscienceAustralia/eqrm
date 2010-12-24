#!/usr/bin/env python

"""
Demonstration of using fig_xyz_histogram function.

Copyright 2010 by Geoscience Australia

"""

import sys

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotProbHaz_Path


input_dir = Demo_Output_PlotProbHaz_Path
site_tag = 'newc'

soil_amp = False
return_period = 7500
period = 1.0

title = 'demo_prob_SA_histogram.py'
plot_file = 'demo_prob_SA_histogram.png'
save_file = None
show_graph = len(sys.argv) > 1

plot_api.fig_xyz_histogram(input_dir, site_tag, soil_amp, period, return_period,
                           plot_file, savefile=save_file,
                           title=title, xlabel=None, ylabel=None,
                           xrange=None, yrange=None,
                           bins=100, bardict=None, show_graph=show_graph)
