import unittest

from scipy import array, exp, log, allclose, newaxis, asarray, zeros
import math

from eqrm_code.ground_motion_specification import *
from eqrm_code.ground_motion_interface import gound_motion_init
from eqrm_code.ground_motion_misc import \
     Australian_standard_model_interpolation
from eqrm_code.ground_motion_calculator import Ground_motion_calculator, \
     Multiple_ground_motion_calculator

classes_with_test_data = ('Allen','AllenSEA06','Gaull_1990_WA',
                          'Toro_1997_midcontinent', 'Sadigh_97',
                          'Youngs_97_interface', 'Youngs_97_intraslab',
                          'Combo_Sadigh_Youngs_M8', 'Boore_08',
                          'Somerville09_Yilgarn', 'Somerville09_Non_Cratonic',
                          'Liang_2008', 'Atkinson06_hard_bedrock',
                          'Atkinson06_soil', 'Atkinson06_bc_boundary_bedrock',
                          'Campbell03', 'Campbell08', 'Abrahamson08', 'Chiou08','Akkar_2010_crustal','Zhao_2006_interface',
                          'Atkinson_2003_intraslab','Atkinson_2003_interface','Zhao_2006_intraslab')

# Atkinson_Boore_97 is out.  It has no test data.


"""
    test_distance : the set of distances used by verification tests
                    dimensions (site, mag)

    test_magnitude : the set of magnitudes used by verification tests
                    dimensions (mag)

    test_period : the set of periods used by verification tests
                    dimensions (period)

    test_mean : the means that must be matched by verification tests
                    dimensions (sites, mag, period).  Units g.  Not log mean

    test_Vs30: the shear wave velocity at a depth of 30.0 meters
               (if not defined, will be assumed to be 1000m/s)
"""

test_data = {}

# ***********************************************************
test_data['Allen_test_distance'] = [30.0]
test_data['Allen_test_magnitude'] = [4.5,5.5,6.5,7.5]
test_data['Allen_test_period'] = [10, 5, 3.003, 2, 1.6,	1, 0.7502, 0.5,	0.4,
           0.3,	0.24,   0.2,	0.16,	0.15,	0.12,	0.1,	0.08,   0.07,
           0.06,	0.055,	0.05,	0.04,   0.0323,	0.025,	0.02,	0.01]
test_data['Allen_test_mean'] = [
    [[3.2254E-06,	        2.13427E-05,	8.87049E-05,	0.000252186,
      0.000417375,	0.001306295,	0.002466791,	0.005243502,
      0.006902655,	0.009918957,	0.012370647,	0.014320455,
      0.015778327,	0.016025567,	0.016223227,	0.015530954,
      0.01394683, 	0.012796361,	0.011232611,	0.010404032,
      0.009575646,	0.007988456,	0.007033039,	0.006323007,
      0.006004762,	0.005705212],
     [9.95104E-05,	0.000647191,	0.00223538,	0.004949904,
      0.00692064,	        0.014388865,	0.021358797,	0.033117945,
      0.037781213,	0.046639186,	0.05309692,	0.057929389,
      0.060564862,	0.06082379,	0.059763646,	0.056588616,
      0.050848608,	0.046959793,	0.041793723,	0.039061642,
      0.036325878,	0.031109154,	0.028047,	0.02575876,
      0.024736682,	0.023791819],
     [0.001899581,	0.009457791,	0.024941229,	0.043514938,
      0.053137664,	0.083172304,	0.106111365,	0.136349428,
      0.14301618,	        0.161925188,	0.175028939,	0.184439357,
      0.186959589,	0.186501006,	0.179721983,	0.168848289,
      0.151573893,	0.140471229,	0.126081821,	0.118478144,
      0.110874377,	0.096535107,	0.088307451,	0.082260788,
      0.0796006,	        0.077194124],
     [0.022436299,	0.066607118,	0.123210362,	0.171334928,
      0.188927578,	0.252288718,	0.302473782,	0.365924329,
      0.374407046,	0.415103448,	0.443112515,	0.462190253,
      0.464132514,	0.461994169,	0.441193996,	0.412573097,
      0.369412442,	0.342507519,	0.308393321,	0.290311959,
      0.272278449,	0.238700914,	0.219520869,	0.205933712,
      0.200087748,	0.194868491]]]

 # getting test data Gaul_1990_WA
a=0.025
b=1.10
c=1.03
g=9.8
R=array([[00.1,20.0,30],[50,60,80]])
ML=array([4,5.5,6.5])
test_data['Gaull_1990_WA_test_distance'] = R
test_data['Gaull_1990_WA_test_magnitude'] = ML

R=R[:,:,newaxis]
ML=ML[newaxis,:,newaxis]
mean=a*exp(b*ML)*(R**-c)

period=array([0.00,0.05,0.10,0.20,0.30,0.50,0.70,1.00,3.00,4.00])
scale=Australian_standard_model_interpolation(period,1.0,0.0)
mean=mean*scale[newaxis,newaxis,:]
mean=mean/g

test_data['Gaull_1990_WA_test_mean'] = mean[:]
test_data['Gaull_1990_WA_test_period'] = period

# ***********************************************************

test_data['Toro_1997_midcontinent_test_distance'] = [[17.004,187.14],
                                            [1.5291,168.8]]
# temp - CHANGED 6.69 to 4.59...
test_data['Toro_1997_midcontinent_test_magnitude'] = [6.59694563,4.78866307]

test_data['Toro_1997_midcontinent_test_period'] = [0.0,1.0]
test_data['Toro_1997_midcontinent_test_mean'] = [[[ 0.32568276,  0.16652828],
                                         [ 0.00317764,  0.00110675]],
                                        [[ 0.83083585,  0.40776479],
                                         [ 0.00372073,  0.00121415]]]

# Atkinson_Boore_97 tests
# These were all AllenSEA06_test.
# Why does AllenSEA06 and Atkinson_Boore_97 have the same test results?
# The Atkinson_Boore_97 tests fail, which makes sense.
# They were AllenSEA06 pretending to be Atkinson_Boore_97 tests.
# So I'm deleting the fake Atkinson_Boore_97 tests.

# ***********************************************************

test_data['Sadigh_97_test_period'] = (
    array([0.0000E+00,7.0000E-02,1.0000E-01,2.0000E-01,
           3.0000E-01,4.0000E-01,5.0000E-01,7.5000E-01,
           1.0000E-00,1.5000E-00,2.0000E-00,3.0000E-00]))

test_data['Sadigh_97_test_distance'] = (
    array([[10.0,25.0,50.0],[50.0,25.0,10.0]]))

test_data['Sadigh_97_test_mean'] = [
    [[2.6847E-01,4.4170E-01,5.4026E-01,5.9924E-01,
            5.0643E-01,4.0426E-01,3.1130E-01,1.9711E-01,
            1.4119E-01,8.1022E-02,5.3910E-02,2.7935E-02],
           [1.0433E-01,1.5859E-01,1.9874E-01,2.3497E-01,
            2.0328E-01,1.6507E-01,1.2971E-01,8.5142E-02,
            6.2797E-02,3.7274E-02,2.5423E-02,1.3534E-02],
           [8.7664E-02,1.1904E-01,1.5147E-01,2.0553E-01,
            2.0108E-01,1.8055E-01,1.5865E-01,1.1717E-01,
            9.3009E-02,6.1934E-02,4.5201E-02,2.6760E-02]],
           [[3.8676E-02,5.4983E-02,7.0113E-02,8.7934E-02,
            7.7967E-02,6.4458E-02,5.1740E-02,3.5270E-02,
            2.6825E-02,1.6497E-02,1.1548E-02,6.3250E-03],
           [1.0433E-01,1.5859E-01,1.9874E-01,2.3497E-01,
            2.0328E-01,1.6507E-01,1.2971E-01,8.5142E-02,
            6.2797E-02,3.7274E-02,2.5423E-02,1.3534E-02],
           [4.4690E-01,6.9942E-01,8.5110E-01,1.03165E-00,
            9.6938E-01,8.4513E-01,7.1715E-01,4.9777E-01,
            3.7571E-01,2.3605E-01,1.6508E-01,9.3287E-02]]
    ]

test_data['Sadigh_97_test_magnitude'] = [6.0,6.0,7.0]

# ***********************************************************

test_data['Youngs_97_interface_test_period'] = [
    0.0000E+00,7.5000E-02,1.0000E-01,2.0000E-01,
    3.0000E-01,4.0000E-01,5.0000E-01,7.5000E-01,
    1.0000E-00,1.5000E-00,2.0000E-00,3.0000E-00]

test_data['Youngs_97_interface_test_distance'] = [10.0,25.0,50.0]

test_data['Youngs_97_interface_test_mean'] = array([
    [2.1565E-01,3.9499E-01,4.3243E-01,4.3860E-01,
     3.6096E-01,3.0698E-01,2.6976E-01,1.6897E-01,
     1.1413E-01,6.1594E-02,3.7546E-02,1.5237E-02],
    [1.3563E-01,2.4153E-01,2.6693E-01,2.7706E-01,
     2.3110E-01,1.9844E-01,1.7568E-01,1.1153E-01,
     7.6054E-02,4.1599E-02,2.5603E-02,1.0531E-02],
    [7.2680E-02,1.2462E-01,1.3948E-01,1.4934E-01,
     1.2684E-01,1.1034E-01,9.8668E-02,6.3782E-02,
     4.4050E-02,2.4533E-02,1.5297E-02,6.4070E-03]])

test_data['Youngs_97_interface_test_mean'] = \
                                 test_data['Youngs_97_interface_test_mean'][:,newaxis,:]
test_data['Youngs_97_interface_test_magnitude'] = [6.5]
test_data['Youngs_97_interface_test_depth'] = [10.0]


# ***********************************************************

test_data['Youngs_97_intraslab_test_period'] = [
    0, 0.02, 0.15, 0.25, 0.35, 0.5,
    0.7, 0.85, 1.0, 1.42, 2.1, 2.5]

tmp = zeros((4,9)) # initialise an array: 3 mags, 3 depths (9 events) and distance to 4 sites
tmp[0,:] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,0.0, 0.0, 0.0] # distance between 1st site and all 9 events - Note that this minimum distance is 10 km, so will be evaluated at 10 km.
tmp[1,:] = [25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0] # distance between 2nd site and all 9 events
tmp[2,:] = [50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0]# distance between 3rd site and all 9 events
tmp[3,:] = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0] # distance between 4th site and all 9 events

test_data['Youngs_97_intraslab_test_distance'] = tmp

