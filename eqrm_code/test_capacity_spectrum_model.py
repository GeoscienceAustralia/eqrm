import os
import sys
#sys.path.append(os.getcwd()+os.sep+os.pardir+os.sep+'eqrm_code')
import unittest

from numpy import array, allclose, asarray

from eqrm_code.capacity_spectrum_model import Capacity_spectrum_model, \
     CSM_DAMPING_REGIMES_USE_ALL, CSM_DAMPING_MODIFY_TAV
from eqrm_code.capacity_spectrum_functions import CSM_DAMPING_USE_SMOOTHING


def reset_seed(use_determ_seed=False):
    """Set random seeds.

    use_determ_seed  True if we use a fixed seed (for testing)
    """
    
    from random import seed as pyseed
    from random import random
    from numpy.random import seed

    if use_determ_seed:
        # reset both seeds to a deterministic inital state
	pyseed(11)
	seed(10)
    else:
        from time import time 

	pyseed(int(time()))
	seed(int(999*random()+time()))

class Test_Capaciy_Spectrum_model(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_OS_bug_search(self):
        """
        Used to trackdown ticket #98
        """
        SA =array([[[
    0.14210731,  0.29123634 , 0.23670422 , 0.13234554, 0.08648546 ,0.06338455,
    0.04945741,  0.04140068 , 0.03497466 , 0.02969136, 0.02525473 ,0.02151188,
    0.018371  ,  0.01571802 , 0.01344816 , 0.01148438, 0.00980236 ,0.00836594,
    0.00714065,  0.00609482],
  [ 0.2093217 ,  0.30976405 , 0.16232743 , 0.06989206, 0.03216174 ,0.01945677,
    0.01347719,  0.00987403 , 0.00799221 , 0.00660128, 0.00547129 ,0.0045463,
    0.0042072 ,  0.00418348 , 0.0041599  , 0.00413222, 0.00410333 ,0.00407463,
    0.00404614,  0.00401785],
  [ 0.01450217,  0.02750284 , 0.02231209 , 0.01127933, 0.00793098 ,0.00621618,
    0.0051103 ,  0.00430777 , 0.00364714 , 0.0031542, 0.00279411 ,0.00247654,
    0.0022153 ,  0.001994   , 0.0017948  , 0.00161223, 0.00144737 ,0.00129929,
    0.00117312,  0.00105988]]])
        csm_params = {
            'building_parameters': {
            'residential_drift_threshold': array([[  21.9456,   43.8912,
                                                     109.728 ,  164.592 ]]),
            'design_strength': array([ 0.033]),
            'design_strength_sigma': array([ 0.3]),
            'height': array([ 7315.2]),
            'ultimate_to_yield': array([ 3.]),
            'ultimate_to_yield_sigma': array([ 0.3]),
            'structure_class':array(['BUILDING'],dtype='|S8'),
            'non_residential_drift_threshold': array([[   5.4864,   43.8912,
                                                      82.296 ,  137.16  ]]) ,
            'damping_Be': array([ 0.1]),
            'fraction_in_first_mode': array([ 0.8]),
            'fraction_in_first_mode_sigma': array([ 0.3]),
            'nsd_a_ratio': array([ 0.7254902]),
            'acceleration_threshold': array([[ 0.2,  0.4,  0.8,  1.6]]),
            'nsd_d_ratio': array([ 0.11764706]),
            'structure_ratio': array([ 0.15686275]),
            'structural_damage_threshold': array([[  26.33472,   41.69664,
                                                     88.87968,  219.456  ]]),
            'natural_elastic_period': array([ 0.5]),
            'natural_elastic_period_sigma': array([ 0.3]),
            'damping_s': array([ 0.4]),
            'drift_threshold': array([[   5.4864,   43.8912,
                                          82.296 ,  137.16  ]]),
            'yield_to_design': array([ 1.5]),
            'yield_to_design_sigma': array([ 0.3]),
            'structure_classification': array(['S1L'],dtype='|S13'),
            'height_to_displacement': array([ 0.75]),
            'height_to_displacement_sigma': array([ 0.3]),
            'ductility': array([ 5.]),
            'ductility_sigma': array([ 0.3]),
            'degrading_alpha': array([0.4]),
            'degrading_alpha_sigma': array([0.3]),
            'degrading_beta': array([0.6]),
            'degrading_beta_sigma': array([0.3]),
            'degrading_delta': array([0.8]),
            'degrading_delta_sigma': array([0.3]),
            'degrading_theta': array([1]),
            'degrading_theta_sigma': array([0.3]),
            'damping_l': array([ 0.]),
            'damping_m': array([ 0.2])},
            'loss_min_pga': 0.050000000000000003,
            'csm_hysteretic_damping': 'Error',
            'csm_variability_method': None,
            'rtol': 0.01,
            'csm_damping_regimes': CSM_DAMPING_REGIMES_USE_ALL,
            'csm_damping_modify_Tav': CSM_DAMPING_MODIFY_TAV,
            'csm_damping_use_smoothing': CSM_DAMPING_USE_SMOOTHING,
            'magnitudes': array([ 6.0201519,  6.0201519,  6.0201519]),
            'periods': array(
            [ 0.     ,  0.17544,  0.35088,  0.52632,  0.70175,  0.87719,
              1.0526 ,  1.2281 ,  1.4035 ,  1.5789 ,  1.7544 ,  1.9298 ,
              2.1053 ,  2.2807 ,  2.4561 ,  2.6316 ,  2.807  ,  2.9825 ,
              3.1579 ,  3.3333 ]),
            'atten_override_RSA_shape': None,
            'atten_cutoff_max_spectral_displacement': False,
            'csm_damping_max_iterations': 7}
        
        reset_seed(True)
        capacity_spectrum_model=Capacity_spectrum_model(**csm_params)
        point=capacity_spectrum_model.building_response(SA)
        point_windows= (array([[ 0.10708486,  0.0642546,   0.]]),
                        array([[ 7.33157578,  3.98902927,  0.]]))
        self.assert_(allclose(asarray(point), asarray(point_windows)),
                     'Expected:\n%s,\nGot:\n%s' % (asarray(point_windows),
                                                   asarray(point)))


    def test_OS_bug_searchII(self):
        """
        Used to trackdown ticket #98
        """
        SA =array([[[
    0.14210731,  0.29123634 , 0.23670422 , 0.13234554, 0.08648546 ,0.06338455,
    0.04945741,  0.04140068 , 0.03497466 , 0.02969136, 0.02525473 ,0.02151188,
    0.018371  ,  0.01571802 , 0.01344816 , 0.01148438, 0.00980236 ,0.00836594,
    0.00714065,  0.00609482]]])
        csm_params = {
            'building_parameters': {
            'residential_drift_threshold': array([[  21.9456,   43.8912,
                                                     109.728 ,  164.592 ]]),
            'design_strength': array([ 0.033]),
            'design_strength_sigma': array([ 0.3]),
            'height': array([ 7315.2]),
            'ultimate_to_yield': array([ 3.]),
            'ultimate_to_yield_sigma': array([ 0.3]),
            'structure_class':array(['BUILDING'],dtype='|S8'),
            'non_residential_drift_threshold': array([[   5.4864,   43.8912,
                                                      82.296 ,  137.16  ]]) ,
            'damping_Be': array([ 0.1]),
            'fraction_in_first_mode': array([ 0.8]),
            'fraction_in_first_mode_sigma': array([ 0.3]),
            'nsd_a_ratio': array([ 0.7254902]),
            'acceleration_threshold': array([[ 0.2,  0.4,  0.8,  1.6]]),
            'nsd_d_ratio': array([ 0.11764706]),
            'structure_ratio': array([ 0.15686275]),
            'structural_damage_threshold': array([[  26.33472,   41.69664,
                                                     88.87968,  219.456  ]]),
            'natural_elastic_period': array([ 0.5]),
            'natural_elastic_period_sigma': array([ 0.3]),
            'damping_s': array([ 0.4]),
            'drift_threshold': array([[   5.4864,   43.8912,
                                          82.296 ,  137.16  ]]),
            'yield_to_design': array([ 1.5]),
            'yield_to_design_sigma': array([ 0.3]),
            'structure_classification': array(['S1L'],dtype='|S13'),
            'height_to_displacement': array([ 0.75]),
            'height_to_displacement_sigma': array([ 0.3]),
            'ductility': array([ 5.]),
            'ductility_sigma': array([ 0.3]),
            'degrading_alpha': array([0.4]),
            'degrading_alpha_sigma': array([0.3]),
            'degrading_beta': array([0.6]),
            'degrading_beta_sigma': array([0.3]),
            'degrading_delta': array([0.8]),
            'degrading_delta_sigma': array([0.3]),
            'degrading_theta': array([1]),
            'degrading_theta_sigma': array([0.3]),
            'damping_l': array([ 0.]),
            'damping_m': array([ 0.2])},
            'loss_min_pga': 0.050000000000000003,
            'csm_hysteretic_damping': 'Error',
            'csm_variability_method': None,
            'rtol': 0.01,
            'csm_damping_regimes': CSM_DAMPING_REGIMES_USE_ALL,
            'csm_damping_modify_Tav': CSM_DAMPING_MODIFY_TAV,
            'csm_damping_use_smoothing': CSM_DAMPING_USE_SMOOTHING,
            'magnitudes': array([ 6.0201519]),
            'periods': array(
            [ 0.     ,  0.17544,  0.35088,  0.52632,  0.70175,  0.87719,
              1.0526 ,  1.2281 ,  1.4035 ,  1.5789 ,  1.7544 ,  1.9298 ,
              2.1053 ,  2.2807 ,  2.4561 ,  2.6316 ,  2.807  ,  2.9825 ,
              3.1579 ,  3.3333 ]),
            'atten_override_RSA_shape': None,
            'atten_cutoff_max_spectral_displacement': False,
            'csm_damping_max_iterations': 7}
        
        reset_seed(True)
        capacity_spectrum_model=Capacity_spectrum_model(**csm_params)
        point=capacity_spectrum_model.building_response(SA)
        point_windows= (array([[ 0.10708486]]),
                        array([[ 7.33157578]]))
        self.assert_(allclose(asarray(point), asarray(point_windows)),
                     'Expected:\n%s,\nGot:\n%s' % (asarray(point_windows),
                                                   asarray(point)))

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Capaciy_Spectrum_model,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
