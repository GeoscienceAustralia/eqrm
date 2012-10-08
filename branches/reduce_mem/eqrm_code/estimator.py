"""
  Title: estimator.py
  
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  Description: Estimate the maximum memory needed, for each node,
  of an EQRM simulation.
  
  Copyright 20012 by Geoscience Australia
"""

from eqrm_code.ANUGA_utilities.log import EVENTS_J, MAXGMPE_J, BLOCKSITES_J, \
    PARALLELSIZE_J

def log_pairs_estimate_mem(log_pairs):
    """
    Given a list of dictionaries of log information estimate the memory
    used, in MB. Add the esimate to the log pairs.
    
    args;
    log_pairs 
    """
    for log_pair in log_pairs:
        mem_kb = estimate_mem_log_format(log_pair)
        print mem_kb
        #continue

def estimate_mem_log_format(log_pair): # = log_pair[]
    events = log_pair[EVENTS_J]
    atten_periods = log_pair['len_atten_periods']
    return_periods= log_pair['len_return_periods']
    parallel_size = log_pair[PARALLELSIZE_J]
    spawning = log_pair['atten_spawn_bins']
    gmm_dimensions = log_pair[MAXGMPE_J]
    rec_mod = 1 # = log_pair['']
    atten_collapse_Sa_of_atten_models = \
        log_pair['atten_collapse_Sa_of_atten_models']
    save_total_financial_loss = log_pair['save_total_financial_loss']
    save_building_loss = log_pair['save_building_loss']
    save_contents_loss = log_pair['save_contents_loss']
    save_hazard_map = log_pair['save_hazard_map']
    save_motion = log_pair['save_motion']
    use_amplification = log_pair['use_amplification']
    
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
                           use_amplification)
    return results

def estimate_mem(events, 
                 atten_periods, 
                 return_periods,
                 parallel_size=1,
                 spawning=1,
                 gmm_dimensions=1,
                 rec_mod=1,
                 atten_collapse_Sa_of_atten_models=False,
                 save_total_financial_loss=False,
                 save_building_loss=False,
                 save_contents_loss=False,
                 save_hazard_map=False,
                 save_motion=False,
                 use_amplification=False,
                 loop_sites=1,
                 item_size=8):
    """

    """
    
    gmm_max = gmm_dimensions
    #FIX ME 
    if atten_collapse_Sa_of_atten_models:
        gmm_after_collapsing = 1
    else:
        gmm_after_collapsing = gmm_max

    # calculate number of bytes for each data structure
    site_block = events/parallel_size

    if save_hazard_map is True:
        bedrock_hazard = (site_block *
                          atten_periods *
                          return_periods) * item_size
    else:
        bedrock_hazard = 0
        
    if save_hazard_map is True and \
           use_amplification is True:
        soil_hazard = bedrock_hazard
    else:
        soil_hazard = 0

    if save_motion is True:
        bedrock_SA_all = (spawning * gmm_dimensions * rec_mod *
                          site_block * events *
                          atten_periods) * item_size
    else:
        bedrock_SA_all = 0
        
    if save_motion is True and \
           use_amplification is True:
        soil_SA_all = bedrock_SA_all
    else:
        soil_SA_all = 0

    #if save_fatalities is True:
     #   total_fatalities = zeros((num_site_block, num_pseudo_events),
      #                              dtype=float)
   # if (eqrm_flags.save_prob_structural_damage is True and
   #      num_pseudo_events == 1):
   #      # total_structure_damage, given as a non-cumulative
   #      # probability. The axis are  sites, model_generated_psudo_events,
   #      # damage_states
   #      # (the damage_states are slight, moderate, extensive and complete.
   #      # subtract all of these from 1 to get the prob of no damage.)
   #      total_structure_damage = zeros((num_site_block, 4), dtype=float)
   # if eqrm_flags.bridges_functional_percentages is not None:
   #      saved_days_to_complete = zeros((
   #          num_site_block, num_pseudo_events,
   #          len(eqrm_flags.bridges_functional_percentages)))
   #  if eqrm_flags.save_hazard_map is True:
   #      data.bedrock_hazard = zeros((num_site_block,
   #                                   len(eqrm_flags.atten_periods),
   #                                   len(eqrm_flags.return_periods)),
   #                                  dtype=float)
   #  else:
   #      data.bedrock_hazard = None
        
    if save_total_financial_loss is True:
        total_building_loss_qw = (site_block * spawning *
                                  gmm_max * rec_mod * events) * item_size
    else:
        total_building_loss_qw = 0

    if save_building_loss is True:
        building_loss_qw =  (site_block * spawning *
                                  gmm_max * rec_mod * events) * item_size
    else:
        building_loss_qw = 0

    if save_contents_loss is True:
        contents_loss_qw =  (site_block * spawning *
                                  gmm_max * rec_mod * events) * item_size
    else:
        contents_loss_qw = 0

    coll_rock_SA_all_events = (spawning * gmm_after_collapsing * rec_mod *
                               site_block * events * atten_periods) * item_size

    rock_SA_overloaded = (loop_sites *
                          events * gmm_max * spawning * rec_mod *
                          atten_periods) * item_size

    if use_amplification is True:
        coll_soil_SA_all_events = coll_rock_SA_all_events          
        soil_SA_overloaded = rock_SA_overloaded
    else:
        coll_soil_SA_all_events = 0           
        soil_SA_overloaded = 0

    array_mem = bedrock_hazard + soil_hazard + bedrock_SA_all + soil_SA_all + \
       total_building_loss_qw + building_loss_qw + contents_loss_qw + \
       coll_rock_SA_all_events + rock_SA_overloaded + \
       coll_soil_SA_all_events + soil_SA_overloaded

    object_mem = 0
    total_mem = array_mem + object_mem
    return total_mem
