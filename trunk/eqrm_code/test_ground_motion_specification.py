import unittest

from scipy import array, exp, log, allclose, newaxis, asarray, zeros
import math

from eqrm_code.ground_motion_specification import *
from eqrm_code.ground_motion_interface import ground_motion_init
from eqrm_code.ground_motion_misc import \
     Australian_standard_model_interpolation
from eqrm_code.ground_motion_calculator import Ground_motion_calculator, \
     Multiple_ground_motion_calculator

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
        """We *must* define a 'distance' method, results unused."""

        return self.Rupture

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

# Test data from test_ground_motions.mat
# Mw=6.0, Rrup=100.0, Depth=5.0
test_data['Allen_2012_test_accelM60R100D5'] = array([
       [  1.00000000e+01,   7.09724397e-02],
       [  7.69230769e+00,   1.16683665e-01],
       [  6.25000000e+00,   1.94701357e-01],
       [  5.00000000e+00,   3.10336049e-01],
       [  4.00000000e+00,   5.14278087e-01],
       [  3.12500000e+00,   8.45214112e-01],
       [  2.50000000e+00,   1.36842969e+00],
       [  2.00000000e+00,   2.29616406e+00],
       [  1.58730159e+00,   3.61505398e+00],
       [  1.25000000e+00,   5.63781306e+00],
       [  1.00000000e+00,   8.25442660e+00],
       [  7.93650794e-01,   1.16450967e+01],
       [  6.28930818e-01,   1.56583414e+01],
       [  5.00000000e-01,   2.12182583e+01],
       [  3.96825397e-01,   2.55604540e+01],
       [  3.15457413e-01,   2.79705808e+01],
       [  2.50626566e-01,   2.90826060e+01],
       [  1.98807157e-01,   2.88387431e+01],
       [  1.57977883e-01,   2.79498016e+01],
       [  1.25470514e-01,   2.64989628e+01],
       [  9.96015936e-02,   2.50721113e+01],
       [  7.91139241e-02,   2.31657039e+01],
       [  6.28535512e-02,   2.16489631e+01],
       [  4.99001996e-02,   2.07896877e+01],
       [  3.96353547e-02,   1.97885043e+01],
       [  3.14762354e-02,   1.90362869e+01],
       [  2.50000000e-02,   1.83050051e+01],
       [  1.01010101e-02,   1.43498929e+01]]).T

# Mw=4.0, Rrup=100, Depth=5.0
test_data['Allen_2012_test_accelM40R100D5'] = array([
       [  1.00000000e+01,   3.20200526e-04],
       [  7.69230769e+00,   5.04840625e-04],
       [  6.25000000e+00,   7.95491093e-04],
       [  5.00000000e+00,   1.27234201e-03],
       [  4.00000000e+00,   2.01920699e-03],
       [  3.12500000e+00,   3.28500865e-03],
       [  2.50000000e+00,   5.42287766e-03],
       [  2.00000000e+00,   9.12949782e-03],
       [  1.58730159e+00,   1.59787738e-02],
       [  1.25000000e+00,   2.81326846e-02],
       [  1.00000000e+00,   5.13965745e-02],
       [  7.93650794e-01,   9.27996193e-02],
       [  6.28930818e-01,   1.65131101e-01],
       [  5.00000000e-01,   2.86233935e-01],
       [  3.96825397e-01,   4.77380322e-01],
       [  3.15457413e-01,   6.86604407e-01],
       [  2.50626566e-01,   9.13783511e-01],
       [  1.98807157e-01,   1.14457586e+00],
       [  1.57977883e-01,   1.32726586e+00],
       [  1.25470514e-01,   1.43357859e+00],
       [  9.96015936e-02,   1.45324093e+00],
       [  7.91139241e-02,   1.42715015e+00],
       [  6.28535512e-02,   1.37699552e+00],
       [  4.99001996e-02,   1.28562224e+00],
       [  3.96353547e-02,   1.15831339e+00],
       [  3.14762354e-02,   1.03911054e+00],
       [  2.50000000e-02,   9.46718326e-01],
       [  1.01010101e-02,   6.45252577e-01]]).T

