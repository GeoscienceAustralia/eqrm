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

Demo_Path = os.path.join(eqrm_path, 'demo')

Implementation_Path = os.path.join(eqrm_path, 'implementation_tests')

Demo_Output_ProbRisk_Path = os.path.join(eqrm_path,
                                         'demo', 'output', 'prob_risk')

Demo_Output_PlotProbRisk_Path = os.path.join(eqrm_path,
                                         'demo', 'output', 'plot_prob_risk')

Demo_Output_ProbHaz_Path = os.path.join(eqrm_path,
                                         'demo', 'output', 'prob_haz')

Demo_Output_PlotProbHaz_Path = os.path.join(eqrm_path,
                                         'demo', 'output', 'plot_prob_haz')

Postprocessing_Path = os.path.join(eqrm_path, 'postprocessing')

Eqrmcode_Plotting_Colourmaps_Path = os.path.join(eqrm_path, 'eqrm_code',
                                                 'plotting', 'colourmaps')