tmp = zeros((4,9,12))
tmp[0,0,:] = [0.29161,0.34538,0.57508,0.50503,
0.41201,0.32507,0.21849,0.16766,
0.13081,0.076054,0.037283,0.025695]
tmp[0,1,:] = [0.37175,0.44029,0.73312,0.64382,
0.52524,0.4144,0.27854,0.21374,
0.16676,0.096954,0.047529,0.032756]
tmp[0,2,:] = [0.50357,0.59642,0.99308,0.87212,
0.71148,0.56135,0.3773,0.28953,
0.22589,0.13133,0.064383,0.044372]
tmp[0,3,:] = [0.35416,0.41032,0.73419,0.7128,
0.61979,0.52329,0.3729,0.29669,
0.23909,0.14781,0.077981,0.055337]
tmp[0,4,:] = [0.45149,0.52308,0.93596,0.90868,
0.79012,0.66709,0.47538,0.37823,
0.30479,0.18843,0.099411,0.070545]
tmp[0,5,:] = [0.61159,0.70855,1.2678,1.2309,
1.0703,0.90364,0.64395,0.51235,
0.41287,0.25524,0.13466,0.09556]
tmp[0,6,:] = [0.39625,0.44847,0.82973,0.87101,
0.79583,0.70824,0.52832,0.43228,
0.3571,0.23162,0.12934,0.093905]
tmp[0,7,:] = [0.50515,0.57172,1.0578,1.1104,
1.0145,0.90287,0.67351,0.55107,
0.45523,0.29528,0.16488,0.11971]
tmp[0,8,:] = [0.68427,0.77444,1.4328,1.5041,
1.3743,1.223,0.91234,0.74648,
0.61665,0.39998,0.22335,0.16216]
tmp[1,0,:] = [0.16816,0.19739,0.3288,0.29508,
0.24405,0.19538,0.13301,0.10285,
0.080788,0.047604,0.023703,0.01644]
tmp[1,1,:] = [0.21437,0.25164,0.41916,0.37617,
0.31112,0.24907,0.16956,0.13112,
0.10299,0.060686,0.030217,0.020959]
tmp[1,2,:] = [0.29038,0.34087,0.56779,0.50956,
0.42144,0.33738,0.22968,0.17761,
0.13951,0.082205,0.040932,0.02839]
tmp[1,3,:] = [0.2528,0.29128,0.52133,0.5129,
0.44974,0.38311,0.27516,0.21996,
0.17798,0.11094,0.05909,0.042096]
tmp[1,4,:] = [0.32227,0.37133,0.6646,0.65386,
0.57333,0.4884,0.35077,0.2804,
0.22689,0.14143,0.075329,0.053665]
tmp[1,5,:] = [0.43655,0.503,0.90026,0.88571,
0.77663,0.66158,0.47515,0.37983,
0.30735,0.19157,0.10204,0.072694]
tmp[1,6,:] = [0.32541,0.36712,0.67931,0.71866,
0.65986,0.5903,0.44236,0.36294,
0.30054,0.19588,0.10999,0.080039]
tmp[1,7,:] = [0.41484,0.46801,0.866,0.91616,
0.84119,0.75253,0.56393,0.46268,
0.38313,0.24971,0.14021,0.10204]
tmp[1,8,:] = [0.56193,0.63396,1.1731,1.241,
1.1395,1.0194,0.76389,0.62674,
0.51899,0.33825,0.18993,0.13822]
tmp[2,0,:] = [0.082252,0.095441,0.15906,0.14683,
0.12361,0.10085,0.069804,0.054519,
0.0432,0.025902,0.013161,0.0092046]
tmp[2,1,:] = [0.10486,0.12167,0.20277,0.18717,
0.15758,0.12856,0.088987,0.069502,
0.055071,0.033021,0.016778,0.011734]
tmp[2,2,:] = [0.14204,0.16481,0.27467,0.25355,
0.21346,0.17415,0.12054,0.094147,
0.074599,0.04473,0.022728,0.015895]
tmp[2,3,:] = [0.15665,0.1791,0.32066,0.32148,
0.28527,0.2461,0.17873,0.14383,
0.11707,0.073824,0.039858,0.028553]
tmp[2,4,:] = [0.1997,0.22832,0.40879,0.40983,
0.36366,0.31374,0.22784,0.18335,
0.14924,0.094112,0.050811,0.0364]
tmp[2,5,:] = [0.27051,0.30928,0.55374,0.55515,
0.49261,0.42498,0.30863,0.24837,
0.20216,0.12748,0.068828,0.049307]
tmp[2,6,:] = [0.24159,0.27124,0.50201,0.53736,
0.49705,0.44818,0.33819,0.27862,
0.23156,0.15202,0.086083,0.062861]
tmp[2,7,:] = [0.30798,0.34578,0.63997,0.68503,
0.63365,0.57134,0.43112,0.35519,
0.2952,0.1938,0.10974,0.080136]
tmp[2,8,:] = [0.41719,0.46839,0.8669,0.92793,
0.85834,0.77394,0.584,0.48114,
0.39987,0.26251,0.14865,0.10855]
tmp[3,0,:] = [0.029792,0.034005,0.056714,0.054488,
0.047048,0.039429,0.027941,0.022135,
0.017758,0.010914,0.0057074,0.0040389]
tmp[3,1,:] = [0.03798,0.043351,0.0723,0.069462,
0.059977,0.050264,0.03562,0.028218,
0.022638,0.013914,0.0072759,0.0051489]
tmp[3,2,:] = [0.051447,0.058722,0.097937,0.094093,
0.081245,0.068087,0.048251,0.038223,
0.030666,0.018848,0.0098558,0.0069746]
tmp[3,3,:] = [0.073944,0.083522,0.14962,0.1545,
0.13968,0.12292,0.090836,0.073869,
0.060678,0.038971,0.021492,0.015531]
tmp[3,4,:] = [0.094265,0.10647,0.19073,0.19696,
0.17807,0.1567,0.1158,0.094169,
0.077353,0.049681,0.027399,0.0198]
tmp[3,5,:] = [0.12769,0.14423,0.25837,0.2668,
0.24121,0.21226,0.15686,0.12756,
0.10478,0.067297,0.037114,0.02682]
tmp[3,6,:] = [0.14534,0.16185,0.29965,0.32723,
0.30654,0.28014,0.21389,0.17747,
0.14842,0.098649,0.056671,0.041627]
tmp[3,7,:] = [0.18528,0.20632,0.382,0.41716,
0.39078,0.35712,0.27267,0.22625,
0.1892,0.12576,0.072245,0.053067]
tmp[3,8,:] = [0.25099,0.27948,0.51745,0.56508,
0.52935,0.48376,0.36936,0.30647,
0.25629,0.17035,0.097862,0.071884]
test_data['Youngs_97_intraslab_test_mean'] = tmp

test_data['Youngs_97_intraslab_test_magnitude'] = [6.1, 6.1, 6.1, 7.2, 7.2, 7.2, 8.3, 8.3, 8.3]

test_data['Youngs_97_intraslab_test_depth'] = [10.0,50.0,100.0,10.0,50.0,100.0,10.0,50.0,100.0]

# ***********************************************************

test_data['Combo_Sadigh_Youngs_M8_test_period'] = [
    0.0000E+00,7.0000E-02,1.0000E-01,2.0000E-01,
    3.0000E-01,4.0000E-01,5.0000E-01,7.5000E-01,
    1.0000E-00,1.5000E-00,2.0000E-00,3.0000E-00]

tmp = zeros((2,3)) # initialise an array: 3 events/mags and distance to 2 sites
tmp[0,:] = [10.0,25.0,50.0] # distance between 1st site and all three events
tmp[1,:] = [50.0,25.0,10.0] # distance between 2nd site and all three events
test_data['Combo_Sadigh_Youngs_M8_test_distance'] = tmp

tmp = zeros((2,3,12)) # 2 sites - 3 events and 12 RSA periods
tmp[0,0,:] = [2.6847E-01,4.4170E-01,5.4026E-01,5.9924E-01,  # meanRSA for site1 - event1
      5.0643E-01,4.0426E-01,3.1130E-01,1.9711E-01,
      1.4119E-01,8.1022E-02,5.3910E-02,2.7935E-02]
tmp[0,1,:] = [1.0433E-01,1.5859E-01,1.9874E-01,2.3497E-01, # meanRSA for site1 - event2
      2.0328E-01,1.6507E-01,1.2971E-01,8.5142E-02,
      6.2797E-02,3.7274E-02,2.5423E-02,1.3534E-02]
tmp[0,2,:] = [1.8915E-01,2.7467E-01,3.4619E-01,4.4380E-01, # meanRSA for site1 - event3
      4.1809E-01,3.9259E-01,3.7183E-01,2.6660E-01,
      1.9858E-01,1.2267E-01,8.2564E-02,3.8355E-02]
tmp[1,0,:] = [3.8676E-02,5.4983E-02,7.0113E-02,8.7934E-02, # meanRSA for site2 - event1
      7.7967E-02,6.4458E-02,5.1740E-02,3.5270E-02,
      2.6825E-02,1.6497E-02,1.1548E-02,6.3250E-03]
tmp[1,1,:] = [1.0433E-01,1.5859E-01,1.9874E-01,2.3497E-01, # meanRSA for site2 - event2
      2.0328E-01,1.6507E-01,1.2971E-01,8.5142E-02,
      6.2797E-02,3.7274E-02,2.5423E-02,1.3534E-02]
tmp[1,2,:] = [2.7888E-01,4.1400E-01,5.1850E-01,6.5197E-01, # meanRSA for site2 - event3
      6.0732E-01,5.6571E-01,5.3245E-01,3.7749E-01,
      2.7896E-01,1.7040E-01,1.1377E-01,5.2258E-02]
test_data['Combo_Sadigh_Youngs_M8_test_mean'] = tmp


test_data['Combo_Sadigh_Youngs_M8_test_magnitude'] = [6.0,6.0,8.8]
test_data['Combo_Sadigh_Youngs_M8_test_depth'] = [10.0]

# ***********************************************************
test_data['Combo_Sadigh_Youngs_M8_trimmed_test_period'] = [
    0.0000E+00,7.5000E-02,1.0000E-01,2.0000E-01,
    3.0000E-01,4.0000E-01,5.0000E-01,7.5000E-01,
    1.0000E-00,1.5000E-00,2.0000E-00,3.0000E-00]

test_data['Combo_Sadigh_Youngs_M8_trimmed_test_distance'] = [10.0,25.0,50.0]

# This data was creating by running the GM model in EQRM
test_data['Combo_Sadigh_Youngs_M8_trimmed_test_mean'] = [
    [[ 0.37461483, 0.62035523, 0.73219532, 0.85177058,  0.76364145, 0.64050752,
    0.52073053, 0.34614203, 0.25454184, 0.15328825, 0.1046282, 0.05682539]],
 [[ 0.1544147, 0.23758813, 0.28608397, 0.35407234, 0.32448126, 0.27655987,
    0.2291531, 0.15755411, 0.11908253, 0.07401914, 0.05170881, 0.02880416]],
 [[ 0.05957871, 0.08608274, 0.105141,  0.13785849, 0.12935183, 0.11216472,
    0.094854, 0.06762632, 0.05264243, 0.03385347, 0.02424689, 0.01387918]]]

test_data['Combo_Sadigh_Youngs_M8_trimmed_test_magnitude'] = [6.5]
test_data['Combo_Sadigh_Youngs_M8_trimmed_test_depth'] = [10.0]

# ***********************************************************


