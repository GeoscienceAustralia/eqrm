import os
import unittest
import numpy
from eqrm_code.estimator import *
from eqrm_code import file_store
from eqrm_code.parse_in_parameters import ParameterData, create_parameter_data
     
def create_base():
    """
    
    """
    sdp = ParameterData()
    
    # Operation Mode
    sdp.run_type = "hazard" 
    sdp.is_scenario = False
    sdp.site_tag = "ENB"
    sdp.scenario_max_width = 15
    sdp.return_periods = [100, 500, 2500]
    
    # Keep this as None to avoid changing the data dir location.
    sdp.input_dir = None #os.path.join('..','EQRMinputs')
                    
    sdp.output_dir = None #os.path.join('.','output')
    
    sdp.use_site_indexes = True #False # 21666 sites, hazard
    sdp.site_indexes = [1]
    sdp.event_control_tag = "" 
    sdp.zone_source_tag = ""
    sdp.fault_source_tag = ""
    sdp.file_array = False
    sdp.prob_number_of_events_in_zones =  [2] * 3
    sdp.prob_number_of_events_in_faults =  [2] * 4
    
    # Attenuation
    sdp.atten_collapse_Sa_of_atten_models = False #True
    sdp.atten_variability_method = 1
    sdp.atten_spawn_bins = 5
    sdp.atten_periods = [0.0, 0.3, 1.0]
    sdp.atten_threshold_distance = 400
    sdp.atten_override_RSA_shape = None
    sdp.atten_cutoff_max_spectral_displacement = False
    sdp.atten_pga_scaling_cutoff = 2
    sdp.atten_smooth_spectral_acceleration = None
    sdp.atten_log_sigma_eq_weight = 0
    
    # Amplification
    sdp.use_amplification = False #True
    sdp.amp_variability_method = None
    sdp.amp_min_factor = 0.6
    sdp.amp_max_factor = 10000
    
    # Save
    sdp.save_hazard_map = True
    sdp.save_motion = False
    
    return sdp


class Test_estimator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_estimator(self):
        
        events = 2
        atten_periods = 3
        return_periods = 5
        parallel_size = 7
        spawning = 11
        gmm_dimensions = 13
        rec_mod = 17
        save_total_financial_loss = True
        save_building_loss = True
        save_contents_loss = True
        save_hazard_map = True
        save_motion = True
        use_amplification = True
        loop_sites = 19
        item_size = 23

        results = estimate_mem(events, 
                               atten_periods, 
                               return_periods,
                               parallel_size,
                               spawning,
                               gmm_dimensions,
                               rec_mod,
                               save_total_financial_loss,
                               save_building_loss,
                               save_contents_loss,
                               save_hazard_map,
                               save_motion,
                               use_amplification,
                               loop_sites,
                               item_size)
        #print results
        # don't test this yet.


    def test_memory(self):
        mem_array = numpy.zeros([1000, 1000], dtype=float)
        self.assertEqual(mem_array.nbytes, 1000*1000*8)

    
    def test_estimate_mem_param_format(self):
        original_DATA_DIR = file_store.DATA_DIR
        sdp = create_base()
        #param = create_parameter_data(sdp)
        #results = estimate_mem_param_format(param)
        
        file_store.DATA_DIR = None

################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_estimator, 'test')
    runner = unittest.TextTestRunner() #verbosity=2) #verbosity=2
    runner.run(suite)