# Mw=3.5, Rrup=100, Depth=10.0
test_data['Allen_2012_test_accelM35R100D10'] = array([
       [  1.00000000e+01,   9.24386200e-05],
       [  7.69230769e+00,   1.43702016e-04],
       [  6.25000000e+00,   2.22092362e-04],
       [  5.00000000e+00,   3.33353108e-04],
       [  4.00000000e+00,   5.11307841e-04],
       [  3.12500000e+00,   7.63708354e-04],
       [  2.50000000e+00,   1.17163538e-03],
       [  2.00000000e+00,   1.88678450e-03],
       [  1.58730159e+00,   3.03654432e-03],
       [  1.25000000e+00,   4.97695311e-03],
       [  1.00000000e+00,   9.01996928e-03],
       [  7.93650794e-01,   1.67451693e-02],
       [  6.28930818e-01,   3.17380215e-02],
       [  5.00000000e-01,   5.88403785e-02],
       [  3.96825397e-01,   1.13359399e-01],
       [  3.15457413e-01,   1.87850769e-01],
       [  2.50626566e-01,   2.95781005e-01],
       [  1.98807157e-01,   4.20239608e-01],
       [  1.57977883e-01,   5.62245833e-01],
       [  1.25470514e-01,   6.74766882e-01],
       [  9.96015936e-02,   7.68501745e-01],
       [  7.91139241e-02,   8.56929902e-01],
       [  6.28535512e-02,   8.89943559e-01],
       [  4.99001996e-02,   8.90715671e-01],
       [  3.96353547e-02,   9.08423192e-01],
       [  3.14762354e-02,   8.76271094e-01],
       [  2.50000000e-02,   8.51859139e-01],
       [  1.01010101e-02,   4.44796721e-01]]).T

# Mw=3.5, Rrup=100, Depth=10.0
test_data['Allen_2012_test_accelM35R10D10'] = array([
       [  1.00000000e+01,   3.01654849e-03],
       [  7.69230769e+00,   4.62967813e-03],
       [  6.25000000e+00,   7.07864549e-03],
       [  5.00000000e+00,   1.00659085e-02],
       [  4.00000000e+00,   1.45756236e-02],
       [  3.12500000e+00,   2.14630582e-02],
       [  2.50000000e+00,   3.18517493e-02],
       [  2.00000000e+00,   4.77313649e-02],
       [  1.58730159e+00,   7.45642630e-02],
       [  1.25000000e+00,   1.16442022e-01],
       [  1.00000000e+00,   2.06870747e-01],
       [  7.93650794e-01,   3.82774832e-01],
       [  6.28930818e-01,   7.19075384e-01],
       [  5.00000000e-01,   1.51096073e+00],
       [  3.96825397e-01,   2.82223113e+00],
       [  3.15457413e-01,   5.25723248e+00],
       [  2.50626566e-01,   9.30472103e+00],
       [  1.98807157e-01,   1.44582151e+01],
       [  1.57977883e-01,   2.04971499e+01],
       [  1.25470514e-01,   2.88668165e+01],
       [  9.96015936e-02,   3.69227255e+01],
       [  7.91139241e-02,   4.34246637e+01],
       [  6.28535512e-02,   4.96002486e+01],
       [  4.99001996e-02,   5.72603909e+01],
       [  3.96353547e-02,   6.37102944e+01],
       [  3.14762354e-02,   6.33848550e+01],
       [  2.50000000e-02,   6.09007927e+01],
       [  1.01010101e-02,   2.75896798e+01]]).T

