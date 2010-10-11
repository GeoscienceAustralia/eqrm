"""
 Title: ground_motion_distribution.py
 
  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, duncan.gray@ga.gov.au
           
  Description: Sample from a log normal distribution.
 
  Version: $Revision: 910 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-03-30 17:17:00 +1100 (Mon, 30 Mar 2009) $
  
  Copyright 2007 by Geoscience Australia
"""

from scipy import exp, log, where, isfinite, reshape, array, r_, rollaxis
from scipy.stats import norm

SPAWN = 1 

class Distribution_Log_Normal(object):
    """
    Log normal distribution.

    Note, since this uses random numbers, just instanciating an instance
    of this class will cause check_scenario to fail.

    """
    def __init__(self, var_method, atten_spawn_bins=None):
        
        self.var_method = var_method        
        self.rvs = norm.rvs # function from scipy.stats
        self.pdf = norm.pdf # function from scipy.stats
        if var_method == None:
            atten_spawn_bins = 1
        self.atten_spawn_bins = atten_spawn_bins
        
        sigma_delta = 2.5
        weights, centroids = normalised_pdf(sigma_delta, atten_spawn_bins)
        self.spawn_weights = weights
        # Get the dimensions ready for applying to log_sigma's
        self.spawn_centroids = centroids #.reshape(1,-1)
        
            
    def sample_for_eqrm(self, log_mean=None, log_sigma=None):
        """
        FIXME needs comments
        """
        
        if self.var_method == SPAWN :
            # spawn
            # log_mean will have dimensions of (site, event, period)
            sample_values = self._spawn(log_mean, log_sigma)    
        else:
            if self.var_method == None:
                sample_values = exp(log_mean)           
            elif self.var_method == 2:
                # monte carlo
                sample_values = self._monte_carlo(log_mean, log_sigma)
            elif self.var_method == 3:
                # + 2 sigma
                sample_values = exp(log_mean+2*log_sigma)  
            elif self.var_method == 4:
                # + 1 sigma
                sample_values = exp(log_mean+1*log_sigma)
            elif self.var_method == 5:
                # - 1 sigma
                sample_values = exp(log_mean-1*log_sigma)
            elif self.var_method == 6:
                # - 2 sigma
                sample_values = exp(log_mean-2*log_sigma)
            #elif self.var_method == 7:
                # corrected mean
             #   sample_values = self.corrected_mean
            new_shape = [1] + list(sample_values.shape)
            # This adds the spawning dimension,
            # as the first dimension
            sample_values = sample_values.reshape(new_shape) 
        return None, sample_values, None
    
    def _spawn(self, log_mean, log_sigma):
        """
        Spawning will add a spawning dimension, as the first dimension.
        Each cut into the spawning dimension represents the SA at
        a different centroid.
        """
        #print "SPAWNING"
        #print "self.spawn_centroids", self.spawn_centroids
        # start off by adding the spawn dimension at the end.
        new_shape = list(log_sigma.shape) + [1]
        log_sigma = log_sigma.reshape(new_shape)
        spawned_log_sigma = log_sigma * self.spawn_centroids
        # roll the spawn dimension to the front
        spawned_log_sigma = rollaxis(spawned_log_sigma,
                                     spawned_log_sigma.ndim-1, 0)
        sample_values = exp(log_mean + spawned_log_sigma)
        return sample_values
        
    def _monte_carlo(self, log_mean=None, log_sigma=None, variate_site=None):
        """
        variate_site should only be used for testing
        """      
        if variate_site is None:
            # size sets the shape of the returned array
            variate_site=self.rvs(size=log_sigma.size)
        sample_values = exp(log_mean + variate_site * log_sigma)        
        return sample_values

    

def normalised_pdf(sigma_delta, atten_spawn_bins):
    """
    
    Parameters
      sigma_delta: Bound the bin centroids within -sigma_delta to sigma_delta.
        There will always be a centroid on the -sigma_delta and sigma_delta,
        unless atten_spawn_bins = 1.
      atten_spawn_bins: the number of centroids that will sample the pdf.

    Return
      An array of weights, sampled from the pdf, at the centroid values.
        These values are then normalised, so the list sums to 1.0.
        len(weights) == len(atten_spawn_bins)
    """
    if atten_spawn_bins == None or atten_spawn_bins <= 1:        
        weights = array([1.])
        centroids = array([0.])
    else:
        centroids = r_[-sigma_delta: sigma_delta: atten_spawn_bins*1j]
        unnormed_weights = norm.pdf(centroids)
        weights = unnormed_weights/sum(unnormed_weights)

    return weights, centroids
    
    
