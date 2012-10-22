"""
# This information has been manually extracted from EQRM by TD
# and PR for testing the python code - 25/10/06

# original in \cit\2\earthquake\eqrm_refactor\EQRM_Damage\Mw6.5

# WARNING - Most of these 'unit' tests are comparing against
# old matlab data - not actually doing small understandable
# tests
"""

import os
import sys
import unittest
from os.path import join
from numpy import array, where, allclose, asarray
from scipy import array, allclose, sqrt, log, newaxis, seterr
from scipy.special import erf

from eqrm_code.capacity_spectrum_model import Capacity_spectrum_model
from eqrm_code.building_params_from_csv import building_params_from_csv
from eqrm_code.structures import Structures
from eqrm_code.util import reset_seed, determine_eqrm_path
from eqrm_code.equivalent_linear_solver import find_intersection
from eqrm_code.capacity_spectrum_functions import nonlin_damp, \
     calculate_reduction_factors, calculate_updated_demand
from eqrm_code.damage_model import cumulative_state_probability, \
     reduce_cumulative_to_pdf, Damage_model, \
     Capacity_spectrum_model
from eqrm_code.capacity_spectrum_model import Capacity_spectrum_model, \
     CSM_DAMPING_REGIMES_USE_ALL, CSM_DAMPING_MODIFY_TAV
from eqrm_code.capacity_spectrum_functions import CSM_DAMPING_USE_SMOOTHING


class Dummy:
    def __init__(self):
        pass

