#!/usr/bin/env python

"""
Demonstration of using the fig_hazard_continuous function.

Copyright 2010 by Geoscience Australia

"""

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotProbHaz_Path


input_dir = Demo_Output_PlotProbHaz_Path
site_tag = 'newc'

soil_amp = False
return_period = 7500
period = 1.0

title = 'demo_hazard_continuous.py'
output_dir = '.'
plot_file = 'fig_from_demo_hazard_continuous.png'
save_file = None
np_posn = 'nw'
s_posn = 'se'
cb_steps = None
colourmap = 't9'
cb_label = 'Acceleration (g)'
annotate = [('text', (151.35, -32.80), "Colourmap is '%s'" % colourmap)]

plot_api.fig_hazard_continuous(input_dir, site_tag, soil_amp, return_period,
                               period, output_dir, plot_file=plot_file,
                               save_file=save_file, title=title,
                               np_posn=np_posn, s_posn=s_posn,
                               cb_steps=cb_steps, annotate=annotate,
                               colourmap=colourmap, cb_label=cb_label)
