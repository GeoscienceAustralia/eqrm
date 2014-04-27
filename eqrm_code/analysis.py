"""
 Title: analysis.py

  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, duncan.gray@ga.gov.au

  Description: The main program of EQRMA. Reads in .par files to do
  simulations. See README-getting-started.txt for information on how
  to use this module.

  Version: $Revision: 1666 $
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-05-10 23:21:10 +1000 (Mon, 10 May 2010) $

  Copyright 2007 by Geoscience Australia
"""

import os
import time
import shutil
import copy
import datetime
import sys
platform = sys.platform

from scipy import where, newaxis, array, isfinite, zeros, \
    arange, reshape, tile, ravel

from eqrm_code.parse_in_parameters import  \
    AttributeSyntaxError, create_parameter_data, eqrm_flags_to_control_file
from eqrm_code.event_set import create_event_set
from eqrm_code.ground_motion_interface import BEDROCKVs30
from eqrm_code.regolith_amplification_model import get_soil_SA, \
    Regolith_amplification_model, load_site_class2Vs30
from eqrm_code.output_manager import save_motion_to_binary, save_distances, \
    save_sites_to_csv, save_sites_to_binary, \
    save_hazard, save_structures, save_val, save_ecloss, \
    join_parallel_files, join_parallel_files_column, \
    join_parallel_data_files, \
    save_damage, save_fatalities, \
    save_bridge_days_to_complete
from eqrm_code.util import reset_seed, determine_eqrm_path, \
    get_local_or_default, add_last_directory
from .ground_motion_distribution import Distribution_Log_Normal, \
    GroundMotionDistributionLogNormal
from eqrm_code.structures import Structures
from eqrm_code.structures_vulnerability import Structures_Vulnerability
from eqrm_code.exceedance_curves import hzd_do_value, \
    collapse_att_model, collapse_source_gmms
from eqrm_code.sites import Sites, truncate_sites_for_test
from eqrm_code.parallel import Parallel
from eqrm_code.ANUGA_utilities import log
from eqrm_code.bridges import Bridges
from . import eqrm_filesystem as eq_fs
from eqrm_code.RSA2MMI import rsa2mmi_array
from eqrm_code.fatalities import forecast_fatality
from eqrm_code.filters import source_model_threshold_distance_subset
from eqrm_code.analysis_data import Analysis_Data

logs_per_scenario_con = 10