# Mw=4.0, R=10.0, Depth=10.0
test_data['Allen_2012_test_accelM40R10D10'] = array([
       [  1.00000000e+01,   9.48342485e-03],
       [  7.69230769e+00,   1.48096127e-02],
       [  6.25000000e+00,   2.31479765e-02],
       [  5.00000000e+00,   3.48267216e-02],
       [  4.00000000e+00,   5.30635287e-02],
       [  3.12500000e+00,   8.31538055e-02],
       [  2.50000000e+00,   1.31665250e-01],
       [  2.00000000e+00,   2.10238446e-01],
       [  1.58730159e+00,   3.46653412e-01],
       [  1.25000000e+00,   5.68253137e-01],
       [  1.00000000e+00,   1.00671383e+00],
       [  7.93650794e-01,   1.81329400e+00],
       [  6.28930818e-01,   3.26070622e+00],
       [  5.00000000e-01,   6.28801115e+00],
       [  3.96825397e-01,   1.06479723e+01],
       [  3.15457413e-01,   1.77708833e+01],
       [  2.50626566e-01,   2.79912831e+01],
       [  1.98807157e-01,   3.95754425e+01],
       [  1.57977883e-01,   5.15677735e+01],
       [  1.25470514e-01,   6.63957926e+01],
       [  9.96015936e-02,   7.89625381e+01],
       [  7.91139241e-02,   8.80293019e+01],
       [  6.28535512e-02,   9.66274777e+01],
       [  4.99001996e-02,   1.06718408e+02],
       [  3.96353547e-02,   1.13209383e+02],
       [  3.14762354e-02,   1.11200171e+02],
       [  2.50000000e-02,   1.05118123e+02],
       [  1.01010101e-02,   5.42485970e+01]]).T

# Mw=6.0, Rrup=10.0, Depth=5.0
test_data['Allen_2012_test_accelM60R10D5'] = array([
       [  1.00000000e+01,   8.73193790e-01],
       [  7.69230769e+00,   1.42293809e+00],
       [  6.25000000e+00,   2.34567651e+00],
       [  5.00000000e+00,   3.80636010e+00],
       [  4.00000000e+00,   6.30716221e+00],
       [  3.12500000e+00,   1.02502760e+01],
       [  2.50000000e+00,   1.67371994e+01],
       [  2.00000000e+00,   2.70266298e+01],
       [  1.58730159e+00,   4.34329200e+01],
       [  1.25000000e+00,   6.59856779e+01],
       [  1.00000000e+00,   9.87316939e+01],
       [  7.93650794e-01,   1.41634127e+02],
       [  6.28930818e-01,   1.94453340e+02],
       [  5.00000000e-01,   2.61071068e+02],
       [  3.96825397e-01,   3.29289485e+02],
       [  3.15457413e-01,   3.90947449e+02],
       [  2.50626566e-01,   4.30832239e+02],
       [  1.98807157e-01,   4.73243987e+02],
       [  1.57977883e-01,   4.90432309e+02],
       [  1.25470514e-01,   5.12966603e+02],
       [  9.96015936e-02,   5.19805476e+02],
       [  7.91139241e-02,   5.29747395e+02],
       [  6.28535512e-02,   5.28899422e+02],
       [  4.99001996e-02,   5.22259378e+02],
       [  3.96353547e-02,   5.10630336e+02],
       [  3.14762354e-02,   4.98926946e+02],
       [  2.50000000e-02,   4.72857186e+02],
       [  1.01010101e-02,   3.19722386e+02]]).T

