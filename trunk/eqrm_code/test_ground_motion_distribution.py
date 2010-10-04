import os
import sys

import unittest
from ground_motion_distribution import *
from scipy import array, log, exp, newaxis, concatenate, allclose, sqrt, \
     r_, alltrue, where, arange, resize


class Test_Log_normal_distribution(unittest.TestCase):
   
    def test_monte_carlo2(self):
        log_mean=array([[1.,2,3],[5,6,7],[9,11,13]])[...,newaxis]
        log_sigma=array([[1.,1.5,4],[1,1,1],[2,3,4]])[...,newaxis]
        variate_eq=array([[20,5,4],[.5,.2,.1],[19,4,5]])[...,newaxis]
        atten_log_sigma_eq_weight=0.3

        var_method = 2
        dist=Log_normal_distribution(var_method, 
            num_psudo_events=log_mean.shape[1],
            variate_eq=variate_eq,
            atten_log_sigma_eq_weight=atten_log_sigma_eq_weight)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)

        variate_site=array([[2,56,42],[5.5,3.2,9.1],[9,46,51]])[...,newaxis]
        sample_values = dist._monte_carlo_intra_inter(
            variate_site=variate_site)
        actual = exp(
            log_mean + atten_log_sigma_eq_weight*variate_eq*log_sigma + \
            (1-atten_log_sigma_eq_weight)*variate_site*log_sigma)        
        assert allclose(sample_values,actual)
        
        variate_site=array([[26,56,2],[.5,3.,.1],[.9,.46,.51]])[...,newaxis]
        sample_values = dist._monte_carlo_intra_inter(
            variate_site=variate_site)
        
        actual = exp(
            log_mean + atten_log_sigma_eq_weight*variate_eq*log_sigma + \
            (1-atten_log_sigma_eq_weight)*variate_site*log_sigma)
        assert allclose(sample_values,actual)
              
    def test_monte_carlo3(self):
        log_mean=array([[1.,2,3],[5,6,7],[9,11,13]])[...,newaxis]
        log_sigma=array([[1.,1.5,4],[1,1,1],[2,3,4]])[...,newaxis]
        variate_eq=array([[20,5,4],[.5,.2,.1],[19,4,5]])[...,newaxis]

        var_method = 2
        atten_log_sigma_eq_weight = 1
        dist=Log_normal_distribution(var_method, \
            num_psudo_events=log_mean.shape[1],
            variate_eq=variate_eq,
            atten_log_sigma_eq_weight=atten_log_sigma_eq_weight)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)

        sample_values = dist._monte_carlo_intra_inter()
        actual = exp(
            log_mean + atten_log_sigma_eq_weight*variate_eq*log_sigma)      
        assert allclose(sample_values,actual)

        event_activity=dist.sample_for_eqrm()     
        assert allclose(sample_values,actual)
        

    def test_monte_carlo4(self):
        log_mean=array([[1.,2,3],[5,6,7],[9,11,13]])[...,newaxis]
        log_sigma=array([[1.,1.5,4],[1,1,1],[2,3,4]])[...,newaxis]
        atten_log_sigma_eq_weight=0.0

        var_method = 2
        dist=Log_normal_distribution(var_method, 
            num_psudo_events=log_mean.shape[1],
            atten_log_sigma_eq_weight=atten_log_sigma_eq_weight)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)

        variate_site=array([[2,56,42],[5.5,3.2,9.1],[9,46,51]])[...,newaxis]
        sample_values = dist._monte_carlo_intra_inter(
            variate_site=variate_site)
        actual = exp(
            log_mean + (1-atten_log_sigma_eq_weight)*variate_site*log_sigma)
        assert allclose(sample_values,actual)
        
    def test_no_variability(self):
        log_mean=array([[1.,2,3],[5,6,7],[9,11,13]])[...,newaxis]
        log_sigma=array([[1.,1.5,4],[1,1,1],[2,3,4]])[...,newaxis]
        atten_log_sigma_eq_weight=0.0

        var_method = None
        dist=Log_normal_distribution(var_method, 
            num_psudo_events=log_mean.shape[1],
            atten_log_sigma_eq_weight=atten_log_sigma_eq_weight)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)

        (_, sample_values, _) = dist.sample_for_eqrm()
        actual = exp(log_mean )
        assert allclose(sample_values,actual)
        
    def test_plus_2_sigma(self):
        log_mean=array([[1.,2,3],[5,6,7],[9,11,13]])[...,newaxis]
        log_sigma=array([[1.,1.5,4],[1,1,1],[2,3,4]])[...,newaxis]
        atten_log_sigma_eq_weight=0.0

        var_method = 3
        dist=Log_normal_distribution(var_method, 
            num_psudo_events=log_mean.shape[1],
            atten_log_sigma_eq_weight=atten_log_sigma_eq_weight)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)

        (_, sample_values, _) = dist.sample_for_eqrm()
        actual = exp(log_mean + 2*log_sigma)
        assert allclose(sample_values,actual)

        
    def test_plus_sigma(self):
        log_mean=array([[1.,2,3],[5,6,7],[9,11,13]])[...,newaxis]
        log_sigma=array([[1.,1.5,4],[1,1,1],[2,3,4]])[...,newaxis]
        atten_log_sigma_eq_weight=0.0

        var_method = 4
        dist=Log_normal_distribution(var_method, 
            num_psudo_events=log_mean.shape[1],
            atten_log_sigma_eq_weight=atten_log_sigma_eq_weight)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)

        (_, sample_values, _) = dist.sample_for_eqrm()
        actual = exp(log_mean + log_sigma)
        assert allclose(sample_values,actual)

    def test_neg_sigma(self):
        log_mean=array([[1.,2,3],[5,6,7],[9,11,13]])[...,newaxis]
        log_sigma=array([[1.,1.5,4],[1,1,1],[2,3,4]])[...,newaxis]
        atten_log_sigma_eq_weight=0.0

        var_method = 5
        dist=Log_normal_distribution(var_method, 
            num_psudo_events=log_mean.shape[1],
            atten_log_sigma_eq_weight=atten_log_sigma_eq_weight)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)

        (_, sample_values, _) = dist.sample_for_eqrm()
        actual = exp(log_mean - log_sigma)
        assert allclose(sample_values,actual)
        
    def test_neg_2_sigma(self):
        log_mean=array([[1.,2,3],[5,6,7],[9,11,13]])[...,newaxis]
        log_sigma=array([[1.,1.5,4],[1,1,1],[2,3,4]])[...,newaxis]
        atten_log_sigma_eq_weight=0.0

        var_method = 6
        dist=Log_normal_distribution(var_method, 
            num_psudo_events=log_mean.shape[1],
            atten_log_sigma_eq_weight=atten_log_sigma_eq_weight)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)

        (_, sample_values, _) = dist.sample_for_eqrm()
        actual = exp(log_mean - 2*log_sigma)
        assert allclose(sample_values,actual)


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
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)
        sample_values = dist._monte_carlo(variate_site=variate)
        
        actual = exp(log_mean + variate*log_sigma)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)


    def test_DLN_no_variability(self):
        # dimensions (2,1,3,4) = 24 elements
        dim = (2,1,3,4)
        count_up = arange(1,24,1)
        log_mean = resize(count_up*10, dim)
        log_sigma = resize(count_up, dim)
        var_method = None
        
        dist = Distribution_Log_Normal(var_method)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)
        (_, sample_values, _) = dist.sample_for_eqrm()
        
        actual = exp(log_mean)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)

        
    def test_DLN_sigmas(self):
        # dimensions (2,1,3,4) = 24 elements
        dim = (2,1,3,4)
        count_up = arange(1,24,1)
        log_mean = resize(count_up*10, dim)
        log_sigma = resize(count_up, dim)
        
        var_method = 3       
        dist = Distribution_Log_Normal(var_method)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)
        (_, sample_values, _) = dist.sample_for_eqrm()       
        actual = exp(log_mean + 2*log_sigma)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)

        var_method = 4      
        dist = Distribution_Log_Normal(var_method)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)
        (_, sample_values, _) = dist.sample_for_eqrm()       
        actual = exp(log_mean + log_sigma)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)
        
        var_method = 5      
        dist = Distribution_Log_Normal(var_method)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)
        (_, sample_values, _) = dist.sample_for_eqrm()       
        actual = exp(log_mean - log_sigma)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)
        
        var_method = 6    
        dist = Distribution_Log_Normal(var_method)
        dist.set_log_mean_log_sigma_etc(log_mean,log_sigma)
        (_, sample_values, _) = dist.sample_for_eqrm()       
        actual = exp(log_mean - 2*log_sigma)
        self.assert_(allclose(sample_values, actual))
        self.assert_(actual.shape == dim)

        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Log_normal_distribution,'test')
    #suite = unittest.makeSuite(Test_Log_normal_distribution,'test_monte_carlo2')
    runner = unittest.TextTestRunner()
    runner.run(suite)