def main(parameter_handle,
         use_determ_seed=True,
         compress_output=False,
         eqrm_dir=None,
         is_parallel=True,
         parallel_finalise=True):
    """Script to run eqrm program.

    The parameters are defined by the parameter_handle.
    If is either a file name, dictionary of the parameters or
    an object with the parameters as attributes.
    See new_param_list.pdf in Documentation for details on the parameters.

    If use_determ_seed is True, then a hardwired seed is used
    (so that results can be replicated). If use_determ_seed is
    False, then the random seeds are reset based on time.

    If compress_output == True (True, 1, etc), output will be
    in the form output_file.txt.gz - a gzip file containing
    output_file.txt

    eqrm_dir: The directory which 'eqrm_code' and 'resources' reside.
    """
    t0 = t0_clock = time.clock()
    t0_time = time.time()

    # Let's work-out the eqrm dir
    if eqrm_dir is None:
        eqrm_dir = determine_eqrm_path(__file__)

    # Get an object that holds all the parameters in parameter_handle.
    # Note that arrays and floating point numbers will be converted,
    # everthing else will be a string.
    try:
        eqrm_flags = create_parameter_data(
            parameter_handle,
            default_input_dir=os.path.join(eqrm_dir,
                                           eq_fs.Resources_Data_Path),
            use_determ_seed=use_determ_seed,
            compress_output=compress_output,
            eqrm_dir=eqrm_dir,
            is_parallel=is_parallel)
    except AttributeSyntaxError as e:
        print 'File parameter error:', e
        import sys
        sys.exit(1)
        # FIXME throw error to catch

    del use_determ_seed
    del compress_output
    del eqrm_dir
    del is_parallel

    # Reset random seeds if required
    # If use_determ_seed is True, then use a hardwired seed.
    # If use_determ_seed is False, set random seeds based on time.
    reset_seed(eqrm_flags.use_determ_seed)

    # Setting up parallelisation
    parallel = Parallel(eqrm_flags.is_parallel)

    # Make the output dir, if it is not present
    if parallel.rank == 0:
        # print "Creating last directory, processor", parallel.rank
        add_last_directory(eqrm_flags.output_dir)

    # copy input parameter file to output directory.
        if isinstance(parameter_handle, str) and parameter_handle[-3:] == '.py':
            shutil.copyfile(parameter_handle,
                            eqrm_flags.output_dir + 'eqrm_flags.py')
        else:
            para_instance = copy.deepcopy(eqrm_flags)
            eqrm_flags_to_control_file(
                os.path.join(eqrm_flags.output_dir, 'eqrm_flags.py'),
                para_instance)
    parallel.barrier()

    # Set up the logging
    # Use defaults.
    #log.console_logging_level = log.INFO
    #log.file_logging_level = log.DEBUG
    log_filename = os.path.join(eqrm_flags.output_dir,
                                'log' + parallel.log_file_tag + '.txt')
    log.log_filename = log_filename
    log.remove_log_file()
    if parallel.rank == 0:
        log.set_log_level(eqrm_flags.file_log_level,
                          eqrm_flags.console_log_level)
    else:
        log.set_log_level(eqrm_flags.file_parallel_log_level,
                          eqrm_flags.console_parallel_log_level)
    log.set_log_file(log_filename)
    log.log_json({log.PARALLELSIZE_J: parallel.size}, log.INFO)
    log.log_json({log.HOSTNAME_J: parallel.node}, log.INFO)
    log.log_json({log.PLATFORM_J: platform}, log.INFO)
    log.log_eqrm_flags_simple(eqrm_flags)

    log.log_svn()
    log.debug('Memory: Initial')
    log.resource_usage(tag=log.INITIAL_J)

    # load event set data
    (event_set, event_activity, source_model) = create_event_set(eqrm_flags,
                                                                 parallel)

    # load all data into a 'sites' object
    # if we have bridge data, 'have_bridge_data' will be True
    sites = load_data(eqrm_flags)

    # if required, 'thin' sites for testing
    all_sites = truncate_sites_for_test(eqrm_flags.use_site_indexes, sites,
                                        eqrm_flags.site_indexes)

    # Save sites to numpy array
    if parallel.rank == 0:
        save_sites_to_binary(eqrm_flags.output_dir,
                             eqrm_flags.site_tag,
                             sites=all_sites)

    del sites
    num_sites = len(all_sites)

    log.info('P%s: Sites set created. Number of sites=%s' % (parallel.rank,
                                                             str(num_sites)))
    log.debug('Memory: Sites created')
    log.resource_usage()

    num_gmm_max = source_model.get_max_num_atten_models()
    log.log_json({log.MAXGMPE_J: num_gmm_max}, log.INFO)
    num_events = len(event_set)
    num_spawning = eqrm_flags.atten_spawn_bins

    num_pseudo_events = num_gmm_max * num_events * num_spawning
    num_rm = event_activity.recurrence_model_count()
    log.log_json({log.RECMOD_J: num_rm}, log.INFO)

    ground_motion_distribution = GroundMotionDistributionLogNormal(
        eqrm_flags.atten_variability_method,
        eqrm_flags.atten_spawn_bins,
        num_rm)

    event_activity.spawn(ground_motion_distribution.spawn_weights)

    log.log_json({log.PSEUDOEVENTS_J: num_pseudo_events}, log.INFO)
    log.debug('Memory: Pseudo Event Set created')
    log.resource_usage()

    # Initialise the ground motion object
    # Tasks here include
    #  - interpolation of coefficients to periods of interest

    # load in soil amplifications factors
    # searches input_dir then defaultdir
    if eqrm_flags.use_amplification is True:
        amp_distribution = Distribution_Log_Normal(
            eqrm_flags.amp_variability_method)

        amp_factor_file = eqrm_flags.site_tag + '_par_ampfactors.xml'
        amp_factor_file = get_local_or_default(amp_factor_file,
                                               eqrm_flags.default_input_dir,
                                               eqrm_flags.input_dir)
        soil_amplification_model = \
            Regolith_amplification_model.from_xml(
                amp_factor_file.name)
    else:
        soil_amplification_model = None
        amp_distribution = None

    # This is where info should be given to all the subprocesses.
    # But what info is there?
    # Also, let's do some timings.
    time_taken_pre_site_loop = (time.clock() - t0)

    # parallelising over the site loop.
    parallel.calc_lo_hi(num_sites)
    all_sites = all_sites[parallel.calc_indices(num_sites)]
    num_site_block = len(all_sites)
    msg = ('blocking over sites if running in parallel. block_size=' +
           str(num_site_block))
    log.debug(msg)
    log.log_json({log.BLOCKSITES_J: num_site_block}, log.DEBUG)

    msg = 'Number of atten_periods=' + str(len(eqrm_flags.atten_periods))
    log.debug(msg)

    if eqrm_flags.use_amplification is True:
        log.log_json({log.SASURFACES_J: 2}, log.DEBUG)
    else:
        log.log_json({log.SASURFACES_J: 1}, log.DEBUG)

    # initialise some matrices.  These matrices have a site dimension and
    # are filled while looping over sites.  Whether they are needed or
    # not often depends on what is being saved.

    data = Analysis_Data()

    if eqrm_flags.save_hazard_map is True:
        data.bedrock_hazard = zeros((num_site_block,
                                     len(eqrm_flags.atten_periods),
                                     len(eqrm_flags.return_periods)),
                                    dtype=float)

        log.log_json({log.BEDROCKHAZ_J: data.bedrock_hazard.nbytes},
                     log.DEBUG)
    else:
        data.bedrock_hazard = None

    if eqrm_flags.save_hazard_map is True and \
            eqrm_flags.use_amplification is True:
        data.soil_hazard = zeros((num_site_block,
                                  len(eqrm_flags.atten_periods),
                                  len(eqrm_flags.return_periods)),
                                 dtype=float)
        log.log_json({log.SOILHAZ_J: data.soil_hazard.nbytes},
                     log.DEBUG)
    else:
        data.soil_hazard = None
    log.debug('Memory: hazard_map array created')
    log.resource_usage()
    num_gmm_dimensions = event_activity.get_gmm_dimensions()

    log.log_json({log.EVENTACTIVITY_J: event_activity.get_bytes()},
                 log.DEBUG)
    if eqrm_flags.save_motion is True:
        data.bedrock_SA_all = zeros((num_spawning, num_gmm_dimensions, num_rm,
                                     num_site_block, num_events,
                                     len(eqrm_flags.atten_periods)),
                                    dtype=float)
        log_dic = {"cra_site_block": num_site_block,
                   "cra_spawning": num_spawning,
                   "cra_num_gmm_dimensions_motion": num_gmm_dimensions,
                   "cra_num_rm": num_rm,
                   "cra_num_events": num_events,
                   "cra_return_periods": len(eqrm_flags.return_periods)}
        log.log_json(log_dic,
                     log.DEBUG)
        log.log_json({log.BEDROCKALL_J: data.bedrock_SA_all.nbytes},
                     log.DEBUG)
    else:
        data.bedrock_SA_all = None

    if eqrm_flags.save_motion is True and \
            eqrm_flags.use_amplification is True:
        data.soil_SA_all = zeros((num_spawning, num_gmm_dimensions, num_rm,
                                  num_site_block, num_events,
                                  len(eqrm_flags.atten_periods)),
                                 dtype=float)
        log.log_json({log.SOILALL_J: data.soil_SA_all.nbytes},
                     log.DEBUG)
    else:
        data.soil_SA_all = None
    log.debug('Memory: save_motion array created')
    log.resource_usage()

    if eqrm_flags.save_fatalities is True:
        total_fatalities = zeros((num_site_block, num_pseudo_events),
                                 dtype=float)

    if eqrm_flags.save_total_financial_loss is True:
        total_building_loss_qw = zeros((num_site_block, num_spawning,
                                        num_gmm_max, num_rm, num_events),
                                       dtype=float)
    if eqrm_flags.save_building_loss is True:
        building_loss_qw = zeros((num_site_block, num_spawning,
                                  num_gmm_max, num_rm, num_events),
                                 dtype=float)
    if eqrm_flags.save_contents_loss is True:
        contents_loss_qw = zeros((num_site_block, num_spawning,
                                  num_gmm_max, num_rm, num_events),
                                 dtype=float)
    if (eqrm_flags.save_prob_structural_damage is True and
            num_pseudo_events == 1):
        # total_structure_damage, given as a non-cumulative
        # probability. The axis are  sites, model_generated_psudo_events,
        # damage_states
        # (the damage_states are slight, moderate, extensive and complete.
        # subtract all of these from 1 to get the prob of no damage.)
        total_structure_damage = zeros((num_site_block, 4), dtype=float)

    # create result array to save 'days to complete' data
    # need to store 'fp' days + state field

    if eqrm_flags.bridges_functional_percentages is not None:
        saved_days_to_complete = zeros((
            num_site_block, num_pseudo_events,
            len(eqrm_flags.bridges_functional_percentages)))

    log.debug('Memory: Created all data collection arrays.')
    log.resource_usage()

    # if we're doing fatality calculation
    # check the attenuation period is 1.0 seconds and only 1 dimension
    if eqrm_flags.run_type == "fatality":
        if not ((len(eqrm_flags.atten_periods) == 1) and
                (eqrm_flags.atten_periods[0] == 1.0)):
            msg = "Attenuation period should be [1.0] for fatality calculation"
            raise RuntimeError(msg)

    for i in xrange(num_site_block):
        rel_i = i  # - parallel.lo
        msg = 'P%i: do site ' % parallel.rank + str(i + 1) + ' of ' + \
            str(num_site_block)
        log.info(msg, logs_per_scenario=logs_per_scenario_con, site=rel_i,
                 sites=num_site_block)

        log.debug('Memory: site ' + str(i + 1),
                  logs_per_scenario=logs_per_scenario_con,
                  site=rel_i,
                  sites=num_site_block)
        log.resource_usage(tag=log.LOOPING_J,
                           logs_per_scenario=logs_per_scenario_con,
                           site=rel_i,
                           sites=num_site_block)

        sites = all_sites[i:i + 1]  # take site i
        distances = sites.distances_from_event_set(event_set)

        ### HAZARD CALCULATIONS ###

        # note if you take sites[i], it will collapse the dimension

        # By not collapsing sites, and making the assignment
        # sites=all_sites[i:i+1], the code will work with a single site
        # at a time, without multiple reference to the loop variable 'i'.

        # This also means that the code below will deal with a vectorized
        # sites without any modification.
        # To remove loop over sites, just disable the loop
        # and remove the 'sites=all_sites[i:i+1]'.
        # and change NUM_SITES_PER_SITE_LOOP

        # CAUTIONS on doing multiple sites in a loop:
        #  1.  this will run out of memory if sites*events is large.
        #  2.  this has not been tested recently
        #  3.  it absolutely will not work

        # A source model subset - each event reference in the source model
        # meets the attenuation threshold criteria i.e.
        # This subset only has close events
        source_model_subset = source_model_threshold_distance_subset(
            distances,
            source_model,
            eqrm_flags.atten_threshold_distance)

        soil_SA, bedrock_SA = calc_and_save_SA(
            eqrm_flags,
            sites,
            event_set,
            distances,
            data.bedrock_SA_all,
            data.soil_SA_all,
            data.bedrock_hazard,
            data.soil_hazard,
            soil_amplification_model,
            i,
            rel_i,
            ground_motion_distribution,
            amp_distribution,
            event_activity,
            source_model_subset,
            num_site_block)

        # soil_SA and bedrock_SA dimensions
        # (num_sites, num_events*num_gmm_max*num_spawn*num_rm, num_periods)
        # soil_SA can also be None

        ### POST-HAZARD SETUP ###

        # Decide which SA to use post-hazard
        if soil_SA is not None:
            SA = soil_SA
        else:
            SA = bedrock_SA

        # smooth SA (function of periods) using a weighted
        # running 3-point smoother

        if not eqrm_flags.run_type == "hazard" and \
                eqrm_flags.atten_smooth_spectral_acceleration is True:
            SA[..., 1:-2] = (0.25 * SA[..., 0:-3] +
                             0.50 * SA[..., 1:-2] +
                             0.25 * SA[..., 2:-1])

        ### RUN TYPE CALCULATIONS ###

        # calculate fatality
        if eqrm_flags.run_type == "fatality":

            MMI = rsa2mmi_array(SA)

            fatality = forecast_fatality(MMI,
                                         sites.attributes['POPULATION'][0],
                                         beta=eqrm_flags.fatality_beta,
                                         theta=eqrm_flags.fatality_theta)

            numelement = MMI.shape[1]

            if eqrm_flags.save_fatalities is True:
                total_fatalities[rel_i, :] = reshape(fatality[0,:, 0], numelement)

        # calculate damage
        elif eqrm_flags.run_type == "risk_csm":

            # This means calc_total_loss does not know about the
            # dimensions of multiple gmms and spawning.
            overloaded_MW = tile(event_set.Mw,
                                 num_gmm_max * num_spawning * num_rm)

            (total_loss,
             damage) = sites.calc_total_loss(SA, eqrm_flags, overloaded_MW)

            assert isfinite(total_loss[0]).all()

            # It is called total building loss since it includes contents
            # break loss tuple into components
            # structure_loss = structural loss
            # nsd_loss = non-structural drift sensitive loss
            # accel_loss = non-structural acceleration  sensitive loss
            # con_loss = contents loss
            (structure_loss, nsd_loss, accel_loss, con_loss) = total_loss
            # The losses have the dimensions of (site, event)
            # the event dimension is overloaded with event * max_gmm * spawning
            # Can unload the event dimension.
            #  dimensions of (site, spawn, max ground motion model, events)
            newshape = (1, num_spawning, num_gmm_max, num_rm, num_events)
            structure_loss_qw = structure_loss.reshape(newshape)
            nsd_loss_qw = nsd_loss.reshape(newshape)
            accel_loss_qw = accel_loss.reshape(newshape)
            con_loss_qw = con_loss.reshape(newshape)

            # Putting economic loss values into a big array
            # (number of buildings versus number of events)
            # Note that this matrix is transposed before saving
            # (i.e. to number of events versus number of buildings)
            if eqrm_flags.save_total_financial_loss is True:
                total_building_loss_qw[rel_i, ...] = (
                    structure_loss_qw + nsd_loss_qw + accel_loss_qw
                    + con_loss_qw)[0, ...]
            if eqrm_flags.save_building_loss is True:
                building_loss_qw[rel_i, ...] = (
                    structure_loss_qw + nsd_loss_qw + accel_loss_qw)[0, ...]
            if eqrm_flags.save_contents_loss is True:
                contents_loss_qw[rel_i, ...] = con_loss_qw[0, ...]

            if (eqrm_flags.save_prob_structural_damage is True and
                    num_pseudo_events == 1):
                # This is not cumulative
                total_structure_damage[rel_i, :] = damage.structure_state

        # calculate bridge damage
        elif eqrm_flags.run_type == "bridge":
            # print 'STARTING bridge damage calculations'

            (damage,
             days_to_complete) = sites.calc_total_loss(SA, eqrm_flags)

            # accumulate days to complete
            if eqrm_flags.bridges_functional_percentages is not None:
                saved_days_to_complete[rel_i, :,:] = days_to_complete

            if (eqrm_flags.save_prob_structural_damage is True and
                    num_pseudo_events == 1):
                # This is not cumulative
                total_structure_damage[rel_i, :] = damage.structure_state

        elif eqrm_flags.run_type == "risk_mmi":
            # print 'STARTING vulnerability damage calculations
            loss = sites.calc_loss(
                SA,
                atten_periods=eqrm_flags.atten_periods)

            # This brings out all the psudo_event dimensions
            newshape = (1, num_spawning, num_gmm_max, num_rm, num_events)
            loss_qw = loss.reshape(newshape)

            if eqrm_flags.save_building_loss is True:
                building_loss_qw[rel_i, ...] = loss_qw[0, ...]

        # Delete some objects before next loop to avoid memory spikes
        del sites
        del distances
        del source_model_subset
        del soil_SA
        del bedrock_SA

    # --------------------------------------------------------------
    # THIS IS THE END OF THE LOOP OVER SITES

    log.debug('Memory: Ended looping over sites')
    log.resource_usage()

    row_files_that_parallel_splits = []
    column_files_that_parallel_splits = []
    data_files_that_parallel_splits = []

    event_loop_time = (time.clock() - t0)
    #time_taken_site_loop = event_loop_time - time_taken_pre_site_loop
    time_pre_site_loop_fraction = time_taken_pre_site_loop / event_loop_time

    log.log_json({log.PRESITELOOP_J: time_pre_site_loop_fraction}, log.INFO)
    msg = "event_loop_time (excluding file saving) " + \
        str(datetime.timedelta(seconds=event_loop_time)) + " hr:min:sec"
    log.info(msg)

    log.log_json({log.EVENTLOOPTIME_J: event_loop_time}, log.INFO)

    # print "time_taken_pre_site_loop", time_taken_pre_site_loop
    # print "time_taken_site_loop", time_taken_site_loop

    # SAVE HAZARD
    if parallel.rank == 0:
        write_title = True
    else:
        write_title = False

    if eqrm_flags.save_hazard_map is True and parallel.lo != parallel.hi:
        files = save_hazard(soil_amp=False, eqrm_flags=eqrm_flags,
                            hazard=data.bedrock_hazard,
                            sites=all_sites,
                            compress=eqrm_flags.compress_output,
                            parallel_tag=parallel.file_tag,
                            write_title=(parallel.rank == False))
        row_files_that_parallel_splits.extend(files)

        if data.soil_hazard is not None:
            files = save_hazard(soil_amp=True, eqrm_flags=eqrm_flags,
                                hazard=data.soil_hazard,
                                compress=eqrm_flags.compress_output,
                                parallel_tag=parallel.file_tag,
                                write_title=(parallel.rank == False))
            row_files_that_parallel_splits.extend(files)

    # Save Ground Motion
    if eqrm_flags.save_motion is True and parallel.lo != parallel.hi:

        # Save to csv
        # TODO: This is deprecated, remove once post-processing scripts written
        a_file = save_sites_to_csv(eqrm_flags.output_dir,
                                   eqrm_flags.site_tag,
                                   sites=all_sites,
                                   compress=eqrm_flags.compress_output,
                                   parallel_tag=parallel.file_tag,
                                   write_title=(parallel.rank == False))
        # save_hazard also calls save_sites. Only append if not already exists.
        # FIXME: This will overwrite what is written in save_hazard.
        #        Is this correct?
        if a_file not in row_files_that_parallel_splits:
            row_files_that_parallel_splits.append(a_file)

        # Save to numpy binary
        a_file, _ = save_motion_to_binary(soil_amp=False,
                                          eqrm_flags=eqrm_flags,
                                          motion=data.bedrock_SA_all,
                                          parallel_tag=parallel.file_tag)
        data_files_that_parallel_splits.append(a_file)

        if data.soil_SA_all is not None:
            # Save to numpy binary
            a_file, _ = save_motion_to_binary(soil_amp=True,
                                              eqrm_flags=eqrm_flags,
                                              motion=data.soil_SA_all,
                                              parallel_tag=parallel.file_tag)
            data_files_that_parallel_splits.append(a_file)

    # Save damage information
    if (eqrm_flags.save_prob_structural_damage is True and
            num_pseudo_events == 1 and
            parallel.lo != parallel.hi):
        # No sites were investigated.
        a_file = save_damage(eqrm_flags.output_dir, eqrm_flags.site_tag,
                             'structural', total_structure_damage,
                             all_sites.attributes['BID'],
                             compress=eqrm_flags.compress_output,
                             parallel_tag=parallel.file_tag,
                             write_title=(parallel.rank == False))
        row_files_that_parallel_splits.append(a_file)

    if ((eqrm_flags.save_motion is True or
         eqrm_flags.save_total_financial_loss is True or
         eqrm_flags.save_building_loss is True or
         eqrm_flags.save_contents_loss is True or
         eqrm_flags.save_prob_structural_damage is True) and
            parallel.lo != parallel.hi):
        files = save_distances(eqrm_flags, sites=all_sites,
                               event_set=event_set,
                               compress=eqrm_flags.compress_output,
                               parallel_tag=parallel.file_tag)
        column_files_that_parallel_splits.extend(files)

    # Save economic loss
    if ((eqrm_flags.save_total_financial_loss is True or
         eqrm_flags.save_building_loss is True or
         eqrm_flags.save_contents_loss is True) and
            parallel.lo != parallel.hi):
        a_file = save_structures(eqrm_flags, all_sites,
                                 compress=eqrm_flags.compress_output,
                                 parallel_tag=parallel.file_tag,
                                 write_title=(parallel.rank == False))
        row_files_that_parallel_splits.append(a_file)

    if (eqrm_flags.save_total_financial_loss is True and
            parallel.lo != parallel.hi):

        #  dimensions of total_building_loss_qw;
        # (site, spawn, max ground motion model, events)
        # want (spawn, max ground motion model, site, events, periods)
        # or (site, spawn, max ground motion model, dummy, events, periods)
        new_total_building_loss_qw = collapse_source_gmms(
            total_building_loss_qw[..., newaxis, :, newaxis],
            source_model, eqrm_flags.atten_collapse_Sa_of_atten_models)
        # collapse out fake site axis and fake periods axis.
        new_total_building_loss_qw = new_total_building_loss_qw[..., 0, :, 0]
        # overload the event
        new_total_building_loss_qw = new_total_building_loss_qw.reshape(
            (num_site_block, -1))

        a_file = save_ecloss('_total_building', eqrm_flags,
                             new_total_building_loss_qw, all_sites,
                             compress=eqrm_flags.compress_output,
                             parallel_tag=parallel.file_tag)
        column_files_that_parallel_splits.append(a_file)

        a_file = save_val(eqrm_flags,
                          sum(
                              all_sites.cost_breakdown(
                                  ci=eqrm_flags.loss_regional_cost_index_multiplier)),
                          '_bval',
                          compress=eqrm_flags.compress_output,
                          parallel_tag=parallel.file_tag)
        row_files_that_parallel_splits.append(a_file)

    if eqrm_flags.save_building_loss is True and parallel.lo != parallel.hi:
        new_building_loss_qw = collapse_source_gmms(
            building_loss_qw[..., newaxis, :, newaxis],
            source_model, eqrm_flags.atten_collapse_Sa_of_atten_models)
        # collapse out fake site axis and fake periods axis.
        new_building_loss_qw = new_building_loss_qw[..., 0, :, 0]
        # overload the event
        new_building_loss_qw = new_building_loss_qw.reshape(
            (num_site_block, -1))
        a_file = save_ecloss('_building', eqrm_flags, new_building_loss_qw,
                             all_sites, compress=eqrm_flags.compress_output,
                             parallel_tag=parallel.file_tag)
        column_files_that_parallel_splits.append(a_file)

        if eqrm_flags.run_type == "risk_mmi":
            # Save the building structure values
            # all_sites.cost_breakdown(
            # ci=eqrm_flags.loss_regional_cost_index_multiplier)
            structure_costs = all_sites.cost_breakdown()
            a_file = save_val(eqrm_flags,
                              structure_costs,
                              '_building_value',
                              compress=eqrm_flags.compress_output,
                              parallel_tag=parallel.file_tag)
            row_files_that_parallel_splits.append(a_file)

    if eqrm_flags.save_contents_loss is True and parallel.lo != parallel.hi:
        new_contents_loss_qw = collapse_source_gmms(
            contents_loss_qw[..., newaxis, :, newaxis],
            source_model, eqrm_flags.atten_collapse_Sa_of_atten_models)
        # collapse out fake site axis and fake periods axis.
        new_contents_loss_qw = new_contents_loss_qw[..., 0, :, 0]
        # overload the event
        new_contents_loss_qw = new_contents_loss_qw.reshape(
            (num_site_block, -1))

        a_file = save_ecloss('_contents', eqrm_flags, new_contents_loss_qw,
                             all_sites, compress=eqrm_flags.compress_output,
                             parallel_tag=parallel.file_tag)
        column_files_that_parallel_splits.append(a_file)

    if eqrm_flags.bridges_functional_percentages is not None and \
            parallel.lo != parallel.hi:
        files = save_bridge_days_to_complete(
            eqrm_flags,
            saved_days_to_complete, compress=eqrm_flags.compress_output,
            parallel_tag=parallel.file_tag)
        row_files_that_parallel_splits.extend(files)

    if (eqrm_flags.save_fatalities is True and
            parallel.lo != parallel.hi):
        # note: will not handle multiple GMPES
        file_row, file_col = save_fatalities(
            '_fatalities', eqrm_flags,
            total_fatalities,
            sites=all_sites,
            compress=eqrm_flags.compress_output,
            parallel_tag=parallel.file_tag,
            write_title=(parallel.rank == False))
        row_files_that_parallel_splits.append(file_row)
        if not file_col is None:
            column_files_that_parallel_splits.append(file_col)

        files = save_distances(eqrm_flags, sites=all_sites,
                               event_set=event_set,
                               compress=eqrm_flags.compress_output,
                               parallel_tag=parallel.file_tag)
        column_files_that_parallel_splits.extend(files)

    # parallel code.  Needed if # of processes is > # of structures
    num_blocks = parallel.calc_num_blocks()

    # Now process 0 can stitch some files together.
    if parallel.is_parallel and parallel.rank == 0:
        block_indices = parallel.calc_all_indices(num_sites)

        join_parallel_files(row_files_that_parallel_splits,
                            num_blocks,
                            block_indices,
                            compress=eqrm_flags.compress_output)

        join_parallel_files_column(column_files_that_parallel_splits,
                                   num_blocks,
                                   block_indices,
                                   compress=eqrm_flags.compress_output)

        join_parallel_data_files(data_files_that_parallel_splits,
                                 num_blocks,
                                 block_indices)

    # Let's stop all the programs at the same time
    # Needed when scenarios are in series.
    # This was hanging nodes, when using mpirun
    log.log_iowait()
    clock_time_taken_overall = (time.clock() - t0_clock)
    wall_time_taken_overall = (time.time() - t0_time)
    msg = "On node %i, %s clock (processor) time taken overall %s hr:min:sec." % \
          (parallel.rank,
           parallel.node,
           str(datetime.timedelta(seconds=clock_time_taken_overall)))
    log.info(msg)

    log.log_json({log.CLOCKTIMEOVERALL_J: clock_time_taken_overall}, log.INFO)

    wall_time_taken_overall = (time.time() - t0_time)
    msg = "On node %i, %s wall time taken overall %s hr:min:sec." % \
          (parallel.rank,
           parallel.node,
           str(datetime.timedelta(seconds=wall_time_taken_overall)))
    log.info(msg)
    log.log_json({log.WALLTIMEOVERALL_J: wall_time_taken_overall}, log.INFO)
    log.info(msg)
    if parallel_finalise:
        parallel.finalize()
    del parallel
    log.debug('Memory: End')
    log.resource_usage(tag=log.FINAL_J)
    log.remove_file_handler()

