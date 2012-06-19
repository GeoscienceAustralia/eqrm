import numpy as np
import matplotlib.pyplot as plt
import catalogue_reader
import earthquake_event
import datetime
import os
from recurrence_from_catalog import calc_recurrence


    
def plot_xsection(EventSet, subset_name, end_point, start_point,  figurename = None, width=None):
    """
    Plot a cross-section of event set or subset
    event_set = event_set object or event_set subset
    start_point, end_point = start and end of cross-section [longitude, latitude]
    width - specify width of cross-section - events off the cross-section
        line will be moved onto this line. Currently only designed for
        Cartesian coordinates.
    """

    # Move events onto line (use cosine rule)
    new_lon = []
    new_lat = []
    depth = []

    for event in EventSet.catalogue_subset[subset_name]:

        a = np.array([event.lon - start_point[0], event.lat - start_point[1]])
        b = np.array([end_point[0] - start_point[0], end_point[1] - start_point[1]])
        c = np.dot(a,b)/np.dot(b,b)*b
        # Think this maths is right but hasn't been tested yet!!!!!
        d = start_point + c
        new_lon.append(d[0])
        new_lat.append(d[1])

        depth.append(-1.0*event.depth)


        
    print 'start, end', start_point, end_point  
        
    plt.scatter(new_lon, depth)
    plt.title(subset_name)
    plt.grid(True)

    if figure_name is not None:
        plt.savefig(figure_name)
    plt.show()



if __name__=='__main__':
    
    file_path = '/model_area/earthquake_hazard/sulawesi/inputs/katalog'
    file_name = 'isc_sulawesi_1905-2010_revision.nordic'
    in_file = os.path.join(file_path, file_name) 
    # Read data
    EventSet = catalogue_reader.CatalogueReader(in_file).EventSet

    
##    # Specify subset parameter

##    subset_name = 'subset1'
##    max_lon = 121.1
##    min_lon = 119.3
##    max_lat = 1.6
##    min_lat = -0.5
##    start_point = [119.5, 1.2]
##    end_point = [120.9, -0.15]
##    min_mag = 4.8
##    min_depth = 35

##    subset_name = 'subset2'
##    max_lon = 122.6
##    min_lon = 120.8
##    max_lat = 2.45
##    min_lat = -0.9
##    start_point = [121.9, 2.2]
##    end_point = [121.9, -0.6]

##    subset_name = 'subset3'
##    max_lon = 124.0
##    min_lon = 122.5
##    max_lat = 1.7
##    min_lat = -1.6
##    start_point = [123.2, 1.7]
##    end_point = [123.2, -1.6]

    subset_name = 'subset4'
    max_lon = 125.4
    min_lon = 124.0
    max_lat = 1.6
    min_lat = -1.0
    start_point = [124.98, -0.301]
    end_point = [123.96, 1.01]
    
##    subset_name = 'subset5'
##    max_lon = 127.1
##    min_lon = 125.4
##    max_lat = 1.2
##    min_lat = -0.6
##    start_point = [127.4, 0.25]
##    end_point = [125.42, 1.07]

##    subset_name = 'subset6'
##    max_lon = 127.2
##    min_lon = 121.5
##    max_lat = 4.3
##    min_lat = 0.7
##    start_point = [121.5, 2.6]
##    end_point = [127.2, 2.6]

##    subset_name = 'subset7'
##    max_lon = 126.2
##    min_lon = 122.4
##    max_lat = -1.1
##    min_lat = -2.6
##    start_point = [122.4, -1.9]
##    end_point = [126.2, -1.9]  
    
    EventSet.create_subset(subset_name, max_lon = max_lon, min_lon = min_lon,
                                    max_lat = max_lat, min_lat = min_lat)#,
                                    #min_mag = min_mag, min_depth= min_depth)

    # Specify line along which to plot cross-section

    if file_name.endswith('.nordic'):
        figure_base = file_name[:-7]
    # Plot cross-section
    xsection_figurefilename = (figure_base + '_' + str(start_point[0]) + '_' + str(start_point[1]) + '_' +
                      str(end_point[0]) + '_' + str(end_point[0]) + '_' + subset_name + '.png')
    figure_name = os.path.join(file_path, 'figures', xsection_figurefilename)    
    plot_xsection(EventSet, subset_name, [max_lon, max_lat], [min_lon, min_lat], figurename = figure_name)

    # Plot recurrence
    recurrence_figure_name = xsection_figurefilename[:-4] + '_recurrence.png'
    figure_name = os.path.join(file_path, 'figures', recurrence_figure_name)  
    calc_recurrence(EventSet.catalogue_subset[subset_name], min_mag = 4.5, max_mag_ls = 5.5, figurepath = figure_name)


