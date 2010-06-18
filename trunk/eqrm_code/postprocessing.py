#!/usr/bin/env python
"""

"""
import scipy
from scipy import loadtxt
import csv 

from eqrm_code.csv_interface import csv_to_arrays
from eqrm_code.structures import attribute_conversions

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
        
# ------------------------------------------------------------
if __name__ == '__main__':  
    pass
