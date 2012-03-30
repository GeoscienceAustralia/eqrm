#!/usr/bin/env python

"""
This is the client facing api of all of the plotting modules.
The data file formats are assumed to be the EQRM data file formats.

These functions should link lower level functions, such as loading data,
processing dta and graphing the data together.

Copyright 2009 by Geoscience Australia

"""


import os
import scipy
import numpy
import matplotlib.pyplot as plt

import eqrm_code.plotting.utilities as util
import eqrm_code.output_manager as om
import eqrm_code.plotting.calc_sum_xyz as csx
import eqrm_code.plotting.plot_gmt_xyz as pgx
import eqrm_code.plotting.plot_gmt_xyz_contour as pgxc
import eqrm_code.plotting.calc_ignore_xyz as cix
import eqrm_code.plotting.calc_annloss_deagg_distmag as cadd
import eqrm_code.plotting.plot_annloss_deagg_distmag as padd
import eqrm_code.plotting.calc_annfatalities_deagg_distmag as cafdd
#import eqrm_code.plotting.plot_annloss_deagg_distmag as padd
import eqrm_code.plotting.plot_barchart as pb
import eqrm_code.plotting.utilities as util

from eqrm_code.plotting import plot_pml
from eqrm_code.plotting import plot_pml_fatalities
from eqrm_code.plotting import calc_pml
from eqrm_code.plotting import calc_annloss


def fig_hazard(input_dir, site_tag, soil_amp, return_period, period,
                plot_file=None, save_file=None, title=None, np_posn=None,
                s_posn=None, cb_steps=None, colourmap=None, cb_label=None,
                annotate=[]):
    """Plot an earthquake hazard map, from probabalistic data.

    input_dir     directory containing EQRM input data files
    site_tag      event descriptor string
    soil_amp      True for results with soil amplification,
                  False for the bedrock results.
    return_period event return period
    period        period of the event
    plot_file     full filename for generated plot file (*.png, *.eps, etc)
    save_file     full filename for saved plot data

    All other parameters are plot parameters as described elsewhere.

    Outputs are:
        plot_file  if specified, a plot file (*.png, *.eps, etc)
        save_file  if specified, a file containing data as plotted,
                   after any 'calc' manipulations.
    """

    # get raw data, all periods
    data = om.load_lat_long_haz_SA(input_dir, site_tag, soil_amp,
                                   period, return_period)

    # would do extra calc functions here, if required

    # if user wants to save actual plotted data
    if save_file:
        save(data, save_file)      ####################### needs change

    # plot the data
    if plot_file:
        # use default contour values if user didn't supply any
        if cb_steps is None:
            cb_steps = [0.1,0.15,0.20,0.30,0.40,0.50]

        if title is None:
            title = 'RP=%s, period=%s' % (return_period, period)

        pgxc.plot_gmt_xyz_contour(data, plot_file, title=title,
                                  np_posn=np_posn, s_posn=s_posn,
                                  cb_label=cb_label, cb_steps=cb_steps,
                                  colourmap=colourmap,
                                  annotate=annotate)


def fig_hazard_continuous(input_dir, site_tag, soil_amp, return_period, period,
                          plot_file=None, save_file=None,
                          title=None, np_posn=None, s_posn=None, cb_steps=None,
                          colourmap=None, cb_label=None, annotate=[]):
    """Plot an earthquake hazard map, from probabalistic data.
    Continuous colourbar and map.

    input_dir     directory containing EQRM input data files
    site_tag      event descriptor string
    soil_amp      True for results with soil amplification,
                  False for the bedrock results.
    return_period event return period
    period        period of the event
    plot_file     full filename for generated plot file (*.png, *.eps, etc)
    save_file     full filename for saved plot data

    All other parameters are plot parameters as described elsewhere.

    Outputs are:
        plot_file  if specified, a plot file (*.png, *.eps, etc)
        save_file  if specified, a file containing data as plotted,
                   after any 'calc' manipulations.
    """

    # get raw data, all periods
    data = om.load_lat_long_haz_SA(input_dir, site_tag, soil_amp,
                                   period, return_period)

    # would do extra calc functions here, if required

    # if user wants to save actual plotted data
    if save_file:
        save(data, save_file)      ####################### needs change

    # plot the data
    if plot_file:
        if title is None:
            title = 'RP=%s, period=%s' % (return_period, period)

        pgx.plot_gmt_xyz_continuous(data, plot_file, title=title,
                                    np_posn=np_posn, s_posn=s_posn,
                                    cb_label=cb_label, cb_steps=cb_steps,
                                    colourmap=colourmap,
                                    annotate=annotate)


def fig_loss_exceedance(input_dir, site_tag, title='',
                        output_file=None, grid=True,
                        show_graph=False, annotate=[]):
    """

    This is also called the pml figure.  This is for probabalistic
    risk simulations.

    Plot the PML data.  Optionally save a file or show the graph (or both).

    Inputs:
    input_dir    input directory
    site_tag     event descriptor string    
    title          if supplied, the graph title string
    output_file    path of file to save plot picture in
    grid           draw a grid on graph if True
    show_graph     show graph on screen if True
    annotate       an iterable like [(x, y, ann, dict), ...] where
                       x    is X screen coordinate
                       y    is Y screen coordinate
                       ann  is the annotation string to display at (x, y)
                       dict is a dictionary of key/value pairs as documented at
                     http://matplotlib.sourceforge.net/api/pyplot_api.html
                            (this is optional)
                     NOTE: if annotate=None is used, no automatic
                     annotation occurs.
                     if annotate=[] is used, auto annotation is generated:
                       timestamp
                       clipping
                       max input data value
    """

    # Load in the structure loss and structure value
    results = om.load_ecloss_and_sites(input_dir, site_tag)
    total_building_loss = results[0]
    total_building_value = results[1]

    # Load in the event activity
    out_dict = om.load_event_set(input_dir, site_tag)
    event_activity = out_dict['event_activity']

    # Do calculations
    pml_curve = calc_pml.calc_pml(total_building_loss,
                                  total_building_value,
                                  event_activity)

    # Plot it.
    plot_pml.plot_pml(pml_curve, title=title,
                      output_file=output_file, grid=grid,
                      show_graph=show_graph, annotate=annotate)
                      
