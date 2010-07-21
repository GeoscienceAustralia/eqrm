#!/usr/bin/env python

"""
A plot module to sample random data into a hexgrid and display on a map.
 
Copyright 2007 by Geoscience Australia

"""


import os
import sys
import re
import time
import scipy

import eqrm_code.plotting.util_get_xyz_extent as gxe
import eqrm_code.plotting.util_timestamp as pts
import eqrm_code.plotting.util_user_annotation as pua
import eqrm_code.plotting.util_colormaps as uc
import eqrm_code.plotting.util_northpointer as unp

from fillocean import *


# the land fill colour
FILL_COLOUR = '#E0E0E0'

# fudge around a matplotlib problem - always define 'linewidth'
DEFAULT_LINEWIDTH = 0.01


def plot_hexbin_map(map_data, bins=100, title='', output_file=None, cblabel='',
                    cbformat='%.1f', show_graph=False, grid=True, colormap=None,
                    annotate=[], scale=None, np_posn=None,
                    hexbin_args=None, map_extent=None):
    """Plot data into a hexgrid  with an underlay map.

    Inputs:
    map_data       (nx3) array containing the data to plot. The first column
                   contains the latitude of a point, the second column contains
                   the longitude and the third column is the value to bin&plot.
    bins           Either a scalar (# bins in X and Y directions) or (nx, ny).
    title          the graph title string
    output_file    path of file to save plot picture in
    cblabel        label to display on the colorbar
    cbformat       format string used to show colormap values
    show_graph     show graph on screen if True
    grid           draw a grid on graph if True
    colormap       if supplied, the colormap name to use (string)
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
    scale          a tuple containing data used to draw a scale:
                   (posn, length, scale_args)
                   where 'posn'       is where to place scale, one of:
                                          'NW', 'NE', 'SW', 'SE'
                                          (case-insensitive)
                     and 'scale_args' is an optional kwargs dictionary
                   see drawmapscale() function at 
                   http://matplotlib.sourceforge.net/basemap/doc/html/api/basemap_api.html#mpl_toolkits.basemap.Basemap.drawmapscale
                   to see values in scale_args
    np_posn        position tuple or a string describing pointer position:
                       'NW', 'NE', 'SW' or 'SE'
                       (case-insensitive)
    hexbin_args    is a dictionary of hexbin() parameters
                   if not supplied, assume {'gridsize': 100,
                                            'reduce_C_function': scipy.sum
                                           }
                   Note: if hexbin_args is supplied but key 'reduce_C_function'
                   isn't supplied in dictionary, insert 'scipy.sum' function
                   Note: allowed values are documented at:
                         http://matplotlib.sourceforge.net/api/pyplot_api.html
    map_extent     sets the extent of the displayed map if supplied
                   (get extent from the data if not supplied)

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
    from mpl_toolkits.basemap import Basemap
    from matplotlib.mlab import griddata

    # create a 'binned' plot on a map
    if output_file or show_graph:
        # decide on the colormap to use
        (cmap_name, my_cmap) = uc.get_colormap(colormap)

        # set the hexbin params
        if hexbin_args is None:
            hexbin_args = {'gridsize': 100,
                           'reduce_C_function': scipy.sum,
                           'linewidth': DEFAULT_LINEWIDTH}

        try:
            _ = hexbin_args['reduce_C_function']
        except KeyError:
            hexbin_args['reduce_C_function'] = scipy.sum

        # here we fiddle with 'linewidth' to get around a bug in plotting
        # if linewidth not set, hex bins overlap each other
        # force linewidth to a small value if not specified
        try:
            _ = hexbin_args['linewidth']
        except KeyError:
            hexbin_args['linewidth'] = DEFAULT_LINEWIDTH


        # if user doesn't define 'edgecolors' at all, use default
        hexbin_args['edgecolors'] = hexbin_args.get('edgecolors', FILL_COLOUR)

        # get extent of point data
        if map_extent:
            extent = map_extent
        else:
            extent = gxe.get_extent(map_data, margin=5)
        (ll_lat, ll_lon, ur_lat, ur_lon) = extent

        # start the plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
            
        # draw the map
        m = Basemap(projection='cyl', llcrnrlat=ll_lat, urcrnrlat=ur_lat,
                    llcrnrlon=ll_lon, urcrnrlon=ur_lon, resolution='h',
                    suppress_ticks=False, area_thresh=0.5)

#        m = Basemap(projection='cass', llcrnrlat=ll_lat, urcrnrlat=ur_lat,
#                    llcrnrlon=ll_lon, urcrnrlon=ur_lon, resolution='h',
#                    lat_0=(ll_lat+ur_lat)/2.0, lon_0=(ll_lon+ur_lon)/2.0,
#                    suppress_ticks=False) #, area_thresh=0.5)

        # draw hexbin data on map
        plt.hexbin(map_data[:,0], map_data[:,1], map_data[:,2],
                   cmap=my_cmap, zorder=4, **hexbin_args)

        # draw the other minor stuff
        m.fillcontinents(color=FILL_COLOUR, zorder=2)
        m.drawcoastlines(linewidth=0.25, color='k', zorder=5)
        m.drawmapboundary()

        cb = plt.colorbar(cmap=my_cmap, format=cbformat)
        cb.set_label(cblabel)
        
        plt.xlabel('longitude', fontsize=8)
        plt.ylabel('latitude', fontsize=8)

        # if user asked for a NORTH pointer
        if np_posn:
            unp.plot_northpointer(m, (ll_lat, ll_lon, ur_lat, ur_lon),
                                  np_posn)

        # add graph 'furniture'
        plt.title(title)
        plt.grid(grid, color='#C0C0C0', linestyle='-', linewidth=0.25)

        # add system annotations: time generated, etc
        if isinstance(annotate, list):
            pts.plot_timestamp(fig)

        # add user annotations, if any
        pua.plot_user_annotation(fig, annotate)

        # show or save graph (or both?)
        if output_file:
            plt.savefig(output_file, dpi=300)
        if show_graph:
            plt.show()

        plt.close()


if __name__ == '__main__':
    import calc_load_data as cld

    # filename with test data
    filename = 'lat_long_eloss.csv.SAVE'
    #filename = 'lat_long_eloss.csv'
    
    # get data from the file
    result = cld.calc_load_data(filename, invert=True)

    # strip out values > 250,000,000
    #result = result[scipy.nonzero(result[:,2] < 250000000), :][0]

    value_scale = 1.0e6
    result[:,2] = result[:,2] / value_scale

    hexbin_args = {#'gridsize': 100,
#                   'reduce_C_function': scipy.sum,
#                   'linewidth': 0.5, 'edgecolors': None,
#                   'fill_color': 'r',
                   'bins': 100,
                  }

    scale_args = ('se', 100)

    # test the plot routine
    plot_hexbin_map(result, bins=10, title='Test of plot_hexbin_map()\nsecond line',
                    output_file='plot_hexbin_map.png', 
                    cblabel='Dollar loss (x %d)' % int(value_scale), cbformat='%.1f',
# to change the colorbar scheme
#                    colormap='gist_rainbow_r',
#                    colormap='Reds',
#                    colormap='jet_r',
#                    colormap='hot_r',
#                    colormap='cool',
#                    colormap='gray_r',
#                    colormap='gist_yarg',
                    colormap='hazmap',
                    show_graph=True, grid=True, hexbin_args=hexbin_args,
                   np_posn='NE')
