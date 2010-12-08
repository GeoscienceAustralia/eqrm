#!/usr/bin/env python

"""
Demonstration of using the plot_motion function.

Copyright 2010 by Geoscience Australia

"""

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotScenGM_Path


input_dir = Demo_Output_PlotScenGM_Path
site_tag = 'newc'

soil_amp = False
period = 1.0

title = 'demo_motion_continuous.py'
output_dir = '.'
plot_file = 'fig_from_demo_motion_continuous.png'
save_file = None
np_posn = 'nw'
s_posn = 'se'
#colourmap = 'hazmap'
colourmap = 't9'
#cb_steps = [0.10]
cb_steps = None
cb_label = 'Median Acceleration (g)'
collapse_function = 'Median'
annotate = []
show_graph = True

plot_api.fig_motion_continuous(input_dir, site_tag, soil_amp, period,
                               output_dir, collapse_function=collapse_function,
                               plot_file=plot_file, save_file=save_file,
                               title=title, np_posn=np_posn, s_posn=s_posn,
                               cb_steps=cb_steps, colourmap=colourmap,
                               cb_label=cb_label, annotate=annotate,
                               show_graph=show_graph)