def fig_fatalities_exceedance(input_dir, site_tag, title='',
                        output_file=None, grid=True,
                        show_graph=False, annotate=[]):
    """

    This is also called the pml figure.  This is for fatalities
    risk simulations.

    Plot the PML data.  Optionally save a file or show the graph (or both).

    Inputs:
    input_dir    input directory
    site_tag     event descriptor string    
    title          if supplied, the graph title string
    output_file    path of file to save plot picture in
    grid           draw a grid on graph if True
    show_graph     show graph on screen if True
    annotate       an iterable like [(x, y, ann, dict), ...] where
                       x    is X screen coordinate
                       y    is Y screen coordinate
                       ann  is the annotation string to display at (x, y)
                       dict is a dictionary of key/value pairs as documented at
                     http://matplotlib.sourceforge.net/api/pyplot_api.html
                            (this is optional)
                     NOTE: if annotate=None is used, no automatic
                     annotation occurs.
                     if annotate=[] is used, auto annotation is generated:
                       timestamp
                       clipping
                       max input data value
    """

    # Load in the structure loss and structure value
    (total_fatalities, _, _) = om.load_fatalities('_fatalities', input_dir, site_tag)
    

    # Load in the event activity
    out_dict = om.load_event_set(input_dir, site_tag)
    event_activity = out_dict['event_activity']
    
    # Check array dimensions

    # Do calculations
    # aggregates fatalities across all sites
    aggfatalities = numpy.sum(total_fatalities, axis=0) # sum rows
    
    pml_curve = calc_pml.calc_pml_fatalities(aggfatalities ,
                                  event_activity)

    # Plot it.
    plot_pml_fatalities.plot_pmlf(pml_curve, title=title,
                      output_file=output_file, grid=grid,
                      show_graph=show_graph, annotate=annotate)
    

def fig_annloss_deagg_distmag(input_dir, site_tag, momag_labels,
                              momag_bin, range_bins, Zlim,
                              R_extend_flag=True, 
                              output_file=None, title=None,
                              show_graph=False, grid=False,
                              colormap=None,
                              annotate=[]):
    """Plot annualised loss deaggregated distance/magnitude data.
    This is for probabalistic risk simulations.

    Inputs:   
    input_dir    input directory
    site_tag     event descriptor string
    momag_labels an iterable containing the y-axis labels for each row of 'data'
    range_bins   an iterable of range values for each column of 'data'
    output_file  path to required output plot file
    title        string used to title graph
    show_graph   if True shows graph in window on screen
    grid         if True puts a grid in the graph
    colormap     name of the colormap to use
    annotate     an iterable like [(x, y, str, dict), ...] where
                     x    is X screen coordinate
                     y    is Y screen coordinate
                     str  is the annotation string to display at (x, y)
                     dict is a dictionary of key/value pairs as documented at
                          http://matplotlib.sourceforge.net/api/pyplot_api.html
                          (this is optional)
                 NOTE: if annotate=None is used, no automatic annotation occurs.
                       if annotate=[] is used, auto annotation is generated:
                           timestamp
                           clipping
                           max input data value   
    """

    # Load in the structure loss and structure value
    results = om.load_ecloss_and_sites(input_dir, site_tag)
    total_building_loss = scipy.transpose(results[0])
    total_building_value = results[1]

    # Load in the event activity, mag and distance
    out_dict = om.load_event_set(input_dir, site_tag)
    event_activity = out_dict['event_activity']
    Mw = out_dict['Mw']
    distance = om.load_distance(input_dir, site_tag, True)

    # Do calculations
    NormDeAggLoss = cadd.calc_annloss_deagg_distmag(total_building_value,
                                                    total_building_loss,
                                                    event_activity,
                                                    distance,
                                                    Mw,
                                                    momag_bin, range_bins, Zlim,
                                                    R_extend_flag=R_extend_flag)

    # Plot it.
    padd.plot_annloss_deagg_distmag(NormDeAggLoss, momag_labels,
                                    range_bins, Zlim,
                                    output_file=output_file,
                                    title=title,
                                    show_graph=show_graph,
                                    grid=grid, colormap=colormap,
                                    annotate=annotate)
                                    

