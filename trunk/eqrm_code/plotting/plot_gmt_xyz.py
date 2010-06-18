#!/usr/bin/env python

"""
A plot module to draw gridded XYZ data onto a GMT map.
 
Copyright 2007 by Geoscience Australia

"""


import os
import tempfile
import shutil
import scipy
import numpy as num


import eqrm_code.plotting.plot_config as cfg
import eqrm_code.plotting.util_get_xyz_extent as ugxe
import eqrm_code.plotting.util_gmt_placement as ugp
import eqrm_code.plotting.utilities as util
import eqrm_code.plotting.util_gmt_annotation as uga
import eqrm_code.plotting.utilities as util


# default colour map
DefaultColourMap = 'hazmap'


def plot_gmt_xyz(data, output_file, bins=100, title=None, np_posn=None,
                 s_posn=None, cb_label=None, colourmap=None, cb_steps=None,
                 annotate=[], show_graph=False, map_extent=None):
    """A function to take gridded XYZ data and plot onto a GMT map.
    
    data         an iterable of *gridded* values in xyz format (lon, lat, val)
    output_file  path to file that should be generated (*.png, *.eps, etc)
    bins         number of bins in the X direction if a single integer, else
                 expect 2-tuple of integers (bins_x, bins_y)
    title        string used to title the plot
    np_posn      code string for north pointer placement, one of:
                     'C'   - centre of plot
                     'NE'  - inside plot, northeast corner
                     'CE'  - inside plot, centre of east edge
                     'NNE' - outside plot, north of NE corner
                     'ENE' - outside plot, east of NE corner
                      etc (see the documentation for 'placement')
                   OR
                     (lon,lat) tuple
    s_posn       code string for scale placement
                     see examples for 'np_posn' above
    cb_label     string containing the label text for the colorbar
                 (if not supplied, no colourbar)
    colourmap    string containing name of required colormap
                 (a local file 'hazmap.cpt' or GMT name 'cool')
    cb_steps     an iterable of desired discrete steps in the DISCRETE
                 colourmap, or an empty list (code chooses steps), or None
                 which gives the default continuous colourmap
    annotate     list of user annotations:
                     if None, no user or system annotations
                     if [],   only system annotations
                     else     system and user annotations
    show_graph   if True try to display final image in system-independant way
    map_extent   sets the extent of the displayed map if supplied
                 (get extent from data if not supplied)

    """

    # create a scratch directory for ephemeral files
    tmp_dir = tempfile.mkdtemp(prefix='plot_map_')

    # set up the GMT default values
    util.set_gmt_defaults(tmp_dir)

    # handle bins parameter
    try:
        (bins_y, bins_x) = bins
    except TypeError:
        bins_x = bins_y = bins

    # handle optional parameters
    if title is None:
        title = ''

    c_map = DefaultColourMap
    if colourmap:
        c_map = colourmap
    c_map = util.get_colourmap(c_map)

    # get extent of data (user-specified, or we get from data)
    if map_extent:
        extent = map_extent
    else:
        extent = ugxe.get_extent(data, margin=0)
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # get max NON-NAN value from XYZ data
    max_val = util.max_nan(data[:,2])
    min_val = util.min_nan(data[:,2])

    # write a GMT XYZ file
    my_xyz_file = os.path.join(tmp_dir, 'data.xyz')
    scipy.savetxt(my_xyz_file, data)

    # convert XYZ to GRD file
    my_grd_file = os.path.join(tmp_dir, 'data.grd')
    util.do_cmd('xyz2grd %s %s -I%d+/%d+ -G%s'
                % (my_xyz_file, r_opt, bins_x, bins_y, my_grd_file))

    # generate CPT file
    my_cpt_file = os.path.join(tmp_dir, 'data.cpt')
    if cb_steps is None:
        util.do_cmd('grd2cpt %s -C%s -Z > %s'
                    % (my_grd_file, c_map, my_cpt_file))
    elif hasattr(cb_steps, '__iter__'):
        if len(cb_steps) == 0:           # code chooses steps
            (start, stop, step) = util.get_scale_min_max_step(max_val, min_val)
            util.do_cmd('makecpt -C%s.cpt -T%f/%f/%f > %s'
                        % (c_map, start, stop, step, my_cpt_file))
        else:                               # user chooses steps
            util.make_discrete_cpt(my_cpt_file, c_map, cb_steps)
    else:
        msg = "cb_steps param must be None or list: got %s" % type(cb_steps)
        raise RuntimeError(msg)

    # think of a postscript filename
    my_ps_file = os.path.join(tmp_dir, 'data.ps')

    # draw GRD data on map
    util.do_cmd('grdimage %s -K %s -JM%fc -C%s -Q > %s'
                % (my_grd_file, r_opt, cfg.MapWidthCentimetres,
                   my_cpt_file, my_ps_file))

    # draw the coast
    util.do_cmd('pscoast %s -K -O -JM%fc -Df -W -S192/216/255 >> %s'
                % (r_opt, cfg.MapWidthCentimetres, my_ps_file))

    # draw the rest of the map
    t_opt = ''
    if np_posn:
        t_opt = ugp.get_northpointer_placement(np_posn, extent)
    l_opt = ''
    if s_posn:
        l_opt = ugp.get_scale_placement(s_posn, extent)

    util.do_cmd('psbasemap %s -K -O -JM%fc -Ba30m:".%s":WSen -Bg30m %s %s >> %s'
                % (r_opt, cfg.MapWidthCentimetres, title, t_opt, l_opt, my_ps_file))

    # do annotations
    if annotate is not None:
        j_opt = '-JM%fc' % cfg.MapWidthCentimetres
        ok_opt = '-K -O'
        jok_opt = '%s %s' % (j_opt, ok_opt)
        uga.generated_annotation(tmp_dir, my_ps_file, extent,
                                 cfg.MapWidthCentimetres, jok_opt)
        uga.user_annotation(tmp_dir, my_ps_file, extent, j_opt, ok_opt, annotate)

    # figure out scale skip from max data value
    skip = util.get_scale_skip(max_val)

    # draw the colorbar
    if cb_label:
        x_offset = cfg.MapWidthCentimetres + 0.5
        util.do_cmd('psscale -O -C%s -D%.1fc/8.0c/9.0c/0.8c -B%f:"%s": >> %s'
                    % (my_cpt_file, x_offset, skip, cb_label, my_ps_file))

    # convert PS to required type
    (_, file_extension) = output_file.rsplit('.', 1)
    try:
        t_opt = util.Extension2TOpt[file_extension.lower()]
    except KeyError:
        raise RuntimeError("Can't handle plot outputfile type: %s" %
                           file_extension)

    util.do_cmd('ps2raster %s -A -T%s' % (my_ps_file, t_opt))
    (my_output_file, _) = my_ps_file.rsplit('.', 1)
    my_output_file += '.' + file_extension
    shutil.copyfile(my_output_file, output_file)

    # if it's required to show the graph ...
    # TODO: Experimental - leave?
    if show_graph:
        import sys
        if sys.platform == 'win32':
            os.startfile(my_output_file)
        else:
            import subprocess
            try:
                subprocess.Popen(['xdg-open', my_output_file])
            except OSError:
                print("Sorry, the 'xdg-open' application is required to "
                      "automatically display images.\nYou can see the image "
                      "in file %s." % output_file)

    # remove the temp directory
    shutil.rmtree(tmp_dir)