test_data['AllenSEA06_test_period'] = [
    0.0000E+00,2.5000E-02,3.1500E-02,3.9600E-02,4.9900E-02,6.2900E-02,
           7.9100E-02,9.9600E-02,1.2550E-01,1.5800E-01,1.9880E-01,2.5060E-01,
           3.1550E-01,3.9680E-01,5.0000E-01,6.2890E-01,7.9370E-01,1.0000E+00,
           1.2500E+00,1.5870E+00,2.0000E+00,2.5000E+00,3.1250E+00,4.0000E+00,
           5.0000E+00,6.2500E+00,7.6920E+00,1.0000E+01]

test_data['AllenSEA06_test_distance'] = [9,14,21.0]

test_data['AllenSEA06_test_mean'] = array([
    [1.9085E-01,2.8322E-01,3.3223E-01,3.8110E-01,
     4.2045E-01,4.3670E-01,4.3483E-01,4.1459E-01,
     3.7654E-01,3.3145E-01,2.8550E-01,2.3414E-01,
     1.8471E-01,1.3908E-01,1.0155E-01,7.0559E-02,
     4.6963E-02,3.0169E-02,1.9345E-02,1.2098E-02,
     7.3549E-03,4.4177E-03,2.6241E-03,1.5683E-03,
     9.2787E-04,5.6127E-04,3.4052E-04,2.0889E-04],
    [9.6752E-02,1.3946E-01,1.6316E-01,1.8794E-01,
     2.0926E-01,2.1961E-01,2.2178E-01,2.1435E-01,
     1.9805E-01,1.7847E-01,1.5664E-01,1.3041E-01,
     1.0413E-01,7.9163E-02,5.8426E-02,4.1004E-02,
     2.7482E-02,1.7674E-02,1.1320E-02,7.0665E-03,
     4.2918E-03,2.5689E-03,1.5203E-03,9.0654E-04,
     5.3461E-04,3.2263E-04,1.9514E-04,1.1944E-04],
    [5.0838E-02,7.0389E-02,8.1847E-02,9.4674E-02,
     1.0654E-01,1.1362E-01,1.1680E-01,1.1483E-01,
     1.0841E-01,1.0042E-01,9.0105E-02,7.6499E-02,
     6.2215E-02,4.7997E-02,3.5791E-02,2.5390E-02,
     1.7166E-02,1.1080E-02,7.0935E-03,4.4272E-03,
     2.6890E-03,1.6056E-03,9.4663E-04,5.6245E-04,
     3.3037E-04,1.9872E-04,1.1973E-04,7.3048E-05]])
test_data['AllenSEA06_test_mean'] = \
                                  test_data['AllenSEA06_test_mean'] \
                                  [:,newaxis,:]
test_data['AllenSEA06_test_magnitude'] = [5.4]


# ***********************************************************

# Boore_08
test_data['Boore_08_test_period'] = [
    0.0000E+00,3.0000E-01,1.0000E-00]

test_data['Boore_08_test_distance'] = [9,14,21.0]

test_data['Boore_08_test_mean'] = array([
    [8.0160e-002,1.2333e-001,2.8450e-002],
    [5.9491e-002,9.4516e-002,2.0631e-002],
    [4.3928e-002,7.2391e-002,1.5113e-002]])
test_data['Boore_08_test_mean'] = \
                                  test_data['Boore_08_test_mean'] \
                                  [:,newaxis,:]
test_data['Boore_08_test_magnitude'] = [5.4]

test_data['Boore_08_test_Vs30'] = 1000.0


# ***********************************************************
# Somerville09_Yilgarn Test

test_data['Somerville09_Yilgarn_test_period'] = [
    0.0, 0.02, 0.025, 0.035, 0.5, 0.7, 1.0, 1.12,3.5,7.4, 9.0, 10.0]

tmp = zeros((4,3)) # initialise an array: 3 events/mags and distance to 2 sites
tmp[0,:] = [0.0, 0.0, 0.0] # distance between 1st site and all three events
tmp[1,:] = [25.0, 25.0, 25.0] # distance between 2nd site and all three events
tmp[2,:] = [50.0, 50.0, 50.0] # distance between 3rd site and all three events
tmp[3,:] = [100.0, 100.0, 100.0] # distance between 4th site and all three events
test_data['Somerville09_Yilgarn_test_distance'] = tmp

tmp = zeros((4,3,12))
tmp[0,0,:] = [0.79328,1.512,1.6554,1.9091,
0.36389,0.22068,0.14152,0.12499,
0.01109,0.0019151,0.0012792,0.0010013]
tmp[0,1,:] = [1.5367,2.7799,3.0742,3.596,
0.81911,0.63697,0.52424,0.48545,
0.070189,0.012536,0.0081888,0.006321]
tmp[0,2,:] = [1.6209,2.9099,3.2226,3.761,
0.8988,0.70965,0.60964,0.56843,
0.0846,0.015165,0.0099231,0.0076675]
tmp[1,0,:] = [0.10928,0.17754,0.20138,0.24681,
0.070582,0.040713,0.023699,0.023272,
0.0031363,0.00047399,0.00031277,0.00024324]
tmp[1,1,:] = [0.26323,0.41325,0.47071,0.58186,
0.18955,0.13698,0.097419,0.10021,
0.021889,0.0037455,0.002452,0.0018957]
tmp[1,2,:] = [0.28445,0.44407,0.5062,0.62392,
0.21211,0.15523,0.11461,0.1187,
0.026671,0.0046267,0.003039,0.002354]
tmp[2,0,:] = [0.04052,0.061976,0.071099,0.08865,
0.030695,0.017486,0.0098273,0.010196,
0.0016578,0.0002463,0.00016119,0.00012472]
tmp[2,1,:] = [0.10794,0.16087,0.18482,0.23182,
0.089439,0.06315,0.042388,0.046051,
0.012105,0.0021232,0.0013877,0.0010714]
tmp[2,2,:] = [0.11796,0.17497,0.20112,0.25146,
0.101,0.072129,0.050134,0.054834,
0.014824,0.0026482,0.0017379,0.0013449]
tmp[3,0,:] = [0.013381,0.016775,0.019013,0.023782,
0.013916,0.0080393,0.0041025,0.0040427,
0.00094167,0.00012969,8.5674e-005,6.6818e-005]
tmp[3,1,:] = [0.039511,0.048677,0.055099,0.06915,
0.044077,0.031215,0.018588,0.019171,
0.0072013,0.001222,0.00081172,0.00063411]
tmp[3,2,:] = [0.043675,0.053604,0.060687,0.075898,
0.050236,0.035942,0.022105,0.022951,
0.0088643,0.0015393,0.0010274,0.00080483]
test_data['Somerville09_Yilgarn_test_mean'] = tmp

test_data['Somerville09_Yilgarn_test_magnitude'] = [5.5, 6.4, 6.5]

# ***********************************************************
# Somerville09_YilgarnNon_Cratonic Test

test_data['Somerville09_Non_Cratonic_test_period'] = [
    0.0, 0.02, 0.025, 0.035, 0.5, 0.7, 1.0, 1.12,3.5,7.4, 9.0, 10.0]

tmp = zeros((4,3)) # initialise an array: 3 events/mags and distance to 2 sites
tmp[0,:] = [0.0, 0.0, 0.0] # distance between 1st site and all three events
tmp[1,:] = [25.0, 25.0, 25.0] # distance between 2nd site and all three events
tmp[2,:] = [50.0, 50.0, 50.0] # distance between 3rd site and all three events
tmp[3,:] = [100.0, 100.0, 100.0] # distance between 4th site and all three events
test_data['Somerville09_Non_Cratonic_test_distance'] = tmp

# results in g.
tmp = zeros((4,3,12))
tmp[0,0,:] = [0.23261,0.2383,0.24951,0.28746,
0.25858,0.15258,0.068723,0.05897,
0.0063585,0.0011718,0.00076641,0.0005924]
tmp[0,1,:] = [0.44287,0.45193,0.46884,0.52551,
0.59385,0.42222,0.23654,0.21556,
0.037114,0.007854,0.005331,0.0042173]
tmp[0,2,:] = [0.47128,0.48059,0.49794,0.55595,
0.65213,0.47107,0.27697,0.25333,
0.046242,0.0099632,0.0067106,0.0052806]
tmp[1,0,:] = [0.051927,0.052947,0.054827,0.061177,
0.070042,0.039684,0.015283,0.012216,
0.0014495,0.00038765,0.00025227,0.00019306]
tmp[1,1,:] = [0.11946,0.12149,0.12501,0.13694,
0.18693,0.12728,0.057896,0.049729,
0.0097291,0.0029459,0.0020422,0.0016278]
tmp[1,2,:] = [0.12983,0.13196,0.13566,0.14817,
0.20873,0.14435,0.068516,0.059146,
0.012312,0.0037896,0.0026145,0.0020769]
tmp[2,0,:] = [0.0239,0.024321,0.025067,0.027594,
0.035504,0.019874,0.0070684,0.0054533,
0.00069028,0.00022804,0.00014799,0.00011263]
tmp[2,1,:] = [0.060007,0.060941,0.062502,0.067823,
0.10156,0.06824,0.02799,0.023331,
0.0049423,0.0018365,0.0012851,0.0010269]
tmp[2,2,:] = [0.065851,0.066843,0.068501,0.07415,
0.11429,0.077983,0.033288,0.027902,
0.0062992,0.0023778,0.001658,0.0013216]
tmp[3,0,:] = [0.0097428,0.0098659,0.010062,0.010718,
0.016503,0.0095091,0.0038182,0.0030106,
0.00038586,0.00012575,8.2084e-005,6.2826e-005]
tmp[3,1,:] = [0.02675,0.027051,0.027491,0.02899,
0.050682,0.03501,0.01582,0.013553,
0.0029513,0.0010747,0.00076577,0.00062048]
tmp[3,2,:] = [0.029648,0.02997,0.030437,0.032034,
0.057482,0.04032,0.01891,0.0163,
0.0037893,0.0014006,0.00099592,0.0008057]
test_data['Somerville09_Non_Cratonic_test_mean'] = tmp

test_data['Somerville09_Non_Cratonic_test_magnitude'] = [5.5, 6.4, 6.5]

################################################################################
# Liang_2008 Test

test_data['Liang_2008_test_period'] = [0.1, 1.0, 10.0]

tmp = zeros((4,4)) # initialise an array: 4 events/mags and distance to 4 sites
tmp[0,:] = [ 50.0,  50.0,  50.0,  50.0] # distance - 1st site and all 4 events
tmp[1,:] = [100.0, 100.0, 100.0, 100.0] # distance - 2nd site and all 4 events
tmp[2,:] = [150.0, 150.0, 150.0, 150.0] # distance - 3rd site and all 4 events
tmp[3,:] = [200.0, 200.0, 200.0, 200.0] # distance - 4th site and all 4 events
test_data['Liang_2008_test_distance'] = tmp

