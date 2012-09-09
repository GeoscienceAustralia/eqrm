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

from scipy import exp, log, where, isfinite, reshape, array, r_, rollaxis, \
    seterr, newaxis, repeat
from scipy.stats import norm

SPAWN = 1 

# By assigning gm_rvs here, it can be reset to something deterministic
# in the test suites in order to produce repeatable results. Note that
# this must happen before instantiating Distribution_Log_Normal() (or
# subclasses) in the test suite.
gm_rvs = norm.rvs  # function from scipy.stats

class Distribution(object):
    """
    Provides a way to pick normally or lognormally distributed samples from 
    a set of normal distributions characterised by mean and standard-deviation 
    parameters.
    
    Choose the distribution by overriding the return value function in the 
    constructor.
    """
    sample_shape = (Ellipsis,) # Essentially a no-op in this base
                               # class. See ._monte_carlo()
    
    def __init__(self, var_method):
        self.var_method = var_method        
        self.rvs = gm_rvs
        self.val_func = exp
            
    def sample_for_eqrm(self, mean, sigma, var_in_last_axis=True): #False):
        """
        mean, sigma: ndarray. Must have identical shapes.

        Returns: ndarray in the same shape as mean. Estimated
        pectral accelerations at a site due to an event.
        """
        assert sigma.shape == mean.shape
        
        if self.var_method == None:
            sample_values = self.val_func(mean)
        elif self.var_method == 2:
            # monte carlo
            sample_values = self._monte_carlo(mean, sigma, var_in_last_axis=
                                              var_in_last_axis)
        elif self.var_method == 3:
            # + 2 sigma
            sample_values = self.val_func(mean+2*sigma)
        elif self.var_method == 4:
            # + 1 sigma
            sample_values = self.val_func(mean+1*sigma)
        elif self.var_method == 5:
            # - 1 sigma
            sample_values = self.val_func(mean-1*sigma)
        elif self.var_method == 6:
            # - 2 sigma
            sample_values = self.val_func(mean-2*sigma)
        else:
            raise RuntimeError('Unknown var_method %s' % str(self.var_method))
        return sample_values
        
    def _vs(self, sigma, var_in_last_axis):
        # Gets overridden in child class
        #return self.rvs(size=sigma.size).reshape(sigma.shape)
        if var_in_last_axis:
            size =  sigma.size
            shape = sigma.shape
        else:
            size =  sigma.size/sigma.shape[-1]
            shape = list(sigma.shape)
            shape[-1] = 1

        variate = self.rvs(size=size).reshape(shape)

        if not var_in_last_axis:
            variate = repeat(variate, sigma.shape[-1],  
                             axis=len(variate.shape)-1)

        return variate 

    def _monte_carlo(self, mean, sigma, var_in_last_axis):
        """
        Perform random sampling about mean with sigma.
        self.sample_shape and self._vs() controls the shape of the
        result.
        """
        assert sigma.shape == mean.shape
        variate_site = self._vs(sigma, var_in_last_axis)

        oldsettings = seterr(over='ignore')
        # self.sample_shape and variate_site will have compatible dims
        sample_values = self.val_func(mean[self.sample_shape] + 
                                      variate_site * sigma[self.sample_shape])
        seterr(**oldsettings)
        return sample_values

class Distribution_Log_Normal(Distribution):
    """
    Provides a way to pick log-normally distributed samples from a set
    of normal distributions characterised by mean and
    standard-deviation parameters.

    """
    
    def __init__(self, var_method):
        super(Distribution_Log_Normal, self).__init__(var_method)
        self.val_func = exp
        
class Distribution_Normal(Distribution):
    """
    Provides a way to pick normally distributed samples from a set
    of normal distributions characterised by mean and
    standard-deviation parameters.

    """
    
    def __init__(self, var_method):
        super(Distribution_Normal, self).__init__(var_method)
        self.val_func = lambda x: x


class GroundMotionDistributionLogNormal(Distribution_Log_Normal):
    """
    As per Distribution_Log_Normal but allows spawning and handles multiple
    recurrence models
    """
    def __init__(self,
                 var_method,
                 atten_spawn_bins,
                 n_recurrence_models):
        super(GroundMotionDistributionLogNormal, self).__init__(var_method)
        self.n_recurrence_models = n_recurrence_models
        if var_method == None:
            atten_spawn_bins = 1
        sigma_delta = 2.5
        weights, centroids = normalised_pdf(sigma_delta, atten_spawn_bins)
        self.spawn_weights = weights
        # Get the dimensions ready for applying to log_sigma's
        self.spawn_centroids = centroids #.reshape(1,-1)        

    sample_shape = (slice(None), newaxis, Ellipsis) 
    # Makes ._monte_carlo() insert a
    # recurence model axis after  gmm. Will get broadcasted in ._monte_carlo()

    
    def _spawn(self, log_mean, log_sigma):
        """
        Spawning will add a spawning dimension, as the first dimension.
        Each cut into the spawning dimension represents the SA at
        a different centroid.
        """
        new_shape = list(log_sigma.shape) + [1]
        log_sigma = log_sigma.reshape(new_shape)
        spawned_log_sigma = log_sigma * self.spawn_centroids
        # roll the spawn dimension to the front
        spawned_log_sigma = rollaxis(spawned_log_sigma,
                                     spawned_log_sigma.ndim-1, 0)
        sample_values = exp(log_mean + spawned_log_sigma)
        return sample_values

    
    def _vs(self, log_sigma, var_in_last_axis):
        # Overriding to cater for multiple recurrence models. 
        # Called by ._monte_carlo()
        ngmm, ns, ne, np = log_sigma.shape
        if  var_in_last_axis:
            s = (ngmm, self.n_recurrence_models, ns, ne, np)
            new_size = log_sigma.size * self.n_recurrence_models
        else:
            s = (ngmm, self.n_recurrence_models, ns, ne, 1)
            new_size = log_sigma.size * self.n_recurrence_models / np

        variate = self.rvs(size = new_size).reshape(s)
      
        if not var_in_last_axis:
            variate = repeat(variate, np, axis=3)
        return variate

    def ground_motion_sample(self, log_mean, log_sigma):
        """
        Like .sample_for_eqrm() but adds spawn and recurrence_model dimensions.

        log_mean, log_sigma: ndarray[gmm, site, event, period]. These
        represent the mean and standard deviation of the predicted
        spectral accelerations (indexed by period) at a site due to an
        event, as calculated by the attenuation model indexed by
        gmm. See the ground_motion_interface module for more
        information.

        Returns: ndarray[spawn, GMmodel, rec_model, site, event,
        period] spectral accelerations, measured in G.
        
        """
        assert log_mean.ndim == 4
        s = (self._spawn(log_mean, log_sigma) if self.var_method == SPAWN
             else self.sample_for_eqrm(log_mean, log_sigma)[newaxis, ...])

        if self.var_method == 2: # monte_carlo has added and populated
                                 # the recurrence model dimension
            return s

        # Add the recurrence model dimension and "manually" broadcast
        # it so that our caller doesn't have to treat this as a
        # special case.
        return repeat(s[:, :, newaxis, :, :, :],
                      self.n_recurrence_models,
                      2)
    
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
