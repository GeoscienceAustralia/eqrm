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


    
def plot_time_vs_magnitude(EventSet, subset_name, figurename = None):
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
    # plot it
    plt.scatter(years, magnitudes, marker = "x")
    plt.title(subset_name)
#    plt.grid(True)

    if figure_name is not None:
        plt.savefig(figure_name)
    plt.show()



if __name__=='__main__':
    
    file_path = '.'
    file_name = 'ISCGEMExtended_SEAsiaOceania.csv'
    in_file = os.path.join(file_path, file_name) 
    # Read data
    EventSet = catalogue_reader.CatalogueReader(in_file, file_format = 'iscgem_extended_csv').EventSet

    subset_name = 'all'
    EventSet.create_subset(subset_name)#subset_name, max_lon = max_lon, min_lon = min_lon,
                                  #  max_lat = max_lat, min_lat = min_lat)#,
                                    #min_mag = min_mag, min_depth= min_depth)

    # Specify line along which to plot cross-section

    if file_name.endswith('.nordic'):
        figure_base = file_name[:-7]
    else:
        figure_base = file_name[:-3]
    # Plot cross-section
    figurefilename = (figure_base + '_' + subset_name + '.png')
    figure_name = os.path.join(file_path, figurefilename)    
    plot_time_vs_magnitude(EventSet, subset_name, figurename = figure_name)