# result values, in 'g' - values taken from spreadsheet
tmp = zeros((4,4,3))		# distance, magnitude, period
# period:     0.1       1.0       10.0
tmp[0,0,:] = [5.16E-03, 8.72E-04, 5.89E-06]	# R= 50.0, ML=4.0
tmp[0,1,:] = [1.72E-02, 4.40E-03, 7.56E-05]	# R= 50.0, ML=5.0
tmp[0,2,:] = [5.72E-02, 2.22E-02, 9.70E-04]	# R= 50.0, ML=6.0
tmp[0,3,:] = [1.90E-01, 1.12E-01, 1.24E-02]	# R= 50.0, ML=7.0
tmp[1,0,:] = [2.04E-03, 3.05E-04, 1.96E-06]	# R=100.0, ML=4.0
tmp[1,1,:] = [6.66E-03, 1.46E-03, 2.59E-05]	# R=100.0, ML=5.0
tmp[1,2,:] = [2.17E-02, 7.03E-03, 3.43E-04]	# R=100.0, ML=6.0
tmp[1,3,:] = [7.09E-02, 3.38E-02, 4.53E-03]	# R=100.0, ML=7.0
tmp[2,0,:] = [9.62E-04, 1.11E-04, 6.92E-07]	# R=150.0, ML=4.0
tmp[2,1,:] = [3.11E-03, 5.19E-04, 9.33E-06]	# R=150.0, ML=5.0
tmp[2,2,:] = [1.00E-02, 2.42E-03, 1.26E-04]	# R=150.0, ML=6.0
tmp[2,3,:] = [3.23E-02, 1.13E-02, 1.69E-03]	# R=150.0, ML=7.0
tmp[3,0,:] = [4.88E-04, 4.12E-05, 2.51E-07]	# R=200.0, ML=4.0
tmp[3,1,:] = [1.56E-03, 1.89E-04, 3.43E-06]	# R=200.0, ML=5.0
tmp[3,2,:] = [5.01E-03, 8.63E-04, 4.68E-05]	# R=200.0, ML=6.0
tmp[3,3,:] = [1.60E-02, 3.95E-03, 6.38E-04]	# R=200.0, ML=7.0
test_data['Liang_2008_test_mean'] = tmp

test_data['Liang_2008_test_magnitude'] = [4.0, 5.0, 6.0, 7.0]

################################################################################
# Atkinson06_hard_bedrock Test

# num_events = 2
test_data['Atkinson06_hard_bedrock_test_magnitude'] = [5.5, 7.5]

# num_periods = 4
test_data['Atkinson06_hard_bedrock_test_period'] = [0.0, 0.2, 1.0, 2.0]

# num_sites = 4
tmp = zeros((4,2)) # initialise an array: (num_sites, num_events)
tmp[0,:] = [  2.0,   2.0,] # distance - 1st site and all 2 events
tmp[1,:] = [ 10.0,  10.0,] # distance - 2nd site and all 2 events
tmp[2,:] = [100.0, 100.0,] # distance - 3rd site and all 2 events
tmp[3,:] = [300.0, 300.0,] # distance - 4th site and all 2 events
test_data['Atkinson06_hard_bedrock_test_distance'] = tmp

# result values, in 'g'
tmp = zeros((4,2,4))		# num_sites, num_events, num_periods
# period:     0.0             0.2             1.0             2.0
tmp[0,0,:] = [2.05886715e+00, 1.65781599e+00, 1.86334093e-01, 5.38980837e-02]
tmp[0,1,:] = [3.69888070e+00, 3.18351811e+00, 6.39932732e-01, 2.79706349e-01]
tmp[1,0,:] = [3.12967560e-01, 2.46010886e-01, 2.76451738e-02, 7.46035209e-03]
tmp[1,1,:] = [1.15744223e+00, 1.15227018e+00, 2.59190646e-01, 1.20992743e-01]
tmp[2,0,:] = [8.17435180e-03, 1.35485346e-02, 2.21682967e-03, 6.17112473e-04]
tmp[2,1,:] = [5.61299072e-02, 1.05659445e-01, 3.72615850e-02, 1.99310108e-02]
tmp[3,0,:] = [1.91430143e-03, 4.55815747e-03, 1.15997953e-03, 3.50372752e-04]
tmp[3,1,:] = [1.81590165e-02, 3.94234225e-02, 2.09360296e-02, 1.26037078e-02]
test_data['Atkinson06_hard_bedrock_test_mean'] = tmp

################################################################################
# Atkinson06_soil Test
# Set Vs30 to 1000.0 for the soil test code below

# num_events = 2
test_data['Atkinson06_soil_test_magnitude'] = [5.5, 7.5]

# num_periods = 3
test_data['Atkinson06_soil_test_period'] = [0.2, 1.0, 2.0]

# num_sites = 3
test_data['Atkinson06_soil_test_Vs30'] = [1000.0, 1000.0, 1000.0]

# num_sites = 3
tmp = zeros((3,2)) # initialise an array: (num_sites, num_events)
tmp[0,:] = [  2.0,   2.0] # distance - 1st site and all 2 events
tmp[1,:] = [ 10.0,  10.0] # distance - 2nd site and all 2 events
tmp[2,:] = [100.0, 100.0] # distance - 3rd site and all 2 events
test_data['Atkinson06_soil_test_distance'] = tmp

# result values, in 'g'
tmp = zeros((3,2,3))		# num_sites, num_events, num_periods
# values below are from Atkinson06_soil_check.py, Vs30=1000.0
# period:       0.2        1.0        2.0
#tmp[0,0,:] = [ 3.174586,  2.178382,  1.636088]	# R=  2.0, ML=5.5
#tmp[0,1,:] = [ 3.457957,  2.714225,  2.351217]	# R=  2.0, ML=7.5
#tmp[1,0,:] = [ 2.346004,  1.349710,  0.777274]	# R= 10.0, ML=5.5
#tmp[1,1,:] = [ 3.016604,  2.321710,  1.987274]	# R= 10.0, ML=7.5
#tmp[2,0,:] = [ 1.086942,  0.253822, -0.305121]	# R=100.0, ML=5.5
#tmp[2,1,:] = [ 1.978958,  1.479352,  1.204044]	# R=100.0, ML=7.5

# values above are log10 cmm/s/s, here converted to ln g, then g:
tmp[0,0,:] = [1.52428201e+00, 1.53766357e-01, 4.41130742e-02]
tmp[0,1,:] = [2.92709167e+00, 5.28085599e-01, 2.28926635e-01]
tmp[1,0,:] = [2.26195169e-01, 2.28133637e-02, 6.10595114e-03]
tmp[1,1,:] = [1.05945697e+00, 2.13889431e-01, 9.90269321e-02]
tmp[2,0,:] = [1.24572255e-02, 1.82936904e-03, 5.05077852e-04]
tmp[2,1,:] = [9.71487740e-02, 3.07490232e-02, 1.63126052e-02]
test_data['Atkinson06_soil_test_mean'] = tmp

################################################################################
# Atkinson06_bc_boundary_bedrock Test

# num_events = 2
test_data['Atkinson06_bc_boundary_bedrock_test_magnitude'] = [5.5, 7.5]

# num_periods = 2
test_data['Atkinson06_bc_boundary_bedrock_test_period'] = [0.2, 1.0]

# num_sites = 3
tmp = zeros((3,2)) # initialise an array: (num_sites, num_events)
tmp[0,:] = [ 10.0,  10.0] # distance - 1st site and all 2 events
tmp[1,:] = [100.0, 100.0] # distance - 2nd site and all 2 events
tmp[2,:] = [300.0, 300.0] # distance - 3rd site and all 2 events
test_data['Atkinson06_bc_boundary_bedrock_test_distance'] = tmp

# result values, in 'g'
tmp = zeros((3,2,2))		# num_sites, num_events, num_periods
# period:      0.2       1.0
#tmp[0,0,:] = [2.512575, 1.559360]	# R= 10.0, ML=5.5
#tmp[0,1,:] = [3.201975, 2.531360]	# R= 10.0, ML=7.5
#tmp[1,0,:] = [1.253036, 0.455175]	# R=100.0, ML=5.5
#tmp[1,1,:] = [2.148640, 1.665492]	# R=100.0, ML=7.5
#tmp[2,0,:] = [0.778744, 0.166573]	# R=300.0, ML=5.5
#tmp[2,1,:] = [2.148640, 1.412705]	# R=300.0, ML=7.5

# values above are log10 cmm/s/s, converted programmatically to ln g, then g:
# period:      0.2       1.0
tmp[0,0,:] = [0.331936, 0.036969]	# R= 10.0, ML=5.5
tmp[0,1,:] = [1.623508, 0.346609]	# R= 10.0, ML=7.5
tmp[1,0,:] = [0.018261, 0.002908]	# R=100.0, ML=5.5
tmp[1,1,:] = [0.143588, 0.047203]	# R=100.0, ML=7.5
tmp[2,0,:] = [0.006127, 0.001496]	# R=300.0, ML=5.5
tmp[2,1,:] = [0.053912, 0.026374]	# R=300.0, ML=7.5
test_data['Atkinson06_bc_boundary_bedrock_test_mean'] = tmp
del tmp

#################################################################################
## Chiou08 Tests - Rock - compare code against 'hand' code results
#
## Vs30 value
#test_data['Chiou08_test_Vs30'] = 520.0
#
## num_events = 2
#test_data['Chiou08_test_magnitude'] = [5.5, 7.5]
#
## num_events = 2
#test_data['Chiou08_test_depth_to_top'] = [0.0, 0.0]
#
## num_events = 2
## 'reverse' fault type index is 0
#test_data['Chiou08_test_fault_type'] = [0, 0]
#
## num_periods = 4
#test_data['Chiou08_test_period'] = [0.01, 0.20, 1.00, 3.00]
#
## num_sites = 3
#tmp = zeros((3,2)) # initialise an array: (num_sites, num_events)
#tmp[0,:] = [  5.0,   5.0] # distance - 1st site and all 2 events
#tmp[1,:] = [ 20.0,  20.0] # distance - 2nd site and all 2 events
#tmp[2,:] = [100.0, 100.0] # distance - 3rd site and all 2 events
#test_data['Chiou08_test_distance'] = tmp
#
## result values, in 'g'
#tmp = zeros((3,2,4))		# num_sites, num_events, num_periods
## period:     0.01      0.20      1.00      3.00
#tmp[0,0,:] = [0.276160, 0.612666, 0.139772, 0.017631] # R=  5.0, ML=5.5
#tmp[0,1,:] = [0.525535, 1.230800, 0.503488, 0.112815] # R=  5.0, ML=7.5
#tmp[1,0,:] = [0.068560, 0.150721, 0.032357, 0.004130] # R= 20.0, ML=5.5
#tmp[1,1,:] = [0.242421, 0.585651, 0.206465, 0.046410] # R= 20.0, ML=7.5
#tmp[2,0,:] = [0.006308, 0.013925, 0.004896, 0.000717] # R=100.0, ML=5.5
#tmp[2,1,:] = [0.052239, 0.117515, 0.055062, 0.013557] # R=100.0, ML=7.5
#test_data['Chiou08_test_mean'] = tmp
#del tmp
#
################################################################################
# Chiou08 Tests - Soil - compare code against BooreFTN code results

