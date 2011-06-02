import os
import sys
import unittest
import tempfile
import csv
from os import sep, path
   
from scipy import array, allclose

from eqrm_code.building_params_from_csv import building_params_from_csv
from eqrm_code.structures import *
from eqrm_code.util import dict2csv, determine_eqrm_path


class Test_Structures(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def not_test_how_it_works(self):
        handle, file_name = tempfile.mkstemp('.csv','test_struct_')
        os.close(handle)
        file_name, attribute_dic = write_test_file(file_name)

        eqrm_path = determine_eqrm_path()
        
        data_dir = os.path.join(eqrm_dir, 'resources', 'data')
        #print "data_dir", data_dir

        # Build lookup table for building parameters
        buildpars={
            0:'building_parameters_workshop_1',
            1:'building_parameters_workshop',
            2:'building_parameters_hazus',
            3:'building_parameters_workshop_2',
            4:'building_parameters_workshop_3'}

        # create links to required building parameters
        building_parameters = os.path.join(data_dir, buildpars[4])
        default_input_dir=os.path.join(eqrm_dir, 'resources','data')
        sites=Structures.from_csv(
            file_name,
            building_parameters,
            default_input_dir,
            eqrm_dir=eqrm_dir
            )
        os.remove(file_name)

    def test_building_parameters_values_hazus(self):

        # All these headings must be present
        attribute_dic={
            'BID':[1,2,3],
            'LATITUDE':[-32.9,-32.7,-32.5],
            'LONGITUDE':[151.7,151.3,151.3],
            'STRUCTURE_CLASSIFICATION':['W1BVTILE','C1MSOFT','URMLMETAL'],
            'STRUCTURE_CATEGORY':['BUILDING','BUILDING','BUILDING'],
            'HAZUS_USAGE':['RES1','COM5','COM5'],
            'SUBURB':['MEREWETHER','MEREWETHER','MEREWETHER'],
            'POSTCODE':[2291,2291,2291],
            'PRE1989':[0,1,0],
            'HAZUS_STRUCTURE_CLASSIFICATION':['W1','C1','URML'],
            'CONTENTS_COST_DENSITY':[300,10000,10],
            'BUILDING_COST_DENSITY':[600,1000,10],
            'FLOOR_AREA':[150,300,1],
            'SURVEY_FACTOR':[1,9.8,500],
            'FCB_USAGE':[111,491,491],
            'SITE_CLASS':['A','B','B']
            }
        sites, returned_attribute_dic = get_sites_from_dic(
            attribute_dic,
            buildings_usage_classification='HAZUS' # HAZUS usage 
            )

        assert returned_attribute_dic == attribute_dic
        
        # check that the __getitem__ works
        #attribute_dic['SITE_CLASS'] = ['AA','B']
        att_keys = ['FLOOR_AREA',] # everything but lat's and longs
        latitude = attribute_dic.pop("LATITUDE")
        longitude = attribute_dic.pop("LONGITUDE")
        att_keys = attribute_dic.keys()

        for key in att_keys:
            try:
                self.assert_(allclose(array(attribute_dic[key]),
                                      sites.attributes[key]))
            except (IndexError, TypeError, NotImplementedError):
                # this checks the string stuff
                self.assertEqual(attribute_dic[key],
                                      sites.attributes[key].tolist())
                
        self.assert_ (allclose(array(sites.latitude),latitude))
        self.assert_ (allclose(array(sites.longitude),longitude))
        
        #print "sites.building_parameters", sites.building_parameters
            
        # There's alot of info that is added to this dic structure,
        # such as non_residential_drift_threshold that seem to come
        # straight from building_params_from_csv

        # There are other bits of info that are calculated that depend
        # on reading data files and looking things up.  I Should hand
        # check the answer and make sure the results are correct.

        # Check the cost splits for the HAZUS usage classifications.
        #STRUCTURE_CLASSIFICATION':['W1BVTILE','C1MSOFT','URMLMETAL'],
        #'HAZUS_USAGE':['RES1','COM5','COM5'],
        
        results = array(sites.building_parameters["structure_ratio"])
        actual = array([.2344,.1379,.1379]) # these results from manual, p97
        # and using RcPerWrtBuildCHazususageEdwards.xls
        self.assert_ (allclose(results, actual, 0.001))

        results = array(sites.building_parameters["nsd_d_ratio"])
        actual = array([.5,.3448,.3448])
        self.assert_ (allclose(results, actual, 0.001))
        results = array(sites.building_parameters["nsd_a_ratio"])
        actual = array([.2656,.5172,.5172])
        self.assert_ (allclose(results, actual, 0.001))

        # only true if not use_refined_btypes?
        self.assertEqual(
            attribute_dic["STRUCTURE_CLASSIFICATION"],
            sites.building_parameters["structure_classification"].tolist())

    def test_building_parameters_values_FCB(self):
        attribute_dic={
            'BID':[1,2,3],
            'LATITUDE':[-32.9,-32.7,-32.5],
            'LONGITUDE':[151.7,151.3,151.3],
            'STRUCTURE_CLASSIFICATION':['W1BVTILE','C1MSOFT','URMLMETAL'],
            'STRUCTURE_CATEGORY':['BUILDING','BUILDING','BUILDING'],
            'HAZUS_USAGE':['RES1','COM5','COM5'],
            'SUBURB':['MEREWETHER','MEREWETHER','MEREWETHER'],
            'POSTCODE':[2291,2291,2291],
            'PRE1989':[0,1,0],
            'HAZUS_STRUCTURE_CLASSIFICATION':['W1','C1','URML'],
            'CONTENTS_COST_DENSITY':[300,10000,10],
            'BUILDING_COST_DENSITY':[600,1000,10],
            'FLOOR_AREA':[150,300,1],
            'SURVEY_FACTOR':[1,9.8,500],
            'FCB_USAGE':[111,491,491],
            'SITE_CLASS':['A','B','B']
            }
        sites, returned_attribute_dic = get_sites_from_dic(
            attribute_dic,
            buildings_usage_classification='FCB' # FCB usage 
            )

        assert returned_attribute_dic == attribute_dic
        
        #print "sites.building_parameters", sites.building_parameters
            
        # Check the cost splits for the FCB usage classifications.
        #STRUCTURE_CLASSIFICATION':['W1BVTILE','C1MSOFT','URMLMETAL']
        #    'FCB_USAGE':[111,491,491],
        
        results = array(sites.building_parameters["structure_ratio"])
        actual = array([.2344,.1532,.1532]) # these results from manual, p97
        # and using RcPerWrtBuildCHazususageEdwards.xls
        self.assert_ (allclose(results, actual, 0.001))

        results = array(sites.building_parameters["nsd_d_ratio"])
        actual = array([.5,.3423,.3423])
        self.assert_ (allclose(results, actual, 0.001))
        results = array(sites.building_parameters["nsd_a_ratio"])
        actual = array([.2656,.5045,.5045])
        self.assert_ (allclose(results, actual, 0.001))

        ci = 0.08
        total_costs = sites.cost_breakdown(ci=ci)
        for site in sites:
            structure_cost = site.attributes['BUILDING_COST_DENSITY']* \
                         site.attributes['FLOOR_AREA']* \
                         site.attributes['SURVEY_FACTOR']* \
                         ci
            
            contents_cost= site.attributes['CONTENTS_COST_DENSITY']* \
                         site.attributes['FLOOR_AREA']* \
                         site.attributes['SURVEY_FACTOR']* \
                         ci
            total_costs=(site.building_parameters["structure_ratio"]* \
                         structure_cost,
                     site.building_parameters["nsd_d_ratio"]*structure_cost,
                     site.building_parameters["nsd_a_ratio"]*structure_cost,
                     contents_cost)
            hand_calc = 1
            for results, actual in map(None, site.cost_breakdown(ci=ci),
                                       total_costs):
                self.assert_ (allclose(results, actual, 0.001))
                
            
        # test drift_threshold and CONTENTS_COST_DENSITY after doing
        # tests for building_params_from_csv


    def test_building_parameters_values_bridges(self):
        attribute_dic={
            'BID':[1],
            'LATITUDE':[-32.9],
            'LONGITUDE':[151.7],
            'STRUCTURE_CLASSIFICATION':['BRIDGE1'],
            'STRUCTURE_CATEGORY':['BRIDGE'],
            'HAZUS_USAGE':['RES1'],
            'SUBURB':['MEREWETHER'],
            'POSTCODE':[2291],
            'PRE1989':[0],
            'HAZUS_STRUCTURE_CLASSIFICATION':['BRIDGE1'],
            'CONTENTS_COST_DENSITY':[300],
            'BUILDING_COST_DENSITY':[600],
            'FLOOR_AREA':[150],
            'SURVEY_FACTOR':[1],
            'FCB_USAGE':[111],
            'SITE_CLASS':['A']
            }
        sites, returned_attribute_dic = get_sites_from_dic(
            attribute_dic,
            buildings_usage_classification='FCB' # FCB usage 
            )

        assert returned_attribute_dic == attribute_dic
        results = array(sites.building_parameters["design_strength"])
        actual = array([0.0])
        self.assert_ (allclose(results, actual, 0.001))
        #print "$$$$$$$$$$$$$$$$$$$$$$$$$$"
        #print "sites.building_parameters", sites.building_parameters
        # This att dic seems to be rather sparce.
        # eg no structural_damage_threshold
        # hazus_usage ['RES1' 'RES3' 'COM8' ..., 'GOV1' 'GOV1' 'GOV1']
        # fcb_usage [111 131 451 ..., 231 231 231]


        
    def test_build_replacement_ratios(self):
        #usage_values_per_struct = ['RES1',
        #                          'RES3', 'COM8', 'GOV1', 'GOV1', 'GOV1']
        usage_values_per_struct = [111, 231, 231]

        rcp_actual = {'structural':[0.2344, 0.1918, 0.1918],
                      'nonstructural drift sensitive':[0.5,0.3288, 0.3288],
                      'nonstructural acceleration sensitive':[0.2656,
                                                              0.4795,
                                                              0.4795
                                                              ]}
        buildings_usage_classification = 'FCB'
        rcp = build_replacement_ratios(usage_values_per_struct,
                                       buildings_usage_classification)
        components = ['structural', 'nonstructural drift sensitive',
        'nonstructural acceleration sensitive']
        for comp in components:
            self.assert_ (allclose(rcp[comp], rcp_actual[comp], 0.001))
            
        usage_values_per_struct = ['RES1', 'COM4', 'COM4']

        rcp_actual = {'structural':[0.2344, 0.1918, 0.1918],
                      'nonstructural drift sensitive':[0.5,0.3288, 0.3288],
                      'nonstructural acceleration sensitive':[0.2656,
                                                              0.4795,
                                                              0.4795
                                                              ]}
        buildings_usage_classification = 'HAZUS'
        rcp = build_replacement_ratios(usage_values_per_struct,
                                       buildings_usage_classification)
        components = ['structural', 'nonstructural drift sensitive',
        'nonstructural acceleration sensitive']
        for comp in components:
            self.assert_ (allclose(rcp[comp], rcp_actual[comp], 0.001))
        
"""
sites.building_parameters {


'residential_drift_threshold':
       array([[  11.09472,22.18944,   55.4736 ,   83.2104 ],
       [  33.528  ,   67.056  ,  167.64   ,  251.46   ],
       [  13.716  ,   27.432  ,   68.58   ,  102.87   ]]),

'structure_class': array(['BUILDING', 'BUILDING', 'BUILDING'],dtype='|S8'),

'height': array([  3962.4,  15240. ,   4572. ]),

'nsd_a_ratio': array([ 0.265625 ,  0.5045045,  0.5045045]),

'ultimate_to_yield': array([ 2. ,  1.25,  2.  ]),

  'design_strength': array([ 0.063,  0.1  ,  0.2  ]),

'non_residential_drift_threshold':
    array([[   2.77368,   22.18944,   41.6052 ,   69.342],
       [   8.382  ,   67.056  ,  125.73   ,  209.55   ],
       [   3.429  ,   27.432  ,   51.435  ,   85.725  ]]),

'damping_Be': array([ 0.08,  0.07,  0.05]),
 
 'nsd_d_ratio': array([ 0.5       ,  0.34234234,  0.34234234]),

'acceleration_threshold': array([[ 0.2,  0.4,  0.8,  1.6],
       [ 0.2,  0.4,  0.8,  1.6],
       [ 0.2,  0.4,  0.8,  1.6]]),

'fraction_in_first_mode': array([ 0.9 ,  1.,  0.75]),

'structure_ratio': array([ 0.234375  ,  0.15315315,  0.15315315]),

'structural_damage_threshold':
       array([[   9.153144,   17.474184,   41.6052  ,   85.98408 ],
       [  41.91    ,   58.674   ,   83.82    ,  251.46    ],
       [   1.7145  ,    2.7432  ,    4.1148  ,    6.858   ]]),
       
'natural_elastic_period': array([ 0.32,  0.85,  0.13]),

'damping_s': array([ 0.001,  0.105,  0.001]),

'drift_threshold': array([[  11.09472,   22.18944,   55.4736 ,   83.2104 ],
       [   8.382  ,   67.056  ,  125.73   ,  209.55   ],
       [   3.429  ,   27.432  ,   51.435  ,   85.725  ]]),

'yield_to_design': array([ 1.75,  1.5 ,  1.5 ]),

'structure_classification': array(['W1BVTILE', 'C1MSOFT', 'URMLMETAL'],

'height_to_displacement': array([ 0.7 ,  0.55,  0.75]),

'ductility': array([ 7.,  2.,  2.]),

'damping_l': array([ 0.001,  0.08 ,  0.001]),

'damping_m': array([ 0.001,  0.08 ,  0.001])}
"""
        
def get_sites_from_dic(attribute_dic=None,
                       buildings_usage_classification='HAZUS'  ):
        handle, file_name = tempfile.mkstemp('.csv','test_struct_')
        os.close(handle)
        file_name, attribute_dic = write_test_file(file_name,attribute_dic)

        eqrm_dir = determine_eqrm_path()
        
        data_dir = os.path.join(eqrm_dir, 'resources', 'data')
        #print "data_dir", data_dir

        # Build lookup table for building parameters
        buildpars={
            0:'building_parameters_workshop_1',
            1:'building_parameters_workshop',
            2:'building_parameters_hazus',
            3:'building_parameters_workshop_2',
            4:'building_parameters_workshop_3'}

        # create links to required building parameters
        building_parameters = os.path.join(data_dir, buildpars[4])
        
        default_input_dir=os.path.join(eqrm_dir, 'resources',
                                       'data')
        sites=Structures.from_csv(
            file_name,
            building_parameters,
            default_input_dir,
            eqrm_dir=eqrm_dir,
             buildings_usage_classification=buildings_usage_classification
            )
        os.remove(file_name)
        return sites, attribute_dic
        
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
    #suite = unittest.makeSuite(Test_Structures,'test_building_parameters_values_bridges')
    runner = unittest.TextTestRunner()
    runner.run(suite)
