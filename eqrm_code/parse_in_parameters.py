"""
  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, duncan.gray@ga.gov.au
           
  Description: Parse in the parameter file.

 
  Version: $Revision: 1643 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-04-25 20:05:29 +1000 (Sun, 25 Apr 2010) $
  
  Copyright 2007 by Geoscience Australia
  
"""

import sys
from sys import path
import os
import imp
from os import sep, getenv, listdir
from os.path import join, splitext, normpath
from time import strftime, localtime
from operator import itemgetter
from scipy import allclose, array, sort, asarray, ndarray
from numpy import ndarray
import copy

from eqrm_code.eqrm_filesystem import eqrm_path
from eqrm_code.capacity_spectrum_model import Capacity_spectrum_model, \
     CSM_DAMPING_MODIFY_TAV, CSM_DAMPING_DO_NOT_MODIFY_TAV
from eqrm_code.capacity_spectrum_functions import CSM_DAMPING_USE_SMOOTHING, \
     CSM_DAMPING_DO_NOT_USE_SMOOTHING
from eqrm_code.ANUGA_utilities import log

# DSG-DSG this needs more comments.
"""
Principals of the set_data.py file format.

All attributes are specified in CONV_DIC_NEW.

If an attribute is not present in the set_data.py file and the
attribute has a default value, this value will be used in THE_PARAM_T.

Setting an attribute to None is not equivaluent to removing the
attribute from the set_data.py file, since not all attributes default
to None.

If an attribute does not have to be defined it is given a default
value of None.  An attribute without a default has to be defined.

Lists are automatically converted to arrays.

"""

ENV_EQRMDATAHOME = 'EQRMDATAHOME'
VAR_NAME_IN_SET_DATA_FILE = 'sdp'
SECOND_LINE = '  EQRM parameter file'