def fig_annfatalities_deagg_distmag(input_dir, site_tag, momag_labels,
                              momag_bin, range_bins, Zlim,
                              R_extend_flag=True, 
                              output_file=None, title=None,
                              show_graph=False, grid=False,
                              colormap=None,
                              annotate=[]):
    """Plot annualised fatalities deaggregated distance/magnitude data.
    This is for probabalistic fatality simulations.

    Inputs:   
    input_dir    input directory
    site_tag     event descriptor string
    momag_labels an iterable containing the y-axis labels for each row of 'data'
    range_bins   an iterable of range values for each column of 'data'
    output_file  path to required output plot file
    title        string used to title graph
    show_graph   if True shows graph in window on screen
    grid         if True puts a grid in the graph
    colormap     name of the colormap to use
    annotate     an iterable like [(x, y, str, dict), ...] where
                     x    is X screen coordinate
                     y    is Y screen coordinate
                     str  is the annotation string to display at (x, y)
                     dict is a dictionary of key/value pairs as documented at
                          http://matplotlib.sourceforge.net/api/pyplot_api.html
                          (this is optional)
                 NOTE: if annotate=None is used, no automatic annotation occurs.
                       if annotate=[] is used, auto annotation is generated:
                           timestamp
                           clipping
                           max input data value   
    """

    # Load in the structure loss and structure value
    results = om.load_fatalities('_fatalities', input_dir, site_tag)
    total_fatalities = scipy.transpose(results[0])

    # Load in the event activity, mag and distance
    out_dict = om.load_event_set(input_dir, site_tag)
    event_activity = out_dict['event_activity']
    Mw = out_dict['Mw']
    distance = om.load_distance(input_dir, site_tag, True)

    # Do calculations
    NormDeAggFatalities = cafdd.calc_annfatalities_deagg_distmag(
                                                    total_fatalities,
                                                    event_activity,
                                                    distance,
                                                    Mw,
                                                    momag_bin, range_bins, Zlim,
                                                    R_extend_flag=R_extend_flag)

    # Plot it.
    padd.plot_annloss_deagg_distmag(NormDeAggFatalities, momag_labels,
                                    range_bins, Zlim,
                                    output_file=output_file,
                                    title=title,
                                    show_graph=show_graph,
                                    grid=grid, colormap=colormap,
                                    annotate=annotate)


def fig_annloss_deagg_cells(input_dir, site_tag,
                            output_file, save_file=None,
                            title=None, np_posn=None, s_posn=None,
                            cb_label=None, cb_steps=None,
                            bins=10, scale=1.0, ignore=None, invert=False,
                            colourmap=None, annotate=None):

    # Load in the structure loss and structure value
    results = om.load_ecloss_and_sites(input_dir, site_tag)
    
    # change dimensions(site, event) to dimensions(event, site)
    total_building_loss = scipy.transpose(results[0])
    total_building_value = results[1]
    lon = results[2]
    lat = results[3]

    # Load in the event activity
    out_dict = om.load_event_set(input_dir, site_tag)
    event_activity = out_dict['event_activity']

    # Run annualised loss calc and bin data
    percent_ann_loss, lat_lon, binx, _ = calc_annloss.calc_annloss_deagg_grid(
        lat,
        lon,
        total_building_loss,
        total_building_value,
        event_activity, bins=bins)
    # check that the bins are equivalent
    lon = lat_lon[:,1]
    lat = lat_lon[:,0]
    loss = scipy.reshape(percent_ann_loss, (-1,1))
    lon = scipy.reshape(lon, (-1,1))
    lat = scipy.reshape(lat, (-1,1))
    lon_lat_ann_loss = scipy.concatenate((lon, lat, loss), axis=1)
    #scipy.set_printoptions(threshold=scipy.nan)
    pgx.plot_gmt_xyz(lon_lat_ann_loss, output_file, bins=binx,
                     title=title, np_posn=np_posn, s_posn=s_posn,
                     cb_label=cb_label, cb_steps=cb_steps, colourmap=colourmap,
                     annotate=annotate, show_graph=False)
                     
def fig_annfatalities_deagg_cells(input_dir, site_tag,
                            output_file, save_file=None,
                            title=None, np_posn=None, s_posn=None,
                            cb_label=None, cb_steps=None,
                            bins=10, scale=1.0, ignore=None, invert=False,
                            colourmap=None, annotate=None):

    # Load in the structure loss and structure value
    results = om.load_fatalities('_fatalities', input_dir, site_tag)
    # change dimensions(site, event) to dimensions(event, site)
    total_fatalities = scipy.transpose(results[0])
    lat = results[1]
    lon = results[2]
    
    # Load in the event activity
    out_dict = om.load_event_set(input_dir, site_tag)
    event_activity = out_dict['event_activity']
    
    print event_activity
    
    # Run annualised loss calc and bin data
    percent_ann_loss, lat_lon, binx, _ = calc_annloss.calc_annfatalities_deagg_grid(
        lat,
        lon,
        total_fatalities,
        event_activity, bins=bins)
    # check that the bins are equivalent
    lon = lat_lon[:,1]
    lat = lat_lon[:,0]
    loss = scipy.reshape(percent_ann_loss, (-1,1))
    lon = scipy.reshape(lon, (-1,1))
    lat = scipy.reshape(lat, (-1,1))
    lon_lat_ann_fatalities = scipy.concatenate((lon, lat, loss), axis=1)
    #scipy.set_printoptions(threshold=scipy.nan)
    pgx.plot_gmt_xyz(lon_lat_ann_fatalities, output_file, bins=binx,
                     title=title, np_posn=np_posn, s_posn=s_posn,
                     cb_label=cb_label, cb_steps=cb_steps, colourmap=colourmap,
                     annotate=annotate, show_graph=False)
                     
