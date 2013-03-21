import unittest

from scipy import array, exp, log, allclose, newaxis, asarray, zeros
import math

from eqrm_code.ground_motion_specification import *
from eqrm_code.ground_motion_interface import ground_motion_init, \
     Log102Ln, LnCmss2Lng
from eqrm_code.ground_motion_misc import \
     Australian_standard_model_interpolation
from eqrm_code.ground_motion_calculator import Ground_motion_calculator, \
     Multiple_ground_motion_calculator
from numpy import power

classes_with_test_data = ('Abrahamson08', 
                          'Abrahamson_Silva_1997', 
                          'Akkar_2010_crustal', 
                          'Allen', 
                          'Allen_2012', 
                          'Atkinson06_bc_boundary_bedrock', 
                          'Atkinson06_hard_bedrock', 
                          'Atkinson06_soil', 
                          'Atkinson_2003_interface', 
                          'Atkinson_2003_intraslab', 
                          'Boore_08', 
                          'Campbell03', 
                          'Campbell08', 
                          'Chiou08', 
                          'Combo_Sadigh_Youngs_M8', 
                          'Gaull_1990_WA', 
                          'Liang_2008', 
                          'Sadigh_97', 
                          'Sadigh_Original_97', 
                          'Somerville09_Non_Cratonic', 
                          'Somerville09_Yilgarn', 
                          'Toro_1997_midcontinent', 
                          'Youngs_97_interface', 
                          'Youngs_97_intraslab', 
                          'Zhao_2006_interface', 
                          'Zhao_2006_intraslab')

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

    test_sigma: : the sigma that must be matched by verification tests
                    dimensions (sites, mag, period).
                    NOTE: These values are log sigma which is inconsistent with 
                    test_mean above

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

# ***********************************************************

# Sadigh '97 test data from the OpenSHA test result set
# https://source.usc.edu/svn/opensha/trunk
# \test\org\opensha\sha\imr\attenRelImpl\test\AttenRelResultSetFiles\SADIGH.txt
# SetParameter("Fault Type") = "Other"
# SetParameter("Sadigh Site Type") = "Rock"
#
# test_sigma calculated by hand
#

# Mw
test_data['Sadigh_Original_97_test_magnitude'] =    [6.0, 6.5, 7.0, 7.5]

# Rrup
tmp = zeros((1,4))
tmp[0,:] =                                          [10.0, 10.0, 10.0, 10.0]
test_data['Sadigh_Original_97_test_distance'] = tmp

# period
test_data['Sadigh_Original_97_test_period'] =       [0.0, 0.10, 1]

test_data['Sadigh_Original_97_test_mean'] =       [[[0.223793, 0.450355, 0.117692],
                                                    [0.312275, 0.610350, 0.212184],
                                                    [0.372536, 0.709483, 0.313197],
                                                    [0.447629, 0.805460, 0.423117]]]

test_data['Sadigh_Original_97_test_sigma'] =      [[[0.55, 0.57, 0.69],
                                                    [0.48, 0.50, 0.62],
                                                    [0.41, 0.43, 0.55],
                                                    [0.38, 0.40, 0.52]]]

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

# Boore_08
# test_data['Boore_08_test_period'] = [
#     0.0000E+00,3.0000E-01,1.0000E-00]

# test_data['Boore_08_test_distance'] = [9,14,21.0]

# test_data['Boore_08_test_mean'] = array([
#     [8.0160e-002,1.2333e-001,2.8450e-002],
#     [5.9491e-002,9.4516e-002,2.0631e-002],
#     [4.3928e-002,7.2391e-002,1.5113e-002]])
# test_data['Boore_08_test_mean'] = \
#                                   test_data['Boore_08_test_mean'] \
#                                   [:,newaxis,:]
# test_data['Boore_08_test_magnitude'] = [5.4]

# test_data['Boore_08_test_Vs30'] = 1000.0

# Boore_08
test_data['Boore_08_test_period'] = [0.01, 0.2, 1.0]

test_data['Boore_08_test_distance'] = [5, 10, 25]

test_data['Boore_08_test_mean'] = array([
    [exp(-3.179415), exp(-2.798686), exp(-5.031195)],
    [exp(-3.717279), exp(-3.230695), exp(-5.576974)],
    [exp(-4.545958), exp(-3.916533), exp(-6.400938)]     ]) #, -0.169129]])
test_data['Boore_08_test_mean'] = \
                                  test_data['Boore_08_test_mean'] \
                                  [:,newaxis,:]
test_data['Boore_08_test_magnitude'] = [4]

test_data['Boore_08_test_Vs30'] = 600.0

test_data['Boore_08_test_fault_type'] = array([2])


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
#test_data['Atkinson06_soil_test_Vs30'] = [1000.0, 1000.0, 1000.0]
test_data['Atkinson06_soil_test_Vs30'] = [1000.0]

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

################################################################################
# Chiou08 Tests - Rock - compare code against 'hand' code results

# Vs30 value
# num_sites = 3
test_data['Chiou08_test_Vs30'] = [520.0, 520.0, 520.0]

# num_events = 2
test_data['Chiou08_test_magnitude'] = [5.5, 7.5]

# num_events = 2
test_data['Chiou08_test_depth_to_top'] = [0.0, 0.0]

# num_events = 2
# 'reverse' fault type index is 0
test_data['Chiou08_test_fault_type'] = [0, 0]

# num_periods = 4
test_data['Chiou08_test_period'] = [0.01, 0.20, 1.00, 3.00]

# num_events = 2
test_data['Chiou08_test_dip'] = [90.0, 90.0]

# num_sites = 3
tmp = zeros((3,2)) # initialise an array: (num_sites, num_events)
tmp[0,:] = [  5.0,   5.0] # distance - 1st site and all 2 events
tmp[1,:] = [ 20.0,  20.0] # distance - 2nd site and all 2 events
tmp[2,:] = [100.0, 100.0] # distance - 3rd site and all 2 events
test_data['Chiou08_test_distance'] = tmp

# result values, in 'g'
tmp = zeros((3,2,4))		# num_sites, num_events, num_periods
# period:     0.01      0.20      1.00      3.00
tmp[0,0,:] = [0.276160, 0.612666, 0.139772, 0.017631] # R=  5.0, ML=5.5
tmp[0,1,:] = [0.525535, 1.230800, 0.503488, 0.112815] # R=  5.0, ML=7.5
tmp[1,0,:] = [0.068560, 0.150721, 0.032357, 0.004130] # R= 20.0, ML=5.5
tmp[1,1,:] = [0.242421, 0.585651, 0.206465, 0.046410] # R= 20.0, ML=7.5
tmp[2,0,:] = [0.006308, 0.013925, 0.004896, 0.000717] # R=100.0, ML=5.5
tmp[2,1,:] = [0.052239, 0.117515, 0.055062, 0.013557] # R=100.0, ML=7.5
test_data['Chiou08_test_mean'] = tmp
del tmp