CONV_NEW = [{'order': 10.0,
             'title': '\n# Operation Mode\n'},
            {'old_para': 'run_type',
             'values': {None: None,
                        1: 'hazard',
                        2: 'risk'},
             'order': 10.01,
             'new_para': 'run_type'},
            {'old_para': 'determ_flag',
             'values': {None: None,
                        1: True,
                        0: False},
             'order': 10.02,
             'new_para': 'is_scenario'},
            {'old_para': 'wdth',
             'order': 10.03,
             'new_para': 'max_width',
             'default': None},
            {'old_para': 'reset_seed_using_time',
             'order': 10.05,
             'new_para': 'reset_seed_using_time',
             'default': True},
            {'old_para': 'compress_output',
             'order': 10.06,
             'new_para': 'compress_output',
             'default': False},
            {'old_para': 'site_loc',
             'order': 10.07,
             'new_para': 'site_tag'},
            {'old_para': 'site_db_tag',
             'order': 10.075,
             'new_para': 'site_db_tag',
             'default': ""},
            {'old_para': 'rtrn_per',
             'order': 10.08,
             'new_para': 'return_periods'},
            {'old_para': 'inputdir',
             'order': 10.11,
             'new_para': 'input_dir'},
            {'old_para': 'savedir',
             'order': 10.12,
             'new_para': 'output_dir'},
            {'old_para': 'small_site_flag',
             'values': {None: None,
                        1: True,
                        0: False},
             'order': 10.13,
             'new_para': 'use_site_indexes',
             'default': False},
            {'old_para': 'SiteInd',
             'order': 10.14,
             'new_para': 'site_indexes',
             'default': None},
            {'old_para': 'fault_source_tag',
             'order': 10.15,
             'new_para': 'fault_source_tag',
             'default': None},
            {'old_para': 'zone_source_tag',
             'order': 10.16,
             'new_para': 'zone_source_tag',
             'default': None},
            {'old_para': 'event_control_tag',
             'order': 10.17,
             'new_para': 'event_control_tag',
             'default': None},
            {'order': 30.0,
             'title': '\n# Scenario input\n'},
            {'old_para': 'determ_azi',
             'order': 30.02,
             'new_para': 'scenario_azimuth',
             'default': None},
            {'old_para': 'determ_r_z',
             'order': 30.03,
             'new_para': 'scenario_depth',
             'default': None},
            {'old_para': 'determ_lat',
             'order': 30.04,
             'new_para': 'scenario_latitude',
             'default': None},
            {'old_para': 'determ_lon',
             'order': 30.05,
             'new_para': 'scenario_longitude',
             'default': None},
            {'old_para': 'determ_mag',
             'order': 30.06,
             'new_para': 'scenario_magnitude',
             'default': None},
            {'order': 30.07,
             'new_para': 'scenario_dip',
             'default': None},
            {'old_para': 'determ_ntrg',
             'order': 30.08,
             'new_para': 'scenario_number_of_events',
             'default': None},
            {'order': 40.0,
             'title': '\n# Probabilistic input\n'},
            {'old_para': 'azi',
             'order': 40.01,
             'new_para': 'prob_azimuth_in_zones',
             'default': None},
            {'old_para': 'd_azi',
             'order': 40.015,
             'new_para': 'prob_delta_azimuth_in_zones',
             'default': None},
            {'old_para': 'min_mag_cutoff',
             'order': 40.02,
             'new_para': 'prob_min_mag_cutoff',
             'default': None},
            {'old_para': 'nbins',
             'order': 40.03,
             'new_para': 'prob_number_of_mag_sample_bins',
             'default': None},
            {'old_para': 'ntrgvector',
             'order': 40.05,
             'new_para': 'prob_number_of_events_in_zones',
             'default': None},
            {'order': 10.18,
             'new_para': 'prob_number_of_events_in_faults',
             'default': None},
            {'old_para': 'dip',
             'order': 40.07,
             'new_para': 'prob_dip_in_zones',
             'default': None},
            {'order': 50.0,
             'title': '\n# Attenuation\n'},
            {'order': 50.01,
             'new_para': 'atten_models',
             'default': None},
            {'order': 50.02,
             'new_para': 'atten_model_weights',
             'default': None},
            {'order': 50.03,
             'new_para': 'atten_collapse_Sa_of_atten_models',
             'default': False},
            {'old_para': 'var_attn_method',
             'order': 50.05,
             'new_para': 'atten_variability_method',
             'default': 2},
            {'old_para': 'periods',
             'order': 50.06,
             'new_para': 'atten_periods'},
            {'old_para': 'Rthrsh',
             'order': 50.07,
             'new_para': 'atten_threshold_distance',
             'default': 400},
            {'order': 50.08,
             'new_para': 'atten_spawn_bins',
             'default': None},
            {'old_para': 'resp_crv_flag',
             'values': {0: None,
                        2: 'Aust_standard_Sa',
                        4: 'HAZUS_Sa'},
             'order': 50.09,
             'new_para': 'atten_override_RSA_shape',
             'default': None},
            {'order': 50.10,
             'new_para': 'atten_cutoff_max_spectral_displacement',
             'default': False},
            {'old_para': 'pgacutoff',
             'order': 50.11,
             'new_para': 'atten_pga_scaling_cutoff',
             'default': 2},
            {'old_para': 'smoothed_response_flag',
             'values': {None: None,
                        1: True,
                        0: False},
             'order': 50.12,
             'new_para': 'atten_smooth_spectral_acceleration',
             'default': False},
            {'old_para': 'log_sigma_eq_weight',
             'order': 50.13,
             'new_para': 'atten_log_sigma_eq_weight',
             'default': 0},
            {'order': 60.0,
             'title': '\n# Amplification\n'},
            {'old_para': 'amp_switch',
             'values': {None: None,
                        1: True,
                        0: False},
             'order': 60.01,
             'new_para': 'use_amplification'},
            {'old_para': 'var_amp_method',
             'order': 60.03,
             'new_para': 'amp_variability_method',
             'default': 2},
            {'old_para': 'MinAmpFactor',
             'order': 60.04,
             'new_para': 'amp_min_factor',
             'default': None},
            {'old_para': 'MaxAmpFactor',
             'order': 60.05,
             'new_para': 'amp_max_factor',
             'default': None},
            {'order': 70.0,
             'title': '\n# Buildings\n'},
            {'old_para': 'b_usage_type_flag',
             'values': {None: None,
                        1: 'HAZUS',
                        2: 'FCB'},
             'order': 70.01,
             'new_para': 'buildings_usage_classification',
             'default': None},
            {'old_para': 'hazus_dampingis5_flag',
             'values': {None: None,
                        1: True,
                        0: False},
             'order': 70.02,
             'new_para': 'buildings_set_damping_Be_to_5_percent',
             'default': None},
            {
             'order': 75.01,
             'new_para': 'bridges_functional_percentages',
             'default': None},
            {'order': 80.0,
             'title': '\n# Capacity Spectrum Method\n'},
            {'old_para': 'var_bcap_flag',
             'values': {None: None,
                        1: True,
                        0: False},
             'order': 80.01,
             'new_para': 'csm_use_variability',
             'default': None},
            {'old_para': 'bcap_var_method',
             'order': 80.02,
             'new_para': 'csm_variability_method',
             'default': 3},
            {'old_para': 'stdcap',
             'order': 80.03,
             'new_para': 'csm_standard_deviation',
             'default': None},
            {'order': 80.04,
             'new_para': 'csm_damping_regimes',
             'default': None},
            {'order': 80.05,
             'new_para': 'csm_damping_modify_Tav',
             'default': None},
            {'order': 80.06,
             'new_para': 'csm_damping_use_smoothing',
             'default': None},
            {'old_para': 'Harea_flag',
             'values': {None: None,
                        1: 'Error',
                        2: 'trapezoidal',
                        3: 'curve'},
             'order': 80.08,
             'new_para': 'csm_hysteretic_damping',
             'default': None},
            {'old_para': 'SDRelTol',
             'order': 80.09,
             'new_para': 'csm_SDcr_tolerance_percentage',
             'default': None},
            {'old_para': 'max_iterations',
             'order': 80.10,
             'new_para': 'csm_damping_max_iterations',
             'default': None},
            {'order': 90.0,
             'title': '\n# Loss\n',
             'default': None},
            {'old_para': 'pga_mindamage',
             'order': 90.01,
             'new_para': 'loss_min_pga',
             'default': None},
            {'old_para': 'ci',
             'order': 90.02,
             'new_para': 'loss_regional_cost_index_multiplier',
             'default': None},
            {'old_para': 'aus_contents_flag',
             'order': 90.03,
             'new_para': 'loss_aus_contents',
             'default': None},
            {'order': 100.0,
             'title': '\n# Save\n',
             'default': None},
            {'old_para': 'hazard_map_flag',
             'values': {None: None,
                        1: True,
                        0: False},
             'order': 100.01,
             'new_para': 'save_hazard_map',
             'default': False},
            {'old_para': 'save_total_financial_loss',
             'order': 100.02,
             'new_para': 'save_total_financial_loss',
             'default': False},
            {'old_para': 'save_building_loss',
             'order': 100.03,
             'new_para': 'save_building_loss',
             'default': False},
            {'old_para': 'save_contents_loss',
             'order': 100.04,
             'new_para': 'save_contents_loss',
             'default': False},
            {'old_para': 'save_motion_flag',
             'values': {None: None,
                        1: True,
                        0: False},
             'order': 100.05,
             'new_para': 'save_motion',
             'default': False},
            {'old_para': 'save_deagecloss_flag',
             'values': {None: None,
                        1: True,
                        0: False},
             'order': 100.06,
             'new_para': 'save_prob_structural_damage',
             'default': False}
            ]

