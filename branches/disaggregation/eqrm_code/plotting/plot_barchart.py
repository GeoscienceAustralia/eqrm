#!/usr/bin/env python

"""
A module to plot a barchart with one series of data.
 
Copyright 2007 by Geoscience Australia

"""


import os
import sys

import eqrm_code.plotting.util_timestamp as pts
import eqrm_code.plotting.util_user_annotation as pua
import eqrm_code.plotting.utilities as util


def plot_barchart(data, output_file=None, title='', xlabel='', ylabel='',
                  xrange=None, yrange=None, grid=True, show_graph=False,
                  bin_width=None, bardict=None, annotate=[]):
    """Plot a barchart.  Optionally save a file or show the graph (or both).

    Inputs:
    data           (nx2) array containing the barchart data. The first column
                   contains the X ordinal and the second column contains the
                   height of the bar
    output_file    path of file to save plot picture in
    title          the graph title string, if supplied
    xlabel         label to put on the X axis
    ylabel         label to put on the Y axis
    xrange         a scalar or iterable indicating min[,max] X value to plot
    yrange         a scalar or iterable indicating min[,max] Y value to plot
    grid           draw a grid on graph if True
    show_graph     show graph on screen if True
    bin_width      width of the bins
    bardict        a dictionary containing extra parameters to the
                   matplotlib.pyplot.bar() routine.  Params are defined at
     http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.bar
    annotate       an iterable like [(x, y, ann, dict), ...] where
                       x    is X screen coordinate
                       y    is Y screen coordinate
                       ann  is the annotation string to display at (x, y)
                       dict is a dictionary of key/value pairs as documented at
                            matplotlib.sourceforge.net/api/pyplot_api.html
                            (this is optional)
                   NOTE: if annotate=None is used, no annotation occurs.
                         if annotate=[] is used, auto annotation is generated:
                             timestamp
                             X and Y range limits

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

    # create the plot if we want a file or must show it
    if output_file or show_graph:
        fig = plt.figure()
        ax = fig.add_subplot(111)
       
        # get bardict into correct form for bar() call below
        bar_kwargs = {}
        if bardict:
            bar_kwargs = bardict

        # plot the data
        if bin_width:
            plt.bar(data[:,0], data[:,1], width=bin_width, align='center',
                    **bar_kwargs)
        else:
            plt.bar(data[:,0], data[:,1], align='center', **bar_kwargs)

        # set X and Y range limits
        xrange = util.get_canonical_range(xrange)
        yrange = util.get_canonical_range(yrange)
        if xrange:
            plt.xlim(xrange)
        if yrange:
            plt.ylim(yrange)

        # do X and Y labels
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # add graph 'furniture'
        if title:
            plt.title(title)
        plt.grid(grid)

        # add system annotations: time generated, etc
        if isinstance(annotate, list):
            pts.plot_timestamp(fig)

        # add range limits annotations
        if annotate is None:
            annotate = []
        if xrange:
            annotate.append((0.02, 0.05,
                             'X range forced to (%.2f,%.2f)' % xrange))
        if yrange:
            annotate.append((0.02, 0.03,
                              'Y range forced to (%.2f,%.2f)' % yrange))

        # add user annotations, if any
        pua.plot_user_annotation(fig, annotate)

        # show or save graph (or both?)
        if output_file:
            plt.savefig(output_file)
        if show_graph:
            plt.show()

        plt.close()

if __name__ == '__main__':
    import scipy

    # fake up some data
    data = scipy.array([[1,1],[2,2.5],[3,4.5],[4,4.0],[5,2.5],[6,1.0]])
    xrange = None
    yrange = None

    # plot the data
    plot_barchart(data, output_file='test.png', title='Example plot_barchart()',
                  xlabel='xlabel', ylabel='ylabel', xrange=xrange, yrange=yrange,
                  grid=True, show_graph=True, annotate=[])


