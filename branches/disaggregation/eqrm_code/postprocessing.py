#!/usr/bin/env python
"""

"""
import scipy
from scipy import loadtxt, load, where
import csv 
import os

from eqrm_code.csv_interface import csv_to_arrays
from eqrm_code.structures import attribute_conversions
from eqrm_code.projections import azimuthal_orthographic_xy_to_ll as xy_to_ll
from eqrm_code.parse_in_parameters import create_parameter_data
from eqrm_code.event_set import load_event_set
from eqrm_code.sites import load_sites
from eqrm_code.output_manager import load_motion, save_motion_to_csv
from eqrm_code.parallel import Parallel

def calc_loss_deagg_suburb(bval_path_file, total_building_loss_path_file,
                            site_db_path_file, file_out):
    """ Given EQRM ouput data, produce a csv file showing loss per suburb

    The produced csv file shows total building loss, total building
    value and loss as a percentage.  All of this is shown per suburb.
    
    bval_path_file - location and name of building value file produced by EQRM
    total_building_loss_path_file - location and name of the total building
      loss file
    site_db_path_file - location and name of the site database file
    
    Note: This can be generalised pretty easily, to get results
          deaggregated on other columns of the site_db
    """
    aggregate_on = ['SUBURB']
    
    # Load all of the files.    
    site = csv_to_arrays(site_db_path_file,
                         **attribute_conversions)
    #print "site", site
    bvals = loadtxt(bval_path_file, dtype=scipy.float64,
                    delimiter=',', skiprows=0)
    #print "bvals", bvals
    #print "len(bvals", len(bvals)
    
    total_building_loss = loadtxt(total_building_loss_path_file,
                                  dtype=scipy.float64,
                                  delimiter=' ', skiprows=1)
    #print "total_building_loss", total_building_loss
    #print "total_building_loss shape", total_building_loss.shape
    site_count = len(site['BID'])
    assert site_count == len(bvals)
    assert site_count == total_building_loss.shape[1]
    # For aggregates
    # key is the unique AGGREGATE_ON combination .eg ('Hughes', 2605,...)
    # Values are a list of indices where the combinations are repeated in site
    aggregates = {} 
    for i in range(site_count):
        assert site['BID'][i] == int(total_building_loss[0,i])
        marker = []
        for name in aggregate_on:
            marker.append(site[name][i])
        marker = tuple(marker)
        aggregates.setdefault(marker,[]).append(i)
    #print "aggregates", aggregates
    
    handle = csv.writer(open(file_out, 'w'), lineterminator='\n')
    
    handle.writerow(['percent losses (building and content) by suburb'])
    handle.writerow(['suburb','loss','value', 'percent loss'])
    handle.writerow(['',' ($ millions)',' ($ millions)', ''])
    keys = aggregates.keys()
    keys.sort()
    for key in keys:
        sum_loss = 0
        sum_bval = 0        
        for row in aggregates[key]:
            sum_loss += total_building_loss[1][row]
            sum_bval += bvals[row]
        handle.writerow([key[0],sum_loss/1000000., sum_bval/1000000., 
                         sum_loss/sum_bval*100.])

