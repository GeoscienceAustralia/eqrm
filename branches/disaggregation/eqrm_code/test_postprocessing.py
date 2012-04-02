import os
import sys
import unittest
import tempfile
import scipy
from scipy import loadtxt, array

from eqrm_code.util import dict2csv
from eqrm_code.postprocessing import *

class Test_postprocessing(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_calc_loss_deagg_suburb(self):
        
        handle, sitedb_file = tempfile.mkstemp('.csv','test_post_processing_')
        os.close(handle)
        sitedb_file, attribute_dic = write_test_file(sitedb_file)
        
        handle, bval_file = tempfile.mkstemp('.csv','test_post_processing_')
        os.close(handle)
        handle = open(bval_file,'w')
        bval = [4000000.00, 2000000.00, 10000000.00]
        bval_str = [str(x) for x in bval]
        column = '\n'.join(bval_str)
        handle.write(column)
        handle.close()
        
        handle, building_loss_file = tempfile.mkstemp(
            '.csv','test_post_processing_')
        os.close(handle)
        handle = open(building_loss_file,'w')
        handle.write('% yeah'+'\n')
        BID = ' '.join([str(x) for x in [1,2,3]])
        #print "BID", BID
        handle.write(BID+'\n')
        loss = [2000000.00, 1000000.00, 2500000.00]
        loss_row = ' '.join([str(x) for x in loss])
        handle.write(loss_row+'\n')
        handle.close()
        
        
        handle, file_out = tempfile.mkstemp(
            '.csv','test_post_processing_')
        os.close(handle)
        
        calc_loss_deagg_suburb(bval_file, building_loss_file,
                               sitedb_file, file_out)
        results = loadtxt(file_out, dtype='string',
                 delimiter=',', skiprows=3)
        #print "results", results
        actual = array([['HUGHES',],['MEREWETHER']])
        self.assert_(results[0,0] == 'HUGHES')
        self.assert_(results[1,0] == 'MEREWETHER')
        # loss
        self.assert_(float(results[0,1]) == 2.5)
        self.assert_(float(results[1,1]) == 3.)
        # b val
        self.assert_(float(results[0,2]) == 10.)
        self.assert_(float(results[1,2]) == 6.)
        # percentage
        self.assert_(float(results[0,3]) == 25.)
        self.assert_(float(results[1,3]) == 50.)
        
        
        # Remove the files
        os.remove(sitedb_file)
        os.remove(building_loss_file)
        os.remove(bval_file)
        os.remove(file_out)

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
            'BID':[1,2,3],
            'LATITUDE':[-32.9,-32.7,-33.],
            'LONGITUDE':[151.7,151.3,151.],
            'STRUCTURE_CLASSIFICATION':['W1BVTILE','S3','S2'],
            'STRUCTURE_CATEGORY':['BUILDING','BUILDING','BUILDING'],
            'HAZUS_USAGE':['RES1','COM8','COM4'],
            'SUBURB':['MEREWETHER','MEREWETHER','HUGHES'],
            'POSTCODE':[2291,2291,2289],
            'PRE1989':[0,1,1],
            'HAZUS_STRUCTURE_CLASSIFICATION':['W1','URML','URML'],
            'CONTENTS_COST_DENSITY':[300,10000,200],
            'BUILDING_COST_DENSITY':[600,1000,700],
            'FLOOR_AREA':[150,300,100],
            'SURVEY_FACTOR':[1,9.8,2],
            'FCB_USAGE':[111,451,121],
            'SITE_CLASS':['A','B','C']
            }    
    dict2csv(file_name, title_index_dic, attribute_dic)
    return file_name, attribute_dic
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_postprocessing,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
