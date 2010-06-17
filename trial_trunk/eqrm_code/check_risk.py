"""This file automatically checks the risk.py code.

 Title: check_risk.py
 
Description: This file automatically checks the risk.py code. Several
.par files are generated.  These are used to run a deterministic risk
model using eqrm_code.analysis.  This produces loss and hazard files.

The hazard file is loaded to do the risk calculation using eqrm_code.risk.py.
This generates a loss file, which is compared to the original loss
file - if they are different the check fails.

 
  Version: $Revision: 1663 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-05-08 23:32:10 +1000 (Sat, 08 May 2010) $
  
  Copyright 2007 by Geoscience Australia
"""
import os
from os.path import join
import sys
import tempfile
import copy
import shutil
import csv
import scipy as num

from eqrm_code.analysis import main
from eqrm_code.risk import risk_main, multi_risk
from eqrm_code.parse_in_parameters import  Parameter_data, \
     create_parameter_data, convert_THE_PARAM_T_to_py
from eqrm_code.util import determine_eqrm_path, get_local_or_default, \
     del_files_dirs_in_dir
from eqrm_code.output_manager import EXTENSION, get_hazard_file_name
from eqrm_code.check_scenarios import file_diff, print_diff_results

    
def check_risk():
    """  Automatically check the risk.py code.
     This is assumed to be running in the eqrm_code dir
    """
    if True:
        files = create_set_data_files()
        c_failed = validate_risk(files)
    else:
        c_failed = 0
        files = []
    failed = check_multi_risk()
    c_failed += failed
    
    try:
        map(os.remove, files)
    except:
        pass
    files = [x + 'c' for x in files]
    try:
        map(os.remove, files)
    except:
        pass
    return c_failed
    
