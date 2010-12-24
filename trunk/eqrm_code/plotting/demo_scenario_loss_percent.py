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
from eqrm_code.eqrm_filesystem import Demo_Output_ScenRisk_Path


input_dir = Demo_Output_ScenRisk_Path
site_tag = 'newc'

title = 'demo_scenario_loss_percent.py'
plot_file = 'demo_scenario_loss_percent.png'
collapse_function = 'mean'
savefile = None
np_posn = 'nw'
s_posn = 'se'
cb_steps = [0, 5, 20, 15, 20]
colourmap = 'hazmap'
cb_label = 'Percent loss'
annotate = [('text', (151.35, -32.80), "Colourmap is '%s'" % colourmap)]
show_graph = len(sys.argv) > 1

plot_api.fig_scenario_loss_percent(input_dir, site_tag,
                                   plot_file=plot_file,
                                   collapse_function=collapse_function,
                                   savefile=None, title=title,
                                   np_posn=np_posn, s_posn=s_posn,
                                   cb_steps=cb_steps, annotate=annotate,
                                   colourmap=colourmap, cb_label=cb_label,
                                   show_graph=show_graph)