##########################################################################
# these are subfunctions
##########################################################################


def calc_and_save_SA(eqrm_flags,
                     sites,
                     event_set,
                     distances,
                     bedrock_SA_all,
                     soil_SA_all,
                     bedrock_hazard,
                     soil_hazard,
                     soil_amplification_model,
                     site_index,  # FIXME = rel_site_index therefore remove
                     rel_site_index,
                     ground_motion_distribution,
                     amp_distribution,
                     event_activity,
                     source_model,
                     num_site_block):
    """
    Calculate the spectral acceleration, in g, for both bedrock and soil.

    Return:
      bedrock_SA_all,
      soil_SA_all,

      bedrock_hazard,
      soil_hazard,

      soil_SA_overloaded,
      rock_SA_overloaded
    """

    num_spawn = event_activity.get_num_spawn()
    num_rm = event_activity.recurrence_model_count()

    # WARNING - this only works if the event activity is not collapsed.
    num_gmm_after_collapsing = event_activity.get_gmm_dimensions()

    num_gmm_max = source_model.get_max_num_atten_models()

    num_sites = len(sites)
    assert num_sites == 1
    num_events = len(event_set)
    num_periods = len(eqrm_flags.atten_periods)

    # Build some arrays to save into.
    # NUM_SITES IS 1

    # Array to save SA into.  Only storing close event info
    num_close_events = 0
    for source in source_model:
        num_close_events += len(source.get_event_set_indexes())

    coll_rock_SA_close_events = zeros(
        (num_spawn, num_gmm_after_collapsing, num_rm,
         num_sites, num_close_events, num_periods),
        dtype=float)

    log_dic = {log.CLOSEROCKSAE_J: coll_rock_SA_close_events.nbytes,
               "cra_num_close_events": num_close_events,
               "cra_num_spawn": num_spawn,
               "cra_num_periods": num_periods,
               "cra_num_gmm_after_collapsing": num_gmm_after_collapsing,
               "cra_close_events_fraction": num_close_events / float(num_events)}
    log.log_json(log_dic,
                 log.DEBUG,
                 logs_per_scenario=logs_per_scenario_con,
                 site=rel_site_index,
                 sites=num_site_block)

    log_dic = {log.CLOSERATIO_J: num_close_events / float(num_events)}
    log.log_json(log_dic, log.DEBUG,
                 logs_per_scenario=logs_per_scenario_con,
                 site=rel_site_index,
                 sites=num_site_block)

    if not eqrm_flags.run_type == "hazard":
        rock_SA_overloaded = zeros((num_sites,
                                    num_events * num_gmm_max *
                                    num_spawn * num_rm,
                                    num_periods),
                                   dtype=float)

        log.log_json({log.ROCKOVERLOADED_J: rock_SA_overloaded.nbytes},
                     log.DEBUG, logs_per_scenario=logs_per_scenario_con,
                     site=rel_site_index,
                     sites=num_site_block)
    else:
        rock_SA_overloaded = None

    if eqrm_flags.use_amplification is True:
        coll_soil_SA_close_events = zeros(
            (num_spawn, num_gmm_after_collapsing, num_rm, num_sites,
             num_close_events, num_periods), dtype=float)

        if not eqrm_flags.run_type == "hazard":
            soil_SA_overloaded = zeros((num_sites,
                                        num_events * num_gmm_max * num_spawn *
                                        num_rm,
                                        num_periods),
                                       dtype=float)
        else:
            soil_SA_overloaded = None
    else:
        soil_SA_overloaded = None

    s_evnti = 0  # start event index for the close event dimension
    e_evnti = 0  # end event index for the close event dimension

    # A list of indexes into the all events dimension
    all_event_indexes = zeros((num_close_events), dtype=int)
    for source in source_model:
        # The event_inds are the close events in this source
        event_inds = source.get_event_set_indexes()
        e_evnti += len(event_inds)
        all_event_indexes[s_evnti:e_evnti] = event_inds
        if len(event_inds) == 0:
            continue
        sub_event_set = event_set[event_inds]
        distance_subset = distances[event_inds]
        atten_model_weights = source.atten_model_weights
        ground_motion_calc = source.ground_motion_calculator

        log_mean_extend_GM, log_sigma_extend_GM = ground_motion_calc.distribution(
            event_set=sub_event_set,
            sites=sites,
            distances=distance_subset,
            Vs30=BEDROCKVs30)
        # *_extend_GM has shape of (GM_model, sites, events, periods)
        # the value of GM_model can change for each source.

        # evaluate the RSA
        # that is desired (i.e. chosen in parameter_handle)
        bedrock_SA = ground_motion_distribution.ground_motion_sample(
            log_mean_extend_GM, log_sigma_extend_GM)
        # bedrock_SA shape (spawn, GM_model, rec_model, sites, events, periods)
        # the events here is close events in this source
        # print 'ENDING Calculating attenuation'

        # Setup for amplification  model
        # handles interpolation to periods of interest
        # finds the mean and sigma (i.e. PDF) based on bedrock PGA and
        # Moment magnitude (if amps are a function of these)
        if eqrm_flags.use_amplification is True:
            soil_SA = get_soil_SA(bedrock_SA,
                                  sites.attributes['SITE_CLASS'],
                                  sub_event_set.Mw, eqrm_flags.atten_periods,
                                  soil_amplification_model,
                                  amp_distribution, ground_motion_calc,
                                  sub_event_set,
                                  sites,
                                  distance_subset,
                                  ground_motion_distribution)
            # Amplification factor cutoffs
            # Applies a minimum and maxium acceptable amplification factor
            # re-scale SAsoil if Ampfactor falls ouside acceptable
            # ampfactor bounds
            if eqrm_flags.amp_variability_method is not None:
                amp_rescale(soil_SA,
                            eqrm_flags.amp_min_factor,
                            eqrm_flags.amp_max_factor,
                            bedrock_SA)
            # PGA cutoff
            assert isfinite(soil_SA).all()
            cutoff_pga(soil_SA,
                       eqrm_flags.atten_pga_scaling_cutoff)
        else: 	# No soil amplification
            soil_SA = None
        cutoff_pga(bedrock_SA,
                   eqrm_flags.atten_pga_scaling_cutoff)

        # collapse  multiple attenuation models
        # gmm is 1 if its collapsed
        if (eqrm_flags.save_motion is True or
                eqrm_flags.save_hazard_map is True):
            collapsed_bedrock_SA = collapse_att_model(
                bedrock_SA,
                atten_model_weights,
                eqrm_flags.atten_collapse_Sa_of_atten_models)

            if soil_SA is not None:
                collapsed_soil_SA = collapse_att_model(
                    soil_SA,
                    atten_model_weights,
                    eqrm_flags.atten_collapse_Sa_of_atten_models)

        # saving RSA - only generally done for Ground Motion Simulation
        # (not for probabilistic hazard or if doing risk/secnario loss)
        # collapsed_bedrock_SA and  collapsed_soil_SA indexed by
        # [spawn, gmm, rm, site, event, period]
        if eqrm_flags.save_motion is True:
            gmm_n = collapsed_bedrock_SA.shape[1]
            # Put into arrays
            assert collapsed_bedrock_SA.shape[3] == 1  # only one site
            coll_bedrock_SA = collapsed_bedrock_SA[:, :,:, 0,:,:]
            bedrock_SA_all[:, :gmm_n, :, rel_site_index, event_inds,:] = \
                coll_bedrock_SA
            if soil_SA is not None:
                coll_soil_SA = collapsed_soil_SA[:, :,:, 0,:,:]
                soil_SA_all[:, :gmm_n, :, rel_site_index, event_inds,:] = \
                    coll_soil_SA
        if eqrm_flags.save_hazard_map is True:
            gmm_n = collapsed_bedrock_SA.shape[1]
            # Build collapsed_bedrock_SA for all events
            # before getting out of the loop
            # collapsed_bedrock_SA shape (spawn, gmm, sites, events, periods)

            coll_rock_SA_close_events[:, :gmm_n, :,:, s_evnti:e_evnti,:] = \
                collapsed_bedrock_SA
            if soil_SA is not None:
                # Build collapsed_soil_SA for all events
                coll_soil_SA_close_events[:, :gmm_n, :,:, s_evnti:e_evnti,:] \
                    = collapsed_soil_SA

        # Set up the arrays to pass to risk
        # This is built up as sources are iterated over.
        # assume one site

        if not eqrm_flags.run_type == "hazard":
            for i_spawn in arange(bedrock_SA.shape[0]):  # loop over spawn
                for i_gmm in arange(bedrock_SA.shape[1]):  # loop over gmm
                    for i_rm in xrange(bedrock_SA.shape[2]):
                        # FIXME Reinventing multidimensional array
                        # indexing here. Just use a ndarray() and return
                        # whataver.reshape(num_sites, -1, num_periods)
                        i_overloaded = (i_spawn * num_rm *
                                        num_gmm_max * num_events
                                        + i_rm * num_gmm_max * num_events +
                                        i_gmm * num_events +
                                        event_inds)
                        # rock_SA_overloaded
                        # dim (sites, events * gmm * rm * spawn, period)
                        rock_SA_overloaded[0, i_overloaded, :] = \
                            bedrock_SA[i_spawn, i_gmm, i_rm, 0, :,:]
                        if soil_SA is not None:
                            soil_SA_overloaded[0, i_overloaded, :] = \
                                soil_SA[i_spawn, i_gmm, i_rm, 0, :,:]

        # can not do this, the current SA only has a subset of all events.
        # 0 to drop site out
        # rock_SA_overloaded_auto = (bedrock_SA[:,:,0,:,:]).reshape(
        #    (num_sites, num_spawn*num_gmm_max*num_events, num_periods))
        s_evnti = e_evnti

    # End source loop

    # Compute hazard if desired
    if eqrm_flags.save_hazard_map is True:
        # event_activity.event_activity is [spawns, gmm, rec_models,
        # events]
        event_act_d_events = event_activity.event_activity.reshape(-1)
        event_act_d_close = event_activity.event_activity[:, :,:, \
                                                          all_event_indexes]
        event_act_d_close = event_act_d_close.reshape(-1)
        assert coll_rock_SA_close_events.shape[3] == 1  # only one site

        for j in xrange(len(eqrm_flags.atten_periods)):
            # Get these two arrays to be vectors.
            # The sites and spawning dimensions are flattened
            # into the events dimension.
            bedrock_SA_close = ravel(coll_rock_SA_close_events[:, :,:,:,:, j])
            bedrock_hazard[site_index, j, :] = \
                hzd_do_value(bedrock_SA_close,
                             event_act_d_close,
                             1.0 / array(eqrm_flags.return_periods))

            if eqrm_flags.use_amplification is True:
                soil_SA_close = ravel(coll_soil_SA_close_events[:, :,:,:,:, j])
                soil_hazard[site_index, j, :] = \
                    hzd_do_value(soil_SA_close, event_act_d_close,
                                 1.0 / array(eqrm_flags.return_periods))

    log.debug('Memory: calc_and_save_SA before return',
              logs_per_scenario=logs_per_scenario_con,
              site=rel_site_index,
              sites=num_site_block)
    log.resource_usage(tag=log.PEAK_J,
                       logs_per_scenario=logs_per_scenario_con,
                       site=rel_site_index,
                       sites=num_site_block)

    return soil_SA_overloaded, rock_SA_overloaded