def validate_risk(scenarios):
    """
    Compare the results from running eqrm_code.analysis and eqrm_code.risk.
    scenarios - A list of .py full file paths
    """
    
    diff_results = []
    results = []

    for i,scenario in enumerate(scenarios):
        THE_PARAM_T = create_parameter_data(scenario)
        
        # Blow away files in both directories
        risk_save_dir = os.path.join("..","test_resources",
                                     "risk_seperated", "")
        files = os.listdir(risk_save_dir)
        files = [os.path.join(risk_save_dir,s) for s in files \
                 if s[-4:] == EXTENSION]
         # I'm getting this error;
        # WindowsError: [Error 13] The process cannot access the file because
        # it is being
        #used by another process:
        # '..\\test_resources\\risk_seperated/log.txt'
        try:
            map(os.remove, files)
        except WindowsError:
            pass
        
        files = os.listdir(THE_PARAM_T.output_dir)
        files = [os.path.join(THE_PARAM_T.output_dir,s) for s in files \
                 if s[-4:] == EXTENSION]

        # I'm getting this error;
        # WindowsError: [Error 13] The process cannot access the file because
        # it is being
        #used by another process:
        # '..\\test_resources\\hazard_seperated/log.txt'
        try:
            map(os.remove, files)
        except WindowsError:
            pass
        
        # Run the scenarios
        main(scenario, True)
        
        # Work out the risk_main parameters.
        #print "THE_PARAM_T", THE_PARAM_T
        eqrm_dir = determine_eqrm_path(__file__)
        THE_PARAM_T.default_input_dir = os.path.join(eqrm_dir, 'resources',
                                                   'data', '')
        site_file = 'sitedb_' + THE_PARAM_T.site_tag + '.csv'
        site_file = get_local_or_default(site_file,
                                         THE_PARAM_T.default_input_dir,
                                         THE_PARAM_T.input_dir)
        if THE_PARAM_T.use_site_indexes is True:
            site_ind = THE_PARAM_T.site_indexes
        else:
            site_ind = None

        if THE_PARAM_T.use_amplification == 0:
            hazard_name = 'bedrock_SA'
        else:
            hazard_name = 'soil_SA'

        # A hacky way of checking adding Mw manually
        if i == 0:
            Mw = float(THE_PARAM_T.determ_magnitude)
        else:
            Mw = None

        # A hacky way of checking loading the SA file
        if len(THE_PARAM_T.return_periods) == 3:
            pr = str(THE_PARAM_T.return_periods[0]).replace('.','pt').replace(' ','')
            file_full_name = os.path.join(THE_PARAM_T.output_dir,
                                          THE_PARAM_T.site_tag+ '_'+ \
                                          hazard_name+'_rp' + \
                                          pr + EXTENSION)
        else:
            file_full_name = None       

        # Check the hard coded values in risk are the same
        assert THE_PARAM_T.csm_hysteretic_damping == 'curve'
        assert THE_PARAM_T.atten_smooth_spectral_acceleration == 0
        assert THE_PARAM_T.atten_rescale_curve_from_pga == None
        if THE_PARAM_T.csm_use_variability is False:
            THE_PARAM_T.csm_variability_method == 3

        # Add more input info
        risk_loss_file_full_name, _ = risk_main(
            site_file,
            THE_PARAM_T.site_tag,
            risk_save_dir,
            hazard_saved_dir=THE_PARAM_T.output_dir,
            hazard_file_full_name=file_full_name,
            buildpars_flag=THE_PARAM_T.buildpars_flag,
            Mw=Mw,
            hazard_name=hazard_name,
            buildings_usage_classification=THE_PARAM_T.buildings_usage_classification,
            use_refined_btypes=(not THE_PARAM_T.hazus_btypes_flag),
            loss_aus_contents=THE_PARAM_T.loss_aus_contents,
            site_ind=site_ind,
            csm_SDcr_tolerance_percentage=THE_PARAM_T.csm_SDcr_tolerance_percentage,
            csm_damping_max_iterations=THE_PARAM_T.csm_damping_max_iterations,
            csm_damping_regimes =THE_PARAM_T.csm_damping_regimes,
            csm_damping_modify_Tav=THE_PARAM_T.csm_damping_modify_Tav,
            csm_damping_use_smoothing=THE_PARAM_T.csm_damping_use_smoothing,
            csm_standard_deviation=THE_PARAM_T.csm_standard_deviation,
            loss_min_pga=THE_PARAM_T.loss_min_pga,
            ci=THE_PARAM_T.loss_regional_cost_index_multiplier,
            buildings_set_damping_Be_to_5_percent=THE_PARAM_T.buildings_set_damping_Be_to_5_percent,
            csm_use_variability=THE_PARAM_T.csm_use_variability)

        # Let's check the files.
        # TODO catch the error of files not being produced.
        haz_loss_file_full_name = os.path.join(THE_PARAM_T.output_dir,
                                               'newc_total_building_loss.txt')
        # initaily assume files are produced
        #if not path.exists(risk_loss_file_full_name):
        is_same, lineA, lineB = file_diff(risk_loss_file_full_name,
                                          haz_loss_file_full_name)
        if is_same:
            results.append('.')
        else:
            results.append('F')
            diff_results.append((risk_loss_file_full_name, lineA, lineB))
    # finish scenario loop
    # Look at check scenarios to how this can be done well
    print
    print "Results" 
    for result in results:
        print result,
    print
    print "Checked %i files. %i failed." %(len(results), results.count('F'))
    print_diff_results(diff_results)
    return results.count('F')
 
