#!/usr/bin/env python

"""
Demonstration of using the fig_hazard_sites() function.

Copyright 2010 by Geoscience Australia

"""

import sys

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotProbHaz_Path


input_dir = Demo_Output_PlotProbHaz_Path
site_tag = 'newc'

soil_amp = True
title = 'demo_hazard_exceedance.py'
plot_file = 'demo_hazard_exceedance.png'
save_file = None
# override X range to show how it is done
xrange = 1.0
# leave space at top for legend (data makes Y range be (0.1,0.9))
yrange = (1.0E-04, 1.0E-01)
show_graph = len(sys.argv) > 1
show_grid = True
# default placement overridden
legend_placement = 'upper right'

# example of optional colour and linestyle specification
sites = [(-32.7928, 151.64931, 0.0, 'r--'),
         (-33.20083, 151.44729, 0.0, 'green')]

plot_api.fig_hazard_exceedance(input_dir, site_tag, soil_amp, sites,
                               plot_file=plot_file, save_file=save_file,
                               title=title, show_graph=show_graph,
                               show_grid=show_grid, xrange=xrange, yrange=yrange,
                               legend_placement=legend_placement)
