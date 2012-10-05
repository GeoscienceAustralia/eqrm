"""
Created on 17/01/2012

@author: Ben Cooper, ben.cooper@ga.gov.au

Functions used by analysis to filter data
"""

import copy

from scipy import where, intersect1d

def apply_threshold_distance(bedrock_SA,
                             soil_SA,
                             sites,
                             atten_threshold_distance,
                             use_amplification,
                             event_set):
    # re-compute the source-site distances
    # (NEEDED because this is not returned from bedrock_SA_pdf)
    # Identify sites which are greater than
    # eqrm_flags.atten_threshold_distance from an event
    # (NO GM computed for these sites)
    # This is not necessarily recomputing, since the
    # distance method used previously may not be Joyner_Boore.
    # But does this need to be Joyner_Boore?
    # FIXME do this earlier, and reduce the distribution calcs to do.
    distances = sites.distances_from_event_set(event_set). \
                distance('Joyner_Boore')
    #print "distances", distances
    site_inds, event_inds = where(distances > atten_threshold_distance)
    #print "site_inds", site_inds
    #print "event_inds", event_inds
    bedrock_SA[..., site_inds, event_inds, :] = 0
    if use_amplification is True:
        soil_SA[..., site_inds, event_inds, :] = 0
    #print "bedrock_SA", bedrock_SA
    #print "soil_SA", soil_SA

def source_model_threshold_distance_subset(distances,
                                           source_model,
                                           atten_threshold_distance):
    """
    source_model_threshold_distance_subset
    Calculate the distances of the event_set from the sites array. For those
    events less than or equal to the attenuation threshold, return a subset 
    source model so that calc_and_save_SA only works on those events.
    
    calc_and_save_SA calculates an SA figure by getting a subset of event
    indices:
    
    for source in source_model:
        event_inds = source.get_event_set_indexes()
        if len(event_inds) == 0:
            continue
        sub_event_set = event_set[event_inds]
    
    Returns source_model_subset
    """
    # A rethink of apply_threshold distance
    # Calculate the distances of the event_set from the sites array and
    # return an event_set where distance <= atten_threshold_distance
    Rjb = distances.distance('Joyner_Boore')
                
    # distances is an ndarray where [sites, events]. We only want the events 
    # dimension for this function as we're trimming events
    (sites_to_keep, events_to_keep) = where(Rjb <= atten_threshold_distance)

    source_model_subset = copy.deepcopy(source_model)
    # Re-sync the event indices in the source model. As we don't want to add
    # events that may already be excluded by generate_synthetic_events_fault(),
    # do the following
    # 1. Grab the event set already calculated
    # 2. The intersection of this and events_to_keep is what we want
    for source in source_model_subset:
        source_indices = source.get_event_set_indexes()
        source.set_event_set_indexes(intersect1d(source_indices,events_to_keep))
    
    return source_model_subset