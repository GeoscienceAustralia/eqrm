"""
Created on 17/01/2012

@author: Ben Cooper, ben.cooper@ga.gov.au

Functions used by analysis to filter data
"""

from scipy import where

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