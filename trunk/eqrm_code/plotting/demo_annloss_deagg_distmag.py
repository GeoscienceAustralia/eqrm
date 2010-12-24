
"""
Demonstration of using the fig_annloss_deagg_distmag

Copyright 2010 by Geoscience Australia

"""

import sys

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_ProbRisk_Path

input_dir = Demo_Output_ProbRisk_Path
site_tag = 'newc'

momag_labels = [4.5, 5.0, 5.5, 6.0, 6.5]
momag_bin = [4.5, 5.0, 5.5, 6.0, 6.5]
range_bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45,
               50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
Zlim = [0, 8]
R_extend_flag=True

title = 'demo_annloss_deagg_distmag.py'
output_file = 'demo_annloss_deagg_distmag.png'
grid = None
show_graph = len(sys.argv) > 1
annotate = None

plot_api.fig_annloss_deagg_distmag(input_dir, site_tag, momag_labels,
                                   momag_bin, range_bins, Zlim,
                                   R_extend_flag=R_extend_flag,
                                   output_file=output_file,
                                   title=title,
                                   show_graph=show_graph,
                                   grid=grid, annotate=annotate)