# Mw=6.0, Rrup=100.0, Depth=10.0
test_data['Allen_2012_test_accelM60R100D10'] = array([
       [  1.00000000e+01,   6.47978886e-02],
       [  7.69230769e+00,   1.05556224e-01],
       [  6.25000000e+00,   1.74241676e-01],
       [  5.00000000e+00,   2.91906022e-01],
       [  4.00000000e+00,   4.85790295e-01],
       [  3.12500000e+00,   8.31218012e-01],
       [  2.50000000e+00,   1.35731006e+00],
       [  2.00000000e+00,   2.26580483e+00],
       [  1.58730159e+00,   3.75154710e+00],
       [  1.25000000e+00,   6.10954721e+00],
       [  1.00000000e+00,   9.64674760e+00],
       [  7.93650794e-01,   1.48068513e+01],
       [  6.28930818e-01,   2.13185956e+01],
       [  5.00000000e-01,   2.91271947e+01],
       [  3.96825397e-01,   3.75535525e+01],
       [  3.15457413e-01,   4.18901306e+01],
       [  2.50626566e-01,   4.44813649e+01],
       [  1.98807157e-01,   4.50076242e+01],
       [  1.57977883e-01,   4.36837483e+01],
       [  1.25470514e-01,   4.11809739e+01],
       [  9.96015936e-02,   3.85002735e+01],
       [  7.91139241e-02,   3.53736519e+01],
       [  6.28535512e-02,   3.35112869e+01],
       [  4.99001996e-02,   3.08692707e+01],
       [  3.96353547e-02,   2.86260515e+01],
       [  3.14762354e-02,   2.69245197e+01],
       [  2.50000000e-02,   2.51355281e+01],
       [  1.01010101e-02,   2.06118095e+01]]).T

# Mw=6.0, Rrup=10.0, Depth=10.0
test_data['Allen_2012_test_accelM60R10D10'] = array([
       [  1.00000000e+01,   7.60921932e-01],
       [  7.69230769e+00,   1.22633590e+00],
       [  6.25000000e+00,   1.99979140e+00],
       [  5.00000000e+00,   3.32509362e+00],
       [  4.00000000e+00,   5.44587947e+00],
       [  3.12500000e+00,   9.06469066e+00],
       [  2.50000000e+00,   1.50328062e+01],
       [  2.00000000e+00,   2.51595723e+01],
       [  1.58730159e+00,   4.18017371e+01],
       [  1.25000000e+00,   6.74905723e+01],
       [  1.00000000e+00,   1.06835866e+02],
       [  7.93650794e-01,   1.62609136e+02],
       [  6.28930818e-01,   2.41069330e+02],
       [  5.00000000e-01,   3.42882718e+02],
       [  3.96825397e-01,   4.47105575e+02],
       [  3.15457413e-01,   5.51952417e+02],
       [  2.50626566e-01,   6.42357435e+02],
       [  1.98807157e-01,   7.08761964e+02],
       [  1.57977883e-01,   7.47889452e+02],
       [  1.25470514e-01,   7.69065090e+02],
       [  9.96015936e-02,   7.63997573e+02],
       [  7.91139241e-02,   7.59970418e+02],
       [  6.28535512e-02,   7.57004897e+02],
       [  4.99001996e-02,   7.37778704e+02],
       [  3.96353547e-02,   7.01687717e+02],
       [  3.14762354e-02,   6.69178570e+02],
       [  2.50000000e-02,   6.15720833e+02],
       [  1.01010101e-02,   4.32471932e+02]]).T

# Mw=4.0, Rrup=10.0, Depth=5.0
test_data['Allen_2012_test_accelM40R10D5'] = array([
       [  1.00000000e+01,   8.76025644e-03],
       [  7.69230769e+00,   1.36157319e-02],
       [  6.25000000e+00,   2.05969649e-02],
       [  5.00000000e+00,   3.13416217e-02],
       [  4.00000000e+00,   4.90257257e-02],
       [  3.12500000e+00,   7.62014807e-02],
       [  2.50000000e+00,   1.16921261e-01],
       [  2.00000000e+00,   1.94171486e-01],
       [  1.58730159e+00,   3.29142269e-01],
       [  1.25000000e+00,   6.02708396e-01],
       [  1.00000000e+00,   1.02146388e+00],
       [  7.93650794e-01,   1.82509386e+00],
       [  6.28930818e-01,   3.22107157e+00],
       [  5.00000000e-01,   5.91068208e+00],
       [  3.96825397e-01,   9.78015872e+00],
       [  3.15457413e-01,   1.57556097e+01],
       [  2.50626566e-01,   2.26247003e+01],
       [  1.98807157e-01,   3.05432448e+01],
       [  1.57977883e-01,   3.87360327e+01],
       [  1.25470514e-01,   4.71816817e+01],
       [  9.96015936e-02,   5.32017467e+01],
       [  7.91139241e-02,   5.72309320e+01],
       [  6.28535512e-02,   5.58988667e+01],
       [  4.99001996e-02,   5.42193257e+01],
       [  3.96353547e-02,   5.44540345e+01],
       [  3.14762354e-02,   5.03220343e+01],
       [  2.50000000e-02,   4.43504113e+01],
       [  1.01010101e-02,   2.77779826e+01]]).T

