import catalogue_reader
import recurrence_from_catalog
import os,sys

file_path = '/model_area/earthquake_hazard/sulawesi/inputs/katalog'
file_name = 'isc_sulawesi_1905-2010_revision.nordic'
in_file = os.path.join(file_path, file_name) 
# Read data
EventSet = catalogue_reader.CatalogueReader(in_file).EventSet

##subset_name = 'slab'
##min_depth = 35
##
##EventSet.create_subset(subset_name, min_depth = min_depth)


##subset_name = 'subset4'
##max_lon = 125.4
##min_lon = 124.0
##max_lat = 1.6
##min_lat = -1.0
##start_point = [124.98, -0.301]
##end_point = [123.96, 1.01]

##subset_name = 'subset4'
##max_lon = 125.4
##min_lon = 124.0
##max_lat = 1.6
##min_lat = -1.0
##start_point = [124.98, -0.301]
##end_point = [123.96, 0.5]
##min_depth = 35
##max_depth = 150

subset_name = 'subset4_shallow'
max_lon = 125.4
min_lon = 124.0
max_lat = 1.6
min_lat = -1.0
start_point = [124.98, -0.301]
end_point = [123.96, 1.01]
min_depth = 150
max_depth = 250

EventSet.create_subset(subset_name, max_lon = max_lon, min_lon = min_lon,
                                    max_lat = max_lat, min_lat = min_lat,
                                    min_depth = min_depth, max_depth = max_depth)

figure_name = in_file[:-7] + '_instraslab_4.png' 
recurrence_from_catalog.calc_recurrence(EventSet.catalogue_subset[subset_name],
                                        min_mag = 4.8, max_mag_ls = 6.0,
                                        figurepath = figure_name)