# num_periods = 3
test_data['Chiou08_test_period'] = [0.01, 1.0, 3.0]

# num_events = 3
test_data['Chiou08_test_magnitude'] = [4.0, 5.5, 7.0]

# num_sites = 3
tmp = zeros((3,3)) # initialize an array: (num_sites, num_events)
tmp[0,:] = [  5.0,   5.0,   5.0] # distance - site 1 & all 3 events
tmp[1,:] = [ 25.0,  25.0,  25.0] # distance - site 2 & all 3 events
tmp[2,:] = [100.0, 100.0, 100.0] # distance - site 3 & all 3 events
test_data['Chiou08_test_distance'] = tmp

# num_events = 3
test_data['Chiou08_test_depth_to_top'] = [0.0, 0.0, 0.0]

# num_events = 3
test_data['Chiou08_test_dip'] = [90.0, 90.0, 90.0]

# num_sites = 3
test_data['Chiou08_test_Vs30'] = [300.0, 300.0, 300.0]

# num_events = 3
# 'reverse' fault type index is 0
# 'normal' fault type index is 1
# 'strikeslip' fault type index is 2
#                                       SS SS SS
test_data['Chiou08_test_fault_type'] = [2, 2, 2]

# mean values, in 'g'
tmp = zeros((3,3,3))    # (num_sites, num_events, num_periods)
tmp[0,0,0] = 5.581E-02 # Rrup=  5.0, Mw=4.0, T=0.01
tmp[1,0,0] = 6.411E-03 # Rrup= 25.0, Mw=4.0, T=0.01
tmp[2,0,0] = 4.692E-04 # Rrup=100.0, Mw=4.0, T=0.01
tmp[0,1,0] = 2.679E-01 # Rrup=  5.0, Mw=5.5, T=0.01
tmp[1,1,0] = 5.575E-02 # Rrup= 25.0, Mw=5.5, T=0.01
tmp[2,1,0] = 7.231E-03 # Rrup=100.0, Mw=5.5, T=0.01
tmp[0,2,0] = 4.268E-01 # Rrup=  5.0, Mw=7.0, T=0.01
tmp[1,2,0] = 1.565E-01 # Rrup= 25.0, Mw=7.0, T=0.01
tmp[2,2,0] = 3.701E-02 # Rrup=100.0, Mw=7.0, T=0.01
tmp[0,0,1] = 9.876E-03 # Rrup=  5.0, Mw=4.0, T=1.00
tmp[1,0,1] = 1.182E-03 # Rrup= 25.0, Mw=4.0, T=1.00
tmp[2,0,1] = 1.864E-04 # Rrup=100.0, Mw=4.0, T=1.00
tmp[0,1,1] = 1.861E-01 # Rrup=  5.0, Mw=5.5, T=1.00
tmp[1,1,1] = 3.414E-02 # Rrup= 25.0, Mw=5.5, T=1.00
tmp[2,1,1] = 7.010E-03 # Rrup=100.0, Mw=5.5, T=1.00
tmp[0,2,1] = 5.130E-01 # Rrup=  5.0, Mw=7.0, T=1.00
tmp[1,2,1] = 1.588E-01 # Rrup= 25.0, Mw=7.0, T=1.00
tmp[2,2,1] = 4.728E-02 # Rrup=100.0, Mw=7.0, T=1.00
tmp[0,0,2] = 8.548E-04 # Rrup=  5.0, Mw=4.0, T=3.00
tmp[1,0,2] = 1.064E-04 # Rrup= 25.0, Mw=4.0, T=3.00
tmp[2,0,2] = 2.024E-05 # Rrup=100.0, Mw=4.0, T=3.00
tmp[0,1,2] = 3.169E-02 # Rrup=  5.0, Mw=5.5, T=3.00
tmp[1,1,2] = 5.605E-03 # Rrup= 25.0, Mw=5.5, T=3.00
tmp[2,1,2] = 1.293E-03 # Rrup=100.0, Mw=5.5, T=3.00
tmp[0,2,2] = 1.561E-01 # Rrup=  5.0, Mw=7.0, T=3.00
tmp[1,2,2] = 4.511E-02 # Rrup= 25.0, Mw=7.0, T=3.00
tmp[2,2,2] = 1.415E-02 # Rrup=100.0, Mw=7.0, T=3.00
test_data['Chiou08_test_mean'] = tmp

# sigma values, in 'g'
tmp = zeros((3,3,3))    # (num_sites, num_events, num_periods)
tmp[0,0,0] = 6.508E-01 # Rrup=  5.0, Mw=4.0, T=0.01
tmp[1,0,0] = 6.718E-01 # Rrup= 25.0, Mw=4.0, T=0.01
tmp[2,0,0] = 6.750E-01 # Rrup=100.0, Mw=4.0, T=0.01
tmp[0,1,0] = 5.770E-01 # Rrup=  5.0, Mw=5.5, T=0.01
tmp[1,1,0] = 6.140E-01 # Rrup= 25.0, Mw=5.5, T=0.01
tmp[2,1,0] = 6.334E-01 # Rrup=100.0, Mw=5.5, T=0.01
tmp[0,2,0] = 4.649E-01 # Rrup=  5.0, Mw=7.0, T=0.01
tmp[1,2,0] = 4.844E-01 # Rrup= 25.0, Mw=7.0, T=0.01
tmp[2,2,0] = 5.090E-01 # Rrup=100.0, Mw=7.0, T=0.01
tmp[0,0,1] = 6.931E-01 # Rrup=  5.0, Mw=4.0, T=1.00
tmp[1,0,1] = 6.958E-01 # Rrup= 25.0, Mw=4.0, T=1.00
tmp[2,0,1] = 6.961E-01 # Rrup=100.0, Mw=4.0, T=1.00
tmp[0,1,1] = 6.539E-01 # Rrup=  5.0, Mw=5.5, T=1.00
tmp[1,1,1] = 6.744E-01 # Rrup= 25.0, Mw=5.5, T=1.00
tmp[2,1,1] = 6.817E-01 # Rrup=100.0, Mw=5.5, T=1.00
tmp[0,2,1] = 6.063E-01 # Rrup=  5.0, Mw=7.0, T=1.00
tmp[1,2,1] = 6.206E-01 # Rrup= 25.0, Mw=7.0, T=1.00
tmp[2,2,1] = 6.353E-01 # Rrup=100.0, Mw=7.0, T=1.00
tmp[0,0,2] = 7.266E-01 # Rrup=  5.0, Mw=4.0, T=3.00
tmp[1,0,2] = 7.268E-01 # Rrup= 25.0, Mw=4.0, T=3.00
tmp[2,0,2] = 7.268E-01 # Rrup=100.0, Mw=4.0, T=3.00
tmp[0,1,2] = 7.181E-01 # Rrup=  5.0, Mw=5.5, T=3.00
tmp[1,1,2] = 7.202E-01 # Rrup= 25.0, Mw=5.5, T=3.00
tmp[2,1,2] = 7.209E-01 # Rrup=100.0, Mw=5.5, T=3.00
tmp[0,2,2] = 6.992E-01 # Rrup=  5.0, Mw=7.0, T=3.00
tmp[1,2,2] = 7.007E-01 # Rrup= 25.0, Mw=7.0, T=3.00
tmp[2,2,2] = 7.024E-01 # Rrup=100.0, Mw=7.0, T=3.00
test_data['Chiou08_test_sigma'] = tmp


del tmp

################################################################################
# Campbell03 Tests - data values from Campbell03_check.py

# num_events = 2
test_data['Campbell03_test_magnitude'] = [5.0, 7.0]

# num_periods = 4
test_data['Campbell03_test_period'] = [0.01, 0.20, 1.00, 3.00]

# num_sites = 4
tmp = zeros((4,2)) # initialise an array: (num_sites, num_events)
tmp[0,:] = [   1.0,    1.0] # distance - 1st site and all 2 events
tmp[1,:] = [  10.0,   10.0] # distance - 2nd site and all 2 events
tmp[2,:] = [ 100.0,  100.0] # distance - 3rd site and all 2 events
tmp[3,:] = [1000.0, 1000.0] # distance - 4th site and all 2 events
test_data['Campbell03_test_distance'] = tmp

# result values, in 'g'
tmp = zeros((4,2,4))		# num_sites, num_events, num_periods
# period:     0.01     0.20     1.00     3.00
tmp[0,0,:] = [0.94335, 0.87035, 0.08436, 0.01070] # R=   1.0, ML=5.0
tmp[0,1,:] = [1.39528, 1.49996, 0.54330, 0.13621] # R=   1.0, ML=7.0
tmp[1,0,:] = [0.29592, 0.28207, 0.02536, 0.00341] # R=  10.0, ML=5.0
tmp[1,1,:] = [0.94139, 1.06850, 0.36296, 0.09306] # R=  10.0, ML=7.0
tmp[2,0,:] = [0.01184, 0.01847, 0.00235, 0.00036] # R= 100.0, ML=5.0
tmp[2,1,:] = [0.07015, 0.12086, 0.04793, 0.01376] # R= 100.0, ML=7.0
tmp[3,0,:] = [0.00013, 0.00017, 0.00014, 0.00005] # R=1000.0, ML=5.0
tmp[3,1,:] = [0.00189, 0.00208, 0.00358, 0.00206] # R=1000.0, ML=7.0
test_data['Campbell03_test_mean'] = tmp
del tmp

################################################################################
# Campbell08 Tests - test against data values from Campbell08_check.py
#                    which got good agreement against FORTRAN code

class Campbell08_distance_object(object):
    def __init__(self, Rrup, Rjb):
        self.Rupture = Rrup
        self.Joyner_Boore = Rjb

    def distance(self, type):
        """We *must* define a 'distance' method, results unused."""

        return self.Rupture

# Rrup distances - num_sites = 7
tmp = zeros((7,4)) # initialise an array: (num_sites, num_events)
tmp[0,:] = [  5.0,   5.0,   5.0,   5.0] # Rrup - 1st site and all 4 events
tmp[1,:] = [ 10.0,  10.0,  10.0,  10.0] # Rrup - 2nd site and all 4 events
tmp[2,:] = [ 15.0,  15.0,  15.0,  15.0] # Rrup - 3rd site and all 4 events
tmp[3,:] = [ 30.0,  30.0,  30.0,  30.0] # Rrup - 4th site and all 4 events
tmp[4,:] = [ 50.0,  50.0,  50.0,  50.0] # Rrup - 5th site and all 4 events
tmp[5,:] = [100.0, 100.0, 100.0, 100.0] # Rrup - 6th site and all 4 events
tmp[6,:] = [200.0, 200.0, 200.0, 200.0] # Rrup - 7th site and all 4 events
Campbell08_Rrup = tmp
del tmp

