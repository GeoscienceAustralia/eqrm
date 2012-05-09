#!/usr/bin/env python

"""
Description: Place user annotation on a plot.
 
Copyright 2007 by Geoscience Australia

"""


import matplotlib.pyplot as plt


def plot_user_annotation(fig, annotate, fontsize=6):
    """
    Place user annotations on graph.

    fig      handle to open plot
    annotate user annotations
    fontsize size of the annotation text
    
    """
    
    if annotate:
        for ann in annotate:
            if len(ann) == 3:
                (x, y, annstr) = ann
                anndict = {}
            elif len(ann) == 4:
                (x, y, annstr, anndict) = ann
            else:
                (x, y, annstr, anndict, _) = ann
            plt.text(x, y, annstr, fontsize=fontsize,
                     transform=fig.transFigure, **anndict)