################################################################################
## Chiou08 Tests - Soil - compare code against BooreFTN code results
#
## num_periods = 3
#test_data['Chiou08_test_period'] = [0.01, 1.0, 3.0]
#
## num_events = 3
#test_data['Chiou08_test_magnitude'] = [4.0, 5.5, 7.0]
#
## num_sites = 3
#tmp = zeros((3,3)) # initialize an array: (num_sites, num_events)
#tmp[0,:] = [  5.0,   5.0,   5.0] # distance - site 1 & all 3 events
#tmp[1,:] = [ 25.0,  25.0,  25.0] # distance - site 2 & all 3 events
#tmp[2,:] = [100.0, 100.0, 100.0] # distance - site 3 & all 3 events
#test_data['Chiou08_test_distance'] = tmp
#
## num_events = 3
#test_data['Chiou08_test_depth_to_top'] = [0.0, 0.0, 0.0]
#
## num_events = 3
#test_data['Chiou08_test_dip'] = [90.0, 90.0, 90.0]
#
## num_sites = 3
#test_data['Chiou08_test_Vs30'] = [300.0, 300.0, 300.0]
#
## num_events = 3
## 'reverse' fault type index is 0
## 'normal' fault type index is 1
## 'strike_slip' fault type index is 2
##                                       SS SS SS
#test_data['Chiou08_test_fault_type'] = [2, 2, 2]
#
## mean values, in 'g'
#tmp = zeros((3,3,3))    # (num_sites, num_events, num_periods)
#tmp[0,0,0] = 5.581E-02 # Rrup=  5.0, Mw=4.0, T=0.01
#tmp[1,0,0] = 6.411E-03 # Rrup= 25.0, Mw=4.0, T=0.01
#tmp[2,0,0] = 4.692E-04 # Rrup=100.0, Mw=4.0, T=0.01
#tmp[0,1,0] = 2.679E-01 # Rrup=  5.0, Mw=5.5, T=0.01
#tmp[1,1,0] = 5.575E-02 # Rrup= 25.0, Mw=5.5, T=0.01
#tmp[2,1,0] = 7.231E-03 # Rrup=100.0, Mw=5.5, T=0.01
#tmp[0,2,0] = 4.268E-01 # Rrup=  5.0, Mw=7.0, T=0.01
#tmp[1,2,0] = 1.565E-01 # Rrup= 25.0, Mw=7.0, T=0.01
#tmp[2,2,0] = 3.701E-02 # Rrup=100.0, Mw=7.0, T=0.01
#tmp[0,0,1] = 9.876E-03 # Rrup=  5.0, Mw=4.0, T=1.00
#tmp[1,0,1] = 1.182E-03 # Rrup= 25.0, Mw=4.0, T=1.00
#tmp[2,0,1] = 1.864E-04 # Rrup=100.0, Mw=4.0, T=1.00
#tmp[0,1,1] = 1.861E-01 # Rrup=  5.0, Mw=5.5, T=1.00
#tmp[1,1,1] = 3.414E-02 # Rrup= 25.0, Mw=5.5, T=1.00
#tmp[2,1,1] = 7.010E-03 # Rrup=100.0, Mw=5.5, T=1.00
#tmp[0,2,1] = 5.130E-01 # Rrup=  5.0, Mw=7.0, T=1.00
#tmp[1,2,1] = 1.588E-01 # Rrup= 25.0, Mw=7.0, T=1.00
#tmp[2,2,1] = 4.728E-02 # Rrup=100.0, Mw=7.0, T=1.00
#tmp[0,0,2] = 8.548E-04 # Rrup=  5.0, Mw=4.0, T=3.00
#tmp[1,0,2] = 1.064E-04 # Rrup= 25.0, Mw=4.0, T=3.00
#tmp[2,0,2] = 2.024E-05 # Rrup=100.0, Mw=4.0, T=3.00
#tmp[0,1,2] = 3.169E-02 # Rrup=  5.0, Mw=5.5, T=3.00
#tmp[1,1,2] = 5.605E-03 # Rrup= 25.0, Mw=5.5, T=3.00
#tmp[2,1,2] = 1.293E-03 # Rrup=100.0, Mw=5.5, T=3.00
#tmp[0,2,2] = 1.561E-01 # Rrup=  5.0, Mw=7.0, T=3.00
#tmp[1,2,2] = 4.511E-02 # Rrup= 25.0, Mw=7.0, T=3.00
#tmp[2,2,2] = 1.415E-02 # Rrup=100.0, Mw=7.0, T=3.00
#test_data['Chiou08_test_mean'] = tmp
#
## sigma values, in 'g'
#tmp = zeros((3,3,3))    # (num_sites, num_events, num_periods)
#tmp[0,0,0] = 6.508E-01 # Rrup=  5.0, Mw=4.0, T=0.01
#tmp[1,0,0] = 6.718E-01 # Rrup= 25.0, Mw=4.0, T=0.01
#tmp[2,0,0] = 6.750E-01 # Rrup=100.0, Mw=4.0, T=0.01
#tmp[0,1,0] = 5.770E-01 # Rrup=  5.0, Mw=5.5, T=0.01
#tmp[1,1,0] = 6.140E-01 # Rrup= 25.0, Mw=5.5, T=0.01
#tmp[2,1,0] = 6.334E-01 # Rrup=100.0, Mw=5.5, T=0.01
#tmp[0,2,0] = 4.649E-01 # Rrup=  5.0, Mw=7.0, T=0.01
#tmp[1,2,0] = 4.844E-01 # Rrup= 25.0, Mw=7.0, T=0.01
#tmp[2,2,0] = 5.090E-01 # Rrup=100.0, Mw=7.0, T=0.01
#tmp[0,0,1] = 6.931E-01 # Rrup=  5.0, Mw=4.0, T=1.00
#tmp[1,0,1] = 6.958E-01 # Rrup= 25.0, Mw=4.0, T=1.00
#tmp[2,0,1] = 6.961E-01 # Rrup=100.0, Mw=4.0, T=1.00
#tmp[0,1,1] = 6.539E-01 # Rrup=  5.0, Mw=5.5, T=1.00
#tmp[1,1,1] = 6.744E-01 # Rrup= 25.0, Mw=5.5, T=1.00
#tmp[2,1,1] = 6.817E-01 # Rrup=100.0, Mw=5.5, T=1.00
#tmp[0,2,1] = 6.063E-01 # Rrup=  5.0, Mw=7.0, T=1.00
#tmp[1,2,1] = 6.206E-01 # Rrup= 25.0, Mw=7.0, T=1.00
#tmp[2,2,1] = 6.353E-01 # Rrup=100.0, Mw=7.0, T=1.00
#tmp[0,0,2] = 7.266E-01 # Rrup=  5.0, Mw=4.0, T=3.00
#tmp[1,0,2] = 7.268E-01 # Rrup= 25.0, Mw=4.0, T=3.00
#tmp[2,0,2] = 7.268E-01 # Rrup=100.0, Mw=4.0, T=3.00
#tmp[0,1,2] = 7.181E-01 # Rrup=  5.0, Mw=5.5, T=3.00
#tmp[1,1,2] = 7.202E-01 # Rrup= 25.0, Mw=5.5, T=3.00
#tmp[2,1,2] = 7.209E-01 # Rrup=100.0, Mw=5.5, T=3.00
#tmp[0,2,2] = 6.992E-01 # Rrup=  5.0, Mw=7.0, T=3.00
#tmp[1,2,2] = 7.007E-01 # Rrup= 25.0, Mw=7.0, T=3.00
#tmp[2,2,2] = 7.024E-01 # Rrup=100.0, Mw=7.0, T=3.00
#test_data['Chiou08_test_sigma'] = tmp
#
#
#del tmp

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
# Campbell08 Tests - test against data values from the Boore FORTRAN.

class Campbell08_distance_object(object):
    def __init__(self, Rrup, Rjb):
        self.Rupture = Rrup
        self.Joyner_Boore = Rjb

    def distance(self, type):
        if type == 'Rupture':
            return self.Rupture
        else:
            return self.Joyner_Boore

# Rjb distances - num_sites = 7
tmp = zeros((7,4)) # initialise an array: (num_sites, num_events)
tmp[0,:] = [  5.0,   5.0,   5.0,   5.0] # Rrup - 1st site and all 4 events
tmp[1,:] = [ 10.0,  10.0,  10.0,  10.0] # Rrup - 2nd site and all 4 events
tmp[2,:] = [ 15.0,  15.0,  15.0,  15.0] # Rrup - 3rd site and all 4 events
tmp[3,:] = [ 30.0,  30.0,  30.0,  30.0] # Rrup - 4th site and all 4 events
tmp[4,:] = [ 50.0,  50.0,  50.0,  50.0] # Rrup - 5th site and all 4 events
tmp[5,:] = [100.0, 100.0, 100.0, 100.0] # Rrup - 6th site and all 4 events
tmp[6,:] = [200.0, 200.0, 200.0, 200.0] # Rrup - 7th site and all 4 events
Campbell08_Rjb = tmp
del tmp

# Rrup distances - num_sites = 7 - values from check code
tmp = zeros((7,4)) # initialise an array: (num_sites, num_events)
tmp[0,:] = [  5.0,  17.1,   5.0,  17.1] # Rjb - 1st site and all 4 events
tmp[1,:] = [ 10.0,  20.6,  10.0,  20.6] # Rjb - 2nd site and all 4 events
tmp[2,:] = [ 15.0,  24.1,  15.0,  24.1] # Rjb - 3rd site and all 4 events
tmp[3,:] = [ 30.0,  35.6,  30.0,  35.6] # Rjb - 4th site and all 4 events
tmp[4,:] = [ 50.0,  53.5,  50.0,  53.5] # Rjb - 5th site and all 4 events
tmp[5,:] = [100.0, 101.8, 100.0, 101.8] # Rjb - 6th site and all 4 events
tmp[6,:] = [200.0, 200.9, 200.0, 200.9] # Rjb - 7th site and all 4 events
Campbell08_Rrup = tmp
del tmp