def check_multi_risk():


    # Loop over scenarios and EQ's
    haz_string = '_hazard_ev'
    mag_string = '_Mw.txt'
    haz_output_dir = os.path.join("..","test_resources", "multi_hazard_output")
    risk_input_dir = os.path.join("..","test_resources", "multi_risk_input")
    risk_output_dir = os.path.join("..","test_resources", "multi_risk_output")

    for dir in [haz_output_dir, risk_input_dir, risk_output_dir]:
        del_files_dirs_in_dir(dir)
    set = get_simple_scenario()
    eq_mags = [8.3, 8.9]
    # These runs show how rounding errors can occur.
    #eq_mags = list(num.arange(4.9,5.2,0.1)) # no error  mw = 5.0
    #eq_mags = num.arange(4.5,6,0.1)  # error at 5
    #eq_mags = list(num.arange(4.5,6,0.1))  # error at 5 mw = 4.9999999999999982
    #eq_mags = list(num.arange(3,6,0.1)) # assert fail
    #eq_mags = list(num.arange(4.9,5.1,0.1)) # no error
    #eq_mags = list(num.arange(4,6,0.05)) # error at 20 Mw = ?
    #eq_mags = list(num.arange(4,6,0.1)) # error at 10  Mw = ?
    # eq_mags = list(num.arange(4,6.2,0.2)) # no error
    
    multi_run = []
    haz_SA_file_dirs = []
    haz_out_dirs = []
    for i,Mw in enumerate(eq_mags):
        new_set = copy.copy(set)
        another_set = copy.copy(set)
        new_set.determ_magnitude = Mw
        site_tag = new_set.site_tag
        #new_set.input_dir = risk_input_dir
        new_set.output_dir = haz_out_dir = os.path.join(haz_output_dir, str(i))
        haz_out_dirs.append(haz_out_dir)
        multi_run.append((Mw, new_set))
       
        # Run the scenarios
        main(new_set, True)
        
        SA_file_dir = os.path.join(haz_out_dir,
                               get_hazard_file_name(site_tag,
                             'soil_SA', set.return_periods[0]))
        # Copy the SA files, to be used as input
        haz_SA_file_dirs.append(SA_file_dir)
        SA_out_file_dir =  os.path.join(risk_input_dir,
                                        site_tag + haz_string +
                                        str(i) + EXTENSION)
        shutil.copyfile(SA_file_dir,
                        SA_out_file_dir)
        
    # Create a magnitude file
    mag_file_dir = os.path.join(risk_input_dir,site_tag + mag_string)
    file = open(mag_file_dir, 'wb')
    writer = csv.writer(file)
    for tup in multi_run:
        writer.writerow([tup[0]])
    file.close()
        
    THE_PARAM_T = create_parameter_data(another_set)
    return_dic = get_risk_parameters(THE_PARAM_T)
    # Check the hard coded values in risk are the same
    assert THE_PARAM_T.csm_hysteretic_damping == 'curve'    
    assert THE_PARAM_T.atten_smooth_spectral_acceleration == 0
    assert THE_PARAM_T.atten_rescale_curve_from_pga == None
    #if THE_PARAM_T.csm_use_variability is False:
     #   pass
        #THE_PARAM_T.csm_variability_method == 3
            
    saved_dirs = multi_risk(
        return_dic['site_file'],
        site_tag,
        risk_output_dir,
        mag_file_dir,
        hazard_saved_dir=risk_input_dir,
        buildings_usage_classification= \
        THE_PARAM_T.buildings_usage_classification,
        use_refined_btypes= \
        (not THE_PARAM_T.hazus_btypes_flag),
        loss_aus_contents=THE_PARAM_T.loss_aus_contents,
        site_ind=return_dic['site_ind'],
        csm_SDcr_tolerance_percentage=THE_PARAM_T.csm_SDcr_tolerance_percentage,
        csm_damping_regimes =THE_PARAM_T.csm_damping_regimes,
        csm_damping_modify_Tav=THE_PARAM_T.csm_damping_modify_Tav,
        csm_damping_use_smoothing=THE_PARAM_T.csm_damping_use_smoothing,
        csm_damping_max_iterations=THE_PARAM_T.csm_damping_max_iterations,
        csm_standard_deviation=THE_PARAM_T.csm_standard_deviation,
        loss_min_pga=THE_PARAM_T.loss_min_pga,
        ci=THE_PARAM_T.loss_regional_cost_index_multiplier,
        buildpars_flag=THE_PARAM_T.buildpars_flag,
        buildings_set_damping_Be_to_5_percent= \
        THE_PARAM_T.buildings_set_damping_Be_to_5_percent,
        csm_use_variability=THE_PARAM_T.csm_use_variability,
        #input_dir=None,
        csm_hysteretic_damping='curve')
    # Let's check the files.
    assert len(saved_dirs) == len(haz_out_dirs)
    diff_results = []
    results = []
    for saved_dir, haz_out_dir in map(None, saved_dirs, haz_out_dirs):
        # TODO catch the error of files not being produced.
        risk_loss_file_full_name = os.path.join(saved_dir,
                                                'newc_total_building_loss.txt')
        haz_loss_file_full_name = os.path.join(haz_out_dir,
                                               'newc_total_building_loss.txt')
        # initaily assume files are produced
        #if not path.exists(risk_loss_file_full_name):
        is_same, lineA, lineB = file_diff(risk_loss_file_full_name,
                                          haz_loss_file_full_name)
        if is_same:
            results.append('.')
        else:
            results.append('F')
            diff_results.append((risk_loss_file_full_name, lineA, lineB))
    # finish scenario loop
    # Look at check scenarios to how this can be done well
    print
    print "Results" 
    for result in results:
        print result,
    print
    print "Checked %i files. %i failed." %(len(results), results.count('F'))
    print_diff_results(diff_results)
    return results.count('F')

    #for file in haz_SA_file_dirs:
    #    os.remove(file)
        