OLD_STYLE_PARAS_HARD_WIRED = {'hazus_btypes_flag':0, 'force_btype_flag':0,
                              'buildpars_flag':4, 'grid_flag':1}
KNOWN_KWARGS = {'use_determ_seed':None,
                     'compress_output':None,
                     'eqrm_dir':None,
                     'is_parallel':None,
                     'default_input_dir':None}
# The key is the depreciated parameter.
# the value is
# None, which means the only action is a warming,
#   OR
# a string, which replaces the depreciated parameter,
#   OR
# the value has a dictinary where the the keys are the value of the
# depreciated parameter and the values are attribute and value pairs
# to use, based on the value of the parameter.  The
DEPRECIATED_PARAS = {'atten_use_variability':
                     {True:None,
                      False:('atten_variability_method', None)},
                     'amp_use_variability':
                     {True:None,
                      False:('amp_variability_method', None)},
                     'atten_use_rescale_curve_from_pga':
                     {True:None, # None means do nothing
                      False:('atten_override_RSA_shape', None)},
                     'csm_use_hysteretic_damping':
                     {True:None, # None means do nothing
                      False:('csm_hysteretic_damping', None)},
                     'atten_use_pga_scaling_cutoff':
                     {True:None, # None means do nothing
                      False:('atten_pga_scaling_cutoff', None)},
                     'atten_aggregate_Sa_of_atten_models':
                     'atten_collapse_Sa_of_atten_models',
                     'atten_rescale_curve_from_pga':
                     'atten_override_RSA_shape',
                     'scenario_azimith':'scenario_azimuth',
                     'determ_azimith':'scenario_azimuth',
                     'determ_depth':'scenario_depth',
                     'determ_latitude':'scenario_latitude',
                     'determ_longitude':'scenario_longitude',
                     'determ_magnitude':'scenario_magnitude',
                     'determ_dip':'scenario_dip',
                     'determ_number_of_events':'scenario_number_of_events',
                     'is_deterministic':'is_scenario',
                     'prob_azimuth_in_zones':None,
                     'prob_delta_azimuth_in_zones':None,
                     'prob_dip_in_zones':None,
                     'prob_number_of_mag_sample_bins':None,
                     'save_prob_strucutural_damage':
                     'save_prob_structural_damage'
#                      'csm_use_variability':
#                      {True:None, # None means do nothing
#                       None:('csm_variability_method', None), 
#                       False:('csm_variability_method', None)},
                     }