# Rjb distances - num_sites = 7 - values from check code
tmp = zeros((7,4)) # initialise an array: (num_sites, num_events)
tmp[0,:] = [  0.0,   0.0,   0.0,   0.0] # Rjb - 1st site and all 4 events
tmp[1,:] = [  0.0,   0.0,   0.0,   0.0] # Rjb - 2nd site and all 4 events
tmp[2,:] = [  6.2,   6.2,   6.2,   6.2] # Rjb - 3rd site and all 4 events
tmp[3,:] = [ 26.0,  26.0,  26.0,  26.0] # Rjb - 4th site and all 4 events
tmp[4,:] = [ 47.7,  47.7,  47.7,  47.7] # Rjb - 5th site and all 4 events
tmp[5,:] = [ 98.9,  98.9,  98.9,  98.9] # Rjb - 6th site and all 4 events
tmp[6,:] = [199.4, 199.4, 199.4, 199.4] # Rjb - 7th site and all 4 events
Campbell08_Rjb = tmp
del tmp

# test distance object
test_data['Campbell08_test_distance_object'] = \
        Campbell08_distance_object(Campbell08_Rrup, Campbell08_Rjb)

# num_events = 4
test_data['Campbell08_test_magnitude'] = [5.0, 7.0, 5.0, 7.0]

# num_events = 4
test_data['Campbell08_test_dip'] = [90.0, 90.0, 45.0, 45.0]

# num_events = 4
test_data['Campbell08_test_depth_to_top'] = [5.0, 0.0, 5.0, 0.0]

# num_events = 4
# 'strikeslip' fault type index is 2, 'reverse' is 0
test_data['Campbell08_test_fault_type'] = [2, 2, 0, 0]

# num_periods = 4
test_data['Campbell08_test_period'] = [0.01, 0.20, 1.00, 3.00]

# Z25 override - num_sites = 7
test_data['Campbell08_test_Z25'] = [2.0]

# Vs30 override - num_sites = 7
test_data['Campbell08_test_Vs30'] = [760.0, 760.0, 760.0, 760.0, 760.0,
                                     760.0, 760.0]

# result values, in 'g' - from 'check' code
tmp = zeros((7,4,4))		# num_sites, num_events, num_periods
# period:     0.01       0.20       1.00       3.00
tmp[0,0,:] = [1.7519e-1, 3.6164e-1, 4.8140e-2, 5.4202e-3] # R=  5.0, ML=5.0, type=SS
tmp[0,1,:] = [3.6907e-1, 8.7425e-1, 2.6571e-1, 7.5109e-2] # R=  5.0, ML=7.0, type=SS
tmp[0,2,:] = [2.3079e-1, 4.7850e-1, 6.2123e-2, 5.4202e-3] # R=  5.0, ML=5.0, type=RV
tmp[0,3,:] = [5.9403e-1, 1.4271e+0, 4.3373e-1, 8.7614e-2] # R=  5.0, ML=7.0, type=RV
tmp[1,0,:] = [1.0306e-1, 2.3247e-1, 2.6472e-2, 2.9806e-3] # R= 10.0, ML=5.0, type=SS
tmp[1,1,:] = [2.5133e-1, 6.2711e-1, 1.7438e-1, 4.9290e-2] # R= 10.0, ML=7.0, type=SS
tmp[1,2,:] = [1.3598e-1, 3.0758e-1, 3.4162e-2, 2.9806e-3] # R= 10.0, ML=5.0, type=RV
tmp[1,3,:] = [4.0581e-1, 1.0236e+0, 2.8464e-1, 5.7497e-2] # R= 10.0, ML=7.0, type=RV
tmp[2,0,:] = [6.7652e-2, 1.5587e-1, 1.7386e-2, 1.9575e-3] # R= 15.0, ML=5.0, type=SS
tmp[2,1,:] = [1.8523e-1, 4.6434e-1, 1.2968e-1, 3.6657e-2] # R= 15.0, ML=7.0, type=SS
tmp[2,2,:] = [8.9346e-2, 2.0624e-1, 2.2436e-2, 1.9575e-3] # R= 15.0, ML=5.0, type=RV
tmp[2,3,:] = [2.4577e-1, 6.1899e-1, 1.7287e-1, 4.0123e-2] # R= 15.0, ML=7.0, type=RV
tmp[3,0,:] = [2.9958e-2, 6.7581e-2, 8.0680e-3, 9.0840e-4] # R= 30.0, ML=5.0, type=SS
tmp[3,1,:] = [1.0249e-1, 2.4772e-1, 7.5513e-2, 2.1345e-2] # R= 30.0, ML=7.0, type=SS
tmp[3,2,:] = [3.9604e-2, 8.9419e-2, 1.0411e-2, 9.0840e-4] # R= 30.0, ML=5.0, type=RV
tmp[3,3,:] = [1.0934e-1, 2.6445e-1, 8.0612e-2, 2.1788e-2] # R= 30.0, ML=7.0, type=RV
tmp[4,0,:] = [1.5913e-2, 3.4483e-2, 4.5128e-3, 5.0811e-4] # R= 50.0, ML=5.0, type=SS
tmp[4,1,:] = [6.4653e-2, 1.4937e-1, 5.0154e-2, 1.4177e-2] # R= 50.0, ML=7.0, type=SS
tmp[4,2,:] = [2.1045e-2, 4.5625e-2, 5.8236e-3, 5.0811e-4] # R= 50.0, ML=5.0, type=RV
tmp[4,3,:] = [6.6118e-2, 1.5278e-1, 5.1297e-2, 1.4278e-2] # R= 50.0, ML=7.0, type=RV
tmp[5,0,:] = [6.6525e-3, 1.3498e-2, 2.0392e-3, 2.2960e-4] # R=100.0, ML=5.0, type=SS
tmp[5,1,:] = [3.4220e-2, 7.3795e-2, 2.8662e-2, 8.1019e-3] # R=100.0, ML=7.0, type=SS
tmp[5,2,:] = [8.8004e-3, 1.7860e-2, 2.6315e-3, 2.2960e-4] # R=100.0, ML=5.0, type=RV
tmp[5,3,:] = [3.4404e-2, 7.4914e-2, 2.8817e-2, 8.1156e-3] # R=100.0, ML=7.0, type=RV
tmp[6,0,:] = [2.7675e-3, 5.2378e-3, 9.1954e-4, 1.0353e-4] # R=200.0, ML=5.0, type=SS
tmp[6,1,:] = [1.8031e-2, 3.6219e-2, 1.6356e-2, 4.6234e-3] # R=200.0, ML=7.0, type=SS
tmp[6,2,:] = [3.6614e-3, 6.9303e-3, 1.1866e-3, 1.0353e-4] # R=200.0, ML=5.0, type=RV
tmp[6,3,:] = [1.8058e-2, 3.6272e-2, 1.6380e-2, 4.6256e-3] # R=200.0, ML=7.0, type=RV

test_data['Campbell08_test_mean'] = tmp
del tmp

