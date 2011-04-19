

"""
Demonstration of using the fig_fatalities_exceedance function.

"""

from eqrm_code.plotting import plot_api
from eqrm_code.eqrm_filesystem import Demo_Output_ProbRisk_Path

input_dir = Demo_Output_ProbRisk_Path
site_tag = 'newc'

title = ''
output_file = 'fig_from_demo_loss_exceedance.png'
grid = False
show_graph = False
annotate = None


plot_api.fig_loss_exceedance(input_dir, site_tag, title=title,
                      output_file=output_file, grid=grid,
                      show_graph=show_graph, annotate=annotate)