# This has all allowable set_data variables
CONV_DIC_NEW = {}
for item in CONV_NEW:
    if item.has_key('new_para'):
        CONV_DIC_NEW[item['new_para']] = item
CONV_DIC_NEW.update(KNOWN_KWARGS)
CONV_DIC_NEW.update(OLD_STYLE_PARAS_HARD_WIRED)


PAR_STYLE_TITLES = [{'title':'\n# Operation Mode\n', 'order':10.0},
                    {'title':'\n# Scenario input\n', 'order':30.0},
                    {'title':'\n# Probabilistic input\n', 'order':40.0},
                    {'title':'\n# Attenuation\n', 'order':50.0},
                    {'title':'\n# Amplification\n', 'order':60.0},
                    {'title':'\n# Buildings\n', 'order':70.0},
                    {'title':'\n# Bridges\n', 'order':75.0},
                    {'title':'\n# Capacity Spectrum Method\n', 'order':80.0},
                    {'title':'\n# Loss\n', 'order':90.0},
                    {'title':'\n# Save\n', 'order':100.0},
                    {'title':'\n# General\n', 'order':110.0}]


class Error(Exception):
    """Base exception for all exceptions raised in parse_in_parameters."""
    pass


class ParameterSyntaxError(Error):
    """There is a syntax Error in the parameters file."""
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    

def create_parameter_data(parameters, **kwargs):
    """
    parameters: Has 2 forms:
      A string of the .py file to load
      or an instance with the required attributes.
    **kwargs:  This are attributes that are attached to THE_PARAM_T
      the known **kwargs are;
        use_determ_seed
        compress_output
        eqrm_dir
        is_parallel
        default_input_dir

    Return:
      THE_PARAM_T, which is a Dict_key_as_attributes object.
    """
    if isinstance(parameters, str) and parameters[-3:] == ".py":
        parameters = from_file_get_params(parameters)
        #print "parameters", parameters
    elif isinstance(parameters, dict):
        parameters = get_no_instance_params(parameters)
    else:
        parameters = introspect_attribute_values(parameters)
    # parameters is now a dictionary
    
    # The parameters value have presidence/overwrite the kwargs
    kwargs.update(parameters)
    THE_PARAM_T = Dict_key_as_attributes(kwargs)

    # Add Hard-wired results  
    THE_PARAM_T.update(OLD_STYLE_PARAS_HARD_WIRED)

    # Remove depreciated attributes
    depreciated_attributes(THE_PARAM_T)
    
    #print "THE_PARAM_T", THE_PARAM_T
    # Add default values
    att_default_values(THE_PARAM_T)

   
    # Check att names
    conv_new_dic = {}
    for key in THE_PARAM_T:
        if not CONV_DIC_NEW.has_key(key):
            msg = ("Parameter Error: Attribute " + key + " is unknown.")
            raise ParameterSyntaxError(msg)
            
    # Do attribute value fixes    
    att_value_fixes(THE_PARAM_T)

    # Check if values are consistant
    verify_THE_PARAM_T(THE_PARAM_T)
    
    return THE_PARAM_T

def get_no_instance_params(parameters):
    # Assume locals() has been called.
    locals = copy.copy(parameters)
    for key in locals.keys():
        if key[-2:] == '__' or callable(locals[key]):
            del locals[key]
    return locals


def att_default_values(THE_PARAM_T):
    """Add default values
    """
        
    for item in CONV_NEW: 
        if item.has_key('new_para') and \
               not THE_PARAM_T.has_key(item['new_para']):
            if item.has_key('default'):
                THE_PARAM_T[item['new_para']] = item['default']
            else:
                raise ParameterSyntaxError(
                "Parameter Error: Attribute "  + item['new_para']
                + " must be defined.")

def depreciated_attributes(THE_PARAM_T):
    """
    Remove/fix depreciated attributes.
    Give a warning.
    """
    for item in DEPRECIATED_PARAS:
        if THE_PARAM_T.has_key(item):
            handle_logic = DEPRECIATED_PARAS[item]
            if handle_logic is None:
                pass
            elif isinstance(handle_logic, str):
                # handle_logic is a replacement string
                # for the parameter name
                THE_PARAM_T[handle_logic] = THE_PARAM_T[item]
                del THE_PARAM_T[item]
            else:                
                # handle_logic is a dictionary
                what_to_do = handle_logic[THE_PARAM_T[item]]
                if what_to_do is not None:
                    # The value is a tuple.
                    # the first value is the att name
                    # the second value is the att value
                    THE_PARAM_T[what_to_do[0]] = what_to_do[1]                
                del THE_PARAM_T[item]
            msg = 'WARNING: ' + item + \
                  ' term in set data files is depreciated.'
            # logging is only set-up after the para file has been passed.
            # So these warnings will not in in the logs.
            log.warning(msg)

