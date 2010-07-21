#!/usr/bin/env python

"""
A plot module to draw contoured XYZ data onto a GMT map.
 
Copyright 2007 by Geoscience Australia

"""


import os
import tempfile
import shutil
import numpy as num

import eqrm_code.plotting.plot_config as cfg
import eqrm_code.plotting.util_get_xyz_extent as ugxe
import eqrm_code.plotting.util_gmt_placement as ugp
import eqrm_code.plotting.util_gmt_annotation as uga
import eqrm_code.plotting.utilities as util


# default colour map
ColourMap = 'hazmap'


def plot_gmt_xyz_contour(data, output_file, title=None,
                         np_posn=None, s_posn=None,
                         cb_label=None, cb_steps=None,
                         colourmap=None, annotate=[], linewidth=1.0,
                         show_graph=False, map_extent=None):
    """A function to take XYZ data and plot contours onto a GMT map.
    
    data         an iterable of values in xyz format (lon, lat, val)
    output_file  path to file that should be generated (*.png, *.eps, etc)
    title        string used to title the plot
    np_posn      code string for north pointer placement, one of:
                     'C'   - centre of plot
                     'NE'  - inside plot, northeast corner
                     'CE'  - inside plot, centre of east edge
                     'NNE' - outside plot, north of NE corner
                     'ENE' - outside plot, east of NE corner
                      etc (see the documentation for 'placement')
    s_posn       code string for scale placement
                     see examples for 'np_posn' above
    cb_label     string containing the label text for the colorbar
                 (if not supplied, no colourbar)
    cb_steps     if supplied is a sequence of discrete values at
                 the colour changes
    colourmap    string containing name of required colormap
    annotate     list of user annotations:
                     if None, no user or system annotations
                     if [],   only system annotations
                     else system and user annotations
    linewidth    width of countour lines in pixels
    show_graph   if True try to display final image in system-independant way
    map_extent   set the extent of the displayed map if supplied
                 (get extent from data if not supplied)

    """

    # create a scratch directory for ephemeral files
    tmp_dir = tempfile.mkdtemp(prefix='plot_gmt_xyz_contour_')

    # set up the GMT default values
    util.set_gmt_defaults(tmp_dir)

    # handle optional parameters
    if title is None:
        title = ''

    # if no colourmap supplied, use default
    c_map = ColourMap
    if colourmap:
        c_map = colourmap

    # get maximum and minimum values
    max_val = util.max_nan(data[:,2])
    min_val = util.min_nan(data[:,2])

    # get extent of data
    if map_extent:
        extent = map_extent
    else:
        extent = ugxe.get_extent(data, margin=0)
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # set the -J option for Mercator projection
    j_opt = '-JM%fc' % cfg.MapWidthCentimetres

    # write a GMT XYZ file (required by GMT)
    my_xyz_file = os.path.join(tmp_dir, 'data.xyz')
    num.savetxt(my_xyz_file, data)

    # generate CPT file
    my_cpt_file = os.path.join(tmp_dir, 'data.cpt')
    if cb_steps is None:
        cb_steps = []
    if len(cb_steps) > 0:
        util.make_discrete_cpt_from_seq(my_cpt_file, cb_steps)
    else:
        (start, stop, step) = util.get_scale_min_max_step(max_val, min_val)
        cm = util.get_colourmap(c_map)
        util.do_cmd('makecpt -C%s.cpt -T%f/%f/%f > %s'
                    % (cm, start, stop, step, my_cpt_file))

    # think of a postscript filename for plot output
    my_ps_file = os.path.join(tmp_dir, 'data.ps')

    # linewidth checking - if width < 1.0, no lines
    w_opt = '-W%.1f/0' % linewidth
    if linewidth < 1.0:
        w_opt = '-W+1'

    # draw contoured data on map
    util.do_cmd('pscontour %s -K -A- -C%s %s %s -I %s > %s'
                % (my_xyz_file, my_cpt_file, r_opt, j_opt, w_opt,
                   my_ps_file))

    # draw the coast
    util.do_cmd('pscoast %s -K -O %s -Df -W -S192/216/255 >> %s'
                % (r_opt, j_opt, my_ps_file))

    # do annotations
    if annotate is not None:
        ok_opt = '-K -O'
        jok_opt = '%s %s' % (ok_opt, j_opt)
        uga.generated_annotation(tmp_dir, my_ps_file, extent,
                                 cfg.MapWidthCentimetres, jok_opt)
        uga.user_annotation(tmp_dir, my_ps_file, extent, j_opt, ok_opt, annotate)

    # draw the colorbar
    if cb_label:
        x_offset = cfg.MapWidthCentimetres + 0.5 
        util.do_cmd('psscale -K -O -E -C%s -D%.1fc/8.0c/9.0c/0.8c "-B:%s:" >> %s'
                    % (my_cpt_file, x_offset, cb_label, my_ps_file))

    # draw the rest of the map
    t_opt = ''
    if np_posn:
        t_opt = ugp.get_northpointer_placement(np_posn, extent)
    l_opt = ''
    if s_posn:
        l_opt = ugp.get_scale_placement(s_posn, extent)

    util.do_cmd('psbasemap %s -O %s "-Ba30m:.%s:WSen" -Bg30m %s %s >> %s'
                % (r_opt, j_opt, title, t_opt, l_opt, my_ps_file))

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


if __name__ == '__main__':
    def usage(msg=None):
        if msg:
            print(msg+'\n')
        print(__doc__)        # module docstring used
    
    
    def main(argv=None):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
        except getopt.error, msg:
            usage()
            return 1
    
        for (opt, param) in opts:
            if opt in ['-h', '--help']:
                usage()
                return 0
    
        if len(args) != 1:
            usage()
            return 1
    
        datafile = args[0]
        outfile = datafile + '.png'
        do_example(datafile, outfile)

    sys.exit(main())


