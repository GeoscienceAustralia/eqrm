#!/usr/bin/env python

"""
Definitions of parts of the EQRM filesystem.

The variables below describe where in the EQRM filesystem
certain parts of the system live.
 
Version: $Revision$  
ModifiedBy: $Author$
ModifiedDate: $Date$

Copyright 2007 by Geoscience Australia

"""


import os

import eqrm_code.util as util


eqrm_path = util.determine_eqrm_path()


# define various paths
Resources_Data_Path = os.path.join(eqrm_path, 'resources', 'data')

demo_path = os.path.join(eqrm_path, 'demo')

Implementation_Path = os.path.join(eqrm_path, 'implementation_tests')

mini_scenario_scenarios_path = os.path.join(eqrm_path, 'implementation_tests',
                                  'mini_scenarios',
                                  'scenarios')

mini_scenario_Path = os.path.join(eqrm_path, 'implementation_tests',
                                  'mini_scenarios')

scenario_input_path = os.path.join(eqrm_path, 'implementation_tests',
                                  'input')
scenario_scenarios_path = os.path.join(eqrm_path, 'implementation_tests',
                                  'scenarios')

scenario_input_bridges_path = os.path.join(eqrm_path, 'implementation_tests',
                                  'input_bridges')


Demo_Output_ProbRisk_Path = os.path.join(eqrm_path,
                                         'demo', 'output', 'prob_risk')

#demo_plot_path = os.path.join(eqrm_path, 'resources', 'plot_data')
# This was changed to get demo/plot/execute_all_demos.p;y going
demo_plot_path = os.path.join(eqrm_path, 'demo', 'plot', 'plot_data')

Demo_Output_PlotProbRisk_Path = os.path.join(demo_plot_path,
                                             'output', 'plot_prob_risk')

Demo_Output_PlotScenRiskMMI_Path = os.path.join(demo_plot_path,
                                             'output', 'plot_scen_risk_mmi')
                                             
Demo_Output_PlotScenGM_Path = os.path.join(demo_plot_path,
                                             'output', 'plot_scen_gm')

Demo_Output_ProbHaz_Path = os.path.join(eqrm_path,
                                         'demo', 'output', 'prob_haz')

Demo_Output_PlotProbHaz_Path = os.path.join(demo_plot_path,
                                            'output', 'plot_prob_haz')

Postprocessing_Path = os.path.join(eqrm_path, 'postprocessing')

Eqrmcode_Plotting_Colourmaps_Path = os.path.join(eqrm_path, 'eqrm_code',
                                                 'plotting', 'colourmaps')

Demo_Output_ScenRisk_Path = os.path.join(eqrm_path,
                                         'demo', 'output', 'scen_risk')
plot_output_scen_risk_path = os.path.join(demo_plot_path,
                                             'output', 'plot_scen_risk')
demo_plot_scenarios = os.path.join(eqrm_path,
                                         'demo', 'plot', 'plot_data')
manual_diagrams = os.path.join(eqrm_path, 'latex_sourcefiles', 'manual_tech',
                               'diags')

