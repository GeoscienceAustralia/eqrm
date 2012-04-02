#!/usr/bin/env python

"""
A plot module to draw a GMT map only (no data).
 
Copyright 2007 by Geoscience Australia

"""


import os
import tempfile
import shutil

import eqrm_code.plotting.plot_config as cfg
import eqrm_code.plotting.util_get_xyz_extent as ugxe
import eqrm_code.plotting.util_gmt_placement as ugp
import eqrm_code.plotting.utilities as util
import eqrm_code.plotting.util_gmt_annotation as uga
import eqrm_code.plotting.utilities as util


def plot_gmt_map(extent, output_file, title=None, np_posn=None,
                 s_posn=None, annotate=[], show_graph=False):
    """A function to draw a GMT map, no data, just annotations.
    
    extent       the map extent (ll_lat, ll_lon, ur_lat, ur_lon)
    output_file  path to file that should be generated (*.png, *.eps, etc)
    title        string used to title the plot
    np_posn      position tuple or code string for north pointer placement,
                 one of:
                     'C'   - centre of plot
                     'NE'  - inside plot, northeast corner
                     'CE'  - inside plot, centre of east edge
                     'NNE' - outside plot, north of NE corner
                     'ENE' - outside plot, east of NE corner
                      etc (see the documentation for 'placement')
    s_posn       code string for scale placement
                     see examples for 'np_posn' above
    annotate     list of user annotations:
                     if None, no user or system annotations
                     if [],   only system annotations
                     else     system and user annotations
    show_graph   if True try to display final image in system-independant way

    Probably useful only for testing.

    """

    # unpack the extent
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # create a scratch directory for ephemeral files
    tmp_dir = tempfile.mkdtemp(prefix='plot_gmt_map_')

    # set up the GMT default values
    util.set_gmt_defaults(tmp_dir)

    # handle optional parameters
    if title is None:
        title = ''

    # think of a postscript filename
    my_ps_file = os.path.join(tmp_dir, 'data.ps')

    # draw the coast
    util.do_cmd('pscoast %s -K -JM%fc -Df -W -S192/216/255 >> %s'
                % (r_opt, cfg.MapWidthCentimetres, my_ps_file))

    # draw the rest of the map
    t_opt = ''
    if np_posn:
        t_opt = ugp.get_northpointer_placement(np_posn, extent)
    l_opt = ''
    if s_posn:
        l_opt = ugp.get_scale_placement(s_posn, extent)

    # do annotations
    if annotate is not None:
        j_opt = '-JM%fc' % cfg.MapWidthCentimetres
        ok_opt = '-K -O'
        jok_opt = '%s %s' % (j_opt, ok_opt)
        uga.generated_annotation(tmp_dir, my_ps_file, extent,
                                 cfg.MapWidthCentimetres, jok_opt)
        uga.user_annotation(tmp_dir, my_ps_file, extent, j_opt, ok_opt, annotate)

    util.do_cmd('psbasemap %s -K -O -JM%fc -Ba30m:".%s":WSen -Bg30m %s %s >> %s'
                % (r_opt, cfg.MapWidthCentimetres, title, t_opt, l_opt,
                   my_ps_file))

    cmd = ('psimage austgov-stacked.sun -O -W3.0/2.0 -C144.200/-38.800 '
           '-F1.0,255/0/0 >> %s' % my_ps_file)
    util.do_cmd(cmd)

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


