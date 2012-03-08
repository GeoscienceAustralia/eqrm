#!/usr/bin/env python

"""
Demonstration of using the plot_motion function.

Copyright 2010 by Geoscience Australia

"""

import sys

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotScenGM_Path


input_dir = Demo_Output_PlotScenGM_Path
site_tag = 'newc'

soil_amp = False
period = 1.0

title = 'demo_motion.py'
plot_file = 'demo_motion.eps'
save_file = None
np_posn = 'nw'
s_posn = 'se'
colourmap = 'hazmap'
cb_steps = [0.0,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.10]
cb_label = 'Mean Acceleration (g)'
collapse_function = None
annotate = []
show_graph = len(sys.argv) > 1

plot_api.fig_motion(input_dir, site_tag, soil_amp, period,
                    collapse_function=collapse_function, plot_file=plot_file,
                    save_file=save_file, title=title, np_posn=np_posn,
                    s_posn=s_posn, cb_steps=cb_steps, colourmap=colourmap,
                    cb_label=cb_label, annotate=annotate, show_graph=show_graph)


