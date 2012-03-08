import os
import sys
import tempfile
import shutil
import unittest

from scipy import array, allclose, asarray

from parse_in_parameters import *

try:
    from eqrm_code.ANUGA_utilities import log
    log_imported = True
except ImportError:
    log_imported = False

class Dummy:
    def __init__(self):
        pass
    
class Test_Parse_in_parameters(unittest.TestCase):
    
    def setUp(self):
        self.inputDir = tempfile.mkdtemp(prefix="inputDir")
        self.outputDir = tempfile.mkdtemp(prefix="outputDir")
        self.dataDir = tempfile.mkdtemp(prefix="dataDir")
        self.dataStoreDir = tempfile.mkdtemp(prefix="dataStoreDir")
        
    def tearDown(self):
        shutil.rmtree(self.inputDir)
        shutil.rmtree(self.outputDir)
        shutil.rmtree(self.dataDir)
        shutil.rmtree(self.dataStoreDir)

    def build_instance_to_eqrm_flags(self):
        set = Dummy()
        # Operation_Mode
        set.run_type = 'risk'
        set.is_scenario = True    # If False, probabilistic input used

        # General
        set.use_site_indexes = True
        set.site_tag= 'newc'
        set.site_db_tag = 'fish'
        set.site_indexes = [2255,11511]
        set.input_dir = self.inputDir
        set.output_dir = self.outputDir
        set.return_periods = [22,11]
        
        # Scenario input 
        set.scenario_azimuth = 20
        set.scenario_depth = 11.5
        set.scenario_latitude = 32.
        set.scenario_longitude = 151.
        set.scenario_magnitude = 5.
        set.scenario_dip= 35  
        set.scenario_number_of_events = 1
        set.scenario_width = 1.5
        set.scenario_length = 0.5

        # Probabilistic input
        set.max_width = 15
        set.prob_number_of_events_in_zones = [5000,1000]
        
        #  Attenuation   
        set.atten_models = ['my_attenuation_model','Gaull_1990_WA']
        set.atten_model_weights = [0.3,0.7]
        set.atten_collapse_Sa_of_atten_models = False 
        set.atten_variability_method = 2 
        set.atten_periods = [0,0.30303,1]
        set.atten_threshold_distance = 400
        set.atten_cutoff_max_spectral_displacement  = True
        set.atten_pga_scaling_cutoff = 4.3  # None or a value
        set.atten_override_RSA_shape = 'HAZUS_Sa'
        set.atten_smooth_spectral_acceleration = True
        set.atten_log_sigma_eq_weight = 1.0

        #  Amplification  
        set.use_amplification = True  
        set.amp_variability_method = 2 
        set.amp_min_factor = 0.6
        set.amp_max_factor = 2

        # Buildings
        set.buildings_usage_classification = 'HAZUS'   # ('HAZUS'|'FCB')
        set.buildings_set_damping_Be_to_5_percent = False
        
        # Bridges
        set.bridges_functional_percentages = [45, 34.5]

        # Building capacity curve
        set.csm_use_variability = True
        set.csm_variability_method = 3
        set.csm_standard_deviation = 0.3
        set.csm_damping_regimes = 0       # (0|1|2) See manual for this
        set.csm_damping_modify_Tav = True 
        set.csm_damping_use_smoothing = True
        set.csm_hysteretic_damping = 'curve'    # ('curve'|'trapezoidal'|None)
        set.csm_SDcr_tolerance_percentage = 2
        set.csm_damping_max_iterations = 7
        
        # Loss
        set.loss_min_pga = 0.05 # May be a crap value to use
        set.loss_regional_cost_index_multiplier = 3.2
        set.loss_aus_contents = 0   # (0|1)

        #  Save
        set.save_hazard_map = False
        set.save_total_financial_loss = True
        set.save_building_loss = True
        set.save_contents_loss = True
        set.save_motion = True
        set.save_prob_structural_damage = True
        
        # Data
        set.data_dir = self.dataDir
        set.event_set_handler = 'generate'
        set.event_set_name = 'test'
        set.data_array_storage = self.dataStoreDir
        
        # Log
        set.file_log_level = 'warning'
        set.console_log_level = 'critical'
        
        return set

        
    def check_eqrm_flags(self, TPT):
        # Check results
        self.failUnless(TPT.run_type == 'risk')
        self.failUnless(TPT.site_tag == 'newc')
        self.failUnless(TPT.site_db_tag == 'fish')
        self.failUnless(allclose(TPT.site_indexes, asarray([2255,11511])))
        
        self.failUnless(os.stat(os.path.abspath(TPT.input_dir)) ==
                        os.stat(os.path.abspath(self.inputDir)))
        self.failUnless(os.stat(os.path.abspath(TPT.output_dir)) ==
                        os.stat(os.path.abspath(self.outputDir)))   
        self.failUnless(allclose(TPT.return_periods, asarray([22,11])))        
        self.failUnless(TPT.grid_flag == 1)
        
        self.failUnless(TPT.use_site_indexes == 1)
        
        self.failUnless(TPT.is_scenario == True)
        self.failUnless(TPT.scenario_azimuth == 20)
        self.failUnless(TPT.scenario_depth == 11.5)
        self.failUnless(TPT.scenario_latitude == 32.)
        self.failUnless(TPT.scenario_longitude == 151.)
        self.failUnless(TPT.scenario_magnitude == 5.)
        self.failUnless(TPT.scenario_number_of_events == 1.)
        self.failUnless(TPT.scenario_width == 1.5)
        self.failUnless(TPT.scenario_length == 0.5)
        
        self.failUnless(TPT.max_width == 15)
        self.failUnless(allclose(TPT.prob_number_of_events_in_zones,
                                 asarray([5000,1000])))
        self.failUnless(allclose(TPT.atten_periods, asarray([0,0.30303,1])))
        self.failUnless(TPT.atten_threshold_distance == 400)
        self.failUnless(TPT.atten_pga_scaling_cutoff ==  4.3)
        self.failUnless(TPT.atten_override_RSA_shape == 'HAZUS_Sa')
        self.failUnless(TPT.atten_cutoff_max_spectral_displacement == True)
        self.failUnless(TPT.atten_variability_method == 2)
        self.failUnless(TPT.atten_smooth_spectral_acceleration == 1)
        self.failUnless(TPT.atten_log_sigma_eq_weight == 1.0)
        self.failUnless(TPT.use_amplification == 1)
        self.failUnless(TPT.amp_variability_method == 2)
        self.failUnless(TPT.amp_min_factor == 0.6)
        self.failUnless(TPT.amp_max_factor == 2)
        
        self.failUnless(TPT.buildings_usage_classification is 'HAZUS')
        self.failUnless(TPT.buildings_set_damping_Be_to_5_percent == 0)
        self.failUnless(TPT.buildpars_flag == 4)

        self.failUnless(allclose(TPT.bridges_functional_percentages, \
                                 asarray([45, 34.5])))
        
        self.failUnless(TPT.csm_use_variability is True)
        self.failUnless(TPT.csm_variability_method == 3)
        self.failUnless(TPT.csm_standard_deviation == .3)
        self.failUnless(TPT.csm_damping_regimes == 0)
        self.failUnless(TPT.csm_damping_modify_Tav == True)
        self.failUnless(TPT.csm_damping_use_smoothing == True)
        self.failUnless(TPT.csm_hysteretic_damping == 'curve')
        self.failUnless(TPT.csm_SDcr_tolerance_percentage == 2.)
        self.failUnless(TPT.csm_damping_max_iterations == 7)
        
        self.failUnless(TPT.loss_min_pga == 0.05)
        self.failUnless(TPT.loss_regional_cost_index_multiplier == 3.2)
        self.failUnless(TPT.loss_aus_contents == 0)

        self.failUnless(TPT.save_hazard_map == False)
        self.failUnless(TPT.save_motion == 1)
        self.failUnless(TPT.save_prob_structural_damage is True)
        self.failUnless(TPT.save_building_loss == True)
        self.failUnless(TPT.save_contents_loss == True)
        self.failUnless(TPT.save_total_financial_loss == True)
        self.failUnless(TPT.atten_models[0] == \
                        'my_attenuation_model')
        self.failUnless(TPT.atten_models[1] == 'Gaull_1990_WA')
        self.failUnless(TPT.atten_model_weights[0] == 0.3)
        self.failUnless(TPT.atten_model_weights[1] == 0.7)
        
        self.failUnless(os.stat(os.path.abspath(TPT.data_dir)) == 
                        os.stat(os.path.abspath(self.dataDir)))
        self.failUnless(TPT.event_set_handler == 'generate')
        self.failUnless(TPT.event_set_name == 'test')
        self.failUnless(os.stat(os.path.abspath(TPT.data_array_storage)) == 
                        os.stat(os.path.abspath(self.dataStoreDir)))
        
        self.failUnless(TPT.file_log_level == 'warning')
        self.failUnless(TPT.console_log_level == 'critical')


    def test_instance_to_eqrm_flags(self):
        set = self.build_instance_to_eqrm_flags()
        TPT = create_parameter_data(set)
        self.check_eqrm_flags(TPT)


    def test_instance_to_eqrm_flags_depreciated_atts(self):
        # Test depreciated_attributes
        set = self.build_instance_to_eqrm_flags()
        set.atten_use_variability = False
        set.amp_use_variability = False
        TPT = create_parameter_data(set)
        self.failUnless(TPT.atten_variability_method == None)
        self.failUnless(TPT.amp_variability_method == None)


    def test_eqrm_flags_to_control_file(self):

        if log_imported:
            # turn logging WARNINGS off
            # This is to stop warning messages appearing when testing
            console_logging_level = log.console_logging_level
            log.console_logging_level = log.ERROR
        
        set = self.build_instance_to_eqrm_flags()
        eqrm_flags = create_parameter_data(set)

        file, file_name = tempfile.mkstemp('.py', 'test_parse_in_para_')
        os.close(file)

        # Write the eqrm_flags to a control file
        eqrm_flags_to_control_file(file_name, eqrm_flags)

        # Read the control file
        eqrm_flags = create_parameter_data(file_name)
        
        os.remove(file_name)
        os.remove(file_name[:-3]+ '.pyc')
        
        self.check_eqrm_flags(eqrm_flags)

        if log_imported:
            # turn logging back to previous levels
            log.console_logging_level = console_logging_level
        
  
    def test_DictKeyAsAttributes(self):
        dic = DictKeyAsAttributes()
        leg = 12
        dic['leg'] = leg
        self.assert_(dic.leg == leg)
        del dic.leg
        self.assert_(not hasattr(dic, 'leg'))
        def del_again():
            del dic.leg
        self.failUnlessRaises(AttributeError, del_again)

        
    def test_add_default_values_raise(self):
        set = Dummy()
        self.failUnlessRaises(AttributeSyntaxError,
                              create_parameter_data, (set,))

   
    def small_set_data(self):
        set = Dummy()
        set.atten_override_RSA_shape = None
        set.atten_cutoff_max_spectral_displacement = False
        set.use_amplification = False
        set.site_tag = 'test_convert_py_2_THE'
        set.run_type = 'risk'
        
        # Other stuff - needed?
        set.csm_damping_regimes = 0
        set.csm_damping_modify_Tav = True
        set.csm_damping_use_smoothing = True

        # Other stuff - needed
        set.return_periods = [10,50,100]
        set.atten_periods = 0.0
        set.atten_models = ['Gaull_1990_WA']
        set.atten_model_weights = [1.]
        set.atten_collapse_Sa_of_atten_models = False
        set.save_motion = False
        set.is_scenario = True    # If False, probabilistic input used
        set.input_dir = '.'
        set.output_dir = '.'
        set.data_dir = '.'

        return set


    def test_convert_py_2_THE(self):
        set = self.small_set_data()
        para_new = create_parameter_data(set)
        self.failUnless(para_new.atten_override_RSA_shape == None)


    def test_fail_on_bad_att(self):
        
        set = Dummy()
        set.run_type = 'hazard'
        set.atten_override_RSA_shape = None
        set.atten_cutoff_max_spectral_displacement = False
        set.cooked_and_ready = False

        set.use_amplification = False
        set.site_tag = 'test_fail_on_bad_att'
        
        # Other stuff - needed
        set.return_periods = [10,50,100]
        set.atten_periods = [0,0.30303,1]
        set.atten_models = ['Gaull_1990_WA']
        set.atten_model_weights = [1.]
        set.save_motion = False
        set.is_scenario = True    # If False, probabilistic input used
        set.input_dir = '.'
        set.output_dir = '.'
        
        self.failUnlessRaises(AttributeSyntaxError,
                              create_parameter_data, (set,))
        

   
    def test_find_set_data_py_files(self):
        
        temp_dir = tempfile.mkdtemp(suffix='test_parse_in_parameters')

        # Add some files
        py_file = join(temp_dir, 'not_control.py')
        f = open(py_file,'w')
        f.write('"""\n')
        f.close()
        
        txt_file = join(temp_dir, 'not_control.txt')
        f = open(txt_file,'w')
        f.write('"""\n')
        f.close()
       
        set_data_files = find_set_data_py_files(temp_dir)        
        initial_files_num = len(set_data_files)
        
        new_set_data_file = join(temp_dir, 'remove_this_file.py')
        
        ## Create the new set_data like file
        set = self.build_instance_to_eqrm_flags()
        TPT = create_parameter_data(set)
        eqrm_flags_to_control_file(new_set_data_file, TPT)
        
        set_data_files = find_set_data_py_files(temp_dir)

        self.failUnlessEqual(len(set_data_files), initial_files_num + 1,
                        "find_set_data_py_files fail.")

        # Clean up
        os.remove(new_set_data_file)
        os.remove(py_file)
        os.remove(txt_file)
        os.rmdir(temp_dir)
      
   
    def test_update_control_file(self):
        set = self.small_set_data()
        para_new = create_parameter_data(set)
        file, file_name = tempfile.mkstemp('.py', __name__+'_')
        os.close(file)
        eqrm_flags_to_control_file(file_name, para_new)
        update_control_file(file_name)
        new_set = create_parameter_data(file_name)
        self.failUnlessEqual(set.csm_damping_regimes,
                             new_set.csm_damping_regimes)
        self.failUnlessEqual(set.csm_damping_use_smoothing,
                             new_set.csm_damping_use_smoothing)
        self.failUnlessEqual(set.csm_damping_regimes,
                             new_set.csm_damping_regimes)
                        
        os.remove(file_name)
        os.remove(file_name[:-3]+ '.pyc')
    
    def test_default_to_attr(self):
        set = self.build_instance_to_eqrm_flags()
        
        # these should default to output_dir
        del set.data_dir
        del set.data_array_storage
        
        eqrm_flags = create_parameter_data(set)
        
        expected_dir = os.path.abspath(eqrm_flags.output_dir)
        
        data_dir = os.path.abspath(eqrm_flags.data_dir)
        self.failUnlessEqual(data_dir, expected_dir)
        
        data_array_storage = os.path.abspath(eqrm_flags.data_array_storage)
        self.failUnlessEqual(data_array_storage, expected_dir)
    
    def test_directory_exists_check(self):
        set = self.build_instance_to_eqrm_flags()
        
        # These parameters are checked to see if they exist
        orig_output_dir = set.output_dir
        orig_data_array_storage = set.data_array_storage
        
        # Shouldn't exist (bad if does!)
        not_exists = join('does','not','exist')
        
        set.output_dir = not_exists
        self.failUnlessRaises(AttributeSyntaxError,
                              create_parameter_data, (set,))
        set.output_dir = orig_output_dir
        
        set.data_array_storage = not_exists
        self.failUnlessRaises(AttributeSyntaxError,
                              create_parameter_data, (set,))
        set.data_array_storage = orig_data_array_storage
        
        # Run again to see if no exception is raised
        create_parameter_data(set)
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Parse_in_parameters,'test')
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)
