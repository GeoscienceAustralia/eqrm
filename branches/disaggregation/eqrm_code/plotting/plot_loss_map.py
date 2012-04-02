#!/usr/bin/env python

"""
Plot a loss map from randomly sampled data.

usage: plot_loss_map <datafile> <outputmap> [<bins> [<savefile>]]

The data is 'gridded' into a user-selected number of bins with multiple
values in one bin being summed.

The <datafile> file is assumed to exist in the <mumble> input directory.

The <outputmap> and <savefile> files will be generated in the <mumble>
output directory.

"""


import os

import calc_sum_xyz as csx
import plot_gmt_xyz as pgx
import calc_ignore_xyz as cix
import utilities as util


def obsolete_plot_loss_map(indir, data, out_dir, output_file, save_file=None,
                  title=None, np_posn=None, s_posn=None, cb_label=None,
                  bins=100, scale=1.0, ignore=None, invert=False,
                  colourmap=None):
    """Plot a loss map from randomly sampled data.

    indir        input directory
    data         name of the data file to plot (in indir)
    out_dir      general output directory
    output_file  name of map output file to create in 'out_dir' directory
    save_file    name of map data output file to create in 'out_dir' directory
    title        title to put on the graph
    np_posn      place to put a north pointer symbol at
    s_posn       place to put a length scale at
    cb_label     label text to put on the colour bar
    bins         either scalar for bins in each direction or (bin_x, bin_y)
    scale        amount to scale the data by
    ignore       the value to ignore if value <= ignore
    colourmap    the base colourmap to use

    """

    # read in and scale XYZ data
    xyz = csx.calc_sum_xyz(data, scale=scale, bins=bins, invert=invert)

    # ignore everything less than an 'ignore' value?
    if ignore is not None:
        xyz = cix.calc_ignore_xyz(xyz, ignore)

    # if we want a save of actual plotted data, do it here
    if save_file:
        save_outfile = os.path.join(out_dir, save_file)
        # write 'xyz' data to 'save_outfile' here

    # generate the plot output required
    plot_outfile = os.path.join(out_dir, output_file)
    pgx.plot_gmt_xyz(xyz, plot_outfile, bins=bins,
                     title=title, cb_label=cb_label,
                     np_posn=np_posn, s_posn=s_posn,
                     colourmap=colourmap)


################################################################################
# Simple harness to run the function as a standalone program using existing
# demo files or a local file.
################################################################################

if __name__ == '__main__':
    import sys
    import getopt
    import eqrm_code.eqrm_filesystem as ef

    def usage(msg=None):
        if msg:
            print(msg+'\n')
        print(__doc__)        # module docstring used
    
    
    def main(argv=None):
        # pick up the input args
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hc:',
                                       ['help', 'colourmap='])
        except getopt.error, msg:
            usage()
            return 1
  
        c_map = None
        for (opt, param) in opts:
            if opt in ['-h', '--help']:
                usage()
                return 0
            if opt in ['-c', '--colourmap']:
                c_map = param
    
        if len(args) < 2 or len(args) > 4:
            usage()
            return 1
   
        datafile = args[0]
        outfile = args[1]
        bins = None
        savefile = None
        if len(args) > 2:
            bins = int(args[2])
            if len(args) > 3:
                savefile = args[2]
        indir = '.'
        outdir = '.'

        # decide if input file is in the demo/... directory
        tmp_path = os.path.join(ef.Demo_Output_ProbRisk_Path, datafile)
        if os.path.isfile(tmp_path):
            indir = ef.Demo_Output_ProbRisk_Path
            outdir = ef.Demo_Output_ProbRisk_Path

        # plot map
        obsolete_plot_loss_map(indir, datafile, outdir, outfile,
                               save_file=savefile,
                               title='Test plot_loss_map.py',
                               np_posn=(145.744,-37.461), s_posn='se',
                               cb_label='$ loss x 1,000,000', scale=1.0e6,
                               bins=150, ignore=0.0, invert=True,
                               colourmap=c_map)

        return 0

    sys.exit(main())


