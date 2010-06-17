"""
 Title: risk.py
 
  Author:   Duncan Gray, duncan.gray@ga.gov.au
             
  Description: Do the risk part of EQRM.  Load in the hazard information.
 
  Version: $Revision: 914 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-04-01 11:11:47 +1100 (Wed, 01 Apr 2009) $
  
  Copyright 2009 by Geoscience Australia
"""

import os
import csv

from scipy import array, zeros

from eqrm_code.util import determine_eqrm_path, add_last_directory
from eqrm_code.structures import Structures
from eqrm_code.structures import build_par_file
from eqrm_code.output_manager import load_hazards, load_event_set_subset, \
     save_ecloss, load_SA, save_damage, EXTENSION
from eqrm_code.damage_model import calc_total_loss
from eqrm_code.capacity_spectrum_model import Capacity_spectrum_model, \
     CSM_DAMPING_REGIMES_USE_ALL, CSM_DAMPING_MODIFY_TAV
from eqrm_code.capacity_spectrum_functions import CSM_DAMPING_USE_SMOOTHING

from eqrm_code.ANUGA_utilities import log

class Error(Exception):
    """Base exception for all exceptions raised in parse_in_parameters."""
    pass

class ParameterError(Error):
    """There is an Error in the parameters."""
    pass

class Dummy:
    def __init__(self):
        pass
    
