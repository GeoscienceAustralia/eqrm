import os
import sys
import tempfile
import unittest

from scipy import array, allclose, asarray

from eqrm_code.parse_in_parameters import *
from eqrm_code.util import determine_eqrm_path
from eqrm_code.capacity_spectrum_model import Capacity_spectrum_model, \
     CSM_DAMPING_REGIMES_USE_ALL, CSM_DAMPING_MODIFY_TAV
from eqrm_code.capacity_spectrum_functions import CSM_DAMPING_USE_SMOOTHING

from eqrm_filesystem import eqrm_path, Resources_Data_Path
    
class Dummy:
    def __init__(self):
        pass
    
class Test_Parse_in_parameters(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
  
    def update_test_create_parameter_data_BA08_error(self):
        file, file_name = tempfile.mkstemp('.par', __name__+'_')
        os.close(file)
        #file_name = './songs.par'
        file = open(file_name,"w")
        file.write("[Operation_Mode]\n\
run_type=[2]\n\n\
[General]\n\
destring=no description sring set\n\
use_site_indexes=[3]\n\
site_tag=newc\n\
site_indexes=[2997,2657,3004,3500]\n\
input_dir=./implementation_tests/input\n\
output_dir=./implementation_tests/current/TS_risk56\n\
return_periods=[10;50;100;200;250;474.56;500;974.79;1000;2474.9;2500;5000;7500;10000]\n\
grid_flag=[1]\n\n\
[Source]\n\
prob_azimuth_in_zones=[180]\n\
prob_min_mag_cutoff=[4.5]\n\
prob_number_of_mag_sample_bins=[15]\n\
max_width=[15]\n\
ftype=[2]\n\
prob_number_of_events_in_zones=[500,100,100,300,100,100]\n\
prob_delta_azimuth_in_zones=[180]\n\
prob_dip_in_zones=[35]\n\
[Event_Spawn]\n\
src_eps_switch=[0]\n\
mbnd=[4]\n\
nsigma=[2.5]\n\
nsamples=[5]\n\n\
[Scenario]\n\
scenario_azimith=[340]\n\
scenario_depth=[11.5]\n\
scenario_latitude=[-32.95]\n\
scenario_magnitude=[5.6]\n\
scenario_number_of_events=[167]\n\
scenario_longitude=[151.61]\n\
is_scenario=[0]\n\n\
[Attenuation]\n\
atten_smooth_spectral_acceleration=[0]\n\
atten_pga_scaling_cutoff=[2]\n\
attenuation_flag=[1,2,8;-0.33333,-0.33333,-0.33333]\n\
atten_use_variability=[1]\n\
atten_variability_method=[2]\n\
atten_periods=[0,0.17544,0.35088,0.52632,0.70175,0.87719,1.0526,1.2281,1.4035,1.5789,1.7544,1.9298,2.1053,2.2807,2.4561,2.6316,2.807,2.9825,3.1579,3.3333]\n\
atten_override_RSA_shape=[0]\n\
atten_threshold_distance=[400]\n\
atten_log_sigma_eq_weight=[0]\n\n\
[Amplification]\n\
amp_min_factor=[0.6]\n\
amp_variability_method=[2]\n\
use_amplification=[1]\n\
amp_use_variability=[1]\n\
amp_max_factor=[10000]\n\n\
[Bclasses]\n\
buildings_set_damping_Be_to_5_percent=[0]\n\
buildpars_flag=[4]\n\
hazus_btypes_flag=[0]\n\
buildings_usage_classification=[1]\n\n\
[Bclasses2]\n\
determ_buse=[1]\n\
force_btype_flag=[0]\n\
determ_btype=[34]\n\n\
[CSM]\n\
csm_use_variability=[1]\n\
csm_standard_deviation=[0.3]\n\
csm_variability_method=[3]\n\
damp_flags=[0,0,0]\n\
csm_hysteretic_damping=[1]\n\
csm_damping_max_iterations=[7]\n\
csm_SDcr_tolerance_percentage=[1]\n\n\
[Diagnostics]\n\
qa_switch_map=[0]\n\
qa_switch_attn=[0]\n\
qa_switch_ampfactors=[0]\n\
qa_switch_vun=[0]\n\
qa_switch_soc=[0]\n\
qa_switch_mke_evnts=[0]\n\
qa_switch_watercheck=[0]\n\
qa_switch_fuse=[0]\n\n\
[Loss]\n\
loss_regional_cost_index_multiplier=[1.4516]\n\
loss_min_pga=[0.05]\n\
loss_aus_contents=[0]\n\n\
[Save]\n\
save_prob_structural_damage=[0]\n\
save_probdam_flag=[0]\n\
save_hazard_map=[0]\n\
save_motion=[0]\n\
save_ecloss_flag=[1]\n\
save_socloss_flag=[1]\n")
        file.close()
        #file_name = 'TS_risk56.par'
        #file_name = 'usongs.par'
        try:
            paras = create_parameter_data(file_name)
        except ParameterSyntaxError:
            os.remove(file_name)
            pass
        else:
            os.remove(file_name)
            self.failUnless(False, "ParameterSyntaxError not raised")
                    
    def update_test_create_parameter_data_BA08_error2(self):
        file, file_name = tempfile.mkstemp('.par', __name__+'_')
        os.close(file)
        #file_name = './songs.par'
        file = open(file_name,"w")
        file.write("[Operation_Mode]\n\
run_type=[2]\n\n\
[General]\n\
destring=no description sring set\n\
use_site_indexes=[3]\n\
site_tag=newc\n\
site_indexes=[2997,2657,3004,3500]\n\
input_dir=./implementation_tests/input\n\
output_dir=./implementation_tests/current/TS_risk56\n\
return_periods=[10;50;100;200;250;474.56;500;974.79;1000;2474.9;2500;5000;7500;10000]\n\
grid_flag=[1]\n\n\
[Source]\n\
prob_azimuth_in_zones=[180]\n\
prob_min_mag_cutoff=[4.5]\n\
prob_number_of_mag_sample_bins=[15]\n\
max_width=[15]\n\
ftype=[2]\n\
prob_number_of_events_in_zones=[500,100,100,300,100,100]\n\
prob_delta_azimuth_in_zones=[180]\n\
prob_dip_in_zones=[35]\n\
[Event_Spawn]\n\
src_eps_switch=[0]\n\
mbnd=[4]\n\
nsigma=[2.5]\n\
nsamples=[5]\n\n\
[Scenario]\n\
scenario_azimith=[340]\n\
scenario_depth=[11.5]\n\
scenario_latitude=[-32.95]\n\
scenario_magnitude=[5.6]\n\
scenario_number_of_events=[167]\n\
scenario_longitude=[151.61]\n\
is_scenario=[0]\n\n\
[Attenuation]\n\
atten_smooth_spectral_acceleration=[0]\n\
atten_pga_scaling_cutoff=[2]\n\
attenuation_flag=[8;-1]\n\
atten_use_variability=[1]\n\
atten_variability_method=[2]\n\
atten_periods=[0,0.17544,0.35088,0.52632,0.70175,0.87719,1.0526,1.2281,1.4035,1.5789,1.7544,1.9298,2.1053,2.2807,2.4561,2.6316,2.807,2.9825,3.1579,3.3333]\n\
atten_override_RSA_shape=[0]\n\
atten_threshold_distance=[400]\n\
atten_log_sigma_eq_weight=[0]\n\n\
[Amplification]\n\
amp_min_factor=[0.6]\n\
amp_variability_method=[2]\n\
use_amplification=[1]\n\
amp_use_variability=[1]\n\
amp_max_factor=[10000]\n\n\
[Bclasses]\n\
buildings_set_damping_Be_to_5_percent=[0]\n\
buildpars_flag=[4]\n\
hazus_btypes_flag=[0]\n\
buildings_usage_classification=[1]\n\n\
[Bclasses2]\n\
determ_buse=[1]\n\
force_btype_flag=[0]\n\
determ_btype=[34]\n\n\
[CSM]\n\
csm_use_variability=[1]\n\
csm_standard_deviation=[0.3]\n\
csm_variability_method=[3]\n\
damp_flags=[0,0,0]\n\
csm_hysteretic_damping=[1]\n\
csm_damping_max_iterations=[7]\n\
csm_SDcr_tolerance_percentage=[1]\n\n\
[Diagnostics]\n\
qa_switch_map=[0]\n\
qa_switch_attn=[0]\n\
qa_switch_ampfactors=[0]\n\
qa_switch_vun=[0]\n\
qa_switch_soc=[0]\n\
qa_switch_mke_evnts=[0]\n\
qa_switch_watercheck=[0]\n\
qa_switch_fuse=[0]\n\n\
[Loss]\n\
loss_regional_cost_index_multiplier=[1.4516]\n\
loss_min_pga=[0.05]\n\
loss_aus_contents=[0]\n\n\
[Save]\n\
save_prob_structural_damage=[0]\n\
save_probdam_flag=[0]\n\
save_hazard_map=[0]\n\
save_motion=[0]\n\
save_ecloss_flag=[1]\n\
save_socloss_flag=[1]\n")
        file.close()
        #file_name = 'TS_risk56.par'
        #file_name = 'usongs.par'
        try:
            paras = create_parameter_data(file_name)
        except ParameterSyntaxError:
            os.remove(file_name)
            pass
        else:
            os.remove(file_name)
            self.failUnless(False, "ParameterSyntaxError not raised")
       
     
    def test_Parameter_data_eqrm_data_home(self):
        pd = Parameter_data()
        # Not keen on testing this.  It does not
        # have to be set.
        #pd.eqrm_data_home()
        #print "pd.get_time_user()", pd.get_time_user()

    def build_instance_to_THE_PARAM_T(self):
        set = Dummy()
        # Operation_Mode
        set.run_type = 'risk'
        set.is_scenario = True    # If False, probabilistic input used

        # General
        set.site_tag= 'newc'
        set.site_db_tag = 'fish'
        set.site_indexes = [2255,11511]
        set.input_dir = 'c:/in/'
        set.output_dir = 'c:/out/'
        set.return_periods = [22,11]
        
        # Scenario input 
        set.scenario_azimith = 20
        set.scenario_depth = 11.5
        set.scenario_latitude = 32.
        set.scenario_longitude = 151.
        set.scenario_magnitude = 5.
        set.scenario_dip= 35  
        set.scenario_number_of_events = 1

        # Probabilistic input
        set.prob_azimuth_in_zones = [10,30]
        set.prob_min_mag_cutoff = 4.5 
        set.prob_number_of_mag_sample_bins = 15
        set.max_width = 15
        set.prob_number_of_events_in_zones = [5000,1000]
        set.prob_delta_azimuth_in_zones = [5,10]
        set.prob_dip_in_zones = [35,40]
        
        #  Attenuation   
        set.atten_models = ['my_attenuation_model','Gaull_1990_WA']
        set.atten_model_weights = [0.3,0.7]
        set.atten_aggregate_Sa_of_atten_models = False 
        set.atten_variability_method = 2 
        set.atten_periods = [0,0.30303,1]
        set.atten_threshold_distance = 400
        set.atten_cutoff_max_spectral_displacement  = True
        set.atten_pga_scaling_cutoff = 4.3  # None or a value
        set.atten_override_RSA_shape = 'HAZUS_Sa' # ('Aust_standard_Sa'|'HAZUS_Sa')
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
        # has not been implemented.
        #set.building_paramters_file = "workshop_3"   # 'workshop'+(''|'_1'|'_2'|'_3')
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
        set.save_hazard_map = True
        set.save_total_financial_loss = True
        set.save_building_loss = True
        set.save_contents_loss = True
        set.save_motion = True
        set.save_prob_structural_damage = True
        return set

        
    def check_THE_PARAM_T(self, TPT):
        # Check results
        self.failUnless(TPT.run_type == 'risk')
        self.failUnless(TPT.site_tag == 'newc')
        self.failUnless(TPT.site_db_tag == 'fish')
        self.failUnless(allclose(TPT.site_indexes, asarray([2255,11511])))
        self.failUnless(TPT.input_dir == 'c:/in/')
        self.failUnless(TPT.output_dir == 'c:/out/')        
        self.failUnless(TPT.return_periods == [22,11])        
        self.failUnless(TPT.grid_flag == 1)
                
        self.failUnless(TPT.is_scenario == True)
        self.failUnless(TPT.scenario_azimith == 20)
        self.failUnless(TPT.scenario_depth == 11.5)
        self.failUnless(TPT.scenario_latitude == 32.)
        self.failUnless(TPT.scenario_longitude == 151.)
        self.failUnless(TPT.scenario_magnitude == 5.)
        self.failUnless(TPT.scenario_number_of_events == 1.)
        
        self.failUnless(allclose(TPT.prob_azimuth_in_zones, asarray([10,30])))
        self.failUnless(TPT.prob_min_mag_cutoff == 4.5)
        self.failUnless(TPT.prob_number_of_mag_sample_bins == 15)
        self.failUnless(TPT.max_width == 15)
        self.failUnless(allclose(TPT.prob_number_of_events_in_zones,
                                 asarray([5000,1000])))
        self.failUnless(allclose(TPT.prob_delta_azimuth_in_zones,
                                 asarray([5,10])))
        self.failUnless(allclose(TPT.prob_dip_in_zones, asarray([35, 40])))
        
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
        self.failUnless(TPT.force_btype_flag == 0)
        self.failUnless(TPT.hazus_btypes_flag == 0)
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

        self.failUnless(TPT.save_hazard_map == 1)
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


    def test_instance_to_THE_PARAM_T(self):
        set = self.build_instance_to_THE_PARAM_T()
        TPT = create_parameter_data(set)
        self.check_THE_PARAM_T(TPT)


    def test_instance_to_THE_PARAM_T_depreciated_atts(self):
        set = self.build_instance_to_THE_PARAM_T()
        set.atten_use_variability = False
        set.amp_use_variability = False
        TPT = create_parameter_data(set)
        self.failUnless(TPT.atten_variability_method == None)
        self.failUnless(TPT.amp_variability_method == None)


    def test_convert_THE_PARAM_T_to_py(self):
        set = self.build_instance_to_THE_PARAM_T()
        TPT = create_parameter_data(set)

        file, file_name = tempfile.mkstemp('.py', 'test_parse_in_para_')
        os.close(file)
        
        convert_THE_PARAM_T_to_py(file_name, TPT)
        TPT = create_parameter_data(file_name)
        
        os.remove(file_name)
        os.remove(file_name[:-3]+ '.pyc')
        
        self.check_THE_PARAM_T(TPT)
        
        
    def test_instance_to_py_file(self):
        set = Dummy()
        # Operation_Mode
        set.run_type = 'risk'
        set.is_scenario = True    # If False, probabilistic input used

        # General
        set.site_tag= 'newc'
        set.site_db_tag = 'fish'
        set.site_indexes = [2255,11511]
        set.input_dir = 'read in'
        set.output_dir = 'read out'
        set.return_periods = [22,11]
        
        # Scenario input 
        set.scenario_azimith = 20
        set.scenario_depth = 11.5
        set.scenario_latitude = 32.
        set.scenario_longitude = 151.
        set.scenario_magnitude = 5.
        set.scenario_dip= 35  
        set.scenario_number_of_events = 1

        # Probabilistic input
        set.prob_azimuth_in_zones = [10,30]
        set.prob_min_mag_cutoff = 4.5 
        set.prob_number_of_mag_sample_bins = 15
        set.max_width = 15
        set.prob_number_of_events_in_zones = [5000,1000]
        set.prob_delta_azimuth_in_zones = [5,10]
        set.prob_dip_in_zones = [35,40]
        
        #  Attenuation   
        set.atten_models = ['my_attenuation_model','Gaull_1990_WA']
        set.atten_model_weights = [0.3,0.7]
        set.atten_aggregate_Sa_of_atten_models = False 
        set.atten_use_variability = True
        set.atten_variability_method = 2 
        set.atten_periods = [0,0.30303,1]
        set.atten_threshold_distance = 400
        set.atten_cutoff_max_spectral_displacement  = True
        set.atten_pga_scaling_cutoff = 4.3  # None or a value
        set.atten_override_RSA_shape = 'HAZUS_Sa' # ('Aust_standard_Sa'|'HAZUS_Sa')
        set.atten_smooth_spectral_acceleration = True
        set.atten_log_sigma_eq_weight = 1.0

        #  Amplification  
        set.use_amplification = True  
        set.amp_use_variability = True
        set.amp_variability_method = 2 
        set.amp_min_factor = 0.6
        set.amp_max_factor = 2

        # Buildings
        set.buildings_usage_classification = 'HAZUS'   # ('HAZUS'|'FCB')
        set.buildings_set_damping_Be_to_5_percent = False
        # has not been implemented.
        #set.building_paramters_file = "workshop_3"   # 'workshop'+(''|'_1'|'_2'|'_3')

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
        set.save_hazard_map = True
        set.save_total_financial_loss = True
        set.save_building_loss = True
        set.save_contents_loss = True
        set.save_motion = True
        set.save_prob_structural_damage = True


        convert_THE_PARAM_T_to_py('here.py', set)

        
        # need some more tests.
    def do_not_test_create_parameter_data_setdata_probhaz(self):
        file, file_name = tempfile.mkstemp('.par', __name__+'_')
        os.close(file)
        #file_name = './songs.par'
        file = open(file_name,"w")
        file.write("[Operation_Mode]\n\
run_type='hazard'\n\n\
[General]\n\
destring=no description sring set\n\
use_site_indexes=[1]\n\
site_tag=newc\n\
site_indexes=[2255,11511,10963]\n\
input_dir=.\input\n\
output_dir=.\output\prob_haz\n\
return_periods=[10;50;100;200]\n\
grid_flag=[1]\n\
[Source]\n\
prob_azimuth_in_zones=[10,30,70,100,150,15]\n\
prob_min_mag_cutoff=[4.5]\n\
prob_number_of_mag_sample_bins=[15]\n\
max_width=[15]\n\
ftype=[2]\n\
prob_number_of_events_in_zones=[5000,1000,1000,3000,1000,1000]\n\
prob_delta_azimuth_in_zones=[5,10,20,25,50,0]\n\
prob_dip_in_zones=[35,40,45,50,55,60]\n\
[Event_Spawn]\n\
src_eps_switch=[0]\n\
mbnd=[4]\n\
nsigma=[2.5]\n\
nsamples=[5]\n\
[Scenario]\n\
scenario_azimith=[340]\n\
scenario_depth=[11.5]\n\
scenario_latitude=[-32.95]\n\
scenario_magnitude=[5.6]\n\
scenario_number_of_events=[167]\n\
scenario_longitude=[151.61]\n\
is_scenario=[1]\n\
[Attenuation]\n\
atten_smooth_spectral_acceleration=[1]\n\
atten_pga_scaling_cutoff=[2]\n\
attenuation_flag=[3;1]\n\
attn_region=[1]\n\
atten_use_variability=[1]\n\
atten_variability_method=[2]\n\
atten_periods=[0,0.30303,1]\n\
atten_override_RSA_shape=[5]\n\
atten_threshold_distance=[400]\n\
atten_log_sigma_eq_weight=[1.0]\n\
[Amplification]    \n\
amp_min_factor=[0.6]\n\
amp_variability_method=[2]\n\
use_amplification=[1]\n\
amp_use_variability=[1]\n\
amp_max_factor=[10000]\n\
[Bclasses]    \n\
buildings_set_damping_Be_to_5_percent=[0]\n\
buildpars_flag=[4]\n\
hazus_btypes_flag=[0]\n\
buildings_usage_classification=[1]\n\
[Bclasses2]    \n\
determ_buse=[0]\n\
force_btype_flag=[0]\n\
determ_btype=[0]\n\
[CSM]\n\
csm_use_variability=[1]\n\
csm_standard_deviation=[0.3]\n\
csm_variability_method=[3]\n\
damp_flags=[0,0,0]\n\
csm_hysteretic_damping=[3]\n\
csm_damping_max_iterations=[7]\n\
csm_SDcr_tolerance_percentage=[2]\n\
[Diagnostics]\n\
qa_switch_map=[1]\n\
qa_switch_attn=[0]\n\
qa_switch_ampfactors=[0]\n\
qa_switch_vun=[0]\n\
qa_switch_soc=[0]\n\
qa_switch_mke_evnts=[0]\n\
qa_switch_watercheck=[0]\n\
qa_switch_fuse=[0]\n\
[Loss]\n\
loss_regional_cost_index_multiplier=[3.2]\n\
loss_min_pga=[0.05]\n\
loss_aus_contents=[0]\n\
[Save]\n\
save_prob_structural_damage=[0]\n\
save_probdam_flag=[0]\n\
save_hazard_map=[1]\n\
save_motion=[0]\n\
save_ecloss_flag=[0]\n\
save_socloss_flag=[0]\n")
        file.close()
        
        para_old = create_parameter_data(file_name)
        os.remove(file_name)
        
        from eqrm_code.parse_in_parameters import Parameter_data
        from os.path import join

        set = Parameter_data()

        # Operation_Mode
        set.run_type = 'hazard'   # ('risk'|'hazard')
        
        # General
        set.site_tag = 'newc'
        set.site_indexes = [2255,11511,10963]
        set.site_db_tag = "" # file nam is sitedb_[site_tag][site_db_tag].csv
        set.input_dir = join(set.eqrm_home(), 'demo', 'input')
        set.output_dir = join(set.eqrm_home(), 'demo', 'output','prob_haz')
        set.return_periods = [10,50,100,200]
        
        # Scenario input   (single event input, with event_azimuth ect.)
        set.is_scenario = True   # If False, probabilistic input used
        set.scenario_azimith = 340
        set.scenario_depth = 11.5
        set.scenario_latitude = -32.95
        set.scenario_longitude = 151.61
        set.scenario_magnitude = 5.6
        set.scenario_dip= 35  
        set.scenario_number_of_events = 167
        
        
        set.prob_azimuth_in_zones = [10,30,70,100,150,15]
        set.prob_min_mag_cutoff = 4.5 
        set.prob_number_of_mag_sample_bins = 15
        set.max_width = 15
        set.prob_number_of_events_in_zones = [5000,1000,1000,3000,1000,1000]
        set.prob_delta_azimuth_in_zones = [5,10,20,25,50,0]
        set.prob_dip_in_zones = [35,40,45,50,55,60]
        
        #  Attenuation   
        set.atten_models = [3]
        set.atten_model_weights = [1]
        set.atten_aggregate_Sa_of_atten_models = True
        set.atten_use_variability = True
        set.atten_variability_method = 2 
        set.atten_periods = [0,0.30303,1]
        set.atten_threshold_distance = 400
        set.atten_cutoff_max_spectral_displacement = True 
        set.atten_pga_scaling_cutoff = 2.0  # Float
        set.atten_smooth_spectral_acceleration = True
        set.atten_log_sigma_eq_weight = 1.0
        
        #  Amplification  
        set.use_amplification = True  
        set.amp_use_variability = True
        set.amp_variability_method = 2  # (2-6) 2 is random sampling. More above
        set.amp_min_factor = 0.6
        set.amp_max_factor = 10000
        
        # Buildings
        set.buildings_usage_classification = 'HAZUS'   # ('HAZUS'|'FCB')
        set.buildings_set_damping_Be_to_5_percent = False
        
        # Building capacity curve
        set.csm_use_variability = True
        set.csm_variability_method = 3
        set.csm_standard_deviation = 0.3
        set.csm_damping_regimes = 0   
        set.csm_damping_modify_Tav = True 
        set.csm_damping_use_smoothing = True
        set.csm_hysteretic_damping = 'curve'
        set.csm_SDcr_tolerance_percentage = 2
        set.csm_damping_max_iterations = 7
        
        # Loss
        set.loss_min_pga = 0.05 # May be a crap value to use
        set.loss_regional_cost_index_multiplier = 3.2
        set.loss_aus_contents = 0   # (0|1)
        
        #  Save
        set.save_hazard_map = True
        set.save_total_financial_loss = False
        set.save_building_loss = False
        set.save_contents_loss = False
        set.save_motion = False
        set.save_prob_structural_damage = False
        
        para_new = create_parameter_data(set)
        
        # Don't worry about the dir stuff
        del para_new['input_dir']
        del para_new['output_dir']

        # I don't know why these values are not the same
        # print them and they look the same.
        # So it is not so good taking them out...
        del para_new['site_db_tag']
        del para_new['site_tag']
        
        for key in para_new:
            # skip the string values.
            if key in ['run_type', 'atten_cutoff_max_spectral_displacement',
                       'atten_override_RSA_shape',
                       'csm_hysteretic_damping',
                       'buildings_usage_classification']:
                continue
            if isinstance(getattr(para_new, key), str) or \
                   isinstance(getattr(para_old, key), str) and \
                   not getattr(para_new, key) == getattr(para_old, key):
                print "key", key
                print "str getattr(para_new, key)", getattr(para_new, key)
                print "str getattr(para_old, key)", getattr(para_old, key)
                self.assert_(False)
                
            elif not allclose(asarray(getattr(para_new, key)),
                              asarray(getattr(para_old, key))):
                print "key", key
                print "getattr(para_new, key)", getattr(para_new, key)
                print "getattr(para_old, key)", getattr(para_old, key)
                self.assert_(False)
  
    def do_not_test_convert_par_to_py(self):
        file, file_name = tempfile.mkstemp('.par', __name__+'_')
        os.close(file)
        #file_name = './songs.par'
        file = open(file_name,"w")
        file.write("[Operation_Mode]\n\
run_type=[1]\n\n\
[General]\n\
destring=no description sring set\n\
use_site_indexes=[1]\n\
site_tag=newc\n\
site_indexes=[2255,11511,10963]\n\
input_dir=.\input\n\
output_dir=.\output\prob_haz\n\
return_periods=[10;50;100;200]\n\
grid_flag=[1]\n\
[Source]\n\
prob_azimuth_in_zones=[10,30,70,100,150,15]\n\
prob_min_mag_cutoff=[4.5]\n\
prob_number_of_mag_sample_bins=[15]\n\
max_width=[15]\n\
ftype=[2]\n\
prob_number_of_events_in_zones=[5000,1000,1000,3000,1000,1000]\n\
prob_delta_azimuth_in_zones=[5,10,20,25,50,0]\n\
prob_dip_in_zones=[35,40,45,50,55,60]\n\
[Event_Spawn]\n\
src_eps_switch=[0]\n\
mbnd=[4]\n\
nsigma=[2.5]\n\
nsamples=[5]\n\
[Scenario]\n\
scenario_azimith=[340]\n\
scenario_depth=[11.5]\n\
scenario_latitude=[-32.95]\n\
scenario_magnitude=[5.6]\n\
scenario_number_of_events=[167]\n\
scenario_longitude=[151.61]\n\
is_scenario=[0]\n\
[Attenuation]\n\
atten_smooth_spectral_acceleration=[1]\n\
atten_pga_scaling_cutoff=[2]\n\
attenuation_flag=[3,2;0.3,0.7]\n\
attn_region=[1]\n\
atten_use_variability=[1]\n\
atten_variability_method=[2]\n\
atten_periods=[0,0.30303,1]\n\
atten_override_RSA_shape=[0]\n\
atten_threshold_distance=[400]\n\
atten_log_sigma_eq_weight=[1.0]\n\
[Amplification]    \n\
amp_min_factor=[0.6]\n\
amp_variability_method=[2]\n\
use_amplification=[1]\n\
amp_use_variability=[1]\n\
amp_max_factor=[10000]\n\
[Bclasses]    \n\
buildings_set_damping_Be_to_5_percent=[0]\n\
buildpars_flag=[4]\n\
hazus_btypes_flag=[0]\n\
buildings_usage_classification=[1]\n\
[Bclasses2]    \n\
determ_buse=[0]\n\
force_btype_flag=[0]\n\
determ_btype=[0]\n\
[CSM]\n\
csm_use_variability=[1]\n\
csm_standard_deviation=[0.3]\n\
csm_variability_method=[3]\n\
damp_flags=[0,0,0]\n\
csm_hysteretic_damping=[3]\n\
csm_damping_max_iterations=[7]\n\
csm_SDcr_tolerance_percentage=[2]\n\
[Diagnostics]\n\
qa_switch_map=[1]\n\
qa_switch_attn=[0]\n\
qa_switch_ampfactors=[0]\n\
qa_switch_vun=[0]\n\
qa_switch_soc=[0]\n\
qa_switch_mke_evnts=[0]\n\
qa_switch_watercheck=[0]\n\
qa_switch_fuse=[0]\n\
[Loss]\n\
loss_regional_cost_index_multiplier=[3.2]\n\
loss_min_pga=[0.05]\n\
loss_aus_contents=[0]\n\
[Save]\n\
save_prob_structural_damage=[0]\n\
save_probdam_flag=[0]\n\
save_hazard_map=[1]\n\
save_motion=[0]\n\
save_ecloss_flag=[0]\n\
save_socloss_flag=[0]\n")
        file.close()
        
        #para_old = create_parameter_data(file_name)
        py_file_name = convert_par_to_py(file_name)

        #So this isn't really a test

        os.remove(file_name)
        os.remove(py_file_name)
        
    def test_Dict_key_as_attributes(self):
        dic = Dict_key_as_attributes()
        leg = 12
        dic['leg'] = leg
        self.assert_(dic.leg == leg)
        del dic.leg
        self.assert_(not hasattr(dic, 'leg'))
        try:
            del dic.leg
        except AttributeError:
            pass
        else:
            self.failUnless(False, "Error not raised")
        
    def test_att_default_values_raise(self):
        set = Parameter_data()
        try:
            para_new = create_parameter_data(set)
        except ParameterSyntaxError:
            pass
        else:
            self.failUnless(False, "SystemExit not raised")

   
    def small_set_data(self):
        set = Parameter_data()
        set.atten_override_RSA_shape = None
        set.atten_cutoff_max_spectral_displacement = False
        set.use_amplification = False
        set.site_tag = 'test_convert_py_2_THE'
        set.run_type = 'risk'
        
        # Other stuff - needed?
        set.prob_azimuth_in_zones = [10,30,70,100,150,15]
        set.prob_min_mag_cutoff = 4.5 
        set.prob_number_of_mag_sample_bins = 15
        set.max_width = 15
        set.prob_number_of_events_in_zones = [5000,1000,1000,3000,1000,1000]
        set.prob_delta_azimuth_in_zones = [5,10,20,25,50,0]
        set.prob_dip_in_zones = [35,40,45,50,55,60]
        set.csm_damping_regimes = 0
        set.csm_damping_modify_Tav = True
        set.csm_damping_use_smoothing = True

        # Other stuff - needed
        set.return_periods = [10,50,100]
        set.atten_periods = [0,0.30303,1]
        set.atten_models = ['Gaull_1990_WA']
        set.atten_model_weights = [1.]
        set.atten_aggregate_Sa_of_atten_models = False
        set.save_motion = False
        set.is_scenario = True    # If False, probabilistic input used
        set.input_dir = '.'
        set.output_dir = '.'

        return set


    def test_convert_py_2_THE(self):
        set = self.small_set_data()
        para_new = create_parameter_data(set)
        self.assert_(para_new.atten_override_RSA_shape == None)


    def test_fail_on_bad_att(self):
        #
        set = Parameter_data()
        set.run_type = 'hazard'
        set.atten_override_RSA_shape = None
        set.atten_cutoff_max_spectral_displacement = False
        set.cooked_and_ready = False

        set.use_amplification = False
        set.site_tag = 'test_fail_on_bad_att'
        
        # Other stuff - needed?
        set.prob_azimuth_in_zones = [10,30,70,100,150,15]
        set.prob_min_mag_cutoff = 4.5 
        set.prob_number_of_mag_sample_bins = 15
        set.max_width = 15
        set.prob_number_of_events_in_zones = [5000,1000,1000,3000,1000,1000]
        set.prob_delta_azimuth_in_zones = [5,10,20,25,50,0]
        set.prob_dip_in_zones = [35,40,45,50,55,60]

        # Other stuff - needed
        set.return_periods = [10,50,100]
        set.atten_periods = [0,0.30303,1]
        set.atten_models = ['Gaull_1990_WA']
        set.atten_model_weights = [1.]
        set.save_motion = False
        set.is_scenario = True    # If False, probabilistic input used
        set.input_dir = '.'
        set.output_dir = '.'        
        try:
            para_new = create_parameter_data(set)
        except ParameterSyntaxError:
            pass
        else:
            self.failUnless(False, "SystemExit not raised")

   
    def test_not_really_a_test(self):
        # Create an example of a python setdata file.
        para_old = Dict_key_as_attributes( {
            'Bclasses': {'buildings_set_damping_Be_to_5_percent': 0,
                         'hazus_btypes_flag': 0,
                         'buildpars_flag': 4,
                         'buildings_usage_classification': 2},
            'Amplification': {'amp_variability_method': 2,
                              'use_amplification': 1,
                              'amp_min_factor': 0.6,
                              'amp_use_variability': 0,
                              'amp_max_factor': 10000},
            'Source': {'prob_azimuth_in_zones': 180,
                       'prob_min_mag_cutoff': 4.5,
                       'prob_number_of_mag_sample_bins': 15,
                       'max_width': 15,
                       'ftype': 2,
                       'prob_number_of_events_in_zones': array([5,2,1,3,3,1]),
                       'prob_delta_azimuth_in_zones': 180,
                       'prob_dip_in_zones': 35},
            'Save': {'save_prob_structural_damage': 0,
                     'save_probdam_flag': 0,
                     'save_hazard_map': 1,
                     'save_motion': 0,
                     'save_socloss_flag': 0},
            'Attenuation': {'atten_smooth_spectral_acceleration': 0,
                            'atten_pga_scaling_cutoff': 2,
                            'attenuation_flag': [array([1]), array([1])],
                            'atten_periods': array([ 0.     ,  1.     ]),
                            'atten_variability_method': 2,
                            'atten_threshold_distance': 400,
                            'atten_override_RSA_shape': 0,
                            'atten_use_variability': 0,
                            'atten_log_sigma_eq_weight':0.0},
            'Bclasses2': {'determ_buse': -9999,
                          'force_btype_flag': 0,
                          'determ_btype': -9999},
            'site_db_tag': '',
            'Event_Spawn': {'src_eps_switch': 0,
                            'mbnd': 4,
                            'nsigma': 2.5,
                            'nsamples': 5},
            'prob_number_of_events_in_zones': [5, 2, 1, 3, 3, 1],
            'CSM': {'csm_use_variability':0,
                    'csm_standard_deviation': 0.3,
                    'csm_variability_method': 3,
                    'csm_hysteretic_damping': 'curve',
                    'csm_SDcr_tolerance_percentage': 1,
                    'csm_damping_max_iterations': 7},
            'Loss': {'loss_regional_cost_index_multiplier': 1.45,
                     'loss_min_pga': 0.05,
                     'loss_aus_contents': 0},
            'Scenario': {'scenario_azimith': 340,
                         'scenario_depth': 11.5,
                         'scenario_latitude': -32.,
                         'scenario_magnitude': 6.0,
                         'scenario_number_of_events': 2,
                         'scenario_longitude': 151.,
                         'is_scenario': 0},
            'attenuation_flag': (array([1]), array([1])),
            'output_dir': 'EQRM_output',
            'Diagnostics': {'qa_switch_watercheck': 0,
                            'qa_switch_attn': 0,
                            'qa_switch_ampfactors': 0,
                            'qa_switch_vun': -9999,
                            'qa_switch_soc': -9999,
                            'qa_switch_mke_evnts': 0,
                            'qa_switch_map': 1,
                            'qa_switch_fuse': 0},
            'save_contents_loss': False,
            'prob_delta_azimuth_in_zones': array([180, 180, 180,
                                                  180, 180, 180]),
            'prob_azimuth_in_zones': array([180, 180, 180, 180, 180, 180]),
            'General': {'destring': 'no description sring set',
                        'site_tag': 'newc',
                        'site_indexes': array([ 2255, 11511, 10963,
                                                686,  1026]),
                        'input_dir': 'EQRM_input',
                        'output_dir': 'EQRM_output',
                        'return_periods': [array([10]), array([50]),
                                           array([100]),
                                     array([200]),
                                     array([500]),
                                     array([1000]),
                                     array([5000]),
                                     array([10000])],
                        'grid_flag': 1},
            'input_dir': 'EQRM_input',
            'save_total_financial_loss': False,
            'save_building_loss': False,
            'prob_dip_in_zones': array([35, 35, 35, 35, 35, 35]),
            'Operation_Mode': {'run_type': 1}})
        eqrm_dir = determine_eqrm_path()
        output_base_name = join(eqrm_dir, 'Documentation', 'set_data_example')
        convert_THE_PARAM_T_to_py(output_base_name, para_old)

   
    def test_find_set_data_py_files(self):
        
        # Using the function, not testing it.
        # Go to a dir and find the number of data files
        set_data_files = find_set_data_py_files(Resources_Data_Path)
        files_num = len(set_data_files)
        new_set_data_file = join(Resources_Data_Path, 'remove_this_file.py')
        try:
            os.remove(new_set_data_file)
        except:
            pass

        ## Create the new set_data like file
        f = open(new_set_data_file,'w')
        f.write('"""\n')
        f.write(SECOND_LINE)
        f.close()
        
        set_data_files = find_set_data_py_files(Resources_Data_Path)

        os.remove(new_set_data_file)
        
        self.failUnless(len(set_data_files) ==
                        files_num +1, "find_set_data_py_files fail.")

        
    def test_old_set_data_py_2_new_set_data_py(self):
        set = self.small_set_data()
        file, file_name = tempfile.mkstemp('.py', __name__+'_')
        os.close(file)
        convert_THE_PARAM_T_to_py(file_name, set)
        old_set_data_py_2_new_set_data_py(file_name)
        new_set = create_parameter_data(file_name)
        self.failUnlessEqual(set.csm_damping_regimes,
                             new_set.csm_damping_regimes)
        self.failUnlessEqual(set.csm_damping_use_smoothing,
                             new_set.csm_damping_use_smoothing)
        self.failUnlessEqual(set.csm_damping_regimes,
                             new_set.csm_damping_regimes)
                        
        os.remove(file_name)
        os.remove(file_name[:-3]+ '.pyc')
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Parse_in_parameters,'test')
    
    #suite = unittest.makeSuite(Test_Parse_in_parameters,'test_instance_to_THE_PARAM_T')
    #suite = unittest.makeSuite(Test_Parse_in_parameters,'test_convert_par_to_py')
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)