def fig_fatalities_map(input_dir, site_tag,
                            output_file, save_file=None, return_period=500, 
                            title=None, np_posn=None, s_posn=None,
                            cb_label=None, cb_steps=None,
                            bins=10, scale=1.0, ignore=None, invert=False,
                            colourmap=None, annotate=None):

    # Load in the structure loss and structure value
    results = om.load_fatalities('_fatalities', input_dir, site_tag)
    # change dimensions(site, event) to dimensions(event, site)
    total_fatalities = scipy.transpose(results[0])
    lat = results[1]
    lon = results[2]
    
    # Load in the event activity
    out_dict = om.load_event_set(input_dir, site_tag)
    event_activity = out_dict['event_activity']
    
    columnscount = total_fatalities.shape[1]
    #sites_pmlf = numpy.zeros(columnscount)
    sites_data = numpy.zeros((columnscount, 3))
    for i in range(columnscount):
        temp = calc_pml.calc_pml_fatalities(total_fatalities[:,i], event_activity, return_period)
        #sites_pmlf[i] = temp[1]
        sites_data[i,0] = lon[i]
        sites_data[i,1] = lat[i]
        sites_data[i,2] = temp[1]
        
    #print sites_pmlf.shape
    
    pgxc.plot_gmt_xyz_contour(sites_data, output_file, title=title,
                         np_posn=np_posn, s_posn=s_posn,
                         cb_label=cb_label, cb_steps=cb_steps,
                         colourmap=colourmap, annotate=annotate, linewidth=1.0,
                         show_graph=False, map_extent=None)
    """
    # Run annualised loss calc and bin data
    percent_ann_loss, lat_lon, binx, _ = calc_annloss.calc_annloss_deagg_grid(
        lat,
        lon,
        total_building_loss,
        total_building_value,
        event_activity, bins=bins)
    # check that the bins are equivalent
    lon = lat_lon[:,1]
    lat = lat_lon[:,0]
    loss = scipy.reshape(percent_ann_loss, (-1,1))
    lon = scipy.reshape(lon, (-1,1))
    lat = scipy.reshape(lat, (-1,1))
    lon_lat_ann_loss = scipy.concatenate((lon, lat, loss), axis=1)
    #scipy.set_printoptions(threshold=scipy.nan)
    pgx.plot_gmt_xyz(lon_lat_ann_loss, output_file, bins=binx,
                     title=title, np_posn=np_posn, s_posn=s_posn,
                     cb_label=cb_label, cb_steps=cb_steps, colourmap=colourmap,
                     annotate=annotate, show_graph=False)
    """

def fig_xyz_histogram(input_dir, site_tag, soil_amp, period, return_period,
                      plot_file=None, savefile=None,
                      title=None, xlabel=None, ylabel=None,
                      xrange=None, yrange=None,
                      bins=100, bardict=None, show_graph=False):
    """Plot a 1D histogram from XYZ data.

    input_dir      general input/output directory
    site_tag       overall site identifier
    soil_amp       soil/bedrock switch - True means soil, False means bedrock
    period         the RSA period to be plotted
    return_period  the data return period
    plot_file      path to plot output file to create (*.png, etc)
    savefile       name of data output file to create
    title          title to put on the graph
    xlabel         text of X axis label
    ylabel         text of Y axis label
    xrange         Either <max> or (<min>, <max>) of X range to plot
    yrange         Either <max> or (<min>, <max>) of Y range to plot
    bins           number of bins to use
    bardict        dictionary of extra keywords to pass to plot_barchart()
                   see plot_barchart.py for the details on this
    show_graph     True if the plot is to be shown on the screen
    """

    # read in raw data - load_lat_long_haz_SA() returns [[[lon, lat, SA], ...]]
    data = om.load_lat_long_haz_SA(input_dir, site_tag, soil_amp, period,
                                   return_period)

    # throw away all but SA values (the Z value)
    data = data[:,2]

    # if we want a save of actual plotted data, do it here
    if savefile:
        save_outfile = os.path.join(input_dir, savefile)
        f = open(save_outfile, 'w')
        for d in data:
            f.write('%f\n' % d)
        f.close()

    # plot the data
    if plot_file:
        # default some of the labels
        if title is None:
            title = ''          #######  needs work!

        if xlabel is None:
            xlabel = ''
        if ylabel is None:
            ylabel = 'Count'

        # now generate histogrammed data
        (hist_data, xedges) = scipy.histogram(data, bins=bins, normed=False)

        # get array of bin centres
        bins = []
        for i in range(len(xedges)-1):
            bins.append(xedges[i] + (xedges[i+1] - xedges[i])/2.0)
        bins = scipy.array(bins)

        # calculate optimal bin width
        bin_width = xedges[1] - xedges[0]

        # return nx2 array of (x, y)
        data = scipy.hstack((bins[:,scipy.newaxis], hist_data[:,scipy.newaxis]))

        # now standardise xrange
        xrange = util.get_canonical_range(xrange)
        yrange = util.get_canonical_range(yrange)

        range_ann = []

        if xrange:
            range_ann.append((0.02, 0.05,
                              'X range forced to (%.2f,%.2f)' % xrange))

        if yrange:
            range_ann.append((0.02, 0.03,
                              'Y range forced to (%.2f,%.2f)' % yrange))

        # actually plot the thing
        pb.plot_barchart(data, plot_file, title=title,
                         xlabel=xlabel, ylabel=ylabel,
                         bin_width=bin_width,
                         xrange=xrange, yrange=yrange,
                         show_graph=show_graph, bardict=bardict,
                         annotate=range_ann)


# function string to object mapping
# later, we will only do this mapping if 'collapse_function' is type string
fig_motion_function_map = {'mean': numpy.mean,
                           'median': numpy.median}