class Test_damage_model(unittest.TestCase):
    def _test_extract_building_parameters(self):
        # in
        aus_mag = 7.2
        btype = 40

        # out:
        params = (0.069, 13,0.3, 0.9, 0.7, 1.75, 2,7)
        dparams = (0.001, 0.001, 0.001, 0.08)
        assert(False) # not implimented


    def test_find_intersection(self):
        SA = array([0.289739794645192, 0.646693092888598, 0.553904993443363,
                    0.449529429311655, 0.379120948142093, 0.335578413347301,
                    0.304315540473696, 0.283748719032318, 0.267585606238139,
                    0.24435435573003, 0.219329239293237, 0.140951829163807,
                    0.0972042308150227, 0.0708216090506566, 0.0486635691749981,
                    0.0350874731334362, 0.0257081139420298, 0.018910471443273,
                    0.0139102359283618])

        SD = array([0,1.60533088580753, 5.49998633698612, 10.0430812761127,
                    15.05788941807, 20.8257362526643, 27.1952446916894,
                    34.5140821612566, 42.5117576683308, 49.1327918769187,
                    54.4456104247827, 78.726251497955, 96.5187076679668,
                    109.878354239657, 108.720841961029, 106.697568070816,
                    102.107240125687, 95.0591053452788, 86.3258461016045])

        SAcap = array([0, 0.0718547880987331, 0.210114969058595,
                       0.255544749303803, 0.26593317666683,
                       0.267982944023487, 0.268291483967979,
                       0.268329691827397, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333])

        '''[SDcrNew, SAcrNew] = find_intersection( SDnew,                 ...
                                        SAnew,                 ...
                                        SAcapNew,              ...
                                        BCAP_PARAMS_T.('DyV'), ...
                                        BCAP_PARAMS_T.('AyV'), ...
                                        BCAP_PARAMS_T.('DuV'), ...
                                        BCAP_PARAMS_T.('AuV'), ...
                                        BCAP_PARAMS_T.('aaV'), ...
                                        BCAP_PARAMS_T.('bbV'), ...
                                        BCAP_PARAMS_T.('ccV')    );'''

        SDcr = find_intersection(SD, SA, SAcap, axis=-1)

        SDcr_m = 42.1418578996947
        assert allclose(SDcr_m, SDcr)


    def test_nonlin_damp_rand(self):
        SA = array([0.289739794645192, 0.646693092888598, 0.553904993443363,
                    0.449529429311655, 0.379120948142093, 0.335578413347301,
                    0.304315540473696, 0.283748719032318, 0.267585606238139,
                    0.24435435573003, 0.219329239293237, 0.140951829163807,
                    0.0972042308150227, 0.0708216090506566, 0.0486635691749981,
                    0.0350874731334362, 0.0257081139420298, 0.018910471443273,
                    0.0139102359283618])

        SD = array([0,1.60533088580753, 5.49998633698612, 10.0430812761127,
                    15.05788941807, 20.8257362526643, 27.1952446916894,
                    34.5140821612566, 42.5117576683308, 49.1327918769187,
                    54.4456104247827, 78.726251497955, 96.5187076679668,
                    109.878354239657, 108.720841961029, 106.697568070816,
                    102.107240125687, 95.0591053452788, 86.3258461016045])

        SAcap = array([0, 0.0718547880987331, 0.210114969058595,
                       0.255544749303803, 0.26593317666683,
                       0.267982944023487, 0.268291483967979,
                       0.268329691827397, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333])
        SDcr = array([42.1418578996947])
        SAcr = array([0.268333333333333])
        (Ay, Dy, Au, Du) = (0.13417, 2.9975, 0.26833, 41.964)
        (aa, bb, cc, kappa) = (-0.3647, 0.33362, 0.26833, 0.001)
        capacity_parameters = (Dy, Ay, Du, Au, aa, bb, cc)
        csm_hysteretic_damping='trapezoidal'
        damping = nonlin_damp(capacity_parameters, kappa, SAcr, SDcr,
                              csm_hysteretic_damping)

        #out
        damping_m = 0.000540396780259699
        assert allclose(damping, damping_m)
    '''[BH, Harea, kappa, Harea0] = ...
                  nonlin_damp_rand( SDcrNew,               ...
                                    SAcrNew,               ...
                                    BCAP_PARAMS_T.('kappa'),  ...
                                    BCAP_PARAMS_T.('DyV'), ...
                                    BCAP_PARAMS_T.('AyV'), ...
                                    eqrm_flags.('csm_hysteretic_damping'), ...
                                    SDnew,                 ...
                                    SAnew,                 ...
                                    SAcapNew  );'''

    def test_update_demand_again(self):
        SA = array([0.342010, 0.763370, 0.653840, 0.530630, 0.44294,
                    0.38397, 0.34452, 0.321240, 0.302940, 0.276640,
                    0.248310, 0.15958, 0.11005, 0.080179, 0.055094,
                    0.039724, 0.029105, 0.021409, 0.015748])
        SA.shape = (1, 1, -1)
        SD = array([0, 1.895, 6.4923, 11.855, 17.593, 23.829,
                    30.789, 39.074, 48.129, 55.625, 61.64,
                    89.128, 109.27, 124.4, 123.09, 120.8,
                    115.6, 107.62, 97.732])
        SD.shape = (1, 1, -1)
        TAV = array([[0.46795]])
        TVD = array([[12.589]])

        damping_factor = [[[0.08+0.000540396780259699]]]
        periods = array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1,
                         1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
        damp_corner_periods = True

        # calc
        (Ra, Rv, Rd) = calculate_reduction_factors(damping_factor)
        if damp_corner_periods:
            TAV = (TAV*(Ra/Rv))[:,:,0]

        (SAnew, SDnew) = calculate_updated_demand(periods, SA, SD,
                                                  Ra, Rv, Rd, TAV, TVD)

        SA_new_m = array([0.289001251823406, 0.645044680932497,
                          0.552493097099059, 0.448383584870071,
                          0.378214709055794, 0.334886136749447,
                          0.303739197972188, 0.283211327986589,
                          0.267078826474521, 0.243891573578266,
                          0.21891385215188, 0.140684880819053,
                          0.0970201359460657, 0.0706874801683211,
                          0.0485714053533709, 0.0350210210488472,
                          0.0256594254042202, 0.0188746569449423,
                          0.0138838913645612])

        assert allclose(SAnew, SA_new_m, rtol=5e-5)


    def test_find_intersection_again(self):
        '''
    [SDcrNew, SAcrNew] = find_intersection( SDnew,                 ...
                                            SAnew,                 ...
                                            SAcapNew,              ...
                                            BCAP_PARAMS_T.('DyV'), ...
                                            BCAP_PARAMS_T.('AyV'), ...
                                            BCAP_PARAMS_T.('DuV'), ...
                                            BCAP_PARAMS_T.('AuV'), ...
                                            BCAP_PARAMS_T.('aaV'), ...
                                            BCAP_PARAMS_T.('bbV'), ...
                                            BCAP_PARAMS_T.('ccV')  );'''

        SAnew = array([0.289001251823406, 0.645044680932497,
                       0.552493097099059, 0.448383584870071,
                       0.378214709055794, 0.334886136749447,
                       0.303739197972188, 0.283211327986589,
                       0.267078826474521, 0.243891573578266,
                       0.21891385215188, 0.140684880819053,
                       0.0970201359460657, 0.0706874801683211,
                       0.0485714053533709, 0.0350210210488472,
                       0.0256594254042202, 0.0188746569449423,
                       0.0138838913645612])
        SDnew = array([0, 1.6012, 5.486, 10.017, 15.022, 20.783, 27.144, 34.449,
                       42.431, 49.04, 54.342, 78.577, 96.336, 109.67, 108.51,
                       106.5, 101.91, 94.879, 86.162])


        SAcap = array([0, 0.0716716312147219, 0.209842038805638,
                       0.25543506124516, 0.265904181516395,
                       0.26797788578358, 0.26829075866169,
                       0.268329611544255, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333,
                       0.268333333333333, 0.268333333333333])

        SDcr = find_intersection(SDnew, SAnew, SAcap, axis=-1)

        SDcr_m = 41.810644943005
        assert allclose(SDcr_m, SDcr)


    def test_capacity_method(self):
        #in
        (Ay, Dy, Au, Du) =(0.13417, 2.9975, 0.26833, 41.964)
        (aa, bb, cc, kappa) =(-0.3647, 0.33362, 0.26833, 0.001)
        capacity_parameters = (Dy, Ay, Du, Au, aa, bb, cc)

        SA_Regolith = array([0.342012967618843, 0.763365709250557,
                             0.653837319165796, 0.530630921234538,
                             0.442943423800148, 0.383969335597378,
                             0.344524949645552, 0.321240620786007,
                             0.302941865445212, 0.27664105478319,
                             0.248309353527187, 0.15957588550857,
                             0.110047888697209, 0.0801793140567643,
                             0.0550935180421332, 0.0397236036505722,
                             0.0291049436633207, 0.0214091242649845,
                             0.0157482043977009])
        SA_Regolith.shape = (1, 1, -1)

        params = (0.069, 13, 0.3, 0.9, 0.7, 1.75, 2, 7)
        dparams = (0.001, 0.001, 0.001, 0.08)

        (C, height, T, a1, a2, y, h, u) =params
        magnitudes = array([7.2])
        (damping_s, damping_m, damping_l, initial_damping) = dparams

        periods = array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,
                         0.9, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

        building_parameters = {}

        building_parameters['design_strength'] = array([C])
        building_parameters['natural_elastic_period'] = array([T])
        building_parameters['fraction_in_first_mode'] = array([a1])
        building_parameters['height_to_displacement'] = array([a2])
        building_parameters['yield_to_design'] = array([y])
        building_parameters['ultimate_to_yield'] = array([h])
        building_parameters['ductility'] = array([u])
        building_parameters['damping_s'] = array([damping_s])
        building_parameters['damping_m'] = array([damping_m])
        building_parameters['damping_l'] = array([damping_l])
        building_parameters['damping_Be'] = array([initial_damping])
        building_parameters['structure_classification'] = ['test_blg']
        
        csm = Capacity_spectrum_model(periods, magnitudes, building_parameters)
        csm.rtol = 0.01
        csm.csm_damping_max_iterations = 7
        csm.use_displacement_corner_period = True
        csm.use_exact_area = True
        csm.damp_corner_periods = True
        point = csm.building_response(SA_Regolith)

        #final
        SDnew = [0, 1.6012, 5.486, 10.017, 15.022, 20.783, 27.144, 34.449,
                 42.431, 49.04, 54.342, 78.577, 96.336, 109.67, 108.51, 106.5,
                 101.91, 94.879, 86.162]

        SAnew = [0, 1.6012, 5.486, 10.017, 15.022, 20.783, 27.144, 34.449,
                 42.431, 49.04, 54.342, 78.577, 96.336, 109.67, 108.51, 106.5,
                 101.91, 94.879, 86.162]

        SDcr = 41.810644943005

        SAcr = 0.26833301410569

        assert allclose(SAcr, point[0])
        assert allclose(SDcr, point[1])


    def test_fragility(self):
        #in
        """
        btype=1

        Thresh=array([3.41376, 27.31008, 51.2064, 102.4128])
        SDcr=0.900320457314158
        beta=0.5

        #out

        0.00384212302089559  4.41097158798698e-012 3.33066907387547e-016 0

        Pr1=array([0.00384212302089559, 4.41097158798698e-012,
                   3.33066907387547e-016, 0])

        Pr_sd=array([0.996157876979104, 0.00384212301648462,
                     4.41063852107959e-012, 3.33066907387547e-016, 0])
        """

        threshold = array([3.41376, 27.31008, 51.2064, 102.4128])
        value = 0.900320457314158
        beta = 0.5
        cdf = cumulative_state_probability(threshold, beta, value)

        cdf_matlab = array([0.00384212302089559, 4.41097158798698e-012,
                            3.33066907387547e-016, 0])
        assert allclose(cdf, cdf_matlab)
        reduce_cumulative_to_pdf(cdf)
        pdf=cdf

        pdf_matlab = array([0.996157876979104, 0.00384212301648462,
                            4.41063852107959e-012, 3.33066907387547e-016, 0])

        assert allclose(pdf, pdf_matlab[1:])

        f1 = array((0.02, 0.1, 0.5, 1.0))	# [newaxis, newaxis, :]
        ci = 1.4516
        Area = 4351.656708
        cost = 113.9023

        damage_matlab = array([0.00875252912708771, 5.02381651487638e-011,
                               1.89685350759916e-014, 0])

        assert allclose(damage_matlab, f1*pdf*cost)

        cost_matlab = 55.2885441482002
        assert allclose(cost_matlab, (f1*pdf*cost*Area*ci).sum())


    def test_cumulative_state_probability(self):
        blocking_block_comments = True
        """Test that cumulative_state_probability works the same way
        as matlab function.

        Test that reduce_cumulative_to_pdf 'looks' right - it should
        look a bit like a bell curve - zero at ends with a max
        somewhere in the middle, and sum=one.
        """

        # test against matlab implimentation:
        beta = 0.4
        value = 5.0
        threshold = array((0.0, 0.00001, 1, 1.5, 2, 3, 4, 5, 10, 100, 1000))

        oldsettings = seterr(divide='ignore')
        x = (1/beta)*log(value/threshold)
        seterr(**oldsettings)
        # matlab:
        # Pr11 = normcdf2(1/THE_VUN_T.('beta_nsd_d')*log(SDcrAll./Thresh))

        root2 = sqrt(2)
        y = 0.5*(1 + erf(x/root2))
        # matlab:
        # root2 = sqrt(2);
        # y = 0.5*(1+erf(x/root2))
        y2 = cumulative_state_probability(threshold, beta, value)
        assert allclose(y, y2)

        reduce_cumulative_to_pdf(y)

        # y should now look a bit  like a bell curve - zero at ends
        # increasing to the middle, sum=one.
        assert (y.sum() == 1.0)
        assert y[0] == 0
        assert y[1] < y[2]
        assert y[-3] > y[-2]


    def test_building_response(self):
        #Test that building response is the same as matlab

        periods=array([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
                       0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7,
                       1.8, 1.9, 2, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9,
                       3])

        SA = array([0.017553049, 0.028380350, 0.036142210, 0.037701113,
                    0.039325398, 0.038083417, 0.036880517, 0.036190107,
                    0.035512489, 0.035088679, 0.034669917, 0.033162774,
                    0.030871523, 0.027841184, 0.025094836, 0.022850476,
                    0.021322256, 0.019895084, 0.018562342, 0.017317833,
                    0.016160874, 0.015195155, 0.014287144, 0.013433394,
                    0.012630662, 0.011875899, 0.011166239, 0.010498986,
                    0.009871606, 0.009281717, 0.008727078, 0.008140645,
                    0.007593619, 0.007083352, 0.006607374, 0.006163380])

        SA = SA[newaxis, newaxis, :]

        magnitudes = array([6.5])

        Btype = 'RM2L'

        eqrm_dir = determine_eqrm_path()
        default_input_dir = join(eqrm_dir, 'resources', 'data', '')
        building_parameters = \
            building_params_from_csv(building_classification_tag = '',
                                     damage_extent_tag = '',
                                     default_input_dir=default_input_dir)

        # Pull the parameters out:
        b_index = where([(bt == Btype) for bt in
                             building_parameters['structure_classification']])
        new_bp = {}
        for key in building_parameters:
            try:
                new_bp[key] = building_parameters[key][b_index]
            except:
                new_bp[key] = building_parameters[key]

        structures = Structures(latitude=[-31], longitude=[150],
                                building_parameters=new_bp,
                                #bridge_parameters={},
                                FCB_USAGE=array([111]),
                                STRUCTURE_CLASSIFICATION=array([Btype]),
                                STRUCTURE_CATEGORY=array(['BUILDING']))
        building_parameters = structures.building_parameters

        # All the same for this type anyway
        csm_use_variability = None
        csm_standard_deviation = None
        damage_model = Damage_model(structures, SA, periods, magnitudes,
                                    csm_use_variability, csm_standard_deviation)

        # set up the capacity model
        capacity_spectrum_model = Capacity_spectrum_model(periods, magnitudes,
                                                          building_parameters)

        capacity_spectrum_model.smooth_damping = True
        capacity_spectrum_model.use_displacement_corner_period = True
        capacity_spectrum_model.damp_corner_periods = True
        capacity_spectrum_model.use_exact_area = True
        capacity_spectrum_model.rtol = 0.01
        capacity_spectrum_model.csm_damping_max_iterations = 7

        ###########################################################

        damage_model.capacity_spectrum_model = capacity_spectrum_model

        # Warning, point is not used
        point = damage_model.get_building_displacement()

        # matlab values
        SAcr = 0.032208873
        SDcr = 0.97944026
        assert allclose(point[0], SAcr)
        assert allclose(point[1], SDcr)
        assert allclose(point, [[[SAcr]], [[SDcr]]])

        # this test is testing against itself, so it will always be True,
        # therefore need a new test
        # point2=damage_model.get_building_displacement()
        # assert allclose(point, point2)


    def test_calc_total_loss_OS_bug_search(self):
        blocking_block_comments = True
        """plugging in results from TS_risk57.par"""
        
        SA =array([[[0.14210731, 0.29123634, 0.23670422, 0.13234554,
                     0.08648546, 0.06338455, 0.04945741, 0.04140068,
                     0.03497466, 0.02969136, 0.02525473, 0.02151188,
                     0.018371, 0.01571802, 0.01344816, 0.01148438,
                     0.00980236, 0.00836594, 0.00714065, 0.00609482],
                    [0.2093217, 0.30976405, 0.16232743, 0.06989206,
                     0.03216174, 0.01945677, 0.01347719, 0.00987403,
                     0.00799221, 0.00660128, 0.00547129, 0.0045463,
                     0.0042072, 0.00418348, 0.0041599, 0.00413222,
                     0.00410333, 0.00407463, 0.00404614, 0.00401785],
                    [0.01450217, 0.02750284, 0.02231209, 0.01127933,
                     0.00793098, 0.00621618, 0.0051103, 0.00430777,
                     0.00364714, 0.0031542, 0.00279411, 0.00247654,
                     0.0022153, 0.001994, 0.0017948, 0.00161223,
                     0.00144737, 0.00129929, 0.00117312, 0.00105988]]])
        event_set = array([6.0201519, 6.0201519, 6.0201519])

        eqrm_flags = Dummy()
        eqrm_flags.csm_variability_method = 3
        eqrm_flags.atten_periods = array([0., 0.17544,0.35088, 0.52632,
                                           0.70175, 0.87719, 1.0526, 1.2281,
                                           1.4035, 1.5789, 1.7544, 1.9298,
                                           2.1053, 2.2807, 2.4561, 2.6316,
                                           2.807,  2.9825, 3.1579, 3.3333 ])
        eqrm_flags.csm_use_variability = True
        eqrm_flags.csm_standard_deviation = 0.3
        eqrm_flags.csm_damping_regimes = CSM_DAMPING_REGIMES_USE_ALL
        eqrm_flags.csm_damping_modify_Tav = CSM_DAMPING_MODIFY_TAV
        eqrm_flags.csm_damping_use_smoothing = CSM_DAMPING_USE_SMOOTHING
        eqrm_flags.csm_SDcr_tolerance_percentage = 1
        eqrm_flags.csm_damping_max_iterations = 7
        eqrm_flags.csm_hysteretic_damping = 'trapezoidal'
        eqrm_flags.bridges_functional_percentages = None
        eqrm_flags.atten_override_RSA_shape = None
        eqrm_flags.atten_pga_scaling_cutoff = False
        eqrm_flags.atten_cutoff_max_spectral_displacement = False
        eqrm_flags.loss_min_pga = 0.05
        eqrm_flags.loss_regional_cost_index_multiplier = 1.4516
        eqrm_flags.loss_aus_contents = 0

        building_parameters = {'residential_drift_threshold':
                                   array([[21.9456, 43.8912,
                                           109.728 ,164.592]]),
                               'structure_class':
                                   array(['BUILDING'], dtype='|S8'),
                               'height': array([7315.2]),
                               'nsd_a_ratio': array([0.7254902]),
                               'design_strength': array([0.033]),
                               'non_residential_drift_threshold':
                                   array([[5.4864, 43.8912, 82.296, 137.16]]),
                               'damping_Be': array([0.1]),
                               'fraction_in_first_mode': array([0.8]),
                               'ultimate_to_yield': array([3.]),
                               'acceleration_threshold':
                                   array([[0.2, 0.4, 0.8, 1.6]]),
                               'nsd_d_ratio': array([0.11764706]),
                               'structure_ratio': array([0.15686275]),
                               'structural_damage_threshold':
                                   array([[26.33472, 41.69664,
                                           88.87968, 219.456]]),
                               'natural_elastic_period': array([0.5]),
                               'damping_s': array([0.4]),
                               'drift_threshold':
                                   array([[5.4864, 43.8912, 82.296, 137.16]]),
                               'yield_to_design': array([1.5]),
                               'structure_classification':
                                   array(['S1L'], dtype='|S13'),
                               'height_to_displacement': array([0.75]),
                               'ductility': array([5.]),
                               'damping_l': array([0.]),
                               'damping_m': array([0.2])}

        # Note, this lats and longs are wrong
        sites = Structures(latitude=[-31],longitude=[150],
                           building_parameters=building_parameters)
        sites.attributes = {'FCB_USAGE': array([311]),
                            'SURVEY_FACTOR': array([1.]),
                            'HAZUS_STRUCTURE_CLASSIFICATION':
                                array(['S1L'], dtype='|S4'),
                            'SITE_CLASS': array(['D'], dtype='|S1'),
                            'FLOOR_AREA': array([3000.]),
                            'CONTENTS_COST_DENSITY': array([823.4392]),
                            'STRUCTURE_CATEGORY':
                                array(['BUILDING'], dtype='|S8'),
                            'STRUCTURE_CLASSIFICATION':
                                array(['S1L'], dtype='|S13'),
                            'SUBURB': array(['LAMBTON'], dtype='|S19'),
                            'HAZUS_USAGE': array(['IND3'], dtype='|S4'),
                            'POSTCODE': array([2299]),
                            'BUILDING_COST_DENSITY': array([548.9594]),
                            'BID': array([3562]),
                            'PRE1989': array([0])}

        reset_seed(True)
        total_loss, _ = sites.calc_total_loss(SA, 
                                              eqrm_flags, 
                                              event_set)

        total_loss_windows = (array([[5.56013748, 0.00899564, 0.]]),
                              array([[4059.31954558, 1473.71938878, 0.]]),
                              array([[9423.06584855, 1181.40856505, 0.]]),
                              array([[9978.48421213, 1226.05473008, 0.]]))
        assert allclose(asarray(total_loss), asarray(total_loss_windows))

    def test_save_structure_damage_states(self):
        pass

    def test_reduce_cumulative_to_pdf(self):
        cumulative = array([1.0, 0.6, 0.3, 0.1])
        non_cummulative = cumulative[:]
        reduce_cumulative_to_pdf(non_cummulative)
        actual = array([0.4, 0.3, 0.2, 0.1])
        assert allclose(asarray(non_cummulative),asarray(actual))

################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_damage_model,'test')
    #suite = unittest.makeSuite(Test_damage_model,'test_calc_total_loss_OS_bug_search')
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)