# Mw=4.0, Rrup=100.0, Depth=10.0
test_data['Allen_2012_test_accelM40R100D10'] = array([
       [  1.00000000e+01,   3.57303511e-04],
       [  7.69230769e+00,   5.64864962e-04],
       [  6.25000000e+00,   8.92177302e-04],
       [  5.00000000e+00,   1.39951389e-03],
       [  4.00000000e+00,   2.23536983e-03],
       [  3.12500000e+00,   3.58048535e-03],
       [  2.50000000e+00,   5.78998367e-03],
       [  2.00000000e+00,   9.77159954e-03],
       [  1.58730159e+00,   1.64813790e-02],
       [  1.25000000e+00,   2.81247718e-02],
       [  1.00000000e+00,   5.06666407e-02],
       [  7.93650794e-01,   9.19990264e-02],
       [  6.28930818e-01,   1.65841654e-01],
       [  5.00000000e-01,   2.86953513e-01],
       [  3.96825397e-01,   4.96529320e-01],
       [  3.15457413e-01,   7.38705801e-01],
       [  2.50626566e-01,   1.04215322e+00],
       [  1.98807157e-01,   1.34379441e+00],
       [  1.57977883e-01,   1.63851928e+00],
       [  1.25470514e-01,   1.82760770e+00],
       [  9.96015936e-02,   1.95731534e+00],
       [  7.91139241e-02,   2.05134068e+00],
       [  6.28535512e-02,   2.07467257e+00],
       [  4.99001996e-02,   2.01245550e+00],
       [  3.96353547e-02,   1.98559203e+00],
       [  3.14762354e-02,   1.89444866e+00],
       [  2.50000000e-02,   1.80879832e+00],
       [  1.01010101e-02,   1.08474140e+00]]).T

# Mw=3.5, Rrup=10.0, Depth=5.0
test_data['Allen_2012_test_accelM35R10D5'] = array([
       [  1.00000000e+01,   2.35850109e-03],
       [  7.69230769e+00,   3.50860825e-03],
       [  6.25000000e+00,   5.12671518e-03],
       [  5.00000000e+00,   7.42728857e-03],
       [  4.00000000e+00,   1.08945428e-02],
       [  3.12500000e+00,   1.58873455e-02],
       [  2.50000000e+00,   2.25891127e-02],
       [  2.00000000e+00,   3.58903099e-02],
       [  1.58730159e+00,   5.95794881e-02],
       [  1.25000000e+00,   1.11787967e-01],
       [  1.00000000e+00,   1.93867034e-01],
       [  7.93650794e-01,   3.68557637e-01],
       [  6.28930818e-01,   7.11549364e-01],
       [  5.00000000e-01,   1.45001486e+00],
       [  3.96825397e-01,   2.67184143e+00],
       [  3.15457413e-01,   4.88424109e+00],
       [  2.50626566e-01,   7.86584454e+00],
       [  1.98807157e-01,   1.15671640e+01],
       [  1.57977883e-01,   1.59903638e+01],
       [  1.25470514e-01,   2.05857800e+01],
       [  9.96015936e-02,   2.42251418e+01],
       [  7.91139241e-02,   2.65414745e+01],
       [  6.28535512e-02,   2.57466939e+01],
       [  4.99001996e-02,   2.45432952e+01],
       [  3.96353547e-02,   2.46291788e+01],
       [  3.14762354e-02,   2.20507363e+01],
       [  2.50000000e-02,   1.88400261e+01],
       [  1.01010101e-02,   1.15198269e+01]]).T