def get_risk_parameters(THE_PARAM_T):
    return_dic = {}
    
    # Work out the risk_main parameters.
    #print "THE_PARAM_T", THE_PARAM_T
    eqrm_dir = determine_eqrm_path(__file__)
    THE_PARAM_T.default_input_dir = os.path.join(eqrm_dir, 'resources',
                                                 'data', '')
    site_file = 'sitedb_' + THE_PARAM_T.site_tag + '.csv'
    return_dic['site_file'] = get_local_or_default(
        site_file,
        THE_PARAM_T.default_input_dir,
        THE_PARAM_T.input_dir)
    if THE_PARAM_T.use_site_indexes == 1:
        return_dic['site_ind'] = THE_PARAM_T.site_indexes
    else:
        return_dic['site_ind'] = None
        
    if THE_PARAM_T.use_amplification == 0:
        return_dic['hazard_name'] = 'bedrock_SA'
    else:
        return_dic['hazard_name'] = 'soil_SA'
       
    return return_dic

        


            
def create_set_data_files():
    """
    Build a list of internally generated par files.
    """
    files = []
    files.append(create_par_file_simple_new())
    files.append(create_par_file_simpleII_new())
    files.append(create_par_file_simpleIII_new())
    files.append(create_par_file_var_with_build_capacity_curve_new())
    return files

def create_par_file_simple_new():
    sdp = Parameter_data()
    # Operation_Mode
    sdp.run_type = 'risk'
    sdp.is_deterministic = True    # If False, probabilistic input used
    
    # General
    sdp.use_site_indexes = True
    sdp.site_tag= 'newc'
    sdp.site_db_tag = ''
    sdp.site_indexes = [1,2,3,4,5,6]
    sdp.input_dir = os.path.join("..","implementation_tests", "input")
    sdp.output_dir = os.path.join("..","test_resources", "hazard_seperated")
    sdp.return_periods = [1,10]
    
    # Deterministic input 
    sdp.determ_azimith = 60
    sdp.determ_depth = 11.5
    sdp.determ_latitude = -32.95
    sdp.determ_longitude = 151.61
    sdp.determ_magnitude = 7.6
    sdp.determ_dip= 35
    sdp.determ_number_of_events = 1
    
    # Probabilistic input
    sdp.prob_azimuth_in_zones = [10]
    sdp.prob_min_mag_cutoff = 4.5 
    sdp.prob_number_of_mag_sample_bins = 15
    sdp.max_width = 15
    sdp.prob_number_of_events_in_zones = [5000]
    sdp.prob_delta_azimuth_in_zones = [5]
    sdp.prob_dip_in_zones = [35]
        
    #  Attenuation   
    sdp.atten_models = ['Gaull_1990_WA']
    sdp.atten_model_weights = [1.0]
    sdp.atten_aggregate_Sa_of_atten_models = False 
    sdp.atten_use_variability = False
    sdp.atten_variability_method = 2 
    sdp.atten_periods = [0, 0.5, 3.3333]
    sdp.atten_threshold_distance = 400
    sdp.atten_cutoff_max_spectral_displacement  = False
    sdp.atten_pga_scaling_cutoff = None  # None or a value
    sdp.atten_use_rescale_curve_from_pga = False
    sdp.atten_rescale_curve_from_pga = None # ('Aust_standard_Sa'|'HAZUS_Sa')
    sdp.atten_smooth_spectral_acceleration = False
    sdp.atten_log_sigma_eq_weight = 1.0
    
    #  Amplification  
    sdp.use_amplification = True  
    sdp.amp_use_variability = True
    sdp.amp_variability_method = 2 
    sdp.amp_min_factor = 0.6
    sdp.amp_max_factor = 10000
    
    # Buildings
    sdp.buildings_usage_classification = 'HAZUS'   # ('HAZUS'|'FCB')
    sdp.buildings_set_damping_Be_to_5_percent = True
    
    # Building capacity curve
    sdp.csm_use_variability = False
    sdp.csm_variability_method = 3
    sdp.csm_standard_deviation = 0.3
    sdp.csm_damping_regimes = 0       # (0|1|2) See manual for this
    sdp.csm_damping_modify_Tav = True 
    sdp.csm_damping_use_smoothing = True
    sdp.csm_hysteretic_damping = 'curve'    # ('curve'|'trapezoidal'|None)
    sdp.csm_SDcr_tolerance_percentage = 2
    sdp.csm_damping_max_iterations = 3
    
    # Loss
    sdp.loss_min_pga = 0.05 # May be a crap value to use
    sdp.loss_regional_cost_index_multiplier = 1.0
    sdp.loss_aus_contents = 0   # (0|1)
    
    #  Save
    sdp.save_hazard_map = True
    sdp.save_total_financial_loss = True
    sdp.save_building_loss = True
    sdp.save_contents_loss = True
    sdp.save_motion = False
    sdp.save_prob_structural_damage = False
    
    # Write .py file
    file, file_name = tempfile.mkstemp('check_risk.py', __name__+'_')
    os.close(file)
    file_name = convert_THE_PARAM_T_to_py(file_name, sdp)
    return file_name
        
