import os
import sys
import unittest
import tempfile
from os import sep, path
   
from scipy import array, allclose

from eqrm_code.util import dict2csv
from eqrm_code.misc import reduce_structure_db

from eqrm_code import perf


class Test_misc(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    @perf.benchmark
    def test_reduce_structure_db(self):
        handle, file_name_in = tempfile.mkstemp('.csv','test_throw_away_')
        os.close(handle)
        handle, file_name_out = tempfile.mkstemp('_out.csv','test_throw_away_')
        os.close(handle)
        file_name_in, attribute_dic = write_test_file(file_name_in)
        reduce_structure_db(file_name_in,file_name_out,[0])

        os.remove(file_name_in)
        os.remove(file_name_out)

    # This is not actually a test.
    # It is setting up for the test.
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
    suite = unittest.makeSuite(Test_misc,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