def amp_rescale(soil_SA,
                amp_min_factor, amp_max_factor, bedrock_SA):
    if amp_min_factor is not None:
        too_low = (soil_SA / bedrock_SA) < amp_min_factor
        soil_SA[where(too_low)] = (amp_min_factor *
                                   bedrock_SA[where(too_low)])
    if amp_max_factor is not None:
        too_high = (soil_SA / bedrock_SA) > amp_max_factor
        soil_SA[where(too_high)] = (amp_max_factor *
                                    bedrock_SA[where(too_high)])


# handles the pga_cutoff
def cutoff_pga(ground_motion, max_pga):
    if max_pga is None:
        return

    # Doing ground_motion[...,0:1] gets the first values of
    # the last dimension,
    # but does not drop a dimension in the return value.
    # ground_motion[...,0] would drop a dimension.
    assert isfinite(ground_motion).all()

    too_high = ground_motion[..., 0:1] > max_pga
    scaling_factor = where(too_high, max_pga / ground_motion[..., 0:1], 1.0)
    ground_motion *= scaling_factor
    assert isfinite(ground_motion).all()


def load_data(eqrm_flags):
    """Load structure and bridge data into memory.

    eqrm_flags  a reference to the global eqrm_flags

    Returns a tuple (data, bridge_data) where:
        data         is a reference to a (possibly combined) structures+bridges
                     object
    """

    if eqrm_flags.run_type == 'risk_csm':

        # Find location of site database (i.e. building database) and get FID
        site_file = ('sitedb_' + eqrm_flags.site_tag +
                     eqrm_flags.site_db_tag + '.csv')
        try:
            site_file = get_local_or_default(site_file,
                                             eqrm_flags.default_input_dir,
                                             eqrm_flags.input_dir)
        except IOError:
            #site_file = None
            msg = "No site file was loaded.  Check file name; " + site_file
            raise RuntimeError(msg)

        # if indeed there is a BUILDING file
        sites = Structures.from_csv(
            site_file,
            building_classification_tag=eqrm_flags.building_classification_tag,
            damage_extent_tag=eqrm_flags.damage_extent_tag,
            default_input_dir=eqrm_flags.default_input_dir,
            input_dir=eqrm_flags.input_dir,
            eqrm_dir=eqrm_flags.eqrm_dir,
            buildings_usage_classification=
            eqrm_flags.buildings_usage_classification,
            use_refined_btypes=True,
            force_btype_flag=False,
            loss_aus_contents=eqrm_flags.loss_aus_contents)

        # FIXME do this after subsampling the sites
        # Hard wires the Demand Curve damping to 5%
        if eqrm_flags.buildings_set_damping_Be_to_5_percent is True:
            sites.building_parameters['damping_Be'] = 0.05  # + \