def att_value_fixes(THE_PARAM_T):
    """
    Change the attribute values so they are in the correct format for EQRM
      e.g. scaler values into arrays
    """
    # convert all lists into arrays
    for att in THE_PARAM_T:
        att_val = getattr(THE_PARAM_T, att)
        if isinstance(att_val, list):
            THE_PARAM_T[att] = asarray(THE_PARAM_T[att])

    # FIXME Change the format to an array or
    # state why this format is needed.
    THE_PARAM_T['return_periods'] = [ \
        array([x]) for x in THE_PARAM_T['return_periods']]

    # Convert scaler values into arrays
    try:
        len_prob_number_of_events_in_zones = len(
            THE_PARAM_T.prob_number_of_events_in_zones)
    except:
        len_prob_number_of_events_in_zones=1 # if only 1 zone
    
    if THE_PARAM_T.is_scenario ==0:
        THE_PARAM_T['prob_dip_in_zones'] = scalar2vec(
            THE_PARAM_T.prob_dip_in_zones,len_prob_number_of_events_in_zones)
        THE_PARAM_T['prob_azimuth_in_zones'] = scalar2vec(
            THE_PARAM_T.prob_azimuth_in_zones,
            len_prob_number_of_events_in_zones)
        THE_PARAM_T['prob_delta_azimuth_in_zones'] = scalar2vec(
            THE_PARAM_T.prob_delta_azimuth_in_zones,
            len_prob_number_of_events_in_zones)
    
    if THE_PARAM_T.save_motion == 1 and THE_PARAM_T.is_scenario == 0:
            raise ValueError('do not save motion for a generated event')

    # FIXME this should happen to the weights from sources as well. 
    weights = THE_PARAM_T.atten_model_weights
    
    if weights is not None:        
        THE_PARAM_T['atten_model_weights'] = check_sum_1_normalise(weights)

    
    # if periods is collapsed (into a scalar), turn it into a vector
    if not isinstance(THE_PARAM_T.atten_periods,ndarray):
        THE_PARAM_T['atten_periods'] = array([THE_PARAM_T.atten_periods])

    # Fix the string specifying the directory structure
    if not THE_PARAM_T.output_dir[-1] == '/':
        THE_PARAM_T['output_dir'] = THE_PARAM_T.output_dir+'/'
    if not THE_PARAM_T.input_dir[-1] == '/':
        THE_PARAM_T['input_dir'] = THE_PARAM_T.input_dir+ '/'
    THE_PARAM_T['output_dir'] = change_slashes(THE_PARAM_T.output_dir)
    THE_PARAM_T['input_dir'] = change_slashes(THE_PARAM_T.input_dir)

    
def check_sum_1_normalise(weights, msg=None):
    """
    
    Check that a list or array basically sums to one.Normalise so it
    exactly sums to one.

    return a 1D array that sums to one.
    """   
    # test if attenuation weights are close to 1 (with 0.01 absolute tolerance)
    # this means that 3 weights with 0.33 should pass  
    if not allclose(weights.sum(),1.0,atol=0.01):
        if msg == None:
            msg =  'Weights should sum to 1.0, got ',weight
        raise ValueError(msg)
    
    # Re-normalise weights so they do sum to 1
    return weights/abs(weights.sum()) # normalize
    

        
def isscalar(x):
    if isinstance(x,int) or isinstance(x,float):
        return True
    else:
        return not hasattr(x,'__len__')

            
def scalar2vec(x,leny):       
    if isscalar(x):
        xtmp = x
        x=[]
        for k in range(leny):
            x.append(xtmp)
        x=array(x)
    return x


def change_slashes(path):
    """Swap from windows to linux file slashes
    """
    if sys.platform == 'linux2':
        split_path = path.split('\\')
        if len(split_path) >= 2:
            path = apply(join, split_path)
    return path


unique_load_source_int = 0            
def from_file_get_params(path_file):
    global unique_load_source_int
    head, tail = os.path.split(os.path.abspath(path_file))
    name = 'name_' + str(unique_load_source_int)
    unique_load_source_int += 1
    para_imp = imp.load_source(name, path_file)
    # FIXME big hack.  The Parameter_data instance name is hard-wired
    # Have it parse the 'sdp = Parameter_data()' line for the name
    try:
        para_imp = getattr(para_imp,VAR_NAME_IN_SET_DATA_FILE)
    except AttributeError:
        pass
        # Assume this is a no instance file
    parameters = introspect_attribute_values(para_imp)
    return parameters


