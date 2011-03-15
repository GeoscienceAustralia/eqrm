#!/usr/bin/env python

"""
Demonstration of using the fig_xyz_histogram function.

Copyright 2010 by Geoscience Australia

"""

######

# You *can't* run this from IDLE.  Use a command line.
######

import sys

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotProbHaz_Path


input_dir = Demo_Output_PlotProbHaz_Path
site_tag = 'newc'
soil_amp = True
return_period = 100
period = 1.0
show_graph = len(sys.argv) > 1

# plot histogram wil auto-decided ranges
plot_file = 'demo_histogram.eps'
title = 'demo_histogram.py'
savefile = None
plot_api.fig_xyz_histogram(input_dir, site_tag, soil_amp, period, return_period,
                           plot_file, savefile=savefile,
                           title=title, xlabel='SA (g)', ylabel='Count',
                           xrange=None, yrange=None,
                           bins=100, bardict=None, show_graph=show_graph)

# now set range to low values around middle peak
# also change colour of plot
plot_file = 'demo_histogram_range.png'
title = 'demo_histogram.py - set range, colour'
savefile = 'test_histogram_data.txt'
xrange = (0.03, 0.04)
yrange = 100
bardict = {'color': 'red'}
plot_api.fig_xyz_histogram(input_dir, site_tag, soil_amp, period, return_period,
                           plot_file, savefile=savefile,
                           title=title, xlabel='SA (g)', ylabel='Count',
                           xrange=xrange, yrange=yrange,
                           bins=100, bardict=bardict, show_graph=show_graph)
