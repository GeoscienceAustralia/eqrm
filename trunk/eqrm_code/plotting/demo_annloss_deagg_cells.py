#!/usr/bin/env python

"""
Demonstration of using the fig_annloss_deagg_cells function.

Copyright 2010 by Geoscience Australia

"""

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotProbRisk_Path

input_dir = Demo_Output_PlotProbRisk_Path
site_tag = 'newc'

title = 'demo_annloss_deagg_cells.py'
output_dir = '.'
output_file = 'fig_from_demo_annloss_deagg_cells.png'
save_file = None
np_posn = 'nw'
s_posn = 'se'
cb_steps = []		# discrete colourbar, code chooses breaks
colourmap = 'hazmap'
cb_label = 'Annualised loss as a percentage of total value, %'
annotate = []

plot_api.fig_annloss_deagg_cells(input_dir, site_tag,
                                 output_file, save_file=save_file,
                                 title=title, np_posn=np_posn, s_posn=s_posn,
                                 cb_label=cb_label, cb_steps=cb_steps, bins=100,
                                 colourmap=colourmap, annotate=annotate)
