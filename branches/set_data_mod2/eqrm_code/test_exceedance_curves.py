import os
import sys
import unittest

from scipy import allclose, array

from eqrm_code.exceedance_curves import *


class Dummy:
    def __init__(self):
        pass
    
class Test_Exceedance(unittest.TestCase):
    def test_exceedance_curve(self):
        # WARNING - MORE A BLACK BOX TEST - BASED ON THE FUNCTIONS OUTPUT,
        # RATHER THAN
        # WHAT IT SHOULD OUTPUT.
        total_building_loss = array([[[ 2080.59298432],
                                      [  807.57878512],
                                      [    0.        ]]])
        index = [0, 0, 0]
        event_activity = [ -0.33333333, -0.33333333,
                                               -0.33333333]
        THE_PARAM_T = Dummy()
        THE_PARAM_T.atten_models = ['Toro_1997_midcontinent',
                                   'Atkinson_Boore_97','Sadigh_97']
        THE_PARAM_T.atten_model_weights = [0.33333333, 0.33333333,
                                               0.33333333]
        THE_PARAM_T.atten_aggregate_Sa_of_atten_models = False
        THE_PARAM_T.src_eps_switch = 1
        THE_PARAM_T.atten_use_variability = True  
        THE_PARAM_T.atten_variability_method = 2 
        THE_PARAM_T.nsamples = 5
        #THE_PARAM_T. = 
        new_total_building_loss, _, _ = do_collapse_logic_tree( \
            total_building_loss,
            index,
            event_activity,
            THE_PARAM_T)
        self.assert_ (allclose(new_total_building_loss, total_building_loss))

        
    def not_test_exceedance_curveII(self):
        # WARNING - MORE A BLACK BOX TEST - BASED ON THE FUNCTIONS OUTPUT,
        # RATHER THAN
        # WHAT IT SHOULD OUTPUT.
        soil_SA = array([[[ 0.63811513,1.1250657, 0.95676206,0.65757182,
                            0.50477204,0.43550808,
                            0.382534,0.35354727,0.3254525, 0.298879,
                            0.27410818,0.25116205,
                            0.22970222,0.2098289, 0.19167379,0.17476049,
                            0.1592502, 0.14510788,
                            0.13222767,0.12049001],
                          [ 0.64301661,1.42372189,1.02827427,0.7456123,
                            0.5216206, 0.38232683,
                             0.30686253,0.26976046,0.24118183,0.21767101,
                            0.19727918,0.17933642,
                             0.1630807, 0.14834511,0.13494016,0.1227293,
                            0.11162576,0.10152067,
                             0.09233478,0.08397954],
                          [ 0.93308996,1.75097807,1.08595565,0.69098001,
                            0.40613985,0.26219224,
                            0.18944009,0.14479323,0.11834137,0.09839466,
                            0.08218122,0.06886769,
                            0.06393146,0.06354505,0.06316098,0.06278116,
                            0.06240455,0.06202999,
                            0.06165789,0.06128802]
,[ 0.68081776,1.35968336,0.83233801,0.54541128,0.31384392,0.19515477
,  0.13810567,0.10431534,0.08466327,0.07009283,0.05836801,0.04881033
,  0.04524745,0.04493017,0.04461511,0.04432146,0.04403633,0.04375288
,  0.04347141,0.04319176]
,[ 0.55339867,1.59387482,1.56301778,1.04489446,0.65405138,0.48026192
,  0.38166964,0.31708251,0.26682543,0.22965146,0.20204715,0.17815543
,  0.15943943,0.1441247, 0.13028101,0.11768048,0.1062808, 0.09597983
,  0.08848198,0.08175583]
,[ 0.52814312,1.90746337,1.54929322,1.16198595,0.57701843,0.37086656
,  0.27604003,0.22161678,0.18278793,0.15542678,0.13559712,0.11886919
  ,0.10596113,0.09552351,0.08611405,0.07765319,0.07003567,0.06316169
  ,0.05814846,0.0536552 ]]])
        index = [0, 1, 0, 1, 0, 1]
        event_activity = array([ 0.33333333, 0.33333333, 0.33333333,
                                 0.33333333, 0.33333333, 0.33333333])
        THE_PARAM_T = Dummy()
        THE_PARAM_T.atten_models = ['Toro_1997_midcontinent',
                                   'Atkinson_Boore_97','Sadigh_97']
        THE_PARAM_T.atten_model_weights = [0.33333333, 0.33333333,
                                               0.33333333]
        THE_PARAM_T.atten_aggregate_Sa_of_atten_models = True
        THE_PARAM_T.src_eps_switch = 0
        THE_PARAM_T.atten_use_variability = True  
        THE_PARAM_T.atten_variability_method = 2 
        THE_PARAM_T.nsamples = 5

        new_soil_SA = [[[0.70820126, 1.48997287, 1.20191183, 0.79781543,
                         0.52165442, 0.39265408
,   0.31788124, 0.27180767, 0.2368731,  0.20897504, 0.18611218, 0.16606172
  , 0.15102437, 0.13916622, 0.12837193, 0.11840738, 0.10931185, 0.10103923
,   0.09412251, 0.08784462]
, [ 0.61732583, 1.56362287, 1.13663517, 0.81766984, 0.47082765, 0.31611605
,   0.24033608, 0.1985642,  0.16954435, 0.14773021, 0.13041477, 0.11567198
,   0.10476309, 0.09626626, 0.08855644, 0.08156798, 0.07523259, 0.06947842
,   0.06465155, 0.0602755 ]]]

        results, _, _ = do_collapse_logic_tree( \
            soil_SA,
            index,
            event_activity,
            THE_PARAM_T)
        self.assert_ (allclose(results, new_soil_SA))
        
    def test_exceedance_curveIII(self):
        
        # WARNING - MORE A BLACK BOX TEST - BASED ON THE FUNCTIONS OUTPUT,
        # RATHER THAN
        # WHAT IT SHOULD OUTPUT.
        soil_SA = array([[[ 0.63811513,1.1250657, 0.95676206,0.65757182,
                            0.50477204,0.43550808,
                            0.382534,0.35354727,0.3254525, 0.298879,
                            0.27410818,0.25116205,
                            0.22970222,0.2098289, 0.19167379,0.17476049,
                            0.1592502, 0.14510788,
                            0.13222767,0.12049001],
                          [ 0.64301661,1.42372189,1.02827427,0.7456123,
                            0.5216206, 0.38232683,
                             0.30686253,0.26976046,0.24118183,0.21767101
                            ,0.19727918,0.17933642,
                             0.1630807, 0.14834511,0.13494016,0.1227293,
                            0.11162576,0.10152067,
                             0.09233478,0.08397954],
                          [ 0.93308996,1.75097807,1.08595565,0.69098001,
                            0.40613985,0.26219224,
                            0.18944009,0.14479323,0.11834137,0.09839466
                            ,0.08218122,0.06886769,
                            0.06393146,0.06354505,0.06316098,0.06278116,
                            0.06240455,0.06202999,
                            0.06165789,0.06128802]
,[ 0.68081776,1.35968336,0.83233801,0.54541128,0.31384392,0.19515477
,  0.13810567,0.10431534,0.08466327,0.07009283,0.05836801,0.04881033
,  0.04524745,0.04493017,0.04461511,0.04432146,0.04403633,0.04375288
,  0.04347141,0.04319176]
,[ 0.55339867,1.59387482,1.56301778,1.04489446,0.65405138,0.48026192
,  0.38166964,0.31708251,0.26682543,0.22965146,0.20204715,0.17815543
,  0.15943943,0.1441247, 0.13028101,0.11768048,0.1062808, 0.09597983
,  0.08848198,0.08175583]
,[ 0.52814312,1.90746337,1.54929322,1.16198595,0.57701843,0.37086656
,  0.27604003,0.22161678,0.18278793,0.15542678,0.13559712,0.11886919
  ,0.10596113,0.09552351,0.08611405,0.07765319,0.07003567,0.06316169
  ,0.05814846,0.0536552 ]]])
        index = [0, 1, 0, 1, 0, 1]
        event_activity = [ 0.33333333, 0.33333333, 0.33333333,
                           0.33333333, 0.33333333, 0.33333333]
        THE_PARAM_T = Dummy()
        THE_PARAM_T.atten_models = ['Gaull_1990_WA', 'Toro_1997_midcontinent',
                                   'Atkinson_Boore_97']
        THE_PARAM_T.atten_model_weights = [0.33333333, 0.33333333,
                                               0.33333333]
        THE_PARAM_T.atten_aggregate_Sa_of_atten_models = True
        THE_PARAM_T.src_eps_switch = 0
        THE_PARAM_T.atten_use_variability = True  
        THE_PARAM_T.atten_variability_method = 2 
        THE_PARAM_T.nsamples = 5

        new_soil_SA = [[[0.70820126, 1.48997287, 1.20191183, 0.79781543,
                         0.52165442, 0.39265408
,   0.31788124, 0.27180767, 0.2368731,  0.20897504, 0.18611218, 0.16606172
  , 0.15102437, 0.13916622, 0.12837193, 0.11840738, 0.10931185, 0.10103923
,   0.09412251, 0.08784462]
, [ 0.61732583, 1.56362287, 1.13663517, 0.81766984, 0.47082765, 0.31611605
,   0.24033608, 0.1985642,  0.16954435, 0.14773021, 0.13041477, 0.11567198
,   0.10476309, 0.09626626, 0.08855644, 0.08156798, 0.07523259, 0.06947842
,   0.06465155, 0.0602755 ]]]

        results, _, _ = do_collapse_logic_tree( \
            soil_SA,
            index,
            event_activity,
            THE_PARAM_T)
        self.assert_ (allclose(results, new_soil_SA))
        
    def test_exceedance_curve4(self):
        
        # WARNING - MORE A BLACK BOX TEST - BASED ON THE FUNCTIONS OUTPUT,
        # RATHER THAN
        # WHAT IT SHOULD OUTPUT.
        soil_SA = array([[[ 0.63811513],
                          [ 0.64301661],
                          [ 0.93308996]
                          ,[ 0.68081776]
                          ,[ 0.55339867]
                          ,[ 0.52814312 ]]])
        index = [0, 1, 0, 1, 0, 1]

        # The length is used, not the values
        event_activity = [ 0.33333333, 0.33333333, 0.33333333,
                           0.33333333, 0.33333333, 0.33333333]
        THE_PARAM_T = Dummy()
        
        THE_PARAM_T.atten_models = ['Toro_1997_midcontinent',
                                   'Atkinson_Boore_97','Sadigh_97']
        THE_PARAM_T.atten_model_weights = [0.33333333, 0.33333333,
                                               0.33333333]
        THE_PARAM_T.atten_aggregate_Sa_of_atten_models = True
        THE_PARAM_T.src_eps_switch = 0
        THE_PARAM_T.atten_use_variability = True  
        THE_PARAM_T.atten_variability_method = 2 
        THE_PARAM_T.nsamples = 5

        new_soil_SA = [[[0.70820126]
, [ 0.61732583]]]

        results, _, _ = do_collapse_logic_tree( \
            soil_SA,
            index,
            event_activity,
            THE_PARAM_T)
        self.assert_ (allclose(results, new_soil_SA))
        
    def test_exceedance_curve5(self):
        # Treating it as a black box and working out what it does
        soil_SA = array([[[ 1],
                          [ 70],
                          [ 3]
                          ,[ 60]
                          ,[ 2]
                          ,[ 80]]])
        index = [0, 1, 0, 1, 0, 1] # The event id
        
        # The length is used, not the values
        event_activity = [ 0.33333333, 0.33333333, 0.33333333,
                           0.33333333, 0.33333333, 0.33333333]
        THE_PARAM_T = Dummy()
        THE_PARAM_T.atten_models = ['Toro_1997_midcontinent',
                                   'Atkinson_Boore_97','Sadigh_97']
        THE_PARAM_T.atten_model_weights = [0.33333333, 0.33333333,
                                               0.33333333]
        THE_PARAM_T.atten_aggregate_Sa_of_atten_models = True
        THE_PARAM_T.src_eps_switch = 0
        THE_PARAM_T.atten_use_variability = True  
        THE_PARAM_T.atten_variability_method = 2 
        THE_PARAM_T.nsamples = 5

        new_soil_SA = [[[2]
                        , [ 70]]]
        results, _, _ = do_collapse_logic_tree( \
            soil_SA,
            index,
            event_activity,
            THE_PARAM_T)
        #print "results", results
        self.assert_ (allclose(results, new_soil_SA))
        
    def test_exceedance_curve6(self):
        # Treating it as a black box and working out what it does
        soil_SA = array([[[ 1],
                          [ 2],
                          [ 3]
                          ,[ 4]
                          ,[ 5]
                          ,[ 6]]])
        index = [0, 1, 0, 1, 0, 1] # The event id
        event_activity = [10., 10., 1, 1., .1, .1]

        
        THE_PARAM_T = Dummy()
        
        THE_PARAM_T.atten_models = ['Gaull_1990_WA', 'Toro_1997_midcontinent',
                                   'Atkinson_Boore_97']
        THE_PARAM_T.atten_model_weights = [10., 1.,
                                               0.1]
        THE_PARAM_T.atten_aggregate_Sa_of_atten_models = True
        THE_PARAM_T.src_eps_switch = 0
        THE_PARAM_T.atten_use_variability = True  
        THE_PARAM_T.atten_variability_method = 2 
        THE_PARAM_T.nsamples = 5

        new_soil_SA = [[[13.5]
                        , [ 24.6]]]
        results, _, _ = do_collapse_logic_tree( \
            soil_SA,
            index,
            event_activity,
            THE_PARAM_T)
        self.assert_ (allclose(results, new_soil_SA))
        
    def test_exceedance_curve7(self):
        # Treating it as a black box and working out what it does
        # Showing how if the atten_aggregate_Sa_of_atten_models is False
        # output = input.
        soil_SA = array([[[ 1],
                          [ 100],
                          [ 2]
                          ,[ 10]
                          ,[ 10]
                          ,[ 1]]])
        index = [0, 1, 0, 1, 0, 1] # The event id
        event_activity = [-999, -999, -9993, -99,-99,-99]

        THE_PARAM_T = Dummy()
        THE_PARAM_T.atten_model_weights = [1., 0., 0.1]
        THE_PARAM_T.atten_aggregate_Sa_of_atten_models = False
        
        THE_PARAM_T.atten_models = ['Toro_1997_midcontinent',
                                   'Atkinson_Boore_97','Sadigh_97']
        
        #  don't collapse.
        THE_PARAM_T.src_eps_switch = 0
        THE_PARAM_T.atten_use_variability = True  
        THE_PARAM_T.atten_variability_method = 2 
        THE_PARAM_T.nsamples = 5

        new_soil_SA = [[[5.6]
                        , [ 12.7]]]
        results, _, _ = do_collapse_logic_tree( \
            soil_SA,
            index,
            event_activity,
            THE_PARAM_T)
        #print "results", results
        self.assert_ (allclose(results, soil_SA))

     
    def test_exceedance_curve8(self):
        # Treating it as a black box and working out what it does
        soil_SA = array([[[ 1.],
                          [ 100.],
                          [ 2.],
                          [ 80],
                          [ 3.],
                          [ 120]]])
        index = [0, 1, 0, 1, 0, 1] # The event id
        event_activity = [0.33333, 0.33333, 0.33333, 0.33333, 0.33333, 0.33333]

        THE_PARAM_T = Dummy()
        THE_PARAM_T.atten_models = ['Toro_1997_midcontinent',
                                   'Atkinson_Boore_97','Sadigh_97']
        THE_PARAM_T.atten_model_weights = [0.33333333, 0.33333333,
                                               0.33333333]
        THE_PARAM_T.atten_aggregate_Sa_of_atten_models = True
        
        #  don't collapse.
        THE_PARAM_T.src_eps_switch = 0
        THE_PARAM_T.atten_use_variability = True  
        THE_PARAM_T.atten_variability_method = 2 
        THE_PARAM_T.nsamples = 5

        new_soil_SA = [[[2.]
                        , [ 100]]]
        results, _, _ = do_collapse_logic_tree( \
            soil_SA,
            index,
            event_activity,
            THE_PARAM_T)
        self.assert_ (allclose(results, new_soil_SA))

        
    def test_exceedance_curve_python_code(self):
        
        # WARNING - MORE A BLACK BOX TEST - BASED ON THE FUNCTIONS OUTPUT,
        # RATHER THAN
        # WHAT IT SHOULD OUTPUT.
        soil_SA = array([[[ 0.63811513,1.1250657, 0.95676206,0.65757182,
                            0.50477204,0.43550808,
                            0.382534,0.35354727,0.3254525, 0.298879,
                            0.27410818,0.25116205,
                            0.22970222,0.2098289, 0.19167379,0.17476049,
                            0.1592502, 0.14510788,
                            0.13222767,0.12049001],
                          [ 0.64301661,1.42372189,1.02827427,0.7456123,
                            0.5216206, 0.38232683,
                             0.30686253,0.26976046,0.24118183,0.21767101,
                            0.19727918,0.17933642,
                             0.1630807, 0.14834511,0.13494016,0.1227293,
                            0.11162576,0.10152067,
                             0.09233478,0.08397954],
                          [ 0.93308996,1.75097807,1.08595565,0.69098001,
                            0.40613985,0.26219224,
                            0.18944009,0.14479323,0.11834137,0.09839466,
                            0.08218122,0.06886769,
                            0.06393146,0.06354505,0.06316098,0.06278116,
                            0.06240455,0.06202999,
                            0.06165789,0.06128802]
,[ 0.68081776,1.35968336,0.83233801,0.54541128,0.31384392,0.19515477
,  0.13810567,0.10431534,0.08466327,0.07009283,0.05836801,0.04881033
,  0.04524745,0.04493017,0.04461511,0.04432146,0.04403633,0.04375288
,  0.04347141,0.04319176]
,[ 0.55339867,1.59387482,1.56301778,1.04489446,0.65405138,0.48026192
,  0.38166964,0.31708251,0.26682543,0.22965146,0.20204715,0.17815543
,  0.15943943,0.1441247, 0.13028101,0.11768048,0.1062808, 0.09597983
,  0.08848198,0.08175583]
,[ 0.52814312,1.90746337,1.54929322,1.16198595,0.57701843,0.37086656
,  0.27604003,0.22161678,0.18278793,0.15542678,0.13559712,0.11886919
  ,0.10596113,0.09552351,0.08611405,0.07765319,0.07003567,0.06316169
  ,0.05814846,0.0536552 ]]])
        index = [0, 1, 0, 1, 0, 1]
        event_activity = [ 0.33333333, 0.33333333, 0.33333333,
                           0.33333333, 0.33333333, 0.33333333]
        THE_PARAM_T = Dummy()
        THE_PARAM_T.atten_models = ['Toro_1997_midcontinent',
                                   'Atkinson_Boore_97','Sadigh_97']
        THE_PARAM_T.atten_model_weights = [0.33333333, 0.33333333,
                                               0.33333333]
        THE_PARAM_T.atten_aggregate_Sa_of_atten_models = True
        THE_PARAM_T.src_eps_switch = 0
        THE_PARAM_T.atten_use_variability = True  
        THE_PARAM_T.atten_variability_method = 2 
        THE_PARAM_T.nsamples = 5
        
        new_soil_SA = [[[0.70820126, 1.48997287, 1.20191183, 0.79781543,
                         0.52165442, 0.39265408
,   0.31788124, 0.27180767, 0.2368731,  0.20897504, 0.18611218, 0.16606172
  , 0.15102437, 0.13916622, 0.12837193, 0.11840738, 0.10931185, 0.10103923
,   0.09412251, 0.08784462]
, [ 0.61732583, 1.56362287, 1.13663517, 0.81766984, 0.47082765, 0.31611605
,   0.24033608, 0.1985642,  0.16954435, 0.14773021, 0.13041477, 0.11567198
,   0.10476309, 0.09626626, 0.08855644, 0.08156798, 0.07523259, 0.06947842
,   0.06465155, 0.0602755 ]]]

        results, _, _ = do_collapse_logic_tree( \
            soil_SA,
            index,
            event_activity,
            THE_PARAM_T, use_C=False)
        self.assert_ (allclose(results, new_soil_SA))

    def test_hzd_do_value(self):
        
        # WARNING - MORE A BLACK BOX TEST - BASED ON THE FUNCTIONS OUTPUT,
        # RATHER THAN
        # WHAT IT SHOULD OUTPUT.
        new_bedrock_SA = array([[0.05118885, 0.02495303, 0.05791614, 0.058257,
                                 0.0681056,  0.00444659,  0.00717228,
                                 0.00976539,
                                 0.13190761, 0.05088149, 0.04986149,
                                 0.00534023,
                                 0.02332557, 0.05212078, 0.00868164]])

        event_activity = array([
            4.63068629e-03,  1.06082894e-02,  5.31673923e-03,  4.03315915e-03
            , 3.05946409e-03,  1.31177366e-02,  1.31177366e-02,  1.99259970e-01
            , 1.80149203e-04,  1.34162872e-03,  8.12142702e-04,  6.01474011e-03
            , 9.26410637e-04,  1.62378129e-03,  4.35012634e-03])
        
        rtrn_rte =  array([[ 0.1       ], [ 0.02      ], [ 0.01      ],
                     [ 0.005     ], [ 0.004     ], [ 0.00210722],
                     [ 0.002     ], [ 0.00102586], [ 0.001     ],
                     [ 0.00040406], [ 0.0004    ],[ 0.0002    ],
                     [ 0.00013333], [ 0.0001    ]])

        hzd = hzd_do_value(new_bedrock_SA, event_activity, rtrn_rte)
   
   
        bedrock_hazard = array([ 0.01435674, 0.05114633, 0.05809098,
                                 0.0625557,  0.06011379
                           , 0.1082926
                           , 0.10605673, 0.08574208, 0.08520275, 0.07277496,
                                 0.07269036,
                           0.06851956
                           , 0.13190761, 0.13190761])
        
        self.assert_ (allclose(hzd, bedrock_hazard))
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Exceedance,'test')
    #suite = unittest.makeSuite(Test_Exceedance,'test_exceedance_curve8')
    runner = unittest.TextTestRunner()
    runner.run(suite)
