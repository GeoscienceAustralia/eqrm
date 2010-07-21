#!/usr/bin/env python

"""Routines to handle local named colour maps.

"""


import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


# This list contains the local colormaps.
# Each tupl is (<name>, <cmap_data>).
# in line with the matplotlib colormap naming convention,
# the inverse of the 'xyzzy' map is named 'xyzzy_r'.
LocalColorMaps = [# the colormap used by the hazmap viewers
                  ('hazmap', {'red':   [(0.0, 0.0, 0.0),
                                        (0.5, 1.0, 1.0),
                                        (1.0, 1.0, 1.0)],
                              'green': [(0.0, 1.0, 1.0),
                                        (0.5, 1.0, 1.0),
                                        (1.0, 0.0, 0.0)],
                              'blue':  [(0.0, 0.0, 0.0),
                                        (0.5, 0.0, 0.0),
                                        (1.0, 0.0, 0.0)]}),
                  ('hazmap_r', {'red':   [(0.0, 1.0, 1.0),
                                          (0.5, 1.0, 1.0),
                                          (1.0, 0.0, 0.0)],
                                'green': [(0.0, 0.0, 0.0),
                                          (0.5, 1.0, 1.0),
                                          (1.0, 1.0, 1.0)],
                                'blue':  [(0.0, 0.0, 0.0),
                                          (0.5, 0.0, 0.0),
                                          (1.0, 0.0, 0.0)]}),
                 ]

# default colormap if name not matched
DefaultColormapNameIndex = 0        # first cmap above is default


def get_colormap(colormap_name):
    """Get a local colormap given a name.

    colormap_name - the name of the desired colormap

    Search the system colormap names first, then locals.
    Returns a tuple (name, colormap object).

    The reason why we return the name is that if the supplied name is 
    not recognized, we use a default colormap.

    """

    # if no colour map supplied, use the default
    if colormap_name is None:
        (colormap_name, cm) = LocalColorMaps[DefaultColormapNameIndex]

    # look for a system colormap of this name
    try:
        return (colormap_name,  plt.get_cmap(colormap_name))
    except AssertionError:
        pass

    # try the local maps
    cmap = None
    for (name, cm) in LocalColorMaps:
        if name == colormap_name:
            return (name, mcolors.LinearSegmentedColormap(name, cm))

    # name not recognized, use the default
    (name, cm) = LocalColorMaps[DefaultColormapNameIndex]
    cmap = mcolors.LinearSegmentedColormap(name, cm)
    return name, cmap