def fig_motion(input_dir, site_tag, soil_amp, period,
               collapse_function=None, plot_file=None, save_file=None,
               title=None, np_posn=None, s_posn=None, cb_steps=None,
               colourmap=None, cb_label=None, annotate=[], show_graph=False):
    """Plot a contoured acceleration map with meaned/medianed data.

    input_dir          general input/output directory
    site_tag           overall site identifier
    soil_amp           soil/bedrock switch - True means soil, False means bedrock
    period             the RSA period to be plotted
    collapse_function  string defining function used to collapse site values
                       ('mean' or 'medium', default is 'mean')
    plot_file          path to plot output file to create (*.png, etc)
    save_file          path to file to save plot data in (UNUSED?)
    title              title to put on the graph
    np_posn            north pointer placement data
    s_posn             scale placement data
    cb_steps           iterable of colourbar step values
    colourmap          name of colourmap to use
    cb_label           colourbar label string
    annotate           iterable of annotate values
    show_graph         True if the plot is to be shown on the screen
    """

    # read in raw data
    data = om.load_motion_sites(input_dir, site_tag, soil_amp, period)

    # get function to use
    if collapse_function is None:
        collapse_function = 'mean'
    collapse_function = collapse_function.lower()

    if isinstance(collapse_function, basestring):
        try:
            func = fig_motion_function_map[collapse_function]
        except KeyError:
            msg = ("Bad function param, got '%s', expected 'mean' or 'median'"
                   % function)
            raise Exception(msg)
    else:
        func = collapse_function

    # split returned data into components
    (SA, lat, lon) = data

    # collapse axis=1 with func object
    # simplest approach - just try to call function and catch exception
    try:
        SA = func(SA, axis=1)
    except:
        msg = 'Exception calling function: %s' % str(func)
        raise Exception(msg)

    # now combine collapsed SA, lat and lon into list of (x, y, z) tuples
    data = []
    for (i, val) in enumerate(SA):
        data.append([lon[i], lat[i], val])
    data = numpy.array(data)

    # plot the data
    if plot_file:
        if title is None:
            title = 'site_tag=%s, period=%s' % (site_tag, period)

        # use default contour values if user didn't supply any
        if cb_steps is None:
            cb_steps = [0.1,0.15,0.20,0.30,0.40,0.50]

        if title is None:
            title = 'RP=%s, period=%s' % (return_period, period)

        pgxc.plot_gmt_xyz_contour(data, plot_file, title=title,
                                  np_posn=np_posn, s_posn=s_posn,
                                  cb_label=cb_label, cb_steps=cb_steps,
                                  colourmap=colourmap,
                                  annotate=annotate)


def fig_motion_continuous(input_dir, site_tag, soil_amp, period,
                          collapse_function=None, plot_file=None,
                          save_file=None, title=None, np_posn=None, s_posn=None,
                          cb_steps=None, colourmap=None, cb_label=None,
                          annotate=[], show_graph=False):
    """Plot a continuous contoured acceleration map with meaned/medianed data.

    input_dir          general input/output directory
    site_tag           overall site identifier
    soil_amp           soil/bedrock switch - True means soil, False means bedrock
    period             the RSA period to be plotted
    collapse_function  string defining function used to collapse site values
                       ('mean' or 'medium', default is 'mean')
    plot_file          path to plot output file to create (*.png, etc)
    save_file          path to file to save plot data in (UNUSED?)
    title              title to put on the graph
    np_posn            north pointer placement data
    s_posn             scale placement data
    cb_steps           iterable of colourbar step values
    colourmap          name of colourmap to use
    cb_label           colourbar label string
    annotate           iterable of annotate values
    show_graph         True if the plot is to be shown on the screen
    """

    # read in raw data
    data = om.load_motion_sites(input_dir, site_tag, soil_amp, period)

    # get function to use
    if collapse_function is None:
        collapse_function = 'mean'
    collapse_function = collapse_function.lower()

    if isinstance(collapse_function, basestring):
        try:
            func = fig_motion_function_map[collapse_function]
        except KeyError:
            msg = ("Bad function param, got '%s', expected 'mean' or 'median'"
                   % function)
            raise Exception(msg)
    else:
        func = collapse_function

    # split returned data into components
    (SA, lat, lon) = data

    # collapse axis=1 with func object
    # simplest approach - just try to call function and catch exception
    try:
        SA = func(SA, axis=1)
    except:
        msg = 'Exception calling function: %s' % str(func)
        raise Exception(msg)

    # now combine collapsed SA, lat and lon into list of (x, y, z) tuples
    data = []
    for (i, val) in enumerate(SA):
        data.append([lon[i], lat[i], val])
    data = numpy.array(data)

    # plot the data
    if plot_file:
        if title is None:
            title = 'site_tag=%s, period=%s' % (site_tag, period)

        if title is None:
            title = 'RP=%s, period=%s' % (return_period, period)

        pgx.plot_gmt_xyz_continuous(data, plot_file, title=title,
                                    np_posn=np_posn, s_posn=s_posn,
                                    cb_label=cb_label, cb_steps=cb_steps,
                                    colourmap=colourmap,
                                    annotate=annotate)


