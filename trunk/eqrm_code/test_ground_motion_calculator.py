
import unittest

from scipy import array, exp, log, allclose, newaxis, asarray

from eqrm_code.ground_motion_specification import *
from eqrm_code.ground_motion_interface import gound_motion_init
from eqrm_code.ground_motion_misc import \
     Australian_standard_model_interpolation 
from eqrm_code.ground_motion_calculator import Ground_motion_calculator, \
     Multiple_ground_motion_calculator


from eqrm_code.test_ground_motion_specification import \
     ground_motion_interface_conformance, data2atts, Distance_stub

class Test_ground_motion_calculator(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def ground_motion_interface_conformance(self, GM_class, model_name):
        median, test_mean = ground_motion_interface_conformance(
            GM_class, model_name)
        self.assert_(allclose(median, test_mean, rtol=0.05),
                     "%s did not pass assert" %model_name )
        
    def test_toro_conformance(self):
        GM_model_name = 'Toro_1997_midcontinent'
        self.ground_motion_interface_conformance(Ground_motion_calculator,
                                                 GM_model_name)

    def no_test_single_conformance(self):
        GM_model_name = 'Youngs_97'
        self.ground_motion_interface_conformance(Ground_motion_calculator,
                                                 GM_model_name)
            
    def test_log_mean(self):
        """
        This checks that for the given test_distance and test_magnitudes,
        the calculated ground motion is the same as the test_ground_motion
        """
        
        model_name = 'Toro_1997_midcontinent'
        (distances, magnitudes,
         test_mean, periods, depths, _, _, _, _, _) = data2atts(model_name)
        
        event_activity = 0.5
        
        gm = Ground_motion_calculator(model_name, periods=periods)
        
        log_mean,log_sigma=gm.distribution_function(
            distances, magnitudes,
            depth=depths,
            event_activity=event_activity)
        
        self.assert_(allclose(exp(log_mean), test_mean, rtol=0.05),
                     "%s did not pass assert" %model_name )
       
    def test_log_sigma_BA08(self):
        model_name = 'Boore_08'
        
        (distances, magnitudes, test_mean,
         periods, depths, _, _, _, _, _) = data2atts('Toro_1997_midcontinent')
        event_activity = 0.5
        periods = array([0.015, 0.45, 4.5 ])
        
        gm = Ground_motion_calculator(model_name, periods=periods)
        
        log_mean,log_sigma=gm.distribution_function(
            distances, magnitudes,
            depth=depths,
            event_activity=event_activity,
            vs30=560.0)
        test_log_sigma = array([0.569, 0.609, 0.716])
        #print "log_sigma", log_sigma
        #FIXME check the shape as well
        self.assert_(allclose(log_sigma, test_log_sigma, rtol=0.05),
                     "%s did not pass assert" %model_name )
        
    def test_log_sigma_Somerville_Yilgarn(self):
        model_name = 'Somerville_Yilgarn'
        
        (distances, magnitudes, test_mean,
         periods, depths, _, _, _, _, _) = data2atts('Toro_1997_midcontinent')
        event_activity = 1
        periods = array([0.010, 0.045, 1.0 ])
        
        gm = Ground_motion_calculator(model_name, periods=periods)
        
        log_mean,log_sigma=gm.distribution_function(
            distances, magnitudes,
            depth=depths,
            event_activity=event_activity)
        test_log_sigma = array([0.5512, 0.55095, 0.6817])
        #FIXME check the shape as well
        self.assert_(allclose(log_sigma, test_log_sigma, rtol=0.0000005),
                     "%s did not pass assert" %model_name )

        
    def test_event_activityII(self):
        """
        This checks that for the given test_distance and test_magnitudes,
        the calculated ground motion is the same as the test_ground_motion
        """
        
        model_name = 'Combo_Sadigh_Youngs_M8_trimmed'        
        (distances, magnitudes,
         test_mean, periods, depths, _, _, _, _, _) = data2atts(model_name)

        model_name2 = 'Youngs_97_interface'        
        (dist2 , mag2, test_mean2,
         periods2, depths2, _, _, _, _, _) = data2atts(model_name2)

        self.assert_(allclose(distances.distance(None), dist2.distance(None)))
        self.assert_(magnitudes == mag2)
        self.assert_(periods == periods2)
        self.assert_(depths == depths2)
        
        model_name = 'Combo_Sadigh_Youngs_M8'

        model_names = [model_name, model_name2]
        model_weights = array([0.1, 0.9])
        gm = Multiple_ground_motion_calculator(model_names,
                                               periods,
                                               model_weights)
        
        log_mean, log_sigma,_, _ = gm._distribution_function(
            distances, magnitudes,
            depths,
            None, None) 
        
        mean_out = []
        for i in range(len(distances.distance(None))):
            mean_out.append([test_mean[i][0], test_mean2[i][0]])
        #print "mean_out", mean_out
        #print "distribution.median", distribution.median
        self.assert_(allclose(exp(log_mean), mean_out, rtol=0.05),
                     "Fail")
    
    
    def test_mult_gm(self):
        """
        This checks that for the given test_distance and test_magnitudes,
        the calculated ground motion is the same as the test_ground_motion
        """

        model_name = 'Toro_1997_midcontinent'
        
        (distances, magnitudes,
         test_mean, periods, depths, _, _, _, _, _) = data2atts(model_name)
        
        model_weights = [1]
        gm = Multiple_ground_motion_calculator(
            [model_name], periods, model_weights)

        # ignoring event_activity, event_id
        log_mean,log_sigma, _, _ =gm._distribution_function(
            distances, magnitudes,
            depth=depths)
        
        self.assert_(allclose(exp(log_mean), test_mean, rtol=0.05),
                     "%s did not pass assert" %model_name  )
        

        
#------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_ground_motion_calculator,'test')
    #suite = unittest.makeSuite(Test_ground_motion_calculator,'test_event_activityII')
    runner = unittest.TextTestRunner()
    runner.run(suite)
