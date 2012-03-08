import os
import sys

import unittest
from ground_motion_distribution import *
from scipy import array, log, exp, newaxis, concatenate, allclose, sqrt, \
     r_, alltrue, where, arange, resize, sum, ones, seterr

from eqrm_code import perf

class Test_Log_normal_distribution(unittest.TestCase):
   
    @perf.benchmark
    def test_DLN_monte_carlo2(self):
        # dimensions (2,1,3,4) = 24 elements
        dim = (2,1,3,4)
        count_up = arange(1,24,1)
        log_mean = resize(count_up*10, dim)
        log_sigma = resize(count_up, dim)
        count_up_2 = arange(1,48,2)
        variate = resize(count_up_2, dim)
        var_method = 2
        
        dist = Distribution_Log_Normal(var_method)
        # Provide a predictable sample
        dist.rvs = lambda size: count_up_2
        sample_values = dist._monte_carlo(log_mean, log_sigma)
        
        oldsettings = seterr(over='ignore')
        actual = exp(log_mean + variate*log_sigma)
        seterr(**oldsettings)
        self.assert_(allclose(sample_values, actual))
        self.assert_(sample_values.shape == dim)

    @perf.benchmark
    def test_DLN_monte_carlo3(self):
        dim = (1,2,3)
        count_up = arange(0,6,1)
        log_mean = resize(count_up*10, dim)
        log_sigma = resize(count_up, dim)
        count_up_2 = arange(1,48,2)
        var_method = 2
        
        dist = Distribution_Log_Normal(var_method)
        sample_values = dist._monte_carlo(log_mean,log_sigma)

        # Can not check result, it's random 
        self.assert_(sample_values.shape == dim)

    @perf.benchmark
    def test_DLN_no_variability(self):
        # dimensions (2,1,3,4) = 24 elements
        dim = (2,1,3,4)
        count_up = arange(1,24,1)
        log_mean = resize(count_up*10, dim)
        log_sigma = resize(count_up, dim)
        var_method = None
        
        dist = Distribution_Log_Normal(var_method)
        sample_values = dist.sample_for_eqrm(log_mean,log_sigma)

        actual = exp(log_mean)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)

    @perf.benchmark
    def test_DLN_sigmas(self):
        # dimensions (2,1,3,4) = 24 elements
        dim = (2,1,3,4)
        count_up = arange(1,24,1)
        log_mean = resize(count_up*10, dim)
        log_sigma = resize(count_up, dim)
        
        var_method = 3       
        dist = Distribution_Log_Normal(var_method)
        sample_values = dist.sample_for_eqrm(log_mean,log_sigma)
        actual = exp(log_mean + 2*log_sigma)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)

        var_method = 4      
        dist = Distribution_Log_Normal(var_method)
        sample_values = dist.sample_for_eqrm(log_mean,log_sigma)
        actual = exp(log_mean + log_sigma)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)
        
        var_method = 5      
        dist = Distribution_Log_Normal(var_method)
        sample_values = dist.sample_for_eqrm(log_mean,log_sigma)
        actual = exp(log_mean - log_sigma)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)
        
        var_method = 6    
        dist = Distribution_Log_Normal(var_method)
        sample_values = dist.sample_for_eqrm(log_mean,log_sigma)
        actual = exp(log_mean - 2*log_sigma)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)       

    @perf.benchmark
    def test_normalised_pdf(self):
        sigma_delta = 3
        number_of_bins = 1
        weights, centroids = normalised_pdf(sigma_delta, number_of_bins)
        self.assert_(weights[0] == 1)       
        self.assert_(len(weights) == 1)    
        self.assert_(centroids == 0)       
        self.assert_(len(centroids) == 1)       
        
    @perf.benchmark
    def test_normalised_pdfII(self):
        sigma_delta = 2.5
        number_of_bins = 2
        weights, centroids = normalised_pdf(sigma_delta, number_of_bins)
        self.assert_(allclose(weights, [0.5,0.5]))       
        self.assert_(len(weights) == 2)    
        self.assert_(allclose(centroids, [-2.5, 2.5]))       
        self.assert_(len(centroids) == 2)
        
    @perf.benchmark
    def test_normalised_pdf3(self):
        sigma_delta = 2.5
        number_of_bins = 10
        weights, centroids = normalised_pdf(sigma_delta, number_of_bins)
        act_cends = array([-2.5000, -1.9444, -1.3889, -0.8333,
                                          -0.2778, 0.2778, 0.8333, 1.3889,
                                          1.9444, 2.5])
        #print "centroids", centroids
        #print "act_cends", act_cends
        self.assert_(allclose(centroids, act_cends, 0.001))       
        self.assert_(len(centroids) == 10)
        
        act_unnormed_wts = [0.0175, 0.0602, 0.1521, 0.2819,
                                        0.3838, 0.3838, 0.2819, 0.1521,
                                        0.0602, 0.0175]
        act_wts = act_unnormed_wts/sum(act_unnormed_wts)
        #print "act_wts", act_wts
        #print "weights", weights
        self.assert_(allclose(weights, act_wts, 0.01))       
        self.assert_(len(weights) == 10)

    @perf.benchmark
    def test_spawning(self):
        spawn_bins = 2

        dln = GroundMotionDistributionLogNormal(var_method=SPAWN,
                                                atten_spawn_bins=spawn_bins,
                                                n_recurrence_models=1)
        log_mean = ones((1, 1, 3,4))
        log_mean *= 10
        log_sigma = ones((1, 1, 3,4))
        sample_values = dln.ground_motion_sample(log_mean,log_sigma)
        act_SA_0 = ones((1, 1, 1, 1, 3, 4)) * (10 - 2.5)
        act_SA_1 = ones((1, 1, 1, 1, 3, 4)) * (10 + 2.5)
        act_SA = exp(concatenate((act_SA_0, act_SA_1)))
        self.assert_(allclose(act_SA, sample_values))   
        
    @perf.benchmark
    def test_spawningII(self):
        spawn_bins = 3

        dln = GroundMotionDistributionLogNormal(var_method=SPAWN,
                                                atten_spawn_bins=spawn_bins,
                                                n_recurrence_models=1)
        log_mean = ones((1, 2, 3, 4))
        log_mean *= 10
        log_sigma = ones((1, 2, 3, 4))
        sample_values = dln.ground_motion_sample(log_mean,log_sigma)
        act_SA_0 = ones((1, 1, 1, 2, 3, 4)) * (10 - 2.5)
        act_SA_1 = ones((1, 1, 1, 2, 3, 4)) * (10)
        act_SA_2 = ones((1, 1, 1, 2, 3, 4)) * (10 + 2.5)
        act_SA = exp(concatenate((act_SA_0, act_SA_1, act_SA_2)))
        self.assert_(allclose(act_SA, sample_values))
               
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Log_normal_distribution,'test')
    #suite = unittest.makeSuite(Test_Log_normal_distribution,'test_DLN_monte_carlo')
    runner = unittest.TextTestRunner() #verbosity=2
    runner.run(suite)
