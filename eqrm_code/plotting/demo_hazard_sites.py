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
return_period = 7500
period = 1.0

title = 'demo_hazard_sites.py'
output_dir = '.'
plot_file = 'fig_from_demo_hazard_sites.png'
save_file = None
xrange = 1.1
yrange = (0.1, 1.3)
show_graph = True
show_grid = True
legend_placement = 'upper right'

sites = [(-32.7928, 151.64931, 7500),(-33.20083, 151.44729, 7500),
         (-32.7928, 151.64931, 10000),(-33.20083, 151.44729, 10000)]

plot_api.fig_hazard_sites(input_dir, site_tag, soil_amp, sites,
                          plot_file=plot_file, save_file=save_file,
                          title=title, show_graph=show_graph,
                          show_grid=show_grid, xrange=xrange, yrange=yrange,
                          legend_placement=legend_placement)
