"""
 Title: recurrence_functions.py
 
  Author:  Duncan Gray, duncan.gray@ga.gov.au
           
  Description: Functions to calculate the event activity.
 
  Version: $Revision: 1663 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-05-08 23:32:10 +1000 (Sat, 08 May 2010) $
  
  Copyright 2007 by Geoscience Australia
"""

from scipy import exp, log, sum, zeros, newaxis, where, array, asarray, r_,sin,cos,sqrt,arctan2,unique,arcsin,arccos
from math import radians, degrees,atan

from eqrm_code.ANUGA_utilities import log as eqrmlog
from eqrm_code.test_distance_functions import azimuths
#ma.core import sin


def calc_event_activity(event_set, source_model):
    """
    event_set - Event_Set instance - this function uses Mw and rupture_centroid
                               and returns a subset of event_set
    source_model - The source_model - holds a list of source_zone_polygons.
   
    when analysis uses this function, the weight used is a constant of [1.0]
    EQRM can currently only handle one source model.
    A source model has many source polygons.
    """
    
    event_activity_matrix=zeros((len(event_set)),float)
    eqrmlog.debug('Memory: event_activity_matrix weight_matrix created')
    eqrmlog.resource_usage()

    # A hacky way of finding the source_zone_id
    # There should really be a source zone object that is
    # used by event set as well
    # And this should know about source_zone_id's.
    # Maybe.  But event set uses generation polygons,
    # which in future versions of EQRM may not be the same
    # as source zone polygons.
    for source in source_model: # loop over source zones 
        zone_mlow = max(source.prob_min_mag_cutoff, source.min_magnitude)
        zone_mhgh = source.max_magnitude
               
        poly_ind = source.event_set_indexes
        mag_ind = where((zone_mlow < event_set.Mw[poly_ind])&
                        (event_set.Mw[poly_ind] < zone_mhgh))[0]
        
        if len(mag_ind)>0:
            zone_b = source.b
            grfctr = grscale(zone_b,zone_mhgh,zone_mlow, source.min_magnitude)
            A_mlow = source.A_min * grfctr
            
            event_ind= poly_ind[mag_ind]
            #event_ind=mag_ind[poly_ind]
            num_of_mag_sample_bins = source.number_of_mag_sample_bins
            mag_bin_centroids=make_bins(zone_mlow,zone_mhgh,
                                        num_of_mag_sample_bins)

            # bin the event magnitudes
            delta_mag = (zone_mhgh-zone_mlow)/num_of_mag_sample_bins
            event_bins = array([int(i) for i in
                                (event_set.Mw[event_ind]
                                 -zone_mlow)/delta_mag])

            # Check to see if all mag_bin_centroids have events
            # Assume that if there are 50 events for every bin
            # all bins will have events.
            if len(event_bins)<(50*num_of_mag_sample_bins):
                new_mag_bin_centroids = array(
                    [where((sum(
                    where(event_bins == [z], 1,0)))>0,
                           mag_bin_centroids[z],0)for z in event_bins])
                
                new_mag_bin_centroids=unique(new_mag_bin_centroids)
                if len(mag_bin_centroids) <> len(new_mag_bin_centroids):
                    list_mag_bin_centroids = new_mag_bin_centroids.tolist()
                    event_bins = array(
                        [(list_mag_bin_centroids.index(
                        mag_bin_centroids[z])) for z in event_bins])
                    mag_bin_centroids= new_mag_bin_centroids

            if source.recurrence_model_distribution=='bounded_gutenberg_richter':
                grpdf = m2grpdfb(zone_b,mag_bin_centroids,zone_mlow,zone_mhgh)
                
            
            if source.recurrence_model_distribution=='characteristic':
                grpdf=calc_activities_from_slip_rate_Characteristic(
                    mag_bin_centroids, 
                    zone_b, zone_mlow,
                    zone_mhgh)
                
        
            event_activity_source = array( [(A_mlow*grpdf[z]/(sum(where(
                                               event_bins == z, 1,0)))) 
                                              for z in event_bins])
            event_activity_matrix[event_ind] = event_activity_source
        event_set.set_event_activity(event_activity_matrix)

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

def calc_A_min_from_slip_rate(b,mMin,mMax,slip_rate_mm,area_kms,dist_model):
    if dist_model == 'characteristic':
        A_min = calc_A_min_from_slip_rate_Characteristic(b,mMin,mMax,
                                                         slip_rate_mm,area_kms)
    else:
        A_min = calc_A_min_from_slip_rate_GR(b,mMin,mMax,slip_rate_mm,area_kms)
    return A_min

def calc_A_min_from_slip_rate_GR(b,mMin,mMax,slip_rate_mm,area_kms):
    c=1.5
    d=16.1
    beta=log(10)*b
    shear= 3*10**11
    Mo_max=10**((c*mMax)+d)
    area=area_kms*10**10
    slip_rate =slip_rate_mm/10
    #M_total= shear*area*slip_rate
    numerator=shear*area*slip_rate*(c-b)*(1-exp(-beta*(mMax-mMin)))
    denominator=Mo_max*exp(-beta*(mMax-mMin))
    return numerator/denominator


def calc_A_min_from_slip_rate_Characteristic(b,mMin,mMax,slip_rate_mm,area_kms):
    c=1.5
    d=16.1
    beta=log(10)*b
    shear= float(3*10**11)
    Mo_max=10**((c*mMax)+d)
    c=1.5
    area=area_kms*10**10
    slip_rate =slip_rate_mm/10
    K =((b*10**(-c/2)) /(c-b)) +((b*exp(beta)*(1-10**(-c/2)))/c)

    numerator=shear*area*slip_rate*(1-exp(-beta*(mMax-mMin-0.5)))
    denominator=Mo_max*K*exp(-beta*(mMax-mMin-0.5))
    lambda_m1 =numerator/denominator
    numerator=beta*lambda_m1*exp(-beta*(mMax-mMin-1.5))
    denominator=2*(1-exp(-beta*(mMax-mMin-0.5)))
    lambda_mc =numerator/denominator
    lambda_m=lambda_m1+lambda_mc
        
    return lambda_m

def calc_activities_from_slip_rate_Characteristic(magnitudes,b,m0,mMax):
    pdfs_tmp =asarray([calc_activity_from_slip_rate_Characteristic(m,b,m0,mMax)
                  for m in magnitudes])
    pdfs=pdfs_tmp/sum(pdfs_tmp)
    return pdfs

def calc_activity_from_slip_rate_Characteristic(magnitude,b,m0,mMax):
    m2=0.5
    m1=1.0
    beta=log(10)*b
    m_c=mMax-m2
    C=((beta*exp(-beta*(mMax-m0-m1-m2)))*m2)/(1-exp(-beta*(mMax-m0-m2)))
    if magnitude <=m_c:
        pdf=(beta*exp(-beta*(magnitude-m0)))/((1-1*exp(-beta*(mMax-m0-m2)))*(1+C)) 
    if magnitude >m_c:
        pdf=(beta*exp(-beta*(mMax-m0-m1-m2)))/((1-1*exp(-beta*(mMax-m0-m2)))*(1+C))
    return pdf
        