def fig_hazard_sites(input_dir, site_tag, soil_amp, sites, title=None,
                     xlabel=None, ylabel=None, xrange=None, yrange=None,
                     show_grid=False, plot_file=None, save_file=None,
                     show_graph=False, legend_placement=None):
    """Plot an earthquake hazard/period graph for multiple sites.

    input_dir         directory containing EQRM input data files
    site_tag          event descriptor string
    soil_amp          True for results with soil amplification,
                      False for the bedrock results.
    sites             a list of required site tuples (lat, lon, RP, [colour])
    title             graph title
    xlabel            text of X axis label
    ylabel            text of Y axis label
    xrange            Either <max> or (<min>, <max>) of X range to plot
    yrange            Either <max> or (<min>, <max>) of Y range to plot
    show_grid         True if a grid is to be drawn
    plot_file         full filename for generated plot file (*.png, *.eps, etc)
    save_file         full filename for saved plot data (CURRENTLY UNUSED)
    show_graph        True if the graph is to be shown on the screen
    legend_placement  a string determining where to place the legend
                      ('lower left' is the default)

    All other parameters are plot parameters as described elsewhere.

    Outputs are:
        plot_file  if specified, a plot file (*.png, *.eps, *.ps, etc)
        save_file  if specified, a file containing data as plotted,
                   after any 'calc' manipulations.

    The optional 'colour' part of the 'sites' tuple is a string as described
    in [http://matplotlib.sourceforge.net/api/colors_api.html].  Note that if
    you specify colour on only a few sites, matplotlib will choose any colour
    it likes for the sites without a 'colour' element.

    Valid legend placement strings may be found at
    [http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.legend]

    Linestyle suffixes to line colours are documented here:
    [http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.plot]
    Note this only seem to work on 'single char' colour strings, ie, 'g--' but not
    'green--'.
    """

    # get raw data, all periods
    # SA      is numpy array of shape (site, periods, RP)
    # RP      is a list of return periods of the SA values
    # periods is a list of return periods of the SA values
    (SA, periods, RP) = om.load_hazards(input_dir, site_tag, soil_amp)

    # now get sites lat&lon data
    (site_lats, site_lons) = om.load_sites(input_dir, site_tag)

    # default the title, axis labels, etc, if necessary
    if title is None:
        title = 'Hazard at location and Return Period'
    if xlabel is None:
        xlabel = 'RSA period (s)'
    if ylabel is None:
        ylabel = 'Hazard (g)'
    if legend_placement is None:
        legend_placement = 'upper right'

    # now find user sites and RPs in the loaded data, create plot dataset
    plot_data = []
    legend_titles = []
    for (i, s) in enumerate(sites):
        try:
            (slat, slon, sRP) = s
            colour = None
        except ValueError:
            (slat, slon, sRP, colour) = s

        # find site index matching user site
        site_index = None
        for (lat, lon) in zip(site_lats, site_lons):
            #if abs(lat - slat) <= delta and abs(lon - slon) <= delta:
            if lat == slat and lon == slon:
                site_index = i
                break
        if site_index is None:
            msg = ("Site (%.3f,%.3f) not found in site data"
                   % (float(slat), float(slon)))
            raise Exception(msg)

        # find RP_index matching user RP
        RP_index = None
        for (i, rp) in enumerate(RP):
            if sRP == rp:
                RP_index = i
                break
        if RP_index is None:
            msg = "RP %.1f not found in site data" % sRP
            raise Exception(msg)

        # at this point we take slices at site and RP indices to get plot data
        data = SA[site_index,:,RP_index]
        plot_data.append(periods)
        plot_data.append(data)
        if colour:
            plot_data.append(colour)

        # generate legend string for this dataset
        legend = ('Location: %.1f,%.1f    Return Period: %d years'
                  %  (slon, slat, int(sRP)))
        legend_titles.append(legend)

    # if user wants to save actual plotted data
#    if save_file:
#        save(data, save_file)      ####################### needs change

    # plot the data
    if plot_file or show_graph:
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(*plot_data)

        leg = ax.legend(legend_titles, legend_placement)

        if xrange:
            try:
                (x_min, x_max) = xrange
            except TypeError:
                # single value
                x_min = 0.0
                x_max = xrange
            ax.set_xlim((x_min, x_max))

        if yrange:
            try:
                (y_min, y_max) = yrange
            except TypeError:
                # single value
                y_min = 0.0
                y_max = xrange
            ax.set_ylim((y_min, y_max))

        ax.grid(show_grid)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        
        # tweak various legend params
        frame  = leg.get_frame()
        frame.set_facecolor('0.95')   # set the frame face color to light gray
        
        for t in leg.get_texts():
            t.set_fontsize('small')    # the legend text fontsize
        
        for l in leg.get_lines():
            l.set_linewidth(2.0)       # the legend line width

        if plot_file:
            plt.savefig(plot_file)

        if show_graph:
            plt.show()


