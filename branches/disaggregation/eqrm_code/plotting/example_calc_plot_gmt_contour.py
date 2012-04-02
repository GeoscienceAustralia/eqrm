#!/usr/bin/env python

"""
An example of plotting randomly sampled data in a contoured form.

Can be run as a standalone program:

    example_calc_plot_gmt_contour.py <datafile>

"""


import sys
import getopt

import calc_load_data as cld
import plot_gmt_xyz_contour as pgxc


def do_example(datafile, outfile, invert=False):
#    ignore_value = 0.025
#
    annotations = []
#    if ignore_value:
#        annotations.append(('text', (143.6,-37.10),
#                            'Values <= %.2f are ignored' % ignore_value))

    data = cld.calc_load_data(datafile, invert=invert)
    # TODO : add call to calc_ignore
    pgxc.plot_gmt_xyz_contour(data, outfile,
                              title='Bedrock Hazard, RP=?, RSA=?',
                              np_posn='NE', s_posn='SE',
                              cb_label='Acceleration (g)',
                              cb_steps=[0.1,0.15,0.20,0.30,0.40,0.50],
                              annotate=annotations, linewidth=0.0)


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