def create_par_file_simpleII_new():
    sdp = Parameter_data()
    # Operation_Mode
    sdp.run_type = 'risk'
    sdp.is_deterministic = True    # If False, probabilistic input used
    
    # General
    sdp.use_site_indexes = True
    sdp.site_tag= 'newc'
    sdp.site_db_tag = ''
    sdp.site_indexes = [0,1,2]
    sdp.input_dir = os.path.join("..","implementation_tests", "input")
    sdp.output_dir = os.path.join("..","test_resources", "hazard_seperated")
    sdp.return_periods = [1,10]
    
    # Deterministic input 
    sdp.determ_azimith = 60
    sdp.determ_depth = 11.5
    sdp.determ_latitude = -32.95
    sdp.determ_longitude = 151.61
    sdp.determ_magnitude = 7.6
    sdp.determ_dip= 35
    sdp.determ_number_of_events = 1
    
    # Probabilistic input
    sdp.prob_azimuth_in_zones = [10]
    sdp.prob_min_mag_cutoff = 4.5 
    sdp.prob_number_of_mag_sample_bins = 15
    sdp.max_width = 15
    sdp.prob_number_of_events_in_zones = [5000]
    sdp.prob_delta_azimuth_in_zones = [5]
    sdp.prob_dip_in_zones = [35]
        
    #  Attenuation   
    sdp.atten_models = ['Toro_1997_midcontinent']
    sdp.atten_model_weights = [1.0]
    sdp.atten_aggregate_Sa_of_atten_models = False 
    sdp.atten_use_variability = False
    sdp.atten_variability_method = 2 
    sdp.atten_periods = [0, 0.5, 2.6, 3.3333]
    sdp.atten_threshold_distance = 400
    sdp.atten_cutoff_max_spectral_displacement  = False
    sdp.atten_pga_scaling_cutoff = None  # None or a value
    sdp.atten_use_rescale_curve_from_pga = False
    sdp.atten_rescale_curve_from_pga = None # ('Aust_standard_Sa'|'HAZUS_Sa')
    sdp.atten_smooth_spectral_acceleration = False
    sdp.atten_log_sigma_eq_weight = 1.0
    
    #  Amplification  
    sdp.use_amplification = True  
    sdp.amp_use_variability = True
    sdp.amp_variability_method = 2 
    sdp.amp_min_factor = 0.6
    sdp.amp_max_factor = 10000
    
    # Buildings
    sdp.buildings_usage_classification = 'HAZUS'   # ('HAZUS'|'FCB')
    sdp.buildings_set_damping_Be_to_5_percent = False
    
    # Building capacity curve
    sdp.csm_use_variability = False
    sdp.csm_variability_method = 3
    sdp.csm_standard_deviation = 0.5
    sdp.csm_damping_regimes = 0       # (0|1|2) See manual for this
    sdp.csm_damping_modify_Tav = False 
    sdp.csm_damping_use_smoothing = False
    sdp.csm_hysteretic_damping = 'curve'    # ('curve'|'trapezoidal'|None)
    sdp.csm_SDcr_tolerance_percentage = 1
    sdp.csm_damping_max_iterations = 7
    
    # Loss
    sdp.loss_min_pga = 0.05 # May be a crap value to use
    sdp.loss_regional_cost_index_multiplier = 1.0
    sdp.loss_aus_contents = 0   # (0|1)
    
    #  Save
    sdp.save_hazard_map = True
    sdp.save_total_financial_loss = True
    sdp.save_building_loss = True
    sdp.save_contents_loss = True
    sdp.save_motion = False
    sdp.save_prob_structural_damage = False
    
    # Write .py file
    file, file_name = tempfile.mkstemp('check_risk.py', __name__+'_')
    os.close(file)
    file_name = convert_THE_PARAM_T_to_py(file_name, sdp)
    return file_name
        
