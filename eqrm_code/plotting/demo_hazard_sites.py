#!/usr/bin/env python

"""
Demonstration of using the fig_hazard_sites() function.

Copyright 2010 by Geoscience Australia

"""

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotProbHaz_Path


input_dir = Demo_Output_PlotProbHaz_Path
site_tag = 'newc'

soil_amp = True
title = 'demo_hazard_sites.py'
plot_file = 'fig_from_demo_hazard_sites.png'
save_file = None
# override X range to show how it is done
xrange = 1.1
# leave space at top for legend (data makes Y range be (0.1,0.9))
#yrange = (0.1, 1.5)
yrange = None
show_graph = True
show_grid = True
# default placement overridden
legend_placement = 'upper right'

# example of optional colour and linestyle specification
sites = [(-32.7928, 151.64931, 7500, 'r--'),
#         (-33.20083, 151.44729, 7500, 'g-'),	# same as below
         (-33.20083, 151.44729, 7500, 'green'),
         (-32.7928, 151.64931, 10000, 'b:'),
         (-33.20083, 151.44729, 10000, 'c-.')]

plot_api.fig_hazard_sites(input_dir, site_tag, soil_amp, sites,
                          plot_file=plot_file, save_file=save_file,
                          title=title, show_graph=show_graph,
                          show_grid=show_grid, xrange=xrange, yrange=yrange,
                          legend_placement=legend_placement)