def verify_THE_PARAM_T(THE_PARAM_T):

    # Value verification, expanding and fixing.
    if not allclose(THE_PARAM_T.atten_periods,
                    sort(THE_PARAM_T.atten_periods)):
        raise ParameterSyntaxError(
            "Syntax Error: Period values are not ascending")

                
#     if THE_PARAM_T.save_motion == True and THE_PARAM_T.is_scenario == True \
#             and THE_PARAM_T.scenario_number_of_events > 1:
#       raise ParameterSyntaxError(
#       'Cannot save motion for a scenario' + 
#                        ' with more than one event.')
    
    if THE_PARAM_T.save_hazard_map == True and THE_PARAM_T.is_scenario == True:
      raise ParameterSyntaxError(
      'Cannot save the hazard map for a scenario.')
  
    if THE_PARAM_T.save_motion == True and THE_PARAM_T.is_scenario == False:
      raise ParameterSyntaxError(
      'Cannot save the RSA values unless you are doing a scenario.')

    if THE_PARAM_T.amp_variability_method == 1 and \
           THE_PARAM_T.run_type == 'risk':
      raise ParameterSyntaxError(
      'Cannot use spawning when doing a risk simulation.')

    # need to change some array sizes, e.g. bedrock_SA_all
#     if THE_PARAM_T.save_motion == True and \
#            THE_PARAM_T.amp_variability_method == 1:
#       raise ParameterSyntaxError(
#       'Cannot save the RSA values and spawn.')

  
    # FIXME This needs to be done, and be updated.
    #assert not ((THE_PARAM_T.save_ecloss_flag)>0 and (THE_PARAM_T.run_type<2))

def find_set_data_py_files(path=None):
    """Return a list of all the set_data .py files in a path directory.

    Based on the file having a .py extension and
    the second line in the file being == SECOND_LINE.
    """
    extension = '.py'
    
    if path is None:
        path = eqrm_path
        
    set_data_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file[-3:] == extension:
                file_path_name = join(root, file)
                f = open(file_path_name,'r')
                _ = f.readline()
                snd_line = f.readline()
                if SECOND_LINE in snd_line:
                    set_data_files.append(file_path_name)  
                f.close()
    return set_data_files

def old_set_data_py_2_new_set_data_py(file_name_path,
                                      new_file_name_path=None):
    """Open a set data .py file and then save it again,
    using the CONV_NEW rules and depreciation rules.

    Used to move attributes position around for all of the
    set_data.py files in the sandpit

    Why is this labeled as old? Because its the old set data format.
    """
    if new_file_name_path is None:
        new_file_name_path = file_name_path
    parameters = from_file_get_params(file_name_path)
    # Remove depreciated attributes
    depreciated_attributes(parameters)
    convert_attribute_dic_to_set_data_py(new_file_name_path, parameters)
    
    
def introspect_attribute_values(instance):
    """
    Puts all the attribite values of the instance into a dictionary
    """
    #for att in dir(instance):
     #   print "att", att
    attributes = [att for att in dir(instance) if not callable(
        getattr(instance, att)) and not att[-2:] == '__']
    att_values = {}
    for att in attributes:
        att_values[att] = getattr(instance, att)
    return att_values

 
    
class Dict_key_as_attributes(dict):
    """
    Expose the dictionary keys as attributes.
    Do not let the attributes be set
    """
    def __getattribute__(self,key):
        try:
            return self[key]
        except:
            for k in dict.keys(self):
                try:
                    return self[k][key]
                except:
                    pass
            return object.__getattribute__(self,key)
        #raise AttributeError(str(key)+ ' was not found')

    def __delattr__(self, name):       
        if self.has_key(name):
            del self[name]
        else:
            deleted = False
            for key in self:
                if isinstance(self[key], dict) and \
                       self[key].has_key(name):
                    del self[key][name]
                    deleted = True
                    continue
            if not deleted:
                # Sparse.  Probably means functions can't be deleted.
                # print "Attribute can not be deleted ",name 
                raise AttributeError
            
#         def __setattr__(self,key,value):
#             # FIXME DSG Should this be used?
#             # It gets messy if the values of THE_PARAM_T can be changed.
            
#             self[key]=value
#             # object.__setattr__(self, key, value)


def eqrm_data_home():
    """Return the EQRM data directory
    """
    results = getenv(ENV_EQRMDATAHOME)
    if results is None:
        print 'The environmental variable ' + ENV_EQRMDATAHOME + \
              ' , used by Parameter_data.eqrm_data_home() is not set.'
        print 'Define this variable error before continuing.'
        ###FIXME raise an error instead
        sys.exit(1)            
    return results

    