def events_shaking_a_site(output_dir,
                          site_tag,
                          site_lat,
                          site_lon,
                          period,
                          is_bedrock):
    """events_shaking_a_site
    Given disaggregated output data produce a csv file showing ground motion 
    and event information for the given site and period. 
    
    Parameters:
    output_dir - path to directory where the simulation data has been produced,
                 and where the output files will be placed
    site_tag   - used to identify the appropriate data as input
    site_lat   - site latitude
    site_lon   - site longitude (use the closest site as the cockey flies)
    period     - attenuation period (must be an exact match)
    is_bedrock - if True use bedrock results, else use soil results
    
    Output file:
    <output_dir>/
    - if is_bedrock:
    <site_tag>_bedrock_SA_events_ap[<period>]_lat[<site_lat>]_lon[<site_lon>].csv
    - else:
    <site_tag>_soil_SA_events_ap[<period>]_lat[<site_lat>]_lon[<site_lon>].csv
    
    Columns:
    'ground_motion'         - ground motion value
    'ground_motion_model'   - ground motion model used
    'trace_start_lat'       - rupture trace start latitude
    'trace_start_lon'       - rupture trace start longitude
    'trace_end_lat'         - rupture trace end latitude
    'trace_end_lon'         - rupture trace end longitude
    'rupture_centroid_lat'  - rupture centroid latitude
    'rupture_centroid_lon'  - rupture centroid longitude
    'depth'                 - rupture depth to centroid (km)
    'azimuth'               - rupture azimuth (degrees from true North)
    'dip'                   - rupture dip
    'Mw'                    - rupture moment magnitude
    'length'                - rupture length
    'width'                 - rupture width
    'activity'              - event activity (probability that the event will
                              occur this year)
    'Rjb'                   - Joyner-Boore distance to rupture plane
    'Rrup'                  - Closest distance to rupture plane
    'site_lat'              - Closest site latitude
    'site_lon'              - Closest site longitude
    """
    
    # Set up objects
    if is_bedrock:
        motion_name = 'bedrock_SA'
    else:
        motion_name = 'soil_SA'
    
    # EQRM flags
    eqrm_flags = create_parameter_data(os.path.join(output_dir, 
                                                    'eqrm_flags.py'))
    atten_periods = eqrm_flags.atten_periods
    if period not in eqrm_flags.atten_periods:
        raise Exception("Period %s not in atten_periods %s" % (period,
                                                               atten_periods))
    period_ind = where(period == atten_periods)[0][0]
    
    parallel = Parallel(is_parallel=False)
    
    # Event set objects
    (event_set,
     event_activity,
     source_model) = load_event_set(parallel, 
                                    os.path.join(output_dir,
                                                 '%s_event_set' % site_tag))
    
    # Site objects
    sites = load_sites(parallel, os.path.join(output_dir,'%s_sites' % site_tag))
    closest_site_ind = sites.closest_site(site_lat, site_lon)
    closest_site_lat = sites[closest_site_ind].latitude[0]
    closest_site_lon = sites[closest_site_ind].longitude[0]
    
    # Ground motion
    motion = load_motion(output_dir, site_tag, motion_name)
    
    # Get the motion that corresponds to this site, collapsing spawn, rm, period
    # Motion dimensions - spawn, gmm, rm, sites, events, period
    motion_for_site = motion[0,:,0,closest_site_ind,:,period_ind]
    
    (event_set.trace_end_lat,
     event_set.trace_end_lon) = xy_to_ll( event_set.rupture_centroid_x,
                                         -event_set.rupture_centroid_y,
                                          event_set.rupture_centroid_lat,
                                          event_set.rupture_centroid_lon,
                                          event_set.azimuth)
    
    # Event activity dimensions - spawn, gmm, rm, events
    # Collapse spawn and rm
    event_activity = event_activity.event_activity[0,:,0,:]
    
    # Distances
    Rjb = sites.distances_from_event_set(event_set).distance('Joyner_Boore')
    Rjb_for_site = Rjb.swapaxes(0,1)[:,closest_site_ind]
    Rrup = sites.distances_from_event_set(event_set).distance('Rupture')
    Rrup_for_site = Rrup.swapaxes(0,1)[:,closest_site_ind]
    
    # Create file and write headers
    filename = '%s_%s_events_ap%s_lat%s_lon%s.csv' % (site_tag,
                                                      motion_name,
                                                      period,
                                                      closest_site_lat,
                                                      closest_site_lon)
    handle = csv.writer(open(os.path.join(output_dir, filename), 'w'))
    handle.writerow(['ground_motion',
                     'ground_motion_model',
                     'trace_start_lat',
                     'trace_start_lon',
                     'trace_end_lat',
                     'trace_end_lon',
                     'rupture_centroid_lat',
                     'rupture_centroid_lon',
                     'depth',
                     'azimuth',
                     'dip',
                     'Mw',
                     'length',
                     'width',
                     'activity',
                     'Rjb',
                     'Rrup',
                     'site_lat',
                     'site_lon'])
    
    # Loop over events
    for i in range(motion_for_site.shape[1]): # events
        trace_start_lat = event_set.trace_start_lat[i]
        trace_start_lon = event_set.trace_start_lon[i]
        trace_end_lat = event_set.trace_end_lat[i]
        trace_end_lon = event_set.trace_end_lon[i]
        rupture_centroid_lat = event_set.rupture_centroid_lat[i]
        rupture_centroid_lon = event_set.rupture_centroid_lon[i]
        depth = event_set.depth[i]
        azimuth = event_set.azimuth[i]
        dip = event_set.dip[i]
        mw = event_set.Mw[i]
        length = event_set.length[i]
        width = event_set.width[i]
        
        rjb = Rjb_for_site[i]
        rrup = Rrup_for_site[i]
        
        ground_motion = motion_for_site[:,i]
        activity = event_activity[:,i]
        
        event_source = source_model[int(event_set.source[i])]
        for gmm in event_source.atten_models:
            gmm_index = where(event_source.atten_models == gmm)[0][0]
            handle.writerow([ground_motion[gmm_index],
                             gmm,
                             trace_start_lat,
                             trace_start_lon,
                             trace_end_lat,
                             trace_end_lon,
                             rupture_centroid_lat,
                             rupture_centroid_lon,
                             depth,
                             azimuth,
                             dip,
                             mw,
                             length,
                             width,
                             activity[gmm_index],
                             rjb,
                             rrup,
                             closest_site_lat,
                             closest_site_lon])
    
    return os.path.join(output_dir, filename)


def generate_motion_csv(output_dir,
                        site_tag,
                        is_bedrock):
    """A wrapper for save_motion_to_csv, previously used by analysis
    TODO: better docstring!
    """
    # Set up objects
    if is_bedrock:
        motion_name = 'bedrock_SA'
    else:
        motion_name = 'soil_SA'
    
    # EQRM flags
    eqrm_flags = create_parameter_data(os.path.join(output_dir,'eqrm_flags.py'))
    
    # Ground motion
    motion = load_motion(output_dir, site_tag, motion_name)
    
    return save_motion_to_csv(not is_bedrock, eqrm_flags, motion)

    
# ------------------------------------------------------------
if __name__ == '__main__':  
    pass