# sigma values, in ln('g') - from 'check' code
tmp = zeros((7,4,4))		# num_sites, num_events, num_periods
# period:     0.01                 0.20                 1.00                 3.00
tmp[0,0,:] = [math.log(4.7403e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=  5.0, ML=5.0, type=SS
tmp[0,1,:] = [math.log(4.7094e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=  5.0, ML=7.0, type=SS
tmp[0,2,:] = [math.log(4.7303e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=  5.0, ML=5.0, type=RV
tmp[0,3,:] = [math.log(4.6852e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=  5.0, ML=7.0, type=RV
tmp[1,0,:] = [math.log(4.7551e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 10.0, ML=5.0, type=SS
tmp[1,1,:] = [math.log(4.7268e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 10.0, ML=7.0, type=SS
tmp[1,2,:] = [math.log(4.7481e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 10.0, ML=5.0, type=RV
tmp[1,3,:] = [math.log(4.7047e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 10.0, ML=7.0, type=RV
tmp[2,0,:] = [math.log(4.7631e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 15.0, ML=5.0, type=SS
tmp[2,1,:] = [math.log(4.7384e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 15.0, ML=7.0, type=SS
tmp[2,2,:] = [math.log(4.7581e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 15.0, ML=5.0, type=RV
tmp[2,3,:] = [math.log(4.7277e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 15.0, ML=7.0, type=RV
tmp[3,0,:] = [math.log(4.7723e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 30.0, ML=5.0, type=SS
tmp[3,1,:] = [math.log(4.7552e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 30.0, ML=7.0, type=SS
tmp[3,2,:] = [math.log(4.7699e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 30.0, ML=5.0, type=RV
tmp[3,3,:] = [math.log(4.7537e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 30.0, ML=7.0, type=RV
tmp[4,0,:] = [math.log(4.7758e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 50.0, ML=5.0, type=SS
tmp[4,1,:] = [math.log(4.7638e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 50.0, ML=7.0, type=SS
tmp[4,2,:] = [math.log(4.7745e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 50.0, ML=5.0, type=RV
tmp[4,3,:] = [math.log(4.7635e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 50.0, ML=7.0, type=RV
tmp[5,0,:] = [math.log(4.7782e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=100.0, ML=5.0, type=SS
tmp[5,1,:] = [math.log(4.7712e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=100.0, ML=7.0, type=SS
tmp[5,2,:] = [math.log(4.7777e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=100.0, ML=5.0, type=RV
tmp[5,3,:] = [math.log(4.7711e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=100.0, ML=7.0, type=RV
tmp[6,0,:] = [math.log(4.7793e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=200.0, ML=5.0, type=SS
tmp[6,1,:] = [math.log(4.7753e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=200.0, ML=7.0, type=SS
tmp[6,2,:] = [math.log(4.7790e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=200.0, ML=5.0, type=RV
tmp[6,3,:] = [math.log(4.7753e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=200.0, ML=7.0, type=RV

#tmp = zeros((7,2,4))		# num_sites, num_events, num_periods
## period:     0.01                 0.20                 1.00                 3.00
#tmp[0,0,:] = [math.log(4.7403e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=  5.0, ML=5.0, type=SS
#tmp[0,1,:] = [math.log(4.7094e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=  5.0, ML=7.0, type=SS
#tmp[1,0,:] = [math.log(4.7551e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 10.0, ML=5.0, type=SS
#tmp[1,1,:] = [math.log(4.7268e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 10.0, ML=7.0, type=SS
#tmp[2,0,:] = [math.log(4.7631e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 15.0, ML=5.0, type=SS
#tmp[2,1,:] = [math.log(4.7384e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 15.0, ML=7.0, type=SS
#tmp[3,0,:] = [math.log(4.7723e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 30.0, ML=5.0, type=SS
#tmp[3,1,:] = [math.log(4.7552e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 30.0, ML=7.0, type=SS
#tmp[4,0,:] = [math.log(4.7758e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 50.0, ML=5.0, type=SS
#tmp[4,1,:] = [math.log(4.7638e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R= 50.0, ML=7.0, type=SS
#tmp[5,0,:] = [math.log(4.7782e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=100.0, ML=5.0, type=SS
#tmp[5,1,:] = [math.log(4.7712e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=100.0, ML=7.0, type=SS
#tmp[6,0,:] = [math.log(4.7793e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=200.0, ML=5.0, type=SS
#tmp[6,1,:] = [math.log(4.7753e-1), math.log(5.3400e-1), math.log(5.6800e-1), math.log(5.5800e-1)] # R=200.0, ML=7.0, type=SS

test_data['Campbell08_test_sigma'] = tmp
del tmp

################################################################################
# Abrahamson08 Tests - test against data values from the 'check' code.

# num_events = 8
test_data['Abrahamson08_test_magnitude'] = [5.0, 7.0, 5.0, 7.0, 5.0, 7.0, 5.0, 7.0]

# num_events = 8
test_data['Abrahamson08_test_dip'] = [90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 60.0, 60.0]

# num_events = 8
test_data['Abrahamson08_test_width'] = [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]

# num_events = 8
#                                              SS   SS   RV   RV   NM   NM   RV   RV
test_data['Abrahamson08_test_depth_to_top'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.0, 5.0]

# num_events = 8
# 'reverse' fault type index is 0
# 'normal' fault type index is 1
# 'strikeslip' fault type index is 2
#                                            SS SS RV RV NM NM RV RV
test_data['Abrahamson08_test_fault_type'] = [2, 2, 0, 0, 1, 1, 0, 0]

# num_periods = 4
test_data['Abrahamson08_test_period'] = [0.01, 0.20, 1.00, 3.00]

# Vs30 override - num_sites = 3
test_data['Abrahamson08_test_Vs30'] = [760.0, 760.0, 300.0]

# num_sites = 3
tmp = zeros((3,8)) # initialise an array: (num_sites, num_events)
#              SS     SS     RV     RV     NM     NM     RV     RV
tmp[0,:] = [  5.0,   5.0,   5.0,   5.0,   5.0,   5.0,   5.0,   5.0] # distance - 1st site, 8 events
tmp[1,:] = [ 20.0,  20.0,  20.0,  20.0,  20.0,  20.0,  20.0,  20.0] # distance - 2nd site, 8 events
tmp[2,:] = [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0] # distance - 3rd site, 8 events
test_data['Abrahamson08_test_distance'] = tmp

# result values, in 'g'
tmp = zeros((3,8,4))		# num_sites, num_events, num_periods
# period:     0.01                 0.20                 1.00                 3.00
tmp[0,0,:] = [math.exp(1.462E-01), math.exp(3.215E-01), math.exp(4.251E-02), math.exp(5.188E-03)] # R=  5.0, ML=5.0, Vs30=760 SS
tmp[0,1,:] = [math.exp(3.470E-01), math.exp(7.928E-01), math.exp(2.560E-01), math.exp(6.410E-02)] # R=  5.0, ML=7.0, Vs30=760 SS
tmp[0,2,:] = [math.exp(1.462E-01), math.exp(3.316E-01), math.exp(4.605E-02), math.exp(5.621E-03)] # R=  5.0, ML=5.0, Vs30=760 RV
tmp[0,3,:] = [math.exp(3.470E-01), math.exp(8.177E-01), math.exp(2.773E-01), math.exp(6.944E-02)] # R=  5.0, ML=7.0, Vs30=760 RV
tmp[0,4,:] = [math.exp(1.378E-01), math.exp(3.028E-01), math.exp(4.003E-02), math.exp(4.886E-03)] # R=  5.0, ML=5.0, Vs30=760 NM
tmp[0,5,:] = [math.exp(3.272E-01), math.exp(7.467E-01), math.exp(2.411E-01), math.exp(6.036E-02)] # R=  5.0, ML=7.0, Vs30=760 NM
tmp[0,6,:] = [math.exp(2.279E-01), math.exp(5.201E-01), math.exp(5.755E-02), math.exp(6.203E-03)] # R=  5.0, ML=5.0, Vs30=760 RV Ztor=5.0
tmp[0,7,:] = [math.exp(5.377E-01), math.exp(1.282E+00), math.exp(3.466E-01), math.exp(6.843E-02)] # R=  5.0, ML=7.0, Vs30=760 RV Ztor=5.0
tmp[1,0,:] = [math.exp(2.995E-02), math.exp(6.507E-02), math.exp(1.030E-02), math.exp(1.273E-03)] # R= 20.0, ML=5.0, Vs30=760 SS
tmp[1,1,:] = [math.exp(1.291E-01), math.exp(2.896E-01), math.exp(1.119E-01), math.exp(2.842E-02)] # R= 20.0, ML=7.0, Vs30=760 SS
tmp[1,2,:] = [math.exp(2.995E-02), math.exp(6.711E-02), math.exp(1.115E-02), math.exp(1.379E-03)] # R= 20.0, ML=5.0, Vs30=760 RV
tmp[1,3,:] = [math.exp(1.291E-01), math.exp(2.987E-01), math.exp(1.212E-01), math.exp(3.079E-02)] # R= 20.0, ML=7.0, Vs30=760 RV
tmp[1,4,:] = [math.exp(2.821E-02), math.exp(6.128E-02), math.exp(9.696E-03), math.exp(1.199E-03)] # R= 20.0, ML=5.0, Vs30=760 NM
tmp[1,5,:] = [math.exp(1.216E-01), math.exp(2.727E-01), math.exp(1.054E-01), math.exp(2.677E-02)] # R= 20.0, ML=7.0, Vs30=760 NM
tmp[1,6,:] = [math.exp(4.690E-02), math.exp(1.053E-01), math.exp(1.394E-02), math.exp(1.521E-03)] # R= 20.0, ML=5.0, Vs30=760 RV Ztor=5.0
tmp[1,7,:] = [math.exp(2.013E-01), math.exp(4.685E-01), math.exp(1.515E-01), math.exp(3.035E-02)] # R= 20.0, ML=7.0, Vs30=760 RV Ztor=5.0
tmp[2,0,:] = [math.exp(4.715E-03), math.exp(1.064E-02), math.exp(2.711E-03), math.exp(4.073E-04)] # R=100.0, ML=5.0, Vs30=300 SS
tmp[2,1,:] = [math.exp(4.580E-02), math.exp(1.043E-01), math.exp(6.762E-02), math.exp(2.113E-02)] # R=100.0, ML=7.0, Vs30=300 SS
tmp[2,2,:] = [math.exp(4.715E-03), math.exp(1.098E-02), math.exp(2.936E-03), math.exp(4.413E-04)] # R=100.0, ML=5.0, Vs30=300 RV
tmp[2,3,:] = [math.exp(4.580E-02), math.exp(1.075E-01), math.exp(7.325E-02), math.exp(2.289E-02)] # R=100.0, ML=7.0, Vs30=300 RV
tmp[2,4,:] = [math.exp(4.441E-03), math.exp(1.003E-02), math.exp(2.553E-03), math.exp(3.836E-04)] # R=100.0, ML=5.0, Vs30=300 NM
tmp[2,5,:] = [math.exp(4.323E-02), math.exp(9.850E-02), math.exp(6.372E-02), math.exp(1.990E-02)] # R=100.0, ML=7.0, Vs30=300 NM
tmp[2,6,:] = [math.exp(7.377E-03), math.exp(1.716E-02), math.exp(3.668E-03), math.exp(4.870E-04)] # R=100.0, ML=5.0, Vs30=300 RV Ztor=5.0
tmp[2,7,:] = [math.exp(7.030E-02), math.exp(1.634E-01), math.exp(9.101E-02), math.exp(2.256E-02)] # R=100.0, ML=7.0, Vs30=300 RV Ztor=5.0
test_data['Abrahamson08_test_mean'] = tmp
del tmp

# sigma values
tmp = zeros((3,8,4))		# num_sites, num_events, num_periods
# period:     0.01       0.20       1.00       3.00
tmp[0,0,:] = [7.171E-01, 8.169E-01, 7.207E-01, 6.851E-01] # R=  5.0, ML=5.0, Vs30=760 SS
tmp[0,1,:] = [5.486E-01, 6.103E-01, 6.477E-01, 6.646E-01] # R=  5.0, ML=7.0, Vs30=760 SS
tmp[0,2,:] = [7.171E-01, 8.169E-01, 7.207E-01, 6.851E-01] # R=  5.0, ML=5.0, Vs30=760 RV
tmp[0,3,:] = [5.486E-01, 6.103E-01, 6.477E-01, 6.646E-01] # R=  5.0, ML=7.0, Vs30=760 RV
tmp[0,4,:] = [7.175E-01, 8.169E-01, 7.207E-01, 6.851E-01] # R=  5.0, ML=5.0, Vs30=760 NM
tmp[0,5,:] = [5.490E-01, 6.103E-01, 6.477E-01, 6.646E-01] # R=  5.0, ML=7.0, Vs30=760 NM
tmp[0,6,:] = [7.139E-01, 8.169E-01, 7.207E-01, 6.851E-01] # R=  5.0, ML=5.0, Vs30=760 RV Ztor=5.0
tmp[0,7,:] = [5.456E-01, 6.103E-01, 6.477E-01, 6.646E-01] # R=  5.0, ML=7.0, Vs30=760 RV Ztor=5.0
tmp[1,0,:] = [7.226E-01, 8.169E-01, 7.207E-01, 6.851E-01] # R= 20.0, ML=5.0, Vs30=760 SS
tmp[1,1,:] = [5.536E-01, 6.103E-01, 6.477E-01, 6.646E-01] # R= 20.0, ML=7.0, Vs30=760 SS
tmp[1,2,:] = [7.226E-01, 8.169E-01, 7.207E-01, 6.851E-01] # R= 20.0, ML=5.0, Vs30=760 RV
tmp[1,3,:] = [5.536E-01, 6.103E-01, 6.477E-01, 6.646E-01] # R= 20.0, ML=7.0, Vs30=760 RV
tmp[1,4,:] = [7.227E-01, 8.169E-01, 7.207E-01, 6.851E-01] # R= 20.0, ML=5.0, Vs30=760 NM
tmp[1,5,:] = [5.538E-01, 6.103E-01, 6.477E-01, 6.646E-01] # R= 20.0, ML=7.0, Vs30=760 NM
tmp[1,6,:] = [7.217E-01, 8.169E-01, 7.207E-01, 6.851E-01] # R= 20.0, ML=5.0, Vs30=760 RV Ztor=5.0
tmp[1,7,:] = [5.517E-01, 6.103E-01, 6.477E-01, 6.646E-01] # R= 20.0, ML=7.0, Vs30=760 RV Ztor=5.0
tmp[2,0,:] = [7.217E-01, 8.136E-01, 7.203E-01, 6.851E-01] # R=100.0, ML=5.0, Vs30=760 SS
tmp[2,1,:] = [5.423E-01, 5.905E-01, 6.450E-01, 6.646E-01] # R=100.0, ML=7.0, Vs30=760 SS
tmp[2,2,:] = [7.217E-01, 8.136E-01, 7.203E-01, 6.851E-01] # R=100.0, ML=5.0, Vs30=760 RV
tmp[2,3,:] = [5.423E-01, 5.905E-01, 6.450E-01, 6.646E-01] # R=100.0, ML=7.0, Vs30=760 RV
tmp[2,4,:] = [7.218E-01, 8.138E-01, 7.203E-01, 6.851E-01] # R=100.0, ML=5.0, Vs30=760 NM
tmp[2,5,:] = [5.432E-01, 5.916E-01, 6.452E-01, 6.646E-01] # R=100.0, ML=7.0, Vs30=760 NM
tmp[2,6,:] = [7.202E-01, 8.118E-01, 7.201E-01, 6.851E-01] # R=100.0, ML=5.0, Vs30=760 RV Ztor=5.0
tmp[2,7,:] = [5.345E-01, 5.803E-01, 6.436E-01, 6.646E-01] # R=100.0, ML=7.0, Vs30=760 RV Ztor=5.0
test_data['Abrahamson08_test_sigma'] = tmp
del tmp

################################################################################
################################################################################
 #Akkar_2010_crustal Tests - data values from Matlab Code
 #num_periods = 4
test_data['Akkar_2010_crustal_test_period'] = [0.0, 0.2]
test_data['Akkar_2010_crustal_test_magnitude'] = [5.0,7.0]
test_data['Akkar_2010_crustal_test_Vs30'] = array([760])
test_data['Akkar_2010_crustal_test_fault_type'] = [0, 0]
tmp = zeros((1,2))
tmp[0,:] = [   10,    100] # distance - 1st site and all 2 events
test_data['Akkar_2010_crustal_test_distance'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.0958, 0.2080]
tmp[:,1,:] = [0.0413, 0.0959] 

test_data['Akkar_2010_crustal_test_mean'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.6431, 0.6956]
tmp[:,1,:] = [0.6431, 0.6956] 

test_data['Akkar_2010_crustal_test_sigma'] = tmp
del tmp

######################################################################################
################################################################################
 #Zhao_Interface Tests - data values from Matlab Code
 #num_periods = 4
test_data['Zhao_2006_interface_test_period'] = [0.0, 0.2]
test_data['Zhao_2006_interface_test_magnitude'] = [5.0,7.0]
test_data['Zhao_2006_interface_test_Vs30'] = array([500])
test_data['Zhao_2006_interface_test_depth'] = [100, 50]
tmp = zeros((1,2))
tmp[0,:] = [   10,    100] # distance - 1st site and all 2 events
test_data['Zhao_2006_interface_test_distance'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.2689, 0.6858]
tmp[:,1,:] = [0.0733, 0.1940] 

test_data['Zhao_2006_interface_test_mean'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.6780, 0.7658]
tmp[:,1,:] = [0.6780, 0.7658] 

test_data['Zhao_2006_interface_test_sigma'] = tmp
del tmp

######################################################################################
################################################################################
 #Zhao_2006_intraslab Tests - data values from Matlab Code
 #num_periods = 4
test_data['Zhao_2006_intraslab_test_period'] = [0.00, 0.2]
test_data['Zhao_2006_intraslab_test_magnitude'] = [5.0,7.0]
test_data['Zhao_2006_intraslab_test_depth'] = [ 100,100]
test_data['Zhao_2006_intraslab_test_Vs30'] = array([760])

tmp = zeros((1,2))
tmp[0,:] = [   10,    10] # distance - 1st site and all 2 events
test_data['Zhao_2006_intraslab_test_distance'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.9415, 1.4446]
tmp[:,1,:] = [4.4703, 6.6522] 

test_data['Zhao_2006_intraslab_test_mean'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.6840, 0.7641]
tmp[:,1,:] = [0.6840, 0.7641] 

test_data['Zhao_2006_intraslab_test_sigma'] = tmp
del tmp

################################################################################

################################################################################
################################################################################
## #Atkinson_2003_interface Tests - data values from Matlab Code
## #num_periods = 4
test_data['Atkinson_2003_interface_test_period'] = [0.0, 0.2]
test_data['Atkinson_2003_interface_test_magnitude'] = [5.0,7.0]
test_data['Atkinson_2003_interface_test_depth'] = [ 100,10]
test_data['Atkinson_2003_interface_test_Vs30'] = array([760])

tmp = zeros((1,2))
tmp[0,:] = [   10,    100] # distance - 1st site and all 2 events
test_data['Atkinson_2003_interface_test_distance'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.1240, 0.1924]
tmp[:,1,:] = [0.0382, 0.0580] 

test_data['Atkinson_2003_interface_test_mean'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.5256, 0.6488]
tmp[:,1,:] = [0.5256, 0.6488] 

test_data['Atkinson_2003_interface_test_sigma'] = tmp
del tmp

################################################################################
################################################################################
 #Atkinson_2003_intraslab Tests - data values from Matlab Code
 #num_periods = 4
test_data['Atkinson_2003_intraslab_test_period'] = [0.0, 0.2]
test_data['Atkinson_2003_intraslab_test_magnitude'] = [5.0,7.0]
test_data['Atkinson_2003_intraslab_test_depth'] = [ 100,10]
test_data['Atkinson_2003_intraslab_test_Vs30'] = array([300])

tmp = zeros((1,2))
tmp[0,:] = [   10,    100] # distance - 1st site and all 2 events
test_data['Atkinson_2003_intraslab_test_distance'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.5241, 0.5373]
tmp[:,1,:] = [0.0366, 0.1329] 

test_data['Atkinson_2003_intraslab_test_mean'] = tmp
del tmp

tmp = zeros((1,2,2))
tmp[:,0,:] = [0.6200, 0.6414]
tmp[:,1,:] = [0.6200, 0.6414] 

test_data['Atkinson_2003_intraslab_test_sigma'] = tmp
del tmp

################################################################################
class Distance_stub(object):
    """This object is used for simple cases.

    For more complex models, this object is overridden.
    """

    def __init__(self, dist):
        self.dist = asarray(dist)
        self.Rupture = self.dist
        self.Joyner_Boore = self.dist
        self.Horizontal = self.dist

    def distance(self, dummy):
        return self.dist

def mag2dict(mag):
    # when using multiple_g_m_calc the mag_type is determined from
    # the g_m_interface, so it could be ML or Mw.
    mag = asarray(mag)
    return {None: mag,
            'ML': mag,
            'Mw': mag}

def data2atts(model_name):
    """Get attributes for a model from the test_data dictionary.

    The Vs30 value is defaulted to 1000 if not defined in test_data.
    """

    # get params that are provided for every model
    # default Vs30 to 1000.0 if not supplied
    magnitudes = mag2dict(test_data[model_name+'_test_magnitude'])
    test_mean = test_data[model_name+'_test_mean']
    periods = test_data[model_name+'_test_period']
    Vs30 = array(test_data.get(model_name+'_test_Vs30', 1000.0))

    # get distance object, if it exists, else use internal object
    try:
        distances = test_data[model_name+'_test_distance_object']
    except KeyError:
        distances = Distance_stub(test_data[model_name+'_test_distance'])

    # params not there for every model (usually return None if not there)
    depths = test_data.get(model_name+'_test_depth', None)
    depth_to_top = test_data.get(model_name+'_test_depth_to_top', None)
    fault_type = test_data.get(model_name+'_test_fault_type', None)
    dip = test_data.get(model_name+'_test_dip', None)
#    if dip is not None:
#        dip = array(dip)[newaxis,:,newaxis]
    width = test_data.get(model_name+'_test_width', None)
#    if width is not None:
#        width = array(width)[newaxis,:,newaxis]
    Z25 = array(test_data.get(model_name+'_test_Z25', None))
    test_sigma = test_data.get(model_name+'_test_sigma', None)

    return (distances, magnitudes, test_mean, test_sigma, periods, depths, Vs30,
            depth_to_top, fault_type, Z25, dip, width)

def ground_motion_interface_conformance(GM_class, model_name):
    """
    This checks that for the given test_distance and test_magnitudes,
    the calculated ground motion is the same as the test_ground_motion
    """

    (distances, magnitudes, test_mean, test_sigma, periods, depths, Vs30,
     depth_to_top, fault_type, Z25, dip, width) = data2atts(model_name)

    if GM_class is Ground_motion_calculator:
        gm = GM_class(model_name, periods)
        (log_mean, log_sigma) = \
            gm.distribution_function(distances, magnitudes, periods=periods,
                                     depth=depths, Vs30=Vs30,
                                     depth_to_top=depth_to_top,
                                     fault_type=fault_type, Z25=Z25,
                                     dip=dip, width=width)
    elif GM_class is Multiple_ground_motion_calculator:
        model_weights = [1]
        gm = GM_class([model_name], periods, model_weights)
        # ignoring event_activity, event_id
        _, _, log_mean, log_sigma = \
            gm._distribution_function(distances, magnitudes, periods=periods,
                                      depth=depths, Vs30=Vs30,
                                      depth_to_top=depth_to_top,
                                      fault_type=fault_type, Z25=Z25,
                                      dip=dip, width=width)

    return (exp(log_mean), test_mean, log_sigma, test_sigma)


class Test_ground_motion_specification(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def ground_motion_interface_conformance(self, GM_class, model_name):
        (median, test_mean,
         sigma, test_sigma) = ground_motion_interface_conformance(GM_class,
                                                                  model_name)


        msg = 'median=\n%s\ntest_median=\n%s' % (str(median), str(test_mean))
#        msg = 'median diff=\n%s' % str(median-test_mean)
        self.assert_(allclose(median, test_mean, rtol=0.05, atol=1.0e-5),
                     "%s did not pass assert:\n%s" % (model_name, msg))

        if test_sigma is not None:
            msg = 'sigma=\n%s\ntest_sigma=\n%s' % (str(sigma), str(test_sigma))
#            msg = 'sigma diff=\n%s' % str(sigma-test_sigma)
            self.assert_(allclose(sigma, test_sigma, rtol=0.05, atol=1.0e-5),
                         "%s did not pass assert:\n%s" % (model_name, msg))


    def test_all_ground_motion_interfaces(self):
        for name in classes_with_test_data:
            self.ground_motion_interface_conformance(Ground_motion_calculator,
                                                     name)

    def test_all_multi_ground_motion_interfaces(self):
        for name in classes_with_test_data:
            self.ground_motion_interface_conformance(
                                       Multiple_ground_motion_calculator,
                                       name)

    def test_Ground_motion_specification_init_(self):
        model_name = 'Gaull_1990_WA'
        model = Ground_motion_specification(model_name)

        # Comparing against the variables in attenuation_models.py
        # A circular sort of test, since attenuation_models is being used
        #  as a data holder
        imported = gound_motion_init[model_name]
        self.failUnless(model.magnitude_type==imported[1],
                        'Model attributes incorrect.')
        self.failUnless(model.distance_type==imported[2],
                        'Model attributes incorrect.')
        self.assert_(allclose(model.coefficient, imported[3]))
        self.failUnless(model.coefficient_period==imported[4],
                        'Model attributes incorrect.')
        self.assert_(allclose(model.sigma_coefficient, imported[6]))
        self.assert_(allclose(model.sigma_coefficient_period, imported[7]))


#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_ground_motion_specification, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