def get_time_user():
    """Return string of date, time and user.  Used to create
    time and user stamped directories.
    """
    time = strftime('%Y%m%d_%H%M%S', localtime())
    if sys.platform == "win32":
        cmd="USERNAME"
    elif sys.platform == "linux2":
        cmd="USER"
    user = os.getenv(cmd)
    return "_".join((time, user))


class Parameter_data(object):
    """Class to build the parameter_data 'onto'.
    The user will add attributes to this class.
    These attributes are used by ?? to create THE_PARAM_T data structure

    This class should not have a lot in it.
    """
    def __init__(self):
        pass

    def eqrm_data_home(self):
        """Return the EQRM data directory
        """
        results = getenv(ENV_EQRMDATAHOME)
        if results is None:
            print 'The environmental variable ' + ENV_EQRMDATAHOME + \
                  ' , used by Parameter_data.eqrm_data_home() is not set.'
            print 'Define this variable error before continuing.'
            ###FIXME raise an error instead
            sys.exit(1)            
        return results

    
    def get_time_user(self):
        """Return string of date, time and user.  Used to create
        time and user stamped directories.
        """
        time = strftime('%Y%m%d_%H%M%S', localtime())
        if sys.platform == "win32":
            cmd="USERNAME"
        elif sys.platform == "linux2":
            cmd="USER"
        user = os.getenv(cmd)
        return "_".join((time, user))
        
def convert_attribute_dic_to_set_data_py(py_file_name, attribute_dic):
    """ Given a dictionary of the set data attribute values convert it
    to a set data .py file.  set data .py files describe the EQRM
    parameters.

    py_file_name: Name of the new file.

    Output:
      A .py set_data file
    """
    
     # A list of lists
     # The inner list should be 2 long.
     #  index 0 is the parameter name
     #  index 1 is the value
    paras2print = []
    for para_dic in CONV_NEW:
        if not para_dic.has_key('new_para'):
            # Add a title from PAR_STYLE_TITLES
            paras2print.append(para_dic['title'])
        elif attribute_dic.has_key(para_dic['new_para']):
            line = [para_dic['new_para']]
            val = attribute_dic[para_dic['new_para']]
#             if not attribute_dic['is_scenario'] and \
#                    (para_dic['new_para'] == 'atten_models' or
#                     para_dic['new_para'] == 'atten_model_weights'):
#                 pass
#             else:
            line.append(val)
            paras2print.append(line)
            # Hack to add zone source tag
            if False and not attribute_dic['is_scenario']:
                print "not a scenario" 
                if para_dic['new_para'] == 'atten_models':
                    if len(val)  == 1:
                        line = ['zone_source_tag', val[0]]
                    else:
                        line = ['zone_source_tag', '3_mods_TAS']
                    print "doing zone_source_tag" 
                    paras2print.append(line)
                    line = ['event_control_tag',  "use" ]
                    paras2print.append(line)
                    
  
    writer = Write_no_instance_python_par_file(py_file_name)
    writer.write_top()
    writer.write_middle(paras2print)    
    writer.write_bottom()

    return py_file_name

# Obsolete?  
def convert_THE_PARAM_T_to_py(py_file_name, THE_PARAM_T):
    """
    Given THE_PARAM_T convert it to a set data .py file.
    set data .py files describe the EQRM parameters.

    py_file_name: Name of the new file.

    Output:
      A .py set_data file
    """
    
     # A list of lists
     # The inner list should be 2 long.
     #  index 0 is the parameter name
     #  index 1 is the value
    paras2print = []
    for para_dic in CONV_NEW:
        if not para_dic.has_key('new_para'):
            # Add a title from PAR_STYLE_TITLES
            paras2print.append(para_dic['title'])
        elif hasattr(THE_PARAM_T, para_dic['new_para']):
            line = [para_dic['new_para']]
            val = getattr(THE_PARAM_T, para_dic['new_para'])
            line.append(val)
            paras2print.append(line)
  
    writer = Write_no_instance_python_par_file(py_file_name)
    writer.write_top()
    writer.write_middle(paras2print)    
    writer.write_bottom()

    return py_file_name


def todo__convert_par_to_py(par_file_name, old_para_instance=None):
    """
    Note, this function can be brought back to life based on
    convert_par_to_py in the repository round  revision 1561.

    
    Given a par file, or THE_PARAM_T convert it to a .py file.

    Warning this is going to be a rough function, since I don't want
    to spend too much time on it. (This code is being used
    more than I thought it would - I'm concerned it's unit tests
    aren't up to scratch.)

    par_file_name: Name of the old style para file.
      The extension is changed to .py to get the output file name 
      eg 'risk.par' to 'risk.py'

    Output:
      A .py file, based on the par_file_name. eg 'risk.py'
    """
    pass 