# test distance object
test_data['Campbell08_test_distance_object'] = \
        Campbell08_distance_object(Campbell08_Rrup, Campbell08_Rjb)

# num_events = 4
test_data['Campbell08_test_dip'] = [90.0, 45.0, 90.0, 45.0]

# num_events = 4
test_data['Campbell08_test_depth_to_top'] = [0.0, 5.0, 0.0, 5.0]

# num_events = 4
test_data['Campbell08_test_magnitude'] = [5.0, 5.0, 7.0, 7.0]

# num_events = 4
# 'strike_slip' fault type index is 2, 'reverse' is 0
test_data['Campbell08_test_fault_type'] = [0, 2, 0, 2]

# num_periods = 4
test_data['Campbell08_test_period'] = [0.01, 0.20, 1.00, 3.00]

# Z25 override - num_sites = 7
test_data['Campbell08_test_Z25'] = [0.640]	# km

# Vs30 override - num_sites = 7
test_data['Campbell08_test_Vs30'] = [760.0, 760.0, 760.0, 760.0, 760.0,
                                     760.0, 760.0]

# result values, in 'g' - from 'check' code
tmp = zeros((7,4,4))		# num_sites, num_events, num_periods
# period:     0.01         0.20         1.00         3.00
tmp[0,0,:] = [1.72717E-01, 3.56477E-01, 4.56106E-02, 4.86561E-03] # R=  5.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[0,1,:] = [5.76729E-02, 1.32968E-01, 1.43209E-02, 1.52771E-03] # R=  5.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[0,2,:] = [3.63924E-01, 8.61762E-01, 2.51753E-01, 6.74238E-02] # R=  5.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[0,3,:] = [2.12307E-01, 5.32415E-01, 1.44370E-01, 3.23540E-02] # R=  5.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[1,0,:] = [1.01596E-01, 2.29145E-01, 2.50815E-02, 2.67562E-03] # R= 10.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[1,1,:] = [4.63737E-02, 1.06564E-01, 1.16432E-02, 1.24206E-03] # R= 10.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[1,2,:] = [2.47801E-01, 6.18154E-01, 1.65214E-01, 4.42472E-02] # R= 10.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[1,3,:] = [1.69086E-01, 4.20015E-01, 1.16266E-01, 2.73501E-02] # R= 10.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[2,0,:] = [6.66910E-02, 1.53644E-01, 1.64724E-02, 1.75723E-03] # R= 15.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[2,1,:] = [3.84208E-02, 8.77455E-02, 9.76028E-03, 1.04120E-03] # R= 15.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[2,2,:] = [1.82617E-01, 4.57704E-01, 1.22867E-01, 3.29059E-02] # R= 15.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[2,3,:] = [1.40405E-01, 3.45231E-01, 9.76740E-02, 2.37779E-02] # R= 15.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[3,0,:] = [2.95311E-02, 6.66158E-02, 7.64411E-03, 8.15451E-04] # R= 30.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[3,1,:] = [2.39413E-02, 5.33585E-02, 6.29940E-03, 6.72001E-04] # R= 30.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[3,2,:] = [1.01034E-01, 2.44184E-01, 7.15458E-02, 1.91612E-02] # R= 30.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[3,3,:] = [9.18350E-02, 2.18936E-01, 6.61387E-02, 1.70260E-02] # R= 30.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[4,0,:] = [1.56861E-02, 3.39902E-02, 4.27571E-03, 4.56120E-04] # R= 50.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[4,1,:] = [1.43994E-02, 3.10117E-02, 3.95418E-03, 4.21820E-04] # R= 50.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[4,2,:] = [6.37340E-02, 1.47237E-01, 4.75187E-02, 1.27263E-02] # R= 50.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[4,3,:] = [6.13436E-02, 1.40806E-01, 4.60787E-02, 1.21368E-02] # R= 50.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[5,0,:] = [6.55753E-03, 1.33053E-02, 1.93205E-03, 2.06105E-04] # R=100.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[5,1,:] = [6.41014E-03, 1.29831E-02, 1.89254E-03, 2.01891E-04] # R=100.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[5,2,:] = [3.37322E-02, 7.27406E-02, 2.71563E-02, 7.27294E-03] # R=100.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[5,3,:] = [3.33944E-02, 7.18819E-02, 2.69400E-02, 7.18264E-03] # R=100.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[6,0,:] = [2.72793E-03, 5.16295E-03, 8.71230E-04, 9.29402E-05] # R=200.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[6,1,:] = [2.71222E-03, 5.13084E-03, 8.66675E-04, 9.24544E-05] # R=200.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[6,2,:] = [1.77740E-02, 3.57011E-02, 1.54970E-02, 4.15037E-03] # R=200.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[6,3,:] = [1.77287E-02, 3.55935E-02, 1.54657E-02, 4.13725E-03] # R=200.0, ML=7.0, dip=45, Ztor=5.0, type=RV

test_data['Campbell08_test_mean'] = tmp
del tmp

