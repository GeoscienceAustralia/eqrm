#!/usr/bin/env python

"""
Demonstration of using the fig_xyz_histogram function.

Copyright 2010 by Geoscience Australia

"""

######
# This demo assumes that the java_*_rp[???].txt files and the
# java_locations.txt filesa are in the demo/output/prob_risk directory.
#
# You *can't* run this from IDLE.  Use a command line.
######


from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_ProbRisk_Path


input_dir = Demo_Output_ProbRisk_Path
site_tag = 'java'
soil_amp = True
return_period = 100
period = 1.0

# plot histogram wil auto-decided ranges
plotfile = 'fig_from_demo_histogram.png'
title = 'demo_histogram.py'
savefile = None
plot_api.fig_xyz_histogram(input_dir, site_tag, soil_amp, period, return_period,
                           plotfile, savefile=savefile,
                           title=title, xlabel='SA (g)', ylabel='Count',
                           xrange=None, yrange=None,
                           bins=100, bardict=None, show_graph=False)

# now set range to low values around middle peak
# also change colour of plot
plotfile = 'fig_from_demo_histogram_range.png'
title = 'demo_histogram.py - set range, colour'
savefile = 'test_histogram_data.txt'
xrange = (0.03, 0.04)
yrange = 100
bardict = {'color': 'red'}
plot_api.fig_xyz_histogram(input_dir, site_tag, soil_amp, period, return_period,
                           plotfile, savefile=savefile,
                           title=title, xlabel='SA (g)', ylabel='Count',
                           xrange=xrange, yrange=yrange,
                           bins=100, bardict=bardict, show_graph=False)