# Warning, this is the old-style format
class write_python_par_file(object):
    def __init__(self, file_name, instance_name = VAR_NAME_IN_SET_DATA_FILE):
        """ Write a pthon parameter file
        """
        self.handle = open(file_name, 'w')
        self.var_name = instance_name

    def write_top(self):
        """ Write the imports ect. at the beginning of the par file
        """
 
        self.handle.write('"""\n')

        self.handle.write(SECOND_LINE)

        self.handle.write('\n\
  All input files are first searched for in the input_dir, then in the\n\
  resources/data directory, which is part of EQRM.\n\
\n\
 All distances are in kilometers.\n\
 Acceleration values are in g.\n\
 Angles, latitude and longitude are in decimal degrees.\n\
\n\
 If a field is not used, set the value to None.\n\
\n\
\n\
"""\n\
\n\
from eqrm_code.parse_in_parameters import Parameter_data\n\
from os.path import join\n\
\n')        
        self.handle.write(self.var_name + ' = Parameter_data()\n')

    def write_middle(self, para_data):
        """ Writes the attribute lines
        para_data: If this is a list of strings, write the strings to the file,
        adding the instance name at the beginning.
        """
        for line in para_data:
            if isinstance(line, list):
                if line[0] == 'input_dir' or line[0] == 'output_dir':
                    add_raw = 'r'
                else:
                    add_raw = ''
                self.handle.write(self.var_name + '.' + line[0] + ' = ' +
                                  add_raw +
                                  add_value(line[1]) + '\n')
            else:    
                self.handle.write(line)
                
            #self.handle.write('\n')
        
    def write_bottom(self):

        """ Write the end of the par file
        """
        self.handle.write("\n\
# If this file is executed the simulation will start\n\
if __name__ == '__main__':\n\
    from eqrm_code.analysis import main\n\
    main(")
        self.handle.write(self.var_name)
        self.handle.write(")\n")
        self.handle.close()
        

#class write_par_file(object):
class Write_no_instance_python_par_file(object):
    def __init__(self, file_name, instance_name = VAR_NAME_IN_SET_DATA_FILE):
        """ Write a python parameter file
        """
        self.handle = open(file_name, 'w')
        self.var_name = instance_name

    def write_top(self):
        """ Write the imports ect. at the beginning of the par file
        """
 
        self.handle.write('"""\n')

        self.handle.write(SECOND_LINE)

        self.handle.write('\n\
  All input files are first searched for in the input_dir, then in the\n\
  resources/data directory, which is part of EQRM.\n\
\n\
 All distances are in kilometers.\n\
 Acceleration values are in g.\n\
 Angles, latitude and longitude are in decimal degrees.\n\
\n\
 If a field is not used, set the value to None.\n\
\n\
\n\
"""\n\
\n\
from eqrm_code.parse_in_parameters import eqrm_data_home, get_time_user\n\
from os.path import join\n\
\n')        

    def write_middle(self, para_data):
        """ Writes the attribute lines
        para_data: If this is a list of strings, write the strings to the file,
        adding the instance name at the beginning.
        """
        for line in para_data:
            if isinstance(line, list):
                if line[0] == 'input_dir' or line[0] == 'output_dir':
                    add_raw = 'r'
                else:
                    add_raw = ''
                self.handle.write(line[0] + ' = ' +
                                  add_raw +
                                  add_value(line[1]) + '\n')
            else:    
                self.handle.write(line)
                
            #self.handle.write('\n')
        
    def write_bottom(self):

        """ Write the end of the par file
        """
        self.handle.write("\n\
# If this file is executed the simulation will start.\n\
# Delete all variables that are not EQRM parameters variables. \n\
if __name__ == '__main__':\n\
    from eqrm_code.analysis import main\n\
    main(locals())\n")
        self.handle.close()
        

def add_value(val):
    """Given a value of unknown type, write it in python syntax.
    """
    if isinstance(val, str):
        val_str = '"' + val + '" '
    else:
        if  isinstance(val, ndarray):
            val_str = str(val.tolist())
        elif isinstance(val, list) and isinstance(val[0], ndarray):
                # Assume all elements are ndarrays, with one element
                 val_str = str([x[0] for x in val])
                
        else:
            # bool, None
            if val == -999 or val == -9999 or val == 999 or val == 9999:
                val = None
            val_str = str(val) 
    return val_str
    
#-------------------------------------------------------------
if __name__ == "__main__":
    pass
