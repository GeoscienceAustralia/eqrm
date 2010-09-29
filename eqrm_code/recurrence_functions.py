"""
 Title: recurrence_functions.py
 
  Author:  Duncan Gray, duncan.gray@ga.gov.au
           
  Description: Functions to calculate the event activity.
 
  Version: $Revision: 1663 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-05-08 23:32:10 +1000 (Sat, 08 May 2010) $
  
  Copyright 2007 by Geoscience Australia
"""

from scipy import exp, log, sum, zeros, newaxis, where, array, allclose, r_,sin,cos,sqrt,arctan2,unique
from math import atan2, radians 

from eqrm_code.ANUGA_utilities import log as eqrmlog


def calc_event_activity(event_set, sources,
                        prob_number_of_mag_sample_bins, weight):
    """
    event_set - Event_Set instance - this function uses Mw and rupture_centroid
                               and returns a subset of event_set
    sources - a list of Source_Model.
    prob_number_of_mag_sample_bins - number of magnitude sample bins.

    when analysis uses this function, the weight used is a constant of [1.0]
    EQRM can currently only handle one source model.
    A source model has many source polygons.
    """
    # print "event_set", event_set
    #print "sources", sources
    #print "len(sources)", len(sources)
    #print "prob_number_of_mag_sample_bins", prob_number_of_mag_sample_bins
    #import sys; sys.exit()

    # EQRM currently does just 1 source
    assert len(weight) == len(sources) == 1
        
    event_activity_matrix=zeros((len(event_set),len(sources)),float)
    #weight_matrix=zeros((len(event_set),len(sources)),float)
    eqrmlog.debug('Memory: event_activity_matrix weight_matrix created')
    eqrmlog.resource_usage()

    # A hacky way of finding the source_zone_id
    # There should really be a source zone object that is
    # used by event set as well
    # And this should know about source_zone_id's.
    # Maybe.  But event set uses generation polygons,
    # which in future versions of EQRM may not be the same
    # as source zone polygons.
    for j in range(len(sources)): # loop over all source models
        for i in range(len(sources[j])): # loop over source zones 
            source=sources[j][i]
            zone_m0=source.min_magnitude            
            zone_mlow=max(source.prob_min_mag_cutoff,zone_m0)
            zone_mhgh=source.max_magnitude
            zone_b=source.b
            zone_f_gr=source.Lambda_Min

            grfctr=grscale(zone_b,zone_mhgh,zone_mlow,zone_m0)
            A_mlow=zone_f_gr*grfctr
            
            
            #length = calc_ll_dist()
            
            #if slip_rate>0 :
                #A_mlow= calc_A_min_from_slip_rate(zone_b,zone_m0,zone_mhgh,slip_rate,source.area)
                #A_min= calc_A_min_from_slip_rate(1,4,7,slip_rate,area)
            # print "zone_f_gr", zone_f_gr
            #print "grfctr",grfctr 
            # print "A_mlow",A_mlow

            #print "zone_mlow",zone_mlow
            #print "zone_mhgh", zone_mhgh
            #get the magnitude index where Mw is in the 
            mag_ind=where((zone_mlow<event_set.Mw)&
                          (event_set.Mw<zone_mhgh))[0]
            #print "mag_ind", mag_ind
            #import sys; sys.exit()
            # WAY ONE - to get the poly_id - probably slow
            # Does the source contain an event set rupture centroid
            # Get the events in this source zone.
            # mag_ind limits the events checked.
            # This info could already be known, since EQRM generated the events
            # Should this function only be used on generated events though?
            contains_point=[source.contains_point((lat,lon), use_cach=False) \
                            for lat,lon in zip(
                event_set.rupture_centroid_lat,
                event_set.rupture_centroid_lon)]
            #print "where(contains_point)",where(contains_point)
            poly_ind=where(contains_point)[0]

            source.set_event_set_indexes(poly_ind)
            
            mag_ind=where((zone_mlow<event_set.Mw[poly_ind])&
                          (event_set.Mw[poly_ind]<zone_mhgh))[0]
            if len(mag_ind)>0:
                event_ind= poly_ind[mag_ind]
                #event_ind=mag_ind[poly_ind]
                num_of_mag_sample_bins = source.number_of_mag_sample_bins
                mag_bin_centroids=make_bins(zone_mlow,zone_mhgh,
                                            num_of_mag_sample_bins)

                # bin the event magnitudes
                delta_mag=(zone_mhgh-zone_mlow)/num_of_mag_sample_bins
                event_bins=array([int(i) for i in
                                  (event_set.Mw[event_ind]
                                   -zone_mlow)/delta_mag])

                if len(event_bins)<(50*num_of_mag_sample_bins):
                    new_mag_bin_centroids = array([where((sum(where(event_bins==[z], 1,0)))>0, mag_bin_centroids[z],0)for z in event_bins])
                    new_mag_bin_centroids=unique(new_mag_bin_centroids)
                    if len(mag_bin_centroids) <> len(new_mag_bin_centroids):
                        list_mag_bin_centroids=new_mag_bin_centroids.tolist()
                        event_bins=array([(list_mag_bin_centroids.index(mag_bin_centroids[z]))for z in event_bins])
                        mag_bin_centroids= new_mag_bin_centroids
                                             
                grpdf=m2grpdfb(zone_b,mag_bin_centroids,zone_mlow,zone_mhgh)
                
                event_activity_source =array([(A_mlow*grpdf[z]/(sum(where(event_bins==z, 1,0))))for z in event_bins])
                #print "sum(event_activity_source) ", sum(event_activity_source)
                #print "A_mlow ", A_mlow
                #old method: event_activity_source = (num_of_mag_sample_bins*A_mlow 
                                         #*grpdf[event_bins]/len(event_ind))
                event_activity_matrix[event_ind,j]=event_activity_source
                #weight_matrix[event_ind,j]=weight[j]

            #endif
        #endfor
        # NOTE, no weights have been applied.
        event_set.set_event_activity(event_activity_matrix[:,j])
    #endfor

    # This should be used to remove events from the scenario's
    # that are not in the mag range.
    # But currently events not in range are removed.
    no_event_activity_index = where(event_set.event_activity==0)

    # If any events are outside of all of the source zones
    # EQRM halts.
    assert len(no_event_activity_index[0]) == 0

    eqrmlog.debug('Memory: Out of the event_activity loop')
    eqrmlog.resource_usage()

    return event_activity_matrix 
    
    #event_activity_index = where(event_set.event_activity!=0)
    # FIXME DSG - Make the weight_matrix an object. These calc's
    # should occur in this object.
    # Then this object can be tested seperately
    #return event_set[event_activity_index]


    """
    #print "weight_matrix", weight_matrix
    weight_sum=weight_matrix.sum(axis=1)
    non_zerod_ind=where(weight_sum!=0)[0]
#     zerod_ind=where(weight_sum==0)[0]
#     if len(zerod_ind) > 0:
#         print "**************************************"
#         print "zerod_ind", zerod_ind
#         print "**************************************"
#         import sys; sys.exit() 
    #print 'zero_ind',where(weight_sum==0)[0]
    #print "len(non_zerod_ind)", len(non_zerod_ind)
    #print 'len(zero_ind)',len(where(weight_sum==0)[0]) # this is 4 indexes
    weight_matrix=weight_matrix[non_zerod_ind,:]/weight_sum[
        non_zerod_ind][:,newaxis]

    # test that the normalised weight matrix sums to 1 for all events:
    if not (weight_matrix.sum(axis=1)==1).all():
        raise Exception('weight_matrix did not sum to 1')
    event_activity=event_activity_matrix[non_zerod_ind,:]*weight_matrix
    event_activity=event_activity.sum(axis=1)
    #print "event_activity", event_activity
     # create a sub set of the current events.
    new_event_set=event_set[non_zerod_ind]
    # FIXME DSG Think about the object design.
    # Maybe this method sould be within event set, since it
    # is adding an attribute to event_set
    new_event_set.set_event_activity(event_activity)
    #print "new_event_set.event_activity", new_event_set.event_activity
    # returning an event set with the attribute event_activity tacked on.
    """
    return event_set
                

