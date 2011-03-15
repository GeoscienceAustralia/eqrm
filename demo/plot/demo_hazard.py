#!/usr/bin/env python

"""
Demonstration of using the plot_hazard function.

Copyright 2010 by Geoscience Australia

"""

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotProbHaz_Path


input_dir = Demo_Output_PlotProbHaz_Path
site_tag = 'newc'

soil_amp = False
return_period = 7500
period = 1.0

title = 'demo_hazard.py'
plot_file = 'demo_hazard.eps'
save_file = None
np_posn = 'nw'
#np_posn = (151.35, -32.82)
s_posn = 'se'
#s_posn = (151.76, -33.175, 5)
cb_steps = None
colourmap = 'hazmap'
cb_label = 'Acceleration (g)'
annotate = []

plot_api.fig_hazard(input_dir, site_tag, soil_amp, return_period, period,
                     plot_file=plot_file, save_file=save_file,
                     title=title, np_posn=np_posn, s_posn=s_posn,
                     cb_steps=cb_steps, annotate=annotate,
                     colourmap=colourmap, cb_label=cb_label)