# Mw=3.5, Rrup=100.0, Depth=5.0
test_data['Allen_2012_test_accelM35R100D5'] = array([
       [  1.00000000e+01,   6.95452881e-05],
       [  7.69230769e+00,   1.06717456e-04],
       [  6.25000000e+00,   1.61313860e-04],
       [  5.00000000e+00,   2.51852546e-04],
       [  4.00000000e+00,   3.76900324e-04],
       [  3.12500000e+00,   5.79984970e-04],
       [  2.50000000e+00,   9.05464041e-04],
       [  2.00000000e+00,   1.44183094e-03],
       [  1.58730159e+00,   2.50760594e-03],
       [  1.25000000e+00,   4.44530587e-03],
       [  1.00000000e+00,   8.54937272e-03],
       [  7.93650794e-01,   1.65705433e-02],
       [  6.28930818e-01,   3.23929949e-02],
       [  5.00000000e-01,   6.12626765e-02],
       [  3.96825397e-01,   1.16068646e-01],
       [  3.15457413e-01,   1.87141062e-01],
       [  2.50626566e-01,   2.78622181e-01],
       [  1.98807157e-01,   3.83051225e-01],
       [  1.57977883e-01,   4.81335010e-01],
       [  1.25470514e-01,   5.47146291e-01],
       [  9.96015936e-02,   5.72657582e-01],
       [  7.91139241e-02,   5.75707587e-01],
       [  6.28535512e-02,   5.61966421e-01],
       [  4.99001996e-02,   5.15351417e-01],
       [  3.96353547e-02,   4.54216570e-01],
       [  3.14762354e-02,   3.93308612e-01],
       [  2.50000000e-02,   3.49050096e-01],
       [  1.01010101e-02,   2.27648385e-01]]).T
       
test_data['Allen_2012_test_sigma_shallow'] = array([
       [ 0.35533697,  0.35624902,  0.35704694,  0.35764279,  0.35845709,
         0.35903936,  0.35960383,  0.36082654,  0.36312035,  0.36584991,
         0.36863937,  0.37079451,  0.37364418,  0.37600683,  0.3777093 ,
         0.378327  ,  0.37920497,  0.38020318,  0.38116609,  0.38355871,
         0.38571442,  0.39112994,  0.39686384,  0.40510136,  0.41515827,
         0.42695297,  0.43836117,  0.41269879]])

test_data['Allen_2012_test_sigma_deep'] = array([
       [ 0.3349771 ,  0.33443175,  0.33432986,  0.33387799,  0.33420823,
         0.33430223,  0.33533873,  0.33655017,  0.33789837,  0.33902168,
         0.3406606 ,  0.34240618,  0.34414659,  0.34721318,  0.34809836,
         0.34886661,  0.34981217,  0.35037704,  0.35281502,  0.35564235,
         0.35967277,  0.36537822,  0.3730547 ,  0.38384394,  0.39650681,
         0.41076258,  0.42518372,  0.39635169]])

# DB:
# In each array the first column has the period in seconds and the second has 
# the corresponding response spectral period in cm/s^2.

# Period
test_data['Allen_2012_test_period'] = \
    test_data['Allen_2012_test_accelM60R100D5'][0]

