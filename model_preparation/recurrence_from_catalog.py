# -*- coding: cp1252 -*-
"""This script calculates Gutenberg-Richter recurrence parameters
(a and b values) from an earthquake catalogue. Recurrence parameters are
calculated using several methods:
    1. Least Squares
    2. Maximum Likelihood (Aki, 1965)
    3. Assuming b = 1

Results are plotted for both straightline fits and bounded
Gutenberg-Richter curves. Also plotted is the curve that would result
assuming a b-value of 1.

This assumes that a subset of a catlogue has already been created based on
depth and location - i.e. this is not a tool for exploring the data.

Usage: python recurrence_from_catalog.py <input_file>
<minimum magnitude = minimum magnitude in catalogue>
<maximum magnitude = maximum magnitude in catalogue + 0.1>
<maximum magnitude for least squares analysis = maximum magnitude - 1.0>
<interval = 0.1>

Arguments:
Required:
Input file: This is the file that contains the earthquake catalogue. It
            is expected to be in sv format with a one-line header. It is expectd
            that the year of the earthquake will be in the 3rd column,
            and the magnitude in 6th column.
Optional:
minimum magnitude: The minimum magnitude for which the catalogue is complete.
            Defaults to the minimum magnitude within the catalogue
maximum magnitude: The maximum magnitude expected for the source zone.
            Defaults to the maximum magnitude in the catalogue plus 0.1 magnitude
            units.
maximum magnitude for least squares: The maximum magnitude used in the least squares
            analysis. Defaults to the maximum magnitude in the catalogue minus 1.0
            magnitude units.
interval: Width of magnitude bins for generating cumulative histogram
            of earthquake recurrence for least squares fit. Default value is
            0.1 magnitude units.    

Ref: Kramer, S.L. 1996. Geotechnical Earthquake Engineering, p123.
Aki, K. (1965). Maximum likelihood estimate of b in the formula log N= a-bM and its confidence limits. Bull. Earthquake Res. Inst. Tokyo Univ 43: 237–239.

Creator: Jonathan Griffin, Australia-Indonesia Facility for Disaster Reduction
Created: 23 August 2010
"""

import sys,os
import csv
import copy
import numpy as np
from scipy import stats
import matplotlib
from matplotlib import pylab as py

import catalogue_reader
import earthquake_event


def maximum_likelihood(magnitudes, min_mag):
    """ Maximum Likelihood Estimator fitting
    Use Aki 1965 for continuous, unbounded data b value
    """
    b_mle = np.log10(np.exp(1)) / (np.mean(magnitudes) - min_mag)
    beta_mle = np.log(10) * b_mle    
    return b_mle, beta_mle

def least_squares(bins, log_cum_sum):
    """ Fit a least squares curve
    """
    b,a = np.polyfit(bins, log_cum_sum, 1)
    alpha = np.log(10) * a
    beta = -1.0 * np.log(10) * b
    return a, b, alpha, beta

def completeness(magnitudes, mag_intervals, interval_multipliers):
    """ Handle catalogue in-completeness by scaling number of event from complete
    years to incopmlete ones. Define catalogue completeness intervals. Increase weight of small events
    to extend completeness.
    FIXME - this has not been tested yet
    """
    counter = []
    magnitudes_old = copy.copy(magnitudes)
    for i in range(len(mag_intervals)):
        if i == 0:
            mult_mag_list = []
            for mag in magnitudes_old:                           
                if mag <= mag_intervals[i]:
                    mult_mag_list.append(mag)
            factor = len(mult_mag_list) * interval_multipliers[i]
            j = 0
            if factor <=0:
                continue
            while j <= factor:
                for k in range(len(mult_mag_list)):
                    magnitudes.append(mult_mag_list[k])
                    j +=1
                    if j > factor:
                        break
                    
        elif i > 0:
            mult_mag_list = []
            for mag in magnitudes_old:
                if mag_intervals[i-1] < mag and mag <= mag_intervals[i]:
                    mult_mag_list.append(mag)
            factor = len(mult_mag_list) * interval_multipliers[i]
            j = 0
            while j <= factor:
                for k in range(len(mult_mag_list)):
                    magnitudes.append(mult_mag_list[k])
                    j +=1
                    if j > factor:
                        break


