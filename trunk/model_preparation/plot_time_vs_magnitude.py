"""plot time vs magnitude
Plots a scatter-plot of time vs magnitude
Jonathan Griffin, Geoscience Australia, March 2014
"""

import numpy as np
import matplotlib.pyplot as plt
import catalogue_reader
import earthquake_event
import datetime
import os
from recurrence_from_catalog import calc_recurrence


    
def plot_time_vs_magnitude(EventSet, subset_name, step_x = None, step_y = None, figurename = None):
    """
    Plot a scatter-plot of time vs magnitude.
    Also plots a step function based on a manually passed array
    """

    # Get times and magnitudes 
    magnitudes = []
    years = []
    for event in EventSet.catalogue_subset[subset_name]:
        magnitudes.append(event.magnitude)
        years.append(event.time.year)
    max_year = max(years)
    min_year = min(years)
    # plot it
    plt.scatter(years, magnitudes, marker = "x")
    plt.title(subset_name)
    ax = plt.gca()
    ax.set_xlabel('Year')
    ax.set_ylabel('Magnitude')
#    plt.grid(True)
    if step_x is not None and step_y is not None:
        # Fill out points to create step function
        x_filled = []
        y_filled = []
        for i in range(len(step_x)):
            if i == 0:
                #Handle first step
                x_filled.append(min_year)
                y_filled.append(step_y[i]) # Extend data to start of time series
                x_filled.append(step_x[i])
                y_filled.append(step_y[i])
                x_filled.append(step_x[i+1]) # Extend step to next data point
                y_filled.append(step_y[i])
            elif i == len(step_x)-1:
                # final step
                x_filled.append(step_x[i])
                y_filled.append(step_y[i])
                x_filled.append(max_year) # Extend to end of time series
                y_filled.append(step_y[i])
            else:
                # Handle final step
                x_filled.append(step_x[i])
                y_filled.append(step_y[i])
                x_filled.append(step_x[i+1]) # Extend step to next data point
                y_filled.append(step_y[i])
        plt.plot(x_filled, y_filled)
            

    if figure_name is not None:
        plt.savefig(figure_name)
    plt.show()



if __name__=='__main__':
    
    file_path = '.'
    file_name = 'ISCGEMExtended_SEAsiaOceania.csv'
    in_file = os.path.join(file_path, file_name) 
    # Read data, specify format
    EventSet = catalogue_reader.CatalogueReader(in_file, file_format = 'iscgem_extended_csv').EventSet

    # Specify array for step-plot manually (optional call to plot_time_vs_magnitude)
    x = [1900, 1920, 1963, 1978, 1997]
    y = [6.3, 6.0, 4.9, 4.7, 4.3]

    subset_name = 'all'
    EventSet.create_subset(subset_name)#subset_name, max_lon = max_lon, min_lon = min_lon,
                                  #  max_lat = max_lat, min_lat = min_lat)#,
                                    #min_mag = min_mag, min_depth= min_depth)

    # Specify line along which to plot cross-section

    if file_name.endswith('.nordic'):
        figure_base = file_name[:-7]
    else:
        figure_base = file_name[:-4]
    # Plot cross-section
    figurefilename = (figure_base + '_' + subset_name + '.png')
    figure_name = os.path.join(file_path, figurefilename)    
    plot_time_vs_magnitude(EventSet, subset_name, step_x = x, step_y = y, figurename = figure_name)



