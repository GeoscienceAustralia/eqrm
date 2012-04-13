import os
import sys
import unittest
import tempfile
from scipy import array, asarray, zeros, save, allclose, array_equal, ones
import shutil

from eqrm_code.csv_interface import csv_to_arrays
from eqrm_code.util import dict2csv, string_array_equal
from eqrm_code.event_set import Event_Set, Event_Activity
from eqrm_code.source_model import Source_Model
from eqrm_code.sites import Sites
from eqrm_code.parse_in_parameters import eqrm_flags_to_control_file

from eqrm_code.postprocessing import *


class Test_postprocessing(unittest.TestCase):
    
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.dir)
    
    def create_analysis_objects(self):
        # Parameters
        rupture_centroid_lat = asarray([-30])
        rupture_centroid_lon = asarray([150])
        length = asarray([1.0])
        azimuth = asarray([2.0])
        width = asarray([3.0])
        dip = asarray([4.0])
        depth = asarray([5.0])
        Mw = asarray([6.0])
        atten_models = asarray(['Allen', 
                                'Toro_1997_midcontinent', 
                                'Sadigh_97', 
                                'Youngs_97_interface', 
                                'Youngs_97_intraslab'])
        atten_model_weights = asarray([0.2, 0.2, 0.2, 0.2, 0.2])
        atten_periods = asarray([0, 1.0, 2.0])
        sites_lat = asarray([-31])
        sites_lon = asarray([150])
        
        # Event Set
        event_set = Event_Set.create(rupture_centroid_lat=rupture_centroid_lat,
                                     rupture_centroid_lon=rupture_centroid_lon,
                                     azimuth=azimuth,
                                     dip=dip,
                                     Mw=Mw,
                                     depth=depth,
                                     area=length*width,
                                     width=width, 
                                     length=length)
        
        # Event Activity
        event_activity = Event_Activity(len(event_set))
        event_activity.set_scenario_event_activity()
        
        # Source Model
        source_model = Source_Model.create_scenario_source_model(len(event_set))
        source_model.set_attenuation(atten_models, atten_model_weights)
        source_model.set_ground_motion_calcs(atten_periods)
        event_set.scenario_setup()
        event_activity.ground_motion_model_logic_split(source_model, True)
        
        # Sites
        sites = Sites(sites_lat, sites_lon)
        
        # SA
        # Set up synthetic SA figures
        # Dimensions -  spawn, gmm, rm, sites, events, period
        motion = zeros((1, 
                        len(atten_models), 
                        1, 
                        len(sites), 
                        len(event_set),
                        len(atten_periods)), dtype=float)
        # Allen
        motion[:,0,:,:,:,0] = 0 # period 0
        motion[:,0,:,:,:,1] = 1 # period 1.0
        motion[:,0,:,:,:,2] = 2 # period 2.0
        # Toro_1997_midcontinent
        motion[:,1,:,:,:,0] = 3 # period 0
        motion[:,1,:,:,:,1] = 4 # period 1.0
        motion[:,1,:,:,:,2] = 5 # period 2.0
        # Sadigh_97
        motion[:,2,:,:,:,0] = 6 # period 0
        motion[:,2,:,:,:,1] = 7 # period 1.0
        motion[:,2,:,:,:,2] = 8 # period 2.0
        # Youngs_97_interface
        motion[:,3,:,:,:,0] = 9  # period 0
        motion[:,3,:,:,:,1] = 10 # period 1.0
        motion[:,3,:,:,:,2] = 11 # period 2.0
        # Young_97_intraslab
        motion[:,4,:,:,:,0] = 12 # period 0
        motion[:,4,:,:,:,1] = 13 # period 1.0
        motion[:,4,:,:,:,2] = 14 # period 2.0
        
        # A minimal set of eqrm_flags so create_parameter_data passes
        # We only care about atten_models -> everything else are dummy values
        eqrm_flags = {}
        eqrm_flags['run_type'] = 'hazard'
        eqrm_flags['is_scenario'] = True
        eqrm_flags['output_dir'] = self.dir
        eqrm_flags['input_dir'] = self.dir
        eqrm_flags['site_tag'] = 'different_to_function'
        eqrm_flags['return_periods'] = [0.0]
        eqrm_flags['use_amplification'] = False
        eqrm_flags['zone_source_tag'] = 'not_used'
        eqrm_flags['atten_periods'] = atten_periods
        eqrm_flags['atten_models'] = atten_models
        
        return (event_set, 
                event_activity, 
                source_model, 
                sites, 
                motion, 
                eqrm_flags)
    
    def test_events_shaking_a_site(self):
        # Parameters
        output_dir = self.dir
        site_tag = 'ernabella'
        site_lat = -31.5
        site_lon = 150.5
        period = 1.0
        is_bedrock = True
        
        # 1. Get objects
        (event_set,
         event_activity,
         source_model,
         sites,
         motion,
         eqrm_flags) = self.create_analysis_objects()
         
        # 2. Save test objects to file
        event_set.save(os.path.join(output_dir, '%s_event_set' % site_tag))
        event_activity.save(os.path.join(output_dir, '%s_event_set' % site_tag))
        source_model.save(os.path.join(output_dir, '%s_event_set' % site_tag))
        sites.save(os.path.join(output_dir, '%s_sites' % site_tag))
        # Motion is an numpy.ndarray so save manually
        os.mkdir(os.path.join(output_dir, '%s_motion' % site_tag))
        save(os.path.join(output_dir, '%s_motion' % site_tag, 'bedrock_SA.npy'), 
             motion)
        # ... and eqrm_flags
        eqrm_flags_to_control_file(os.path.join(output_dir, 'eqrm_flags.py'),
                                   eqrm_flags)
        
        # 3. Run through events_shaking_a_site
        events_filename = events_shaking_a_site(output_dir,
                                                site_tag,
                                                site_lat,
                                                site_lon,
                                                period,
                                                is_bedrock)
        
        # 4. Read in generated CSV to a dict
        events_attributes = {'ground_motion': float,
                             'ground_motion_model': str,
                             'trace_start_lat': float,
                             'trace_start_lon': float,
                             'trace_end_lat': float,
                             'trace_end_lon': float,
                             'rupture_centroid_lat': float,
                             'rupture_centroid_lon': float,
                             'depth': float,
                             'azimuth': float,
                             'dip': float,
                             'Mw': float,
                             'length': float,
                             'width': float,
                             'activity': float,
                             'Rjb': float,
                             'Rrup': float,
                             'site_lat': float,
                             'site_lon': float}
        events_arrays = csv_to_arrays(events_filename, **events_attributes)
        
        # 5. Expected results
        expected_ground_motion = asarray([1, 4, 7, 10, 13]) # period == 1.0
        expected_ground_motion_model = asarray(['Allen', 
                                                'Toro_1997_midcontinent', 
                                                'Sadigh_97', 
                                                'Youngs_97_interface', 
                                                'Youngs_97_intraslab'])
        
        # Manually calculated
        expected_trace_start_lat = -29.98204065*ones(5)
        expected_trace_start_lon = 149.25728051*ones(5)
        expected_trace_end_lat = -29.97304727*ones(5)
        expected_trace_end_lon = 149.25764315*ones(5)
        
        # Input values
        expected_rupture_centroid_lat = -30*ones(5)
        expected_rupture_centroid_lon = 150*ones(5)
        expected_length = 1.0*ones(5)
        expected_azimuth = 2.0*ones(5)
        expected_width = 3.0*ones(5)
        expected_dip = 4.0*ones(5)
        expected_depth = 5.0*ones(5)
        expected_Mw = 6.0*ones(5)
        
        # Same as atten_model_weights
        expected_activity = 0.2*ones(5) 
        
        # Manually calculated
        expected_Rjb = 110.59526125*ones(5)
        expected_Rrup = 131.86940242*ones(5)
        
        # Different to input site lat/lon
        expected_site_lat = -31*ones(5) 
        expected_site_lon = 150*ones(5)
        
        # 6. Compare results
        self.assert_(allclose(expected_ground_motion, 
                              events_arrays['ground_motion']))
        
        self.assert_(string_array_equal(expected_ground_motion_model,
                                        events_arrays['ground_motion_model']))
        
        self.assert_(allclose(expected_trace_start_lat, 
                              events_arrays['trace_start_lat']))
        
        self.assert_(allclose(expected_trace_start_lon, 
                              events_arrays['trace_start_lon']))
        
        self.assert_(allclose(expected_trace_end_lat, 
                              events_arrays['trace_end_lat']))
        
        self.assert_(allclose(expected_trace_end_lon, 
                              events_arrays['trace_end_lon']))
        
        self.assert_(allclose(expected_rupture_centroid_lat, 
                              events_arrays['rupture_centroid_lat']))
        
        self.assert_(allclose(expected_rupture_centroid_lon, 
                              events_arrays['rupture_centroid_lon']))
        
        self.assert_(allclose(expected_length, 
                              events_arrays['length']))
        
        self.assert_(allclose(expected_azimuth, 
                              events_arrays['azimuth']))
        
        self.assert_(allclose(expected_width, 
                              events_arrays['width']))
        
        self.assert_(allclose(expected_dip, 
                              events_arrays['dip']))
        
        self.assert_(allclose(expected_depth, 
                              events_arrays['depth']))
        
        self.assert_(allclose(expected_Mw, 
                              events_arrays['Mw']))
        
        self.assert_(allclose(expected_Rjb, 
                              events_arrays['Rjb']))
        
        self.assert_(allclose(expected_Rrup, 
                              events_arrays['Rrup']))
        
        self.assert_(allclose(expected_activity, 
                              events_arrays['activity']))
        
        self.assert_(allclose(expected_site_lat, 
                              events_arrays['site_lat']))
        
        self.assert_(allclose(expected_site_lon, 
                              events_arrays['site_lon']))
        
        
    
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
