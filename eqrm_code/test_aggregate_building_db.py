import os
import sys
import unittest
import tempfile
import csv
import copy
from os import sep, path
from os.path import join
   
from scipy import array, allclose

from eqrm_code.csv_interface import csv_to_arrays
from eqrm_code.aggregate_building_db import aggregate_building_db, \
     Building_db_writer
from eqrm_code.structures import attribute_conversions, Structures
from eqrm_code.util import dict2csv

"""
"""

class Test_Structures(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def not_test_how_it_works(self):
        handle, file_name = tempfile.mkstemp('.csv','test_struct_')
        os.close(handle)
        file_name, attribute_dic = write_test_file(file_name)

        # Let's get the current dir position
        this_dir, tail = path.split( __file__)
        #print "eqrm_dir", eqrm_dir
        if this_dir == '':
            this_dir = '.'
        eqrm_dir = this_dir+sep+'..'
        data_dir = eqrm_dir+sep+'resources'+sep+'data'+sep
        #print "data_dir", data_dir

        # Build lookup table for building parameters
        buildpars={
            0:'building_parameters_workshop_1',
            1:'building_parameters_workshop',
            2:'building_parameters_hazus',
            3:'building_parameters_workshop_2',
            4:'building_parameters_workshop_3',
            5:'building_parameters_degrading_capacity'}

        # create links to required building parameters
        building_parameters=data_dir+buildpars[5]
        sites=Structures.from_csv(
            file_name,
            building_parameters,
            eqrm_dir
            )
        os.remove(file_name)
    
    
    
    def test_aggregate_building_db(self):
        attribute_dic={
            'BID':[1,2,3], # This is really ufi
            'LATITUDE':[-1.20,-1.15,-1.60],
            'LONGITUDE':[1.30,1.15,1.60],
            'STRUCTURE_CLASSIFICATION':['W1BVTILE','URMLMETAL','URMLMETAL'],
            'STRUCTURE_CATEGORY':['BUILDING','BUILDING','BUILDING'],
            'HAZUS_USAGE':['RES1','COM5','COM5'],
            'SUBURB':['MEREWETHER','MEREWETHER','MEREWETHER'],
            'POSTCODE':[22,2291,2291],
            'PRE1989':[0,0,0],
            'HAZUS_STRUCTURE_CLASSIFICATION':['W1','C1','C1'],
            'CONTENTS_COST_DENSITY':[150,15,60],
            'BUILDING_COST_DENSITY':[30,1.5,6.0],
            'FLOOR_AREA':[50,40,10],
            'SURVEY_FACTOR':[1,2,1],
            'FCB_USAGE':[111,491,491],
            'SITE_CLASS':['A','B','B']
            }
        attribute_dic, site = write_aggregate_read_csv(attribute_dic)
        #print "test_aggregate_building_db site", site
        
        self.assertEqual(2,len(site['UFI']))
        for i in [0,1]:
            if site['UFI'][i] == 1:
                self.assertEqual(site['LATITUDE'][i], -1.20)
                self.assertEqual( 
                    site['STRUCTURE_CLASSIFICATION'][i], 'W1BVTILE')
                self.assertEqual(site['SURVEY_FACTOR'][i], 1)
                self.assertEqual( site['CONTENTS_COST_DENSITY'][i] , 150)
                self.assertEqual(site['FCB_USAGE'][i] , 111)
                self.assertEqual(site['POSTCODE'][i] , 22)
                self.assertEqual(
                    site['HAZUS_STRUCTURE_CLASSIFICATION'][i] , 'W1')
                
            elif site['UFI'][i] == 2:
                self.assertEqual(site['LATITUDE'][i] , -1.30)
                self.assertEqual( 
                    site['STRUCTURE_CLASSIFICATION'][i], 'URMLMETAL')
                self.assertEqual(site['SURVEY_FACTOR'][i], 3)
                self.assertEqual(site['CONTENTS_COST_DENSITY'][i] , 30)
                self.assertEqual(site['FCB_USAGE'][i] , 491)
                self.assertEqual(site['POSTCODE'][i] , 2291)
            

    def test_structure_aggregate_building_db_load(self):
        attribute_dic={
            'BID':[1,2,3], # This is really ufi
            'LATITUDE':[-20,-15,-60],
            'LONGITUDE':[130,115,160],
            'STRUCTURE_CLASSIFICATION':['W1BVTILE','URMLMETAL','URMLMETAL'],
            'STRUCTURE_CATEGORY':['BUILDING','BUILDING','BUILDING'],
            'HAZUS_USAGE':['RES1','COM5','COM5'],
            'SUBURB':['MEREWETHER','MEREWETHER','MEREWETHER'],
            'POSTCODE':[22,2291,2291],
            'PRE1989':[0,0,0],
            'HAZUS_STRUCTURE_CLASSIFICATION':['W1','C1','C1'],
            'CONTENTS_COST_DENSITY':[150,15,60],
            'BUILDING_COST_DENSITY':[30,1.5,6.0],
            'FLOOR_AREA':[50,40,10],
            'SURVEY_FACTOR':[1,2,1],
            'FCB_USAGE':[111,491,491],
            'SITE_CLASS':['A','B','B']
            }
        attribute_dic, sites = write_aggregate_read_struct(attribute_dic)
        site = sites.attributes
        #print "site", site
        self.assertEqual(2,len(site['FCB_USAGE']))
        for i in [0,1]:
            if site['FCB_USAGE'][i] == 111:
                self.assertEqual(sites.latitude[i], -20)
                self.assertEqual( 
                    site['STRUCTURE_CLASSIFICATION'][i], 'W1BVTILE')
                self.assertEqual(site['SURVEY_FACTOR'][i], 1)
                self.assertEqual( site['CONTENTS_COST_DENSITY'][i] , 150)
                self.assertEqual(site['POSTCODE'][i] , 22)
                self.assertEqual(
                    site['HAZUS_STRUCTURE_CLASSIFICATION'][i] , 'W1')
                
            elif site['FCB_USAGE'][i] == 491:
                self.assertEqual(sites.latitude[i] , -30)
                self.assertEqual( 
                    site['STRUCTURE_CLASSIFICATION'][i], 'URMLMETAL')
                self.assertEqual(site['SURVEY_FACTOR'][i], 3)
                self.assertEqual(site['CONTENTS_COST_DENSITY'][i] , 30)
                self.assertEqual(site['POSTCODE'][i] , 2291)
            else:
                self.assertEqual(1==2)
                

                
    def Xtest_Building_db_writer(self):
        # manual check of the file.
        handle, file_name = tempfile.mkstemp('.csv','test_aggregate_')
        os.close(handle)
        
        a = Building_db_writer(file_name)
        a.write_header()
        aggregate = [0,1,2,3,4,5,6,7,8,9]
        row_aggrigate = [0,1,2,3,4,5]
        survey_factor_sum = 4
        a.write_row(aggregate,row_aggrigate, survey_factor_sum)
        a.write_row(aggregate,row_aggrigate, survey_factor_sum)
        
        
        
def write_aggregate_read_csv(attribute_dic=None,
                       buildings_usage_classification='HAZUS'  ):
        handle, file_name = tempfile.mkstemp('.csv','test_aggregate_csv_')
        os.close(handle)
        file_name, attribute_dic = write_test_file(file_name,attribute_dic)

        attribute_conversions_extended = copy.deepcopy(attribute_conversions)
        attribute_conversions_extended['UFI'] = int
        file_out = file_name + "out"
        aggregate_building_db(file_name, file_out)
        site = csv_to_arrays(file_out,
                         **attribute_conversions_extended)
        os.remove(file_name)
        os.remove(file_out)
        return  attribute_dic, site
        
def write_aggregate_read_struct(attribute_dic=None,
                       buildings_usage_classification='HAZUS'  ):
        handle, file_name = tempfile.mkstemp('.csv','test_aggregate_struct_')
        os.close(handle)
        file_name2delete, attribute_dic = write_test_file(
            file_name,attribute_dic)
        
        # Let's get the current dir position
        this_dir, tail = path.split( __file__)
        #print "eqrm_dir", eqrm_dir
        if this_dir == '':
            this_dir = '.'
        eqrm_dir = this_dir+sep+'..'

        attribute_conversions_extended = copy.deepcopy(attribute_conversions)
        attribute_conversions_extended['UFI'] = int
        aggregate_building_db(file_name)

        
        # Build lookup table for building parameters
        buildpars={
            0:'building_parameters_workshop_1',
            1:'building_parameters_workshop',
            2:'building_parameters_hazus',
            3:'building_parameters_workshop_2',
            4:'building_parameters_workshop_3',
            5:'building_parameters_degrading_capacity'}

        # create links to required building parameters
        building_parameters = buildpars[5]
        default_input_dir = join(eqrm_dir,
                                 'resources','data','')
        sites=Structures.from_csv(
            file_name,
            building_parameters,
            default_input_dir=default_input_dir,
            eqrm_dir=eqrm_dir,
             buildings_usage_classification=buildings_usage_classification
            )
        os.remove(file_name2delete)
        return  attribute_dic, sites
    
def write_test_file(file_name, attribute_dic=None):

    title_index_dic={
        'BID':0,
        'LATITUDE':1,
        'LONGITUDE':2,
        'STRUCTURE_CLASSIFICATION':3,
        'STRUCTURE_CATEGORY':4,
        'HAZUS_USAGE':5,
        'SUBURB':6,
        'POSTCODE':7,
        'PRE1989':8,
        'HAZUS_STRUCTURE_CLASSIFICATION':9,
        'CONTENTS_COST_DENSITY':10,
        'BUILDING_COST_DENSITY':11,
        'FLOOR_AREA':12,
        'SURVEY_FACTOR':13,
        'FCB_USAGE':14,
        'SITE_CLASS':15
        }    

    if attribute_dic is None:
        attribute_dic={
            'BID':[1,2],
            'LATITUDE':[-32.9,32.7],
            'LONGITUDE':[151.7,151.3],
            'STRUCTURE_CLASSIFICATION':['W1BVTILE','S3'],
            'STRUCTURE_CATEGORY':['BUILDING','BUILDING'],
            'HAZUS_USAGE':['RES1','COM8'],
            'SUBURB':['MEREWETHER','MEREWETHER'],
            'POSTCODE':[2291,2291],
            'PRE1989':[0,1],
            'HAZUS_STRUCTURE_CLASSIFICATION':['W1','URML'],
            'CONTENTS_COST_DENSITY':[300,10000],
            'BUILDING_COST_DENSITY':[600,1000],
            'FLOOR_AREA':[150,300],
            'SURVEY_FACTOR':[1,9.8],
            'FCB_USAGE':[111,451],
            'SITE_CLASS':['A','B']
            }    
    dict2csv(file_name, title_index_dic, attribute_dic)
    return file_name, attribute_dic
    

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Structures,'test')
    #suite = unittest.makeSuite(Test_Structures,'test_aggregate_building_db')
    runner = unittest.TextTestRunner()
    runner.run(suite)
