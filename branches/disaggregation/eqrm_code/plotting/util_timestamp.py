#!/usr/bin/env python

"""
Description: Place a 'generated at ...' annotation on a plot.
 
Copyright 2007 by Geoscience Australia

"""


import time

import matplotlib.pyplot as plt


def plot_timestamp(fig, x=0.02, y=0.02, fontsize=6):
    """
    Place a 'generated at ...' annotation on an open plot.

    fig      the open plot to annotate
    x        screen coordinate to draw timestamp at
    y        screen coordinate to draw timestamp at
    fontsize size of the annotation text

    """
    
    time_str = 'generated at %s on %s' % (time.strftime('%H:%M:%S'),
                                          time.strftime('%a %d %b %Y'))
    plt.text(0.02, 0.01, time_str, fontsize=fontsize, transform=fig.transFigure)