# sigma values, in ln('g') - from 'check' code
tmp = zeros((7,4,4))		# num_sites, num_events, num_periods
# period:     0.01         0.20         1.00         3.00
tmp[0,0,:] = [5.22221E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=  5.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[0,1,:] = [5.24460E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=  5.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[0,2,:] = [5.19428E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=  5.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[0,3,:] = [5.21556E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=  5.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[1,0,:] = [5.23547E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 10.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[1,1,:] = [5.24708E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 10.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[1,2,:] = [5.21002E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 10.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[1,3,:] = [5.22284E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 10.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[2,0,:] = [5.24267E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 15.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[2,1,:] = [5.24885E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 15.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[2,2,:] = [5.22050E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 15.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[2,3,:] = [5.22801E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 15.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[3,0,:] = [5.25086E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 30.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[3,1,:] = [5.25215E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 30.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[3,2,:] = [5.23558E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 30.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[3,3,:] = [5.23744E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 30.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[4,0,:] = [5.25407E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 50.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[4,1,:] = [5.25437E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 50.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[4,2,:] = [5.24330E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 50.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[4,3,:] = [5.24381E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R= 50.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[5,0,:] = [5.25623E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=100.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[5,1,:] = [5.25626E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=100.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[5,2,:] = [5.24991E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=100.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[5,3,:] = [5.24998E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=100.0, ML=7.0, dip=45, Ztor=5.0, type=RV
tmp[6,0,:] = [5.25715E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=200.0, ML=5.0, dip=90, Ztor=0.0, type=SS
tmp[6,1,:] = [5.25715E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=200.0, ML=5.0, dip=45, Ztor=5.0, type=RV
tmp[6,2,:] = [5.25358E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=200.0, ML=7.0, dip=90, Ztor=0.0, type=SS
tmp[6,3,:] = [5.25359E-01, 5.89200E-01, 6.22615E-01, 6.46251E-01] # R=200.0, ML=7.0, dip=45, Ztor=5.0, type=RV

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
# 'strike_slip' fault type index is 2
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
# period:     0.01       0.20       1.00       3.00
tmp[0,0,:] = [1.462E-01, 3.215E-01, 4.251E-02, 5.188E-03] # R=  5.0, ML=5.0, Vs30=760 SS
tmp[0,1,:] = [3.470E-01, 7.928E-01, 2.560E-01, 6.410E-02] # R=  5.0, ML=7.0, Vs30=760 SS
tmp[0,2,:] = [1.462E-01, 3.316E-01, 4.605E-02, 5.621E-03] # R=  5.0, ML=5.0, Vs30=760 RV
tmp[0,3,:] = [3.470E-01, 8.177E-01, 2.773E-01, 6.944E-02] # R=  5.0, ML=7.0, Vs30=760 RV
tmp[0,4,:] = [1.378E-01, 3.028E-01, 4.003E-02, 4.886E-03] # R=  5.0, ML=5.0, Vs30=760 NM
tmp[0,5,:] = [3.272E-01, 7.467E-01, 2.411E-01, 6.036E-02] # R=  5.0, ML=7.0, Vs30=760 NM
tmp[0,6,:] = [2.279E-01, 5.201E-01, 5.755E-02, 6.203E-03] # R=  5.0, ML=5.0, Vs30=760 RV Ztor=5.0
tmp[0,7,:] = [5.377E-01, 1.282E+00, 3.466E-01, 6.843E-02] # R=  5.0, ML=7.0, Vs30=760 RV Ztor=5.0
tmp[1,0,:] = [2.995E-02, 6.507E-02, 1.030E-02, 1.273E-03] # R= 20.0, ML=5.0, Vs30=760 SS
tmp[1,1,:] = [1.291E-01, 2.896E-01, 1.119E-01, 2.842E-02] # R= 20.0, ML=7.0, Vs30=760 SS
tmp[1,2,:] = [2.995E-02, 6.711E-02, 1.115E-02, 1.379E-03] # R= 20.0, ML=5.0, Vs30=760 RV
tmp[1,3,:] = [1.291E-01, 2.987E-01, 1.212E-01, 3.079E-02] # R= 20.0, ML=7.0, Vs30=760 RV
tmp[1,4,:] = [2.821E-02, 6.128E-02, 9.696E-03, 1.199E-03] # R= 20.0, ML=5.0, Vs30=760 NM
tmp[1,5,:] = [1.216E-01, 2.727E-01, 1.054E-01, 2.677E-02] # R= 20.0, ML=7.0, Vs30=760 NM
tmp[1,6,:] = [4.690E-02, 1.053E-01, 1.394E-02, 1.521E-03] # R= 20.0, ML=5.0, Vs30=760 RV Ztor=5.0
tmp[1,7,:] = [2.013E-01, 4.685E-01, 1.515E-01, 3.035E-02] # R= 20.0, ML=7.0, Vs30=760 RV Ztor=5.0
tmp[2,0,:] = [4.715E-03, 1.064E-02, 2.711E-03, 4.073E-04] # R=100.0, ML=5.0, Vs30=300 SS
tmp[2,1,:] = [4.580E-02, 1.043E-01, 6.762E-02, 2.113E-02] # R=100.0, ML=7.0, Vs30=300 SS
tmp[2,2,:] = [4.715E-03, 1.098E-02, 2.936E-03, 4.413E-04] # R=100.0, ML=5.0, Vs30=300 RV
tmp[2,3,:] = [4.580E-02, 1.075E-01, 7.325E-02, 2.289E-02] # R=100.0, ML=7.0, Vs30=300 RV
tmp[2,4,:] = [4.441E-03, 1.003E-02, 2.553E-03, 3.836E-04] # R=100.0, ML=5.0, Vs30=300 NM
tmp[2,5,:] = [4.323E-02, 9.850E-02, 6.372E-02, 1.990E-02] # R=100.0, ML=7.0, Vs30=300 NM
tmp[2,6,:] = [7.377E-03, 1.716E-02, 3.668E-03, 4.870E-04] # R=100.0, ML=5.0, Vs30=300 RV Ztor=5.0
tmp[2,7,:] = [7.030E-02, 1.634E-01, 9.101E-02, 2.256E-02] # R=100.0, ML=7.0, Vs30=300 RV Ztor=5.0
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
test_data['Atkinson_2003_interface_test_period'] = array([0.0, 0.2])
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
test_data['Atkinson_2003_intraslab_test_period'] = array([0.0, 0.2])
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
#---------
test_data['Abrahamson_Silva_1997_test_magnitude']  = test_data['Abrahamson08_test_magnitude'] 
test_data['Abrahamson_Silva_1997_test_dip']  = test_data['Abrahamson08_test_dip'] 
test_data['Abrahamson_Silva_1997_test_width']  = test_data['Abrahamson08_test_width'] 
test_data['Abrahamson_Silva_1997_test_depth_to_top']  = test_data['Abrahamson08_test_depth_to_top'] 
test_data['Abrahamson_Silva_1997_test_fault_type']  = test_data['Abrahamson08_test_fault_type'] 
test_data['Abrahamson_Silva_1997_test_period']  = test_data['Abrahamson08_test_period'] 
test_data['Abrahamson_Silva_1997_test_Vs30']  = test_data['Abrahamson08_test_Vs30'] 
test_data['Abrahamson_Silva_1997_test_distance']  = test_data['Abrahamson08_test_distance'] 
test_data['Abrahamson_Silva_1997_test_mean']  = [
 [[  2.10186127e-01,  4.33934068e-01,  5.72372135e-02,  6.32623876e-03],
  [  6.57728743e-01,  1.53262356e+00,  4.37270970e-01,  9.35135830e-02],
  [  2.85143755e-01,  5.88685806e-01,  7.31274839e-02,  7.72688548e-03],
  [  7.49040161e-01,  1.74539521e+00,  4.40122489e-01,  8.64967376e-02],
  [  1.54933107e-01,  3.19862944e-01,  4.47998268e-02,  5.17948623e-03],
  [  5.77548604e-01,  1.34578975e+00,  4.34437926e-01,  1.01099653e-01],
  [  2.85143755e-01,  5.88685806e-01,  7.31274839e-02,  7.72688548e-03],
  [  7.49040161e-01,  1.74539521e+00,  4.40122489e-01,  8.64967376e-02]],

 [[  5.14527643e-02,  1.03240496e-01,  1.59912008e-02,  1.98812196e-03],
  [  2.27566954e-01,  5.23072386e-01,  1.82766337e-01,  4.42239964e-02],
  [  6.98021065e-02,  1.40058638e-01,  2.04306989e-02,  2.42829764e-03],
  [  2.59159707e-01,  5.95689680e-01,  1.83958188e-01,  4.09056234e-02],
  [  3.79270352e-02,  7.61009829e-02,  1.25163854e-02,  1.62773659e-03],
  [  1.99825503e-01,  4.59307473e-01,  1.81582209e-01,  4.78115645e-02],
  [  6.98021065e-02,  1.40058638e-01,  2.04306989e-02,  2.42829764e-03],
  [  2.59159707e-01,  5.95689680e-01,  1.83958188e-01,  4.09056234e-02]],

 [[  8.27661887e-03,  1.69613378e-02,  4.39371181e-03,  6.98752384e-04],
  [  5.28817586e-02,  1.10433924e-01,  8.63203019e-02,  2.71875990e-02],
  [  1.10833261e-02,  2.24639912e-02,  5.61349985e-03,  8.53564233e-04],
  [  5.91335877e-02,  1.22641347e-01,  8.68832113e-02,  2.51205683e-02],
  [  6.16263663e-03,  1.27468722e-02,  3.43897817e-03,  5.72031655e-04],
  [  4.72466549e-02,  9.93706999e-02,  8.57610395e-02,  2.94263494e-02],
  [  1.10833261e-02,  2.24639912e-02,  5.61349985e-03,  8.53564233e-04],
  [  5.91335877e-02,  1.22641347e-01,  8.68832113e-02,  2.51205683e-02]]]



test_data['Abrahamson_Silva_1997_test_sigma']  = [[
  [ 0.7,   0.77,  0.83,  0.87 ],
  [ 0.43,  0.5,   0.594,  0.676],
  [ 0.7,   0.77,  0.83,  0.87 ],
  [ 0.43,  0.5,   0.594,  0.676],
  [ 0.7,   0.77,  0.83,  0.87 ],
  [ 0.43,  0.5,   0.594,  0.676],
  [ 0.7,   0.77,  0.83,  0.87 ],
  [ 0.43,  0.5,   0.594,  0.676]]]


#------

#***************  ALLEN 2012 MODEL  ***********************

# Test data from All12.unit_test_data.txt
# FORMAT: PERIOD (SEC) LOG10 PSA (CM/S/S)


# 1) MW = 4.5; Rrup = 20; h = 7
test_data['Allen_2012_test_accel1'] = array([[0.0100,	1.2021],
                                             [0.0200,	1.3351],
                                             [0.0300,	1.4107],
                                             [0.0500,	1.4663],
                                             [0.0750,	1.4849],
                                             [0.1000,	1.4796],
                                             [0.1500,	1.4363],
                                             [0.2000,	1.3712],
                                             [0.2500,	1.3004],
                                             [0.3000,	1.2253],
                                             [0.4000,	1.0533],
                                             [0.5000,	0.8847],
                                             [0.7500,	0.5156],
                                             [1.0000,	0.2298],
                                             [1.5000,	-0.1924],
                                             [2.0000,	-0.4887],
                                             [3.0000,	-0.8921],
                                             [4.0000,	-1.1672]]).T


# 2) MW = 4.5; Rrup = 20; h = 14
test_data['Allen_2012_test_accel2'] = array([[0.0100,	1.2642],
                                              [0.0200,	1.4099],
                                              [0.0300,	1.5013],
                                              [0.0500,	1.5754],
                                              [0.0750,	1.5851],
                                              [0.1000,	1.5631],
                                              [0.1500,	1.4912],
                                              [0.2000,	1.3976],
                                              [0.2500,	1.2981],
                                              [0.3000,	1.1984],
                                              [0.4000,	0.9912],
                                              [0.5000,	0.8003],
                                              [0.7500,	0.3989],
                                              [1.0000,	0.0951],
                                              [1.5000,	-0.3380],
                                              [2.0000,	-0.6326],
                                              [3.0000,	-1.0265],
                                              [4.0000,	-1.2938]]).T


# 3) MW = 4.5; Rrup = 50; h = 7
test_data['Allen_2012_test_accel3'] = array([[0.0100,	0.5040],
                                              [0.0200,	0.6449],
                                              [0.0300,	0.7043],
                                              [0.0500,	0.7657],
                                              [0.0750,	0.7967],
                                              [0.1000,	0.8042],
                                              [0.1500,	0.7879],
                                              [0.2000,	0.7428],
                                              [0.2500,	0.6854],
                                              [0.3000,	0.6199],
                                              [0.4000,	0.4598],
                                              [0.5000,	0.2983],
                                              [0.7500,	-0.0624],
                                              [1.0000,	-0.3455],
                                              [1.5000,	-0.7717],
                                              [2.0000,	-1.0747],
                                              [3.0000,	-1.4856],
                                              [4.0000,	-1.7663]]).T


# 4) MW = 4.5; Rrup = 50; h = 14
test_data['Allen_2012_test_accel4'] = array([[0.0100,	0.5336],
                                              [0.0200,	0.6725],
                                              [0.0300,	0.7552],
                                              [0.0500,	0.8400],
                                              [0.0750,	0.8677],
                                              [0.1000,	0.8615],
                                              [0.1500,	0.8149],
                                              [0.2000,	0.7393],
                                              [0.2500,	0.6531],
                                              [0.3000,	0.5630],
                                              [0.4000,	0.3676],
                                              [0.5000,	0.1831],
                                              [0.7500,	-0.2099],
                                              [1.0000,	-0.5093],
                                              [1.5000,	-0.9482],
                                              [2.0000,	-1.2538],
                                              [3.0000,	-1.6602],
                                              [4.0000,	-1.9346]]).T


# 5) MW = 4.5; Rrup = 100; h = 7
test_data['Allen_2012_test_accel5'] = array([[0.0100,	0.0639],
                                              [0.0200,	0.1937],
                                              [0.0300,	0.2405],
                                              [0.0500,	0.3083],
                                              [0.0750,	0.3543],
                                              [0.1000,	0.3758],
                                              [0.1500,	0.3841],
                                              [0.2000,	0.3586],
                                              [0.2500,	0.3172],
                                              [0.3000,	0.2635],
                                              [0.4000,	0.1155],
                                              [0.5000,	-0.0422],
                                              [0.7500,	-0.3987],
                                              [1.0000,	-0.6777],
                                              [1.5000,	-1.1051],
                                              [2.0000,	-1.4137],
                                              [3.0000,	-1.8295],
                                              [4.0000,	-2.1118]]).T


# 6) MW = 4.5; Rrup = 100; h = 14
test_data['Allen_2012_test_accel6'] = array([[0.0100,	0.0742],
                                              [0.0200,	0.1952],
                                              [0.0300,	0.2711],
                                              [0.0500,	0.3618],
                                              [0.0750,	0.4071],
                                              [0.1000,	0.4171],
                                              [0.1500,	0.3932],
                                              [0.2000,	0.3354],
                                              [0.2500,	0.2648],
                                              [0.3000,	0.1869],
                                              [0.4000,	0.0041],
                                              [0.5000,	-0.1765],
                                              [0.7500,	-0.5653],
                                              [1.0000,	-0.8610],
                                              [1.5000,	-1.3017],
                                              [2.0000,	-1.6136],
                                              [3.0000,	-2.0282],
                                              [4.0000,	-2.3072]]).T


# 7) MW = 4.5; Rrup = 200; h = 7
test_data['Allen_2012_test_accel7'] = array([[0.0100,	-0.3488],
                                              [0.0200,	-0.2961],
                                              [0.0300,	-0.2658],
                                              [0.0500,	-0.2106],
                                              [0.0750,	-0.1453],
                                              [0.1000,	-0.0929],
                                              [0.1500,	-0.0224],
                                              [0.2000,	0.0124],
                                              [0.2500,	0.0273],
                                              [0.3000,	0.0184],
                                              [0.4000,	-0.0798],
                                              [0.5000,	-0.2179],
                                              [0.7500,	-0.5657],
                                              [1.0000,	-0.8479],
                                              [1.5000,	-1.2760],
                                              [2.0000,	-1.5813],
                                              [3.0000,	-1.9988],
                                              [4.0000,	-2.2852]]).T


# 8) MW = 4.5; Rrup = 200; h = 14
test_data['Allen_2012_test_accel8'] = array([[0.0100,	-0.3595],
                                              [0.0200,	-0.3094],
                                              [0.0300,	-0.2571],
                                              [0.0500,	-0.1841],
                                              [0.0750,	-0.1128],
                                              [0.1000,	-0.0641],
                                              [0.1500,	-0.0162],
                                              [0.2000,	-0.0091],
                                              [0.2500,	-0.0208],
                                              [0.3000,	-0.0527],
                                              [0.4000,	-0.1872],
                                              [0.5000,	-0.3521],
                                              [0.7500,	-0.7357],
                                              [1.0000,	-1.0321],
                                              [1.5000,	-1.4721],
                                              [2.0000,	-1.7820],
                                              [3.0000,	-2.1942],
                                              [4.0000,	-2.4735]]).T


# 9) MW = 5.5; Rrup = 20; h = 7
test_data['Allen_2012_test_accel9'] = array([[0.0100,	1.7698],
                                              [0.0200,	1.8800],
                                              [0.0300,	1.9405],
                                              [0.0500,	1.9940],
                                              [0.0750,	2.0206],
                                              [0.1000,	2.0286],
                                              [0.1500,	2.0193],
                                              [0.2000,	1.9911],
                                              [0.2500,	1.9557],
                                              [0.3000,	1.9134],
                                              [0.4000,	1.8019],
                                              [0.5000,	1.6847],
                                              [0.7500,	1.4121],
                                              [1.0000,	1.1907],
                                              [1.5000,	0.8310],
                                              [2.0000,	0.5577],
                                              [3.0000,	0.1659],
                                              [4.0000,	-0.1138]]).T


# 10) MW = 5.5; Rrup = 20; h = 14
test_data['Allen_2012_test_accel10'] = array([[0.0100,	1.9109],
                                               [0.0200,	2.0355],
                                               [0.0300,	2.0978],
                                               [0.0500,	2.1632],
                                               [0.0750,	2.1899],
                                               [0.1000,	2.1937],
                                               [0.1500,	2.1784],
                                               [0.2000,	2.1423],
                                               [0.2500,	2.0972],
                                               [0.3000,	2.0451],
                                               [0.4000,	1.9148],
                                               [0.5000,	1.7816],
                                               [0.7500,	1.4745],
                                               [1.0000,	1.2256],
                                               [1.5000,	0.8322],
                                               [2.0000,	0.5414],
                                               [3.0000,	0.1363],
                                               [4.0000,	-0.1452]]).T


# 11) MW = 5.5; Rrup = 50; h = 7
test_data['Allen_2012_test_accel11'] = array([[0.0100,	1.1383],
                                               [0.0200,	1.2479],
                                               [0.0300,	1.2957],
                                               [0.0500,	1.3542],
                                               [0.0750,	1.3939],
                                               [0.1000,	1.4142],
                                               [0.1500,	1.4270],
                                               [0.2000,	1.4166],
                                               [0.2500,	1.3957],
                                               [0.3000,	1.3645],
                                               [0.4000,	1.2666],
                                               [0.5000,	1.1564],
                                               [0.7500,	0.8924],
                                               [1.0000,	0.6752],
                                               [1.5000,	0.3178],
                                               [2.0000,	0.0436],
                                               [3.0000,	-0.3517],
                                               [4.0000,	-0.6354]]).T


# 12) MW = 5.5; Rrup = 50; h = 14
test_data['Allen_2012_test_accel12'] = array([[0.0100,	1.2533],
                                               [0.0200,	1.3665],
                                               [0.0300,	1.4292],
                                               [0.0500,	1.4984],
                                               [0.0750,	1.5407],
                                               [0.1000,	1.5600],
                                               [0.1500,	1.5666],
                                               [0.2000,	1.5472],
                                               [0.2500,	1.5163],
                                               [0.3000,	1.4754],
                                               [0.4000,	1.3589],
                                               [0.5000,	1.2325],
                                               [0.7500,	0.9334],
                                               [1.0000,	0.6888],
                                               [1.5000,	0.2960],
                                               [2.0000,	0.0025],
                                               [3.0000,	-0.4060],
                                               [4.0000,	-0.6902]]).T


# 13) MW = 5.5; Rrup = 100; h = 7
test_data['Allen_2012_test_accel13'] = array([[0.0100,	0.7692],
                                               [0.0200,	0.8587],
                                               [0.0300,	0.8963],
                                               [0.0500,	0.9603],
                                               [0.0750,	1.0144],
                                               [0.1000,	1.0484],
                                               [0.1500,	1.0836],
                                               [0.2000,	1.0928],
                                               [0.2500,	1.0896],
                                               [0.3000,	1.0719],
                                               [0.4000,	0.9858],
                                               [0.5000,	0.8765],
                                               [0.7500,	0.6145],
                                               [1.0000,	0.4047],
                                               [1.5000,	0.0486],
                                               [2.0000,	-0.2312],
                                               [3.0000,	-0.6282],
                                               [4.0000,	-0.9094]]).T


# 14) MW = 5.5; Rrup = 100; h = 14
test_data['Allen_2012_test_accel14'] = array([[0.0100,	0.8714],
                                               [0.0200,	0.9630],
                                               [0.0300,	1.0205],
                                               [0.0500,	1.0887],
                                               [0.0750,	1.1451],
                                               [0.1000,	1.1795],
                                               [0.1500,	1.2065],
                                               [0.2000,	1.2048],
                                               [0.2500,	1.1915],
                                               [0.3000,	1.1650],
                                               [0.4000,	1.0634],
                                               [0.5000,	0.9414],
                                               [0.7500,	0.6447],
                                               [1.0000,	0.4017],
                                               [1.5000,	0.0099],
                                               [2.0000,	-0.2851],
                                               [3.0000,	-0.7011],
                                               [4.0000,	-0.9904]]).T


# 15) MW = 5.5; Rrup = 200; h = 7
test_data['Allen_2012_test_accel15'] = array([[0.0100,	0.3700],
                                              [0.0200,	0.3983],
                                              [0.0300,	0.4183],
                                              [0.0500,	0.4671],
                                              [0.0750,	0.5343],
                                              [0.1000,	0.5932],
                                              [0.1500,	0.6815],
                                              [0.2000,	0.7440],
                                              [0.2500,	0.7911],
                                              [0.3000,	0.8139],
                                              [0.4000,	0.7735],
                                              [0.5000,	0.6830],
                                              [0.7500,	0.4288],
                                              [1.0000,	0.2142],
                                              [1.5000,	-0.1422],
                                              [2.0000,	-0.4165],
                                              [3.0000,	-0.8117],
                                              [4.0000,	-1.0953]]).T


# 16) MW = 5.5; Rrup = 200; h = 14
test_data['Allen_2012_test_accel16'] = array([[0.0100,	0.4681],
                                              [0.0200,	0.4978],
                                              [0.0300,	0.5325],
                                              [0.0500,	0.5869],
                                              [0.0750,	0.6551],
                                              [0.1000,	0.7146],
                                              [0.1500,	0.8047],
                                              [0.2000,	0.8617],
                                              [0.2500,	0.8989],
                                              [0.3000,	0.9115],
                                              [0.4000,	0.8523],
                                              [0.5000,	0.7455],
                                              [0.7500,	0.4563],
                                              [1.0000,	0.2141],
                                              [1.5000,	-0.1761],
                                              [2.0000,	-0.4690],
                                              [3.0000,	-0.8820],
                                              [4.0000,	-1.1711]]).T


# 17) MW = 6.5; Rrup = 20; h = 7
test_data['Allen_2012_test_accel17'] = array([[0.0100,	2.1974],
                                               [0.0200,	2.2994],
                                               [0.0300,	2.3485],
                                               [0.0500,	2.3940],
                                               [0.0750,	2.4187],
                                               [0.1000,	2.4302],
                                               [0.1500,	2.4370],
                                               [0.2000,	2.4265],
                                               [0.2500,	2.4071],
                                               [0.3000,	2.3803],
                                               [0.4000,	2.3019],
                                               [0.5000,	2.2162],
                                               [0.7500,	2.0138],
                                               [1.0000,	1.8482],
                                               [1.5000,	1.5694],
                                               [2.0000,	1.3511],
                                               [3.0000,	1.0329],
                                               [4.0000,	0.7969]]).T


# 18) MW = 6.5; Rrup = 20; h = 14
test_data['Allen_2012_test_accel18'] = array([[0.0100,	2.3755],
                                               [0.0200,	2.4887],
                                               [0.0300,	2.5246],
                                               [0.0500,	2.5820],
                                               [0.0750,	2.6141],
                                               [0.1000,	2.6278],
                                               [0.1500,	2.6377],
                                               [0.2000,	2.6281],
                                               [0.2500,	2.6079],
                                               [0.3000,	2.5789],
                                               [0.4000,	2.4935],
                                               [0.5000,	2.4001],
                                               [0.7500,	2.1763],
                                               [1.0000,	1.9905],
                                               [1.5000,	1.6784],
                                               [2.0000,	1.4361],
                                               [3.0000,	1.0873],
                                               [4.0000,	0.8336]]).T


# 19) MW = 6.5; Rrup = 50; h = 7
test_data['Allen_2012_test_accel19'] = array([[0.0100,	1.6338],
                                               [0.0200,	1.7267],
                                               [0.0300,	1.7669],
                                               [0.0500,	1.8168],
                                               [0.0750,	1.8549],
                                               [0.1000,	1.8783],
                                               [0.1500,	1.9020],
                                               [0.2000,	1.9070],
                                               [0.2500,	1.9030],
                                               [0.3000,	1.8888],
                                               [0.4000,	1.8255],
                                               [0.5000,	1.7467],
                                               [0.7500,	1.5529],
                                               [1.0000,	1.3931],
                                               [1.5000,	1.1226],
                                               [2.0000,	0.9093],
                                               [3.0000,	0.5915],
                                               [4.0000,	0.3531]]).T


# 20) MW = 6.5; Rrup = 50; h = 14
test_data['Allen_2012_test_accel20'] = array([[0.0100,	1.7919],
                                               [0.0200,	1.8891],
                                               [0.0300,	1.9343],
                                               [0.0500,	1.9894],
                                               [0.0750,	2.0347],
                                               [0.1000,	2.0637],
                                               [0.1500,	2.0923],
                                               [0.2000,	2.0980],
                                               [0.2500,	2.0927],
                                               [0.3000,	2.0763],
                                               [0.4000,	2.0063],
                                               [0.5000,	1.9202],
                                               [0.7500,	1.7044],
                                               [1.0000,	1.5228],
                                               [1.5000,	1.2176],
                                               [2.0000,	0.9805],
                                               [3.0000,	0.6373],
                                               [4.0000,	0.3852]]).T


# 21) MW = 6.5; Rrup = 100; h = 7
test_data['Allen_2012_test_accel21'] = array([[0.0100,	1.3271],
                                               [0.0200,	1.3951],
                                               [0.0300,	1.4271],
                                               [0.0500,	1.4801],
                                               [0.0750,	1.5306],
                                               [0.1000,	1.5666],
                                               [0.1500,	1.6113],
                                               [0.2000,	1.6354],
                                               [0.2500,	1.6494],
                                               [0.3000,	1.6491],
                                               [0.4000,	1.5978],
                                               [0.5000,	1.5192],
                                               [0.7500,	1.3264],
                                               [1.0000,	1.1745],
                                               [1.5000,	0.9054],
                                               [2.0000,	0.6870],
                                               [3.0000,	0.3705],
                                               [4.0000,	0.1372]]).T


# 22) MW = 6.5; Rrup = 100; h = 14
test_data['Allen_2012_test_accel22'] = array([[0.0100,	1.4803],
                                               [0.0200,	1.5549],
                                               [0.0300,	1.5937],
                                               [0.0500,	1.6425],
                                               [0.0750,	1.6975],
                                               [0.1000,	1.7396],
                                               [0.1500,	1.7881],
                                               [0.2000,	1.8118],
                                               [0.2500,	1.8250],
                                               [0.3000,	1.8240],
                                               [0.4000,	1.7705],
                                               [0.5000,	1.6898],
                                               [0.7500,	1.4750],
                                               [1.0000,	1.2924],
                                               [1.5000,	0.9887],
                                               [2.0000,	0.7536],
                                               [3.0000,	0.4038],
                                               [4.0000,	0.1469]]).T


# 23)MW = 6.5; Rrup = 200; h = 7
test_data['Allen_2012_test_accel23'] = array([[0.0100,	0.9423],
                                               [0.0200,	0.9655],
                                               [0.0300,	0.9788],
                                               [0.0500,	1.0147],
                                               [0.0750,	1.0713],
                                               [0.1000,	1.1253],
                                               [0.1500,	1.2130],
                                               [0.2000,	1.2832],
                                               [0.2500,	1.3414],
                                               [0.3000,	1.3771],
                                               [0.4000,	1.3679],
                                               [0.5000,	1.3080],
                                               [0.7500,	1.1228],
                                               [1.0000,	0.9650],
                                               [1.5000,	0.6955],
                                               [2.0000,	0.4844],
                                               [3.0000,	0.1728],
                                               [4.0000,	-0.0609]]).T


# 24) MW = 6.5; Rrup = 200; h = 14
test_data['Allen_2012_test_accel24'] = array([[0.0100,	1.1085],
                                               [0.0200,	1.1311],
                                               [0.0300,	1.1489],
                                               [0.0500,	1.1873],
                                               [0.0750,	1.2401],
                                               [0.1000,	1.2934],
                                               [0.1500,	1.3940],
                                               [0.2000,	1.4699],
                                               [0.2500,	1.5255],
                                               [0.3000,	1.5570],
                                               [0.4000,	1.5404],
                                               [0.5000,	1.4744],
                                               [0.7500,	1.2696],
                                               [1.0000,	1.0896],
                                               [1.5000,	0.7885],
                                               [2.0000,	0.5551],
                                               [3.0000,	0.2090],
                                               [4.0000 ,-0.0464]]).T


# 25) MW = 7.5; Rrup = 20; h = 7
test_data['Allen_2012_test_accel25'] = array([[0.0100,	2.4859],
                                               [0.0200,	2.5942],
                                               [0.0300,	2.6357],
                                               [0.0500,	2.6674],
                                               [0.0750,	2.6802],
                                               [0.1000,	2.6855],
                                               [0.1500,	2.6901],
                                               [0.2000,	2.6780],
                                               [0.2500,	2.6554],
                                               [0.3000,	2.6267],
                                               [0.4000,	2.5538],
                                               [0.5000,	2.4796],
                                               [0.7500,	2.3213],
                                               [1.0000,	2.2029],
                                               [1.5000,	2.0232],
                                               [2.0000,	1.8923],
                                               [3.0000,	1.7097],
                                               [4.0000,	1.5655]]).T

# 26) MW = 7.5; Rrup = 20; h = 14
test_data['Allen_2012_test_accel26'] = array([[0.0100,	2.6588],
                                               [0.0200,	2.7703],
                                               [0.0300,	2.7825],
                                               [0.0500,	2.8330],
                                               [0.0750,	2.8589],
                                               [0.1000,	2.8669],
                                               [0.1500,	2.8706],
                                               [0.2000,	2.8563],
                                               [0.2500,	2.8315],
                                               [0.3000,	2.8011],
                                               [0.4000,	2.7285],
                                               [0.5000,	2.6570],
                                               [0.7500,	2.5058],
                                               [1.0000,	2.3914],
                                               [1.5000,	2.2024],
                                               [2.0000,	2.0532],
                                               [3.0000,	1.8284],
                                               [4.0000,	1.6445]]).T


# 27) MW = 7.5; Rrup = 50; h = 7
test_data['Allen_2012_test_accel27'] = array([[0.0100,	1.9904],
                                               [0.0200,	2.0813],
                                               [0.0300,	2.1180],
                                               [0.0500,	2.1535],
                                               [0.0750,	2.1799],
                                               [0.1000,	2.1965],
                                               [0.1500,	2.2130],
                                               [0.2000,	2.2141],
                                               [0.2500,	2.2075],
                                               [0.3000,	2.1929],
                                               [0.4000,	2.1364],
                                               [0.5000,	2.0691],
                                               [0.7500,	1.9193],
                                               [1.0000,	1.8081],
                                               [1.5000,	1.6428],
                                               [2.0000,	1.5225],
                                               [3.0000,	1.3442],
                                               [4.0000,	1.1992]]).T


# 28) MW = 7.5; Rrup = 50; h = 14
test_data['Allen_2012_test_accel28'] = array([[0.0100,	2.1494],
                                               [0.0200,	2.2405],
                                               [0.0300,	2.2708],
                                               [0.0500,	2.3132],
                                               [0.0750,	2.3500],
                                               [0.1000,	2.3728],
                                               [0.1500,	2.3923],
                                               [0.2000,	2.3919],
                                               [0.2500,	2.3826],
                                               [0.3000,	2.3660],
                                               [0.4000,	2.3102],
                                               [0.5000,	2.2466],
                                               [0.7500,	2.1032],
                                               [1.0000,	1.9931],
                                               [1.5000,	1.8169],
                                               [2.0000,	1.6806],
                                               [3.0000,	1.4699],
                                               [4.0000,	1.2917]]).T


# 29) MW = 7.5; Rrup = 100; h = 7
test_data['Allen_2012_test_accel29'] = array([[0.0100,	1.7366],
                                               [0.0200,	1.8028],
                                               [0.0300,	1.8324],
                                               [0.0500,	1.8671],
                                               [0.0750,	1.9023],
                                               [0.1000,	1.9298],
                                               [0.1500,	1.9664],
                                               [0.2000,	1.9858],
                                               [0.2500,	1.9957],
                                               [0.3000,	1.9940],
                                               [0.4000,	1.9505],
                                               [0.5000,	1.8852],
                                               [0.7500,	1.7368],
                                               [1.0000,	1.6312],
                                               [1.5000,	1.4641],
                                               [2.0000,	1.3401],
                                               [3.0000,	1.1658],
                                               [4.0000,	1.0270]]).T


# 30) MW = 7.5; Rrup = 100; h = 14
test_data['Allen_2012_test_accel30'] = array([[0.0100,	1.9002],
                                               [0.0200,	1.9705],
                                               [0.0300,	1.9903],
                                               [0.0500,	2.0226],
                                               [0.0750,	2.0636],
                                               [0.1000,	2.0969],
                                               [0.1500,	2.1375],
                                               [0.2000,	2.1560],
                                               [0.2500,	2.1650],
                                               [0.3000,	2.1634],
                                               [0.4000,	2.1248],
                                               [0.5000,	2.0681],
                                               [0.7500,	1.9253],
                                               [1.0000,	1.8104],
                                               [1.5000,	1.6340],
                                               [2.0000,	1.5016],
                                               [3.0000,	1.2858],
                                               [4.0000,	1.1042]]).T


# 31) MW = 7.5; Rrup = 200; h = 7
test_data['Allen_2012_test_accel31'] = array([[0.0100,	1.3672],
                                               [0.0200,	1.4052],
                                               [0.0300,	1.4155],
                                               [0.0500,	1.4317],
                                               [0.0750,	1.4651],
                                               [0.1000,	1.5025],
                                               [0.1500,	1.5714],
                                               [0.2000,	1.6294],
                                               [0.2500,	1.6775],
                                               [0.3000,	1.7071],
                                               [0.4000,	1.7025],
                                               [0.5000,	1.6564],
                                               [0.7500,	1.5159],
                                               [1.0000,	1.4039],
                                               [1.5000,	1.2363],
                                               [2.0000,	1.1207],
                                               [3.0000,	0.9541],
                                               [4.0000,	0.8168]]).T


# 32) MW = 7.5; Rrup = 200; h = 14
test_data['Allen_2012_test_accel32'] = array([[0.0100,	1.5614],
                                              [0.0200,	1.5902],
                                              [0.0300,	1.5916],
                                              [0.0500,	1.6167],
                                              [0.0750,	1.6417],
                                              [0.1000,	1.6716],
                                              [0.1500,	1.7513],
                                              [0.2000,	1.8152],
                                              [0.2500,	1.8587],
                                              [0.3000,	1.8834],
                                              [0.4000,	1.8766],
                                              [0.5000,	1.8342],
                                              [0.7500,	1.7037],
                                              [1.0000,	1.5940],
                                              [1.5000,	1.4210],
                                              [2.0000,	1.2893],
                                              [3.0000,	1.0782],
                                              [4.0000,	0.9001]]).T

test_data['Allen_2012_test_sigma_shallow'] = array([0.4120,
                                                    0.4383,
                                                    0.4310,
                                                    0.3994,
                                                    0.3805,
                                                    0.3720,
                                                    0.3637,
                                                    0.3594,
                                                    0.3575,
                                                    0.3558,
                                                    0.3544,
                                                    0.3522,
                                                    0.3495,
                                                    0.3487,
                                                    0.3492,
                                                    0.3484,
                                                    0.3467,
                                                    0.3457]).T


test_data['Allen_2012_test_sigma_deep'] = array([0.36530,
                                                 0.38970,
                                                 0.38400,
                                                 0.35580,
                                                 0.33920,
                                                 0.33230,
                                                 0.32710,
                                                 0.32470,
                                                 0.32460,
                                                 0.32450,
                                                 0.32480,
                                                 0.32250,
                                                 0.31880,
                                                 0.31800,
                                                 0.31610,
                                                 0.31420,
                                                 0.31130,
                                                 0.3097]).T


# In each array the first column has the period in seconds and the second has 
# the corresponding response spectral period in cm/s^2.

# Period
test_data['Allen_2012_test_period'] = \
    test_data['Allen_2012_test_accel1'][0]

# Mean
tmp = zeros((32, 18)) 
tmp[0,:] =  test_data['Allen_2012_test_accel1'][1] 
tmp[1,:] =  test_data['Allen_2012_test_accel2'][1]   
tmp[2,:] =  test_data['Allen_2012_test_accel3'][1]   
tmp[3,:] =  test_data['Allen_2012_test_accel4'][1] 
tmp[4,:] =  test_data['Allen_2012_test_accel5'][1]
tmp[5,:] =  test_data['Allen_2012_test_accel6'][1]
tmp[6,:] =  test_data['Allen_2012_test_accel7'][1]
tmp[7,:] =  test_data['Allen_2012_test_accel8'][1]
tmp[8,:] =  test_data['Allen_2012_test_accel9'][1]
tmp[9,:] =  test_data['Allen_2012_test_accel10'][1]
tmp[10,:] = test_data['Allen_2012_test_accel11'][1]
tmp[11,:] = test_data['Allen_2012_test_accel12'][1]
tmp[12,:] =  test_data['Allen_2012_test_accel13'][1] 
tmp[13,:] =  test_data['Allen_2012_test_accel14'][1]   
tmp[14,:] =  test_data['Allen_2012_test_accel15'][1]   
tmp[15,:] =  test_data['Allen_2012_test_accel16'][1] 
tmp[16,:] =  test_data['Allen_2012_test_accel17'][1]
tmp[17,:] =  test_data['Allen_2012_test_accel18'][1]
tmp[18,:] =  test_data['Allen_2012_test_accel19'][1]
tmp[19,:] =  test_data['Allen_2012_test_accel20'][1]
tmp[20,:] =  test_data['Allen_2012_test_accel21'][1]
tmp[21,:] =  test_data['Allen_2012_test_accel22'][1]
tmp[22,:] = test_data['Allen_2012_test_accel23'][1]
tmp[23,:] = test_data['Allen_2012_test_accel24'][1]
tmp[24,:] =  test_data['Allen_2012_test_accel25'][1] 
tmp[25,:] =  test_data['Allen_2012_test_accel26'][1]   
tmp[26,:] =  test_data['Allen_2012_test_accel27'][1]   
tmp[27,:] =  test_data['Allen_2012_test_accel28'][1] 
tmp[28,:] =  test_data['Allen_2012_test_accel29'][1]
tmp[29,:] =  test_data['Allen_2012_test_accel30'][1]
tmp[30,:] =  test_data['Allen_2012_test_accel31'][1]
tmp[31,:] =  test_data['Allen_2012_test_accel32'][1]

# Convert cm/sec**2 to g
#test_data['Allen_2012_test_mean'] = tmp/980.665
test_data['Allen_2012_test_mean'] = power(10,tmp)/980.665
del tmp

# Sigma
#tmp = zeros((12, 18))
#tmp[0,:] =  test_data['Allen_2012_test_sigma_shallow'] # accelM60R100D5
#tmp[1,:] =  test_data['Allen_2012_test_sigma_shallow'] # accelM40R100D5
#tmp[2,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM35R100D10
#tmp[3,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM35R10D10
#tmp[4,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM40R10D10
#tmp[5,:] =  test_data['Allen_2012_test_sigma_shallow'] # accelM60R10D5
#tmp[6,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM60R100D10
#tmp[7,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM60R10D10
#tmp[8,:] =  test_data['Allen_2012_test_sigma_shallow'] # accelM40R10D5
#tmp[9,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM40R100D10
#tmp[10,:] = test_data['Allen_2012_test_sigma_shallow'] # accelM35R10D5
#tmp[11,:] = test_data['Allen_2012_test_sigma_shallow'] # accelM35R100D5
# Convert cm/sec**2 to natural log of g
#test_data['Allen_2012_test_sigma'] = tmp/Log102Ln #- LnCmss2Lng
#del tmp
    
# Mw
test_data['Allen_2012_test_magnitude'] = [4.5, 
                                          4.5,
                                          4.5,
                                          4.5, 
                                          4.5, 
                                          4.5, 
                                          4.5,
                                          4.5, 
                                          5.5,
                                          5.5, 
                                          5.5, 
                                          5.5, 
                                          5.5, 
                                          5.5,
                                          5.5, 
                                          5.5, 
                                          6.5, 
                                          6.5, 
                                          6.5, 
                                          6.5, 
                                          6.5, 
                                          6.5, 
                                          6.5, 
                                          6.5, 
                                          7.5, 
                                          7.5,
                                          7.5, 
                                          7.5, 
                                          7.5,
                                          7.5,
                                          7.5,
                                          7.5]


# Rrup
test_data['Allen_2012_test_distance'] = [[20,
                                          20,
                                          50,
                                          50,
                                          100,
                                          100,
                                          200,
                                          200,
                                          20,
                                          20,
                                          50,
                                          50,
                                          100,
                                          100,
                                          200,
                                          200,
                                          20,
                                          20,
                                          50,
                                          50,
                                          100,
                                          100,
                                          200,
                                          200,
                                          20,
                                          20,
                                          50,
                                          50,
                                          100,
                                          100,
                                          200,
                                          200]]


# Depth
test_data['Allen_2012_test_depth'] =     [7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14,
                                          7,
                                          14]



#***************  END ALLEN 2012 MODEL  ***********************

################################################################################
class Distance_stub(object):
    """This object is used for simple cases.

    For more complex models, this object is overridden.
    """

    def __init__(self, dist):
        dist = asarray(dist)
        self.Rupture = dist
        self.Joyner_Boore = dist
        self.Horizontal = dist
        self.Hypocentral = dist
        self.Epicentral = dist

    def distance(self, dummy):
        return self.Rupture

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
        
    distance_types = distances.__dict__.keys()
        

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

    return (distances, distance_types, magnitudes, test_mean, test_sigma, 
            periods, depths, Vs30, depth_to_top, fault_type, Z25, dip, width)

def ground_motion_interface_conformance(GM_class, model_name):
    """
    This checks that for the given test_distance and test_magnitudes,
    the calculated ground motion is the same as the test_ground_motion
    """

    (distances, distance_types, magnitudes, test_mean, test_sigma, periods, 
     depths, Vs30, depth_to_top, fault_type, Z25, dip, 
     width) = data2atts(model_name)

    if GM_class is Ground_motion_calculator:
        gm = GM_class(model_name, periods)
        (log_mean, log_sigma) = \
            gm.distribution_function(distances, distance_types,
                                     magnitudes, periods=periods,
                                     depth=depths, Vs30=Vs30,
                                     depth_to_top=depth_to_top,
                                     fault_type=fault_type, Z25=Z25,
                                     dip=dip, width=width)
    elif GM_class is Multiple_ground_motion_calculator:
        model_weights = [1]
        gm = GM_class([model_name], periods, model_weights)
        # ignoring event_activity
        log_mean, log_sigma = \
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
        imported = ground_motion_init[model_name]
        self.failUnless(model.magnitude_type==imported[1],
                        'Model attributes incorrect.')
        self.failUnless(model.distance_types==imported[2],
                        'Model attributes incorrect.')
        self.assert_(allclose(model.coefficient, imported[3]))
        self.failUnless(model.coefficient_period==imported[4],
                        'Model attributes incorrect.')
        self.assert_(allclose(model.sigma_coefficient, imported[6]))
        self.assert_(allclose(model.sigma_coefficient_period, imported[7]))


#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_ground_motion_specification, 'test')
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)
