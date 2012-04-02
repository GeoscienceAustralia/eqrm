"""
 Title: aggregate_building_db.py
  
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  CreationDate:  2008-02-11 

  Description: A stand alone preprocessing tool.  Used to aggregate
  site data so similar buildings are represented by 1 site, by
  changing the SURVEY_FACTOR.

  The lat and longs of all the sites in a grouping are averaged to get
  the position of the structure representing the group.
  
NOTE: Currently this is hard coded to fcb_usage and STRUCTURE_CLASSIFICATION,
which is Edwards structure catergories

  Version: $Revision: 1073 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-08-19 16:47:42 +1000 (Wed, 19 Aug 2009) $
  
  Copyright 2007 by Geoscience Australia
"""

from eqrm_code.csv_interface import csv_to_arrays
from eqrm_code.structures import attribute_conversions
from scipy import zeros
import csv 

# WARNING this info is hard coded in Building_db_writer
AGGREGATE_ON = ['POSTCODE',
                'SITE_CLASS',
                'STRUCTURE_CLASSIFICATION',
                'FCB_USAGE',
                'PRE1989',
                'STRUCTURE_CATEGORY',
                'HAZUS_USAGE',
                'SUBURB',
                'HAZUS_STRUCTURE_CLASSIFICATION']

# WARNING this info is hard coded in Building_db_writer
AVERAGE_ON = [
    'FLOOR_AREA',
    'LATITUDE',
    'LONGITUDE',
    'CONTENTS_COST_DENSITY',
    'BUILDING_COST_DENSITY'
    ]
# NOTE,  SURVEY_FACTOR  handled seperately

def aggregate_building_db(sites_filename_in, sites_filename_out=None):
    """
    Aggregate building data base data.
    All structures with the same 'POSTCODE',
                'SITE_CLASS',
                'STRUCTURE_CLASSIFICATION',
                'FCB_USAGE',
                'PRE1989',
                'STRUCTURE_CATEGORY',
                'HAZUS_USAGE',
                'SUBURB',
                'HAZUS_STRUCTURE_CLASSIFICATION'

                Are aggregated as one structure.

    These attributes are averaged;
                                  'FLOOR_AREA',
                                  'LATITUDE',
                                  'LONGITUDE',
                                  'CONTENTS_COST_DENSITY',
                                  'BUILDING_COST_DENSITY'

    #FIXME DSG Add a column that gives the BID's (building ID) from the
                                  unaggredated data for each structure
     
    """
    if sites_filename_out is None:
        sites_filename_out = sites_filename_in
        
    #if aggregate_on is None:
    aggregate_on = AGGREGATE_ON

    #if average_on is None:
    average_on = AVERAGE_ON
        
    survey_factor = 'SURVEY_FACTOR'
    ufi_name = 'BID'
    
    site = csv_to_arrays(sites_filename_in,
                         **attribute_conversions)
    writer = Building_db_writer(sites_filename_out)
    writer.write_header()
    
    # For aggregates
    # key is the unique AGGREGATE_ON combination .eg ('Hughes', 2605,...)
    # Values are a list of indices where the combinations are repeated in site
    aggregates = {} 
    for i in range(len(site['BID'])):
        #print "site['BID'][i]",site['BID'][i]
        marker = []
        for name in aggregate_on:
            marker.append(site[name][i])
        marker = tuple(marker)
        aggregates.setdefault(marker,[]).append(i)

    for agg, agg_indexes in aggregates.iteritems():
        
        # An agg_indexes is a collection of rows, specified by index,
        # to be aggregated        
        row_sum = zeros(len(average_on),dtype=float)
        survey_factor_sum = 0.0
        UFI = site[ufi_name][agg_indexes[0]]
        for row in agg_indexes:
            survey_factor_sum += site[survey_factor][row]
            for i, name in enumerate(average_on):
                row_sum[i] += site[name][row]*site[survey_factor][row]
        row_aggrigate = row_sum/survey_factor_sum
        writer.write_row(agg, row_aggrigate, survey_factor_sum, UFI)

class Building_db_writer(object):
    """ Class to write a site file 
    """
    def __init__(self, file_out):
        self.handle = csv.writer(open(file_out, 'w'), lineterminator='\n')
        self.BID = 1
        aggregate_on = AGGREGATE_ON
        average_on = AVERAGE_ON

        self.aggregate_on_index = {}
        for i,agg in enumerate(aggregate_on):
            self.aggregate_on_index[agg]=i
        
        self.average_on_index = {}
        for i,agg in enumerate(average_on):
            self.average_on_index[agg]=i    

        
    def write_header(self, header=None):
        if header is None:
            header = ['BID','LATITUDE','LONGITUDE',
            'STRUCTURE_CLASSIFICATION',
            'STRUCTURE_CATEGORY',
            'HAZUS_USAGE',
            'SUBURB',
            'POSTCODE',
            'PRE1989',
            'HAZUS_STRUCTURE_CLASSIFICATION',
            'CONTENTS_COST_DENSITY',
            'BUILDING_COST_DENSITY',
            'FLOOR_AREA',
            'SURVEY_FACTOR',
            'FCB_USAGE',
            'SITE_CLASS',
            'UFI']
            self.handle.writerow(header)

            
            
    def write_row(self, aggregate, row_aggrigate, survey_factor_sum, UFI):
        row = []
        row.append(self.BID)
        self.BID += 1
        row.append(row_aggrigate[self.average_on_index['LATITUDE']])
        row.append(row_aggrigate[self.average_on_index['LONGITUDE']])
        row.append(aggregate[self.aggregate_on_index['STRUCTURE_CLASSIFICATION']])
        row.append(aggregate[self.aggregate_on_index['STRUCTURE_CATEGORY']])
        row.append(aggregate[self.aggregate_on_index['HAZUS_USAGE']])
        row.append(aggregate[self.aggregate_on_index['SUBURB']])
        row.append(aggregate[self.aggregate_on_index['POSTCODE']])
        row.append(aggregate[self.aggregate_on_index['PRE1989']])
        row.append(aggregate[self.aggregate_on_index['HAZUS_STRUCTURE_CLASSIFICATION']])
        row.append(row_aggrigate[self.average_on_index['CONTENTS_COST_DENSITY']])
        row.append(row_aggrigate[self.average_on_index['BUILDING_COST_DENSITY']])
        row.append(row_aggrigate[self.average_on_index['FLOOR_AREA']])
        row.append(survey_factor_sum)
        row.append(aggregate[self.aggregate_on_index['FCB_USAGE']])
        row.append(aggregate[self.aggregate_on_index['SITE_CLASS']])
        row.append(UFI)
        self.handle.writerow(row)
