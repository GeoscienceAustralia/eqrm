#!/usr/bin/env python

"""
An example of plotting randomly sampled data in a gridded form.

Can be run as a standalone program:

    example_calc_plot_mean_xyz_map.py <datafile>

"""


import sys
import getopt

import calc_mean_xyz as cmx
import plot_gmt_xyz as pgx


def do_example(datafile, outfile, invert=False):
    annotations = [('text', (144.5, -37.40),
                    '@;red;example_calc_plot_mean_xyz_map@;;')]
    (bins_x, xyz) = cmx.calc_mean_xyz(datafile, scale=1e3, invert=invert)
    pgx.plot_gmt_xyz(xyz, outfile, bins_x,
                     title='Loss mean binned values',
                     np_posn='NE', s_posn='SE',
                     cb_label='$ loss x 1,000',
                     annotate=annotations)


if __name__ == '__main__':
    def usage(msg=None):
        if msg:
            print(msg+'\n')
        print(__doc__)        # module docstring used
    
    
    def main(argv=None):
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hi', ['help', 'invert'])
        except getopt.error, msg:
            usage()
            return 1
   
        invert = False
        for (opt, param) in opts:
            if opt in ['-h', '--help']:
                usage()
                return 0
            if opt in ['-i', '--invert']:
                invert = True
    
        if len(args) != 1:
            usage()
            return 1
    
        datafile = args[0]
        outfile = datafile + '.png'
        do_example(datafile, outfile, invert=invert)


    sys.exit(main())