def risk_main(site_file,
              site_tag,
              risk_save_dir,
              hazard_file_full_name=None,
              hazard_saved_dir=None,
              Mw=None,
              hazard_name='soil_SA',
              #main_dir=None,
              buildings_usage_classification='HAZUS',
              use_refined_btypes=True,
              loss_aus_contents=0,
              site_ind=None,
              #atten_smooth_spectral_acceleration=0,
              csm_SDcr_tolerance_percentage=1,
              csm_damping_max_iterations=7,
              csm_standard_deviation=0.3,
              csm_damping_regimes=CSM_DAMPING_REGIMES_USE_ALL,
              csm_damping_modify_Tav=CSM_DAMPING_MODIFY_TAV,
              csm_damping_use_smoothing=CSM_DAMPING_USE_SMOOTHING,
              loss_min_pga=0.05,
              ci=1.0,
              buildpars_flag=4, # WARNING 4 is the only value tested
              buildings_set_damping_Be_to_5_percent=False,
              csm_use_variability=False,
              input_dir=None,
              csm_hysteretic_damping='curve'):
    """
    Calculate the risk and structural damage given a single event and
    a hazard map at the structures of interest.
    The hazard map gives SA per site and period.
    
    site_file - The path and file name of the site file,
                or a handle to the file.
    
    site_tag - string used to define the site of interest, e.g. newc.

    hazard_saved_dir - The directory the hazard files are in.

    risk_save_dir - The directory the risk files will be saved to.

    hazard_file_full_name - The file and path of the hazard file.
    
    Mw - Magnitude of the earthquake.  If not given it will be loaded from
         the event file. Given as a float.

    hazard_name - used to determine the SA file name. 'soil_SA' or 'bedrock_SA'

    buildings_usage_classification - The building usage classification system.
                        1 for HAZUS usage classification
                        2 for FCB usage classification
                        
    use_refined_btypes - The building construction classification system.
                        0 for HAZUS classification
                        1 for refined HAZUS classification

    loss_aus_contents - Double the contents cost fraction for being in
                        each damage state
    
    site_indexes - If this is None all of the sites in the site file are
    loaded. If it is a list only use the listed sites.  The list is
    the index if the sites to use. The first site is index 1.

    csm_SDcr_tolerance_percentage - Tolerance as a percentage for SDcr,
      in non-linear damping calculations.
    
    csm_damping_regimes - damping multiplicative formula to use
      damage model. 0,1 or 2.  0 is preferred.
      
    csm_damping_modify_Tav - Modify transition building period.
      True to modify as in HAZUS

    csm_damping_use_smoothing - True to smooth damped curve.

    csm_damping_max_iterations - maximum iterations for nonlinear
    damping calculations.

    csm_standard_deviation - standard deviation for capacity curve log normal
      PDF.

    loss_min_pga - minimum PGA(g) below which financial loss is
    assigned to zero.

    ci - Regional cost index multiplier to convert dollar values in
    building database to desired regional and temporal
    (i.e. inflation) values.
    
    buildpars_flag - Engineering parameters to be used:
    0     Australian Engineers Workshop Parameters (AEWP) with Edwards
                            modifications 1;
    1     AEWP;
    2     original HAZUS paramaters;
    3     AEWP with Edwards modifications 2; 
    4     AEWP with Edwards modifications 3.
    If a string is passed the engineering parameters used are assumed to
    be in the file; building_parameters_demo_[buildpars_flag]_params.csv
    This file has to be in the resources\data directory.

    buildings_set_damping_Be_to_5_percent - Level of damping when
      buildpars_flag is 2.
    0   Use damping from the structure classification file. 
    1  Use 5% damping.

    csm_use_variability - Variability with building capacity curve
    0  Variability not included
    1  Variability included

    input_dir - The location where input files are loaded from.
      If a file is not found here it is loaded from the
      default_input_dir, which is resources/data
    
    In the SA the period axis must have 2 or more values.
    """
     # Set up the logging
    log.console_logging_level = log.INFO
    log.file_logging_level = log.DEBUG
    log_filename = os.path.join(risk_save_dir,
                                'log.txt')
    log.log_filename = log_filename
    log.set_log_file(log_filename)
    
    #if main_dir is None:
    main_dir = determine_eqrm_path()   
    default_input_dir = os.path.join(main_dir, 'resources',
                         'data', '')
    building_par_file = build_par_file(buildpars_flag)    
    # load site info.
    if isinstance(site_file, Structures):
        all_sites = site_file
    else:
        all_sites = Structures.from_csv(
            site_file,
            building_par_file,
            default_input_dir,
            input_dir=input_dir,
            eqrm_dir=main_dir,
            buildings_usage_classification=buildings_usage_classification,
            use_refined_btypes=use_refined_btypes,
            force_btype_flag=False,
            loss_aus_contents=loss_aus_contents)
        if site_ind is not None:
            all_sites = all_sites[site_ind-1]

        # Hard wires the Demmand Curve damping to 5%
        if buildings_set_damping_Be_to_5_percent:
            all_sites.building_parameters['damping_Be']=(
                0.05+0*all_sites.building_parameters['damping_Be'])
    
    # load SA - should be able to do currently.
    if hazard_file_full_name is None:
        if hazard_saved_dir is None:
            raise ParameterError(
                "Need a hazard_file_full_name"
                " or hazard_saved_dir parameter value.")
        else:       
            SA, periods, _ = load_hazards(hazard_saved_dir,
                                          site_tag,
                                          hazard_name)
    else:
        SA, periods = load_SA(hazard_file_full_name)
        
    # SA has the axis site, period, return_p
    # load event set Mw - This has to be before it is collapsed.
    # If an array is colapsed or not is not currently checked.
    if Mw is None:
        if hazard_saved_dir is None:
            raise ParameterError(
            "Need a Mw or hazard_saved_dir parameter value.")
        else:
            dic = load_event_set_subset(hazard_saved_dir,
                                        site_tag)
            Mw = dic['Mw'] # per event
            event_activity = dic['event_activity'] # per event
    else: 
        Mw = array([Mw])
        event_activity = array([1.0])
        
    # do some assertions
    assert len(Mw) == len(event_activity) == 1
    assert event_activity[0] == 1.0 # 

    # Build the param_T file
    THE_PARAM_T=Dummy()
    THE_PARAM_T.atten_periods = array(periods)
    
    # Inital, less flexable function.
    THE_PARAM_T.csm_use_variability = csm_use_variability
    
    # 1 is not implemented, 2 contains an error
    THE_PARAM_T.csm_variability_method = 3
    THE_PARAM_T.csm_hysteretic_damping = csm_hysteretic_damping
    THE_PARAM_T.csm_SDcr_tolerance_percentage = csm_SDcr_tolerance_percentage
    THE_PARAM_T.csm_damping_max_iterations = csm_damping_max_iterations
    THE_PARAM_T.csm_damping_regimes = csm_damping_regimes
    THE_PARAM_T.csm_damping_modify_Tav = csm_damping_modify_Tav
    THE_PARAM_T.csm_damping_use_smoothing = csm_damping_use_smoothing
    THE_PARAM_T.csm_standard_deviation = csm_standard_deviation

    # Inital, less flexable function.
    THE_PARAM_T.atten_rescale_curve_from_pga = None

    # Inital, less flexable function.
    THE_PARAM_T.atten_cutoff_max_spectral_displacement = None 
    THE_PARAM_T.loss_min_pga = loss_min_pga
    THE_PARAM_T.loss_regional_cost_index_multiplier = ci
    THE_PARAM_T.loss_aus_contents = loss_aus_contents
    THE_PARAM_T.output_dir = risk_save_dir
    THE_PARAM_T.site_tag = site_tag

    array_size = len(all_sites)
    
    total_building_loss = zeros((array_size, 1), dtype=float)
    building_loss = zeros((array_size,1), dtype=float)
    contents_loss = zeros((array_size, 1), dtype=float)
    
    # total_structure_damage axis sites, damage_states
    total_structure_damage = zeros((array_size, 4), dtype=float)
    
    # loop over sites
    for i in range(array_size):
        print 'do site ',i+1,' of ', array_size        
        sites=all_sites[i:i+1] # take site i
        SA_slice =  SA[i,:,0] # 0, so only looking at the first return_p data
        #print "SA_slice", SA_slice
        SA_slice.shape = 1,1,-1
        #print "Mw", Mw
        # smooth SA (function of periods) using a weighted
        # running 3-point smoother
        # I've taken this out, since it is not tested in the imp tests
        if False and atten_smooth_spectral_acceleration is True:
            SA_slice[:,:,1:-2] = (0.25*SA_slice[:,:,0:-3]+
                            0.50*SA_slice[:,:,1:-2]+
                            0.25*SA_slice[:,:,2:-1])
        # A lot is done here. the function is in eqrm_code.damage_model
        total_loss, damage = calc_total_loss(sites,SA_slice,THE_PARAM_T,
                                     array(Mw))
        #print "risk total_loss",total_loss

        # break loss tuple into components
        # structure_loss = structural loss
        # nsd_loss = non-structural drift sensitive loss
        # accel_loss = non-structural acceleration  sensitive loss
        # con_loss = contents loss
        structure_loss,nsd_loss,accel_loss,con_loss=total_loss

        total_building_loss[i,:]=(structure_loss+nsd_loss+
                                      accel_loss+con_loss)[0,:]
        building_loss[i,:]=( \
                        structure_loss+nsd_loss+accel_loss)[0,:]
        contents_loss[i,:]=con_loss[0,:]
        total_structure_damage[i,:] = damage.structure_state
    # End loop over sites

    # not doing do_collapse_logic_tree
    
    ecloss_file_full_name = save_ecloss(
        '_total_building', THE_PARAM_T, total_building_loss, all_sites)
    save_ecloss('_building', THE_PARAM_T, building_loss, all_sites)
    save_ecloss('_contents', THE_PARAM_T, contents_loss, all_sites)
    struct_damage_file_full_name = save_damage(risk_save_dir,
                                               site_tag,
                                               'structural',
                                               total_structure_damage,
                                               all_sites.attributes['BID'],
                                               compress=False)

    log.remove_file_handler()
    return ecloss_file_full_name, all_sites

