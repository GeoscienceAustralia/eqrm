#!/usr/bin/env python

"""
Description: A python module to plot PML dta.
 
Copyright 2007 by Geoscience Australia

"""


import os
import sys
import time

#from eqrm_code.plotting import calc_annloss
#import eqrm_code.plotting.acquire_riskval as ar

import eqrm_code.plotting.util_timestamp as pts
import eqrm_code.plotting.util_user_annotation as pua


def plot_pml(pml_data, title='', output_file=None, grid=True,
             show_graph=False, annotate=[]):
    """Plot the PML data.  Optionally save a file or show the graph (or both).

    Inputs:
    pml_data       (nx3) array containing the PML curve. The first column
                   contains the probability of exceedance (in one year) values,
                   the second column contains the direct financial losses
                   for each of the probabilities of exceedance and the third 
                   column contains the financial losses as a percentage of the 
                   total building value.
    title          if supplied, the graph title string
    output_file    path of file to save plot picture in
    grid           draw a grid on graph if True
    show_graph     show graph on screen if True
    annotate       an iterable like [(x, y, ann, dict), ...] where
                       x    is X screen coordinate
                       y    is Y screen coordinate
                       ann  is the annotation string to display at (x, y)
                       dict is a dictionary of key/value pairs as documented at
                            http://matplotlib.sourceforge.net/api/pyplot_api.html
                            (this is optional)
                   NOTE: if annotate=None is used, no automatic annotation occurs.
                         if annotate=[] is used, auto annotation is generated:
                             timestamp
                             clipping
                             max input data value


    """

    # decide if we have a 'gui-less' plot or not.
    import matplotlib
    if output_file and not show_graph:
        # no plot to be shown - no gui
        matplotlib.use('Agg', warn=False)
    elif show_graph:
        # decide if we *can* show the plot - error if not
        if sys.platform != 'win32':
            try:
                display = os.environ['DISPLAY']
            except KeyError:
                msg = ("No DISPLAY variable set.  "
                       "Did you do 'ssh -X <machine>'?")
                raise RuntimeError(msg)

    # go ahead with the plot
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    # create a plot of annualised loss versus return period if requested
    if output_file or show_graph:
        # unpack pml_data
        [ProbExceedSmall, trghzd_agg, Norm_trghzd_agg] = pml_data
                 
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        plt.semilogy(Norm_trghzd_agg, ProbExceedSmall, color='b')
        
        plt.xlabel('Direct financial loss (%)')
        plt.ylabel('Probability of exceedance in one year')

        # add graph 'furniture'
        if title:
            plt.title(title)
        plt.grid(grid)

        # add system annotations: time generated, etc
        if isinstance(annotate, list):
            pts.plot_timestamp(fig)

        # add user annotations, if any
        pua.plot_user_annotation(fig, annotate)

        # show or save graph (or both?)
        if output_file:
            plt.savefig(output_file)
        if show_graph:
            plt.show()

        plt.close()