def fig_hazard_exceedance(input_dir, site_tag, soil_amp, sites, title=None,
                          xlabel=None, ylabel=None, xrange=None, yrange=None,
                          show_grid=False, plot_file=None, save_file=None,
                          show_graph=False, legend_placement=None):
    """Plot an earthquake hazard exceedance graph for multiple sites.

    input_dir         directory containing EQRM input data files
    site_tag          event descriptor string
    soil_amp          True for results with soil amplification,
                      False for the bedrock results.
    sites             a list of required site tuples (lat, lon, period, [colour])
    title             graph title
    xlabel            text of X axis label
    ylabel            text of Y axis label
    xrange            Either <max> or (<min>, <max>) of X range to plot
    yrange            Either <max> or (<min>, <max>) of Y range to plot
    show_grid         True if a grid is to be drawn
    plot_file         full filename for generated plot file (*.png, *.eps, etc)
    save_file         full filename for saved plot data (CURRENTLY UNUSED)
    show_graph        True if the graph is to be shown on the screen
    legend_placement  a string determining where to place the legend
                      ('lower left' is the default)

    All other parameters are plot parameters as described elsewhere.

    Outputs are:
        plot_file  if specified, a plot file (*.png, *.eps, *.ps, etc)
        save_file  if specified, a file containing data as plotted,
                   after any 'calc' manipulations.

    The optional 'colour' part of the 'sites' tuple is a string as described
    in [http://matplotlib.sourceforge.net/api/colors_api.html].  Note that if
    you specify colour on only a few sites, matplotlib will choose any colour
    it likes for the sites without a 'colour' element.

    Valid legend placement strings may be found at
    [http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.legend]

    Linestyle suffixes to line colours are documented here:
    [http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.plot]
    Note this only seem to work on 'single char' colour strings, ie, 'g--' but not
    'green--'.
    """

    # get raw data, all periods
    # SA           is numpy array of shape (site, periods, RP)
    # RP           is a list of return periods of the SA values
    # periods      is a list of return periods of the SA values
    # prob_exceed  is inverse of RP (Y data)
    (SA, periods, RP) = om.load_hazards(input_dir, site_tag, soil_amp)
    prob_exceed = [1/rp for rp in RP]

    # now get sites lat&lon data
    (site_lats, site_lons) = om.load_sites(input_dir, site_tag)

    # default the title, axis labels, etc, if necessary
    if title is None:
        title = 'Hazard Exceedance'
    if xlabel is None:
        xlabel = 'Hazard (g)'
    if ylabel is None:
        ylabel = 'Probability of Exceedance in One Year'
    if legend_placement is None:
        legend_placement = 'upper right'

    # now find user sites and period in the loaded data, create plot dataset
    plot_data = []
    legend_titles = []
    for (j, s) in enumerate(sites):
        try:
            (slat, slon, period) = s
            colour = None
        except ValueError:
            (slat, slon, period, colour) = s

        # find site index matching user site
        site_index = None
        i=0
        for (lat, lon) in zip(site_lats, site_lons):
            #if abs(lat - slat) <= delta and abs(lon - slon) <= delta:
            if lat == slat and lon == slon:
                site_index = i
                break
            i+=1
        if site_index is None:
            msg = ("Site (%.3f,%.3f) not found in site data"
                   % (float(slat), float(slon)))
            raise Exception(msg)

        # find index matching user period
        period_index = None
        for (i, rp) in enumerate(periods):
            if period == rp:
                period_index = i
                break
        if period_index is None:
            msg = "period %.1f not found in site data" % period
            raise Exception(msg)

        # at this point we take slices at site and period indices -> plot data
        data = SA[site_index,period_index,:]
        plot_data.append(data)		# X data
        plot_data.append(prob_exceed)		# Y data
        if colour:
            plot_data.append(colour)	# line attributes

        # generate legend string for this dataset
        legend = ('Location: %.1f,%.1f    RSA Period: %.1f'
                  %  (slon, slat, int(period)))
        legend_titles.append(legend)

    # if user wants to save actual plotted data
#    if save_file:
#        save(data, save_file)      ####################### needs change

    # plot the data
    if plot_file or show_graph:
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(*plot_data)

        leg = ax.legend(legend_titles, legend_placement)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_yscale('log')
        ax.grid(show_grid)
        
        if xrange:
            try:
                (x_min, x_max) = xrange
            except TypeError:
                # single value
                x_min = 0.0
                x_max = xrange
            ax.set_xlim((x_min, x_max))

        if yrange:
            try:
                (y_min, y_max) = yrange
            except TypeError:
                # single value
                y_min = 0.0
                y_max = xrange
            ax.set_ylim((y_min, y_max))

        # tweak various legend params
        frame  = leg.get_frame()
        frame.set_facecolor('0.95')   # set the frame face color to light gray
        
        for t in leg.get_texts():
            t.set_fontsize('small')    # the legend text fontsize
        
        for l in leg.get_lines():
            l.set_linewidth(2.0)       # the legend line width

        if plot_file:
            plt.savefig(plot_file)

        if show_graph:
            plt.show()


def fig_scenario_building_loss(input_dir, site_tag, plot_file=None, scale=None,
                               savefile=None, title=None, xlabel=None,
                               ylabel=None, xrange=None, yrange=None, bins=100,
                               bardict=None, show_graph=False):
    """Plot a 1D histogram of scenario building loss.

    input_dir      general input/output directory
    site_tag       overall site identifier
    plot_file      path to plot output file to create
    scale          None or scaling factor to *divide* data with
                   (eg, if *billions* of dollars, uses scale=1.0e+9)
    savefile       path to data output file to create (UNUSED)
    title          title to put on the graph
    xlabel         text of X axis label
    ylabel         text of Y axis label
    xrange         Either <max> or (<min>, <max>) of X range to plot
    yrange         Either <max> or (<min>, <max>) of Y range to plot
    bins           number of bins to use
    bardict        dictionary of extra keywords to pass to plot_barchart()
                   see plot_barchart.py for the details on this
    show_graph     True if the plot is to be shown on the screen
    """

    # Load in the structure loss data, shape = (location, event)
    (total_building_loss, _, _, _) = om.load_ecloss_and_sites(input_dir, site_tag)

    # sum over location -> (event,)
    data = numpy.sum(total_building_loss, axis=0)

    # scale data, if required
    if scale:
        data = data / scale
        

    # plot the data
    if plot_file or show_graph:
        if title is None:
            title = ''          #######  needs work!

        # now generate histogrammed data
        (hist_data, xedges) = scipy.histogram(data, bins=bins, normed=False)

        # get array of bin centres
        bins = []
        for i in range(len(xedges)-1):
            bins.append(xedges[i] + (xedges[i+1] - xedges[i])/2.0)
        bins = scipy.array(bins)

        # calculate optimal bin width
        bin_width = xedges[1] - xedges[0]

        # return nx2 array of (x, y)
        plot_data = scipy.hstack((bins[:,scipy.newaxis], hist_data[:,scipy.newaxis]))

        # now standardise xrange
        xrange = util.get_canonical_range(xrange)
        yrange = util.get_canonical_range(yrange)

        range_ann = []

        # assert number of events == sum of frequencies
        y_sum = numpy.sum(plot_data[:,1])
        msg = 'num of events(%d) != sum(frequency)(%d)' % (len(data), y_sum)
        assert len(data) == y_sum, msg

        # annotate any range coercions
        if xrange:
            range_ann.append((0.02, 0.05,
                              'X range forced to (%.2f,%.2f)' % xrange))

        if yrange:
            range_ann.append((0.02, 0.03,
                              'Y range forced to (%.2f,%.2f)' % yrange))

        # actually plot the thing
        pb.plot_barchart(plot_data, plot_file, title=title,
                         xlabel=xlabel, ylabel=ylabel,
                         bin_width=bin_width,
                         xrange=xrange, yrange=yrange,
                         show_graph=show_graph, bardict=bardict,
                         annotate=range_ann)


