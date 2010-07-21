#!/usr/bin/env python

"""
An example of plotting randomly sampled data in a contoured form.

Can be run as a standalone program:

    example_calc_plot_gmt_contour.py <datafile>

"""


import sys
import getopt

import calc_load_data as cld
import plot_gmt_xyz_image_contour as pgxic


def do_example(datafile, outfile, invert=False):
    contours = [0.10, 0.15, 0.20, 0.30, 0.40, 0.50]

    data = cld.calc_load_data(datafile, invert=invert)
    pgxic.plot_gmt_xyz_image_contour(data, outfile,
                                     bin_sum=True,
                                     cb_label='Acceleration (g)',
                                     #cb_steps=contours,
                                     contours=contours,
                                     title='Bedrock Hazard, RP=?, RSA=?')


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