def m2grpdfb(b,m,m0,mmax):
    """
    from matlab;
    Computes the PDF, fm for the bounded Gutenberg-Richter distribution.
    This is eq3.4, page 32, of v3.0 of the manual.
    % m2grpdfb: returns GR pdf given b, [m0,mmax] and magnitude array
%
% USE:     pdf = m2grpdfb(b,m,m0,mmax)
%                b:     scalar b-value
%                m:     array of magnitudes
%                m0:    scalar lower GR m
%                mmax:  scalar upper GR m
%          output dim(pdf) == input dim(m(:))
%
% NOTES:   based on m2grpdf (m0 & mmax added)
%          comparison between m2gfpdf & mdprpdfb: delta circa 10^-15
%          int(pdf) == 1 (assumes dm = 1)
%          this is a TRUNCATED GR pdf
%                                                Andres Mendez       
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
    
    # determine the probability of each event from the bounded GR PDF
    # This is eq3.6, page 32, of v3.0 of the manual.
    beta=log(10)*b

    # This is eq3.5, page 32, of v3.0 of the manual.
    pdf_tmp = beta*exp(-beta*(m-m0))/(1-exp(-beta*(mmax-m0)))
    #print "pdf_tmp", pdf_tmp

    # This is eq3.4, page 32, of v3.0 of the manual.
    # Normalise so the array sums to 1
    pdf=pdf_tmp/sum(pdf_tmp)
    return pdf
        

def make_bins(min_magnitude,max_magnitude,num_bins):
    
    delta_mag = (max_magnitude-min_magnitude)/num_bins
    bins = r_[min_magnitude+delta_mag/2:max_magnitude-delta_mag/2:num_bins*1j]
    #approximate the number of earthquakes in discrete (0.1 unit) bins
    return bins



def grscale(b,max_magnitude,new_min,min_magnitude):
    """
    Return Lambda for mag, max_magnitude, and min_magnitude
    
    This is eq3.3, page 32, of v3.0 of the manual, without the Amin.

    The Amin is applied in calc_event_activity.
    
    """
    #print b,max_magnitude,new_min,min_magnitude
    # calculate rate of exceedence for magnitude "mag" using Kramer eqn 4.10
    beta=log(10)*b
    
    numerator=(exp(-beta*(new_min-min_magnitude))
               -exp(-beta*(max_magnitude-min_magnitude)))

    denominator=1-exp(-beta*(max_magnitude-min_magnitude))
    return numerator/denominator

def calc_A_min_from_slip_rate_GR(b,mMin,mMax,slip_rate,area):
    c=1.5
    d=16.1
    beta=log(10)*b
    shear= 3*10**11
    Mo_max=10**((c*mMax)+d)
    #M_total= shear*area*slip_rate
    numerator=shear*area*slip_rate*(c-b)*(1-exp(-beta*(mMax-mMin)))
    denominator=Mo_max*exp(-beta*(mMax-mMin))
    return numerator/denominator


def calc_A_min_from_slip_rate_Characteristic(b,mMin,mMax,slip_rate,area):
    c=1.5
    d=16.1
    m2=0.5
    m1=1
    beta=log(10)*b
    m_c=mMax-m2
    shear= float(3*10**11)
    Mo_max=10**((c*mMax)+d)
    c=1.5
    K =((b*10**(-c/2)) /(c-b)) +((b*exp(beta)*(1-10**(-c/2)))/c)
    K2 = (( b*10**(-c/2)) / (c - b))  + ( (b*exp(beta)*(1-10**(-c/2))) / (c))


    numerator=shear*area*slip_rate*(1-exp(-beta*(mMax-mMin-0.5)))
    denominator=Mo_max*K*exp(-beta*(mMax-mMin-0.5))
    lambda_m1 =numerator/denominator
    numerator=beta*lambda_m1*exp(-beta*(mMax-mMin-1.5))
    denominator=2*(1-exp(-beta*(mMax-mMin-0.5)))
    lambda_mc =numerator/denominator
    lambda_m=lambda_m1+lambda_mc
        
    return lambda_m

def calc_activity_from_slip_rate_Characteristic(magnitude,b,m0,mMax):
    c=1.5
    d=16.1
    m2=0.5
    m1=1.0
    m=magnitude
    beta=log(10)*b
    m_c=mMax-m2
    C=((beta*exp(-beta*(mMax-m0-m1-m2)))*m2)/(1-exp(-beta*(mMax-m0-m2)))
    if magnitude <=m_c:
        pdf=(beta*exp(-beta*(m-m0-m1-m2)))/((1-1*exp(-beta*(mMax-m0-m2)))*(1+C)) 
    if magnitude >m_c:
        pdf=(beta*exp(-beta*(m-m0-m1-m2)))/((1-1*exp(-beta*(mMax-m0-m2)))*(1+C))
    return pdf
        

def calc_ll_dist(lat1,lon1,lat2,lon2):
    R = 6371
    dLat = radians(abs(lat2-lat1))
    dLon = radians(abs(lon2-lon1))
    a = (sin(dLat/2) * sin(dLat/2) +
            cos(radians(lat1)) * cos(radians(lat2)) *
            sin(dLon/2) * sin(dLon/2))
    c = 2 * arctan2(sqrt(a), sqrt(1-a))
    return R * c
    
