

"""
Demonstration of using the fig_loss_exceedance function.

Copyright 2010 by Geoscience Australia

"""

import sys

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_PlotProbRisk_Path

input_dir = Demo_Output_PlotProbRisk_Path
site_tag = 'newc'

title = 'demo_loss_exceedance.py'
output_file = 'demo_loss_exceedance.png'
grid = False
show_graph = len(sys.argv) > 1
annotate = None


plot_api.fig_loss_exceedance(input_dir, site_tag, title=title,
                      output_file=output_file, grid=grid,
                      show_graph=show_graph, annotate=annotate)