def create_par_file_simpleIII_new():
    sdp = Parameter_data()
    # Operation_Mode
    sdp.run_type = 'risk'
    sdp.is_deterministic = True    # If False, probabilistic input used
    
    # General
    sdp.use_site_indexes = True
    sdp.site_tag= 'newc'
    sdp.site_db_tag = ''
    sdp.site_indexes = [1,2,3]
    sdp.input_dir = os.path.join("..","implementation_tests", "input")
    sdp.output_dir = os.path.join("..","test_resources", "hazard_seperated")
    sdp.return_periods = [1,10,1000000]
    
    # Deterministic input 
    sdp.determ_azimith = 60
    sdp.determ_depth = 11.5
    sdp.determ_latitude = -32.95
    sdp.determ_longitude = 151.61
    sdp.determ_magnitude = 8.6
    sdp.determ_dip= 35
    sdp.determ_number_of_events = 1
    
    # Probabilistic input
    sdp.prob_azimuth_in_zones = [10]
    sdp.prob_min_mag_cutoff = 4.5 
    sdp.prob_number_of_mag_sample_bins = 15
    sdp.max_width = 15
    sdp.prob_number_of_events_in_zones = [5000]
    sdp.prob_delta_azimuth_in_zones = [5]
    sdp.prob_dip_in_zones = [35]
        
    #  Attenuation   
    sdp.atten_models = ['Gaull_1990_WA']
    sdp.atten_model_weights = [1.0]
    sdp.atten_aggregate_Sa_of_atten_models = False 
    sdp.atten_use_variability = False
    sdp.atten_variability_method = 2 
    sdp.atten_periods = [0.1, 3.3333]
    sdp.atten_threshold_distance = 400
    sdp.atten_cutoff_max_spectral_displacement  = False
    sdp.atten_pga_scaling_cutoff = None  # None or a value
    sdp.atten_use_rescale_curve_from_pga = False
    sdp.atten_rescale_curve_from_pga = None # ('Aust_standard_Sa'|'HAZUS_Sa')
    sdp.atten_smooth_spectral_acceleration = False
    sdp.atten_log_sigma_eq_weight = 1.0
    
    #  Amplification  
    sdp.use_amplification = False  
    sdp.amp_use_variability = True
    sdp.amp_variability_method = 2 
    sdp.amp_min_factor = 0.6
    sdp.amp_max_factor = 10000
    
    # Buildings
    sdp.buildings_usage_classification = 'HAZUS'   # ('HAZUS'|'FCB')
    sdp.buildings_set_damping_Be_to_5_percent = False
    
    # Building capacity curve
    sdp.csm_use_variability = False
    sdp.csm_variability_method = 3
    sdp.csm_standard_deviation = 0.3
    sdp.csm_damping_regimes = 1       # (0|1|2) See manual for this
    sdp.csm_damping_modify_Tav = True 
    sdp.csm_damping_use_smoothing = True
    sdp.csm_hysteretic_damping = 'curve'    # ('curve'|'trapezoidal'|None)
    sdp.csm_SDcr_tolerance_percentage = 2
    sdp.csm_damping_max_iterations = 3
    
    # Loss
    sdp.loss_min_pga = 0.05 # May be a crap value to use
    sdp.loss_regional_cost_index_multiplier = 1.45
    sdp.loss_aus_contents = 0   # (0|1)
    
    #  Save
    sdp.save_hazard_map = True
    sdp.save_total_financial_loss = True
    sdp.save_building_loss = True
    sdp.save_contents_loss = True
    sdp.save_motion = False
    sdp.save_prob_structural_damage = False
    
    # Write .py file
    file, file_name = tempfile.mkstemp('check_risk.py', __name__+'_')
    os.close(file)
    file_name = convert_THE_PARAM_T_to_py(file_name, sdp)
    return file_name