def fig_scenario_building_loss_percent(input_dir, site_tag, plot_file=None,
                                       savefile=None, title=None,
                                       xlabel=None, ylabel=None, xrange=None,
                                       yrange=None, bins=100, bardict=None,
                                       show_graph=False):
    """Plot a 1D histogram of scenario percent building loss.

    input_dir      general input/output directory
    site_tag       overall site identifier
    plot_file      path to plot output file to create
    savefile       path to data output file to create (UNUSED)
    title          title to put on the graph
    xlabel         text of X axis label
    ylabel         text of Y axis label
    xrange         Either <max> or (<min>, <max>) of X range to plot
    yrange         Either <max> or (<min>, <max>) of Y range to plot
    bins           number of bins to use
    bardict        dictionary of extra keywords to pass to plot_barchart()
                   see plot_barchart.py for the details on this
    show_graph     True if the plot is to be shown on the screen
    """

    # Load in the structure loss data, shape = (location, event)
    (total_building_loss, building_value,
      _, _) = om.load_ecloss_and_sites(input_dir, site_tag)

    # sum over location -> (event,), get % of building value
    data = numpy.sum(total_building_loss, axis=0)
    building_value = numpy.sum(building_value)
    data = (data/building_value)*100.0

    # plot the data
    if plot_file or show_graph:
        # default the labels
        if title is None:
            title = ''          #######  needs work!

        if xlabel is None:
            xlabel = ''
        if ylabel is None:
            ylabel = 'Count'

        # now generate histogrammed data
        (hist_data, xedges) = scipy.histogram(data, bins=bins, normed=False)

        # get array of bin centres
        bins = []
        for i in range(len(xedges)-1):
            bins.append(xedges[i] + (xedges[i+1] - xedges[i])/2.0)
        bins = scipy.array(bins)

        # calculate optimal bin width
        bin_width = xedges[1] - xedges[0]

        # return nx2 array of (x, y)
        plot_data = scipy.hstack((bins[:,scipy.newaxis], hist_data[:,scipy.newaxis]))

        # now standardise xrange
        xrange = util.get_canonical_range(xrange)
        yrange = util.get_canonical_range(yrange)

        range_ann = []

        # assert number of events == sum of frequencies
        y_sum = numpy.sum(plot_data[:,1])
        msg = 'num of events(%d) != sum(frequency)(%d)' % (len(data), y_sum)
        assert len(data) == y_sum, msg

        # annotate any range coercions
        if xrange:
            range_ann.append((0.02, 0.05,
                              'X range forced to (%.2f,%.2f)' % xrange))

        if yrange:
            range_ann.append((0.02, 0.03,
                              'Y range forced to (%.2f,%.2f)' % yrange))

        # actually plot the thing
        pb.plot_barchart(plot_data, plot_file, title=title,
                         xlabel=xlabel, ylabel=ylabel,
                         bin_width=bin_width,
                         xrange=xrange, yrange=yrange,
                         show_graph=show_graph, bardict=bardict,
                         annotate=range_ann)


# function string to object mapping
# later, we will only do this mapping if 'collapse_function' is of type string
fig_scenario_loss_percent_map = {'mean': numpy.mean,
                                 'median': numpy.median}

def fig_scenario_loss_percent(input_dir, site_tag, plot_file=None,
                              collapse_function='mean',
                              savefile=None, title='',
                              np_posn=None, s_posn=None,
                              cb_steps=None, colourmap=None,
                              cb_label=None, annotate=None,
                              show_graph=False):
    """Plot a set of gridded % loss data over a map of an area.

    input_dir          general input/output directory
    site_tag           overall site identifier
    plot_file          full path to plot output file to create (*.png, etc)
    collapse_function  string defining function used to collapse site values
                       ('mean' or 'medium', default is 'mean')
    save_file          path to file to save plot data in (UNUSED?)
    title              title to put on the graph
    np_posn            north pointer placement data
    s_posn             scale placement data
    cb_steps           iterable of colourbar step values
    colourmap          name of colourmap to use
    cb_label           colourbar label string
    annotate           iterable of annotate values
    show_graph         True if the plot is to be shown on the screen
    """

    # Load in the structure loss data, shape = (location, event)
    # and building value -> (location, event)
    # and lon & lat -> (location,)
    (total_building_loss, building_value,
      lon, lat) = om.load_ecloss_and_sites(input_dir, site_tag)



