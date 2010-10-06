#!/usr/bin/env python

"""
An example of plotting randomly sampled XYVV data in a gridded form.

Can be run as a standalone program:

    example_calc_plot_xyvv <datafile>

"""


import sys
import getopt

import calc_load_xyvv as clx
import plot_gmt_xyz as pgx
import calc_xyvv_percentage as cxp
import calc_grid_sum_xyvs as cgsx
import calc_ignore_xyz as cix


def do_example(datafile, outfile, invert=False, bins=100, ignore=0.0):
    xyvv = clx.calc_load_xyvv(datafile, invert=invert)
    (bins, xyvv) = cgsx.calc_grid_sum_xyvs(xyvv)
    xyz = cxp.calc_xyvv_percentage(xyvv)
    xyz = cix.calc_ignore_xyz(xyz, ignore=ignore)
    pgx.plot_gmt_xyz(xyz, outfile, title='%loss sum binned values',
                     np_posn='NE', s_posn='SE',
                     cb_label='% loss')


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