def create_par_file_var_with_build_capacity_curve_new():
    sdp = Parameter_data()
    # Operation_Mode
    sdp.run_type = 'risk'
    sdp.is_deterministic = True    # If False, probabilistic input used
    
    # General
    sdp.use_site_indexes = True
    sdp.site_tag= 'newc'
    sdp.site_db_tag = ''
    sdp.site_indexes = [0,1,2]
    sdp.input_dir = os.path.join("..","implementation_tests", "input")
    sdp.output_dir = os.path.join("..","test_resources", "hazard_seperated")
    sdp.return_periods = [1,10]
    
    # Deterministic input 
    sdp.determ_azimith = 60
    sdp.determ_depth = 11.5
    sdp.determ_latitude = -32.95
    sdp.determ_longitude = 151.61
    sdp.determ_magnitude = 8.6
    sdp.determ_dip= 35
    sdp.determ_number_of_events = 1
    
    # Probabilistic input
    sdp.prob_azimuth_in_zones = [10]
    sdp.prob_min_mag_cutoff = 4.5 
    sdp.prob_number_of_mag_sample_bins = 15
    sdp.max_width = 15
    sdp.prob_number_of_events_in_zones = [5000]
    sdp.prob_delta_azimuth_in_zones = [5]
    sdp.prob_dip_in_zones = [35]
        
    #  Attenuation   
    sdp.atten_models = ['Toro_1997_midcontinent']
    sdp.atten_model_weights = [1.0]
    sdp.atten_aggregate_Sa_of_atten_models = False 
    sdp.atten_use_variability = False
    sdp.atten_variability_method = 2 
    sdp.atten_periods = [0, 0.5, 2.6, 3.3333]
    sdp.atten_threshold_distance = 400
    sdp.atten_cutoff_max_spectral_displacement  = False
    sdp.atten_pga_scaling_cutoff = None  # None or a value
    sdp.atten_use_rescale_curve_from_pga = False
    sdp.atten_rescale_curve_from_pga = None # ('Aust_standard_Sa'|'HAZUS_Sa')
    sdp.atten_smooth_spectral_acceleration = False
    sdp.atten_log_sigma_eq_weight = 0.5
    
    #  Amplification  
    sdp.use_amplification = True  
    sdp.amp_use_variability = True
    sdp.amp_variability_method = 2 
    sdp.amp_min_factor = 0.6
    sdp.amp_max_factor = 10000
    
    # Buildings
    sdp.buildings_usage_classification = 'HAZUS'   # ('HAZUS'|'FCB')
    sdp.buildings_set_damping_Be_to_5_percent = False
    
    # Building capacity curve
    sdp.csm_use_variability = False
    sdp.csm_variability_method = 3
    sdp.csm_standard_deviation = 0.3
    sdp.csm_damping_regimes = 0       # (0|1|2) See manual for this
    sdp.csm_damping_modify_Tav = False 
    sdp.csm_damping_use_smoothing = False
    sdp.csm_hysteretic_damping = 'curve'    # ('curve'|'trapezoidal'|None)
    sdp.csm_SDcr_tolerance_percentage = 1
    sdp.csm_damping_max_iterations = 7
    
    # Loss
    sdp.loss_min_pga = 0.05 # May be a crap value to use
    sdp.loss_regional_cost_index_multiplier = 1.0
    sdp.loss_aus_contents = 0   # (0|1)
    
    #  Save
    sdp.save_hazard_map = True
    sdp.save_total_financial_loss = True
    sdp.save_building_loss = True
    sdp.save_contents_loss = True
    sdp.save_motion = False
    sdp.save_prob_structural_damage = False
    
    # Write .py file
    file, file_name = tempfile.mkstemp('check_risk.py', __name__+'_')
    os.close(file)
    file_name = convert_THE_PARAM_T_to_py(file_name, sdp)
    return file_name
        