# FIXME: REMOVE THIS CLASS  THIS CLASS IS OBSOLETE.  DO NOT USE#
class Log_normal_distribution(object):
    """
    Log normal distribution.

    Note, since this uses random numbers, just instanciating an instance
    of this class will cause check_scenario to fail.

    """
    def __init__(self,
                 var_method,
                 num_psudo_events=None,
                 num_sites_per_site_loop=1, 
                 atten_log_sigma_eq_weight=0,
                 variate_eq=None):
        # var_flag is not used.
                
        self.min_cutoff=None
        self.max_cutoff=None

        #if var_method is None:
        #    var_method = 1
        
        self.var_method = var_method        
        self.rvs=norm.rvs # function from scipy.stats
        self.pdf=norm.pdf # function from scipy.stats
        self.num_psudo_events = num_psudo_events
        self.atten_log_sigma_eq_weight = atten_log_sigma_eq_weight

        # Randomness that is the same for each site  
        if self.var_method == 2:
            if variate_eq is None:
            
                self.variate_eq=self.rvs(size=(
                    num_sites_per_site_loop*
                    num_psudo_events))
                #print "self.variate_eq", self.variate_eq
                # make a variate the same size as sites * n * events
                self.variate_eq.shape=(num_sites_per_site_loop,
                                       num_psudo_events,
                                       1)
            else:
                self.variate_eq = variate_eq
            
    def set_log_mean_log_sigma_etc(self, log_mean, log_sigma,
                 event_activity=None, event_id=None):
        """
        The event_activity and event_id are attributes that
        ground_motion_calc.distribution pass 'through'
        Log_normal_distribution.
        Log_normal_distribution does not change these values
        """
        self.log_mean = log_mean
        self.log_sigma = log_sigma
        self.event_activity = event_activity
        self.event_id = event_id
        #print "self.log_mean", self.log_mean
        #print "self.log_sigma", self.log_sigma 
        #assert self.num_psudo_events == self.log_mean.shape[1]
        

    def sample_for_eqrm(self):
        """
        FIXME needs comments
        """
        if True:
            if self.var_method == None:
                #print "self.log_mean", self.log_mean
                sample_values=exp(self.log_mean)           
            elif self.var_method == 2:
                # monte carlo
                sample_values = self._monte_carlo_intra_inter()
            elif self.var_method == 3:
                # + 2 sigma
                sample_values = exp(self.log_mean+2*self.log_sigma)  
            elif self.var_method == 4:
                # + 1 sigma
                sample_values = exp(self.log_mean+1*self.log_sigma)
            elif self.var_method == 5:
                # - 1 sigma
                sample_values = exp(self.log_mean-1*self.log_sigma)
            elif self.var_method == 6:
                # - 2 sigma
                sample_values = exp(self.log_mean-2*self.log_sigma)
            elif self.var_method == 7:
                # corrected mean
                sample_values = self.corrected_mean

            # min_cutoff and max_cutoff are obsolete
            if self.min_cutoff is not None:
                sample_values=where(sample_values>self.min_cutoff,
                                    sample_values,self.min_cutoff)
            if self.max_cutoff is not None:
                sample_values=where(sample_values<self.max_cutoff,
                                    sample_values,self.max_cutoff)
                
        return self.event_id, sample_values, self.event_activity
    

    def _monte_carlo_intra_inter(self, variate_site=None):
        """
        variate_site should only be used for testing
        """      
        if variate_site is None:
            # size sets the shape of the returned array
            variate_site=self.rvs(size=(self.log_mean.shape[0]*
                                   self.log_mean.shape[1]))
            # make a variate the same size as sites * n * events
            variate_site.shape=(self.log_mean.shape[0],
                           self.log_mean.shape[1],
                           1)
            # reshape the variate to be the same shape as n*sigma,
            # execpt for periods
        sample_values=exp(
            self.log_mean + \
            self.atten_log_sigma_eq_weight*self.variate_eq*self.log_sigma + \
            (1-self.atten_log_sigma_eq_weight)*variate_site*self.log_sigma)
        
        return sample_values

    
    def get_corrected_mean(self):
        ground_motion=exp(self.log_mean+(self.log_sigma**2)/2)
        return ground_motion
    
    def get_median(self):
        ground_motion=exp(self.log_mean)
        return ground_motion
    
    def get_mode(self):
        ground_motion=exp(self.log_mean-(self.log_sigma**2))
        return ground_motion

    corrected_mean = property(get_corrected_mean)    
    median = property(get_median)    
    mode = property(get_mode)


    
    

    
