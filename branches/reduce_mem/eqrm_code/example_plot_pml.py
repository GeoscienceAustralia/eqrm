#!/usr/bin/env python

"""
Description: Example of how to use plot_pml.py.
 
Copyright 2007 by Geoscience Australia

"""


import os
import numpy as num
import re

import eqrm_filesystem
import util
import plot_pml


# while we have load_????() functions defined here
__all__ = ['harness_plot_pml']


# we should get this from a parameter (file or *.py)
site_tag = 'newc'

# get regular expression to parse line delimited by whitespace or commas
SplitPattern = re.compile(' +| *, *')


def load_data(filename):
    '''Load a data file of MxN float values into a numpy array.

    Ignore all blank lines and those starting with '%' or '#'.

    Values in the line may be separated by whitespace or commas.
    '''

    # get data from file
    fd = open(filename, 'r')
    lines = fd.readlines()
    fd.close()

    # start collecting rows
    result = []
    for line in lines:
        line = line.strip()

        # ignore blank lines
        if line == '':
            continue
        
        # ignore comment lines
        if line[0] in '%#':
            continue

        # split line into fields, append to result
        if line:
            data = [float(f) for f in SplitPattern.split(line)]
            result.append(data)

    return num.array(result)


def harness_plot_pml():
    '''Harness to run plot_pml.py with demo data.

    Input:
    root_eqrm_dir  path to the root directory for EQRM
    
    '''

    # get EQRM root path
    eqrm_path = util.determine_eqrm_path()

    # create paths to various sub-directories
    datadir = os.path.join(eqrm_path, eqrm_filesystem.Resources_Data_Path)
    demodir= os.path.join(eqrm_path,
                          eqrm_filesystem.Demo_Output_ProbRisk_Path)
    outputdir = os.path.join(eqrm_path, eqrm_filesystem.Postprocessing_Path)

    # get input file data into memory
    saved_ecbval2 = \
            load_data(os.path.join(eqrm_path,
                                   eqrm_filesystem.Demo_Output_ProbRisk_Path,
                                   site_tag + '_bval.txt'))
    saved_ecloss = \
            load_data(os.path.join(eqrm_path,
                                   eqrm_filesystem.Demo_Output_ProbRisk_Path,
                                   site_tag + '_total_building_loss.txt'))
    saved_ecloss = saved_ecloss[1:]
    saved_nu = load_data(os.path.join(eqrm_path,
                                      eqrm_filesystem.Demo_Output_ProbRisk_Path,
                                      site_tag + '_event_set.txt'))
    saved_nu = saved_nu[:, 8]

    # plot the data
    out_file = 'harness_plot_pml.png'
    pml_curve = plot_pml.plot_pml(saved_ecloss, saved_ecbval2, saved_nu,
                                  outputdir, title='Harness plot_pml()',
                                  output_file=out_file, grid=True,
                                  datestamp=True, show_graph=True)

    # draw curve data on screen
    print('pml_curve=%s' % str(pml_curve))
          

if __name__ == '__main__':
    harness_plot_pml()
