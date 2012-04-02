#!/usr/bin/env python

"""
Plot scenario loss statistics.

usage: plot_scen_loss_stats <datafile> <outputmap> [<bins> [<savefile>]]

The <datafile> file is assumed to exist in the <mumble> input directory.

The <outputmap> and <savefile> files will be generated in the <mumble>
output directory.

"""


import os
import scipy

import eqrm_code.convert_Py2Mat_Risk as cpr
import eqrm_code.output_manager as om
import eqrm_code.plotting.calc_xy_histogram as cxh
import eqrm_code.plotting.plot_barchart as pb
import eqrm_code.plotting.utilities as util


def make_scen_loss_stats_filename(site_tag):
    """Make a scenarion loss statistics filename given:

    site_tag      event descriptor string

    """

    return '%s_huh.txt' % site_tag


def plot_scen_loss_stats(input_dir, site_tag, output_dir,
#                         plot_file, save_file=None,
                         pre89=False, dollars89=False, resonly=False):
    """Plot a scenario loss statistics graph from scenario data.

    input_dir  input directory
    site_tag   event descriptor string
    output_dir general output directory
##    plot_file  name of map output file to create in 'output_dir' directory
##    save_file  name of map data output file to create in 'output_dir' directory
    pre89      if True consider buildings that existed before 1989 only
    dollars89  if True express dollar values in pre-1989 dollars
    resonly    if True consider only residential buildings

    """

    # read in raw data
    data = cpr.obsolete_convert_Py2Mat_Risk(site_tag)

    # filter data depending on various flags
    temp_ecloss = data.ecloss
    temp_bval2 = data.ecbval2
    
    if pre89:
        if resonly:
            take_array = [x[2] and x[11] for x in data.structures]
            temp_ecloss = scipy.take(data.ecloss, take_array)
            temp_bval2 = scipy.take(data.ecbval2, take_array)
        else:
            take_array = [x[2] for x in data.structures]
            temp_ecloss = scipy.take(data.ecloss, take_array)
            temp_bval2 = scipy.take(data.ecbval2, take_array)
    else:
        if resonly:
            take_array = [x[11] == 'RES1' for x in data.structures]
            temp_ecloss = scipy.take(data.ecloss, resonly_array)
            temp_bval2 = scipy.take(data.ecbval2, resonly_array)
        else:
            temp_ecloss = data.ecloss
            temp_bval2 = data.ecbval2

    # which dollars does user want
    doll_str = 'in 2002 dollars'
    cvt_doll = 1.0
    if dollars89:
        doll_str = 'in 1989 dollars'
        cvt_doll = 1/1.37

    f_ecloss = cvt_doll * temp_ecloss
    f_bval2 = cvt_doll * temp_bval2

    f_aggloss_bill = scipy.sum(f_bval2) / 1e9
    
    print('f_ecloss=%s' % str(f_ecloss))
    print('f_bval2=%s' % str(f_bval2))
    print('f_aggbval2_bill=%s' % str(f_aggloss_bill))

    h_data = cxh.calc_xy_histogram(f_aggloss_bill, bins=10)
    plot_out = os.path.join(output_dir, 'test1.png')
    title = 'Newc89 agg loss, pre89, 1989 dollars'
    xlabel = '$ %s (x 1e+9)' % doll_str
    pb.plot_barchart(h_data, output_file=plot_out, title=title,
                     xlabel=xlabel, ylabel='frequency',
                     xrange=None, yrange=None, grid=True,
                     show_graph=True, annotate=[])


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
            opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
        except getopt.error, msg:
            usage()
            return 1
  
        for (opt, param) in opts:
            if opt in ['-h', '--help']:
                usage()
                return 0
    
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
        plot_scen_loss_stats(indir, 'newc', outdir, outfile)

        return 0

    sys.exit(main())


