#!/usr/bin/env python

"""
Plot an earthquake hazard map from gridded data.

Can be run as a standalone program:

    plot_hazard_map.py <datafile> <outputmap> [<savefile>]

"""


import calc_load_data as cld
import plot_gmt_xyz_contour as pgxc


def obsolete_plot_hazard_map(indir, datafile, out_dir, output_file, save_file=None,
                    title=None, np_posn=None, s_posn=None, cb_label=None,
                    cb_steps=None, invert=False, colourmap=None,
                    annotate=None):
    """Plot a hazard map from gridded data.

    indir       input directory
    data        name of the data file to plot (in indir)
    out_dir     general output directory
    output_file name of map output file to create in 'out_dir' directory
    save_file   name of map data output file to create in 'out_dir' directory
    title       title to put on the graph
    np_posn     place to put a north pointer symbol at
    s_posn      place to put a length scale at
    cb_label    label text to put on the colour bar
                (if not defined, no colour bar)
    cb_steps    sequence of required values in colourbar
    colourmap   the base colourmap to use
    annotate    user annotations required

    """

    if cb_steps is None:
        cb_steps = [0.1,0.15,0.20,0.30,0.40,0.50]

    data = cld.calc_load_data(datafile, invert=invert)
    pgxc.plot_gmt_xyz_contour(data, output_file,
                              title=title, np_posn=np_posn,
                              s_posn=s_posn, cb_label=cb_label,
                              cb_steps=cb_steps, annotate=annotate)


if __name__ == '__main__':
    import sys
    import os
    import getopt
    import eqrm_code.eqrm_filesystem as ef

    def usage(msg=None):
        if msg:
            print(msg+'\n')
        print(__doc__)        # module docstring used
    
    
    def main(argv=None):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hic:',
                                       ['help', 'invert', 'colourmap='])
        except getopt.error, msg:
            usage()
            return 1
   
        invert = False
        colourmap = None
        for (opt, param) in opts:
            if opt in ['-h', '--help']:
                usage()
                return 0
            if opt in ['-i', '--invert']:
                invert = True
            if opt in ['-c', '--colourmap']:
                colourmap = param
    
        if len(args) < 2 or len(args) > 3:
            usage()
            return 1
    
        datafile = args[0]
        output_file = args[1]
        save_file = None
        if len(args) > 2:
            save_file = args[2]
        indir = '.'
        outdir = '.'

        # decide if the input file is in the ../demo directory
        tmp_path = os.path.join(ef.Demo_Output_ProbRisk_Path, datafile)
        if os.path.isfile(tmp_path):
            indir = ef.Demo_Output_ProbRisk_Path
            outdir = ef.Demo_Output_ProbRisk_Path

        obsolete_plot_hazard_map(indir, datafile, outdir, output_file,
                                 save_file=save_file,
                        title='Bedrock Hazard, RP=?, RSA=?', np_posn='NE',
                        s_posn='SE', cb_label='Acceleration (g)',
                        cb_steps=None, invert=invert,
                        colourmap=None, annotate=[])

    sys.exit(main())


