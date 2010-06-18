#!/usr/bin/env python

"""
A plot module to draw an XYZ image and contour lines onto a GMT map.
 
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
DefaultColourmap = 'hazmap.cpt'


def plot_gmt_xyz_image_contour(data, output_file, title=None, colourmap=None,
                               cb_label=None, cb_steps=None, annotate=[],
                               show_graph=False, bin_sum=False,
                               map_extent=None):
    """Plot XYZ data as a 'heatmap' and contours onto a GMT map.
    
    data         an iterable of values in xyz format (lon, lat, val)
                 (must be 'binned' XYZ data)
    output_file  path to file that should be generated (*.png, *.eps, etc)
    title        string used to title the plot
    colourmap    name of the colourmap to use, may be name of *.cpt file or 
                 internal GMT colourmap name
    cb_label    label on colourmap legend
    cb_steps     sequence of contour values (default is no contours drawn)
    annotate     list of user annotations:
                     if None, no user or system annotations
                     if [],   only system annotations
                     else     system and user annotations
                 (see documentation for form of user annotations)
    show_graph   if True try to display final image in system-independant way
    bin_sum      True if values in grid bin are to be summed (default: mean)
    map_extent   sets the extent of the displayed map if supplied
                 (get extent from data if not supplied)

    """

    # create a scratch directory for ephemeral files
    tmp_dir = tempfile.mkdtemp(prefix='plot_gmt_xyz_image_contour_')

    # use XYZ data bin numbers
    bins = util.get_xyz_bin_inc(data, 1.0e-4)
    if bins is None:
        raise RuntimeError("plot_gmt_xyz_image_contour(): "
                           "XYZ data has no implicit binning")
    (x_bins, y_bins) = bins
    x_inc = '%d+' % x_bins
    y_inc = '%d+' % y_bins

    # set up the default GMT environment
    util.set_gmt_defaults(tmp_dir)

    # handle optional parameters
    if title is None:
        title = ''

    if colourmap is None:
        colourmap = DefaultColourmap

    # get maximum/minimum values
    max_val = num.max(data[:,2])
    min_val = num.min(data[:,2])

    # get extent of data
    if map_extent:
        extent = map_extent
    else:
        extent = ugxe.get_extent(data, margin=0)
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # set the -J option for Mercator projection
    j_opt = '-JM%fc' % cfg.MapWidthCentimetres

    # write a GMT XYZ *file* (required by GMT)
    tmp_xyz = os.path.join(tmp_dir, 'data.xyz')
    num.savetxt(tmp_xyz, data)

    # create GRD file from XYZ data
    tmp_grd = os.path.join(tmp_dir, 'data.grd')
    a_opt = ''
    if bin_sum:
        a_opt = '-A'
    util.do_cmd('xyz2grd %s -G%s -I%s/%s -F %s %s'
                % (tmp_xyz, tmp_grd, x_inc, y_inc, r_opt, a_opt))

    # generate CPT file
    tmp_cpt = os.path.join(tmp_dir, 'data.cpt')
    if cb_steps is None:
        cb_steps = []
    if len(cb_steps) > 0:
        util.make_discrete_cpt_from_seq(tmp_cpt, cb_steps)
    else:
        (start, stop, step) = util.get_scale_min_max_step(max_val, min_val)
        cm = util.get_colourmap(c_map)
        util.do_cmd('makecpt -C%s.cpt -T%f/%f/%f > %s'
                    % (cm, start, stop, step, tmp_cpt))

    # think of a postscript filename for plot output
    tmp_ps = os.path.join(tmp_dir, 'data.ps')

    # draw image of gridded data
    util.do_cmd('grdimage %s -K -C%s %s -Q -Sc -Ei > %s'
                % (tmp_grd, tmp_cpt, j_opt, tmp_ps))

    # draw contours on the image
    if contours:
        # make a contour file
        tmp_cnt = os.path.join(tmp_dir, 'data.cnt')
        fd = open(tmp_cnt, 'w')
        for n in contours:
            fd.write('%f A\n' % n)
        fd.close()

        # draw the contours
        util.do_cmd('grdcontour %s -K -O -C%s %s %s >> %s'
                    % (tmp_grd, tmp_cnt, j_opt, r_opt, tmp_ps))

    # draw the coast
    util.do_cmd('pscoast %s -K -O %s -Df -W -S192/216/255 >> %s'
                % (r_opt, j_opt, tmp_ps))

    # draw the colorbar
    if cb_label:
        x_offset = cfg.MapWidthCentimetres + 0.5 
        util.do_cmd('psscale -K -O -E -C%s -D%.1fc/8.0c/9.0c/0.8c "-B:%s:" >> %s'
                    % (tmp_cpt, x_offset, cb_label, tmp_ps))

    # do annotations
    if annotate is not None:
        ok_opt = '-K -O'
        jok_opt = '%s %s' % (ok_opt, j_opt)
        uga.generated_annotation(tmp_dir, tmp_ps, extent,
                                 cfg.MapWidthCentimetres, jok_opt)
        uga.user_annotation(tmp_dir, tmp_ps, extent, j_opt, ok_opt, annotate)

    # draw the rest of the map
    util.do_cmd('psbasemap %s -O %s "-Ba30m:.%s:WSen" -Bg30m >> %s'
                % (r_opt, j_opt, title, tmp_ps))

    # convert PS to required type
    (_, file_extension) = output_file.rsplit('.', 1)
    try:
        t_opt = util.Extension2TOpt[file_extension.lower()]
    except KeyError:
        raise RuntimeError("Can't handle plot outputfile type: %s" %
                           file_extension)

    util.do_cmd('ps2raster %s -A -T%s' % (tmp_ps, t_opt))
    (tmp_output, _) = tmp_ps.rsplit('.', 1)
    tmp_output += '.' + file_extension
    shutil.copyfile(tmp_output, output_file)

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
    import sys

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


