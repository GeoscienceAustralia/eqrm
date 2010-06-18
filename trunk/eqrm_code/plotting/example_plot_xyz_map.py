#!/usr/bin/env python

"""
An example of plotting randomly sampled data in a gridded form.

Can be run as a standalone program:

    example_plot_xyz_map.py <datafile>

"""


import sys
import getopt

import calc_load_xyz as clx
import plot_gmt_xyz as pgx


def do_example(datafile, outfile, invert=False):
    annotations = [('text', (144.0, -37.10),
                    '@;blue;cb_steps = (0.01,0.05,0.1,0.2,0.3,0.4), bins = 200@;;')]
    bins = 200
    #cb_steps = None
    #cb_steps = ()
    cb_steps = (0.01,0.05,0.1,0.2,0.3,0.4)
    data = clx.calc_load_xyz(datafile, invert=invert)
    pgx.plot_gmt_xyz(data, outfile, bins=bins,
                     title='example_plot_xyz_map.py',
                     np_posn='NE', s_posn='SE',
                     cb_label='$ loss x 1,000',
                     colourmap='hazmap',
                     cb_steps=cb_steps,
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