def build_histograms(magnitudes, min_mag, max_catalogue, num_years, max_mag_ls = None, interval = 0.1, verbose = True):
    """ Build histograms for least-squares analysis and plotting
    """
    # Maximum magnitude for least square fit
    # Ignore largest magnitudes because we want to fit the straight part of
    # the G-R relationship
    if max_mag_ls is None:
        max_mag_bin = max(max_catalogue - 1.0, min(magnitudes) + 1.0) + interval
    else:
        max_mag_bin = max_mag_ls + interval

    if verbose:
        print 'Maximum magnitude used in least squares analysis ', max_mag_bin

    # Magnitude bins - we will re-arrange bins later
    bins = np.arange(min_mag, max_mag_bin, interval)

    # Magnitude bins for plotting - we will re-arrange bins later
    bins_plot = np.arange(min_mag, max_catalogue + 2*interval, interval)

    # Generate histogram for LS analysis
    # Note that numpy bins are closed on the LHS and open on the RHS
    # i.e. the bin [1, 2) includes 1 but not 2 (which would be in the
    # bin [2, 3). Except for the last bin which is closed on both sides
    # e.g. [8, 9]
    hist = np.histogram(magnitudes, bins=bins_plot)

    # Generate histogram for plotting
    hist_plot = np.histogram(magnitudes, bins=bins_plot)

    # Reverse array orders
    bins = hist[1][::-1]
    counts = hist[0][::-1]

    hist_plot = hist_plot[0][::-1]
    bins_plot = bins_plot[::-1]
    
    # Calculate cumulative sums
    cum_hist = counts.cumsum()
    cum_hist_plot = hist_plot.cumsum()    

    # Ensure bins have the same length as the cumulative histogram.
    # Remove the upper bound for the highest interval.
    bins = bins[1:]
    bins_plot = bins_plot[1:]

    # Get annual rate
    cum_annual_rate = cum_hist/float(num_years)
    cum_annual_rate_plot = cum_hist_plot/float(num_years)
    
    new_cum_annual_rate = []
    for i in cum_annual_rate:
        new_cum_annual_rate.append(i+1e-20)

    new_cum_annual_rate_plot = []
    for i in cum_annual_rate_plot:
        new_cum_annual_rate_plot.append(i+1e-20)


    # Remove large values from catalogue for LS calculation, as these will
    # bias the solution
    new_cum_annual_rate_clip = []
    for i, value in enumerate(bins[::-1]):
        new_cum_annual_rate_clip.append(new_cum_annual_rate[-i-1])
    new_cum_annual_rate_clip = new_cum_annual_rate_clip[::-1]
            
    # Take logarithm
    log_cum_sum = np.log10(new_cum_annual_rate_clip)

    # Find annual rate of earthquakes greater than mean magnitude (of entire complete catalogue)
    mean_mag = np.mean(magnitudes)
    for i, value in enumerate(bins_plot[::-1]):

        if value >= mean_mag:
            annual_rate_mean_eq = new_cum_annual_rate[-i-1]
            break
        else:
            pass

    return bins, log_cum_sum, bins_plot, new_cum_annual_rate_plot, annual_rate_mean_eq
    