def multi_risk(site_file,
               site_tag,
               risk_save_dir,
               Mw_file,
               hazard_saved_dir=None,
               buildings_usage_classification='HAZUS',
               use_refined_btypes=True,
               loss_aus_contents=0,
               site_ind=None,
               csm_SDcr_tolerance_percentage=1,               
               csm_damping_regimes=0,
               csm_damping_modify_Tav=True,
               csm_damping_use_smoothing=True,
               csm_damping_max_iterations=7,
               csm_standard_deviation=0.3,
               loss_min_pga=0.05,
               ci=1.0,
               buildpars_flag=4,
               buildings_set_damping_Be_to_5_percent=False,
               csm_use_variability=False,
               input_dir=None,
               csm_hysteretic_damping='curve'):
    """
    Calculate the risk and structural damage given multiple events and
    a hazard map for each event at the structures of interest.
    The hazard map gives SA per site and period.

    This function calls risk_main.  See the comments in risk main
    for parameter definitions.

    The harard files are assumed to be in the hazard_saved_dir folder.
    The hazard files have the format [site_tag]_hazard_ev[event_id].txt
    The event_id must be 0, 1, 2 etc, corresponding to the rows in the
      earthquake magnitude file.
    
    Mw_file_dir - The path and name of the earthquake magnitude file.

    """
    extension = '.txt'
    beginning = site_tag + '_' + 'hazard' + '_ev'
    ev_start_index = len(beginning)
    ev_end_index = -(len(extension))
    files = os.listdir(hazard_saved_dir)
    files = [s for s in files if s.startswith(beginning)and \
               s[-4:] == EXTENSION]
    file_dic = {}
    for file in files:
        event_tag = file[ev_start_index:ev_end_index]
        file_dic[int(event_tag)] = file

    keys = file_dic.keys()
    keys.sort()
    assert keys == range(len(keys))
    files = [file_dic[key] for key in keys]
    mw_reader = csv.reader(open(Mw_file, "rb"))
    Mws = [float(x[0]) for x in mw_reader]
    assert len(Mws) == len(files)

    # Let's run risk once, for each event
    # Putting output in a folder in the output_dir
    i = 0
    event_risk_save_dirs = []
    for event, Mw in map(None, files, Mws):
        # Let's get the event tag
        event_tag = event[ev_start_index:ev_end_index]
        hazard_file_full_name = os.path.join(hazard_saved_dir, event)
        event_risk_save_dir = os.path.join(risk_save_dir, str(i))
        event_risk_save_dirs.append(event_risk_save_dir)
        i += 1
        add_last_directory(event_risk_save_dir)
        # Site_file can be a closed handle,
        # which needs to be changed
        try:
            if site_file.closed:
                site_file = site_file.name
        except AttributeError:
            pass
        _, all_sites = risk_main(
            site_file,
            site_tag,
            event_risk_save_dir,
            hazard_file_full_name=hazard_file_full_name,
            Mw=Mw,
            buildings_usage_classification=buildings_usage_classification,
            use_refined_btypes=use_refined_btypes,
            loss_aus_contents=loss_aus_contents,
            site_ind=site_ind,
            csm_SDcr_tolerance_percentage=csm_SDcr_tolerance_percentage,
            csm_damping_regimes=csm_damping_regimes,
            csm_damping_modify_Tav=csm_damping_modify_Tav,
            csm_damping_use_smoothing=csm_damping_use_smoothing,
            csm_damping_max_iterations=csm_damping_max_iterations,
            csm_standard_deviation=csm_standard_deviation,
            loss_min_pga=loss_min_pga,
            ci=ci,
            buildpars_flag=buildpars_flag,
            buildings_set_damping_Be_to_5_percent= \
            buildings_set_damping_Be_to_5_percent,
            csm_use_variability=csm_use_variability,
            input_dir=input_dir,
            csm_hysteretic_damping=csm_hysteretic_damping)
        site_file = all_sites # So the site file is only loaded once
    return event_risk_save_dirs
    
    
# this will run if eqrm_analysis.py is called from DOS prompt or double clicked
if __name__ == '__main__':
    risk()
