#!/usr/bin/env python

"""
Demonstration of using the fig_scenario_building_loss function.

Copyright 2010 by Geoscience Australia

"""

######
# This demo assumes that the java_*_rp[???].txt files and the
# java_locations.txt filesa are in the demo/output/prob_risk directory.
#
# You *can't* run this from IDLE.  Use a command line.
######

import sys

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_ProbRisk_Path


input_dir = Demo_Output_ProbRisk_Path
site_tag = 'newc'
bins = 10

# plot histogram wil auto-decided ranges
plotfile = 'demo_scenario_building_loss.png'
savefile = None
title = 'demo_scenario_building_loss.py'
xlabel = 'Loss in million$'
ylabel = 'frequency'
scale = 1.0e+6
xrange = None
yrange = None
show_graph = len(sys.argv) > 1


plot_api.fig_scenario_building_loss(input_dir, site_tag, plotfile, scale=scale,
                                    savefile=None, title=title, xlabel=xlabel,
                                    ylabel=ylabel, xrange=xrange, yrange=yrange,
                                    bins=bins, bardict=None, show_graph=show_graph)
