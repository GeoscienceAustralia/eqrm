#!/usr/bin/env python

"""
An example of plotting randomly sampled data in a gridded form.

Can be run as a standalone program:

    example_calc_plot_sum_xyz_map.py <datafile>

"""


import sys
import getopt

import calc_sum_xyz as csx
import plot_gmt_xyz as pgx


def do_example(datafile, outfile, invert=False):
    xyz = csx.calc_sum_xyz(datafile, scale=1e6, invert=invert)
    pgx.plot_gmt_xyz(xyz, outfile, #bins_x,
                     title='Loss sum binned values',
                     np_posn='NE', s_posn='SE',
                     cb_label='$ loss x 1,000,000')


################################################################################
# Simple harness to run the example as a standalone program:
################################################################################

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