# 0*sites.building_parameters['damping_Be']

    elif eqrm_flags.run_type == 'risk_mmi':
        # we are running a vulnerability calculation
        name = 'sitedb_' + eqrm_flags.site_tag + \
            eqrm_flags.site_db_tag + '.csv'

        # find the location and FID for the grid file
        # i.e. searches input_dir then defaultdir
        name = get_local_or_default(name, eqrm_flags.default_input_dir,
                                    eqrm_flags.input_dir)

        sites = Structures_Vulnerability.from_csv(name, eqrm_flags)

    elif eqrm_flags.run_type == "hazard":
        # we are running hazard or ground motion scenario (i.e. no damage)
        if eqrm_flags.grid_flag == 1:
            # grid is from a GIS output
            name = eqrm_flags.site_tag + '_par_site.csv'
        elif eqrm_flags.grid_flag == 2:
            # Grid is from the grid_generator.py script
            name = eqrm_flags.site_tag + '_par_site_uniform.csv'

        # find the location and FID for the grid file
        # i.e. searches input_dir then defaultdir
        name = get_local_or_default(name, eqrm_flags.default_input_dir,
                                    eqrm_flags.input_dir)
        sites = Sites.from_csv(name, SITE_CLASS=str, VS30=float)

    elif eqrm_flags.run_type == "fatality":
        # we are running fatality calculation
        name = eqrm_flags.site_tag + '_popexp.csv'

        # find the location and FID for the grid file
        # i.e. searches input_dir then defaultdir
        name = get_local_or_default(name, eqrm_flags.default_input_dir,
                                    eqrm_flags.input_dir)
        sites = Sites.from_csv(name,
                               SITE_CLASS=str,
                               VS30=float,
                               POPULATION=float)

    elif eqrm_flags.run_type == "bridge":
        #raise RuntimeError('run_type "hazard" not yet modified for Bridges')

        # we are running fatality calculation
        name = ('bridgedb_' + eqrm_flags.site_tag +
                eqrm_flags.site_db_tag + '.csv')

        # find the location and FID for the grid file
        # i.e. searches input_dir then defaultdir
        name = get_local_or_default(name, eqrm_flags.default_input_dir,
                                    eqrm_flags.input_dir)

        sites = Bridges.from_csv(name)

    else:
        raise ValueError('Got bad value for eqrm_flags.run_type: %s'
                         % eqrm_flags.run_type)

    # check if we actually have some data to work with
    if sites is None:
        raise RuntimeError("Couldn't find BUILDING or BRIDGE data?")

    if sites.attributes.get('Vs30') is None:
        # Load the site_class 2 Vs30 mapping
        amp_factor_file = 'site_class2vs30.csv'
        amp_factor_file = get_local_or_default(amp_factor_file,
                                               eqrm_flags.default_input_dir,
                                               eqrm_flags.input_dir)
        # Load Vs30 mapping
        site_class2Vs30 = load_site_class2Vs30(amp_factor_file)
        # Use the mapping to add Vs30 info to add Vs30 info to structures
        sites.set_Vs30(site_class2Vs30)

    return sites

##########################################################################

# this will run if eqrm_analysis.py is called from DOS prompt or double clicked
if __name__ == '__main__':
    from sys import argv
    if len(argv) > 2:
        f = argv[1]  # note argv[0] will be 'main.py'
        use_determ_seed = argv[2]
        if use_determ_seed is 'y':
            print 'RESETTING RANDOM SEED'
            use_determ_seed = True
        elif use_determ_seed is 'n':
            print 'NOT RESETTING RANDOM SEED'
            use_determ_seed = False
        else:
            raise 'Input seed parameter must be y or n'
        compress_output = False
        if len(argv) > 3:
            compress_output = argv[3]
            if compress_output is 'y':
                print 'Compressing output'
                compress_output = True
            elif compress_output is 'n':
                print 'Not compressing output'
                compress_output = False
        main(f, use_determ_seed, compress_output=compress_output)
    else:
        assert len(argv) == 1
        import profile
        profile.run("main('setdata.txt',True)", 'fooprof')
        import pstats
        p = pstats.Stats('fooprof')
        p.sort_stats('cumulative').print_stats(10)
        p.sort_stats('cumulative').strip_dirs().print_callees(
            'distribution_function')

        # main('setdata.txt',True)