def calc_recurrence(event_set, min_mag = None, max_mag = None, max_mag_ls = None,
                    interval = 0.1, figurepath = None, subset = 'all', verbose = True):

    """This function reads an earthquake catalogue file and calculates the
    Gutenberg-Richter recurrence parameters using both least squares and
    maximum likelihood (Aki 1965) approaches.

    Results are plotted for both straightline fits and bounded
    Gutenberg-Richter curves. Also plotted is the curve that would result
    assuming a b-value of 1.

    Funtion arguments:

        infile: file containing earthquake catalogue
                Expected input file format: csv
                One header line
                Year of earthquake in 3rd column, magnitude in 6th column.
        min_mag: minimum magnitude for which data will be used - i.e. catalogue
                completeness
        max_mag: maximum magnitude used in bounded G-R curve. If not specified,
                defined as the maximum magnitude in the catlogue + 0.1 magnitude
                units.
        maximum magnitude for least squares: The maxumum magnitude used in the least squares
            analysis. Defaults to the maximum magnitude in the catalogue minus 1.0
            magnitude units.
        interval: Width of magnitude bins for generating cumulative histogram
                of earthquake recurrence for least squares fit. Default value is
                0.1 magnitude units.  
    
    """
    
    # If minimum magnitude is not specified, read all magnitudes
    if min_mag is not None:
        subset_name = 'clip_min_mag'
        event_set.create_subset(subset_name, min_mag=min_mag)
        event_subset = event_set.catalogue_subset[subset_name]
    else:
        subset_name = subset
        event_subset = event_set.catalogue_subset[subset_name]

    # Get data from catalogue
    event_set.get_magnitudes(subset_name=subset_name)
    magnitudes = event_set.magnitudes[subset_name]    
    event_set.get_times(subset_name=subset_name)
    years = event_set.times[subset_name]
    
    # If minimum magnitude is not specified default value to minimum in catalogue
    if min_mag is None:
        min_mag = min(magnitudes)
    else:
        min_mag = min(min(magnitudes), min_mag)
                      
    # If maximum magnitude is not specified default value to maximum in catalogue
    if max_mag is not None:
        pass
    else:
        max_mag = max(magnitudes) + 0.1

    num_eq = len(magnitudes)
    num_years = max(years).year-min(years).year
    annual_num_eq = float(num_eq)/num_years
    max_catalogue = max(magnitudes)

    if verbose:    
        print 'Minimum magnitude:', min_mag
        print 'Total number of earthquakes:', num_eq
        print 'years', num_years    
        print 'Annual number of earthquakes greater than Mw', min_mag,':', \
        annual_num_eq    
        print 'Maximum catalog magnitude:', max_catalogue
        print 'Mmax = ', max_mag 
    
    bins, log_cum_sum, bins_plot, new_cum_annual_rate_plot, annual_rate_mean_eq = \
                                        build_histograms(magnitudes, min_mag,
                                                         max_catalogue, num_years,
                                                         max_mag_ls = max_mag_ls,
                                                         interval = interval,
                                                         verbose = verbose)


    
    ###########################################################################
    # Fit a and b parameters using a varity of methods
    ###########################################################################
    a, b, alpha, beta = least_squares(bins, log_cum_sum)
    if verbose:
        print 'Least Squares: b value', -1. * b, 'a value', a
    b_mle, beta_mle = maximum_likelihood(magnitudes, min_mag)
    if verbose:
        print 'Maximum Likelihood: b value', b_mle
    
    ###########################################################################
    # Generate data to plot results
    ###########################################################################

    # Generate data to plot least squares linear curve
    # Calculate y-intercept for least squares solution
    yintercept = log_cum_sum[-1] - b * min_mag
    ls_fit = b * bins_plot + yintercept
    log_ls_fit = []
    for value in ls_fit:
        log_ls_fit.append(np.power(10,value))

    # Generate data to plot bounded Gutenberg-Richter for LS solution
    numer = np.exp(-1. * beta * (bins_plot - min_mag)) - \
            np.exp(-1. *beta * (max_mag - min_mag))
    denom = 1. - np.exp(-1. * beta * (max_mag - min_mag))
    ls_bounded = annual_num_eq * (numer / denom)
        
    # Generate data to plot maximum likelihood linear curve
    # Annual number of earthquakes greater than mean value
    #annual_num_mean_eq = np.mean(magnitudes)
    mle_fit = -1.0 * b_mle * bins_plot + 1.0 * b_mle * np.mean(magnitudes) + np.log10(annual_rate_mean_eq)
    log_mle_fit = []
    for value in mle_fit:
        log_mle_fit.append(np.power(10,value))

    # Generate data to plot bounded Gutenberg-Richter for MLE solution
    numer = np.exp(-1. * beta_mle * (bins_plot - min_mag)) - \
            np.exp(-1. *beta_mle * (max_mag - min_mag))
    denom = 1. - np.exp(-1. * beta_mle * (max_mag - min_mag))
    mle_bounded = annual_num_eq * (numer / denom)

    # Compare b-value of 1
    fit_data = -1.0 * bins_plot + min_mag + np.log10(annual_num_eq)
    log_fit_data = []
    for value in fit_data:
        log_fit_data.append(np.power(10,value))

    ###########################################################################
    # Plot the results
    ###########################################################################

    # Plotting
    fig = py.figure(figsize = (12,10))
    ax = fig.add_subplot(1,1,1)
    ax.scatter(bins_plot, new_cum_annual_rate_plot, label = 'Catalogue')
    ax.plot(bins_plot, log_ls_fit, c = 'r', label = 'Least Squares')
    ax.plot(bins_plot, ls_bounded, c = 'r', linestyle ='--', label = 'Least Squares Bounded')
    ax.plot(bins_plot, log_mle_fit, c = 'g', label = 'Maximum Likelihood')
    ax.plot(bins_plot, mle_bounded, c = 'g', linestyle ='--', label = 'Maximum Likelihood Bounded')
    ax.plot(bins_plot, log_fit_data, c = 'b', label = 'b = 1')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontsize(20) 
    ax.set_yscale('log')
    ax.legend(loc=1)
    ax.set_ylim([min(log_ls_fit) * 0.1, max(log_ls_fit) * 10.])
    ax.set_xlim([min_mag - 0.5, max_mag + 0.5])
    ax.set_ylabel('Annual probability', fontsize = '20')
    ax.set_xlabel('Magnitude', fontsize = '20')

    ax.grid(True)

    s = 'Minimum magnitude: %.1f \nAnnual number earthquakes > min mag: %.2f \nLS a,b: %.2f, %.2f \nMLE b: %.2f' \
    % (min_mag, annual_num_eq, a, -1. * b, b_mle)
    ax.text(min_mag - 0.25, min(log_ls_fit)* 0.5, s, fontsize = '14',
            bbox=dict(facecolor = 'white', alpha=0.5, pad = 10.))

    if figurepath is not None:
        py.savefig(figurepath)
        print 'Figure saved as', figurepath

    ##############################
    return a, b, b_mle, annual_num_eq


