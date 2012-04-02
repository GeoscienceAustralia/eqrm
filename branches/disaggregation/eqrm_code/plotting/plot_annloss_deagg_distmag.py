#!/usr/bin/env python

"""
Description: A python module to plot Annual Loss Deaggregated Distance
             and Magnitude data.

This module is designed to not error or hang if executed in a Linux
environment that doesn't have the X DISPLAY environment variable
AS LONG AS THE USER DOESN'T WISH TO DISPLAY THE PLOT ON THE SCREEN.
 
Copyright 2007 by Geoscience Australia

"""


import os
import sys
import time
import scipy
import numpy as num

import eqrm_code.plotting.util_timestamp as pts
import eqrm_code.plotting.util_user_annotation as pua
import eqrm_code.plotting.util_colormaps as uc


def plot_annloss_deagg_distmag(data, momag_labels, range_bins, pct_limits=None,
                               output_file=None, title=None,
                               show_graph=False, grid=False, colormap=None,
                               annotate=[]):
    """Plot annualised loss deaggregated distance/magnitude data.

    Inputs:
    data         an MxN array containing % annualised loss values with axes
                 of moment/magnitude data (M) versus distance (N)
    momag_labels an iterable containing the y-axis labels for each row of 'data'
    range_bins   an iterable of range values for each column of 'data'
    pct_limits   a tuple (min_pct, max_pct) for % range to plot
    output_file  path to required output plot file
    title        string used to title graph
    show_graph   if True shows graph in window on screen
    grid         if True puts a grid in the graph
    colormap     name of the colormap to use
    annotate     an iterable like [(x, y, str, dict), ...] where
                     x    is X screen coordinate
                     y    is Y screen coordinate
                     str  is the annotation string to display at (x, y)
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

    # decide if we are going to plot
    if output_file or show_graph:
        # get colormap to use
        (cmap_name, my_cmap) = uc.get_colormap(colormap)

        # get maximum data value
        #max_pct = scipy.max(data)
        max_pct = num.max(data)
        
        # limit values to within pct_limits here
        if pct_limits:
            (floor, ceil) = pct_limits
            plot_data = scipy.clip(data, floor, ceil)
        else:
            plot_data = data

        # drop last range bin row from data
        plot_data = plot_data[:,:-1]
        
        # Get data X and Y limits
        max_x = range_bins[-1]
        min_x = range_bins[0]
        max_y = momag_labels[-1]
        min_y = momag_labels[0]
        max_z = num.max(plot_data)
        min_z = num.min(plot_data)

        # calculate required aspect ration (the *2 is a fudge)
        (y_size, x_size) = scipy.shape(plot_data)
        ratio = float(x_size/y_size) * 2

        # start plot
        fig = plt.figure()
        ax = fig.add_subplot(111)

        im = plt.imshow(plot_data, interpolation='nearest', cmap=my_cmap,
                        origin='lower', extent=[min_x,max_x,min_y,max_y])

        # add color bar
        for step in (1, 2, 5, 10, 20, 50, 100):
            cb_ticks = [x for x in range(int(min_z), int(max_z+1), step)]
            if len(cb_ticks) <= 12:
                break
        cb = plt.colorbar(orientation='horizontal', ticks=cb_ticks)
        cb.set_label('% of annual loss')
        
        # label axes
        plt.xlabel('Distance (km)')
        plt.ylabel('Moment Magnitude')

        # set main plot aspect ratio
        plt.axes().set_aspect(ratio)

        # add graph 'furniture'
        if title:
            plt.title(title)
        plt.grid(grid) 
                
        # add system annotations: the clipping in effect, time generated, etc
        if isinstance(annotate, list):
            pts.plot_timestamp(fig)

            if pct_limits:
                clip_str = 'Data values clipped to [%.1f,%.1f]' % (floor, ceil)
                plt.text(0.98, 0.02, clip_str, fontsize=6,
                         transform=fig.transFigure, horizontalalignment='right')
            pct_str = '%.2f%%' % max_pct
            plt.text(0.91, 0.185, pct_str, horizontalalignment='left',
                     fontsize=8, transform=fig.transFigure, )

        # add user annotations, if any
        pua.plot_user_annotation(fig, annotate)

        # show or save graph (or both?)
        if output_file:
            plt.savefig(output_file)
        if show_graph:
            plt.show()

        plt.close()


if __name__ == '__main__':
    data = scipy.random.random((4, 21))*10.0
    anndict = {'alpha': 0.5,                    # half transparent
               'color': 'blue',
               'horizontalalignment': 'center', # or 'right' or 'left'
               'rotation': 90.0,
               'style': 'italic',               # or 'normal' or 'oblique'
               'weight': 'bold',                # 'regular', 'light', 'black'
               'zorder': 100                    # not sure what this does
              }
    anndict2 = {'color': 'green',
                'weight': 'light',              # 'regular', 'light', 'black'
                'zorder': 1                     # not sure what this does
               }
    momag_bins = (4.5, 5.0, 5.5, 6.0, 6.5)
    range_bins = (0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100)
    pct_limits = (0, 8)
    plot_annloss_deagg_distmag(data, momag_bins, range_bins, pct_limits,
                               title='plot_annloss_deagg_distmag()',
                               output_file='test.png',
                               show_graph=True,
                               annotate=[(0.5, 0.5, 'test annotate', anndict),
                                         (0.25, 0.25, '"no dict"'),
                                         (0.75, 0.75, 'another test', anndict2)])