def get_simple_scenario():
    sdp = Parameter_data()
    # Operation_Mode
    sdp.run_type = 'risk'
    sdp.is_deterministic = True   # If False, probabilistic input used
    
    # General
    sdp.use_site_indexes = True
    sdp.site_tag= 'newc'
    sdp.site_db_tag = ''
    sdp.site_indexes = [1,2,3,4,5,6]
    sdp.input_dir = os.path.join("..","implementation_tests", "input")
    sdp.output_dir = 'over written'
    sdp.return_periods = [1,10]
    
    # Deterministic input 
    sdp.determ_azimith = 20
    sdp.determ_depth = 11.5
    sdp.determ_latitude = -32.95
    sdp.determ_longitude = 151.61
    sdp.determ_magnitude = 5.
    sdp.determ_dip= 35
    sdp.determ_number_of_events = 1
    
    # Probabilistic input
    sdp.prob_azimuth_in_zones = [10]
    sdp.prob_min_mag_cutoff = 4.5 
    sdp.prob_number_of_mag_sample_bins = 15
    sdp.max_width = 15
    sdp.prob_number_of_events_in_zones = [5000]
    sdp.prob_delta_azimuth_in_zones = [5]
    sdp.prob_dip_in_zones = [35]
        
    #  Attenuation   
    sdp.atten_models = ['Gaull_1990_WA']
    sdp.atten_model_weights = [1.0]
    sdp.atten_aggregate_Sa_of_atten_models = False 
    sdp.atten_use_variability = False
    sdp.atten_variability_method = 2 
    sdp.atten_periods = [0,0.30303,1]
    sdp.atten_threshold_distance = 400
    sdp.atten_cutoff_max_spectral_displacement  = False
    sdp.atten_pga_scaling_cutoff = 4.3  # None or a value
    sdp.atten_use_rescale_curve_from_pga = False
    sdp.atten_rescale_curve_from_pga = None
    sdp.atten_smooth_spectral_acceleration = False
    sdp.atten_log_sigma_eq_weight = 1.0
    
    #  Amplification  
    sdp.use_amplification = True  
    sdp.amp_use_variability = False
    sdp.amp_variability_method = 2 
    sdp.amp_min_factor = 0.6
    sdp.amp_max_factor = 2
    
    # Buildings
    sdp.buildings_usage_classification = 'HAZUS'   # ('HAZUS'|'FCB')
    sdp.buildings_set_damping_Be_to_5_percent = False
    
    # Building capacity curve
    sdp.csm_use_variability = False
    sdp.csm_variability_method = 3
    sdp.csm_standard_deviation = 0.3
    sdp.csm_damping_regimes = 0       # (0|1|2) See manual for this
    sdp.csm_damping_modify_Tav = True 
    sdp.csm_damping_use_smoothing = True
    sdp.csm_hysteretic_damping = 'curve'    # ('curve'|'trapezoidal'|None)
    sdp.csm_SDcr_tolerance_percentage = 2
    sdp.csm_damping_max_iterations = 7
    
    # Loss
    sdp.loss_min_pga = 0.05 # May be a crap value to use
    sdp.loss_regional_cost_index_multiplier = 1.0
    sdp.loss_aus_contents = 0   # (0|1)
    
    #  Save
    sdp.save_hazard_map = True
    sdp.save_total_financial_loss = True
    sdp.save_building_loss = True
    sdp.save_contents_loss = True
    sdp.save_motion = False
    sdp.save_prob_structural_damage = True

    return sdp


# this will run if this file is called from DOS prompt or double clicked
if __name__ == '__main__':
    # This is assumed to be running in the eqrm_code dir
    c_failed = check_risk()
    sys.exit(c_failed) 