###############################################################################
    
if __name__=="__main__":

    if len(sys.argv) < 2:
        print 'Usage: python recurrence_from_catalog.py <input_file> <minimum magnitude = minimum magnitude in catalogue> \
<maximum magnitude = maximum magnitude in catalogue + 0.1> <maximum magnitude for least squares analysis = maximum magnitude - 1.0> <interval = 0.1>'
        sys.exit(-1)

    infile  = sys.argv[1]

    try:
        min_mag = float(sys.argv[2])
    except IndexError:
        print '\nMinimum magnitude not specified, defaulting to minimum magnitude in catalogue'
        min_mag = None

    try:       
        max_mag = float(sys.argv[3])
    except IndexError:
        print '\nMaximum magnitude not specified, defaulting to maximum magnitude in catalogue + 0.1'
        max_mag = None

    try:       
        max_mag_ls = float(sys.argv[4])
    except IndexError:
        print '\nMaximum magnitude for least squares analysis not specified, defaulting \
to maximum magnitude in catalogue - 1.0. You may want to check this after examining \
the data.'
        max_mag_ls = None

    try:
        interval = float(sys.argv[5])
    except IndexError:
        print '\nMagnitude bin interval not specfied, defaulting to 0.1 magnitude units'
        interval = 0.1

    figurepath = infile[:-4] + '.png'  
    EventSet = catalogue_reader.CatalogueReader(infile).EventSet
    calc_recurrence(EventSet, min_mag = min_mag, max_mag = max_mag,
                    max_mag_ls = max_mag_ls, interval = interval,
                    figurepath = figurepath, subset='all')
    py.show()