# Mean
tmp = zeros((12, 28)) 
tmp[0,:] =  test_data['Allen_2012_test_accelM60R100D5'][1]
tmp[1,:] =  test_data['Allen_2012_test_accelM40R100D5'][1]
tmp[2,:] =  test_data['Allen_2012_test_accelM35R100D10'][1]
tmp[3,:] =  test_data['Allen_2012_test_accelM35R10D10'][1]
tmp[4,:] =  test_data['Allen_2012_test_accelM40R10D10'][1]
tmp[5,:] =  test_data['Allen_2012_test_accelM60R10D5'][1]
tmp[6,:] =  test_data['Allen_2012_test_accelM60R100D10'][1]
tmp[7,:] =  test_data['Allen_2012_test_accelM60R10D10'][1]
tmp[8,:] =  test_data['Allen_2012_test_accelM40R10D5'][1]
tmp[9,:] =  test_data['Allen_2012_test_accelM40R100D10'][1]
tmp[10,:] = test_data['Allen_2012_test_accelM35R10D5'][1]
tmp[11,:] = test_data['Allen_2012_test_accelM35R100D5'][1]
test_data['Allen_2012_test_mean'] = tmp
del tmp

# Sigma
tmp = zeros((12, 28))
tmp[0,:] =  test_data['Allen_2012_test_sigma_shallow'] # accelM60R100D5
tmp[1,:] =  test_data['Allen_2012_test_sigma_shallow'] # accelM40R100D5
tmp[2,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM35R100D10
tmp[3,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM35R10D10
tmp[4,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM40R10D10
tmp[5,:] =  test_data['Allen_2012_test_sigma_shallow'] # accelM60R10D5
tmp[6,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM60R100D10
tmp[7,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM60R10D10
tmp[8,:] =  test_data['Allen_2012_test_sigma_shallow'] # accelM40R10D5
tmp[9,:] =  test_data['Allen_2012_test_sigma_deep']    # accelM40R100D10
tmp[10,:] = test_data['Allen_2012_test_sigma_shallow'] # accelM35R10D5
tmp[11,:] = test_data['Allen_2012_test_sigma_shallow'] # accelM35R100D5
test_data['Allen_2012_test_sigma'] = tmp
del tmp
    
# Mw
test_data['Allen_2012_test_magnitude'] = [6.0,   # accelM60R100D5
                                          4.0,   # accelM40R100D5
                                          3.5,   # accelM35R100D10
                                          3.5,   # accelM35R10D10
                                          4.0,   # accelM40R10D10
                                          6.0,   # accelM60R10D5
                                          6.0,   # accelM60R100D10
                                          6.0,   # accelM60R10D10
                                          4.0,   # accelM40R10D5
                                          4.0,   # accelM40R100D10
                                          3.5,   # accelM35R10D5
                                          3.5]   # accelM35R100D5

# Rrup
test_data['Allen_2012_test_distance'] = [[100.0, # accelM60R100D5
                                          100.0, # accelM40R100D5
                                          100.0, # accelM35R100D10
                                          10.0,  # accelM35R10D10
                                          10.0,  # accelM40R10D10
                                          10.0,  # accelM60R10D5
                                          100.0, # accelM60R100D10
                                          10.0,  # accelM60R10D10
                                          10.0,  # accelM40R10D5
                                          100.0, # accelM40R100D10
                                          10.0,  # accelM35R10D5
                                          100.0]]# accelM35R100D5

# Depth
test_data['Allen_2012_test_depth'] =     [5.0,   # accelM60R100D5
                                          5.0,   # accelM40R100D5
                                          10.0,  # accelM35R100D10
                                          10.0,  # accelM35R10D10
                                          10.0,  # accelM40R10D10
                                          5.0,   # accelM60R10D5
                                          10.0,  # accelM60R100D10
                                          10.0,  # accelM60R10D10
                                          5.0,   # accelM40R10D5
                                          10.0,  # accelM40R100D10
                                          5.0,   # accelM35R10D5
                                          5.0]   # accelM35R100D5

#***************  END ALLEN 2012 MODEL  ***********************

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
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)
