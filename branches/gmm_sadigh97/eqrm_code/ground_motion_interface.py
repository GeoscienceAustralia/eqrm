"""
Title: ground_motion_interface.py
                                                       
Version: $Revision: 1672 $  
ModifiedBy: $Author: dgray $
ModifiedDate: $Date: 2010-05-12 16:14:00 +1000 (Wed, 12 May 2010) $
  
Copyright 2007 by Geoscience Australia
Author:  Peter Row, peter.row@ga.gov.au
         Duncan Gray, duncan.gray@ga.gov.au
           
Description: 
    This is where ground motion models are defined.

    The heart of this module are the distribution functions for each model
    which calculate the level of motion observed at a distance from an event
    given a event magnitude and depth.  The level of motion is defined as
    the natural logarithm of the response spectral acceleration (RSA), in
    units of 'g'. 

    The data required to calculate the ground motion (coefficients, constants,
    etc) is placed into a list which is stored in a dictionary
    'ground_motion_init' (sic) with the model name as key.

    Each dictionary list contains (in the following order):
        distribution function
            reference to the actual function to get RSA log mean and log sigma.
        magnitude_type
            string describing the magnitude value used in the distribution
            function - currently 'Mw' and 'ML' are the only options.
        distance_type
            string determining how distance is measured - this is actually the
            name of a distance *function* in distance_functions.py.
        coefficient
            a reference to an array of model coefficients with shape of
            (num_coefficients, num_periods).  'num_coefficients' may vary from
            model to model.
        coefficient_period
            an array of shape (num_periods,) holding the reference periods at
            which the ground motion model coefficients are defined.
        coefficient_interpolation function
            a reference to a function used to interpolate coefficient values
            for periods not in 'coefficient_period'.  Called:
                interpolate(new_period, coefficient, old_period)
        sigmacoefficient
            a reference to an array of model coefficients used to determine
            sigma values - has a shape of (num_sigmacoefficients, num_periods).

            to avoid the interpolation crashing, define for more than one
            period.  For example, if the sigma coefficient is a constant use
            the same repeated value (1.2, 1.2) over an arbitrary period (0, 1).
            See below for an example.
        sigmacoefficient_period
            an array of shape (num_periods,) holding the reference periods at
            which the ground motion model sigma coefficients are defined.
        sigmacoefficient_interpolation function
            a reference to a function used to interpolate sigma coefficient
            values for periods not in 'sigmacoefficient_period'.  Called:
                interpolate(new_period, sigmacoefficient, old_period)

    Note: the list contents shapes mentioned above are *not* the shapes seen
          for this data in the actual distribution function.  See below for
          discussion on that matter.


    distribution function parameters
    --------------------------------
        Each distribution function is called:
            distribution_function(**kwargs)
        where the 'kwargs' is a dictionary containing keyword parameters, such
        as:
            periods           periods of interest
            mag               event magnitude
            dip               fault dip
            depth             depth of the event
            depth_to_top      depth to top of rupture (Ztor)
            width             rupture width
            fault_type        type of fault
            distance          distance of the site from the event (deprecated)
            dist_object       a distance object, attributes are distances,
                              eg:  Rjb = dist_object.Joyner_Boore
            Vs30              shear wave velocity at 30m
            coefficient       an array of model coefficients
            sigmacoefficient  an array of model sigma coefficients

        The shapes of each parameter are:
            periods              (periods,)
            mag                  (sites, events, 1)
            dip                  (sites, events, 1)
            depth                (sites, events, 1)
            depth_to_top         (sites, events, 1)
            width                (sites, events, 1)
            fault_type           (sites, events, 1)
            distance             (sites, events, 1)   
            dist_object.Rupture  (sites, events)      (etc)
            Vs30                 (sites,)
            coefficient          (coefficients, 1, 1, periods)
            sigmacoefficient     (sigmacoefficients, 1, 1, periods)

        The shapes of the returned arrays are:
            log_mean             (sites, events, periods)
            log_sigma            (sites, events, periods)

        Note that the 'sites' dimension above is the number of sites passed to
        the model code and is currently 1.  You should not confuse this with the
        actual number of sites being processed by EQRM.
"""

import math
from copy import  deepcopy
from scipy import where, sqrt, array, asarray, exp, log, newaxis, zeros, \
                  log10, isfinite, weave, ones, shape, reshape, concatenate, \
                  tanh, cosh, power, shape, tile, cos, pi, copy, resize, \
                  logical_and, logical_or, sum, minimum, maximum, ones_like, \
                  seterr, allclose
 
from eqrm_code.ground_motion_misc import linear_interpolation, \
                                         Australian_standard_model, \
                                         Australian_standard_model_interpolation
from eqrm_code import util 
from eqrm_code import conversions
from eqrm_code import ground_motion_misc
from eqrm_code import weave_converters

# Note, this is covering up, in Abrahamson08_distribution, Ztor being 0,
# causing divide by 0 errors.  It may be covering up other things.
# This is to suppress warnings in Windows.
#seterr(divide='ignore')


LOG10E = math.log10(math.e)
BEDROCKVs30 = array([760.]) # m/s

# A dictionary of all the info specified bellow.  This is used by
# ground_motion_specification.  Each entry is a list, which gets
# passed as *args to
# ground_motion_specification._set_interface_values()


# FIXME Refactor this module and incorporate the functionality of
# ground_motion_specification.  ground_motion_init[] elements should
# be classes (with class methods) or instances instead of a list so we
# can just say whataver =
# ground_motion_init[model_name].method(event_and_site_args) . The
# classes should inherit from a base class that has methods for
# interpolating the coefficients (currently done in
# ground_motion_specification) and then the coefficients can be class
# attributes.

ground_motion_init = {}

#***************  START OF ALLEN MODEL  ****************************

Allen_coefficient_period=[ 10.,5. ,3.003 , 2. ,   1.6   ,   1.,
         0.7502,   0.5   ,   0.4   ,   0.3   ,   0.24  ,   0.2   ,
         0.16  ,   0.15  ,   0.12  ,   0.1   ,   0.08  ,   0.07  ,
         0.06  ,   0.055 ,   0.05  ,   0.04  ,   0.0323,   0.025 ,
         0.02  ,   0.01  ]
Allen_coefficient=[
    [-21.8702, -18.3005, -15.225 , -12.7432, -11.4433,  -8.5082,
     -6.7579,  -4.4525,  -3.3069,  -1.8805,  -0.8188,   0.1416,
     1.0249,   1.205 ,   1.9958,   2.3232,   2.3007,   2.1033,
     1.6085,   1.348 ,   1.0695,   0.4338,   0.0729,  -0.3766,
     -0.5665,  -0.7655],
    [  2.8736,   2.6008,   2.3016,   2.0264,   1.8696,   1.5271,
       1.3317,   1.0786,   0.9523,   0.8122,   0.7134,   0.6282,
       0.5411,   0.5212,   0.436 ,   0.3878,   0.3603,   0.3595,
       0.38  ,   0.3908,   0.4033,   0.4371,   0.4605,   0.4954,
       0.5118,   0.5302],
    [-11.    , -10.    ,  -9.7   ,  -9.2   ,  -8.4   ,  -0.7   ,
     0.2   ,   0.9   ,   1.2   ,   1.5   ,   1.7   ,   1.9   ,
     2.    ,   2.    ,   2.1   ,   2.1   ,   2.    ,   1.9   ,
     1.7   ,   1.6   ,   1.5   ,   1.3   ,   1.3   ,   1.2   ,
     1.2   ,   1.2   ],
    [ -1.0306,  -1.0884,  -1.1887,  -1.2996,  -1.3656,  -1.5514,
      -1.6958,  -1.921 ,  -2.0661,  -2.2576,  -2.4222,  -2.5899,
      -2.7617,  -2.8002,  -2.9774,  -3.0705,  -3.1098,  -3.0987,
      -3.0347,  -3.0013,  -2.9643,  -2.8732,  -2.8224,  -2.7489,
      -2.7181,  -2.6852],
    [  0.0222,   0.0239,   0.0325,   0.0433,   0.0496,   0.0665,
       0.0789,   0.0967,   0.1081,   0.1221,   0.1343,   0.1471,
       0.1618,   0.1655,   0.1826,   0.1937,   0.2021,   0.2044,
       0.2029,   0.2023,   0.2013,   0.1977,   0.1952,   0.1899,
       0.1874,   0.1845],
    [ -0.24  ,  -0.365 ,  -0.4074,  -0.4016,  -0.385 ,  -0.3224,
      -0.2778,  -0.214 ,  -0.1844,  -0.1517,  -0.132 ,  -0.1197,
      -0.109 ,  -0.1067,  -0.1015,  -0.0999,  -0.1007,  -0.1022,
      -0.1049,  -0.1067,  -0.1087,  -0.1136,  -0.1182,  -0.1217,
      -0.1235,  -0.1255]
    ]
Allen_sigma_coefficient_period=deepcopy(Allen_coefficient_period)
Allen_sigma_coefficient=[
    [ 1.2756,  1.1358,  0.9711,  0.8642,  0.7764,  0.6627,  0.6599,
             0.5899,  0.5648,  0.557 ,  0.533 ,  0.5208,  0.5101,  0.5114,
             0.5184,  0.4997,  0.489 ,  0.4884,  0.4918,  0.4851,  0.4891,
             0.4847,  0.4793,  0.4742,  0.4768,  0.4774],
           [ 0.235 ,  0.258 ,  0.2739,  0.2938,  0.3074,  0.3373,  0.3546,
             0.3832,  0.4015,  0.4298,  0.456 ,  0.4786,  0.4996,  0.5064,
             0.5219,  0.5327,  0.5211,  0.5074,  0.4848,  0.4696,  0.4574,
             0.4525,  0.4547,  0.4482,  0.4429,  0.4404]]

Allen_interpolation=linear_interpolation

def Allen_distribution(**kwargs):

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    events = distance.shape[1]
    
    num_periods=coefficient.shape[3]
    assert coefficient.shape==(6,1,1,num_periods)
    assert sigma_coefficient.shape==(2,1,1,num_periods)
    c1,c2,c4,c6,c7,c10=coefficient
    model_sigma,regression_sigma=sigma_coefficient
    log_mean=c1+c2*mag+log((distance+exp(c4))**(c6+c7*mag))+c10*(mag-6.0)**2
    log_sigma = tile(model_sigma+regression_sigma,(1,events,1))
    return log_mean,log_sigma


Allen_magnitude_type='Mw'
Allen_distance_type='Hypocentral'

Allen_uses_Vs30 = False

Allen_args=[
    Allen_distribution,
    Allen_magnitude_type,
    Allen_distance_type,
    
    Allen_coefficient,
    Allen_coefficient_period,
    Allen_interpolation,
    
    Allen_sigma_coefficient,
    Allen_sigma_coefficient_period,
    Allen_interpolation,

    Allen_uses_Vs30]

ground_motion_init['Allen'] = Allen_args

#***************  END OF ALLEN MODEL  ****************************

#***************  START OF Gaull 1990 WA MODEL  ****************************

Gaull_1990_WA_magnitude_type='ML'
Gaull_1990_WA_distance_type='Rupture'
#Gaull_1990_WA_coefficient=[log(0.025),1.10,1.03,log(9.8)]
# log(0.025) - log(9.8) = -5.9712618397904631
# Previously coefficient d was used to convert the results from
# m/s2 to g.  In this version coefficient a and d have been rolled
# into one value
# showing a lot of significant figures so the scenario tests pass
Gaull_1990_WA_coefficient=[-5.971261839790,1.10,1.03]
Gaull_1990_WA_coefficient_period=[0.0]
Gaull_1990_WA_sigma_coefficient=[[0.28,0.28],[0.28,0.28]]
Gaull_1990_WA_sigma_coefficient_period=[0.0,1.0]

def Gaull_1990_WA_distribution(**kwargs):    
    """
    This eq is eq(5.6) from the EQRM tech manual.
    """
    
    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    num_periods = coefficient.shape[3]
    events = distance.shape[1]
    assert coefficient.shape==(3,1,1,num_periods)
    assert sigma_coefficient.shape==(2,1,1,num_periods)
    # mag.shape (site, events, 1)
    # distance.shape (site, events, 1)
    
    a,b,c = coefficient
    log_sigma = tile(sigma_coefficient[0],(1,events,1))
    log_mean = a+b*mag-c*log(distance)
    return log_mean, log_sigma


def Gaull_1990_WA_coefficient_interpolation(new_period,c,old_period):
    """
    Gaull isn't interpolated, it is scaled to the Australian standard model.

    Note that a is the only coefficient scaled. Scaling the other ones
    doesn't make sense - the linear form of Gaull is:
        exp(a) * exp(b*mag) * distance**(-c) / g

    So to achieve linear scaling (in the real world), exp(a) is scaled
    by the ASM, and everything else is kept constant.
    
    
    input: c=[a,b,c,d]
    output: c=[new_a_array,b_array,c_array,d_array]

    # old_period are the known period values on the coefficient curve.
    # new_period are the period values where coefficient values are needed.
    # (More accurate terms?)
    
    This function/method has attributes of c values associated with
    period (old period) values.  Give it new period values it will
    determine new c values.
    
    """
    a,b,c=c

    # put log_space a into the real world
    a=exp(a)
    
    new_a=Australian_standard_model_interpolation(new_period,a,old_period)
    # scale it to the ASM
    
    new_a=log(new_a)
    # bring it back to log space
    
    # resize the other coefficients to match the new a
    new_b=b+new_a*0
    new_c=c+new_a*0
    return asarray([new_a,new_b,new_c])
    
Gaull_1990_WA_sigma_coefficient_interpolation=linear_interpolation

Gaull_1990_WA_uses_Vs30 = False

Gaull_1990_WA_args=[
    Gaull_1990_WA_distribution,
    Gaull_1990_WA_magnitude_type,
    Gaull_1990_WA_distance_type,
    
    Gaull_1990_WA_coefficient,
    Gaull_1990_WA_coefficient_period,
    Gaull_1990_WA_coefficient_interpolation,
    
    Gaull_1990_WA_sigma_coefficient,
    Gaull_1990_WA_sigma_coefficient_period,
    Gaull_1990_WA_sigma_coefficient_interpolation,

    Gaull_1990_WA_uses_Vs30]

ground_motion_init['Gaull_1990_WA'] = Gaull_1990_WA_args

#***************  End of Gaull 1990 WA MODEL  ****************************

#***************  Start of Toro_1997_midcontinent MODEL  ******************

Toro_1997_midcontinent_coefficient=[
    [  2.20000000e+00, 2.20000000e+00, 4.00000000e+00, 3.68000000e+00,
              2.37000000e+00,   1.73000000e+00,   1.07000000e+00,
              9.00000000e-02,  -7.40000000e-01,  -3.23000000e+00],
           [  8.10000000e-01,  8.10000000e-01, 7.90000000e-01, 8.00000000e-01,
              8.10000000e-01,   8.40000000e-01,   1.05000000e+00,
              1.42000000e+00,   1.86000000e+00,   3.18000000e+00],
           [  0.00000000e+00, 0.00000000e+00,  0.00000000e+00, 0.00000000e+00,
              0.00000000e+00,   0.00000000e+00,  -1.00000000e-01,
              -2.00000000e-01,  -3.10000000e-01,  -6.40000000e-01],
           [  1.27000000e+00, 1.27000000e+00, 1.57000000e+00, 1.46000000e+00,
              1.10000000e+00,   9.80000000e-01,   9.30000000e-01,
              9.00000000e-01,   9.20000000e-01,   9.80000000e-01],
           [  1.16000000e+00,  1.16000000e+00, 1.83000000e+00, 1.77000000e+00,
              1.02000000e+00,   6.60000000e-01,   5.60000000e-01,
              4.90000000e-01,   4.60000000e-01,   3.70000000e-01],
           [  2.10000000e-03, 2.10000000e-03,   8.00000000e-04, 1.30000000e-03,
              4.00000000e-03,   4.20000000e-03,   3.30000000e-03,
              2.30000000e-03,   1.70000000e-03,  -1.00000000e-04],
           [  9.30000000e+00,   9.30000000e+00, 1.11000000e+01,  .05000000e+01,
              8.30000000e+00,   7.50000000e+00,   7.10000000e+00,
              6.80000000e+00,   6.90000000e+00,   7.20000000e+00]]

Toro_1997_midcontinent_coefficient_period=[
    0.00000000e+00,   0.02,2.85000000e-02,   4.00000000e-02,
             1.00000000e-01,   2.00000000e-01,   4.00000000e-01,
             1.00000000e+00,   2.00000000e+00,   5.00000000e+00]

Toro_1997_midcontinent_sigma_coefficient = [
    [0.55, 0.55, 0.62, 0.62, 0.59, 0.60, 0.63, 0.63, 0.61, 0.61],
           [0.59,0.59, 0.63, 0.63, 0.61, 0.64, 0.68, 0.64, 0.62, 0.62],
           [0.50, 0.50, 0.50, 0.50, 0.50, 0.56, 0.64, 0.67, 0.66, 0.66],
           [0.54, 0.54, 0.62, 0.57, 0.50, 0.45, 0.45, 0.45, 0.45, 0.45],
           [0.20, 0.20, 0.35, 0.29, 0.17, 0.12, 0.12, 0.12, 0.12, 0.12],
           [0.36,0.36,0.36,0.36,0.36,0.36,0.36,0.35,0.34,0.34],
           [0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.65,0.6,0.6]]

Toro_1997_midcontinent_sigma_coefficient_period = [
    0, 0.02, 1.0/35, 0.04, 0.1, 0.2, 0.4, 1, 2, 10]

    #Tref = [0 1/35, 0.04, 0.1 0.2 0.4 1 2 10];
    #origd1 = [0.55 0.62 0.62 0.59 0.60 0.63 0.63 0.61 0.61];
    #origd2 = [0.59 0.63 0.63 0.61 0.64 0.68 0.64 0.62 0.62];
    #origd3 = [0.50 0.50 0.50 0.50 0.56 0.64 0.67 0.66 0.66];

    #Tref = [0 1/35 0.04, 0.1 0.2 0.4 1 2 10];
    #origf1 = [0.54 0.62 0.57 0.50 0.45 0.45 0.45 0.45 0.45];
    #origf2 = [0.20 0.35 0.29 0.17 0.12 0.12 0.12 0.12 0.12];

    #epistemic1 = [0.36,0.36,0.36,0.36,0.36,0.36,0.35,0.34,0.34]
    #epistemic2 = [0.7,0.7,0.7,0.7,0.7,0.7,0.65,0.6,0.6]

def Toro_1997_midcontinent_distribution_python(**kwargs):
    """The usual parameters passed are:
        mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    """

    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    (num_sites, num_events) = distance.shape[0:2]
    num_periods = coefficient.shape[3]

    assert coefficient.shape == (7,1,1,num_periods)
    assert mag.shape == (1,num_events,1)
    assert distance.shape == (num_sites,num_events,1)

    (c1, c2, c3, c4, c5, c6, c7) = coefficient
    (d1, d2, d3, f1, f2, e1, e2) = sigma_coefficient
    
    Rm = sqrt(distance**2 + c7**2)
    log_Rm = log(Rm)
    log_100 = 4.60517018599 
    log_mean = (c1 + c2*(mag-6.0) + c3*((mag-6.0)**2) - c4*log_Rm -
                (c5-c4)*where((log_Rm-log_100)>0, (log_Rm-log_100), 0) - c6*Rm)
    del log_Rm, log_100, Rm

    log_sigma_aleatory1 = ((mag <= 5)*d1 +(5 < mag)*(mag <= 5.5)*(d1 +
                           (d2-d1)*(mag-5)/0.5) +
                           (5.5 < mag)*(mag <= 8)*(d2 + (d3-d2)*(mag-5.5)/2.5) +
                           (8 < mag)*d3)

    # getting the aleatory (mag part) sigma
    log_sigma_aleatory2 = ((distance <= 5)*f1 +
                           (5 < distance)*(distance <= 20)*(f1+(f2-f1)*(distance-5)/15) +
                           (20 < distance)*f2)

    log_sigma = sqrt(log_sigma_aleatory1**2 + log_sigma_aleatory2**2)

    return (log_mean, log_sigma)

def Toro_1997_midcontinent_distribution(**kwargs):
    """The usual parameters passed are:
        mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    """

    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    (num_sites, num_events) = distance.shape[0:2]
    num_periods = coefficient.shape[3]

    assert coefficient.shape == (7,1,1,num_periods)
    #assert sigma_coefficient.shape==(7,1,1,num_periods)
    assert mag.shape == (1,num_events,1)
    assert distance.shape == (num_sites,num_events,1)

    log_mean = zeros((num_sites,num_events,num_periods), dtype=float)
    log_sigma = zeros((num_sites,num_events,num_periods), dtype=float)

    coefficient = coefficient[:,0,0,:]
    sigma_coefficient = sigma_coefficient[:,0,0,:]
    mag = mag[0,:,0]
    distance = distance[:,:,0]
    
    code = """
    double c1, c2, c3, c4, c5, c6, c7;
    double d1, d2, d3, f1, f2, e1, e2;
    double m, d;
    double Rm,log_Rm, log_Rm_100, log_100;
    double sig_1, sig_2;

    for (int i=0; i < num_sites; ++i) {
        for (int j=0; j < num_events; ++j) {
            m = mag(j);
            d = distance(i, j);
            
            for (int k=0; k < num_periods; ++k) {
                c1 = coefficient(0, k);
                c2 = coefficient(1, k);
                c3 = coefficient(2, k);
                c4 = coefficient(3, k);
                c5 = coefficient(4, k);
                c6 = coefficient(5, k);
                c7 = coefficient(6, k);
                
                Rm = sqrt(d*d + c7*c7);
                log_Rm = log(Rm);
                log_100 = 4.6051701859880918; /* log(100) */
                log_Rm_100 = log_Rm - log_100;

                if (log_Rm_100 < 0.0)
                    log_Rm_100 = 0.0;

                log_mean(i, j, k) = c1 + c2*(m-6.0) + c3*((m-6.0)*(m-6.0))
                                       - c4*log_Rm - (c5-c4)*log_Rm_100-c6*Rm;

                d1 = sigma_coefficient(0, k);
                d2 = sigma_coefficient(1, k);
                d3 = sigma_coefficient(2, k);
                f1 = sigma_coefficient(3, k);
                f2 = sigma_coefficient(4, k);
                e1 = sigma_coefficient(5, k);
                e2 = sigma_coefficient(6, k);

                sig_1 = (m <= 5)*d1 +
                            (5 < m)*(m <= 5.5)*(d1 + (d2-d1)*(m-5)/0.5) +
                            (5.5 < m)*(m <= 8)*(d2 + (d3-d2)*(m-5.5)/2.5) +
                            (8 < m)*d3;
                sig_2 = (d <= 5)*f1 +
                            (5 < d)*(d <= 20)*(f1 + (f2-f1)*(d-5)/15) +
                            (20 < d)*f2;
                log_sigma(i, j, k) = sqrt(sig_1*sig_1 + sig_2*sig_2);
            }       
        }
    }

    return_val = 0;
    """

    try:
        weave.inline(code,
                     ['num_sites', 'num_events', 'num_periods',
                      'coefficient', 'sigma_coefficient',
                      'mag', 'log_mean', 'distance', 'log_sigma'],
                     type_converters=weave_converters.eqrm,
                     compiler='gcc')   
    except IOError:
        raise util.WeaveIOError 
    
    return (log_mean, log_sigma)

Toro_1997_midcontinent_magnitude_type='Mw'
Toro_1997_midcontinent_distance_type='Joyner_Boore'

Toro_1997_midcontinent_interpolation=linear_interpolation
Toro_1997_midcontinent_sigma_coefficient_interpolation=linear_interpolation

Toro_1997_midcontinent_test_distance=[[17.004,187.14],
                                            [1.5291,168.8]]
# temp - CHANGED 6.69 to 4.59...
Toro_1997_midcontinent_test_magnitude=[6.59694563,4.78866307]

Toro_1997_midcontinent_test_period=[0.0,1.0]
Toro_1997_midcontinent_test_mean=[[[ 0.32568276,  0.16652828],
                                         [ 0.00317764,  0.00110675]],
                                        [[ 0.83083585,  0.40776479],
                                         [ 0.00372073,  0.00121415]]]

# temp - CHANGED 6.69 to 4.59...
#I get:
#[[[ 0.0644522   0.00704784]
#  [ 0.00317764  0.00110675]]
# [[ 0.16442134  0.0172575 ]
#  [ 0.00372073  0.00121415]]]
#XLS gets:
#[[[0.06445220  0.00704784]
#  [0.00276765  0.00066167]]
# [[0.16442134  0.01725750]
#  [0.00331483  0.00078984]]]

# temp - CHANGED 6.69 to 2.59...
#I get:
#[[[  1.27550056e-02   6.02217426e-05]
# [[  3.25387683e-02   1.47460272e-04]
#XLS gets:
#[[[0.01275501  0.00006022]
# [[0.03253877  0.00014746]

# temp - CHANGED 6.69 to 0.59...
#I get:
#[[[  2.52419901e-03   1.03891309e-07]
# [[  6.43937992e-03   2.54390524e-07]
#XLS gets:
#[[[2.524199E-03  1.038913E-07]
# [[6.439380E-03  2.543905E-07]


# In other words, I am accurate for low distances, but not high ones.


# Note:
# for ground motions:
#   period0,period1
# [[[m0s0p0,m0s0p1]   magnitude0  site0
#   [m1s0p0,m1s0p1]]  magnitude1  site0
#  [[m0s1p0,m1s1p1]   magnitude0  site1
#   [m1s1p0,m1s1p1]]] magnitude1  site1

# for distances:
# event0 event1
# [[] ,   [], site0
#  [] ,   []] site1

# I get:
# [[[ 0.32568276  0.16652828]
#   [ 0.00317764  0.00110675]]
#  [[ 0.83083585  0.40776479]
#   [ 0.00372073  0.00121415]]]


# Matlab gets:
#[[[  3.37250000e-01   1.75160000e-01]
#  [  2.53560000e-03   6.40940000e-04]]
#
# [[  8.60320000e-01   4.28880000e-01]
#  [  2.96880000e-03   7.03120000e-04]]]

# IASPIE - Campbell Workbook.xls gets:
#[[[0.32568276  0.16652828]
#  [0.00276765  0.00066167]]
# [[0.83083586  0.40776479]
#  [0.00331483  0.00078984]]]

#Changed XLS: No change
#[[[0.32568276    0.16652828]
#  [2.767647E-03  6.616664E-04]]
# [[0.83083586    0.40776479]
#  [3.314829E-03  7.898408E-04]]]

Toro_1997_midcontinent_uses_Vs30 = False

Toro_1997_midcontinent_args=[
    Toro_1997_midcontinent_distribution,
    Toro_1997_midcontinent_magnitude_type,
    Toro_1997_midcontinent_distance_type,
    
    Toro_1997_midcontinent_coefficient,
    Toro_1997_midcontinent_coefficient_period,
    Toro_1997_midcontinent_interpolation,
    
    Toro_1997_midcontinent_sigma_coefficient,
    Toro_1997_midcontinent_coefficient_period,
    Toro_1997_midcontinent_sigma_coefficient_interpolation,

    Toro_1997_midcontinent_uses_Vs30]

ground_motion_init['Toro_1997_midcontinent'] = Toro_1997_midcontinent_args

#***************  End of Toro_1997_midcontinent MODEL  ******************

#***************  Start of AllenSEA06 MODEL  ******************

AllenSEA06_coefficient_period=[
    0.     ,   0.025  ,   0.03148,   0.03964,   0.0499 ,   0.06285,
    0.07911,   0.0996 ,   0.1255 ,   0.158  ,   0.1988 ,   0.2506 ,
    0.3155 ,   0.3968 ,   0.5    ,   0.6289 ,   0.7937 ,   1.     ,
    1.25   ,   1.587  ,   2.     ,   2.5    ,   3.125  ,   4.     ,
    5.     ,   6.25   ,   7.692  ,  10.     ]

AllenSEA06_coefficient=[
    [-1.301  , -0.7679 , -0.632  , -0.5447 , -0.5376 , -0.6008 ,
            -0.7511 , -0.9949 , -1.361  , -1.92   , -2.496  , -3.17   ,
            -3.918  , -4.615  , -5.286  , -5.868  , -6.344  , -6.644  ,
            -6.845  , -6.89   , -6.809  , -6.61   , -6.38   , -6.143  ,
            -5.93   , -5.767  , -5.704  , -5.723  ],
           [ 1.076  ,  0.9752 ,  0.9465 ,  0.9274 ,  0.9256 ,  0.9415 ,
             0.975  ,  1.04   ,  1.134  ,  1.278  ,  1.427  ,  1.603  ,
             1.789  ,  1.956  ,  2.108  ,  2.223  ,  2.293  ,  2.307  ,
             2.281  ,  2.2    ,  2.078  ,  1.914  ,  1.742  ,  1.572  ,
             1.413  ,  1.279  ,  1.183  ,  1.118  ],
           [-0.07192, -0.06487, -0.06227, -0.0603 , -0.05961, -0.06025,
            -0.0621 , -0.06684, -0.07361, -0.08364, -0.09446, -0.1076 ,
            -0.1206 , -0.1323 , -0.1425 , -0.1498 , -0.1528 , -0.1516 ,
            -0.1465 , -0.1368 , -0.1243 , -0.1081 , -0.09157, -0.07562,
            -0.06099, -0.04897, -0.04048, -0.03476],
           [-1.683  , -1.772  , -1.748  , -1.704  , -1.643  , -1.583  ,
            -1.517  , -1.472  , -1.422  , -1.329  , -1.278  , -1.241  ,
            -1.186  , -1.161  , -1.147  , -1.157  , -1.171  , -1.216  ,
            -1.251  , -1.307  , -1.375  , -1.436  , -1.494  , -1.546  ,
            -1.591  , -1.632  , -1.657  , -1.669  ],
           [ 0.1527 ,  0.1575 ,  0.1523 ,  0.146  ,  0.1392 ,  0.1329 ,
             0.1274 ,  0.1248 ,  0.1222 ,  0.1134 ,  0.1114 ,  0.1111 ,
             0.1069 ,  0.1066 ,  0.1078 ,  0.1134 ,  0.1184 ,  0.1273 ,
             0.1339 ,  0.144  ,  0.1563 ,  0.1662 ,  0.1753 ,  0.1834 ,
         0.1901 ,  0.1962 ,  0.1991 ,  0.1997 ],
           [-3.452  , -3.619  , -3.788  , -4.014  , -4.267  , -4.379  ,
            -4.327  , -4.104  , -3.671  , -3.185  , -2.709  , -2.348  ,
            -2.083  , -1.869  , -1.76   , -1.597  , -1.489  , -1.478  ,
            -1.547  , -1.458  , -1.507  , -1.537  , -1.606  , -1.731  ,
        -1.837  , -1.913  , -1.99   , -2.034  ],
           [ 0.3054 ,  0.3251 ,  0.3455 ,  0.3705 ,  0.3958 ,  0.3967 ,
             0.3733 ,  0.3283 ,  0.2611 ,  0.1947 ,  0.1444 ,  0.1167 ,
             0.1008 ,  0.09321,  0.09447,  0.08727,  0.08609,  0.09615,
             0.1196 ,  0.1111 ,  0.1249 ,  0.1372 ,  0.1507 ,  0.1743 ,
             0.191  ,  0.2028 ,  0.2138 ,  0.2192 ],
           [ 1.24   ,  1.179  ,  1.218  ,  1.278  ,  1.332  ,  1.454  ,
             1.515  ,  1.449  ,  1.508  ,  1.432  ,  1.448  ,  1.583  ,
             1.747  ,  1.88   ,  1.812  ,  1.766  ,  1.753  ,  1.737  ,
             1.718  ,  1.747  ,  1.691  ,  1.66   ,  1.599  ,  1.53   ,
             1.482  ,  1.428  ,  1.39   ,  1.352  ],
           [-0.1626 , -0.1686 , -0.1779 , -0.184  , -0.1901 , -0.2007 ,
            -0.2082 , -0.1913 , -0.1958 , -0.1728 , -0.1714 , -0.1895 ,
            -0.2109 , -0.2283 , -0.2172 , -0.2065 , -0.1999 , -0.1942 ,
            -0.1925 , -0.1999 , -0.1902 , -0.1847 , -0.1754 , -0.1642 ,
            -0.1573 , -0.1488 , -0.1431 , -0.1369 ],
           [ 0.5773 ,  0.6028 ,  0.6021 ,  0.5876 ,  0.5901 ,  0.5618 ,
             0.5709 ,  0.5562 ,  0.5431 ,  0.5002 ,  0.5008 ,  0.5007 ,
             0.5125 ,  0.5222 ,  0.522  ,  0.5208 ,  0.5151 ,  0.5182 ,
             0.5419 ,  0.5756 ,  0.5948 ,  0.6098 ,  0.6183 ,  0.6111 ,
             0.6098 ,  0.6037 ,  0.5982 ,  0.5867 ],
           [ 0.8436 ,  0.9009 ,  0.9401 ,  0.9771 ,  0.9718 ,  0.9878 ,
             0.9411 ,  0.9286 ,  0.9016 ,  0.9215 ,  0.8754 ,  0.8358 ,
             0.7731 ,  0.7176 ,  0.6997 ,  0.6864 ,  0.6771 ,  0.6535 ,
             0.6062 ,  0.5314 ,  0.4867 ,  0.4527 ,  0.4353 ,  0.4515 ,
             0.4565 ,  0.4692 ,  0.4809 ,  0.503  ],
           [-0.9537 , -1.001  , -1.024  , -1.039  , -1.034  , -1.038  ,
            -1.013  , -1.009  , -0.9894 , -0.9977 , -0.9647 , -0.9351 ,
            -0.8892 , -0.8454 , -0.8345 , -0.8208 , -0.8062 , -0.7894 ,
            -0.7615 , -0.7143 , -0.6838 , -0.6594 , -0.6494 , -0.6595 ,
        -0.6649 , -0.6734 , -0.681  , -0.6946 ],
           [ 0.1708 ,  0.1759 ,  0.1773 ,  0.1774 ,  0.1763 ,  0.1779 ,
             0.1763 ,  0.1793 ,  0.1784 ,  0.1834 ,  0.1788 ,  0.1743 ,
             0.1661 ,  0.1574 ,  0.1565 ,  0.1534 ,  0.1494 ,  0.1468 ,
             0.1417 ,  0.1328 ,  0.1265 ,  0.1211 ,  0.1194 ,  0.1212 ,
             0.1228 ,  0.1246 ,  0.1261 ,  0.1288 ]]


AllenSEA06_sigma_coefficient_period=[
    10.   ,   5.    ,   3.003 ,   2.    ,   1.6   ,   1.    ,
    0.7502,   0.5   ,   0.4   ,   0.3   ,   0.24  ,   0.2   ,
    0.16  ,   0.15  ,   0.12  ,   0.1   ,   0.08  ,   0.07  ,
    0.06  ,   0.055 ,   0.05  ,   0.04  ,   0.0323,   0.025 ,
    0.02  ,   0.01  ]

model_sigma=[
    [
    1.2756,  1.1358,  0.9711,  0.8642,  0.7764,  0.6627,  0.6599,
    0.5899,  0.5648,  0.557 ,  0.533 ,  0.5208,  0.5101,  0.5114,
    0.5184,  0.4997,  0.489 ,  0.4884,  0.4918,  0.4851,  0.4891,
    0.4847,  0.4793,  0.4742,  0.4768,  0.4774]]

regression_sigma=[
    [
    0.235 ,  0.258 ,  0.2739,  0.2938,  0.3074,  0.3373,  0.3546,
    0.3832,  0.4015,  0.4298,  0.456 ,  0.4786,  0.4996,  0.5064,
    0.5219,  0.5327,  0.5211,  0.5074,  0.4848,  0.4696,  0.4574,
    0.4525,  0.4547,  0.4482,  0.4429,  0.4404]]


AllenSEA06_sigma_coefficient=model_sigma+regression_sigma

AllenSEA06_magnitude_type='Mw'
AllenSEA06_distance_type='Mendez_rupture'

AllenSEA06_interpolation=linear_interpolation
AllenSEA06_sigma_coefficient_interpolation=linear_interpolation

def AllenSEA06_distribution(**kwargs):

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13=coefficient
    
    r0 = 10; # km
    r1 = 90;
    r2 = 160;

    log10_dist=log10(distance)
    
    #TA:
    # f0 = max([log10(r0./RrupMatrix) zeros(size(RrupMatrix))]);

    # noting that log(a/b) = log(a) - log(b)
    f0 = log10(r0) - log10_dist
    f0 = where(f0>0,f0,0)
    
    #TA:
    # f1 = min([log10(RrupMatrix) log10(repmat(r1,size(RrupMatrix)))]);
    f1 = log10_dist
    f1 = where(f1>log10(r1),log10(r1),f1)

    #TA:
    # f2 = max([log10(RrupMatrix./r2) zeros(size(RrupMatrix))]);
    f2 = log10_dist - log10(r2)
    f2 = where(f2>0,f2,0)

    #TA:
    # D = (c10 + c11.*log10(RrupMatrix) + c12.*log10(RrupMatrix).^2
    #     + c13.*log10(RrupMatrix).^3);
    D=(c10+c11*log10_dist+c12*(log10_dist**2)+c13*(log10_dist**3));

    # TA:
    # lnSA = log(10.^(c1 + c2.*MagMatrix + c3.*MagMatrix.^2 +
    # (c4 + c5.*MagMatrix).*f1 ...
    # + (c6 + c7.*MagMatrix).*f2 + (c8 + c9.*MagMatrix).*f0 + D)/980);

    # Noting that log_e(10**x)=log10(10**x)/log10(e)=x/log10(e)

    # or log_e(10**x/y)=log10(10**x/y)/log10(e)=(x-log10(y))/log10(e)
    
    log_mean = ((c1+c2*mag+c3*(mag**2)+(c4+c5*mag)*f1+
                (c6+c7*mag)*f2+(c8+c9*mag)*f0+D)-log10(980))/LOG10E
                
    num_events = distance.shape[1]
    log_sigma = tile(sigma_coefficient[0],(1,num_events,1))
    return log_mean,log_sigma

AllenSEA06_uses_Vs30 = False

AllenSEA06_args=[
    AllenSEA06_distribution,
    AllenSEA06_magnitude_type,
    AllenSEA06_distance_type,
    
    AllenSEA06_coefficient,
    AllenSEA06_coefficient_period,
    AllenSEA06_interpolation,
    
    AllenSEA06_sigma_coefficient,
    AllenSEA06_sigma_coefficient_period,
    AllenSEA06_sigma_coefficient_interpolation,

    AllenSEA06_uses_Vs30]

ground_motion_init['AllenSEA06'] = AllenSEA06_args

#***************  End of AllenSEA06 MODEL  ******************

#***************  Start of Atkinson_Boore_97 MODEL  ******************

Atkinson_Boore_97_coefficient=[
    [  1.84100000e+00,   2.76200000e+00,   2.46300000e+00,
        2.30100000e+00,   2.14000000e+00,   1.74900000e+00,
        1.26500000e+00,   6.20000000e-01,  -9.40000000e-02,
        -5.08000000e-01,  -9.00000000e-01,  -1.66000000e+00],
     [  6.86000000e-01,   7.55000000e-01,   7.97000000e-01,
        8.29000000e-01,   8.64000000e-01,   9.63000000e-01,
        1.09400000e+00,   1.26700000e+00,   1.39100000e+00,
        1.42800000e+00,   1.46200000e+00,   1.46000000e+00],
     [ -1.23000000e-01,  -1.10000000e-01,  -1.13000000e-01,
       -1.21000000e-01,  -1.29000000e-01,  -1.48000000e-01,
       -1.65000000e-01,  -1.47000000e-01,  -1.18000000e-01,
       -9.40000000e-02,  -7.10000000e-02,  -3.90000000e-02],
     [ -3.11000000e-03,  -5.20000000e-03,  -3.52000000e-03,
       -2.79000000e-03,  -2.07000000e-03,  -1.05000000e-03,
       -2.40000000e-04,   0.00000000e+00,   0.00000000e+00,
       0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]

Atkinson_Boore_97_coefficient_period= [
    0.00000000e+00,   5.00000000e-02,   7.70000000e-02,
    1.00000000e-01,   1.30000000e-01,   2.00000000e-01,
    3.10000000e-01,   5.00000000e-01,   7.70000000e-01,
    1.00000000e+00,   1.25000000e+00,   2.00000000e+00]

Atkinson_Boore_97_interpolation=linear_interpolation


Atkinson_Boore_97_sigma_coefficient=[
    [0.622, 0.622, 0.599, 0.553, 0.553, 0.553]]

Atkinson_Boore_97_sigma_coefficient_period=[0, 0.10, 0.20, 0.50, 1.00, 100]

Atkinson_Boore_97_sigma_coefficient_interpolation=linear_interpolation

def Atkinson_Boore_97_distribution_python(**kwargs):
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    (num_sites, num_events) = distance.shape[0:2]
    num_periods = coefficient.shape[3]

    assert coefficient.shape == (4,1,1,num_periods)
    assert sigma_coefficient.shape == (1,1,1,num_periods)
    assert mag.shape == (1,num_events,1)
    assert distance.shape == (num_sites,num_events,1)

    (c1, c2, c3, c4) = coefficient
    log_mean = c1 + c2*(mag-6) + c3*(mag-6)**2 - log(distance) - c4*distance
    log_sigma = tile(sigma_coefficient[0], (1, num_events, 1))   

    return (log_mean, log_sigma)

def Atkinson_Boore_97_distribution(**kwargs):
    """The usual parameters passed are:
           mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    """

    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
   
    (num_sites, num_events) = distance.shape[0:2]
    num_periods=coefficient.shape[3]

    assert coefficient.shape == (4,1,1,num_periods)
    assert sigma_coefficient.shape == (1,1,1,num_periods)
    assert mag.shape == (1,num_events,1)
    assert distance.shape == (num_sites,num_events,1)

    log_mean = zeros((num_sites, num_events, num_periods), dtype=float)
    log_sigma = zeros((num_sites, num_events, num_periods), dtype=float)

    coefficient = coefficient[:,0,0,:]
    sigma_coefficient = sigma_coefficient[0,0,0,:]
    mag = mag[0,:,0]
    distance = distance[:,:,0]
    code="""
    double c1, c2, c3, c4;
    double m, d;
    for (int i=0; i < num_sites; ++i) {
        for (int j=0; j < num_events; ++j) {
            m = mag(j);
            d = distance(i,j);
            for (int k=0; k < num_periods; ++k) {
                c1 = coefficient(0, k);
                c2 = coefficient(1, k);
                c3 = coefficient(2, k);
                c4 = coefficient(3, k);
                
                log_mean(i, j, k) = c1 + c2*(m-6) + (c3*(m-6)*(m-6)) - log(d) - c4*d;
                log_sigma(i, j, k) = sigma_coefficient(k);
            }       
        }
    }

    return_val = 0;
    """

    try:
        weave.inline(code,
                     ['num_sites', 'num_events', 'num_periods',
                      'coefficient', 'sigma_coefficient',
                      'mag', 'log_mean', 'distance', 'log_sigma'],
                     type_converters=weave_converters.eqrm,
                     compiler='gcc')     
    except IOError:
        raise util.WeaveIOError 
  
    return (log_mean, log_sigma)

Atkinson_Boore_97_distance_type='Rupture'
Atkinson_Boore_97_magnitude_type='Mw'

Atkinson_Boore_97_uses_Vs30 = False

Atkinson_Boore_97_args=[
    Atkinson_Boore_97_distribution,
    Atkinson_Boore_97_magnitude_type,
    Atkinson_Boore_97_distance_type,
    
    Atkinson_Boore_97_coefficient,
    Atkinson_Boore_97_coefficient_period,
    Atkinson_Boore_97_interpolation,
    
    Atkinson_Boore_97_sigma_coefficient,
    Atkinson_Boore_97_sigma_coefficient_period,
    Atkinson_Boore_97_sigma_coefficient_interpolation,

    Atkinson_Boore_97_uses_Vs30
    ]


ground_motion_init['Atkinson_Boore_97'] = Atkinson_Boore_97_args


#***************  End of Atkinson_Boore_97 MODEL  ******************

#***************  Start of Sadigh_97 MODEL  ************

Sadigh_97_coefficient_less65=[
      [  1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01],
       [ -6.24000000e-01,  -9.00000000e-02,   1.10000000e-01,
          2.12000000e-01,   2.75000000e-01,   3.48000000e-01,
          3.07000000e-01,   2.85000000e-01,   2.39000000e-01,
          1.53000000e-01,   6.00000000e-02,  -5.70000000e-02,
         -2.98000000e-01,  -5.88000000e-01,  -1.20800000e+00,
         -1.70500000e+00,  -2.40700000e+00,  -2.94500000e+00,
         -3.70000000e+00,  -4.23000000e+00,  -4.71400000e+00,
         -5.53000000e+00],
       [  1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
          1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
          1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
          1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
          1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
          1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
          1.00000000e+00,   1.00000000e+00,   1.00000000e+00,
          1.00000000e+00],
       [  0.00000000e+00,   6.00000000e-03,   6.00000000e-03,
          6.00000000e-03,   6.00000000e-03,   5.00000000e-03,
          4.00000000e-03,   2.00000000e-03,   0.00000000e+00,
         -4.00000000e-03,  -1.10000000e-02,  -1.70000000e-02,
         -2.80000000e-02,  -4.00000000e-02,  -5.00000000e-02,
         -5.50000000e-02,  -6.50000000e-02,  -7.00000000e-02,
         -8.00000000e-02,  -1.00000000e-01,  -1.00000000e-01,
         -1.10000000e-01],
       [ -2.10000000e+00,  -2.12800000e+00,  -2.12800000e+00,
         -2.14000000e+00,  -2.14800000e+00,  -2.16200000e+00,
         -2.14400000e+00,  -2.13000000e+00,  -2.11000000e+00,
         -2.08000000e+00,  -2.05300000e+00,  -2.02800000e+00,
         -1.99000000e+00,  -1.94500000e+00,  -1.86500000e+00,
         -1.80000000e+00,  -1.72500000e+00,  -1.67000000e+00,
         -1.61000000e+00,  -1.57000000e+00,  -1.54000000e+00,
         -1.51000000e+00],
       [  0.00000000e+00,  -8.20000000e-02,  -8.20000000e-02,
         -5.20000000e-02,  -4.10000000e-02,  -1.40000000e-02,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  3.65640000e+00,   3.65640000e+00,   3.65640000e+00,
          3.65640000e+00,   3.65640000e+00,   3.65640000e+00,
          3.65640000e+00,   3.65640000e+00,   3.65640000e+00,
          3.65640000e+00,   3.65640000e+00,   3.65640000e+00,
          3.65640000e+00,   3.65640000e+00,   3.65640000e+00,
          3.65640000e+00,   3.65640000e+00,   3.65640000e+00,
          3.65640000e+00,   3.65640000e+00,   3.65640000e+00,
          3.65640000e+00],
       [  2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
          2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
          2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
          2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
          2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
          2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
          2.50000000e-01,   2.50000000e-01,   2.50000000e-01,
          2.50000000e-01]]
Sadigh_97_coefficient_more65=[
      [  1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01,   1.82000000e-01,   1.82000000e-01,
          1.82000000e-01],
       [ -1.27400000e+00,  -7.40000000e-01,  -5.40000000e-01,
         -4.38000000e-01,  -3.75000000e-01,  -3.02000000e-01,
         -3.43000000e-01,  -3.65000000e-01,  -4.11000000e-01,
         -4.97000000e-01,  -5.90000000e-01,  -7.07000000e-01,
         -9.48000000e-01,  -1.23800000e+00,  -1.85800000e+00,
         -2.35500000e+00,  -3.05700000e+00,  -3.59500000e+00,
         -4.35000000e+00,  -4.88000000e+00,  -5.36400000e+00,
         -6.18000000e+00],
       [  1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
          1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
          1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
          1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
          1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
          1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
          1.10000000e+00,   1.10000000e+00,   1.10000000e+00,
          1.10000000e+00],
       [  0.00000000e+00,   6.00000000e-03,   6.00000000e-03,
          6.00000000e-03,   6.00000000e-03,   5.00000000e-03,
          4.00000000e-03,   2.00000000e-03,   0.00000000e+00,
         -4.00000000e-03,  -1.10000000e-02,  -1.70000000e-02,
         -2.80000000e-02,  -4.00000000e-02,  -5.00000000e-02,
         -5.50000000e-02,  -6.50000000e-02,  -7.00000000e-02,
         -8.00000000e-02,  -1.00000000e-01,  -1.00000000e-01,
         -1.10000000e-01],
       [ -2.10000000e+00,  -2.12800000e+00,  -2.12800000e+00,
         -2.14000000e+00,  -2.14800000e+00,  -2.16200000e+00,
         -2.14400000e+00,  -2.13000000e+00,  -2.11000000e+00,
         -2.08000000e+00,  -2.05300000e+00,  -2.02800000e+00,
         -1.99000000e+00,  -1.94500000e+00,  -1.86500000e+00,
         -1.80000000e+00,  -1.72500000e+00,  -1.67000000e+00,
         -1.61000000e+00,  -1.57000000e+00,  -1.54000000e+00,
         -1.51000000e+00],
       [  0.00000000e+00,  -8.20000000e-02,  -8.20000000e-02,
         -5.20000000e-02,  -4.10000000e-02,  -1.40000000e-02,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
          0.00000000e+00],
       [  6.16000000e-01,   6.16000000e-01,   6.16000000e-01,
          6.16000000e-01,   6.16000000e-01,   6.16000000e-01,
          6.16000000e-01,   6.16000000e-01,   6.16000000e-01,
          6.16000000e-01,   6.16000000e-01,   6.16000000e-01,
          6.16000000e-01,   6.16000000e-01,   6.16000000e-01,
          6.16000000e-01,   6.16000000e-01,   6.16000000e-01,
          6.16000000e-01,   6.16000000e-01,   6.16000000e-01,
          6.16000000e-01],
       [  5.24000000e-01,   5.24000000e-01,   5.24000000e-01,
          5.24000000e-01,   5.24000000e-01,   5.24000000e-01,
          5.24000000e-01,   5.24000000e-01,   5.24000000e-01,
          5.24000000e-01,   5.24000000e-01,   5.24000000e-01,
          5.24000000e-01,   5.24000000e-01,   5.24000000e-01,
          5.24000000e-01,   5.24000000e-01,   5.24000000e-01,
          5.24000000e-01,   5.24000000e-01,   5.24000000e-01,
          5.24000000e-01]]
Sadigh_97_coefficient=Sadigh_97_coefficient_less65 + \
                       Sadigh_97_coefficient_more65
Sadigh_97_coefficient= Sadigh_97_coefficient

Sadigh_97_coefficient_period= [
    0.00000000e+00,   5.00000000e-02,   7.00000000e-02,
    9.00000000e-02,   1.00000000e-01,   1.20000000e-01,
    1.40000000e-01,   1.50000000e-01,   1.70000000e-01,
    2.00000000e-01,   2.40000000e-01,   3.00000000e-01,
    4.00000000e-01,   5.00000000e-01,   7.50000000e-01,
    1.00000000e+00,   1.50000000e+00,   2.00000000e+00,
    3.00000000e+00,   4.00000000e+00,   5.00000000e+00,
    7.50000000e+00]

Sadigh_97_interpolation=linear_interpolation


Sadigh_97_sigma_coefficient= [
    [  1.39000000e+00,   1.39000000e+00,   1.40000000e+00,
       1.40000000e+00,   1.41000000e+00,   1.41000000e+00,
       1.42000000e+00,   1.42000000e+00,   1.42000000e+00,
       1.43000000e+00,   1.44000000e+00,   1.45000000e+00,
       1.48000000e+00,   1.50000000e+00,   1.52000000e+00,
       1.53000000e+00,   1.53000000e+00,   1.53000000e+00,
       1.53000000e+00,   1.53000000e+00,   1.53000000e+00,
       1.53000000e+00],
    [  1.40000000e-01,   1.40000000e-01,   1.40000000e-01,
       1.40000000e-01,   1.40000000e-01,   1.40000000e-01,
       1.40000000e-01,   1.40000000e-01,   1.40000000e-01,
       1.40000000e-01,   1.40000000e-01,   1.40000000e-01,
       1.40000000e-01,   1.40000000e-01,   1.40000000e-01,
       1.40000000e-01,   1.40000000e-01,   1.40000000e-01,
       1.40000000e-01,   1.40000000e-01,   1.40000000e-01,
       1.40000000e-01],
    [  3.80000000e-01,   3.80000000e-01,   3.90000000e-01,
       3.90000000e-01,   4.00000000e-01,   4.00000000e-01,
       4.10000000e-01,   4.10000000e-01,   4.10000000e-01,
       4.20000000e-01,   4.30000000e-01,   4.40000000e-01,
       4.70000000e-01,   4.90000000e-01,   5.10000000e-01,
       5.20000000e-01,   5.20000000e-01,   5.20000000e-01,
       5.20000000e-01,   5.20000000e-01,   5.20000000e-01,
       5.20000000e-01]]
Sadigh_97_sigma_coefficient=Sadigh_97_sigma_coefficient

Sadigh_97_sigma_coefficient_period=[
    0.00000000e+00,   5.00000000e-02,   7.00000000e-02,
    9.00000000e-02,   1.00000000e-01,   1.20000000e-01,
    1.40000000e-01,   1.50000000e-01,   1.70000000e-01,
    2.00000000e-01,   2.40000000e-01,   3.00000000e-01,
    4.00000000e-01,   5.00000000e-01,   7.50000000e-01,
    1.00000000e+00,   1.50000000e+00,   2.00000000e+00,
    3.00000000e+00,   4.00000000e+00,   5.00000000e+00,
    7.50000000e+00]

Sadigh_97_sigma_coefficient_interpolation=linear_interpolation

def Sadigh_97_distribution_python(**kwargs):

    """
    distance is a 3D array. First D is sites, second dimension is events,
    third can only have one value.
    """
    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    (num_sites, num_events) = distance.shape[0:2]
    num_periods = coefficient.shape[3]

    assert coefficient.shape == (16,1,1,num_periods)
    assert sigma_coefficient.shape == (3,1,1,num_periods)
    assert mag.shape == (1,num_events,1)
    assert distance.shape == (num_sites,num_events,1)

    #if not (mag < 8.5).all():
    #    raise ValueError('Sadigh 97 is not valid for magnitude > 8.5')
        
    F=1.0

    c_less65 = coefficient[:8] + mag*0
    #c_less65 = c_less65+mag*0 # expand it to size of mag
    
    c_more65 = coefficient[8:] + mag*0
    #c_more65 = c_more65+mag*0 # expand it to size of mag

    coefficient = where((mag + c_less65*0) >6.5, c_more65, c_less65)
    
    (c1, c2, c3, c4, c5, c6, c7, c8) = coefficient
    R = distance + c7*exp(c8*mag)
    
    log_mean = c1*F + c2 + c3*mag + c4*(8.5-mag)**2.5 + c5*log(R)+ c6*log(distance+2)

    (s1, s2, s3) = sigma_coefficient
    
    log_sigma = where((mag + 0*s1) > 7.21, s3+0*mag, s1-s2*mag)

    assert isfinite(log_mean).all()

    return (log_mean, log_sigma)

def Sadigh_97_distribution(**kwargs):

    """
    distance is a 3D array. First D is sites, second dimension is events,
    third can only have one value.
    """
    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30

    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    
    (num_sites, num_events) = distance.shape[0:2]
    num_periods = coefficient.shape[3]

    assert coefficient.shape == (16,1,1,num_periods)
    assert sigma_coefficient.shape == (3,1,1,num_periods)
    assert mag.shape == (1,num_events,1)
    assert distance.shape == (num_sites,num_events,1)

    log_mean =zeros((num_sites, num_events, num_periods), dtype=float)
    log_sigma =zeros((num_sites, num_events, num_periods), dtype=float)

    coefficient = coefficient[:,0,0,:]
    sigma_coefficient = sigma_coefficient[:,0,0,:]
    mag = mag[0,:,0]
    distance = distance[:,:,0]
    code = """
    double F = 1.0;
    double c1,c2,c3,c4,c5,c6,c7,c8;
    double s1,s2,s3;
    double m,d;
    double R;
    int c_offset;

    for (int i=0; i < num_sites; ++i) {
        for (int j=0; j < num_events; ++j) {
            m = mag(j);
            d = distance(i,j);

            c_offset = (m > 6.5) ? 8 : 0;            
#ifdef JUNK
            if (m > 6.5)
                c_offset=8;
            else
                c_offset=0;
#endif

            for (int k=0; k < num_periods; ++k) {
                c1 = coefficient((0 + c_offset), k);
                c2 = coefficient((1 + c_offset), k);
                c3 = coefficient((2 + c_offset), k);
                c4 = coefficient((3 + c_offset), k);
                c5 = coefficient((4 + c_offset), k);
                c6 = coefficient((5 + c_offset), k);
                c7 = coefficient((6 + c_offset), k);
                c8 = coefficient((7 + c_offset), k);
                
                R = d + c7*exp(c8*m);
                log_mean(i, j, k) = c1*F + c2 + c3*m + c4*pow((8.5-m), 2.5) +
                                        c5*log(R)+ c6*log(d+2.0);

                s1 = sigma_coefficient(0, k);
                s2 = sigma_coefficient(1, k);
                s3 = sigma_coefficient(2, k);

                log_sigma(i, j, k) = (m > 7.21) ? s3 : s1 - s2*m;
#ifdef JUNK
                if (m > 7.21)
                    log_sigma(i, j, k) = s3;
                else
                    log_sigma(i, j, k) = s1 - s2*m;
#endif
            }       
        }
    }

    return_val = 0;
    """
    try:
        weave.inline(code,
                     ['num_sites', 'num_events', 'num_periods',
                      'coefficient', 'sigma_coefficient',
                      'mag', 'log_mean', 'distance', 'log_sigma'],
                     type_converters=weave_converters.eqrm,
                     compiler='gcc')   
    except IOError:
        raise util.WeaveIOError 

    assert isfinite(log_mean).all()

    return (log_mean, log_sigma)

Sadigh_97_distance_type='Rupture'
Sadigh_97_magnitude_type='Mw'

Sadigh_97_uses_Vs30 = False

Sadigh_97_args=[
    Sadigh_97_distribution,
    Sadigh_97_magnitude_type,
    Sadigh_97_distance_type,
    
    Sadigh_97_coefficient,
    Sadigh_97_coefficient_period,
    Sadigh_97_interpolation,
    
    Sadigh_97_sigma_coefficient,
    Sadigh_97_sigma_coefficient_period,
    Sadigh_97_sigma_coefficient_interpolation,

    Sadigh_97_uses_Vs30]

ground_motion_init['Sadigh_97'] = Sadigh_97_args


#***************  End of Sadigh_97 MODEL  ************

#***************  Start of Sadigh_Original_97 MODEL  ************

# Note: zero period acceleration (ZPA) assumed to be 0. 

# Coefficients as per 
# Appendix C, t. C-8, p. C-15,
# Evaluation of Earthquake Ground Motions,
# Idriss et al.,
# 2007
# M <= 6.5
Sadigh_Original_97_model_low = asarray([
    # Period,  C1,    C2, C3,     C4,    C5,      C6,     C7
    [0,       -0.624, 1,  0.000, -2.100, 1.29649, 0.250,  0.000],
    [0.03,    -0.624, 1,  0.000, -2.100, 1.29649, 0.250,  0.000],
    [0.07,     0.110, 1,  0.006, -2.128, 1.29649, 0.250, -0.082],
    [0.1,      0.275, 1,  0.006, -2.148, 1.29649, 0.250, -0.041],
    [0.2,      0.153, 1, -0.004, -2.080, 1.29649, 0.250,  0.000],
    [0.3,     -0.057, 1, -0.017, -2.028, 1.29649, 0.250,  0.000],
    [0.4,     -0.298, 1, -0.028, -1.990, 1.29649, 0.250,  0.000],
    [0.5,     -0.588, 1, -0.040, -1.945, 1.29649, 0.250,  0.000],
    [0.75,    -1.208, 1, -0.050, -1.865, 1.29649, 0.250,  0.000],
    [1,       -1.705, 1, -0.055, -1.800, 1.29649, 0.250,  0.000],
    [1.5,     -2.407, 1, -0.065, -1.725, 1.29649, 0.250,  0.000],
    [2,       -2.945, 1, -0.070, -1.670, 1.29649, 0.250,  0.000],
    [3,       -3.700, 1, -0.080, -1.610, 1.29649, 0.250,  0.000],
    [4,       -4.230, 1, -0.100, -1.570, 1.29649, 0.250,  0.000]
]).T
Sadigh_Original_97_coefficient_low = Sadigh_Original_97_model_low[1:]
Sadigh_Original_97_coefficient_period_low = Sadigh_Original_97_model_low[0]

# M > 6.5
Sadigh_Original_97_model_high = asarray([
    # Period,  C1,    C2,   C3,     C4,     C5,      C6,     C7
    [0,       -1.237, 1.1,  0.000, -2.100, -0.48451, 0.524,  0.000],
    [0.03,    -1.237, 1.1,  0.000, -2.100, -0.48451, 0.524,  0.000],
    [0.07,    -0.540, 1.1,  0.006, -2.128, -0.48451, 0.524, -0.082],
    [0.1,     -0.375, 1.1,  0.006, -2.148, -0.48451, 0.524, -0.041],
    [0.2,     -0.497, 1.1, -0.004, -2.080, -0.48451, 0.524,  0.000],
    [0.3,     -0.707, 1.1, -0.017, -2.028, -0.48451, 0.524,  0.000],
    [0.4,     -0.948, 1.1, -0.028, -1.990, -0.48451, 0.524,  0.000],
    [0.5,     -1.238, 1.1, -0.040, -1.945, -0.48451, 0.524,  0.000],
    [0.75,    -1.858, 1.1, -0.050, -1.865, -0.48451, 0.524,  0.000],
    [1,       -2.355, 1.1, -0.055, -1.800, -0.48451, 0.524,  0.000],
    [1.5,     -3.057, 1.1, -0.065, -1.725, -0.48451, 0.524,  0.000],
    [2,       -3.595, 1.1, -0.070, -1.670, -0.48451, 0.524,  0.000],
    [3,       -4.350, 1.1, -0.080, -1.610, -0.48451, 0.524,  0.000],
    [4,       -4.880, 1.1, -0.100, -1.570, -0.48451, 0.524,  0.000]
]).T
Sadigh_Original_97_coefficient_high = Sadigh_Original_97_model_high[1:]
Sadigh_Original_97_coefficient_period_high= Sadigh_Original_97_model_high[0]

Sadigh_Original_97_coefficient = concatenate((Sadigh_Original_97_coefficient_low,
                                              Sadigh_Original_97_coefficient_high))
Sadigh_Original_97_coefficient_period = Sadigh_Original_97_coefficient_period_low

# Sigma coefficients as per 
# Appendix C, t. C-7, p. C-14,
# Evaluation of Earthquake Ground Motions,
# Idriss et al.,
# 2007
# M < 7.21 -> sigma = coeff - 0.14M
# M >= 7.12 -> sigma = coeff
Sadigh_Original_97_sigma_model = asarray([
    # Period, M < 7.21, M >= 7.21
    [0,       1.39,     0.38],
    [0.07,    1.40,     0.39],
    [0.1,     1.41,     0.40],
    [0.2,     1.43,     0.42],
    [0.3,     1.45,     0.44],
    [0.4,     1.48,     0.47],
    [0.5,     1.50,     0.49],
    [0.75,    1.52,     0.51],
    [1,       1.53,     0.52],
    [1.5,     1.53,     0.52],
    [2,       1.53,     0.52],
    [3,       1.53,     0.52],
    [4,       1.53,     0.52]
]).T
Sadigh_Original_97_sigma_coefficient_period = Sadigh_Original_97_sigma_model[0]
Sadigh_Original_97_sigma_coefficient = Sadigh_Original_97_sigma_model[1:]


# TODO: Are these correct?
Sadigh_Original_97_uses_Vs30 = False
Sadigh_Original_97_magnitude_type='Mw'
Sadigh_Original_97_distance_type='Rupture'
Sadigh_Original_97_interpolation=linear_interpolation

def Sadigh_Original_97_distribution(**kwargs):
    """
    Sadigh et al. (1997) distribution.
    Equation for ground motion as per 
    Appendix C, eq. [C-17], p. C-14,
    Evaluation of Earthquake Ground Motions,
    Idriss et al.,
    2007
    """
    dist_object = kwargs['dist_object']
    Mw = kwargs['mag']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    # Rrup from distance object
    Rrup = dist_object.Rupture

    num_sites = Mw.shape[0]
    num_events = Mw.shape[1]
    num_periods = coefficient.shape[3]

    # Check we have the right shapes
    msg = 'Expected %s.shape=%s, got %s'

    assert Mw.shape == (1, num_events, 1), (msg
               % ('Mw', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Mw.shape)))

    # ignore first dimension of distances
    assert Rrup.shape[1:] == (num_events,), (msg
               % ('Rrup', '(?,%d)' % num_events, str(Rrup.shape)))

    assert coefficient.shape == (14, 1, 1, num_periods), (msg
               % ('coefficient', '(14,1,1,%d)' % num_periods,
                  str(coefficient.shape)))

    Rrup = dist_object.Rupture[:,:,newaxis]
    
    # Low mag coefficients (M <= 6.5)
    c_low = coefficient[:7]
    
    # High mag coefficients (M > 6.5)
    c_high = coefficient[7:]
    
    # Determine coefficients based on mag
    c = where(Mw > 6.5, c_high, c_low)
    
    c1, c2, c3, c4, c5, c6, c7 = c
    
    log_mean = c1 + \
               c2*Mw + \
               c3*((8.5-Mw)**2.5) + \
               c4*log(Rrup + exp(c5 + c6*Mw)) + \
               c7*log(Rrup + 2)
    
    # Low mag sigma (M < 7.21)
    s_low = sigma_coefficient[0] - 0.14*Mw
    
    # High mag sigma (M >= 7.21)
    s_high = sigma_coefficient[1]
    
    log_sigma = where(Mw >= 7.21, s_high, s_low)

    return (log_mean, log_sigma)

Sadigh_Original_97_args=[
    Sadigh_Original_97_distribution,
    Sadigh_Original_97_magnitude_type,
    Sadigh_Original_97_distance_type,
    
    Sadigh_Original_97_coefficient,
    Sadigh_Original_97_coefficient_period,
    Sadigh_Original_97_interpolation,
    
    Sadigh_Original_97_sigma_coefficient,
    Sadigh_Original_97_sigma_coefficient_period,
    Sadigh_Original_97_interpolation,

    Sadigh_Original_97_uses_Vs30]

ground_motion_init['Sadigh_Original_97'] = Sadigh_Original_97_args

#***************  End of Sadigh_Original_97 MODEL  ************

#***************  Start of Youngs_97 MODEL common block  ************

#Youngs et al 1997 attenuation model jgriffin 28/06/07
Youngs_97_coefficient=[
    [  0.00000000e+00,   1.27500000e+00,   1.18800000e+00,
          7.22000000e-01,   2.46000000e-01,  -1.15000000e-01,
         -4.00000000e-01,  -1.14900000e+00,  -1.73600000e+00,
         -2.63400000e+00,  -3.32800000e+00,  -4.51100000e+00],
       [  0.00000000e-00,   0.00000000e-00,  -1.10000000e-03,
         -2.70000000e-03,  -3.60000000e-03,  -4.30000000e-03,
         -4.80000000e-03,  -5.70000000e-03,  -6.40000000e-03,
         -7.30000000e-03,  -8.00000000e-03,  -8.90000000e-03],
       [ -2.55200000e-00,  -2.70700000e-00,  -2.65500000e-00,
         -2.52800000e-00,  -2.45400000e-00,  -2.40100000e-00,
         -2.36000000e-00,  -2.28600000e-00,  -2.234000000e-00,
         -2.16000000e-00,  -2.10700000e-00,  -2.03300000e-00]]

Youngs_97_coefficient = Youngs_97_coefficient

Youngs_97_sigma_coefficient=[
    [  1.45000000e+00,   1.45000000e+00,   1.45000000e+00,
          1.45000000e+00,   1.45000000e+00,   1.45000000e+00,
          1.45000000e+00,   1.45000000e+00,   1.45000000e+00,
          1.50000000e+00,   1.55000000e+00,   1.65000000e+00,
          ],
       [ -1.00000000e-01,  -1.00000000e-01,  -1.00000000e-01,
         -1.00000000e-01,  -1.00000000e-01,  -1.00000000e-01,
         -1.00000000e-01,  -1.00000000e-01,  -1.00000000e-01,
         -1.00000000e-01,  -1.00000000e-01,  -1.00000000e-01,
          ]]



Youngs_97_interpolation=linear_interpolation

Youngs_97_coefficient_period=[
    0.00000000e+00,   7.50000000e-02,   1.00000000e-01,
    2.00000000e-01,   3.00000000e-01,   4.00000000e-01,
    5.00000000e-01,   7.50000000e-01,   1.00000000e+00,
    1.50000000e+00,   2.00000000e+00,   3.00000000e+00,]

Youngs_97_sigma_coefficient_period=[
    0.00000000e+00,   7.50000000e-02,   1.00000000e-01,
    2.00000000e-01,   3.00000000e-01,   4.00000000e-01,
    5.00000000e-01,   7.50000000e-01,   1.00000000e+00,
    1.50000000e+00,   2.00000000e+00,   3.00000000e+00,]

Youngs_97_sigma_coefficient_interpolation=linear_interpolation

def Youngs_97_distribution_python(**kwargs):
    """
    
    Relationships for Subduction Zone Earthquakes, 1997
    
    """
    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    depth = kwargs['depth']

    # The depth that is passed in is depth to centroid.
    # The actual depth required is focal depth,
    # but we are assuming depth to centroid is close enough.
    
    c1,c2,c3,Z_t=coefficient

    # Z_t=0.0 for interface earthquakes
    # Z_t=1 for intraslab earthquakes

    use_dist=(distance<10)
    use_dist=use_dist*1.0
    use_dist2=(1-use_dist)
    distance=distance*use_dist2+10*use_dist
    log_mean=0.2418+1.414*mag+c1+c2*((10.0-mag)**3)+c3* \
              log(distance+1.7818*exp(0.554*mag))+0.00607*depth+0.3846*Z_t
    s1,s2=sigma_coefficient
    use_m=(mag<8)
    use_m=use_m*1.0
    use_n=(1-use_m)
    log_sigma=s1+s2*mag*use_m+s2*8*use_n #SD uses magnitude=8 for magnitude>8
    assert isfinite(log_mean).all()
    return log_mean,log_sigma

Youngs_97_distance_type='Rupture'
Youngs_97_magnitude_type='Mw'

Youngs_97_uses_Vs30 = False

#***************  End of Youngs_97 MODEL common block  ************

#***************  Start of Youngs_97 interface MODEL  ************

# Create list of Z_t constant of same length as coefficients
Z_t_interface = [0.0]*len(Youngs_97_coefficient[0])

Youngs_97_interface_coefficient =  Youngs_97_coefficient[:]
Youngs_97_interface_coefficient.append(Z_t_interface)

Youngs_97_interface_args=[
    Youngs_97_distribution_python,
    Youngs_97_magnitude_type,
    Youngs_97_distance_type,
    
    Youngs_97_interface_coefficient,
    Youngs_97_coefficient_period,
    Youngs_97_interpolation,
    
    Youngs_97_sigma_coefficient,
    Youngs_97_sigma_coefficient_period,
    Youngs_97_sigma_coefficient_interpolation,

    Youngs_97_uses_Vs30]

ground_motion_init['Youngs_97_interface'] = Youngs_97_interface_args

#***************  End of Youngs_97 interface MODEL  ***********

#***************  Start of Youngs_97 intraslab MODEL  ***********

# Create list of Z_t constant of same length as coefficients
Z_t_intraslab = [1.0]*len(Youngs_97_coefficient[0])

Youngs_97_intraslab_coefficient = Youngs_97_coefficient[:]
Youngs_97_intraslab_coefficient.append(Z_t_intraslab) 

Youngs_97_intraslab_args=[
    Youngs_97_distribution_python,
    Youngs_97_magnitude_type,
    Youngs_97_distance_type,
    
    Youngs_97_intraslab_coefficient,
    Youngs_97_coefficient_period,
    Youngs_97_interpolation,
    
    Youngs_97_sigma_coefficient,
    Youngs_97_sigma_coefficient_period,
    Youngs_97_sigma_coefficient_interpolation,

    Youngs_97_uses_Vs30]

ground_motion_init['Youngs_97_intraslab'] = Youngs_97_intraslab_args

#***************  End of Youngs_97 intraslab MODEL  ***********

#***************  End of Youngs_97 MODEL  ************

#***************  Start of Combo_Sadigh_Youngs_M8 MODEL  ************

# concatenate Young (interp to Sadigh periods) and Sadigh)
Combo_Sadigh_Youngs_M8_coeff= list(
    linear_interpolation(Sadigh_97_coefficient_period,
                         Youngs_97_interface_coefficient,
                         Youngs_97_coefficient_period))+list(
    Sadigh_97_coefficient)

Combo_Sadigh_Youngs_M8_coeff=Combo_Sadigh_Youngs_M8_coeff
Combo_Sadigh_Youngs_M8_sigma_coeff=list(
    linear_interpolation(Sadigh_97_sigma_coefficient_period,
                         Youngs_97_sigma_coefficient,
                         Youngs_97_sigma_coefficient_period))+list(
    Sadigh_97_sigma_coefficient)

Combo_Sadigh_Youngs_M8_sigma_coeff=Combo_Sadigh_Youngs_M8_sigma_coeff

def Combo_Sadigh_Youngs_M8_distribution_python(**kwargs):

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    depth = kwargs['depth']
    
    y_coefficient=coefficient[:4]
    y_sigma_coefficient=sigma_coefficient[:2]
    use_y=(mag>8.0)
    use_y=use_y*1.0 # convert from boolean to float
    y_log_mean,y_log_sigma=Youngs_97_distribution_python(
        mag=mag*use_y,
        distance=distance,
        coefficient=y_coefficient,
        sigma_coefficient=y_sigma_coefficient,
        depth=depth)
    
    s_coefficient=coefficient[4:]
    s_sigma_coefficient=sigma_coefficient[2:]
    use_s=(1-use_y)
    s_log_mean,s_log_sigma=Sadigh_97_distribution_python(
        mag=mag*use_s,
        distance=distance,
        coefficient=s_coefficient,
        sigma_coefficient=s_sigma_coefficient,
        depth=depth)

    log_mean=use_y*y_log_mean+use_s*s_log_mean
    log_sigma=use_y*y_log_sigma+use_s*s_log_sigma
    return log_mean,log_sigma

    
    
Youngs_97_distance_type='Rupture'
Youngs_97_magnitude_type='Mw'

Combo_Sadigh_Youngs_M8_uses_Vs30 = False

Combo_Sadigh_Youngs_M8_args=[
    Combo_Sadigh_Youngs_M8_distribution_python,
    Youngs_97_magnitude_type,
    Youngs_97_distance_type,
    
    Combo_Sadigh_Youngs_M8_coeff,
    Sadigh_97_coefficient_period,
    linear_interpolation,  
 
    Combo_Sadigh_Youngs_M8_sigma_coeff,
    Sadigh_97_sigma_coefficient_period,
    linear_interpolation,

    Combo_Sadigh_Youngs_M8_uses_Vs30]

ground_motion_init['Combo_Sadigh_Youngs_M8'] = Combo_Sadigh_Youngs_M8_args

#***************  End of Combo_Sadigh_Youngs_M8 MODEL  ************

"""
#***************  Start of Youngs_97 MODEL  ************

#Youngs et al 1997 attenuation model jgriffin 28/06/07
Youngs_97_coefficient=[
    [  0.00000000e+00,   1.27500000e+00,   1.18800000e+00,
          7.22000000e-01,   2.46000000e-01,  -1.15000000e-01,
         -4.00000000e-01,  -1.14900000e+00,  -1.73600000e+00,
         -2.63400000e+00,  -3.32800000e+00,  -4.51100000e+00],
       [  0.00000000e-00,   0.00000000e-00,  -1.10000000e-03,
         -2.70000000e-03,  -3.60000000e-03,  -4.30000000e-03,
         -4.80000000e-03,  -5.70000000e-03,  -6.40000000e-03,
         -7.30000000e-03,  -8.00000000e-03,  -8.90000000e-03],
       [ -2.55200000e-00,  -2.70700000e-00,  -2.65500000e-00,
         -2.52800000e-00,  -2.45400000e-00,  -2.40100000e-00,
         -2.36000000e-00,  -2.28600000e-00,  -2.234000000e-00,
         -2.16000000e-00,  -2.10700000e-00,  -2.03300000e-00]]

Youngs_97_coefficient = Youngs_97_coefficient

Youngs_97_sigma_coefficient=[
    [  1.45000000e+00,   1.45000000e+00,   1.45000000e+00,
          1.45000000e+00,   1.45000000e+00,   1.45000000e+00,
          1.45000000e+00,   1.45000000e+00,   1.45000000e+00,
          1.50000000e+00,   1.55000000e+00,   1.65000000e+00,
          ],
       [ -1.00000000e-01,  -1.00000000e-01,  -1.00000000e-01,
         -1.00000000e-01,  -1.00000000e-01,  -1.00000000e-01,
         -1.00000000e-01,  -1.00000000e-01,  -1.00000000e-01,
         -1.00000000e-01,  -1.00000000e-01,  -1.00000000e-01,
          ]]



Youngs_97_interpolation=linear_interpolation

Youngs_97_coefficient_period=[
    0.00000000e+00,   7.50000000e-02,   1.00000000e-01,
    2.00000000e-01,   3.00000000e-01,   4.00000000e-01,
    5.00000000e-01,   7.50000000e-01,   1.00000000e+00,
    1.50000000e+00,   2.00000000e+00,   3.00000000e+00,]

Youngs_97_sigma_coefficient_period=[
    0.00000000e+00,   7.50000000e-02,   1.00000000e-01,
    2.00000000e-01,   3.00000000e-01,   4.00000000e-01,
    5.00000000e-01,   7.50000000e-01,   1.00000000e+00,
    1.50000000e+00,   2.00000000e+00,   3.00000000e+00,]

Youngs_97_sigma_coefficient_interpolation=linear_interpolation

def Youngs_97_distribution_python(**kwargs):

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    depth = kwargs['depth']
    
    c1,c2,c3=coefficient
    Z_t=0.0 #for interface earthquakes
    #Z_t=1 #for intraslab earthquakes

    use_dist=(distance<10)
    use_dist=use_dist*1.0
    use_dist2=(1-use_dist)
    distance=distance*use_dist2+10*use_dist
    log_mean=0.2418+1.414*mag+c1+c2*((10.0-mag)**3)+c3* \
              log(distance+1.7818*exp(0.554*mag))+0.00607*depth+0.3846*Z_t
    s1,s2=sigma_coefficient
    use_m=(mag<8)
    use_m=use_m*1.0
    use_n=(1-use_m)
    log_sigma=s1+s2*mag*use_m+s2*8*use_n #SD uses magnitude=8 for magnitude>8
    assert isfinite(log_mean).all()
    return log_mean,log_sigma

Youngs_97_distance_type='Rupture'
Youngs_97_magnitude_type='Mw'

Youngs_97_args=[
    Youngs_97_distribution_python,
    Youngs_97_magnitude_type,
    Youngs_97_distance_type,
    
    Youngs_97_coefficient,
    Youngs_97_coefficient_period,
    Youngs_97_interpolation,
    
    Youngs_97_sigma_coefficient,
    Youngs_97_sigma_coefficient_period,
    Youngs_97_sigma_coefficient_interpolation]

ground_motion_init['Youngs_97'] = Youngs_97_args

#***************  End of Youngs_97 MODEL  ************

#***************  Start of Combo_Sadigh_Youngs_M8 MODEL  ************

# concatenate Young (interp to Sadigh periods) and Sadigh)
Combo_Sadigh_Youngs_M8_coeff= list(
    linear_interpolation(Sadigh_97_coefficient_period,
                         Youngs_97_coefficient,
                         Youngs_97_coefficient_period))+list(
    Sadigh_97_coefficient)

Combo_Sadigh_Youngs_M8_coeff=Combo_Sadigh_Youngs_M8_coeff
Combo_Sadigh_Youngs_M8_sigma_coeff=list(
    linear_interpolation(Sadigh_97_sigma_coefficient_period,
                         Youngs_97_sigma_coefficient,
                         Youngs_97_sigma_coefficient_period))+list(
    Sadigh_97_sigma_coefficient)

Combo_Sadigh_Youngs_M8_sigma_coeff=Combo_Sadigh_Youngs_M8_sigma_coeff

def Combo_Sadigh_Youngs_M8_distribution_python(**kwargs):

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    depth = kwargs['depth']

    y_coefficient=coefficient[:3]
    y_sigma_coefficient=sigma_coefficient[:2]
    use_y=(mag>8.0)
    use_y=use_y*1.0 # convert from boolean to float
    y_log_mean,y_log_sigma=Youngs_97_distribution_python(
        mag=mag*use_y,
        distance=distance,
        coefficient=y_coefficient,
        sigma_coefficient=y_sigma_coefficient,
        depth=depth)
    
    s_coefficient=coefficient[3:]
    s_sigma_coefficient=sigma_coefficient[2:]
    use_s=(1-use_y)
    s_log_mean,s_log_sigma=Sadigh_97_distribution_python(
        mag=mag*use_s,
        distance=distance,
        coefficient=s_coefficient,
        sigma_coefficient=s_sigma_coefficient,
        depth=depth)

    log_mean=use_y*y_log_mean+use_s*s_log_mean
    log_sigma=use_y*y_log_sigma+use_s*s_log_sigma
    return log_mean,log_sigma

    
    
Youngs_97_distance_type='Rupture'
Youngs_97_magnitude_type='Mw'

Youngs_97_uses_Vs30 = False

Combo_Sadigh_Youngs_M8_args=[
    Combo_Sadigh_Youngs_M8_distribution_python,
    Youngs_97_magnitude_type,
    Youngs_97_distance_type,    
    Combo_Sadigh_Youngs_M8_coeff,
    Sadigh_97_coefficient_period,
    linear_interpolation,   
    Combo_Sadigh_Youngs_M8_sigma_coeff,
    Sadigh_97_sigma_coefficient_period,
    linear_interpolation,
    Youngs_97_uses_Vs30]

ground_motion_init['Combo_Sadigh_Youngs_M8'] = Combo_Sadigh_Youngs_M8_args

#***************  End of Combo_Sadigh_Youngs_M8 MODEL  ************
"""

#***************  Start of Boore_08 MODEL  ************
# This is what the coefficients are;
# %T c1 c2 c3 h e1 e2 e3 e4 e5 e6 e7 mh sig tu sigtu tm sigtm blin b1 b2
# PGV -0.87370 0.10060 -0.00334 2.54 5.00121 5.04727 4.63188 5.08210 0.18322 -0.12736 0.00000 8.50 0.500 0.286 0.576 0.256 0.560 -0.600 -0.500 -0.06

# The axis for this is period, coefficient
# It has to be coefficient, period.  So there is a transpose at the end.
Boore_08_coefficient_raw = array([
    [ -0.66050,0.11970,-0.01151,1.35,-0.53804,-0.50350,-0.75472,-0.50970,
      0.28805,-0.10164,0.00000,6.75,0.502,0.265,0.566,0.260,0.564,-0.360,
      -0.640,-0.14],
    [-0.6622,0.12,-0.01151,1.35,-0.52883,-0.49429,-0.74551,-0.49966,
     0.28897,-0.10019,0,6.75,0.502,0.267,0.569,0.262,0.566,-0.36,-0.64,
     -0.14],
    [-0.666,0.1228,-0.01151,1.35,-0.52192,-0.48508,-0.73906,-0.48895,0.25144,
     -0.11006,0,6.75,0.502,0.267,0.569,0.262,0.566,-0.34,-0.63,-0.12],
    [-0.6901,0.1283,-0.01151,1.35,-0.45285,-0.41831,-0.66722,-0.42229,0.17976,
     -0.12858,0,6.75,0.507,0.276,0.578,0.274,0.576,-0.33,-0.62,-0.11],
    [-0.717,0.1317,-0.01151,1.35,-0.28476,-0.25022,-0.48462,-0.26092,0.06369,
     -0.15752,0,6.75,0.516,0.286,0.589,0.286,0.589,-0.29,-0.64,-0.11],
    [-0.7205,0.1237,-0.01151,1.55,0.00767,0.04912,-0.20578,0.02706,0.0117,
     -0.17051,0,6.75,0.513,0.322,0.606,0.32,0.606,-0.23,-0.64,-0.11],
    [-0.7081,0.1117,-0.01151,1.68,0.20109,0.23102,0.03058,0.22193,0.04697,
     -0.15948,0,6.75,0.52,0.313,0.608,0.318,0.608,-0.25,-0.6,-0.13],
    [-0.6961,0.09884,-0.01113,1.86,0.46128,0.48661,0.30185,0.49328,0.1799,
     -0.14539,0,6.75,0.518,0.288,0.592,0.29,0.594,-0.28,-0.53,-0.18],
    [-0.583,0.04273,-0.00952,1.98,0.5718,0.59253,0.4086,0.61472,0.52729,
     -0.12964,0.00102,6.75,0.523,0.283,0.596,0.288,0.596,-0.31,-0.52,-0.19],
    [-0.5726,0.02977,-0.00837,2.07,0.51884,0.53496,0.3388,0.57747,0.6088,
     -0.13843,0.08607,6.75,0.527,0.267,0.592,0.267,0.592,-0.39,-0.52,-0.16],
    [-0.5543,0.01955,-0.0075,2.14,0.43825,0.44516,0.25356,0.5199,0.64472,
     -0.15694,0.10601,6.75,0.546,0.272,0.608,0.269,0.608,-0.44,-0.52,-0.14],
    [-0.6443,0.04394,-0.00626,2.24,0.3922,0.40602,0.21398,0.4608,0.7861,
     -0.07843,0.02262,6.75,0.541,0.267,0.603,0.267,0.603,-0.5,-0.51,-0.1],
    [-0.6914,0.0608,-0.0054,2.32,0.18957,0.19878,0.00967,0.26337,0.76837,
     -0.09054,0,6.75,0.555,0.265,0.615,0.265,0.615,-0.6,-0.5,-0.06],
    [-0.7408,0.07518,-0.00409,2.46,-0.21338,-0.19496,-0.49176,-0.10813,
     0.75179,-0.14053,0.10302,6.75,0.571,0.311,0.649,0.299,0.645,-0.69,
     -0.47,0],
    [-0.8183,0.1027,-0.00334,2.54,-0.46896,-0.43443,-0.78465,-0.3933,
     0.6788,-0.18257,0.05393,6.75,0.573,0.318,0.654,0.302,0.647,-0.7,
     -0.44,0],
    [-0.8303,0.09793,-0.00255,2.66,-0.86271,-0.79593,-1.20902,-0.88085,
     0.70689,-0.2595,0.19082,6.75,0.566,0.382,0.684,0.373,0.679,-0.72,
     -0.4,0],
    [-0.8285,0.09432,-0.00217,2.73,-1.22652,-1.15514,-1.57697,-1.27669,0.77989,
     -0.29657,0.29888,6.75,0.58,0.398,0.702,0.389,0.7,-0.73,-0.38,0],
    [-0.7844,0.07282,-0.00191,2.83,-1.82979,-1.7469,-2.22584,-1.91814,0.77966,
     -0.45384,0.67466,6.75,0.566,0.41,0.7,0.401,0.695,-0.74,-0.34,0],
    [-0.6854,0.03758,-0.00191,2.89,-2.24656,-2.15906,-2.58228,-2.38168,1.24961,
     -0.35874,0.79508,6.75,0.583,0.394,0.702,0.385,0.698,-0.75,-0.31,0],
    [-0.5096,-0.02391,-0.00191,2.93,-1.28408,-1.2127,-1.50904,-1.41093,0.14271,
     -0.39006,0,8.5,0.601,0.414,0.73,0.437,0.744,-0.75,-0.291,0],
    [-0.3724,-0.06568,-0.00191,3,-1.43145,-1.31632,-1.81022,-1.59217,0.52407,
     -0.37578,0,8.5,0.626,0.465,0.781,0.477,0.787,-0.692,-0.247,0],
    [-0.09824,-0.138,-0.00191,3.04,-2.15446,-2.16137,-2.53323,-2.14635,0.40387,
     -0.48492,0,8.5,0.645,0.355,0.735,0.477,0.801,-0.65,-0.215,0]])

Boore_08_coefficient = Boore_08_coefficient_raw.transpose()

PGA_BA08 = 0
Boore_08_coefficient_period=[0.0,0.01,0.02,0.03,0.05,0.075,0.1,0.15,0.2,0.25,
                             0.3,0.4,0.5,0.75,1.,1.5,2.,3.,4.,5.,7.5,10.]
assert Boore_08_coefficient_period[PGA_BA08] == 0.0

Boore_08_sigma_coefficient=[[
    0.566, 0.569, 0.569, 0.578, 0.589, 0.606, 0.608, 0.592, 0.596, 0.592,
    0.608,
    0.603, 0.615, 0.649, 0.654, 0.684, 0.702, 0.7, 0.702, 0.73, 0.781, 0.735]]

Boore_08_interpolation=linear_interpolation

Boore_08_sigma_coefficient_period = [
    0.0,0.01,0.02,0.03,0.05,0.075,0.1,0.15,0.2,0.25,
    0.3,0.4,0.5,0.75,1.,1.5,2.,3.,4.,5.,7.5,10.]

Boore_08_sigma_coefficient_interpolation=linear_interpolation

# DEPENDENT ON EACH OTHER #
VREF_BOORE_08 = 760. # m/s
V1_BOORE_08 = 180. #  m/s
V2_BOORE_08 = 300. #  m/s
RECIP_LOG_V1_DIV_V2 =  -1.95761518897 # 1/log(v1/v2)
RECIP_LOG_V2_DIV_VREF = -1.07580561109 #1/log(V2_BOORE_08/VREF_BOORE_08)
# DEPENDENT ON EACH OTHER #


# faulting type flag encodings
#                            'type':     (e2, e3, e4)
Boore_08_faulting_flags = {'reverse':    (0, 0, 1),
                             'normal':     (0, 1, 0),
                             'strike_slip': (1, 0, 0)}

# generate 'Boore_08_fault_type' from the dictionary above
tmp = []
for (k, v) in Boore_08_faulting_flags.iteritems():
    index = ground_motion_misc.FaultTypeDictionary[k]
    tmp.append((index, v))

# sort and make array in correct index order
tmp2 = []
tmp.sort()
for (_, flags) in tmp:
    tmp2.append(flags)
Boore_08_fault_type = array(tmp2)
del tmp, tmp2

def Boore_08_distribution(**kwargs):
    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    Vs30 = kwargs['Vs30']
    fault_type = kwargs['fault_type']	        # event-specific

    if Vs30 is None:
        raise Exception, "Vs30 value unknown"       
        
    # An expensive way of showing what the dimensions must be?
    num_sites,num_events=distance.shape[0:2]

    num_periods=coefficient.shape[3]
    assert coefficient.shape==(20,1,1,num_periods)
    #assert sigma_coefficient.shape==(3,1,1,num_periods)
    assert mag.shape==(1,num_events,1) # (num_sites,num_events,1)?
    assert distance.shape==(num_sites,num_events,1)

    c1, c2, c3, h, e1 = coefficient[:5]
    e2, e3, e4 = coefficient[5:8]
    e5, e6, e7 = coefficient[8:11]
    mh, sig, tu, sigtu, tm, sigtm, blin, b1, b2 = coefficient[11:]

    c1_pga, c2_pga, c3_pga, h_pga = Boore_08_coefficient_raw[PGA_BA08][0:4]
    e1_pga = Boore_08_coefficient_raw[PGA_BA08][4:5]
    e2_pga, e3_pga, e4_pga = Boore_08_coefficient_raw[PGA_BA08][5:8]
    e5_pga, e6_pga, e7_pga = Boore_08_coefficient_raw[PGA_BA08][8:11]
    mh_pga, sig_pga = Boore_08_coefficient_raw[PGA_BA08][11:13]
    tu_pga, sigtu_pga = Boore_08_coefficient_raw[PGA_BA08][13:15]
    tm_pga, sigtm_pga, blin_pga = Boore_08_coefficient_raw[PGA_BA08][15:18]
    b1_pga, b2_pga = Boore_08_coefficient_raw[PGA_BA08][18:20]
    fd = fd_Boore_08(c1, c2, c3, distance, h, mag)
    fd_pga = fd_Boore_08(c1_pga, c2_pga, c3_pga, distance, h, mag)

    fm = fm_Boore_08(e1, e2, e3, e4, e5, e6, e7, mag, mh, fault_type)
    fm_pga = fm_Boore_08(e1_pga, e2_pga, e3_pga, e4_pga,
                         e5_pga, e6_pga, e7_pga, mag, mh_pga, fault_type)
    
    bnl = bnl_Boore_08(b1, b2, Vs30)

    pga4nl = exp(fd_pga + fm_pga)
    fs = fs_Boore_08(blin, pga4nl, bnl, Vs30)
    
    log_mean = fd + fm + fs    # BA08 (1)
    
    log_sigma = ones((log_mean.shape))*sigtu
    return log_mean,log_sigma

def fd_Boore_08(c1, c2, c3, distance, h, mag):  
    mref = 4.5  
    rref = 1.0 # km     
    r = sqrt(distance**2 + h**2) # BA08 (4)
    fd = (c1 + c2*(mag - mref))* log(r/rref) + c3*(r - rref) # BA08 (4)
    return fd

def fm_Boore_08(e1, e2, e3, e4, e5, e6, e7, mag, mh, fault_type):
    """
    Calculates equations (5a) and (5b) from the Boore 08 paper.

    Precondition;
    mag, mh and fault_type must have the same dimensions.
    """
    mag = asarray(mag)
    # Note, no distance, so it is the same for all sites.
    # Cache to speed this.
    # get flag values from 'fault_type'
    E2 = Boore_08_fault_type[:,0][fault_type]
    E3 = Boore_08_fault_type[:,1][fault_type]
    E4 = Boore_08_fault_type[:,2][fault_type]
    temp = E2*e2+E3*e3+E4*e4
    # BA08 (5a) & (5b) mod.
    # Note the ( + 0*e1) is to get the index shape correct.
    fm = where(mag + 0*e1<= mh,
               temp + e5*(mag - mh) + e6*(mag - mh)**2,
               temp + e7*(mag - mh))               
    return fm

# def memoize(function):
#     b1 = None
#     b2 = 'hear'
#     Vs30 = None
#     rv = None
#     print "here"
#     def wrapper(*args):
#         print "args", args
#         print "b1", b1 # Error, b1 is not defined.
#         if args[0] is b1:
#             print "There"
#             return memo[args]
#         else:
#             print "doing calc"
#             rv = function(*args)
#             b1 = args[0]
#             return rv
        
#     return wrapper

#@memoize
def bnl_Boore_08(b1, b2, Vs30):
    # Should memoize the answer.
    Vs30 = float(Vs30)
    # get bnl   
    if Vs30 <= V1_BOORE_08:
        bnl = b1  # BA08 (13a)
    elif Vs30 <= V2_BOORE_08:
        # BA08 (13b)
        bnl = (b1-b2)*log(Vs30/V2_BOORE_08)*RECIP_LOG_V1_DIV_V2 + b2
    elif Vs30 < VREF_BOORE_08:   
        bnl = b2*log(Vs30/VREF_BOORE_08)*RECIP_LOG_V2_DIV_VREF  # BA08 (13c)
    else:
        bnl = 0.0    # BA08 (13d)
    return bnl
 
def fs_Boore_08(blin, pga4nl, bnl, Vs30):
    pga4nl = asarray(pga4nl)
    
    # DEPENDENT ON EACH OTHER #
    a1 = 0.03
    a2 = 0.09
    dx = 1.09861228867 #log(a2/a1)   # BA08 (11)
    pgalow = 0.06
    LOG_A2_DIV_PGALOW = 0.405465108108
    RECIP_DX_POW_2 = 0.828535449687 # 1/dx**2
    RECIP_DX_POW_3 = 0.754165466955 # 1/dx**3
    # DEPENDENT ON EACH OTHER #
    
    dy = bnl*LOG_A2_DIV_PGALOW  # hard code this log   # BA08 (12)
    flin = blin * log(Vs30/VREF_BOORE_08)   # BA08 (7)

    # Note, the +0*pga4nl below is to get the array size right
    # It does not effect the calculation.
    # With regards to the calculation, c and d are set to 0 if
    # pga4nl <= a1.  This is so 8a and 8b can be combined into
    # one equation.
    c = where(pga4nl <= a1,
                0,
                (3*dy - (bnl+0*pga4nl)*dx)*RECIP_DX_POW_2 ) # BA08 (9)
    d = where((pga4nl <= a1),
                0,
                -(2*dy - (bnl+0*pga4nl)*dx) *RECIP_DX_POW_3 ) # BA08 (10)
    
     # BA08 (8)
    fnl = where((pga4nl <= a2),
                bnl*log(pgalow/0.1) + c*(log(pga4nl/a1))**2 + \
                d*(log(pga4nl/a1))**3,
                bnl*log(pga4nl/0.1) ) 
 
    return flin + fnl   # BA08 (6)


Boore_08_distance_type='Joyner_Boore'
Boore_08_magnitude_type='Mw'

Boore_08_uses_Vs30 = True

Boore_08_args=[
    Boore_08_distribution,
    Boore_08_magnitude_type,
    Boore_08_distance_type,
    
    Boore_08_coefficient,
    Boore_08_coefficient_period,
    Boore_08_interpolation,
    
    Boore_08_sigma_coefficient,
    Boore_08_sigma_coefficient_period,
    Boore_08_sigma_coefficient_interpolation,

    Boore_08_uses_Vs30]

ground_motion_init['Boore_08'] = Boore_08_args

#***************  End of Boore_08 MODEL  ************


#***************  START COMMON_SOMMERVILLE BLOCK  ************

Somerville09_interpolation=linear_interpolation

Somerville09_sigma_coefficient_interpolation=linear_interpolation

def Somerville09_distribution(**kwargs):

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  Vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    # An expensive way of showing what the dimensions must be?
    num_sites,num_events=distance.shape[0:2]
    num_periods=coefficient.shape[3]
    assert coefficient.shape==(8,1,1,num_periods)
    #assert sigma_coefficient.shape==(3,1,1,num_periods)
    assert mag.shape==(1,num_events,1) # (num_sites,num_events,1)?
    assert distance.shape==(num_sites,num_events,1)

    log_mean = Somerville09_log_mean(coefficient, mag, distance)
    num_events = distance.shape[1]
    log_sigma = tile(sigma_coefficient[0],(1,num_events,1))
    assert isfinite(log_mean).all()
    return log_mean,log_sigma

def Somerville09_log_mean(coefficient, mag, distance):
    c1, c2, c3, c4, c5, c6, c7, c8 = coefficient
    m1 = 6.4
    mag = asarray(mag)
    distance = asarray(distance)
    ln_R = log((distance**2 + 36.0)**0.5)
    
    mag_neg_m1 = (mag - m1)
    # Note the ( + 0*e1) is to get the index shape correct.
    T2 = where(mag + 0*c2 < m1,
               c2*mag_neg_m1,
               c7*mag_neg_m1)
    # ln_R1 = log((r1**2 + h**2)**0.5)   
    # ln_R1 = log((50**2 + 6**2)**0.5)
    ln_R1 = 3.9191716577785582
    # To get the index shape correct
    ln_R1 = ln_R1 + 0*distance
    T6 = where(distance + 0*c6 < 50.0,
               0,
               c6*(ln_R-ln_R1))
    T3 = where(distance + 0*c3 < 50.0,
               c3*ln_R,
               c3*ln_R1)
    log_mean = c1 + T2 + T3 + c4*mag_neg_m1*ln_R + c5*distance + T6 + \
               c8*(8.5 - mag)**2
    return log_mean

Somerville09_distance_type='Joyner_Boore'
Somerville09_magnitude_type='Mw'

#***************  END COMMON_SOMMERVILLE BLOCK  ************

#***************  Start of Somerville_Yilgarn MODEL  ************
# dimension = (period, coeffiecient)
Somerville09_Yilgarn_coefficient_raw = array([
    [1.5456,1.4565,-1.1151,0.1664,-0.00567,-1.049,1.0553,0.2],
    [1.5551,1.4638,-1.1146,0.1662,-0.00568,-1.0484,1.0585,0.2014],
    [2.338,1.3806,-1.2297,0.1801,-0.00467,-1.3985,0.9599,0.2013],
    [2.4809,1.3754,-1.1762,0.1712,-0.00542,-1.3872,0.9693,0.1928],
    [2.3145,1.6025,-1.126,0.1715,-0.00629,-1.2791,1.0704,0.2356],
    [2.2686,1.5584,-1.0734,0.1471,-0.00709,-1.0891,1.1075,0.2067],
    [1.9707,1.6803,-1.0154,0.1456,-0.00737,-0.9193,1.1829,0.2217],
    [1.7103,1.7507,-0.9933,0.1382,-0.00746,-0.7814,1.2939,0.2379],
    [1.5231,1.6916,-0.9631,0.1333,-0.00713,-0.6733,1.2243,0.2102],
    [1.3683,1.5794,-0.9472,0.1364,-0.00677,-0.6269,1.1776,0.1895],
    [1.4018,1.2894,-0.9441,0.1436,-0.00617,-0.6707,1.0561,0.1459],
    [1.45,1.0463,-0.9488,0.1476,-0.00581,-0.687,0.9404,0.1104],
    [1.4415,0.9282,-0.9183,0.1132,-0.00576,-0.5952,0.8628,0.0406],
    [1.4038,0.6916,-0.9101,0.1348,-0.00557,-0.6239,0.7123,0.0062],
    [1.5084,0.758,-0.9901,0.1126,-0.00458,-0.6904,0.6859,-0.0563],
    [2.1063,0.3818,-1.0868,0.0795,-0.00406,-0.9034,0.6185,-0.1825],
    [2.5579,-0.8427,-0.8181,0.0765,-0.0022,-1.3532,-0.2544,-0.4666],
    [2.396,-1.3995,-0.7044,0.0677,-0.00366,-0.9086,-0.6432,-0.596],
    [0.9604,-0.4612,-0.7045,0.0645,-0.00429,-0.5119,-0.1643,-0.4631],
    [0.1219,-0.0698,-0.7591,0.0849,-0.00374,-0.4145,0.1235,-0.3925],
    [-0.8424,0.5316,-0.796,0.1033,-0.0018,-0.6213,0.5368,-0.2757],
    [-1.9226,0.6376,-0.819,0.1455,-0.00066,-0.7574,0.6902,-0.2329],
    [-2.6033,0.5906,-0.8094,0.1609,-0.00106,-0.6855,0.7035,-0.2291]])

# dimension = (coeffiecient, period)
Somerville09_Yilgarn_coefficient = Somerville09_Yilgarn_coefficient_raw.transpose()

Somerville09_Yilgarn_sigma_coefficient=[[
    0.5513, 0.5512, 0.551, 0.5508 ,0.5509, 0.551, 0.5514, 0.5529, 0.5544,
    0.5558, 0.5583, 0.5602, 0.5614, 0.5636, 0.5878, 0.6817, 0.8514,
    0.8646, 0.8424, 0.8225, 0.8088, 0.7808, 0.7624
    ]]

Somerville09_Yilgarn_coefficient_period=[
    0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3003,
   0.4, 0.5, 0.75, 1., 1.4993, 2., 3.003, 4., 5., 7.5019, 10.,]

Somerville09_Yilgarn_sigma_coefficient_period=[
   0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3003,
   0.4, 0.5, 0.75, 1., 1.4993, 2., 3.003, 4., 5., 7.5019, 10.,]

Somerville09_Yilgarn_uses_Vs30 = False

Somerville09_Yilgarn_args=[
    Somerville09_distribution,
    Somerville09_magnitude_type,
    Somerville09_distance_type,
    
    Somerville09_Yilgarn_coefficient,
    Somerville09_Yilgarn_coefficient_period,
    Somerville09_interpolation,
    
    Somerville09_Yilgarn_sigma_coefficient,
    Somerville09_Yilgarn_sigma_coefficient_period,
    Somerville09_sigma_coefficient_interpolation,

    Somerville09_Yilgarn_uses_Vs30]

ground_motion_init['Somerville09_Yilgarn'] = Somerville09_Yilgarn_args
#***************  End of Somerville_Yilgarn MODEL   ************
#***************  Start of Somerville_Non_Cratonic MODEL   ************
# dimension = (period, coeffiecient)
Somerville09_Non_Cratonic_coefficient_raw = array([
    [1.03780,-0.03970,-0.79430,0.14450,-0.00618,-0.72540,-0.03590,-0.09730],
    [1.05360,-0.04190,-0.79390,0.14450,-0.00619,-0.72660,-0.03940,-0.09740],
    [1.05680,-0.03920,-0.79680,0.14550,-0.00617,-0.73230,-0.03930,-0.09600],
    [1.13530,-0.04790,-0.80920,0.15000,-0.00610,-0.76410,-0.05710,-0.09210],
    [1.30000,-0.07020,-0.83150,0.15920,-0.00599,-0.82850,-0.09810,-0.08530],
    [1.47680,-0.09310,-0.83330,0.15600,-0.00606,-0.86740,-0.12740,-0.09130],
    [1.70220,-0.05160,-0.80720,0.14560,-0.00655,-0.87690,-0.10970,-0.08690],
    [1.65720,0.15080,-0.77590,0.13100,-0.00708,-0.77830,0.01690,-0.05980],
    [1.94440,-0.09620,-0.75000,0.11670,-0.00698,-0.69490,-0.13320,-0.12530],
    [1.82720,-0.06230,-0.73430,0.11940,-0.00677,-0.64380,-0.09570,-0.11920],
    [1.74380,-0.02530,-0.72480,0.11950,-0.00646,-0.63740,-0.06250,-0.11650],
    [1.80560,-0.27020,-0.73190,0.13490,-0.00606,-0.66440,-0.17470,-0.14340],
    [1.88750,-0.37820,-0.70580,0.09960,-0.00589,-0.58770,-0.24420,-0.21890],
    [2.03760,-0.79590, -0.69730,0.11470,-0.00565,-0.59990,-0.48670,-0.29690],
    [1.93060,-0.80280,-0.74510,0.11220,-0.00503,-0.59460,-0.50120,-0.34990],
    [1.60380,-0.47800,-0.86950,0.07320,-0.00569,-0.41590,0.06360,-0.33730],
    [0.47740,0.90960,-1.02440,0.11060,-0.00652,-0.19000,1.09610,-0.10660],
    [-0.25810,1.37770,-1.01000,0.10310,-0.00539,-0.27340,1.50330,-0.04530],
    [-0.96360,1.14690,-0.88530,0.10380,-0.00478,-0.40420,1.54130,-0.11020],
    [-1.46140,1.07950,-0.80490,0.10960,-0.00395,-0.46040,1.41960,-0.14700],
    [-1.61160,0.74860,-0.78100,0.09650,-0.00307,-0.46490,1.24090,-0.22170],
    [-2.35310,0.35190,-0.64340,0.09590,-0.00138,-0.68260,0.92880,-0.31230],
    [-3.26140,0.69730,-0.62760,0.12920,-0.00155,-0.61980,1.01050,-0.24550]])


# dimension = (coeffiecient, period)
Somerville09_Non_Cratonic_coefficient = Somerville09_Non_Cratonic_coefficient_raw.transpose()

Somerville09_Non_Cratonic_sigma_coefficient=[[
    0.5513, 0.5512, 0.551, 0.5508 ,0.5509, 0.551, 0.5514, 0.5529, 0.5544,
    0.5558, 0.5583, 0.5602, 0.5614, 0.5636, 0.5878, 0.6817, 0.8514,
    0.8646, 0.8424, 0.8225, 0.8088, 0.7808, 0.7624
    ]]

Somerville09_Non_Cratonic_coefficient_period=[
    0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3003,
   0.4, 0.5, 0.75, 1., 1.4993, 2., 3.003, 4., 5., 7.5019, 10.,]

Somerville09_Non_Cratonic_sigma_coefficient_period=[
   0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3003,
   0.4, 0.5, 0.75, 1., 1.4993, 2., 3.003, 4., 5., 7.5019, 10.,]

Somerville09_Non_Cratonic_uses_Vs30 = False

Somerville09_Non_Cratonic_args=[
    Somerville09_distribution,
    Somerville09_magnitude_type,
    Somerville09_distance_type,
    
    Somerville09_Non_Cratonic_coefficient,
    Somerville09_Non_Cratonic_coefficient_period,
    Somerville09_interpolation,
    
    Somerville09_Non_Cratonic_sigma_coefficient,
    Somerville09_Non_Cratonic_sigma_coefficient_period,
    Somerville09_sigma_coefficient_interpolation,

    Somerville09_Non_Cratonic_uses_Vs30]

ground_motion_init['Somerville09_Non_Cratonic'] = Somerville09_Non_Cratonic_args
#***************  End of Somerville_Non_Cratonic MODEL   ************

#########################  Start of Liang_2008 model  ##########################

# conversion factor: ln mm/s/s -> ln g (log(9.80665 * 1000)
LnMmss2Lng = math.log(9.80665*1000)


def Liang_2008_distribution(**kwargs):
    """The Liang_2008 model function.

    kwargs  dictionary os parameters, expect:
                mag, distance, coefficient, sigma_coefficient

    The algorithm here is taken from [1], page 399.

    Due to the equation diverging at distance == 0, we assume any distance
    less than 10km is 10km.

    [1] Liang, J.Z., Hao, H., Gaull, B.A., and Sinadinovskic, C. [2008]
        "Estimation of Strong Ground Motions in Southwest Western Australia
        with a Combined Greens Function and Stochastic Approach",
        Journal of Earthquake Engineering, 12:3, 382-405
    """

    # get args
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    # check some shapes (num_periods should be 1 below)
    num_periods = coefficient.shape[3]
    assert coefficient.shape == (5, 1, 1, num_periods)
    assert sigma_coefficient.shape == (2, 1, 1, num_periods)

    # Force a lower limit for distance of 10km
    # eg, if distance is 5km, assume 10km
    distance = where(distance < 10.0, 10.0, distance)

    # calculate result in ln(mm/s/s)
    (a, b, c, d, e) = coefficient
    log_mean = a + b*mag + c*distance + d*log(distance) + e*mag*log(distance)
    num_events = distance.shape[1]
    log_sigma = tile(sigma_coefficient[0],(1,num_events,1))

    # return mean as ln(g)
    return (log_mean - LnMmss2Lng, log_sigma - LnMmss2Lng)

Liang_2008_magnitude_type='ML'
Liang_2008_distance_type='Epicentral'

# data here has dim = (#periods, #coefficients)
tmp = array([[  3.688, 0.832, -0.016, -1.374, +0.147], # period=0.0, from eqn 22
             [  1.776, 1.253, -0.016, -0.294, -0.028],
             [  1.598, 1.312, -0.010, -0.507, -0.028],
             [  1.939, 1.279, -0.005, -0.706, -0.018],
             [  1.570, 1.243, -0.008, -0.571, -0.014],
             [  1.102, 1.322, -0.008, -0.502, -0.024],
             [  1.310, 1.321, -0.006, -0.623, -0.024],
             [  1.361, 1.335, -0.006, -0.688, -0.021],
             [  1.147, 1.322, -0.010, -0.611, -0.012],
             [  1.021, 1.289, -0.013, -0.579,  0.004],
             [  0.476, 1.330, -0.016, -0.419, -0.002],
             [ -0.323, 1.430, -0.018, -0.175, -0.033],
             [ -0.857, 1.487, -0.019, -0.050, -0.045],
             [ -1.371, 1.554, -0.019,  0.029, -0.054],
             [ -1.716, 1.602, -0.019,  0.017, -0.053],
             [ -2.124, 1.663, -0.019,  0.019, -0.055],
             [ -2.515, 1.715, -0.019,  0.047, -0.059],
             [ -3.000, 1.786, -0.019,  0.116, -0.070],
             [ -3.475, 1.850, -0.019,  0.188, -0.081],
             [ -3.780, 1.885, -0.019,  0.196, -0.081],
             [ -3.901, 1.892, -0.019,  0.134, -0.070],
             [ -6.193, 2.126, -0.017, -0.199, -0.022],
             [ -7.234, 2.208, -0.016, -0.333,  0.000],
             [ -8.124, 2.287, -0.018, -0.311,  0.004],
             [ -8.704, 2.322, -0.018, -0.298,  0.009],
             [ -9.127, 2.330, -0.019, -0.332,  0.020],
             [ -9.455, 2.326, -0.019, -0.376,  0.033],
             [ -9.867, 2.346, -0.019, -0.373,  0.036],
             [-10.260, 2.364, -0.019, -0.376,  0.040],
             [-10.565, 2.380, -0.019, -0.395,  0.044],
             [-12.462, 2.477, -0.018, -0.334,  0.031],
             [-13.499, 2.527, -0.018, -0.195,  0.009]])
# convert to dim = (#coefficients, #periods)
Liang_2008_coefficient = tmp.transpose()
del tmp

# dim = (period,)
Liang_2008_coefficient_period = [0.00, 0.05, 0.10, 0.15, 0.20,
                                 0.25, 0.30, 0.35, 0.40, 0.45,
                                 0.50, 0.55, 0.60, 0.65, 0.70,
                                 0.75, 0.80, 0.85, 0.90, 0.95,
                                 1.00, 2.00, 3.00, 4.00, 5.00,
                                 6.00, 7.00, 8.00, 9.00, 10.00,
                                 20.00,30.00]

# dim = (sigmacoefficient, period)
sigma = 1.166
Liang_2008_sigma_coefficient = [[sigma,sigma], [sigma,sigma]]
Liang_2008_sigma_coefficient_period = [0.0, 1.0]

Liang_2008_interpolation = linear_interpolation

Liang_2008_uses_Vs30 = False

Liang_2008_args = [Liang_2008_distribution,
                   Liang_2008_magnitude_type,
                   Liang_2008_distance_type,
                   Liang_2008_coefficient,
                   Liang_2008_coefficient_period,
                   Liang_2008_interpolation,
                   Liang_2008_sigma_coefficient,
                   Liang_2008_sigma_coefficient_period,
                   Liang_2008_interpolation,
                   Liang_2008_uses_Vs30]

ground_motion_init['Liang_2008'] = Liang_2008_args

##########################  End of Liang_2008 model  ###########################

############################  Start of Atkinson06  #############################

# conversion factor: ln cm/s/s -> ln g
LnCmss2Lng = math.log(9.80665*100)

# conversion factor: log10 -> ln
# use this so: ln(x) = log10(X) / log10(e)
Log102Ln = math.log10(math.e)

# other constants (these are scale distances?)
Atkinson06_R0 = 10.0
Atkinson06_R1 = 70.0
Atkinson06_R2 = 140.0

# computed constants
Log10Atkinson06_R1 = math.log10(Atkinson06_R1)


def Atkinson06_basic(**kwargs):
    """The basic Atkinson06 model function.

    kwargs  dictionary of parameters, expect:
                mag, distance, coefficient, sigma_coefficient, S

    The algorithm here is taken from [1], page 2191 and returns results
    that are log10 cm/s/s.

    This algorithm does not compute the S parameter but takes it from outside.

    [1] Atkinson, G.M., and Boore, D.M. [2006] "Earthquake Ground-Motion
        Prediction Equations for Eastern North America", Bulletin of the
        Seismological Society of America, Vol. 96, pp 2181-2205
    """

    # get args
    M = kwargs['mag']
    Rcd = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    S = kwargs['S']

    # intermediate calculated coefficients
    tmp = log10(Atkinson06_R0/Rcd)
    f0 = where(tmp < 0, 0, tmp)

    tmp = log10(Rcd)
    f1 = where(tmp < Log10Atkinson06_R1, tmp, Log10Atkinson06_R1)

    tmp = log10(Rcd/Atkinson06_R2)
    f2 = where(tmp < 0, 0, tmp)
    del tmp
    
    # calculate result in log10(cm/s/s)
    (c1, c2, c3, c4, c5, c6, c7, c8, c9, c10) = coefficient[:10,...]

    log_mean = (c1 + c2*M + c3*M*M + (c4 + c5*M)*f1 + (c6 + c7*M)*f2 +
                   (c8 + c9*M)*f0 + c10*Rcd + S)

    # there is only a single value, just create array of required size
    log_sigma = ones_like(log_mean) * sigma_coefficient[0,0,0,0]
#    num_events = M.shape[1]
#    num_sites = Rcd.shape[0]
#    num_periods = coefficient.shape[3]
#    log_sigma = tile(sigma_coefficient[0,0,0,0], (num_sites,num_events,num_periods))

    return (log_mean, log_sigma)

def Atkinson06_hard_bedrock_distribution(**kwargs):
    """The Atkinson06_hard_bedrock model function.

    kwargs  dictionary of parameters, expect:
                mag, distance, coefficient, sigma_coefficient

    This function just calls Atkinson06_basic() with S=0 (bedrock algorithm)
    and converts the result to ln g.
    """

    # get args
    try:
        M = kwargs['mag']
        Rcd = kwargs['distance']
        coefficient = kwargs['coefficient']
        sigma_coefficient = kwargs['sigma_coefficient']
    except KeyError, e:
        msg = ('kwargs dictionary to Atkinson06_basic() '
               'is missing a parameter: %s' % e)
        raise RuntimeError(msg)

    # check we have the right shapes
    num_sites = Rcd.shape[0]
    num_events = M.shape[1]
    num_periods = coefficient.shape[3]

    msg = 'Expected %s.shape=%s, got %s'

    assert M.shape == (1, num_events, 1), (msg
               % ('M', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(M.shape)))
    assert Rcd.shape == (num_sites, num_events, 1), (msg
               % ('Rcd', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Rcd.shape)))
    assert coefficient.shape == (13, 1, 1, num_periods), (msg
               % ('coefficient', '(13,1,1,%d)' % num_periods,
                  str(coefficient.shape)))
    assert sigma_coefficient.shape == (2, 1, 1, num_periods), (msg
               % ('sigma_coefficient', '(2,1,1,%d)' % num_periods,
                  str(sigma_coefficient.shape)))

    # get result in log10(cm/s/s)
    (log_mean, log_sigma) = Atkinson06_basic(S=0.0, **kwargs)

    # convert to g and natural log
    log_mean = log_mean/Log102Ln - LnCmss2Lng
    log_sigma = log_sigma/Log102Ln - LnCmss2Lng

    # check result has right dimensions
    num_sites = Rcd.shape[0]
    assert log_mean.shape == (num_sites, num_events, num_periods), (msg
               % ('log_mean', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(log_mean.shape)))
    assert log_sigma.shape == (num_sites, num_events, num_periods), (msg
               % ('log_sigma', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(log_sigma.shape)))

    return (log_mean, log_sigma)

# constants for S calculations
Atkinson06_Vref = array([[[760.0]]])
Atkinson06_V2 = 300.0
Atkinson06_V1 = 180.0
Atkinson06_logV1divV2 = math.log(Atkinson06_V1 / Atkinson06_V2)
Atkinson06_logV2divVref = math.log(Atkinson06_V2 / Atkinson06_Vref)

def Atkinson06_calcS(pgaBC, **kwargs):
    """Calculate the S parameter for soil.

    pgaBC   the pgaBC value to use
    kwargs  dictionary of parameters, expect:
                coefficient, Vs30
    """

    # get args
    coefficient = kwargs['coefficient']
    Vs30 = array(kwargs['Vs30'])

    # check we have the right shapes
    num_periods = coefficient.shape[3]
    assert coefficient.shape == (13, 1, 1, num_periods)

    # get the Blin, B1 and B2 coefficients.
    (Blin, B1, B2) = coefficient[-3:]

    # ensure Vs30 is one-dimensional only, then ensure canonical shape
    assert len(Vs30.shape) == 1, (msg
               % ('Vs30', '(?,)', str(Vs30.shape)))
    #Vs30 = Vs30[:,newaxis,newaxis] + zeros(B1.shape)
    Vs30 = Vs30 + zeros(B1.shape)

    # get the Bnl array from eqns 8A, 8B, 8C, 8D, page 2200.
    # we do this by calculating 4 arrays for each of 8A, 8b, 8C and 8D
    # and then filling appropriate elements of resultant Bnl.
    BnlA = B1
    BnlB = (B1 - B2) * log(Vs30/Atkinson06_V2) / Atkinson06_logV1divV2 + B2
    BnlC = B2 * log(Vs30/Atkinson06_Vref) / Atkinson06_logV2divVref
    Bnl = zeros(BnlC.shape)

    Bnl = where(Vs30 <= Atkinson06_Vref, BnlC, Bnl)
    Bnl = where(Vs30 <= Atkinson06_V2, BnlB, Bnl)
    Bnl = where(Vs30 <= Atkinson06_V1, BnlA, Bnl)

    # limit element-wise pgaBC values to be >= 60
    pgaBC = where(pgaBC < 60.0, 60.0, pgaBC)

    # return the S value
    return log10(exp(Blin*log(Vs30/Atkinson06_Vref) + Bnl*log(pgaBC/100)))

def Atkinson06_soil_distribution(**kwargs):
    """The Atkinson06_soil model function.

    kwargs  dictionary of parameters, expect:
                mag, distance, coefficient, sigma_coefficient, Vs30

    This function just calls Atkinson06_basic() with a computed S value
    and converts the result to ln g.
    """

    # get required kwarg values, check shapes
    try:
        mag = kwargs['mag']
        distance = kwargs['distance']
        Vs30 = kwargs['Vs30']
        coefficient = kwargs['coefficient']
        sigma_coefficient = kwargs['sigma_coefficient']
    except KeyError, e:
        print('kwargs dictionary to Atkinson06_soil_distribution() '
              'is missing a parameter: %s' % e)
        raise

    # check we have the right shapes
    num_sites = distance.shape[0]
    num_events = mag.shape[1]
    num_periods = coefficient.shape[3]

    msg = 'Expected %s.shape=%s, got %s'

    assert mag.shape == (1, num_events, 1), (msg
               % ('mag', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(mag.shape)))
    assert distance.shape == (num_sites, num_events, 1), (msg
               % ('distance', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(distance.shape)))
    assert coefficient.shape == (13, 1, 1, num_periods), (msg
               % ('coefficient', '(13,1,1,%d)' % num_periods,
                  str(coefficient.shape)))
    assert sigma_coefficient.shape == (2, 1, 1, num_periods), (msg
               % ('sigma_coefficient', '(2,1,1,%d)' % num_periods,
                  str(sigma_coefficient.shape)))

    # ensure Vs30 is one-dimensional only
    assert len(Vs30.shape) == 1, (msg
               % ('Vs30', '(?,)', str(Vs30.shape)))

    # calculate pgaBC here, use PGA (period=0.0) coefficients
    (pgaBC, _) = Atkinson06_basic(mag=kwargs['mag'],
                                  distance=kwargs['distance'],
                                  coefficient=Atkinson06_coefficient_pga,
                                  sigma_coefficient=kwargs['sigma_coefficient'],
                                  S=0.0)

    # check that pgaBC has the right shape
    assert pgaBC.shape == distance.shape

    # compute S parameter
    S = Atkinson06_calcS(pgaBC, **kwargs)

    # get result in log10(cm/s/s)
    (log_mean, log_sigma) = Atkinson06_basic(S=S, **kwargs)

    # convert to g and natural log
    log_mean = log_mean/Log102Ln - LnCmss2Lng
    log_sigma = log_sigma/Log102Ln - LnCmss2Lng

    # check result has right dimensions
    num_sites = distance.shape[0]
    assert log_mean.shape == (num_sites, num_events, num_periods), (msg
               % ('log_mean', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(log_mean.shape)))
    assert log_sigma.shape == (num_sites, num_events, num_periods), (msg
               % ('log_sigma', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(log_sigma.shape)))

    return (log_mean, log_sigma)

def Atkinson06_bc_boundary_bedrock(**kwargs):
    """The Atkinson06_bc_boundary_bedrock model function.

    kwargs  dictionary of parameters, expect:
                mag, distance, coefficient, sigma_coefficient

    This function just calls Atkinson06_basic() with S=0 (bedrock algorithm)
    and converts the result to ln g.

    This appears identical to the Atkinson06_hard_bedrock_distribution()
    function but gets passed coefficients from tables 9 and 8 (not 6 and 8).
    """

    # get args
    try:
        M = kwargs['mag']
        Rcd = kwargs['distance']
        coefficient = kwargs['coefficient']
        sigma_coefficient = kwargs['sigma_coefficient']
    except KeyError, e:
        msg = ('kwargs dictionary to Atkinson06_basic() '
               'is missing a parameter: %s' % e)
        raise RuntimeError(msg)

    # check we have the right shapes
    num_sites = Rcd.shape[0]
    num_events = M.shape[1]
    num_periods = coefficient.shape[3]

    msg = 'Expected %s.shape=%s, got %s'

    assert M.shape == (1, num_events, 1), (msg
               % ('M', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(M.shape)))
    assert Rcd.shape == (num_sites, num_events, 1), (msg
               % ('Rcd', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Rcd.shape)))
    assert coefficient.shape == (13, 1, 1, num_periods), (msg
               % ('coefficient', '(13,1,1,%d)' % num_periods,
                  str(coefficient.shape)))
    assert sigma_coefficient.shape == (2, 1, 1, num_periods), (msg
               % ('sigma_coefficient', '(2,1,1,%d)' % num_periods,
                  str(sigma_coefficient.shape)))

    # get result in log10(cm/s/s)
    (log_mean, log_sigma) = Atkinson06_basic(S=0.0, **kwargs)

    # convert to g and natural log
    log_mean = log_mean/Log102Ln - LnCmss2Lng
    log_sigma = log_sigma/Log102Ln - LnCmss2Lng

    # check result has right dimensions
    num_sites = Rcd.shape[0]
    assert log_mean.shape == (num_sites, num_events, num_periods), (msg
               % ('log_mean', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(log_mean.shape)))
    assert log_sigma.shape == (num_sites, num_events, num_periods), (msg
               % ('log_sigma', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(log_sigma.shape)))

    return (log_mean, log_sigma)


Atkinson06_magnitude_type = 'Mw'
Atkinson06_distance_type = 'Rupture'

# dimension = (#periods, #coefficients)
Atkinson06_Table6 = array([
#  c1        c2         c3         c4        c5         c6        c7         c8         c9         c10
[-5.41E+00, 1.71E+00, -9.01E-02, -2.54E+00, 2.27E-01, -1.27E+00, 1.16E-01,  9.79E-01, -1.77E-01, -1.76E-04],  # 5.00
[-5.79E+00, 1.92E+00, -1.07E-01, -2.44E+00, 2.11E-01, -1.16E+00, 1.02E-01,  1.01E+00, -1.82E-01, -2.01E-04],  # 4.00
[-6.04E+00, 2.08E+00, -1.22E-01, -2.37E+00, 2.00E-01, -1.07E+00, 8.95E-02,  1.00E+00, -1.80E-01, -2.31E-04],  # 3.13
[-6.17E+00, 2.21E+00, -1.35E-01, -2.30E+00, 1.90E-01, -9.86E-01, 7.86E-02,  9.68E-01, -1.77E-01, -2.82E-04],  # 2.50
[-6.18E+00, 2.30E+00, -1.44E-01, -2.22E+00, 1.77E-01, -9.37E-01, 7.07E-02,  9.52E-01, -1.77E-01, -3.22E-04],  # 2.00
[-6.04E+00, 2.34E+00, -1.50E-01, -2.16E+00, 1.66E-01, -8.70E-01, 6.05E-02,  9.21E-01, -1.73E-01, -3.75E-04],  # 1.59
[-5.72E+00, 2.32E+00, -1.51E-01, -2.10E+00, 1.57E-01, -8.20E-01, 5.19E-02,  8.56E-01, -1.66E-01, -4.33E-04],  # 1.25
[-5.27E+00, 2.26E+00, -1.48E-01, -2.07E+00, 1.50E-01, -8.13E-01, 4.67E-02,  8.26E-01, -1.62E-01, -4.86E-04],  # 1.00
[-4.60E+00, 2.13E+00, -1.41E-01, -2.06E+00, 1.47E-01, -7.97E-01, 4.35E-02,  7.75E-01, -1.56E-01, -5.79E-04],  # 0.794
[-3.92E+00, 1.99E+00, -1.31E-01, -2.05E+00, 1.42E-01, -7.82E-01, 4.30E-02,  7.88E-01, -1.59E-01, -6.95E-04],  # 0.629
[-3.22E+00, 1.83E+00, -1.20E-01, -2.02E+00, 1.34E-01, -8.13E-01, 4.44E-02,  8.84E-01, -1.75E-01, -7.70E-04],  # 0.500
[-2.44E+00, 1.65E+00, -1.08E-01, -2.05E+00, 1.36E-01, -8.43E-01, 4.48E-02,  7.39E-01, -1.56E-01, -8.51E-04],  # 0.397
[-1.72E+00, 1.48E+00, -9.74E-02, -2.08E+00, 1.38E-01, -8.89E-01, 4.87E-02,  6.10E-01, -1.39E-01, -9.54E-04],  # 0.315
[-1.12E+00, 1.34E+00, -8.72E-02, -2.08E+00, 1.35E-01, -9.71E-01, 5.63E-02,  6.14E-01, -1.43E-01, -1.06E-03],  # 0.251
[-6.15E-01, 1.23E+00, -7.89E-02, -2.09E+00, 1.31E-01, -1.12E+00, 6.79E-02,  6.06E-01, -1.46E-01, -1.13E-03],  # 0.199
[-1.46E-01, 1.12E+00, -7.14E-02, -2.12E+00, 1.30E-01, -1.30E+00, 8.31E-02,  5.62E-01, -1.44E-01, -1.18E-03],  # 0.158
[ 2.14E-01, 1.05E+00, -6.66E-02, -2.15E+00, 1.30E-01, -1.61E+00, 1.05E-01,  4.27E-01, -1.30E-01, -1.15E-03],  # 0.125
[ 4.80E-01, 1.02E+00, -6.40E-02, -2.20E+00, 1.27E-01, -2.01E+00, 1.33E-01,  3.37E-01, -1.27E-01, -1.05E-03],  # 0.100
[ 6.91E-01, 9.97E-01, -6.28E-02, -2.26E+00, 1.25E-01, -2.49E+00, 1.64E-01,  2.14E-01, -1.21E-01, -8.47E-04],  # 0.079
[ 9.11E-01, 9.80E-01, -6.21E-02, -2.36E+00, 1.26E-01, -2.97E+00, 1.91E-01,  1.07E-01, -1.17E-01, -5.79E-04],  # 0.063
[ 1.11E+00, 9.72E-01, -6.20E-02, -2.47E+00, 1.28E-01, -3.39E+00, 2.14E-01, -1.39E-01, -9.84E-02, -3.17E-04],  # 0.050
[ 1.26E+00, 9.68E-01, -6.23E-02, -2.58E+00, 1.32E-01, -3.64E+00, 2.28E-01, -3.51E-01, -8.13E-02, -1.23E-04],  # 0.040
[ 1.44E+00, 9.59E-01, -6.28E-02, -2.71E+00, 1.40E-01, -3.73E+00, 2.34E-01, -5.43E-01, -6.45E-02, -3.23E-05],  # 0.031
[ 1.52E+00, 9.60E-01, -6.35E-02, -2.81E+00, 1.46E-01, -3.65E+00, 2.36E-01, -6.54E-01, -5.50E-02, -4.85E-05],  # 0.025
[ 9.07E-01, 9.83E-01, -6.60E-02, -2.70E+00, 1.59E-01, -2.80E+00, 2.12E-01, -3.01E-01, -6.53E-02, -4.48E-04],  # 0.010 (PGA)
[ 9.07E-01, 9.83E-01, -6.60E-02, -2.70E+00, 1.59E-01, -2.80E+00, 2.12E-01, -3.01E-01, -6.53E-02, -4.48E-04]]) # 0.000 (PGA)

# dimension = (#periods, #coefficients)
#                             Blin    B1      B2
Atkinson06_Table8 = array([[-0.752, -0.300,  0.000],  # 5.00
                           [-0.745, -0.310,  0.000],  # 4.00
                           [-0.740, -0.330,  0.000],  # 3.13
                           [-0.736, -0.350,  0.000],  # 2.50
                           [-0.730, -0.375,  0.000],  # 2.00
                           [-0.726, -0.395,  0.000],  # 1.59
                           [-0.714, -0.397,  0.000],  # 1.25
                           [-0.700, -0.440,  0.000],  # 1.00
                           [-0.690, -0.465, -0.002],  # 0.794
                           [-0.670, -0.480, -0.031],  # 0.629
                           [-0.600, -0.495, -0.060],  # 0.500
                           [-0.500, -0.508, -0.095],  # 0.397
                           [-0.445, -0.513, -0.130],  # 0.315
                           [-0.390, -0.518, -0.160],  # 0.251
                           [-0.306, -0.521, -0.185],  # 0.199
                           [-0.280, -0.528, -0.185],  # 0.158
                           [-0.260, -0.560, -0.140],  # 0.125
                           [-0.250, -0.595, -0.132],  # 0.100
                           [-0.232, -0.637, -0.117],  # 0.079
                           [-0.249, -0.642, -0.105],  # 0.063
                           [-0.286, -0.643, -0.105],  # 0.050
                           [-0.314, -0.609, -0.105],  # 0.040
                           [-0.322, -0.618, -0.108],  # 0.031
                           [-0.330, -0.624, -0.115],  # 0.025
                           [-0.361, -0.641, -0.144],  # 0.010 (PGA)
                           [-0.361, -0.641, -0.144]]) # 0.000 (PGA)

Atkinson06_Table9 = array([
[-4.85E+00, 1.58E+00, -8.07E-02, -2.53E+00, 2.22E-01, -1.43E+00, 1.36E-01,  6.34E-01, -1.41E-01, -1.61E-04],  # 5.00
[-5.26E+00, 1.79E+00, -9.79E-02, -2.44E+00, 2.07E-01, -1.31E+00, 1.21E-01,  7.34E-01, -1.56E-01, -1.96E-04],  # 4.00
[-5.59E+00, 1.97E+00, -1.14E-01, -2.33E+00, 1.91E-01, -1.20E+00, 1.10E-01,  8.45E-01, -1.72E-01, -2.45E-04],  # 3.13
[-5.80E+00, 2.13E+00, -1.28E-01, -2.26E+00, 1.79E-01, -1.12E+00, 9.54E-02,  8.91E-01, -1.80E-01, -2.60E-04],  # 2.50
[-5.85E+00, 2.23E+00, -1.39E-01, -2.20E+00, 1.69E-01, -1.04E+00, 8.00E-02,  8.67E-01, -1.79E-01, -2.86E-04],  # 2.00
[-5.75E+00, 2.29E+00, -1.45E-01, -2.13E+00, 1.58E-01, -9.57E-01, 6.76E-02,  8.67E-01, -1.79E-01, -3.43E-04],  # 1.59
[-5.49E+00, 2.29E+00, -1.48E-01, -2.08E+00, 1.50E-01, -9.00E-01, 5.79E-02,  8.21E-01, -1.72E-01, -4.07E-04],  # 1.25
[-5.06E+00, 2.23E+00, -1.45E-01, -2.03E+00, 1.41E-01, -8.74E-01, 5.41E-02,  7.92E-01, -1.70E-01, -4.89E-04],  # 1.00
[-4.45E+00, 2.12E+00, -1.39E-01, -2.01E+00, 1.36E-01, -8.58E-01, 4.98E-02,  7.08E-01, -1.59E-01, -5.75E-04],  # 0.794
[-3.75E+00, 1.97E+00, -1.29E-01, -2.00E+00, 1.31E-01, -8.42E-01, 4.82E-02,  6.77E-01, -1.56E-01, -6.76E-04],  # 0.629
[-3.01E+00, 1.80E+00, -1.18E-01, -1.98E+00, 1.27E-01, -8.47E-01, 4.70E-02,  6.67E-01, -1.55E-01, -7.68E-04],  # 0.500
[-2.28E+00, 1.63E+00, -1.05E-01, -1.97E+00, 1.23E-01, -8.88E-01, 5.03E-02,  6.84E-01, -1.58E-01, -8.59E-04],  # 0.397
[-1.56E+00, 1.46E+00, -9.31E-02, -1.98E+00, 1.21E-01, -9.47E-01, 5.58E-02,  6.50E-01, -1.56E-01, -9.55E-04],  # 0.315
[-8.76E-01, 1.29E+00, -8.19E-02, -2.01E+00, 1.23E-01, -1.03E+00, 6.34E-02,  5.81E-01, -1.49E-01, -1.05E-03],  # 0.251
[-3.06E-01, 1.16E+00, -7.21E-02, -2.04E+00, 1.22E-01, -1.15E+00, 7.38E-02,  5.08E-01, -1.43E-01, -1.14E-03],  # 0.199
[ 1.19E-01, 1.06E+00, -6.47E-02, -2.05E+00, 1.19E-01, -1.36E+00, 9.16E-02,  5.16E-01, -1.50E-01, -1.18E-03],  # 0.158
[ 5.36E-01, 9.65E-01, -5.84E-02, -2.11E+00, 1.21E-01, -1.67E+00, 1.16E-01,  3.43E-01, -1.32E-01, -1.13E-03],  # 0.125
[ 7.82E-01, 9.24E-01, -5.56E-02, -2.17E+00, 1.19E-01, -2.10E+00, 1.48E-01,  2.85E-01, -1.32E-01, -9.90E-04],  # 0.100
[ 9.67E-01, 9.03E-01, -5.48E-02, -2.25E+00, 1.22E-01, -2.53E+00, 1.78E-01,  1.00E-01, -1.15E-01, -7.72E-04],  # 0.079
[ 1.11E+00, 8.88E-01, -5.39E-02, -2.33E+00, 1.23E-01, -2.88E+00, 2.01E-01, -3.19E-02, -1.07E-01, -5.48E-04],  # 0.063
[ 1.21E+00, 8.83E-01, -5.44E-02, -2.44E+00, 1.30E-01, -3.04E+00, 2.13E-01, -2.10E-01, -9.00E-02, -4.15E-04],  # 0.050
[ 1.26E+00, 8.79E-01, -5.52E-02, -2.54E+00, 1.39E-01, -2.99E+00, 2.16E-01, -3.91E-01, -6.75E-02, -3.88E-04],  # 0.040
[ 1.19E+00, 8.88E-01, -5.64E-02, -2.58E+00, 1.45E-01, -2.84E+00, 2.12E-01, -4.37E-01, -5.87E-02, -4.33E-04],  # 0.031
[ 1.05E+00, 9.03E-01, -5.77E-02, -2.57E+00, 1.48E-01, -2.65E+00, 2.07E-01, -4.08E-01, -5.77E-02, -5.12E-04],  # 0.025
[ 5.23E-01, 9.69E-01, -6.20E-02, -2.44E+00, 1.47E-01, -2.34E+00, 1.91E-01, -8.70E-02, -8.29E-02, -6.30E-04],  # 0.010, (PGA)
[ 5.23E-01, 9.69E-01, -6.20E-02, -2.44E+00, 1.47E-01, -2.34E+00, 1.91E-01, -8.70E-02, -8.29E-02, -6.30E-04]]) # 0.000, (PGA)

# join tables 6 and 8, convert to dim = (#coefficients, #periods)
Atkinson06_coefficient68 = concatenate((Atkinson06_Table6, Atkinson06_Table8), axis=1)
Atkinson06_coefficient68 = Atkinson06_coefficient68.transpose()

# join tables 9 and 8, convert to dim = (#coefficients, #periods)
Atkinson06_coefficient98 = concatenate((Atkinson06_Table9, Atkinson06_Table8), axis=1)
Atkinson06_coefficient98 = Atkinson06_coefficient98.transpose()	# used for bc_boundary_bedrock

# get tables 6+8 PGA row (ie, end row) for soil calculations
Atkinson06_coefficient_pga = reshape(Atkinson06_coefficient68[:,-1], (-1,1,1,1))

# dim = (period,)
Atkinson06_coefficient_period = [5.000, 4.000, 3.130, 2.500, 2.000,
                                 1.590, 1.250, 1.000, 0.794, 0.629,
                                 0.500, 0.397, 0.315, 0.251, 0.199,
                                 0.158, 0.125, 0.100, 0.079, 0.063,
                                 0.050, 0.040, 0.031, 0.025, 0.010,
                                 0.000]

Atkinson06_interpolation = linear_interpolation

# dim = (period,)
sigma = 0.30
Atkinson06_sigma_coefficient = [[sigma,sigma], [sigma,sigma]]
Atkinson06_sigma_coefficient_period = [0.0, 1.0]

Atkinson06_hard_bedrock_uses_Vs30 = False

ground_motion_init['Atkinson06_hard_bedrock'] = \
                        [Atkinson06_hard_bedrock_distribution,
                         Atkinson06_magnitude_type,
                         Atkinson06_distance_type,
                         Atkinson06_coefficient68,
                         Atkinson06_coefficient_period,
                         Atkinson06_interpolation,
                         Atkinson06_sigma_coefficient,
                         Atkinson06_sigma_coefficient_period,
                         Atkinson06_interpolation,
                         Atkinson06_hard_bedrock_uses_Vs30]

Atkinson06_soil_uses_Vs30 = True

ground_motion_init['Atkinson06_soil'] = [Atkinson06_soil_distribution,
                                        Atkinson06_magnitude_type,
                                        Atkinson06_distance_type,
                                        Atkinson06_coefficient68,
                                        Atkinson06_coefficient_period,
                                        Atkinson06_interpolation,
                                        Atkinson06_sigma_coefficient,
                                        Atkinson06_sigma_coefficient_period,
                                        Atkinson06_interpolation,
                                        Atkinson06_soil_uses_Vs30]

Atkinson06_bc_boundary_bedrock_uses_Vs30 = False

ground_motion_init['Atkinson06_bc_boundary_bedrock'] = \
                        [Atkinson06_bc_boundary_bedrock,
                         Atkinson06_magnitude_type,
                         Atkinson06_distance_type,
                         Atkinson06_coefficient98,
                         Atkinson06_coefficient_period,
                         Atkinson06_interpolation,
                         Atkinson06_sigma_coefficient,
                         Atkinson06_sigma_coefficient_period,
                         Atkinson06_interpolation,
                         Atkinson06_bc_boundary_bedrock_uses_Vs30]

#############################  End of Atkinson06  ##############################

##########################  Start of Chiou08 model  ############################

"""Code here is based on the FORTRAN file nga_gm_tmr_subs.for from
[www.daveboore.com/nga_gm_tmr/nga_gm_tmr_zips.zip]
"""

######
# Set up a numpy array to convert a 'fault_type' flag to an array slice
# that encodes the Frv/Fnm flags.
######

# faulting type flag encodings
#                    'type':      (Frv, Fnm)
Ch_faulting_flags = {'reverse':     (1, 0),
                     'normal':      (0, 1),
                     'strike_slip': (0, 0)}

# generate 'Ch_fault_type' from the dictionary above 

# FIXME --vvv-- DRY and just plain silly. See
# Abrahamson_Silva_1997_distribution() for a reliable and simpler way
tmp = []
for (k, v) in Ch_faulting_flags.iteritems():
    index = ground_motion_misc.FaultTypeDictionary[k]
    tmp.append((index, v))

# sort and make array in correct index order
tmp2 = []
tmp.sort()
for (_, flags) in tmp:
    tmp2.append(flags)
Ch_fault_type = array(tmp2)
del tmp, tmp2

######
# The model function.
######

def Chiou08_distribution(**kwargs):
    """The Chiou08 model.

    kwargs  dictionary of parameters, expect:
                mag, distance, fault_type, depth_to_top, Vs30, dip,
                coefficient, sigma_coefficient

    The algorithm here is taken from the code in
        [www.daveboore.com/nga_gm_tmr/nga_gm_tmr_zips.zip]
    """

    # get args
    Mw = kwargs['mag']                   # event-specific
    dist_object = kwargs['dist_object']
    fault_type = kwargs['fault_type']    # event-specific
    Ztor = kwargs['depth_to_top']        # event-specific
    Dip = kwargs['dip']                  # event-specific
    Vs30 = kwargs['Vs30']                # site-specific
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    # for testing, can pass in 'Fhw' param
    Fhw = kwargs.get('Fhw', 0)

    # assumed (for now) parameters
    AS = 0

    # Rrup, Rjb and Rx from distance object
    Rrup = dist_object.Rupture
    Rjb = dist_object.Joyner_Boore
    Rx = dist_object.Horizontal

    # check we have the right shapes
    num_sites = 1
    num_events = Mw.shape[1]
    num_periods = coefficient.shape[3]

    msg = 'Expected %s.shape=%s, got %s'

    assert Mw.shape == (1, num_events, 1), (msg
               % ('Mw', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Mw.shape)))

    # ignore first dimension of distances
    assert Rrup.shape[1:] == (num_events,), (msg
               % ('Rrup', '(?,%d)' % num_events, str(Rrup.shape)))
    assert Rjb.shape[1:] == (num_events,), (msg
               % ('Rjb', '(?,%d)' % num_events, str(Rjb.shape)))
    assert Rx.shape[1:] == (num_events,), (msg
               % ('Rx', '(?,%d)' % num_events, str(Rx.shape)))

    assert fault_type.shape == (num_sites, num_events, 1), (msg
               % ('fault_type', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(fault_type.shape)))
    assert Ztor.shape == (num_sites, num_events, 1), (msg
               % ('Ztor', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Ztor.shape)))
    assert Dip.shape == (num_sites, num_events, 1), (msg
               % ('Dip', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Dip.shape)))

    # ensure Vs30 is one-dimensional only
    assert len(Vs30.shape) == 1, (msg
               % ('Vs30', '(?,)', str(Vs30.shape)))

    assert coefficient.shape == (29, 1, 1, num_periods), (msg
               % ('coefficient', '(29,1,1,%d)' % num_periods,
                  str(coefficient.shape)))
    assert sigma_coefficient.shape == (6, 1, 1, num_periods), (msg
               % ('sigma_coefficient', '(6,1,1,%d)' % num_periods,
                  str(sigma_coefficient.shape)))

    # unpack coefficients
    (c2T, c3T, c4T, c4aT, crbT, chmT, cg3T, c1T, c1aT, c1bT, cnT, cmT, c5T,
     c6T, c7T, c7aT, c9T, c9aT, c10T, cg1T, cg2T,
     phi1T, phi2T, phi3T, phi4T, phi5T, phi6T, phi7T, phi8T) = coefficient

    (tau1T, tau2T, sig1T, sig2T, sig3T, sig4T) = sigma_coefficient

    # get flag values from 'fault_type'
    Frv = Ch_fault_type[:,0][fault_type]
    Fnm = Ch_fault_type[:,1][fault_type]

    # resize to standard form
    Rrup = Rrup[:,:,newaxis]
    Rjb = Rjb[:,:,newaxis]
    Rx = Rx[:,:,newaxis]
    Vs30 = Vs30[:,newaxis,newaxis]

    # estimate Z10 (m) from Vs30
    Z10 = conversions.convert_Vs30_to_Z10(Vs30) * 1000.0

    ######
    # CALCULATE ROCK PSA (Vs30 = 1130 m/sec)
    ######

    # Style-of-Faulting Term
    f_flt = c1T + (c1aT*Frv + c1bT*Fnm + c7T*(Ztor - 4.0))*(1.0 - AS) + (c10T + c7aT*(Ztor - 4.0))*AS

    # Magnitude Term
    f_mag = c2T*(Mw - 6.0) + ((c2T-c3T)/cnT)*log(1.0 + exp(cnT*(cmT - Mw)))

    # Distance Term

    R = sqrt(Rrup**2 + crbT**2)
    f_dis = c4T*log(Rrup + c5T*cosh(c6T*maximum(Mw-chmT,0.0))) + (c4aT-c4T)*log(R) + (cg1T + cg2T/cosh(maximum(Mw-cg3T,0.0)))*Rrup

    # Hanging-Wall Term
    f_hng = c9T*Fhw*tanh(Rx*(cos(Dip*pi/180.0)**2)/c9aT) * (1.0 - sqrt(Rjb**2+Ztor**2)/(Rrup+0.001))

    # Value of PSA on Rock (Vs30 = 1130 m/sec)
    Yref = exp(f_flt + f_mag + f_dis + f_hng)

    ######
    # CALCULATE STRONG MOTION PARAMETER
    ######

    # Site Response Term
    a = phi1T*minimum(log(Vs30/1130.0),0.0)
    b = phi2T*(exp(phi3T*(minimum(Vs30,1130.0)-360.0)) - exp(phi3T*770.0))
    c = phi4T

    f_site = a + b*log((Yref+c)/c)

    # Sediment Depth Term
    f_sed = phi5T*(1.0 - 1.0/cosh(phi6T*maximum(Z10-phi7T,0.0))) + phi8T/cosh(0.15*minimum(maximum(Z10-15.0,0.0),300.0))
    
    # Value of Ground Motion Parameter
    Y = exp(log(Yref) + f_site + f_sed)

    ######
    # CALCULATE ALEATORY UNCERTAINTY
    ######

    # Standard Deviation of Geometric Mean of ln Y

    NL0 = b*Yref/(Yref+c)
    Tau = tau1T + ((tau2T-tau1T)/2.0)*(minimum(maximum(Mw,5.0),7.0)-5.0)

    # Inferred Vs30
    Finferred = 1.0
    Fmeasured = 0.0

    SigInfer = (sig1T + ((sig2T-sig1T)/2.0)*(minimum(maximum(Mw,5.0),7.0)-5.0) + sig4T*AS)*sqrt(sig3T*Finferred + 0.7*Fmeasured + (1.0+NL0)**2)
    SigTinfer = sqrt(((1.0+NL0)**2)*Tau**2 + SigInfer**2)

    # Measured Vs30
    Finferred = 0.0
    Fmeasured = 1.0

    SigMeas = (sig1T + ((sig2T-sig1T)/2.0)*(minimum(maximum(Mw,5.0),7.0)-5.0) + sig4T*AS)*sqrt(sig3T*Finferred + 0.7*Fmeasured + (1.0+NL0)**2)
    SigTmeas = sqrt(((1.0+NL0)**2)*Tau**2 + SigMeas**2)

    # check result has right dimensions
    num_sites = Rrup.shape[0]
    assert Y.shape == (num_sites, num_events, num_periods), (msg
               % ('Y', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(Y.shape)))
    assert SigTmeas.shape == (num_sites, num_events, num_periods), (msg
               % ('SigTmeas', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(SigTmeas.shape)))

    return (log(Y), SigTmeas)


Chiou08_combined_coeff = array([
#T (s) c2   c3    c4   c4a crb  chm cg3  c1      c1a     c1b    cn    cm     c5     c6     c7     c7a    c9     c9a     c10     cg1      cg2      phi1    phi2    phi3     phi4     phi5   phi6     phi7   phi8   tau1   tau2   sig1   sig2   sig3   sig4
[ 0.0, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-1.2687, 0.1000,-0.2550,2.996,4.1840,6.1600,0.4893,0.0512,0.0860,0.7900,1.5005,-0.3218,-0.00804,-0.00785,-0.4417,-0.1417,-0.007010,0.102151,0.2289,0.014996,580.0, 0.0700,0.3437,0.2637,0.4458,0.3459,0.8000,0.0663],
[0.010,1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-1.2687, 0.1000,-0.2550,2.996,4.1840,6.1600,0.4893,0.0512,0.0860,0.7900,1.5005,-0.3218,-0.00804,-0.00785,-0.4417,-0.1417,-0.007010,0.102151,0.2289,0.014996,580.0, 0.0700,0.3437,0.2637,0.4458,0.3459,0.8000,0.0663],
[0.020,1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-1.2515, 0.1000,-0.2550,3.292,4.1879,6.1580,0.4892,0.0512,0.0860,0.8129,1.5028,-0.3323,-0.00811,-0.00792,-0.4340,-0.1364,-0.007279,0.108360,0.2289,0.014996,580.0, 0.0699,0.3471,0.2671,0.4458,0.3459,0.8000,0.0663],
[0.030,1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-1.1744, 0.1000,-0.2550,3.514,4.1556,6.1550,0.4890,0.0511,0.0860,0.8439,1.5071,-0.3394,-0.00839,-0.00819,-0.4177,-0.1403,-0.007354,0.119888,0.2289,0.014996,580.0, 0.0701,0.3603,0.2803,0.4535,0.3537,0.8000,0.0663],
[0.040,1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-1.0671, 0.1000,-0.2550,3.563,4.1226,6.1508,0.4888,0.0508,0.0860,0.8740,1.5138,-0.3453,-0.00875,-0.00855,-0.4000,-0.1591,-0.006977,0.133641,0.2289,0.014996,579.9, 0.0702,0.3718,0.2918,0.4589,0.3592,0.8000,0.0663],
[0.050,1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-0.9464, 0.1000,-0.2550,3.547,4.1011,6.1441,0.4884,0.0504,0.0860,0.8996,1.5230,-0.3502,-0.00912,-0.00891,-0.3903,-0.1862,-0.006467,0.148927,0.2290,0.014996,579.9, 0.0701,0.3848,0.3048,0.4630,0.3635,0.8000,0.0663],
[0.075,1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-0.7051, 0.1000,-0.2540,3.448,4.0860,6.1200,0.4872,0.0495,0.0860,0.9442,1.5597,-0.3579,-0.00973,-0.00950,-0.4040,-0.2538,-0.005734,0.190596,0.2292,0.014996,579.6, 0.0686,0.3878,0.3129,0.4702,0.3713,0.8000,0.0663],
[0.10, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-0.5747, 0.1000,-0.2530,3.312,4.1030,6.0850,0.4854,0.0489,0.0860,0.9677,1.6104,-0.3604,-0.00975,-0.00952,-0.4423,-0.2943,-0.005604,0.230662,0.2297,0.014996,579.2, 0.0646,0.3835,0.3152,0.4747,0.3769,0.8000,0.0663],
[0.15, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-0.5309, 0.1000,-0.2500,3.044,4.1717,5.9871,0.4808,0.0479,0.0860,0.9660,1.7549,-0.3565,-0.00883,-0.00862,-0.5162,-0.3113,-0.005845,0.266468,0.2326,0.014988,577.2, 0.0494,0.3719,0.3128,0.4798,0.3847,0.8000,0.0612],
[0.20, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-0.6352, 0.1000,-0.2449,2.831,4.2476,5.8699,0.4755,0.0471,0.0860,0.9334,1.9157,-0.3470,-0.00778,-0.00759,-0.5697,-0.2927,-0.006141,0.255253,0.2386,0.014964,573.9,-0.0019,0.3601,0.3076,0.4816,0.3902,0.8000,0.0530],
[0.25, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-0.7766, 0.1000,-0.2382,2.658,4.3184,5.7547,0.4706,0.0464,0.0860,0.8946,2.0709,-0.3379,-0.00688,-0.00671,-0.6109,-0.2662,-0.006439,0.231541,0.2497,0.014881,568.5,-0.0479,0.3522,0.3047,0.4815,0.3946,0.7999,0.0457],
[0.30, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-0.9278, 0.0999,-0.2313,2.505,4.3844,5.6527,0.4665,0.0458,0.0860,0.8590,2.2005,-0.3314,-0.00612,-0.00598,-0.6444,-0.2405,-0.006704,0.207277,0.2674,0.014639,560.5,-0.0756,0.3438,0.3005,0.4801,0.3981,0.7997,0.0398],
[0.40, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-1.2176, 0.0997,-0.2146,2.261,4.4979,5.4997,0.4607,0.0445,0.0850,0.8019,2.3886,-0.3256,-0.00498,-0.00486,-0.6931,-0.1975,-0.007125,0.165464,0.3120,0.013493,540.0,-0.0960,0.3351,0.2984,0.4758,0.4036,0.7988,0.0312],
[0.50, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-1.4695, 0.0991,-0.1972,2.087,4.5881,5.4029,0.4571,0.0429,0.0830,0.7578,2.5000,-0.3189,-0.00420,-0.00410,-0.7246,-0.1633,-0.007435,0.133828,0.3610,0.011133,512.9,-0.0998,0.3353,0.3036,0.4710,0.4079,0.7966,0.0255],
[0.75, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-1.9278, 0.0936,-0.1620,1.812,4.7571,5.2900,0.4531,0.0387,0.0690,0.6788,2.6224,-0.2702,-0.00308,-0.00301,-0.7708,-0.1028,-0.008120,0.085153,0.4353,0.006739,441.9,-0.0765,0.3429,0.3205,0.4621,0.4157,0.7792,0.0175],
[1.0,  1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-2.2453, 0.0766,-0.1400,1.648,4.8820,5.2480,0.4517,0.0350,0.0450,0.6196,2.6690,-0.2059,-0.00246,-0.00241,-0.7990,-0.0699,-0.008444,0.058595,0.4629,0.005749,391.8,-0.0412,0.3577,0.3419,0.4581,0.4213,0.7504,0.0133],
[1.5,  1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-2.7307, 0.0022,-0.1184,1.511,5.0697,5.2194,0.4507,0.0280,0.0134,0.5101,2.6985,-0.0852,-0.00180,-0.00176,-0.8382,-0.0425,-0.007707,0.031787,0.4756,0.005544,348.1, 0.0140,0.3769,0.3703,0.4493,0.4213,0.7136,0.0090],
[2.0,  1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-3.1413,-0.0591,-0.1100,1.470,5.2173,5.2099,0.4504,0.0213,0.0040,0.3917,2.7085, 0.0160,-0.00147,-0.00143,-0.8663,-0.0302,-0.004792,0.019716,0.4785,0.005521,332.5, 0.0544,0.4023,0.4023,0.4459,0.4213,0.7035,0.0068],
[3.0,  1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-3.7413,-0.0931,-0.1040,1.456,5.4385,5.2040,0.4501,0.0106,0.0010,0.1244,2.7145, 0.1876,-0.00117,-0.00115,-0.9032,-0.0129,-0.001828,0.009643,0.4796,0.005517,324.1, 0.1232,0.4406,0.4406,0.4433,0.4213,0.7006,0.0045],
[4.0,  1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-4.1814,-0.0982,-0.1020,1.465,5.5977,5.2020,0.4501,0.0041,0.0000,0.0086,2.7164, 0.3378,-0.00107,-0.00104,-0.9231,-0.0016,-0.001523,0.005379,0.4799,0.005517,321.7, 0.1859,0.4784,0.4784,0.4424,0.4213,0.7001,0.0034],
[5.0,  1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-4.5187,-0.0994,-0.1010,1.478,5.7276,5.2010,0.4500,0.0010,0.0000,0.0000,2.7172, 0.4579,-0.00102,-0.00099,-0.9222, 0.0000,-0.001440,0.003223,0.4799,0.005517,320.9, 0.2295,0.5074,0.5074,0.4420,0.4213,0.7000,0.0027],
[7.5,  1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-5.1224,-0.0999,-0.1010,1.498,5.9891,5.2000,0.4500,0.0000,0.0000,0.0000,2.7177, 0.7514,-0.00096,-0.00094,-0.8346, 0.0000,-0.001369,0.001134,0.4800,0.005517,320.3, 0.2660,0.5328,0.5328,0.4416,0.4213,0.7000,0.0018],
[10.0, 1.06,3.45,-2.1,-0.5,50.0,3.0,4.0,-5.5872,-0.1000,-0.1000,1.502,6.1930,5.2000,0.4500,0.0000,0.0000,0.0000,2.7180, 1.1856,-0.00094,-0.00091,-0.7332, 0.0000,-0.001361,0.000515,0.4800,0.005517,320.1, 0.2682,0.5542,0.5542,0.4414,0.4213,0.7000,0.0014],
])

# dim = (#coefficients, #periods)
Chiou08_coefficient = Chiou08_combined_coeff[:,1:30].transpose()

# dim = (period,)
Chiou08_coefficient_period = Chiou08_combined_coeff[:,0]

# dim = (sigmacoefficient, period)
Chiou08_sigma_coefficient = Chiou08_combined_coeff[:,30:].transpose()

# dim = (period,)
Chiou08_sigma_coefficient_period = Chiou08_combined_coeff[:,0]

Chiou08_PGA_coefficients = Chiou08_combined_coeff[0,1:30]

Chiou08_PGA_sigma_coefficients = Chiou08_combined_coeff[0,30:]

# number of periods
Chiou08_nper = len(Chiou08_coefficient_period)

Chiou08_magnitude_type = 'Mw'
Chiou08_distance_type = 'Rupture'

Chiou08_interpolation = linear_interpolation

Chiou08_uses_Vs30 = True

ground_motion_init['Chiou08'] = [Chiou08_distribution,
                                Chiou08_magnitude_type,
                                Chiou08_distance_type,
                                Chiou08_coefficient,
                                Chiou08_coefficient_period,
                                Chiou08_interpolation,
                                Chiou08_sigma_coefficient,
                                Chiou08_sigma_coefficient_period,
                                Chiou08_interpolation,
                                Chiou08_uses_Vs30]

###########################  End of Chiou08 model  #############################

########################  Start of Campbell03 model  ###########################

"""Code here is based on Campbell [1].

    [1] Campbell K.W., 2003 Prediction of Strong Ground Motion Using the Hybrid
        Empirical Method and Its Use in the Development of Ground-Motion
        (Attenuation) Relations in Eastern North America,
        Bulletin of the Seismological Society of America, Vol. 93, No. 3,
        pp 1012-1033.
"""

######
# Globals - constants from [1] page 1021
######

Ca_R1 = 70.0
Ca_R2 = 130.0

Ca_M1 = 7.16

######
# The model function, from [1] page 1021.
######

def Campbell03_distribution(**kwargs):
    """The Campbell03 model.

    kwargs  dictionary of parameters, expect:
                mag, distance, coefficient

    The algorithm here is taken from [1], page 1021  and returns results
    that are log g.
    """

    # get args
    Mw = kwargs['mag']				# event-specific
    Rrup = kwargs['distance']			# event-site-specific
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    # check we have the right shapes
    num_sites = Rrup.shape[0]
    num_events = Mw.shape[1]
    num_periods = coefficient.shape[3]

    msg = 'Expected %s.shape=%s, got %s'

    assert Mw.shape == (1, num_events, 1), (msg
               % ('Mw', '(%d,%d,%d)' % (1, num_events, 1),
                  str(Mw.shape)))
    assert Rrup.shape == (num_sites, num_events, 1), (msg
               % ('Rrup', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Rrup.shape)))
    assert coefficient.shape == (10, 1, 1, num_periods), (msg
               % ('coefficient', '(10,1,1,%d)' % num_periods,
                  str(coefficient.shape)))
    assert sigma_coefficient.shape == (3, 1, 1, num_periods), (msg
               % ('sigma_coefficient', '(3,1,1,%d)' % num_periods,
                  str(sigma_coefficient.shape)))

    # unpack coefficients
    (C1, C2, C3, C4, C5, C6, C7, C8, C9, C10) = coefficient
    (C11, C12, C13) = sigma_coefficient

    # equation 33 first
    tmp = C7*exp(C8*Mw)
    R = sqrt(Rrup*Rrup + tmp*tmp)

    # then equations 31, 32 and 33
    tmp = 8.5 - Mw
    F1 = C2*Mw + C3*tmp*tmp
    F2 = C4*log(R) + (C5 + C6*Mw)*Rrup
    F3 = zeros(Rrup.shape) + zeros(C1.shape)

    XCa_R1 = Ca_R1 + zeros(C1.shape)
    XCa_R2 = Ca_R2 + zeros(C1.shape)

    F3 = where(Rrup > XCa_R1, C9*(log(Rrup)-log(XCa_R1)), F3)
    F3 = where(Rrup > XCa_R2,
               C9*(log(Rrup)-log(XCa_R1))+C10*(log(Rrup)-log(XCa_R2)), F3)
    del tmp

    log_mean = C1 + F1 + F2 + F3

    # calculate sigma values
    XCa_M1 = Ca_M1 + zeros(Mw.shape) + zeros(C1.shape)
    XC11 = C11 + zeros(Mw.shape)
    XC12 = C12 + zeros(Mw.shape)
    log_sigma = C13 + zeros(Mw.shape)
    log_sigma = where(Mw < XCa_M1, C11+C12*Mw, log_sigma)

    # check result has right dimensions
    assert log_mean.shape == (num_sites, num_events, num_periods), (msg
               % ('log_mean', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(log_mean.shape)))
    assert log_sigma.shape[1:] == (num_events, num_periods), (msg
               % ('log_sigma', '(?,%d,%d)' % (num_events, num_periods),
                  str(log_sigma.shape)))

    return (log_mean, log_sigma)

Campbell03_magnitude_type = 'Mw'
Campbell03_distance_type = 'Rupture'

######
# Start building the coefficient array
######

# dimension = (#periods, #coefficients)
Campbell03_Table6 = array([
# c1      c2      c3       c4      c5       c6        c7     c8     c9      c10    c11     c12     c13
[ 0.0305, 0.633, -0.0427, -1.591, -0.00428, 0.000483, 0.683, 0.416, 1.140, -0.873, 1.030, -0.0860, 0.414],  # PGA
[ 0.0305, 0.633, -0.0427, -1.591, -0.00428, 0.000483, 0.683, 0.416, 1.140, -0.873, 1.030, -0.0860, 0.414],  # 0.01
[ 1.3535, 0.630, -0.0404, -1.787, -0.00388, 0.000497, 1.020, 0.363, 0.851, -0.715, 1.030, -0.0860, 0.414],  # 0.02
[ 1.1860, 0.622, -0.0362, -1.691, -0.00367, 0.000501, 0.922, 0.376, 0.759, -0.922, 1.030, -0.0860, 0.414],  # 0.03
[ 0.3736, 0.616, -0.0353, -1.469, -0.00378, 0.000500, 0.630, 0.423, 0.771, -1.239, 1.042, -0.0838, 0.443],  # 0.05
[-0.0395, 0.615, -0.0353, -1.383, -0.00421, 0.000486, 0.491, 0.463, 0.955, -1.349, 1.052, -0.0838, 0.453],  # 0.075
[-0.1475, 0.613, -0.0353, -1.369, -0.00454, 0.000460, 0.484, 0.467, 1.096, -1.284, 1.059, -0.0838, 0.460],  # 0.10
[-0.1901, 0.616, -0.0478, -1.368, -0.00473, 0.000393, 0.461, 0.478, 1.239, -1.079, 1.068, -0.0838, 0.469],  # 0.15
[-0.4328, 0.617, -0.0586, -1.320, -0.00460, 0.000337, 0.399, 0.493, 1.250, -0.928, 1.077, -0.0838, 0.478],  # 0.20
[-0.6906, 0.609, -0.0786, -1.280, -0.00414, 0.000263, 0.349, 0.502, 1.241, -0.753, 1.081, -0.0838, 0.482],  # 0.30
[-0.5907, 0.534, -0.1379, -1.216, -0.00341, 0.000194, 0.318, 0.503, 1.166, -0.606, 1.098, -0.0824, 0.508],  # 0.50
[-0.5429, 0.480, -0.1806, -1.184, -0.00288, 0.000160, 0.304, 0.504, 1.110, -0.526, 1.105, -0.0806, 0.528],  # 0.75
[-0.6104, 0.451, -0.2090, -1.158, -0.00255, 0.000141, 0.299, 0.503, 1.067, -0.482, 1.110, -0.0793, 0.543],  # 1.0
[-0.9666, 0.441, -0.2405, -1.135, -0.00213, 0.000119, 0.304, 0.500, 1.029, -0.438, 1.099, -0.0771, 0.547],  # 1.5
[-1.4306, 0.459, -0.2552, -1.124, -0.00187, 0.000103, 0.310, 0.499, 1.015, -0.417, 1.093, -0.0758, 0.551],  # 2.0
[-2.2331, 0.492, -0.2646, -1.121, -0.00154, 0.000084, 0.310, 0.499, 1.014, -0.393, 1.090, -0.0737, 0.562],  # 3.0
[-2.7975, 0.507, -0.2738, -1.119, -0.00135, 0.000074, 0.294, 0.506, 1.018, -0.386, 1.092, -0.0722, 0.575]]) # 4.0

# convert to dim = (#coefficients, #periods)
Campbell03_coefficient = Campbell03_Table6[:,0:10].transpose()

# dim = (period,)
Campbell03_coefficient_period = [0.000, 0.010, 0.020, 0.030, 0.050,
                                 0.075, 0.100, 0.150, 0.200, 0.300,
                                 0.500, 0.750, 1.000, 1.500, 2.000,
                                 3.000, 4.000]

# dim = (period,)
Campbell03_sigma_coefficient = Campbell03_Table6[:,10:].transpose()
Campbell03_sigma_coefficient_period = [0.000, 0.010, 0.020, 0.030, 0.050,
                                       0.075, 0.100, 0.150, 0.200, 0.300,
                                       0.500, 0.750, 1.000, 1.500, 2.000,
                                       3.000, 4.000]

Campbell03_interpolation = linear_interpolation

Campbell03_uses_Vs30 = False

ground_motion_init['Campbell03'] = [Campbell03_distribution,
                                   Campbell03_magnitude_type,
                                   Campbell03_distance_type,
                                   Campbell03_coefficient,
                                   Campbell03_coefficient_period,
                                   Campbell03_interpolation,
                                   Campbell03_sigma_coefficient,
                                   Campbell03_sigma_coefficient_period,
                                   Campbell03_interpolation,
                                   Campbell03_uses_Vs30]

del Campbell03_Table6

#########################  End of Campbell03 model  ############################

########################  Start of Campbell08 model  ###########################

"""Code here is based on Campbell [1].

    [1] Campbell K.W., Bozorgnia Y.,2008 NGA Ground Motion Model for the
        Geometric Mean Horizontal Component of PGA, PGV, PGD and 5% Damped
        Linear Elastic Response Spectra for Periods Ranging from 0.01 to 10s
        Earthquake Spectra, Volume 24, No. 1, pp 139-171.

    The FORTRAN code from the Boore website 
    [www.daveboore.com/nga_gm_tmr/nga_gm_tmr_zips.zip] was used as a basis.
"""

# some constants from the paper
Campbell08_C = 1.88		# table 2, page 148
Campbell08_N = 1.18

Campbell08_ElnAF = 0.3		# page 150
Campbell08_ElnPGA = 0.478	# ElnY for PGA, table 3, page 149

# code constants
Campbell08_exp_min_075 = math.exp(-0.75)

######
# Set up a numpy array to convert a 'fault_type' flag to an array slice
# that encodes the Frv/Fnm flags.  We want a list of three elements that
# indexes 'fault type' to a (Frv, Fnm) tuple.
######

# faulting type flag encodings
#                            'type':      (Frv, Fnm)
Campbell08_faulting_flags = {'reverse':     (1, 0),
                             'normal':      (0, 1),
                             'strike_slip': (0, 0)}

# generate 'Campbell08_fault_type' from the dictionary above
tmp = []
for (k, v) in Campbell08_faulting_flags.iteritems():
    index = ground_motion_misc.FaultTypeDictionary[k]
    tmp.append((index, v))

# sort and make array in correct index order
tmp2 = []
tmp.sort()
for (_, flags) in tmp:
    tmp2.append(flags)
Campbell08_fault_type = array(tmp2)
del tmp, tmp2

######
# Code mimicing the FORTRAN
######

def Campbell08_distribution(**kwargs):
    """The Campbell08 model.

    kwargs  dictionary of parameters

    The algorithm here is described in [1], pp 144-146 but the code
    is copied from the FORTRAN in
    [www.daveboore.com/nga_gm_tmr/nga_gm_tmr_zips.zip].
    """

    # get args
    periods = kwargs['periods']			# site-specific
    Mw = kwargs['mag']				# event-specific
    dist_object = kwargs['dist_object']		# distance object
    Ztor = kwargs['depth_to_top']		# event-specific
    Vs30 = kwargs['Vs30']			# site-specific
    Dip = kwargs['dip']				# event-specific
    fault_type = kwargs['fault_type']	        # event-specific
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    periods = array(periods)

    # get required distances
    Rrup = dist_object.Rupture
    Rjb = dist_object.Joyner_Boore

    # check we have the right shapes
    num_sites = 1
    num_events = Mw.shape[1]
    num_periods = len(periods)

    msg = 'Expected %s.shape=%s, got %s'

    assert Mw.shape == (1, num_events, 1), (msg
               % ('Mw', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Mw.shape)))

    # ignore first dimension of distances
    assert Rrup.shape[1:] == (num_events,), (msg
               % ('Rrup', '(?,%d)' % num_events, str(Rrup.shape)))
    assert Rjb.shape[1:] == (num_events,), (msg
               % ('Rjb', '(?,%d)' % num_events, str(Rjb.shape)))

    assert fault_type.shape == (num_sites, num_events, 1), (msg
               % ('fault_type', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(fault_type.shape)))
    assert Ztor.shape == (num_sites, num_events, 1), (msg
               % ('Ztor', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Ztor.shape)))
    assert Dip.shape == (num_sites, num_events, 1), (msg
               % ('Dip', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Dip.shape)))

    # ensure Vs30 is one-dimensional only
    assert len(Vs30.shape) == 1, (msg
               % ('Vs30', '(?,)', str(Vs30.shape)))

    assert coefficient.shape == (18, 1, 1, num_periods), (msg
               % ('coefficient', '(18,1,1,%d)' % num_periods,
                  str(coefficient.shape)))
    assert sigma_coefficient.shape == (5, 1, 1, num_periods), (msg
               % ('sigma_coefficient', '(5,1,1,%d)' % num_periods,
                  str(sigma_coefficient.shape)))

    # get flag values from 'fault_type'
    Frv = Campbell08_fault_type[:,0][fault_type]
    Fnm = Campbell08_fault_type[:,1][fault_type]

    # set correct shape for params
    Rrup = Rrup[:,:,newaxis]
    Rjb = Rjb[:,:,newaxis]
    Vs30 = array(Vs30)[:,newaxis,newaxis]

    # if user passed us Z25, use it, else calculate from Vs30 (result in km)
    # (we should only pass in Z25 during testing)
    Z25 = kwargs.get('Z25', None)
    if Z25 is None:
        tmp = conversions.convert_Vs30_to_Z10(Vs30)
        Z25 = conversions.convert_Z10_to_Z25(tmp)
        del tmp
    else:
        Z25 = array(Z25)[:,newaxis,newaxis]

    # unpack coefficients
    (c0T,c1T,c2T,c3T,c4T,c5T,c6T,c7T,
     c8T,c9T,c10T,c11T,c12T,k1T,k2T,k3T,cT,nT) = coefficient
    (slnYT,tlnYT,slnAFT,sigCT,rhoT) = sigma_coefficient

    # further Vs30 massaging - add num_periods dimension
    Vs30 = Vs30 + zeros(c0T.shape)

    # unpack the PGA coefficients
    (c0_22,c1_22,c2_22,c3_22,c4_22,c5_22,c6_22,c7_22,c8_22,c9_22,c10_22,
     c11_22,c12_22,k1_22,k2_22,k3_22,c_22,n_22) = Campbell08_PGA_coefficient
    (slnY_22,tlnY_22,slnAF_22,sigC_22,rho_22) = Campbell08_PGA_sigma_coefficient

    ######
    # CALCULATE ROCK PGA (Per = 0; Vs30 = 1100 m/sec)
    ######

    # Magnitude Term
    f_mag = ones(Mw.shape) * c0_22 + c1_22*Mw + c2_22*(Mw-5.5) + c3_22*(Mw-6.5)
    f_mag = where(Mw <= 6.5, c0_22 + c1_22*Mw + c2_22*(Mw-5.5), f_mag)
    f_mag = where(Mw <= 5.5, c0_22 + c1_22*Mw, f_mag)

    # Distance Term
    R = sqrt(Rrup**2 + c6_22**2)
    f_dis = (c4_22 + c5_22*Mw)*log(R)

    # Style-of-Faulting (Fault Mechanism) Term
    f_fltZ = ones(Ztor.shape)
    f_fltZ = where(Ztor < 1.0, Ztor, f_fltZ)

    f_flt = c7_22*Frv*f_fltZ + c8_22*Fnm

    # Hanging-Wall Term
    Rmax = maximum(Rrup, sqrt(Rjb**2 + 1.0))
    f_hngR = ones(Rjb.shape) * (Rrup - Rjb)/Rrup
    f_hngR = where(Ztor + zeros(Rmax.shape)< 1.0, (Rmax - Rjb)/Rmax, f_hngR)
    f_hngR = where(Rjb == 0.0, 1.0, f_hngR)

    f_hngM = ones(Mw.shape)
    f_hngM = where(Mw < 6.5, 2.0*(Mw - 6.0), f_hngM)
    f_hngM = where(Mw <= 6.0, 0.0, f_hngM)

    f_hngZ = ones(Ztor.shape) * (20.0 - Ztor)/20.0
    f_hngZ = where(Ztor >= 20.0, 0.0, f_hngZ)

    f_hngD = ones(Dip.shape) * (90.0 - Dip)/20.0
    f_hngD = where(Dip <= 70.0, 1.0, f_hngD)

    f_hng = c9_22*f_hngR*f_hngM*f_hngZ*f_hngD

    # Shallow Site Response Term (Vs30 = 1100 m/s)
    f_site = (c10_22 + k2_22*n_22)*log(1100.0/k1_22)

    # Basin (Sediment) Response Term
    f_sed = ones(Z25.shape) * c12_22*k3_22*exp(-0.75)*(1.0 - exp(-0.25*(Z25 - 3.0)))
    f_sed = where(Z25 <= 3.0, 0.0, f_sed)
    f_sed = where(Z25 < 1.0, c11_22*(Z25 - 1.0), f_sed)

    # Value of PGA on Rock
    A_1100 = exp(f_mag + f_dis + f_flt + f_hng + f_site + f_sed)

    # Value of PGA on Local Site Conditions
    PGA = exp(log(A_1100) - f_site)

    f_site = ones(Vs30.shape) * (c10_22 + k2_22*n_22)*log(1100.0/k1_22)	# correct shape?
    f_site = where(Vs30 < 1100.0, (c10_22 + k2_22*n_22)*log(Vs30/k1_22), f_site)
    XA_1100 = A_1100 + zeros(Vs30.shape)
    XVs30 = Vs30 + zeros(XA_1100.shape)
    Xf_site = f_site + zeros(XVs30.shape)
    #f_site = where(Vs30 < k1_22, c10_22*log(Vs30/k1_22) + k2_22*(log(A_1100 + c_22*(Vs30/k1_22)**n_22) - log(A_1100 + c_22)), f_site)
    f_site = where(XVs30 < k1_22, c10_22*log(XVs30/k1_22) + k2_22*(log(XA_1100 + c_22*(XVs30/k1_22)**n_22) - log(XA_1100 + c_22)), Xf_site)

    PGA = exp(log(PGA) + f_site)

    ######
    # CALCULATE STRONG MOTION PARAMETER
    ######

    # Magnitude Term
    f_mag = ones(Mw.shape) * c0T + c1T*Mw + c2T*(Mw-5.5) + c3T*(Mw-6.5)
    f_mag = where((Mw <= 6.5) + zeros(c0T.shape), c0T + c1T*Mw + c2T*(Mw-5.5), f_mag)
    f_mag = where((Mw <= 5.5) + zeros(c0T.shape), c0T + c1T*Mw, f_mag)

    # Distance Term
    R = sqrt(Rrup**2 + c6T**2)
    f_dis = (c4T + c5T*Mw)*log(R)

    # Style-of-Faulting Term
    f_fltZ = ones(Ztor.shape)
    f_fltZ = where(Ztor < 1.0, Ztor, f_fltZ)

    f_flt = c7T*Frv*f_fltZ + c8T*Fnm

    # Hanging-Wall Term
    Rmax = maximum(Rrup, sqrt(Rjb**2 + 1.0))

    f_hngR = ones(Rjb.shape) * (Rrup - Rjb)/Rrup
    f_hngR = where(Ztor + zeros(Rmax.shape)< 1.0, (Rmax - Rjb)/Rmax, f_hngR)
    f_hngR = where(Rjb == 0.0, 1.0, f_hngR)

    f_hngM = ones(Mw.shape)
    f_hngM = where(Mw < 6.5, 2.0*(Mw - 6.0), f_hngM)
    f_hngM = where(Mw <= 6.0, 0.0, f_hngM)

    f_hngZ = ones(Ztor.shape) * (20.0 - Ztor)/20.0
    f_hngZ = where(Ztor >= 20.0, 0.0, f_hngZ)

    f_hngD = ones(Dip.shape) * (90.0 - Dip)/20.0
    f_hngD = where(Dip <= 70.0, 1.0, f_hngD)

    f_hng = c9T*f_hngR*f_hngM*f_hngZ*f_hngD

    # Shallow Site Response Term
    f_site = ones(Vs30.shape) * (c10T + k2T*nT)*log(1100.0/k1T)
    f_site = where(Vs30 < 1100.0, (c10T + k2T*nT)*log(Vs30/k1T), f_site)
    XA_1100 = A_1100 + zeros(Vs30.shape)
    XVs30 = Vs30 + zeros(XA_1100.shape)
    Xf_site = f_site + zeros(XVs30.shape)
    #f_site = where(Vs30 < k1T, c10T*log(Vs30/k1T) + k2T*(log(A_1100 + cT*(Vs30/k1T)**nT) - log(A_1100 + cT)), f_site)
    f_site = where(XVs30 < k1T, c10T*log(XVs30/k1T) + k2T*(log(XA_1100 + cT*(XVs30/k1T)**nT) - log(XA_1100 + cT)), Xf_site)

    # Basin (Sediment) Response Term
    f_sed = ones(Z25.shape) * c12T*k3T*exp(-0.75)*(1.0 - exp(-0.25*(Z25 - 3.0)))
    f_sed = where((Z25 <= 3.0) + zeros(f_sed.shape), 0.0, f_sed)
    f_sed = where((Z25 < 1.0) + zeros(f_sed.shape), c11T*(Z25 - 1.0), f_sed)

    # Calculate Ground Motion Parameter
    Y = exp(f_mag + f_dis + f_flt + f_hng + f_site + f_sed)

    # Check Whether Y < PGA at Short Periods - use PGA if so
    short_period = logical_and(periods >= 0.0, periods <= 0.25)
    Y = where(logical_and(short_period, Y < PGA), PGA, Y)

    ######
    # CALCULATE ALEATORY UNCERTAINTY
    ######

    # Linearized Relationship Between f_site and ln PGA
    Alpha = zeros(Vs30.shape)
    XA_1100 = A_1100 + zeros(Vs30.shape)
    XVs30 = Vs30 + zeros(XA_1100.shape)
    XAlpha = Alpha + zeros(XVs30.shape)
    #Alpha = where(Vs30 < k1T, k2T*A_1100*(1.0/(A_1100 + cT*(Vs30/k1T)**nT) - 1.0/(A_1100 + cT)), Alpha)
    Alpha = where(XVs30 < k1T, k2T*XA_1100*(1.0/(XA_1100 + cT*(XVs30/k1T)**nT) - 1.0/(XA_1100 + cT)), XAlpha)

    # Intra-Event Standard Deviation at Base of Site Profile
    slnPGA = slnY_22
    tlnPGA = tlnY_22
    slnYB = sqrt(slnYT**2 - slnAFT**2)
    slnAB = sqrt(slnPGA**2 - slnAFT**2)
    
    # Standard Deviation of Geometric Mean of ln Y
    Sigma = sqrt(slnYB**2 + slnAFT**2 + Alpha**2*slnAB**2 + 2.0*Alpha*rhoT*slnYB*slnAB)
    Tau = tlnYT
    SigT = sqrt(Sigma**2 + Tau**2)

    # Standard Deviation of Arbitrary Horizontal Component of ln Y
    SigArb = sqrt(SigT**2 + sigCT**2)

    # check result has right dimensions
    num_sites = Rrup.shape[0]
    assert Y.shape == (num_sites, num_events, num_periods), (msg
               % ('Y', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(Y.shape)))
    assert SigT.shape == (num_sites, num_events, num_periods), (msg
               % ('SigT', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(SigT.shape)))
 
    return (log(Y), SigT)


######
# Set up a numpy array to convert a 'fault_type' flag to an array slice
# that encodes the Frv/Fnm flags.  We want a list of three elements that
# indexes 'fault type' to a (Frv, Fnm) tuple.
######

# faulting type flag encodings
#                            'type':      (Frv, Fnm)
Campbell08_faulting_flags = {'reverse':     (1, 0),
                             'normal':      (0, 1),
                             'strike_slip': (0, 0)}

# generate 'Campbell08_fault_type' from the dictionary above
tmp = []
for (k, v) in Campbell08_faulting_flags.iteritems():
    index = ground_motion_misc.FaultTypeDictionary[k]
    tmp.append((index, v))

# sort and make array in correct index order
tmp2 = []
tmp.sort()
for (_, flags) in tmp:
    tmp2.append(flags)
Campbell08_fault_type = array(tmp2)
del tmp, tmp2


# coefficient table from CB08_COEFS.TXT, T=0.0 moved to top, etc
tmp = array([
#T(s)  c0     c1     c2     c3     c4    c5   c6   c7     c8    c9     c10   c11   c12    k1   k2    k3    c    n    s_lny t_lny s_lnAF c_lny rho
[ 0.0, -1.715,0.500,-0.530,-0.262,-2.118,0.17,5.60,0.280,-0.120,0.490, 1.058,0.040,0.610, 865,-1.186,1.839,1.88,1.18,0.478,0.219,0.300, 0.166,1.000],
[0.010,-1.715,0.500,-0.530,-0.262,-2.118,0.17,5.60,0.280,-0.120,0.490, 1.058,0.040,0.610, 865,-1.186,1.839,1.88,1.18,0.478,0.219,0.300, 0.166,1.000],
[0.020,-1.680,0.500,-0.530,-0.262,-2.123,0.17,5.60,0.280,-0.120,0.490, 1.102,0.040,0.610, 865,-1.219,1.840,1.88,1.18,0.480,0.219,0.300, 0.166,0.999],
[0.030,-1.552,0.500,-0.530,-0.262,-2.145,0.17,5.60,0.280,-0.120,0.490, 1.174,0.040,0.610, 908,-1.273,1.841,1.88,1.18,0.489,0.235,0.300, 0.165,0.989],
[0.050,-1.209,0.500,-0.530,-0.267,-2.199,0.17,5.74,0.280,-0.120,0.490, 1.272,0.040,0.610,1054,-1.346,1.843,1.88,1.18,0.510,0.258,0.300, 0.162,0.963],
[0.075,-0.657,0.500,-0.530,-0.302,-2.277,0.17,7.09,0.280,-0.120,0.490, 1.438,0.040,0.610,1086,-1.471,1.845,1.88,1.18,0.520,0.292,0.300, 0.158,0.922],
[0.10, -0.314,0.500,-0.530,-0.324,-2.318,0.17,8.05,0.280,-0.099,0.490, 1.604,0.040,0.610,1032,-1.624,1.847,1.88,1.18,0.531,0.286,0.300, 0.170,0.898],
[0.15, -0.133,0.500,-0.530,-0.339,-2.309,0.17,8.79,0.280,-0.048,0.490, 1.928,0.040,0.610, 878,-1.931,1.852,1.88,1.18,0.532,0.280,0.300, 0.180,0.890],
[0.20, -0.486,0.500,-0.446,-0.398,-2.220,0.17,7.60,0.280,-0.012,0.490, 2.194,0.040,0.610, 748,-2.188,1.856,1.88,1.18,0.534,0.249,0.300, 0.186,0.871],
[0.25, -0.890,0.500,-0.362,-0.458,-2.146,0.17,6.58,0.280, 0.000,0.490, 2.351,0.040,0.700, 654,-2.381,1.861,1.88,1.18,0.534,0.240,0.300, 0.191,0.852],
[0.30, -1.171,0.500,-0.294,-0.511,-2.095,0.17,6.04,0.280, 0.000,0.490, 2.460,0.040,0.750, 587,-2.518,1.865,1.88,1.18,0.544,0.215,0.300, 0.198,0.831],
[0.40, -1.466,0.500,-0.186,-0.592,-2.066,0.17,5.30,0.280, 0.000,0.490, 2.587,0.040,0.850, 503,-2.657,1.874,1.88,1.18,0.541,0.217,0.300, 0.206,0.785],
[0.50, -2.569,0.656,-0.304,-0.536,-2.041,0.17,4.73,0.280, 0.000,0.490, 2.544,0.040,0.883, 457,-2.669,1.883,1.88,1.18,0.550,0.214,0.300, 0.208,0.735],
[0.75, -4.844,0.972,-0.578,-0.406,-2.000,0.17,4.00,0.280, 0.000,0.490, 2.133,0.077,1.000, 410,-2.401,1.906,1.88,1.18,0.568,0.227,0.300, 0.221,0.628],
[1.00, -6.406,1.196,-0.772,-0.314,-2.000,0.17,4.00,0.255, 0.000,0.490, 1.571,0.150,1.000, 400,-1.955,1.929,1.88,1.18,0.568,0.255,0.300, 0.225,0.534],
[1.50, -8.692,1.513,-1.046,-0.185,-2.000,0.17,4.00,0.161, 0.000,0.490, 0.406,0.253,1.000, 400,-1.025,1.974,1.88,1.18,0.564,0.296,0.300, 0.222,0.411],
[2.00, -9.701,1.600,-0.978,-0.236,-2.000,0.17,4.00,0.094, 0.000,0.371,-0.456,0.300,1.000, 400,-0.299,2.019,1.88,1.18,0.571,0.296,0.300, 0.226,0.331],
[3.00,-10.556,1.600,-0.638,-0.491,-2.000,0.17,4.00,0.000, 0.000,0.154,-0.820,0.300,1.000, 400, 0.000,2.110,1.88,1.18,0.558,0.326,0.300, 0.229,0.289],
[4.00,-11.212,1.600,-0.316,-0.770,-2.000,0.17,4.00,0.000, 0.000,0.000,-0.820,0.300,1.000, 400, 0.000,2.200,1.88,1.18,0.576,0.297,0.300, 0.237,0.261],
[5.00,-11.684,1.600,-0.070,-0.986,-2.000,0.17,4.00,0.000, 0.000,0.000,-0.820,0.300,1.000, 400, 0.000,2.291,1.88,1.18,0.601,0.359,0.300, 0.237,0.200],
[7.50,-12.505,1.600,-0.070,-0.656,-2.000,0.17,4.00,0.000, 0.000,0.000,-0.820,0.300,1.000, 400, 0.000,2.517,1.88,1.18,0.628,0.428,0.300, 0.271,0.174],
[10.0,-13.087,1.600,-0.070,-0.422,-2.000,0.17,4.00,0.000, 0.000,0.000,-0.820,0.300,1.000, 400, 0.000,2.744,1.88,1.18,0.667,0.485,0.300, 0.290,0.174]])

# construct required coefficient tables for EQRM
# shape = (#coefficients, #periods)
Campbell08_coefficient = array(tmp[:,1:19]).transpose()
Campbell08_sigma_coefficient = array(tmp[:,19:]).transpose()


# coefficient period arrays
# dim = (period,) 
Campbell08_coefficient_period = array(tmp[:,0]).transpose()
Campbell08_sigma_coefficient_period = array(tmp[:,0]).transpose()

# PGA coefficient & sigma coefficient tables
Campbell08_PGA_coefficient = array(tmp[0,1:19]).transpose()
Campbell08_PGA_sigma_coefficient = array(tmp[0,19:]).transpose()

# now for the rest of the model attributes
Campbell08_magnitude_type = 'Mw'
Campbell08_distance_type = 'Rupture'
Campbell08_interpolation = linear_interpolation
Campbell08_uses_Vs30 = True

ground_motion_init['Campbell08'] = [Campbell08_distribution,
                                   Campbell08_magnitude_type,
                                   Campbell08_distance_type,
                                   Campbell08_coefficient,
                                   Campbell08_coefficient_period,
                                   Campbell08_interpolation,
                                   Campbell08_sigma_coefficient,
                                   Campbell08_sigma_coefficient_period,
                                   Campbell08_interpolation,
                                   Campbell08_uses_Vs30]

del tmp
#########################  End of Campbell08 model  ##########################



#************  values to use in test ground motion models   ************
mean_model_magnitude_type='ML'
mean_model_distance_type='Rupture'
mean_model_coefficient=[[0.28,0.28],[0.28,0.28]]
mean_model_coefficient_period=[0.0,1.0]
mean_model_sigma_coefficient=[[0.28,0.28],[0.28,0.28]]
mean_model_sigma_coefficient_period=[0.0,1.0]
mean_model_sigma_coefficient_interpolation = linear_interpolation
mean_model_coefficient_interpolation = linear_interpolation
mean_model_uses_Vs30 = False
#***************  START OF mean_10_sigma_1  ****************************


def mean_10_sigma_1_distribution(**kwargs):
    
    num_sites =  kwargs['distance'].shape[0]
    num_events =  kwargs['distance'].shape[1]
    num_periods = kwargs['coefficient'].shape[3]

    log_mean = ones((num_sites, num_events, num_periods))*10
    log_sigma = ones((num_sites, num_events, num_periods))
    return log_mean, log_sigma


mean_10_sigma_1_args=[
    mean_10_sigma_1_distribution,
    mean_model_magnitude_type,
    mean_model_distance_type,
    
    mean_model_coefficient,
    mean_model_coefficient_period,
    mean_model_coefficient_interpolation,
    
    mean_model_sigma_coefficient,
    mean_model_sigma_coefficient_period,
    mean_model_sigma_coefficient_interpolation,

    mean_model_uses_Vs30]

ground_motion_init['mean_10_sigma_1'] = mean_10_sigma_1_args

#***************  End of mean_10_sigma_1 ****************************

#***************  START OF mean_20_sigma_2  ****************************

def mean_20_sigma_2_distribution(**kwargs):
    
    num_sites =  kwargs['distance'].shape[0]
    num_events =  kwargs['distance'].shape[1]
    num_periods = kwargs['coefficient'].shape[3]

    log_mean = ones((num_sites, num_events, num_periods))*20
    log_sigma = ones((num_sites, num_events, num_periods))*2
    return log_mean, log_sigma

mean_20_sigma_2_args=[
    mean_20_sigma_2_distribution,
    mean_model_magnitude_type,
    mean_model_distance_type,
    
    mean_model_coefficient,
    mean_model_coefficient_period,
    mean_model_coefficient_interpolation,
    
    mean_model_sigma_coefficient,
    mean_model_sigma_coefficient_period,
    mean_model_sigma_coefficient_interpolation,

    mean_model_uses_Vs30]

ground_motion_init['mean_20_sigma_2'] = mean_20_sigma_2_args

#***************  End of mean_20_sigma_2 ****************************

#***************  START OF mean_10_sigma_1  ****************************


def mean_1_sigma_0pt5_distribution(**kwargs):
    
    num_sites =  kwargs['distance'].shape[0]
    num_events =  kwargs['distance'].shape[1]
    num_periods = kwargs['coefficient'].shape[3]

    log_mean = ones((num_sites, num_events, num_periods))
    log_sigma = ones((num_sites, num_events, num_periods))*0.5
    return log_mean, log_sigma


mean_1_sigma_0pt5_args=[
    mean_1_sigma_0pt5_distribution,
    mean_model_magnitude_type,
    mean_model_distance_type,
    
    mean_model_coefficient,
    mean_model_coefficient_period,
    mean_model_coefficient_interpolation,
    
    mean_model_sigma_coefficient,
    mean_model_sigma_coefficient_period,
    mean_model_sigma_coefficient_interpolation,

    mean_model_uses_Vs30]

ground_motion_init['mean_1_sigma_0pt5'] = mean_1_sigma_0pt5_args

#***************  End of mean_1_sigma_0pt5 ****************************
#***************  START OF return_Vs30  ****************************


def return_Vs30_distribution(**kwargs):
    
    num_sites =  kwargs['distance'].shape[0]
    num_events =  kwargs['distance'].shape[1]
    num_periods = kwargs['coefficient'].shape[3]
    Vs30 = kwargs['Vs30']
    log_mean = ones((num_sites, num_events, num_periods))*log(Vs30)
    log_sigma = zeros((num_sites, num_events, num_periods))
    
    return log_mean, log_sigma

return_Vs30_uses_Vs30 = True


return_Vs30_args=[
    return_Vs30_distribution,
    mean_model_magnitude_type,
    mean_model_distance_type,
    
    mean_model_coefficient,
    mean_model_coefficient_period,
    mean_model_coefficient_interpolation,
    
    mean_model_sigma_coefficient,
    mean_model_sigma_coefficient_period,
    mean_model_sigma_coefficient_interpolation,

    return_Vs30_uses_Vs30]

ground_motion_init['return_Vs30'] = return_Vs30_args

#***************  End of return_Vs30 ****************************
#***************  START OF mean_2_sigma_1  ****************************

def mean_2_sigma_1_distribution(**kwargs):
    
    num_sites =  kwargs['distance'].shape[0]
    num_events =  kwargs['distance'].shape[1]
    num_periods = kwargs['coefficient'].shape[3]

    log_mean = ones((num_sites, num_events, num_periods))*2
    log_sigma = ones((num_sites, num_events, num_periods))
    return log_mean, log_sigma

mean_2_sigma_1_args=[
    mean_2_sigma_1_distribution,
    mean_model_magnitude_type,
    mean_model_distance_type,
    
    mean_model_coefficient,
    mean_model_coefficient_period,
    mean_model_coefficient_interpolation,
    
    mean_model_sigma_coefficient,
    mean_model_sigma_coefficient_period,
    mean_model_sigma_coefficient_interpolation,

    mean_model_uses_Vs30]

ground_motion_init['mean_2_sigma_1'] = mean_2_sigma_1_args

#***************  End of Gaull 1990 WA MODEL  ****************************

########################  Start of Abrahamson08 model  #########################

def Abrahamson08_distribution(**kwargs):
    """The Abrahamson08 model function.

    kwargs  dictionary os parameters, expect:
                mag, distance, coefficient, sigma_coefficient

    The algorithm here is described in [1], but the code is copied from the
    FORTRAN in [www.daveboore.com/nga_gm_tmr/nga_gm_tmr_zips.zip].

    [1] Abrahamson N., Silva W., "Summary of the Abrahamson & Silva NGA
        Ground-Motion Relations", Earthquake Spectra, Volume 24, No. 1,
        pp 67-97, February 2008
    """
    #import pdb; pdb.set_trace();
    # get args
    Per = kwargs['periods']
    Mw = kwargs['mag']
    dist_object = kwargs['dist_object'] 
    fault_type = kwargs['fault_type']
    Ztor = kwargs['depth_to_top']
    Dip = kwargs['dip']
    W = kwargs['width']
    Vs30 = kwargs['Vs30']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    # for testing, pass in 'Z10' and 'Fhw' params
    Z10 = kwargs.get('Z10', None)
    Fhw = kwargs.get('Fhw', 0)

    # get required distance arrays
    Rrup = dist_object.Rupture
    Rjb = dist_object.Joyner_Boore
    Rx = dist_object.Horizontal

    # check we have the right shapes
    num_sites = 1
    num_events = Mw.shape[1]
    num_periods = len(Per)

    msg = 'Expected %s.shape=%s, got %s'

    assert Mw.shape == (1, num_events, 1), (msg
               % ('Mw', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Mw.shape)))

    # ignore first dimension of distances
    assert Rrup.shape[1:] == (num_events,), (msg
               % ('Rrup', '(?,%d)' % num_events, str(Rrup.shape)))
    assert Rjb.shape[1:] == (num_events,), (msg
               % ('Rjb', '(?,%d)' % num_events, str(Rjb.shape)))
    assert Rx.shape[1:] == (num_events,), (msg
               % ('Rx', '(?,%d)' % num_events, str(Rx.shape)))

    assert fault_type.shape == (num_sites, num_events, 1), (msg
               % ('fault_type', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(fault_type.shape)))
    assert Ztor.shape == (num_sites, num_events, 1), (msg
               % ('Ztor', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Ztor.shape)))
    assert Dip.shape == (num_sites, num_events, 1), (msg
               % ('Dip', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(Dip.shape)))
    assert W.shape == (num_sites, num_events, 1), (msg
               % ('W', '(%d,%d,%d)' % (num_sites, num_events, 1),
                  str(W.shape)))

    # ensure Vs30 is one-dimensional only
    assert len(Vs30.shape) == 1, (msg
               % ('Vs30', '(?,)', str(Vs30.shape)))

    assert coefficient.shape == (20, 1, 1, num_periods), (msg
               % ('coefficient', '(20,1,1,%d)' % num_periods,
                  str(coefficient.shape)))
    assert sigma_coefficient.shape == (7, 1, 1, num_periods), (msg
               % ('sigma_coefficient', '(7,1,1,%d)' % num_periods,
                  str(sigma_coefficient.shape)))

    # get flag values from 'fault_type'
    Frv = AS08_fault_type[:,0][fault_type]
    Fnm = AS08_fault_type[:,1][fault_type]

    # these parameters are assumed 0 (for now)
    Fas = 0

    # set correct shape for params
    Rrup = Rrup[:,:,newaxis]
    Rjb = Rjb[:,:,newaxis]
    Rx = Rx[:,:,newaxis]
    Per = array(Per)[newaxis,newaxis,:]
    Vs30 = array(Vs30)[:,newaxis,newaxis]

    # get Z1.0 value from Vs30 (Z10 will be supplied if testing)
    if Z10 is None:
        (Z10, _) = conversions.AS08_convert_Vs30_to_Z10_Z25(Vs30)

    # unpack coefficients
    (c1T, c4T, a3T, a4T, a5T, nT, cT, c2T, VlinT, bT,
     a1T, a2T, a8T, a10T, a12T, a13T, a14T, a15T, a16T, a18T) = coefficient

    (s1estT, s2estT, s1meaT, s2meaT, s3T, s4T, rhoT) = sigma_coefficient

    # unpack PGA coefficients
    (AS08_PGA_c1, AS08_PGA_c4, AS08_PGA_a3, AS08_PGA_a4, AS08_PGA_a5,
     AS08_PGA_n, AS08_PGA_c, AS08_PGA_c2, AS08_PGA_Vlin, AS08_PGA_b,
     AS08_PGA_a1, AS08_PGA_a2, AS08_PGA_a8, AS08_PGA_a10, AS08_PGA_a12,
     AS08_PGA_a13, AS08_PGA_a14, AS08_PGA_a15, AS08_PGA_a16,
     AS08_PGA_a18) = AS08_PGA_coefficients
    
    (AS08_PGA_s1est, AS08_PGA_s2est, AS08_PGA_s1mea, AS08_PGA_s2mea,
     AS08_PGA_s3, AS08_PGA_s4, AS08_PGA_rho) = AS08_PGA_sigma_coefficients

    #####
    # CALCULATE ROCK PGA (Per = 0, Vs30 = 1100 m/sec)
    #####

    R = sqrt(Rrup**2 + AS08_PGA_c4**2)
    f_1 = (AS08_PGA_a1 + AS08_PGA_a5*(Mw-AS08_PGA_c1) + 
           AS08_PGA_a8*(8.5-Mw)**2 + 
           (AS08_PGA_a2 + AS08_PGA_a3*(Mw-AS08_PGA_c1))*log(R))
    # This is to get the Mw the same shape as f_1.  f_1's shape is
    # based on Rrup.  In tests the site component of this is not
    # always zero.
    Mw_tiled = tile(Mw,(f_1.shape[0],1,1))
    f_1 = where(Mw_tiled <= AS08_PGA_c1,
                AS08_PGA_a1 + AS08_PGA_a4*(Mw-AS08_PGA_c1) +
                AS08_PGA_a8*(8.5-Mw)**2 +
                (AS08_PGA_a2 + AS08_PGA_a3*(Mw-AS08_PGA_c1))*log(R),
                f_1)
    del R

    #####
    # Hanging-Wall Term
    #####

    RxTest = W*cos(Dip*pi/180.0)

    T1 = zeros(Rjb.shape)
    T1 = where(Rjb < 30.0, 1.0 - Rjb/30.0, T1)

    T2 = 0.5 + Rx/(2.0*RxTest)
    T2 = where(logical_or(Rx > RxTest, Dip == 90.0), 1.0, T2)

    oldsettings = seterr(divide='ignore')
    T3 = Rx/Ztor
    seterr(**oldsettings)
    
    T3 = where(Rx >= Ztor, 1.0, T3)

    T4 = ones(Mw.shape)
    T4 = where(Mw < 7.0, Mw - 6.0, T4)
    T4 = where(Mw <= 6.0, 0.0, T4)

    T5 = ones(Dip.shape)
    T5 = where(Dip >= 30.0, 1.0 - (Dip - 30.0)/60.0, T5)

    f_4 = AS08_PGA_a14*T1*T2*T3*T4*T5

    del RxTest, T1, T2, T3, T4, T5

    #####
    # Shallow Site Response Term (Vs30 = 1100 m/sec)
    #####

    f_5 = (AS08_PGA_a10 + AS08_PGA_b*AS08_PGA_n)*log(1100/AS08_PGA_Vlin)

    # depth to top of rupture term

    f_6 = ones(Ztor.shape) * AS08_PGA_a16
    f_6 = where(Ztor < 10.0, AS08_PGA_a16*Ztor/10.0, f_6)

    # large distance term

    T6 = ones(Mw.shape) * 0.5
    T6 = where(Mw <= 6.5, 0.5*(6.5 - Mw) + 0.5, T6)
    T6 = where(Mw < 5.5, 1.0, T6)

    f_8 = AS08_PGA_a18*(Rrup - 100.0)*T6
    f_8 = where(Rrup < 100.0, 0.0, f_8)

    del T6

    # PGA value for rock

    PGA_1100 = exp(f_1 + AS08_PGA_a12*Frv + AS08_PGA_a13*Fnm + AS08_PGA_a15*Fas + f_5  + Fhw*f_4 + f_6 + f_8)

    del f_1, f_4, f_5, f_6, f_8

    # determine index of period for constant displacement calculation

    Td = 10.0**(-1.25 + 0.3*Mw)

    # get indices of periods either side of the Td value.
    # this is different from the Boore FORTRAN because we must be vector
    # and because the Boore periods includes oddballs like '-1'.

    # we want indices iTd1 and iTd2 into list of periods
    # that bracket the period Td, limited at top so iTd2 is legal.

    tmp = sum(where(Abrahamson08_coefficient_period < Td, 1, 0), axis=2).flatten()
    iTd1 = where(tmp >= AS08_nper, AS08_nper - 1, tmp) - 1	# make an index
    iTd2 = iTd1 + 1
    
    # unpack coefficients for the bracket periods
    (c1_iTd1, c4_iTd1, a3_iTd1, a4_iTd1, a5_iTd1, n_iTd1, c_iTd1, c2_iTd1,
     Vlin_iTd1, b_iTd1, a1_iTd1, a2_iTd1, a8_iTd1, a10_iTd1, a12_iTd1,
     a13_iTd1, a14_iTd1, a15_iTd1,
     a16_iTd1, a18_iTd1) = Abrahamson08_coefficient[:,iTd1]

    c1_iTd1 = c1_iTd1[newaxis,:,newaxis]	# must reshape to get right results
    c4_iTd1 = c4_iTd1[newaxis,:,newaxis]
    a3_iTd1 = a3_iTd1[newaxis,:,newaxis]
    a4_iTd1 = a4_iTd1[newaxis,:,newaxis]
    a5_iTd1 = a5_iTd1[newaxis,:,newaxis]
    n_iTd1 = n_iTd1[newaxis,:,newaxis]
    c_iTd1 = c_iTd1[newaxis,:,newaxis]
    c2_iTd1 = c2_iTd1[newaxis,:,newaxis]
    Vlin_iTd1 = Vlin_iTd1[newaxis,:,newaxis]
    b_iTd1 = b_iTd1[newaxis,:,newaxis]
    a1_iTd1 = a1_iTd1[newaxis,:,newaxis]
    a2_iTd1 = a2_iTd1[newaxis,:,newaxis]
    a8_iTd1 = a8_iTd1[newaxis,:,newaxis]
    a10_iTd1 = a10_iTd1[newaxis,:,newaxis]
    a12_iTd1 = a12_iTd1[newaxis,:,newaxis]
    a13_iTd1 = a13_iTd1[newaxis,:,newaxis]
    a14_iTd1 = a14_iTd1[newaxis,:,newaxis]
    a15_iTd1 = a15_iTd1[newaxis,:,newaxis]
    a16_iTd1 = a16_iTd1[newaxis,:,newaxis]
    a18_iTd1 = a18_iTd1[newaxis,:,newaxis]

    (s1est_iTd1, s2est_iTd1, s1mea_iTd1, s2mea_iTd1,
     s3_iTd1, s4_iTd1, rho_iTd1) = Abrahamson08_sigma_coefficient[:,iTd1]

    s1est_iTd1 = s1est_iTd1[newaxis,:,newaxis]
    s2est_iTd1 = s2est_iTd1[newaxis,:,newaxis]
    s1mea_iTd1 = s1mea_iTd1[newaxis,:,newaxis]
    s2mea_iTd1 = s2mea_iTd1[newaxis,:,newaxis]
    s3_iTd1 = s3_iTd1[newaxis,:,newaxis]
    s4_iTd1 = s4_iTd1[newaxis,:,newaxis]
    rho_iTd1 = rho_iTd1[newaxis,:,newaxis]

    (c1_iTd2, c4_iTd2, a3_iTd2, a4_iTd2, a5_iTd2, n_iTd2, c_iTd2, c2_iTd2,
     Vlin_iTd2, b_iTd2, a1_iTd2, a2_iTd2, a8_iTd2, a10_iTd2, a12_iTd2,
     a13_iTd2, a14_iTd2, a15_iTd2,
     a16_iTd2, a18_iTd2) = Abrahamson08_coefficient[:,iTd2]

    c1_iTd2 = c1_iTd2[newaxis,:,newaxis]
    c4_iTd2 = c4_iTd2[newaxis,:,newaxis]
    a3_iTd2 = a3_iTd2[newaxis,:,newaxis]
    a4_iTd2 = a4_iTd2[newaxis,:,newaxis]
    a5_iTd2 = a5_iTd2[newaxis,:,newaxis]
    n_iTd2 = n_iTd2[newaxis,:,newaxis]
    c_iTd2 = c_iTd2[newaxis,:,newaxis]
    c2_iTd2 = c2_iTd2[newaxis,:,newaxis]
    Vlin_iTd2 = Vlin_iTd2[newaxis,:,newaxis]
    b_iTd2 = b_iTd2[newaxis,:,newaxis]
    a1_iTd2 = a1_iTd2[newaxis,:,newaxis]
    a2_iTd2 = a2_iTd2[newaxis,:,newaxis]
    a8_iTd2 = a8_iTd2[newaxis,:,newaxis]
    a10_iTd2 = a10_iTd2[newaxis,:,newaxis]
    a12_iTd2 = a12_iTd2[newaxis,:,newaxis]
    a13_iTd2 = a13_iTd2[newaxis,:,newaxis]
    a14_iTd2 = a14_iTd2[newaxis,:,newaxis]
    a15_iTd2 = a15_iTd2[newaxis,:,newaxis]
    a16_iTd2 = a16_iTd2[newaxis,:,newaxis]
    a18_iTd2 = a18_iTd2[newaxis,:,newaxis]

    (s1est_iTd2, s2est_iTd2, s1mea_iTd2, s2mea_iTd2,
     s3_iTd2, s4_iTd2, rho_iTd2) = Abrahamson08_sigma_coefficient[:,iTd2]

    s1est_iTd2 = s1est_iTd2[newaxis,:,newaxis]
    s2est_iTd2 = s2est_iTd2[newaxis,:,newaxis]
    s1mea_iTd2 = s1mea_iTd2[newaxis,:,newaxis]
    s2mea_iTd2 = s2mea_iTd2[newaxis,:,newaxis]
    s3_iTd2 = s3_iTd2[newaxis,:,newaxis]
    s4_iTd2 = s4_iTd2[newaxis,:,newaxis]
    rho_iTd2 = rho_iTd2[newaxis,:,newaxis]

    T_iTd1 = Abrahamson08_coefficient_period[:,iTd1]
    T_iTd2 = Abrahamson08_coefficient_period[:,iTd2]

    T_iTd1 = T_iTd1[newaxis,:,newaxis]
    T_iTd2 = T_iTd2[newaxis,:,newaxis]

    ######
    # Magnitude and Distance Terms
    ######

    R = sqrt(Rrup**2 + c4T**2)

    f_1 = a1T + a5T*(Mw-c1T) + a8T*(8.5-Mw)**2 + (a2T + a3T*(Mw-c1T))*log(R)
    f_1 = where(Mw_tiled <= c1T,
                a1T + a4T*(Mw-c1T) + a8T*(8.5-Mw)**2 +
                    (a2T + a3T*(Mw-c1T))*log(R),
                f_1)

    del R

    # Calculation for Constant Displacement

    RTd1 = sqrt(Rrup**2 + c4_iTd1**2)

    f_1Td1 = (a1_iTd1 + a5_iTd1*(Mw-c1_iTd1) + a8_iTd1*(8.5-Mw)**2 +
              (a2_iTd1 + a3_iTd1*(Mw-c1_iTd1)) * log(RTd1))
    f_1Td1 = where(Mw_tiled <= c1_iTd1,
                   a1_iTd1 + a4_iTd1*(Mw-c1_iTd1) + a8_iTd1*(8.5-Mw)**2 +
                       (a2_iTd1 + a3_iTd1*(Mw-c1_iTd1)) * log(RTd1),
                   f_1Td1)

    del RTd1

    RTd2 = sqrt(Rrup**2 + c4_iTd2**2)

    f_1Td2 = (a1_iTd2 + a5_iTd2*(Mw-c1_iTd2) + a8_iTd2*(8.5-Mw)**2 +
              (a2_iTd2 + a3_iTd2*(Mw-c1_iTd2)) * log(RTd2))
    
    f_1Td2 = where(Mw_tiled <= c1_iTd2,
                   a1_iTd2 + a4_iTd2*(Mw-c1_iTd2) + a8_iTd2*(8.5-Mw)**2 +
                       (a2_iTd2 + a3_iTd2*(Mw-c1_iTd2)) * log(RTd2),
                   f_1Td2)

    del RTd2

    ######
    # Hanging-Wall Term
    ######

    RxTest = W*cos(Dip*pi/180.0)

    T1 = zeros(Rjb.shape)
    T1 = where(Rjb < 30.0, 1.0 - Rjb/30.0, T1)

    T2 = 0.5 + Rx/(2.0*RxTest)
    T2 = where(logical_or(Rx > RxTest, Dip == 90.0), 1.0, T2)

    oldsettings = seterr(divide='ignore')
    T3 = Rx/Ztor
    seterr(**oldsettings)
    
    T3 = where(Rx >= Ztor, 1.0, T3)

    T4 = ones(Mw.shape)
    T4 = where(Mw < 7.0, Mw - 6.0, T4)
    T4 = where(Mw <= 6.0, 0.0, T4)

    T5 = ones(Dip.shape)
    T5 = where(Dip >= 30.0, 1.0 - (Dip - 30.0)/60.0, T5)

    f_4 = a14T*T1*T2*T3*T4*T5

    # Calculation for Constant Displacement

    f_4Td1 = a14_iTd1*T1*T2*T3*T4*T5
    f_4Td2 = a14_iTd2*T1*T2*T3*T4*T5

    del RxTest, T1, T2, T3, T4, T5

    ######
    # Shallow Site Response Term for Rock (Vs30 = 1100 m/sec)
    ######

    V1 = ones(Per.shape) * 700.0
    V1 = where(Per < 2.0, exp(6.76 - 0.297*log(Per)), V1)
    V1 = where(Per <= 1.0, exp(8.0 - 0.795*log(Per/0.21)), V1)
    V1 = where(Per <= 0.5, 1500.0, V1)


    V30 = V1
    
    V30 = where(1100.0 < V1+zeros(Vs30.shape), Vs30+zeros(V30.shape),
                V30+zeros(Vs30.shape))

    f_5 = (a10T + bT*nT)*log(V30/VlinT)

    del V1, V30

    # Calculation for Constant Displacement

    V1Td1 = ones(T_iTd1.shape) * 700.0
    V1Td1 = where(T_iTd1 < 2.0, exp(6.76 - 0.297*log(T_iTd1)), V1Td1)
    V1Td1 = where(T_iTd1 <= 1.0, exp(8.0 - 0.795*log(T_iTd1/0.21)), V1Td1)
    V1Td1 = where(T_iTd1 <= 0.5, 1500.0, V1Td1)

    V30Td1 = copy(V1Td1)
    #Vs30X = Vs30 + 0*V1Td1
    Vs30X = Vs30 + ones(V1Td1.shape)
    V30Td1 = where(1100.0 < V1Td1+ones(Vs30.shape), Vs30X,
                   V30Td1+ones(Vs30.shape))
    f_5Td1 = (a10_iTd1 + b_iTd1*n_iTd1)*log(V30Td1/Vlin_iTd1)

    del V1Td1, V30Td1, Vs30X

    V1Td2 = ones(T_iTd2.shape) * 700.0
    V1Td2 = where(T_iTd2 < 2.0, exp(6.76 - 0.297*log(T_iTd2)), V1Td2)
    V1Td2 = where(T_iTd2 <= 1.0, exp(8.0 - 0.795*log(T_iTd2/0.21)), V1Td2)
    V1Td2 = where(T_iTd2 <= 0.5, 1500.0, V1Td2)

    V30Td2 = V1Td2
    V30Td2 = where(1100.0 < V1Td2+zeros(Vs30.shape), Vs30+zeros( V1Td2.shape),
                   V30Td2+zeros(Vs30.shape))
    f_5Td2 = (a10_iTd2 + b_iTd2*n_iTd2)*log(V30Td2/Vlin_iTd2)

    del V1Td2, V30Td2

    ######
    # Depth to top of Rupture Term
    ######

    f_6 = ones(Ztor.shape) * a16T
    XZtor = Ztor + zeros(f_6.shape)
    #f_6 = where(Ztor < 10.0, a16T*Ztor/10.0, f_6)
    f_6 = where(XZtor < 10.0, a16T*XZtor/10.0, f_6)
    del XZtor

    # Calcuation for Constant Dispalcement

    f_6Td1 = ones(Ztor.shape) * a16_iTd1
    f_6Td1 = where(Ztor < 10.0, a16_iTd1*Ztor/10.0, f_6Td1)

    f_6Td2 = ones(Ztor.shape) * a16_iTd2
    f_6Td2 = where(Ztor < 10.0, a16_iTd2*Ztor/10.0, f_6Td2)

    ######
    # Large Distance Term
    ######

    T6 = ones(Mw.shape) * 0.5
    T6 = where(Mw <= 6.5, 0.5*(6.5 - Mw) + 0.5, T6)
    T6 = where(Mw < 5.5, 1.0, T6)

    f_8 = a18T*(Rrup - 100.0)*T6
    XRrup = Rrup + zeros(f_8.shape)
    #f_8 = where(Rrup < 100.0, 0.0, f_8)
    f_8 = where(XRrup < 100.0, 0.0, f_8)
    del XRrup

    # Calculation for Constant Displacement

    f_8Td1 = a18_iTd1*(Rrup - 100.0)*T6
    f_8Td1 = where(Rrup < 100.0, 0.0, f_8Td1)

    f_8Td2 = a18_iTd2*(Rrup - 100.0)*T6
    f_8Td2 = where(Rrup < 100.0, 0.0, f_8Td2)

    del T6

    #####
    # Ground Motion on Rock Before Constant Displacement Adjustment
    #####

    Y_1100 = exp(f_1 + a12T*Frv + a13T*Fnm + a15T*Fas + f_5 +
                     Fhw*f_4 + f_6 + f_8)

    Y_1100Td1 = exp(f_1Td1 + a12_iTd1*Frv + a13_iTd1*Fnm +
                    a15_iTd1*Fas + f_5Td1 + Fhw*f_4Td1 + f_6Td1 + f_8Td1)

    Y_1100Td2 = exp(f_1Td2 + a12_iTd2*Frv + a13_iTd2*Fnm +
                    a15_iTd2*Fas + f_5Td2 + Fhw*f_4Td2 + f_6Td2 + f_8Td2)

    del f_1Td1, f_1Td2
    del f_6Td1, f_6Td2
    del f_8Td1, f_8Td2

    #####
    # Ground Motion on Rock After Constant Displacement Adjustment
    #####

    Y_1100Td0 = exp(log(Y_1100Td2/Y_1100Td1) /
                    log(T_iTd2/T_iTd1) *
                    log(Td/T_iTd1) + log(Y_1100Td1))

    Y_1100Td = Y_1100Td0*(Td/Per)**2
    Y_1100Td = where(Per <= Td+zeros(Y_1100.shape), Y_1100, Y_1100Td)

    del Y_1100, Y_1100Td0, Y_1100Td1, Y_1100Td2

    #####
    # Ground Motion on Local Site Conditions
    #####

    Y = exp(log(Y_1100Td) - f_5)

    del Y_1100Td, f_5

    # Shallow Site Response Term

    V1 = ones(Per.shape) * 700.0
    V1 = where(Per < 2.0, exp(6.76 - 0.297*log(Per)), V1)
    V1 = where(Per <= 1.0, exp(8.0 - 0.795*log(Per/0.21)), V1)
    V1 = where(Per <= 0.5, 1500.0, V1)

    V30 = V1
    XVs30 = Vs30 + zeros(V30.shape)
    #V30 = where(Vs30 < V1, Vs30, V1)
    V30 = where(XVs30 < V1+zeros(Vs30.shape), XVs30, V1+zeros(Vs30.shape))

    f_5 = (a10T + bT*nT)*log(V30/VlinT)
    f_5 = where(Vs30 < VlinT+zeros(PGA_1100.shape),
                a10T*log(V30/VlinT) - bT*log(PGA_1100 + cT) +
                    bT*log(PGA_1100 + cT*(V30/VlinT)**nT),
                f_5+zeros(PGA_1100.shape))
    del XVs30

    # Soil Depth Term

    Z10_med = exp(5.394 - 4.48*log(Vs30/500.0))
    Z10_med = where(Vs30 <= 500.0, exp(6.745 - 1.35*log(Vs30/180.0)), Z10_med)
    Z10_med = where(Vs30 < 180.0, exp(6.745), Z10_med)

    e2 = ones(Per.shape) * -0.25*log(Vs30/1000.0)*log(2.0/0.35)
    e2 = where(Per*ones(Vs30.shape) <= 2.0,
               -0.25*log(Vs30/1000.0)*log(Per/0.35), e2)
    e2 = where(logical_or(Per < 0.35, Vs30 > 1000.0), 0.0, e2)

    a22 = ones(Per.shape) * 0.0625*(Per - 2.0)
    a22 = where(Per < 2.0, 0.0, a22)

    a21Test = ((a10T + bT*nT)*log(V30/minimum(V1,1000.0)) +
               e2*log((Z10+c2T)/(Z10_med+c2T)))

    a21 = e2
    
    oldsettings = seterr(invalid='ignore')
    seterr(divide='ignore')
    a21 = where(a21Test < 0.0,
                -(a10T + bT*nT) *
                    log(V30/minimum(V1,1000.0))/log((Z10+c2T)/(Z10_med+c2T)),
                a21)
    seterr(**oldsettings)
    
    XVs30 = Vs30 + zeros(a21.shape)
    #a21 = where(Vs30 >= 1000.0, 0.0, a21)
    a21 = where(XVs30 >= 1000.0, 0.0, a21)

    f_10 = a21*log((Z10+c2T)/(Z10_med+c2T))
    XZ10 = Z10 + zeros(f_10.shape)
    XZ10_med = Z10_med + zeros(f_10.shape)
#    f_10 = where(Z10 >= 200.0,
#                 a21*log((Z10+c2T)/(Z10_med+c2T)) + a22*log(Z10/200.0),
#                 f_10)
    f_10 = where(XZ10 >= 200.0,
                 a21*log((XZ10+c2T)/(XZ10_med+c2T)) + a22*log(XZ10/200.0),
                 f_10)

    del Z10_med, e2, a22, a21Test, a21, XVs30, XZ10, XZ10_med, V1

    #####
    # Value of Ground Motion Parameter
    #####

    Y = exp(log(Y) + f_5 + f_10)

    del f_5, f_10

    #####
    # CALCULATE ALEATORY UNCERTAINTY
    # Partial Derivative of ln f_5 With Respect to ln PGA
    #####
    Alpha = zeros(V30.shape) + zeros(PGA_1100.shape)
    Alpha = where(Vs30 < VlinT+zeros(PGA_1100.shape),
                  bT*PGA_1100 * (1.0/(PGA_1100 + cT*(V30/VlinT)**nT) -
                                 1.0/(PGA_1100 + cT)),
                  Alpha)
    del V30

    #####
    # Intra-Event Standard Deviation
    #####

    slnAF = 0.3

    # Estimated Vs30

    s0Aest = ones(Mw.shape) * AS08_PGA_s2est
    s0Aest = where(Mw <= 7.0,
                   AS08_PGA_s1est + (AS08_PGA_s2est-AS08_PGA_s1est)*(Mw-5.0)/2.0,
                   s0Aest)
    s0Aest = where(Mw < 5.0, AS08_PGA_s1est, s0Aest)

    s0Yest = ones(Mw.shape) * s2estT
    XMw = Mw + zeros(s0Yest.shape)
#    s0Yest = where(Mw <= 7.0, s1estT + (s2estT-s1estT)*(Mw-5.0)/2.0, s0Yest)
#    s0Yest = where(Mw < 5.0, s1estT, s0Yest)
    s0Yest = where(XMw <= 7.0, s1estT + (s2estT-s1estT)*(XMw-5.0)/2.0, s0Yest)
    s0Yest = where(XMw < 5.0, s1estT*ones(Mw.shape), s0Yest)
    sBAest = sqrt(s0Aest**2 - slnAF**2)
    sBYest = sqrt(s0Yest**2 - slnAF**2)

    del s0Aest, s0Yest, XMw 

    # Measured Vs30

    s0Amea = ones(Mw.shape) * AS08_PGA_s2mea
    s0Amea = where(Mw <= 7.0,
                   (AS08_PGA_s1mea + AS08_PGA_s2mea-AS08_PGA_s1mea)*(Mw-5.0)/2.0,
                   s0Amea)
    s0Amea = where(Mw < 5.0, AS08_PGA_s1mea, s0Amea)

    s0Ymea = ones(Mw.shape) * s2meaT
    XMw = Mw + zeros(s0Ymea.shape)
#    s0Ymea = where(Mw <= 7.0, s1meaT + (s2meaT-s1meaT)*(Mw-5.0)/2.0, s0Ymea)
#    s0Ymea = where(Mw < 5.0, s1meaT, s0Ymea)
    s0Ymea = where(XMw <= 7.0, s1meaT + (s2meaT-s1meaT)*(XMw-5.0)/2.0, s0Ymea)
    s0Ymea = where(XMw < 5.0, s1meaT*ones(Mw.shape), s0Ymea)

    sBAmea = sqrt(s0Amea**2 - slnAF**2)
    sBYmea = sqrt(s0Ymea**2 - slnAF**2)

    del s0Amea, s0Ymea, XMw

    #####
    # Inter-Event Standard Deviation
    #####

    tau0A = ones(Mw.shape) * AS08_PGA_s4
    tau0A = where(Mw <= 7.0,
                  AS08_PGA_s3 + (AS08_PGA_s4-AS08_PGA_s3)*(Mw-5.0)/2.0,
                  tau0A)
    tau0A = where(Mw < 5.0, AS08_PGA_s3, tau0A)

    tau0Y = ones(Mw.shape) * s4T
    XMw = Mw + zeros(tau0Y.shape)
#    tau0Y = where(Mw <= 7.0, s3T + (s4T-s3T)*(Mw-5.0)/2.0, tau0Y)
#    tau0Y = where(Mw < 5.0, s3T, tau0Y)
    tau0Y = where(XMw <= 7.0, s3T + (s4T-s3T)*(XMw-5.0)/2.0, tau0Y)
    tau0Y = where(XMw < 5.0, s3T*ones(Mw.shape), tau0Y)

    tauBA = tau0A
    tauBY = tau0Y

    del tau0A

    #####
    # Standard Deviation of Geometric Mean of ln Y
    #####

    Tau = sqrt(tau0Y**2 + (Alpha**2)*(tauBA**2) + 2.0*Alpha*rhoT*tauBY*tauBA)

    del tau0Y, tauBA, tauBY

    # Estimated Vs30

    Sigest = sqrt(sBYest**2 + slnAF**2 + (Alpha**2)*(sBAest**2) +
                  2.0*Alpha*rhoT*sBYest*sBAest)
    del sBAest, sBYest

    SigTest = sqrt(Sigest**2 + Tau**2)

    del Sigest, Tau

# unused
#    # Measured Vs30
#
#    Sigmea = sqrt(sBYmea**2 + slnAF**2 + (Alpha**2)*(sBAmea**2) +
#                  2.0*Alpha*rhoT*sBYmea*sBAmea)
#
#    SigTmea = sqrt(Sigmea**2 + Tau**2)

    # check result has right dimensions
    num_sites = Vs30.shape[0]
    assert Y.shape == (num_sites, num_events, num_periods), (msg
               % ('Y', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(Y.shape)))
    assert SigTest.shape == (num_sites, num_events, num_periods), (msg
               % ('SigTest', '(%d,%d,%d)' % (num_sites, num_events, num_periods),
                  str(SigTest.shape)))

    return (log(Y), SigTest)


######
# Set up a numpy array to convert a 'fault_type' flag to an array
# that encodes the Frv/Fnm flags.
######

# faulting type flag encodings
#                      'type':      (Frv, Fnm)
AS08_faulting_flags = {'reverse':     (1, 0),
                       'normal':      (0, 1),
                       'strike_slip': (0, 0)}

# generate 'AS08_fault_type' from the dictionary above
tmp = []
for (k, v) in AS08_faulting_flags.iteritems():
    index = ground_motion_misc.FaultTypeDictionary[k]
    tmp.append((index, v))

# sort and make array in correct index order
tmp2 = []
tmp.sort()
for (_, flags) in tmp:
    tmp2.append(flags)
AS08_fault_type = array(tmp2)
del tmp, tmp2

# Tables 4. 5a, 5b and 6
# Abrahamson and Silva (2008); Final Model; Earthquake Spectra, Vol. 24, p. 67-97 (2008)
# Coefficients for the Average Horizontal Component of Ground Motion

AS08_coeff = array([
#T(s)  c1   c4  a3     a4     a5    n    c    c2    VLIN   b      a1      a2      a8      a10    a12     a13    a14     a15     a16     a18    s1est s2est s1mea s2mea s3    s4    rho
[0.000,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 865.1,-1.186, 0.8040,-0.9679,-0.0372, 0.9445,0.0000,-0.0600,1.0800,-0.3500, 0.9000,-0.0067,0.590,0.470,0.576,0.453,0.470,0.300,1.000],
[0.010,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 865.1,-1.186, 0.8110,-0.9679,-0.0372, 0.9445,0.0000,-0.0600,1.0800,-0.3500, 0.9000,-0.0067,0.590,0.470,0.576,0.453,0.420,0.300,1.000],
[0.020,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 865.1,-1.219, 0.8550,-0.9774,-0.0372, 0.9834,0.0000,-0.0600,1.0800,-0.3500, 0.9000,-0.0067,0.590,0.470,0.576,0.453,0.420,0.300,1.000],
[0.030,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 907.8,-1.273, 0.9620,-1.0024,-0.0372, 1.0471,0.0000,-0.0600,1.1331,-0.3500, 0.9000,-0.0067,0.605,0.478,0.591,0.461,0.462,0.305,0.991],
[0.040,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 994.5,-1.308, 1.0370,-1.0289,-0.0315, 1.0884,0.0000,-0.0600,1.1708,-0.3500, 0.9000,-0.0067,0.615,0.483,0.602,0.466,0.492,0.309,0.982],
[0.050,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0,1053.5,-1.346, 1.1330,-1.0508,-0.0271, 1.1333,0.0000,-0.0600,1.2000,-0.3500, 0.9000,-0.0076,0.623,0.488,0.610,0.471,0.515,0.312,0.973],
[0.075,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0,1085.7,-1.471, 1.3750,-1.0810,-0.0191, 1.2808,0.0000,-0.0600,1.2000,-0.3500, 0.9000,-0.0093,0.630,0.495,0.617,0.479,0.550,0.317,0.952],
[0.100,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0,1032.5,-1.624, 1.5630,-1.0833,-0.0166, 1.4613,0.0000,-0.0600,1.2000,-0.3500, 0.9000,-0.0093,0.630,0.501,0.617,0.485,0.550,0.321,0.929],
[0.150,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 877.6,-1.931, 1.7160,-1.0357,-0.0254, 1.8071,0.0181,-0.0600,1.1683,-0.3500, 0.9000,-0.0093,0.630,0.509,0.616,0.491,0.550,0.326,0.896],
[0.200,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 748.2,-2.188, 1.6870,-0.9700,-0.0396, 2.0773,0.0309,-0.0600,1.1274,-0.3500, 0.9000,-0.0083,0.630,0.514,0.614,0.495,0.520,0.329,0.874],
[0.250,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 654.3,-2.381, 1.6460,-0.9202,-0.0539, 2.2794,0.0409,-0.0600,1.0956,-0.3500, 0.9000,-0.0069,0.630,0.518,0.612,0.497,0.497,0.332,0.856],
[0.300,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 587.1,-2.518, 1.6010,-0.8974,-0.0656, 2.4201,0.0491,-0.0600,1.0697,-0.3500, 0.9000,-0.0057,0.630,0.522,0.611,0.499,0.479,0.335,0.841],
[0.400,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 503.0,-2.657, 1.5110,-0.8677,-0.0807, 2.5510,0.0619,-0.0600,1.0288,-0.3500, 0.8423,-0.0039,0.630,0.527,0.608,0.501,0.449,0.338,0.818],
[0.500,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 456.6,-2.669, 1.3970,-0.8475,-0.0924, 2.5395,0.0719,-0.0600,0.9971,-0.3191, 0.7458,-0.0025,0.630,0.532,0.606,0.504,0.426,0.341,0.783],
[0.750,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 410.5,-2.401, 1.1370,-0.8206,-0.1137, 2.1493,0.0800,-0.0600,0.9395,-0.2629, 0.5704, 0.0000,0.630,0.539,0.602,0.506,0.385,0.346,0.680],
[1.000,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0,-1.955, 0.9150,-0.8088,-0.1289, 1.5705,0.0800,-0.0600,0.8985,-0.2230, 0.4460, 0.0000,0.630,0.545,0.594,0.503,0.350,0.350,0.607],
[1.500,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0,-1.025, 0.5100,-0.7995,-0.1534, 0.3991,0.0800,-0.0600,0.8409,-0.1668, 0.2707, 0.0000,0.615,0.552,0.566,0.497,0.350,0.350,0.504],
[2.000,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0,-0.299, 0.1920,-0.7960,-0.1708,-0.6072,0.0800,-0.0600,0.8000,-0.1270, 0.1463, 0.0000,0.604,0.558,0.544,0.491,0.350,0.350,0.431],
[3.000,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-0.2800,-0.7960,-0.1954,-0.9600,0.0800,-0.0600,0.4793,-0.0708,-0.0291, 0.0000,0.589,0.565,0.527,0.500,0.350,0.350,0.328],
[4.000,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-0.6390,-0.7960,-0.2128,-0.9600,0.0800,-0.0600,0.2518,-0.0309,-0.1535, 0.0000,0.578,0.570,0.515,0.505,0.350,0.350,0.255],
[5.000,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-0.9360,-0.7960,-0.2263,-0.9208,0.0800,-0.0600,0.0754, 0.0000,-0.2500, 0.0000,0.570,0.587,0.510,0.529,0.350,0.350,0.200],
[7.500,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-1.5270,-0.7960,-0.2509,-0.7700,0.0800,-0.0600,0.0000, 0.0000,-0.2500, 0.0000,0.611,0.618,0.572,0.579,0.350,0.350,0.200],
[10.00,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-1.9930,-0.7960,-0.2683,-0.6630,0.0800,-0.0600,0.0000, 0.0000,-0.2500, 0.0000,0.640,0.640,0.612,0.612,0.350,0.350,0.200]])

# dim = (#coefficients, #periods)
Abrahamson08_coefficient = AS08_coeff[:,1:21].transpose()

# dim = (period,)
Abrahamson08_coefficient_period = AS08_coeff[:,0]

# dim = (sigmacoefficient, period)
Abrahamson08_sigma_coefficient = AS08_coeff[:,21:28].transpose()

# dim = (period,)
Abrahamson08_sigma_coefficient_period = AS08_coeff[:,0]

AS08_PGA_coefficients = AS08_coeff[0,1:21]

AS08_PGA_sigma_coefficients = AS08_coeff[0,21:28]

# number of periods
AS08_nper = len(Abrahamson08_coefficient_period)

Abrahamson08_magnitude_type='ML'
Abrahamson08_distance_type='Epicentral'
Abrahamson08_interpolation = linear_interpolation
Abrahamson08_uses_Vs30 = True


Abrahamson08_args = [Abrahamson08_distribution,
                     Abrahamson08_magnitude_type,
                     Abrahamson08_distance_type,

                     Abrahamson08_coefficient,
                     Abrahamson08_coefficient_period,
                     Abrahamson08_interpolation,

                     Abrahamson08_sigma_coefficient,
                     Abrahamson08_sigma_coefficient_period,
                     Abrahamson08_interpolation,

                     Abrahamson08_uses_Vs30]

ground_motion_init['Abrahamson08'] = Abrahamson08_args

del AS08_coeff

#########################  End of Abrahamson08 model  ##########################

########################  Start of Akkar-Bommer 2010 model  #####################

"""Code here is based on Akkar and Bommer [1].

    [1] 
"""
def Akkar_2010_crustal_distribution(**kwargs):

    # get args
    M = kwargs['mag']
##    print M
    Rjb = kwargs['distance']
    FT = kwargs['fault_type']
    Vs30 = kwargs['Vs30']
##    Sso = kwargs['soft_soil']
##    Ssti = kwargs['stiff_soil']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
##    # check we have the right shapes
    num_periods = coefficient.shape[3]
    msg = ('Expected coefficient.shape %s, got %s'
           % (str((10, 1, 1, num_periods)), str(coefficient.shape)))
    assert coefficient.shape == (10, 1, 1, num_periods), msg
    msg = ('Expected sigma_coefficient.shape %s, got %s'
           % (str((2, 1, 1, num_periods)), str(sigma_coefficient.shape)))
    assert sigma_coefficient.shape == (2, 1, 1, num_periods), msg

    # unpack coefficients
    (b1, b2, b3, b4, b5, b6, b7, b8, b9, b10) = coefficient
    (b11, b12) = sigma_coefficient

    # Model
    Frv = 0;
    Fnm = 0;
    Frv = where(FT==0,1,Frv)
    Fnm = where(FT==1,1,Fnm)
    Sso = 0
    Ssti = 0
    Sso = where(Vs30<360,1,Sso)
    Ssti = where(logical_and(Vs30>360,Vs30<750),1,Ssti)
    
##    print Fnm,Frv,Sso,Ssti,M,Rjb
    logSa = b1 + b2*M + b3*M**2 + (b4+b5*M)*log10(sqrt(Rjb**2+b6**2)) + b7*Sso + b8*Ssti + b9*Fnm + b10*Frv;
##    print logSa
    logSa = log(10**(logSa)/981);
    sigma = sqrt(b11**2+b12**2)
    
    sigma = log(10**sigma)
    events_num = Rjb.shape[1]
    sigma = tile(sigma,(1,events_num,1))
    return (logSa , sigma)

Akkar_2010_crustal_magnitude_type = 'Mw'
Akkar_2010_crustal_distance_type = 'Joyner_Boore'

######
# Start building the coefficient array
######
coefficient = array ( [(1.04159,2.11528,2.11994,1.64489,0.92065,0.13978,-0.84006,-1.32207,-1.70320,-1.97201,-2.76925,-3.51672,-3.92759,-4.49490,-4.62925,-4.95053,-5.32863,-5.75799,-5.82689,-5.90592,-6.17066,-6.60337,-6.90379,-6.96180,-6.99236,-6.74613,-6.51719,-6.55821,-6.61945,-6.62737,-6.71787,-6.80776,-6.83632,-6.88684,-6.94600,-7.09166,-7.22818,-7.29772,-7.35522,-7.40716,-7.50404,-7.55598,-7.53463,-7.50811,-8.09168,-8.11057,-8.16272,-7.94704,-7.96679,-7.97878,-7.88403,-7.68101,-7.72574,-7.53288,-7.41587,-7.34541,-7.24561,-7.07107,-6.99332,-6.95669,-6.92924),
    (0.91333,0.72571,0.75179,0.83683,0.96815,1.13068,1.37439,1.47055,1.5593,1.61645,1.83268,2.02523,2.08471,2.21154,2.21764,2.29142,2.38389,2.50635,2.50287,2.51405,2.58558,2.69584,2.77044,2.75857,2.73427,2.62375,2.51869,2.52238,2.52611,2.49858,2.49486,2.50291,2.51009,2.54048,2.57151,2.62938,2.66824,2.67565,2.67749,2.68206,2.71004,2.72737,2.71709,2.71035,2.91159,2.92087,2.93325,2.85328,2.85363,2.849,2.81817,2.7572,2.82043,2.74824,2.69012,2.65352,2.61028,2.56123,2.52699,2.51006,2.45899),
    (-0.08140,-0.07351,-0.07448,-0.07544,-0.07903,-0.08761,-0.10349,-0.10873,-0.11388,-0.11742,-0.13202,-0.14495,-0.14648,-0.15522,-0.15491,-0.15983,-0.16571,-0.17479,-0.17367,-0.17417,-0.17938,-0.18646,-0.19171,-0.18890,-0.18491,-0.17392,-0.16330,-0.16307,-0.16274,-0.15910,-0.15689,-0.15629,-0.15676,-0.15995,-0.16294,-0.16794,-0.17057,-0.17004,-0.16934,-0.16906,-0.17130,-0.17291,-0.17221,-0.17212,-0.18920,-0.19044,-0.19155,-0.18539,-0.18561,-0.18527,-0.18320,-0.17905,-0.18717,-0.18142,-0.17632,-0.17313,-0.16951,-0.16616,-0.16303,-0.16142,-0.15513),
    (-2.92728,-3.33201,-3.10538,-2.75848,-2.49264,-2.33824,-2.19123,-2.12993,-2.12718,-2.16619,-2.12969,-2.04211,-1.88144,-1.79031,-1.79800,-1.81321,-1.77273,-1.77068,-1.76295,-1.79854,-1.80717,-1.73843,-1.71109,-1.66588,-1.59120,-1.52886,-1.46527,-1.48223,-1.48257,-1.43310,-1.35301,-1.31227,-1.33260,-1.40931,-1.47676,-1.54037,-1.54273,-1.50936,-1.46988,-1.43816,-1.44395,-1.45794,-1.46662,-1.49679,-1.55644,-1.59537,-1.60461,-1.57428,-1.57833,-1.57728,-1.60381,-1.65212,-1.88782,-1.89525,-1.87041,-1.86079,-1.85612,-1.90422,-1.89704,-1.90132,-1.76801),
    (0.2812,0.33534,0.30253,0.2549,0.2179,0.20089,0.18139,0.17485,0.17137,0.177,0.16877,0.15617,0.13621,0.12916,0.13495,0.1392,0.13273,0.13096,0.13059,0.13535,0.13599,0.12485,0.12227,0.11447,0.10265,0.09129,0.08005,0.08173,0.08213,0.07577,0.06379,0.05697,0.0587,0.0686,0.07672,0.08428,0.08325,0.07663,0.07065,0.06525,0.06602,0.06774,0.0694,0.07429,0.08428,0.09052,0.09284,0.09077,0.09288,0.09428,0.09887,0.1068,0.14049,0.14356,0.14283,0.1434,0.14444,0.15127,0.15039,0.15081,0.13314),
    (7.86638,7.74734,8.21405,8.31786,8.21914,7.20688,6.54299,6.24751,6.57173,6.78082,7.17423,6.7617,6.10103,5.19135,4.46323,4.27945,4.37011,4.62192,4.65393,4.8454,4.97596,5.04489,5.00975,5.08902,5.03274,5.08347,5.14423,5.29006,5.3349,5.19412,5.1575,5.27441,5.54539,5.93828,6.36599,6.82292,7.11603,7.31928,7.25988,7.25344,7.26059,7.4032,7.46168,7.51273,7.77062,7.87702,7.91753,7.61956,7.59643,7.50338,7.53947,7.61893,8.12248,7.92236,7.49999,7.26668,7.11861,7.36277,7.45038,7.60234,7.2195),
    (0.08753,0.04707,0.02667,0.02578,0.06557,0.0981,0.12847,0.16213,0.21222,0.24121,0.25944,0.26498,0.27718,0.28574,0.30348,0.31516,0.32153,0.3352,0.34849,0.35919,0.36619,0.37278,0.37756,0.38149,0.3812,0.38782,0.38862,0.38677,0.38625,0.38285,0.37867,0.37267,0.36952,0.36531,0.35936,0.35284,0.34775,0.34561,0.34142,0.3372,0.33298,0.3301,0.32645,0.32439,0.31354,0.30997,0.30826,0.32071,0.31801,0.31401,0.31104,0.30875,0.31122,0.30935,0.30688,0.30635,0.30534,0.30508,0.30362,0.29987,0.29772),
    (0.01527,-0.02426,-0.00062,0.01703,0.02105,0.03919,0.0434,0.06695,0.09201,0.11675,0.13562,0.14446,0.15156,0.15239,0.15652,0.16333,0.17366,0.1848,0.19061,0.19411,0.19519,0.19461,0.19423,0.19402,0.19309,0.19392,0.19273,0.19082,0.19285,0.19161,0.18812,0.18568,0.18149,0.17617,0.17301,0.16945,0.16743,0.1673,0.16325,0.16171,0.15839,0.15496,0.15337,0.15264,0.1443,0.1443,0.14412,0.14321,0.14301,0.14324,0.14332,0.14343,0.14255,0.14223,0.14074,0.14052,0.13923,0.13933,0.13776,0.13584,0.13198),
    (-0.04189,-0.04260,-0.04906,-0.04184,-0.02098,-0.04853,-0.05554,-0.04722,-0.05145,-0.05202,-0.04283,-0.04259,-0.03853,-0.03423,-0.04146,-0.04050,-0.03946,-0.03786,-0.02884,-0.02209,-0.02269,-0.02613,-0.02655,-0.02088,-0.01623,-0.01826,-0.01902,-0.01842,-0.01607,-0.01288,-0.01208,-0.00845,-0.00533,-0.00852,-0.01204,-0.01386,-0.01402,-0.01526,-0.01563,-0.01848,-0.02258,-0.02626,-0.02920,-0.03484,-0.03985,-0.04155,-0.04238,-0.04963,-0.04910,-0.04812,-0.04710,-0.04607,-0.05106,-0.05024,-0.04887,-0.04743,-0.04731,-0.04522,-0.04203,-0.03863,-0.03855),
    (0.08015,0.08649,0.0791,0.0784,0.08438,0.08577,0.09221,0.09003,0.09903,0.09943,0.08579,0.06945,0.05932,0.05111,0.04661,0.04253,0.03373,0.02867,0.02475,0.02502,0.02121,0.01115,0.0014,0.00148,0.00413,0.00413,-0.00369,-0.00897,-0.00876,-0.00564,-0.00215,-0.00047,-0.00006,-0.00301,-0.00744,-0.01387,-0.01492,-0.01192,-0.00703,-0.00351,-0.00486,-0.00731,-0.00871,-0.01225,-0.01927,-0.02322,-0.02626,-0.02342,-0.02570,-0.02643,-0.02769,-0.02819,-0.02966,-0.02930,-0.02963,-0.02919,-0.02751,-0.02776,-0.02615,-0.02487,-0.02469),
    (0.261,0.272,0.2728,0.2788,0.2821,0.2871,0.2902,0.2983,0.2998,0.3037,0.3078,0.307,0.3007,0.3004,0.2978,0.2973,0.2927,0.2917,0.2915,0.2912,0.2895,0.2888,0.2896,0.2871,0.2878,0.2863,0.2869,0.2885,0.2875,0.2857,0.2839,0.2845,0.2844,0.2841,0.284,0.284,0.2834,0.2828,0.2826,0.2832,0.2835,0.2836,0.2832,0.283,0.283,0.283,0.2829,0.2815,0.2826,0.2825,0.2818,0.2818,0.2838,0.2845,0.2854,0.2862,0.2867,0.2869,0.2874,0.2872,0.2876),
    (0.0994,0.1142,0.1167,0.1192,0.1081,0.099,0.0976,0.1054,0.1101,0.1123,0.1163,0.1274,0.143,0.1546,0.1626,0.1602,0.1584,0.1543,0.1521,0.1484,0.1483,0.1465,0.1427,0.1435,0.1439,0.1453,0.1427,0.1428,0.1458,0.1477,0.1468,0.145,0.1457,0.1503,0.1537,0.1558,0.1582,0.1592,0.1611,0.1642,0.1657,0.1665,0.1663,0.1661,0.1627,0.1627,0.1633,0.1632,0.1645,0.1665,0.1681,0.1688,0.1741,0.1759,0.1772,0.1783,0.1794,0.1788,0.1784,0.1783,0.1785)])

Akkar_2010_crustal_coefficient = coefficient[0:10,:]
Akkar_2010_crustal_coefficient_period = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2,2.05,2.1,2.15,2.2,2.25,2.3,2.35,2.4,2.45,2.5,2.55,2.6,2.65,2.7,2.75,2.8,2.85,2.9,2.95,3]

Akkar_2010_crustal_sigma_coefficient = coefficient[10:,:]
Akkar_2010_crustal_sigma_coefficient_period = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1,1.05,1.1,1.15,1.2,1.25,1.3,1.35,1.4,1.45,1.5,1.55,1.6,1.65,1.7,1.75,1.8,1.85,1.9,1.95,2,2.05,2.1,2.15,2.2,2.25,2.3,2.35,2.4,2.45,2.5,2.55,2.6,2.65,2.7,2.75,2.8,2.85,2.9,2.95,3]
    
Akkar_2010_crustal_interpolation = linear_interpolation

Akkar_2010_crustal_uses_Vs30 = True

ground_motion_init['Akkar_2010_crustal'] = [Akkar_2010_crustal_distribution,
                                Akkar_2010_crustal_magnitude_type,
                                Akkar_2010_crustal_distance_type,
                                
                                Akkar_2010_crustal_coefficient,
                                Akkar_2010_crustal_coefficient_period,
                                Akkar_2010_crustal_interpolation,
                                
                                Akkar_2010_crustal_sigma_coefficient,
                                Akkar_2010_crustal_sigma_coefficient_period,
                                Akkar_2010_crustal_interpolation,
                                
                                Akkar_2010_crustal_uses_Vs30]

#---------------------------end of Akkar and Bommer 2010-----------------------


##########################  Start of Atkinson_Boore_interface model (Atkinson_2003_interface)  ###########################
### Atkinson_Boore model for interface events (Zt = 0)
##
########
### The model function, from [1] .
########
##
##def Atkinson_2003_interface_distribution(**kwargs): #T,M,h,Df,Zt,Vs30,Zl):
##
##    
##    # get args
##    T = kwargs['periods']
##    M = kwargs['mag']				# event-specific
##    h = kwargs['depth']
##    Df = kwargs['distance']			# event-site-specific
##    Vs30 = kwargs['Vs30']
####    Zl = kwargs['region']
##    coefficient = kwargs['coefficient']
##    sigma_coefficient = kwargs['sigma_coefficient']
###    coefficient_PGA = kwargs['coefficient_PGA']
##
##    # unpack coefficients
##    (c1_it,c1_it_jp,c1_it_cas,c2_it,c3_it,c4_it,c5_it,c6_it,c7_it) = coefficient
##    (c10_it,c10_it_jp,c10_it_cas,c20_it,c30_it,c40_it,c50_it,c60_it,c70_it) = Atkinson_2003_interface_PGA_coefficient
####    (sigma_it) = sigma_coefficient
##    (sig1,sig2) = sigma_coefficient
##
##     # Model estimation
##
##    h = where (h>=100,100,h)   
##
##
##
##    M = where(M >= 8.5, 8.5, M)
##    
##    delta = 0.00724*(10**(0.507*M))
##    R = sqrt(Df**2 + delta**2)
##
##
##    g = 10**(1.2 - 0.18*M)
##           
##
##    Sc = zeros(shape(Vs30))
##    Sd = zeros(shape(Vs30))
##    Se = zeros(shape(Vs30))
##    Ze = zeros(shape(Vs30))
##    
##    Sc = where(Vs30<180,0,Ze)
##    Sd = where(Vs30<180,0,Ze)
##    Se = where(Vs30<180,1,Ze)
##    
##    Sc = where(Vs30>=180,0,Sc)
##    Sd = where(Vs30>=180,1,Sd)
##    Se = where(Vs30>=180,0,Se)
##    
##    Sc = where(Vs30>360,1,Sc)
##    Sd = where(Vs30>360,0,Sd)
##    Se = where(Vs30>360,0,Se)
##    
##    Sc = where(Vs30>760,0,Sc)
##    Sd = where(Vs30>760,0,Sd)
##    Se = where(Vs30>760,0,Se)
##
####    print Vs30,Sc, Sd, Se
##    Zl = 0
##    c10 = c10_it_jp
##    c10 = where(Zl == 1, c10_it_cas, c10)
##    c10 = where(Zl == 0, c10_it, c10)
##    
##    log_PGArx = c10 + c20_it*M + c30_it*h + c40_it*R - g*log10(R)
##    PGArx = 10**(log_PGArx)
####    print PGArx
##    T = where(T==0,.00000000000001,T)
##    sl = [0]
##    sl = where(logical_and(1/T>=2,PGArx<500),1 - (PGArx - 100)/400,sl)
##    sl = where(logical_and(1/T<2,PGArx<500),1 - ((1/T)-1)*(PGArx - 100)/400,sl)
##    sl = where(logical_and(1/T<2,PGArx>=500),1 - ((1/T)-1),sl)
##
####    print sl
##    c1 = c1_it_jp
##    c1 = where(Zl == 1, c1_it_cas, c1)
##    c1 = where(Zl == 0, c1_it, c1)
##
##    #print c1,c2_it,c3_it,c4_it,c5_it,c6_it,c7_it
##    #print M,h,R,sl,Sc,Sd,Se,g
##    log_10_Y = c1 + c2_it*M + c3_it*h + c4_it*R - g*log10(R) + c5_it*sl*Sc + c6_it*sl*Sd + c7_it*sl*Se
####    print log_10_Y
##    logSa = log(10**(log_10_Y)/981)
####    print logSa
##    
##    sigma_10 = sqrt(sig1**2+sig2**2)
##    sigma = log(10**sigma_10)
##    events_num = Df.shape[1]
##    sigma = tile(sigma,(1,events_num,1))
####    print sigma_10
####
##    return (logSa, sigma)
##
##Atkinson_2003_interface_magnitude_type = 'Mw'
##Atkinson_2003_interface_distance_type = 'Rupture'
####    
##    # Interslab Events Coefficients
##
##coef_it = array([(0,0.0400000000000000,0.100000000000000,0.200000000000000,0.400000000000000,1,2,3.03030303030303),
##    (2.99100000000000,2.87530000000000,2.77890000000000,2.66380000000000,2.52490000000000,2.14420000000000,2.19070000000000,2.30100000000000),
##    (3.14000000000000,3.05000000000000,2.95000000000000,2.84000000000000,2.58000000000000,2.18000000000000,2.14000000000000,2.27000000000000),
##    (2.79000000000000,2.60000000000000,2.50000000000000,2.54000000000000,2.50000000000000,2.18000000000000,2.33000000000000,2.36000000000000),
##    (0.0352500000000000,0.0705200000000000,0.0984100000000000,0.123860000000000,0.147700000000000,0.134500000000000,0.0714800000000000,0.0223700000000000),
##    (0.00759000000000000,0.0100400000000000,0.00974000000000000,0.00884000000000000,0.00728000000000000,0.00521000000000000,0.00224000000000000,0.000120000000000000),
##    (-0.00206000000000000,-0.00278000000000000,-0.00287000000000000,-0.00280000000000000,-0.00235000000000000,-0.00110000000000000,0,0),
##    (0.190000000000000,0.150000000000000,0.150000000000000,0.150000000000000,0.130000000000000,0.100000000000000,0.100000000000000,0.100000000000000),
##    (0.240000000000000,0.200000000000000,0.230000000000000,0.270000000000000,0.370000000000000,0.300000000000000,0.250000000000000,0.250000000000000),
##    (0.290000000000000,0.200000000000000,0.200000000000000,0.250000000000000,0.380000000000000,0.550000000000000,0.400000000000000,0.360000000000000),
##    (0.230000000000000,0.260000000000000,0.270000000000000,0.280000000000000,0.290000000000000,0.340000000000000,0.340000000000000,0.360000000000000),
##    (0.200000000000000,0.220000000000000,0.250000000000000,0.250000000000000,0.250000000000000,0.280000000000000,0.290000000000000,0.310000000000000),
##    (0.110000000000000,0.140000000000000,0.100000000000000,0.130000000000000,0.150000000000000,0.190000000000000,0.180000000000000,0.180000000000000)])
##Atkinson_2003_interface_coefficient = coef_it[1:10,:]
##Atkinson_2003_interface_coefficient_period = coef_it[0]
##Atkinson_2003_interface_sigma_coefficient = coef_it[11:13,:]
##Atkinson_2003_interface_sigma_coefficient_period = coef_it[0]
##
##Atkinson_2003_interface_PGA_coefficient = coef_it[1:10,0]
##
##Atkinson_2003_interface_interpolation = linear_interpolation
##
##Atkinson_2003_interface_uses_Vs30 = True
##
##ground_motion_init['Atkinson_2003_interface'] = [Atkinson_2003_interface_distribution,
##                              Atkinson_2003_interface_magnitude_type,
##                              Atkinson_2003_interface_distance_type,
##
##                              Atkinson_2003_interface_coefficient,
##                              Atkinson_2003_interface_coefficient_period,
##                              Atkinson_2003_interface_interpolation,
##                          
##                              Atkinson_2003_interface_sigma_coefficient,
##                              Atkinson_2003_interface_sigma_coefficient_period,
##                              Atkinson_2003_interface_interpolation,
##                          
##                              Atkinson_2003_interface_uses_Vs30]
##########################  Start of Atkinson_Boore_slab model (Atkinson_2003_intraslab)  ###########################
# Atkinson_Boore model for slab events (Zt = 1)

######
# The model function, from [1] .
######

def Atkinson_2003_intraslab_distribution(**kwargs): #T,M,h,Df,Zt,Vs30,Zl):

    
    # get args
    T = kwargs['periods']
    M = kwargs['mag']				# event-specific
    h = kwargs['depth']
    Df = kwargs['distance']			# event-site-specific
    Vs30 = kwargs['Vs30']
##    Zl = kwargs['region']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
#    coefficient_PGA = kwargs['coefficient_PGA']

    T = T[newaxis,newaxis,:]

    # unpack coefficients
    (c1_it,c1_it_jp,c1_it_cas,c2_it,c3_it,c4_it,c5_it,c6_it,c7_it) = coefficient
    (c10_it,c10_it_jp,c10_it_cas,c20_it,c30_it,c40_it,c50_it,c60_it,c70_it) = Atkinson_2003_intraslab_PGA_coefficient
##    (sigma_it) = sigma_coefficient
    (sig1,sig2) = sigma_coefficient

     # Model estimation

    h = where (h>=100,100,h)   



    M = where(M >= 8.0, 8.0, M)
    
    delta = 0.00724*(10**(0.507*M))
    R = sqrt(Df**2 + delta**2)


    g = 10**(0.301 - 0.01*M)
##    print g      

    Sc = zeros(shape(Vs30))
    Sd = zeros(shape(Vs30))
    Se = zeros(shape(Vs30))
    Ze = zeros(shape(Vs30))
    
    Sc = where(Vs30<180,0,Ze)
    Sd = where(Vs30<180,0,Ze)
    Se = where(Vs30<180,1,Ze)
    
    Sc = where(Vs30>=180,0,Sc)
    Sd = where(Vs30>=180,1,Sd)
    Se = where(Vs30>=180,0,Se)
    
    Sc = where(Vs30>360,1,Sc)
    Sd = where(Vs30>360,0,Sd)
    Se = where(Vs30>360,0,Se)
    
    Sc = where(Vs30>760,0,Sc)
    Sd = where(Vs30>760,0,Sd)
    Se = where(Vs30>760,0,Se)

##    print Vs30,Sc, Sd, Se
    Zl = zeros(c1_it.shape)
    c10 = c10_it_jp
    c10 = where(Zl == 1, c10_it_cas, c10)
    c10 = where(Zl == 0, c10_it, c10)
    
    log_PGArx = c10 + c20_it*M + c30_it*h + c40_it*R - g*log10(R)
    PGArx = 10**(log_PGArx) + zeros(T.shape)

##    print PGArx
    T = where(T==0,.00000000000001,T)
    sl = zeros(PGArx.shape)
    sl = where(logical_and(1/T>=2,PGArx<500),1 - (PGArx - 100)/400,sl)
    sl = where(logical_and(1/T<2,PGArx<500),1 - ((1/T)-1)*(PGArx - 100)/400,sl)
    sl = where(logical_and(1/T<2,PGArx>=500),1 - ((1/T)-1)+zeros(PGArx.shape),sl)

##    print sl
    c1 = c1_it_jp
    c1 = where(Zl == 1, c1_it_cas, c1)
    c1 = where(Zl == 0, c1_it, c1)

    #print c1,c2_it,c3_it,c4_it,c5_it,c6_it,c7_it
    #print M,h,R,sl,Sc,Sd,Se,g
    log_10_Y = c1 + c2_it*M + c3_it*h + c4_it*R - g*log10(R) + c5_it*sl*Sc + c6_it*sl*Sd + c7_it*sl*Se
##    print log_10_Y
    logSa = log(10**(log_10_Y)/981)
##    print logSa
    
    sigma_10 = sqrt(sig1**2+sig2**2)
    sigma = log(10**sigma_10)
    events_num = Df.shape[1]
    sigma = tile(sigma,(1,events_num,1))
##    print sigma_10
##
    return (logSa, sigma)

Atkinson_2003_intraslab_magnitude_type = 'Mw'
Atkinson_2003_intraslab_distance_type = 'Rupture'
##    
    # Interslab Events Coefficients

coef_it = array ([(0,0.0400000000000000,0.100000000000000,0.200000000000000,0.400000000000000,1,2,3.03030303030303),
(-0.0471300000000000,0.506970000000000,0.439280000000000,0.515890000000000,0.00544500000000000,-1.02133000000000,-2.39234000000000,-3.70012000000000),
(0.100000000000000,0.680000000000000,0.610000000000000,0.700000000000000,0.0700000000000000,-0.980000000000000,-2.44000000000000,-3.73000000000000),
(-0.250000000000000,0.230000000000000,0.160000000000000,0.400000000000000,-0.0100000000000000,-0.980000000000000,-2.25000000000000,-3.64000000000000),
(0.690900000000000,0.632730000000000,0.666750000000000,0.691860000000000,0.772700000000000,0.878900000000000,0.996400000000000,1.11690000000000),
(0.0113000000000000,0.0127500000000000,0.0108000000000000,0.00572000000000000,0.00173000000000000,0.00130000000000000,0.00364000000000000,0.00615000000000000),
(-0.00202000000000000,-0.00234000000000000,-0.00219000000000000,-0.00192000000000000,-0.00178000000000000,-0.00173000000000000,-0.00118000000000000,-0.000450000000000000),
(0.190000000000000,0.150000000000000,0.150000000000000,0.150000000000000,0.130000000000000,0.100000000000000,0.100000000000000,0.100000000000000),
(0.240000000000000,0.200000000000000,0.230000000000000,0.270000000000000,0.370000000000000,0.300000000000000,0.250000000000000,0.250000000000000),
(0.290000000000000,0.200000000000000,0.200000000000000,0.250000000000000,0.380000000000000,0.550000000000000,0.400000000000000,0.360000000000000),
(0.270000000000000,0.250000000000000,0.280000000000000,0.280000000000000,0.280000000000000,0.290000000000000,0.300000000000000,0.300000000000000),
(0.230000000000000,0.240000000000000,0.270000000000000,0.260000000000000,0.260000000000000,0.270000000000000,0.280000000000000,0.290000000000000),
(0.140000000000000,0.0700000000000000,0.0700000000000000,0.100000000000000,0.100000000000000,0.110000000000000,0.110000000000000,0.0800000000000000)])

Atkinson_2003_intraslab_coefficient = coef_it[1:10,:]
Atkinson_2003_intraslab_coefficient_period = coef_it[0]
Atkinson_2003_intraslab_sigma_coefficient = coef_it[11:13,:]
Atkinson_2003_intraslab_sigma_coefficient_period = coef_it[0]

Atkinson_2003_intraslab_PGA_coefficient = coef_it[1:10,0]

Atkinson_2003_intraslab_interpolation = linear_interpolation

Atkinson_2003_intraslab_uses_Vs30 = True

ground_motion_init['Atkinson_2003_intraslab'] = [Atkinson_2003_intraslab_distribution,
                              Atkinson_2003_intraslab_magnitude_type,
                              Atkinson_2003_intraslab_distance_type,

                              Atkinson_2003_intraslab_coefficient,
                              Atkinson_2003_intraslab_coefficient_period,
                              Atkinson_2003_intraslab_interpolation,
                          
                              Atkinson_2003_intraslab_sigma_coefficient,
                              Atkinson_2003_intraslab_sigma_coefficient_period,
                              Atkinson_2003_intraslab_interpolation,
                          
                              Atkinson_2003_intraslab_uses_Vs30]

    

########################  Start of Zhao et al model (Zhao_2006_intraslab)  ###########################
### Zhao model for slab events 
##
########
### The model function, from [1] .
########
##
##def Zhao_2006_intraslab_distribution(**kwargs): #T,M,h,Df,Zt,Vs30,Zl):
##
##    
##    # get args
##    T = kwargs['periods']
##    M = kwargs['mag']
##    x = kwargs['distance']
##    h = kwargs['depth']
##    Vs30 = kwargs['Vs30']
##    coefficient = kwargs['coefficient']
##    sigma_coefficient = kwargs['sigma_coefficient']
##
##    Vs30 = array(Vs30)
####    print shape(T)
####    print shape(M)
####    print shape(x)
####    print shape(h)
####    print shape(Vs30)
####    print shape(coefficient)
##    # unpack coefficients
##    (a,b,c,d,e,Ss,Ssl,CH,C1,C2,C3,C4,Pst,Qst,Wst) = coefficient
##    
##    (s_t,t_s) = sigma_coefficient
##
##    # Preliminary Computations
##    h = where (h>=125,125,h)
##
##    hc = zeros(shape(h))+15
##
##    delh = zeros(shape(h))
##
##    delh = where(h>=hc,1,delh)
##
##    Mc = zeros(shape(M))+6.5
##
##    lnS_MS = Pst*(M - Mc) + Qst*((M - Mc)**2) + Wst
####    print lnS_MS
##    SS = Ss
##    SSL = Ssl
##
##    CK = zeros(shape(C1))
##
##    CK = where(Vs30>=1100,CH,CK)
##    CK = where(logical_and(Vs30>600,Vs30<1100),C1,CK)
##    CK = where(logical_and(Vs30>300,Vs30<=600),C2,CK)
##    CK = where(logical_and(Vs30>=200,Vs30<=300),C3,CK)
##    CK = where(Vs30<=200,C4,CK)
####    print Vs30,CK
####    print type(Vs30)
##    r = x + c*exp(d*M)
##    
####    print r
##    lnY = a*M + b*x - log(r) + e*(h-hc)*delh + SS + SSL*log(x) + CK + lnS_MS #% Log Sa in cm/s^2
####    print lnY
##    sigma = sqrt(s_t**2 + t_s**2)
##
##    Sa = exp (lnY)/981 #% Median Sa in g
##    logSa = log(Sa)
####    print Sa
####    print shape(Sa)
####    print logSa.shape
##
##    events_num = x.shape[1]
##    sigma = tile(sigma,(1,events_num,1))
##
##
##
####    print 'Zhao.shape=%s' % str(logSa.shape)
####    print 'Zhao_sig.shape = %s' % str(sigma.shape)
##    return(logSa,sigma)
##
##Zhao_2006_intraslab_magnitude_type = 'Mw'
##Zhao_2006_intraslab_distance_type = 'Rupture'
##
####    
##    # Interslab Events Coefficients
##
##coef = array([(1.10100000000000,1.07600000000000,1.11800000000000,1.13400000000000,1.14700000000000,1.14900000000000,1.16300000000000,1.20000000000000,1.25000000000000,1.29300000000000,1.33600000000000,1.38600000000000,1.43300000000000,1.47900000000000,1.55100000000000,1.62100000000000,1.69400000000000,1.74800000000000,1.75900000000000,1.82600000000000,1.82500000000000),
##(-0.00564000000000000,-0.00671000000000000,-0.00787000000000000,-0.00722000000000000,-0.00659000000000000,-0.00590000000000000,-0.00520000000000000,-0.00422000000000000,-0.00338000000000000,-0.00282000000000000,-0.00258000000000000,-0.00242000000000000,-0.00232000000000000,-0.00220000000000000,-0.00207000000000000,-0.00224000000000000,-0.00201000000000000,-0.00187000000000000,-0.00147000000000000,-0.00195000000000000,-0.00237000000000000),
##(0.00550000000000000,0.00750000000000000,0.00900000000000000,0.0100000000000000,0.0120000000000000,0.0140000000000000,0.0150000000000000,0.0100000000000000,0.00600000000000000,0.00300000000000000,0.00250000000000000,0.00220000000000000,0.00200000000000000,0.00200000000000000,0.00200000000000000,0.00200000000000000,0.00250000000000000,0.00280000000000000,0.00320000000000000,0.00400000000000000,0.00500000000000000),
##(1.08000000000000,1.06000000000000,1.08300000000000,1.05300000000000,1.01400000000000,0.966000000000000,0.934000000000000,0.959000000000000,1.00800000000000,1.08800000000000,1.08400000000000,1.08800000000000,1.10900000000000,1.11500000000000,1.08300000000000,1.09100000000000,1.05500000000000,1.05200000000000,1.02500000000000,1.04400000000000,1.06500000000000),
##(0.0141200000000000,0.0146300000000000,0.0142300000000000,0.0150900000000000,0.0146200000000000,0.0145900000000000,0.0145800000000000,0.0125700000000000,0.0111400000000000,0.0101900000000000,0.00979000000000000,0.00944000000000000,0.00972000000000000,0.0100500000000000,0.0100300000000000,0.00928000000000000,0.00833000000000000,0.00776000000000000,0.00644000000000000,0.00590000000000000,0.00510000000000000),
##(2.60700000000000,2.76400000000000,2.15600000000000,2.16100000000000,1.90100000000000,1.81400000000000,2.18100000000000,2.43200000000000,2.62900000000000,2.70200000000000,2.65400000000000,2.48000000000000,2.33200000000000,2.23300000000000,2.02900000000000,1.58900000000000,0.966000000000000,0.789000000000000,1.03700000000000,0.561000000000000,0.225000000000000),
##(-0.528000000000000,-0.551000000000000,-0.420000000000000,-0.431000000000000,-0.372000000000000,-0.360000000000000,-0.450000000000000,-0.506000000000000,-0.554000000000000,-0.575000000000000,-0.572000000000000,-0.540000000000000,-0.522000000000000,-0.509000000000000,-0.469000000000000,-0.379000000000000,-0.248000000000000,-0.221000000000000,-0.263000000000000,-0.169000000000000,-0.120000000000000),
##(0.293000000000000,0.939000000000000,1.49900000000000,1.46200000000000,1.28000000000000,1.12100000000000,0.852000000000000,0.365000000000000,-0.207000000000000,-0.705000000000000,-1.14400000000000,-1.60900000000000,-2.02300000000000,-2.45100000000000,-3.24300000000000,-3.88800000000000,-4.78300000000000,-5.44400000000000,-5.83900000000000,-6.59800000000000,-6.75200000000000),
##(1.11100000000000,1.68400000000000,2.06100000000000,1.91600000000000,1.66900000000000,1.46800000000000,1.17200000000000,0.655000000000000,0.0710000000000000,-0.429000000000000,-0.866000000000000,-1.32500000000000,-1.73200000000000,-2.15200000000000,-2.92300000000000,-3.54800000000000,-4.41000000000000,-5.04900000000000,-5.43100000000000,-6.18100000000000,-6.34700000000000),
##(1.34400000000000,1.79300000000000,2.13500000000000,2.16800000000000,2.08500000000000,1.94200000000000,1.68300000000000,1.12700000000000,0.515000000000000,-0.00300000000000000,-0.449000000000000,-0.928000000000000,-1.34900000000000,-1.77600000000000,-2.54200000000000,-3.16900000000000,-4.03900000000000,-4.69800000000000,-5.08900000000000,-5.88200000000000,-6.05100000000000),
##(1.35500000000000,1.74700000000000,2.03100000000000,2.05200000000000,2.00100000000000,1.94100000000000,1.80800000000000,1.48200000000000,0.934000000000000,0.394000000000000,-0.111000000000000,-0.620000000000000,-1.06600000000000,-1.52300000000000,-2.32700000000000,-2.97900000000000,-3.87100000000000,-4.49600000000000,-4.89300000000000,-5.69800000000000,-5.87300000000000),
##(1.42000000000000,1.81400000000000,2.08200000000000,2.11300000000000,2.03000000000000,1.93700000000000,1.77000000000000,1.39700000000000,0.955000000000000,0.559000000000000,0.188000000000000,-0.246000000000000,-0.643000000000000,-1.08400000000000,-1.93600000000000,-2.66100000000000,-3.64000000000000,-4.34100000000000,-4.75800000000000,-5.58800000000000,-5.79800000000000),
##(0.139200000000000,0.163600000000000,0.169000000000000,0.166900000000000,0.163100000000000,0.158800000000000,0.154400000000000,0.146000000000000,0.138100000000000,0.130700000000000,0.123900000000000,0.117600000000000,0.111600000000000,0.106000000000000,0.0933000000000000,0.0821000000000000,0.0628000000000000,0.0465000000000000,0.0322000000000000,0.00830000000000000,-0.0117000000000000),
##(0.158400000000000,0.193200000000000,0.205700000000000,0.198400000000000,0.185600000000000,0.171400000000000,0.157300000000000,0.130900000000000,0.107800000000000,0.0878000000000000,0.0705000000000000,0.0556000000000000,0.0426000000000000,0.0314000000000000,0.00930000000000000,-0.00620000000000000,-0.0235000000000000,-0.0287000000000000,-0.0261000000000000,-0.00650000000000000,0.0246000000000000),
##(-0.0529000000000000,-0.0841000000000000,-0.0877000000000000,-0.0773000000000000,-0.0644000000000000,-0.0515000000000000,-0.0395000000000000,-0.0183000000000000,-0.000800000000000000,0.0136000000000000,0.0254000000000000,0.0352000000000000,0.0432000000000000,0.0498000000000000,0.0612000000000000,0.0674000000000000,0.0692000000000000,0.0622000000000000,0.0496000000000000,0.0150000000000000,-0.0268000000000000),
##(0.604000000000000,0.640000000000000,0.694000000000000,0.702000000000000,0.692000000000000,0.682000000000000,0.670000000000000,0.659000000000000,0.653000000000000,0.653000000000000,0.652000000000000,0.647000000000000,0.653000000000000,0.657000000000000,0.660000000000000,0.664000000000000,0.669000000000000,0.671000000000000,0.667000000000000,0.647000000000000,0.643000000000000),
##(0.321000000000000,0.378000000000000,0.420000000000000,0.372000000000000,0.324000000000000,0.294000000000000,0.284000000000000,0.278000000000000,0.272000000000000,0.285000000000000,0.290000000000000,0.299000000000000,0.289000000000000,0.286000000000000,0.277000000000000,0.282000000000000,0.300000000000000,0.292000000000000,0.274000000000000,0.281000000000000,0.296000000000000)])
##
##Zhao_2006_intraslab_coefficient = coef[0:15,:]
##Zhao_2006_intraslab_coefficient_period = array([0,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.25,1.5,2,2.5,3,4,5])
##Zhao_2006_intraslab_sigma_coefficient = coef[15:17,:]
##Zhao_2006_intraslab_sigma_coefficient_period = array([0,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.25,1.5,2,2.5,3,4,5])
##
##Zhao_2006_intraslab_interpolation = linear_interpolation
##
##Zhao_2006_intraslab_uses_Vs30 = True
##
##ground_motion_init['Zhao_2006_intraslab'] = [Zhao_2006_intraslab_distribution,
##                              Zhao_2006_intraslab_magnitude_type,
##                              Zhao_2006_intraslab_distance_type,
##
##                              Zhao_2006_intraslab_coefficient,
##                              Zhao_2006_intraslab_coefficient_period,
##                              Zhao_2006_intraslab_interpolation,
##                          
##                              Zhao_2006_intraslab_sigma_coefficient,
##                              Zhao_2006_intraslab_sigma_coefficient_period,
##                              Zhao_2006_intraslab_interpolation,
##                          
##                              Zhao_2006_intraslab_uses_Vs30]
    
########################  Start of Zhao et al model (Zhao_2006_interface)  ###########################
# Zhao model for Interface events 

######
# The model function, from [1] .
######

def Zhao_2006_interface_distribution(**kwargs): #T,M,h,Df,Zt,Vs30,Zl):

    
    # get args
    T = kwargs['periods']
    M = kwargs['mag']
    x = kwargs['distance']
    h = kwargs['depth']
    Vs30 = kwargs['Vs30']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

##    print shape(T)
##    print shape(M)
##    print shape(x)
##    print shape(h)
##    print shape(Vs30)
##    print shape(coefficient)
    # unpack coefficients
    (a,b,c,d,e,Si,CH,C1,C2,C3,C4,Qst,Wst) = coefficient
    
    (s_t,t_s) = sigma_coefficient

    # massage shapes
    Vs30 = array(Vs30) + zeros(CH.shape)

    # Preliminary Computations
    h = where (h>=125,125,h)

    hc = zeros(shape(h))+15

    delh = zeros(shape(h))

    delh = where(h>=hc,1,delh)

    Mc = zeros(shape(M))+6.3
    

    lnS_MS = Qst*((M - Mc)**2) + Wst
##    print lnS_MS
    SI = Si

    CK = zeros(shape(C1))

    CK = where(Vs30>=1100,CH,CK)
    CK = where(logical_and(Vs30>600,Vs30<1100),C1,CK)
    CK = where(logical_and(Vs30>300,Vs30<=600),C2,CK)
    CK = where(logical_and(Vs30>=200,Vs30<=300),C3,CK)
    CK = where(Vs30<=200,C4,CK)
##    print Vs30,CK
##    print type(Vs30)
    r = x + c*exp(d*M)
    
##    print r
    lnY = a*M + b*x - log(r) + e*(h-hc)*delh + SI + CK + lnS_MS #% Log Sa in cm/s^2
##    print lnY
    sigma = sqrt(s_t**2 + t_s**2)

    Sa = exp (lnY)/981 #% Median Sa in g
    logSa = log(Sa)
##    print Sa
##    print shape(Sa)
##    print logSa.shape

    events_num = x.shape[1]
    sigma = tile(sigma,(1,events_num,1))



##    print 'Zhao.shape=%s' % str(logSa.shape)
##    print 'Zhao_sig.shape = %s' % str(sigma.shape)
    return(logSa,sigma)

Zhao_2006_interface_magnitude_type = 'Mw'
Zhao_2006_interface_distance_type = 'Rupture'

##    
    # Interface Events Coefficients

coef =array([(1.10100000000000,1.07600000000000,1.11800000000000,1.13400000000000,1.14700000000000,1.14900000000000,1.16300000000000,1.20000000000000,1.25000000000000,1.29300000000000,1.33600000000000,1.38600000000000,1.43300000000000,1.47900000000000,1.55100000000000,1.62100000000000,1.69400000000000,1.74800000000000,1.75900000000000,1.82600000000000,1.82500000000000),
(-0.00564000000000000,-0.00671000000000000,-0.00787000000000000,-0.00722000000000000,-0.00659000000000000,-0.00590000000000000,-0.00520000000000000,-0.00422000000000000,-0.00338000000000000,-0.00282000000000000,-0.00258000000000000,-0.00242000000000000,-0.00232000000000000,-0.00220000000000000,-0.00207000000000000,-0.00224000000000000,-0.00201000000000000,-0.00187000000000000,-0.00147000000000000,-0.00195000000000000,-0.00237000000000000),
(0.00550000000000000,0.00750000000000000,0.00900000000000000,0.0100000000000000,0.0120000000000000,0.0140000000000000,0.0150000000000000,0.0100000000000000,0.00600000000000000,0.00300000000000000,0.00250000000000000,0.00220000000000000,0.00200000000000000,0.00200000000000000,0.00200000000000000,0.00200000000000000,0.00250000000000000,0.00280000000000000,0.00320000000000000,0.00400000000000000,0.00500000000000000),
(1.08000000000000,1.06000000000000,1.08300000000000,1.05300000000000,1.01400000000000,0.966000000000000,0.934000000000000,0.959000000000000,1.00800000000000,1.08800000000000,1.08400000000000,1.08800000000000,1.10900000000000,1.11500000000000,1.08300000000000,1.09100000000000,1.05500000000000,1.05200000000000,1.02500000000000,1.04400000000000,1.06500000000000),
(0.0141200000000000,0.0146300000000000,0.0142300000000000,0.0150900000000000,0.0146200000000000,0.0145900000000000,0.0145800000000000,0.0125700000000000,0.0111400000000000,0.0101900000000000,0.00979000000000000,0.00944000000000000,0.00972000000000000,0.0100500000000000,0.0100300000000000,0.00928000000000000,0.00833000000000000,0.00776000000000000,0.00644000000000000,0.00590000000000000,0.00510000000000000),
(0,0,0,0,0,0,0,-0.0410000000000000,-0.0530000000000000,-0.103000000000000,-0.146000000000000,-0.164000000000000,-0.206000000000000,-0.239000000000000,-0.256000000000000,-0.306000000000000,-0.321000000000000,-0.337000000000000,-0.331000000000000,-0.390000000000000,-0.498000000000000),
(0.293000000000000,0.939000000000000,1.49900000000000,1.46200000000000,1.28000000000000,1.12100000000000,0.852000000000000,0.365000000000000,-0.207000000000000,-0.705000000000000,-1.14400000000000,-1.60900000000000,-2.02300000000000,-2.45100000000000,-3.24300000000000,-3.88800000000000,-4.78300000000000,-5.44400000000000,-5.83900000000000,-6.59800000000000,-6.75200000000000),
(1.11100000000000,1.68400000000000,2.06100000000000,1.91600000000000,1.66900000000000,1.46800000000000,1.17200000000000,0.655000000000000,0.0710000000000000,-0.429000000000000,-0.866000000000000,-1.32500000000000,-1.73200000000000,-2.15200000000000,-2.92300000000000,-3.54800000000000,-4.41000000000000,-5.04900000000000,-5.43100000000000,-6.18100000000000,-6.34700000000000),
(1.34400000000000,1.79300000000000,2.13500000000000,2.16800000000000,2.08500000000000,1.94200000000000,1.68300000000000,1.12700000000000,0.515000000000000,-0.00300000000000000,-0.449000000000000,-0.928000000000000,-1.34900000000000,-1.77600000000000,-2.54200000000000,-3.16900000000000,-4.03900000000000,-4.69800000000000,-5.08900000000000,-5.88200000000000,-6.05100000000000),
(1.35500000000000,1.74700000000000,2.03100000000000,2.05200000000000,2.00100000000000,1.94100000000000,1.80800000000000,1.48200000000000,0.934000000000000,0.394000000000000,-0.111000000000000,-0.620000000000000,-1.06600000000000,-1.52300000000000,-2.32700000000000,-2.97900000000000,-3.87100000000000,-4.49600000000000,-4.89300000000000,-5.69800000000000,-5.87300000000000),
(1.42000000000000,1.81400000000000,2.08200000000000,2.11300000000000,2.03000000000000,1.93700000000000,1.77000000000000,1.39700000000000,0.955000000000000,0.559000000000000,0.188000000000000,-0.246000000000000,-0.643000000000000,-1.08400000000000,-1.93600000000000,-2.66100000000000,-3.64000000000000,-4.34100000000000,-4.75800000000000,-5.58800000000000,-5.79800000000000),
(0,0,0,-0.0138000000000000,-0.0256000000000000,-0.0348000000000000,-0.0423000000000000,-0.0541000000000000,-0.0632000000000000,-0.0707000000000000,-0.0771000000000000,-0.0825000000000000,-0.0874000000000000,-0.0917000000000000,-0.100900000000000,-0.108300000000000,-0.120200000000000,-0.129300000000000,-0.136800000000000,-0.148600000000000,-0.157800000000000),
(0,0,0,0.0286000000000000,0.0352000000000000,0.0403000000000000,0.0445000000000000,0.0511000000000000,0.0562000000000000,0.0604000000000000,0.0639000000000000,0.0670000000000000,0.0697000000000000,0.0721000000000000,0.0772000000000000,0.0814000000000000,0.0880000000000000,0.0931000000000000,0.0972000000000000,0.103800000000000,0.109000000000000),
(0.604000000000000,0.640000000000000,0.694000000000000,0.702000000000000,0.692000000000000,0.682000000000000,0.670000000000000,0.659000000000000,0.653000000000000,0.653000000000000,0.652000000000000,0.647000000000000,0.653000000000000,0.657000000000000,0.660000000000000,0.664000000000000,0.669000000000000,0.671000000000000,0.667000000000000,0.647000000000000,0.643000000000000),
(0.308000000000000,0.343000000000000,0.403000000000000,0.367000000000000,0.328000000000000,0.289000000000000,0.280000000000000,0.271000000000000,0.277000000000000,0.296000000000000,0.313000000000000,0.329000000000000,0.324000000000000,0.328000000000000,0.339000000000000,0.352000000000000,0.360000000000000,0.356000000000000,0.338000000000000,0.307000000000000,0.272000000000000)])


Zhao_2006_interface_coefficient = coef[0:13,:]
Zhao_2006_interface_coefficient_period = array([0,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.25,1.5,2,2.5,3,4,5])
Zhao_2006_interface_sigma_coefficient = coef[13:17,:]
Zhao_2006_interface_sigma_coefficient_period = array([0,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.25,1.5,2,2.5,3,4,5])

Zhao_2006_interface_interpolation = linear_interpolation

Zhao_2006_interface_uses_Vs30 = True

ground_motion_init['Zhao_2006_interface'] = [Zhao_2006_interface_distribution,
                              Zhao_2006_interface_magnitude_type,
                              Zhao_2006_interface_distance_type,

                              Zhao_2006_interface_coefficient,
                              Zhao_2006_interface_coefficient_period,
                              Zhao_2006_interface_interpolation,
                          
                              Zhao_2006_interface_sigma_coefficient,
                              Zhao_2006_interface_sigma_coefficient_period,
                              Zhao_2006_interface_interpolation,
                          
                              Zhao_2006_interface_uses_Vs30]
    


########################  Start of Atkinson_Boore_interface model (Atkinson_2003_interface)  ###########################
# Atkinson_Boore model for interface events (Zt = 0)

######
# The model function, from [1] .
######

def Atkinson_2003_interface_distribution(**kwargs): #T,M,h,Df,Zt,Vs30,Zl):

    
    # get args
    T = kwargs['periods']
    M = kwargs['mag']				# event-specific
    h = kwargs['depth']
    Df = kwargs['distance']			# event-site-specific
    Vs30 = kwargs['Vs30']
##    Zl = kwargs['region']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
#    coefficient_PGA = kwargs['coefficient_PGA']

    T = T[newaxis,newaxis,:]

    # unpack coefficients
    (c1_it,c1_it_jp,c1_it_cas,c2_it,c3_it,c4_it,c5_it,c6_it,c7_it) = coefficient
    (c10_it,c10_it_jp,c10_it_cas,c20_it,c30_it,c40_it,c50_it,c60_it,c70_it) = Atkinson_2003_interface_PGA_coefficient
##    (sigma_it) = sigma_coefficient
    (sig1,sig2) = sigma_coefficient

     # Model estimation

    h = where (h>=100,100,h)   



    M = where(M >= 8.5, 8.5, M)
    
    delta = 0.00724*(10**(0.507*M))
    R = sqrt(Df**2 + delta**2)


    g = 10**(1.2 - 0.18*M)
           

    Sc = zeros(shape(Vs30))
    Sd = zeros(shape(Vs30))
    Se = zeros(shape(Vs30))
    Ze = zeros(shape(Vs30))
    
    Sc = where(Vs30<180,0,Ze)
    Sd = where(Vs30<180,0,Ze)
    Se = where(Vs30<180,1,Ze)
    
    Sc = where(Vs30>=180,0,Sc)
    Sd = where(Vs30>=180,1,Sd)
    Se = where(Vs30>=180,0,Se)
    
    Sc = where(Vs30>360,1,Sc)
    Sd = where(Vs30>360,0,Sd)
    Se = where(Vs30>360,0,Se)
    
    Sc = where(Vs30>760,0,Sc)
    Sd = where(Vs30>760,0,Sd)
    Se = where(Vs30>760,0,Se)

##    print Vs30,Sc, Sd, Se
    Zl = zeros(c1_it_jp.shape)
    c10 = c10_it_jp
    c10 = where(Zl == 1, c10_it_cas, c10)
    c10 = where(Zl == 0, c10_it, c10)
    
    log_PGArx = c10 + c20_it*M + c30_it*h + c40_it*R - g*log10(R)
    PGArx = 10**(log_PGArx) + zeros(T.shape)

##    print PGArx
    T = where(T==0,.00000000000001,T)
    sl = zeros(PGArx.shape)
    sl = where(logical_and(1/T>=2,PGArx<500),1 - (PGArx - 100)/400,sl)
    sl = where(logical_and(1/T<2,PGArx<500),1 - ((1/T)-1)*(PGArx - 100)/400,sl)
    sl = where(logical_and(1/T<2,PGArx>=500),1 - ((1/T)-1)+zeros(PGArx.shape),sl)

##    print sl
    c1 = c1_it_jp
    c1 = where(Zl == 1, c1_it_cas, c1)
    c1 = where(Zl == 0, c1_it, c1)

    #print c1,c2_it,c3_it,c4_it,c5_it,c6_it,c7_it
    #print M,h,R,sl,Sc,Sd,Se,g
    log_10_Y = c1 + c2_it*M + c3_it*h + c4_it*R - g*log10(R) + c5_it*sl*Sc + c6_it*sl*Sd + c7_it*sl*Se
##    print log_10_Y
    logSa = log(10**(log_10_Y)/981)
##    print logSa
    
    sigma_10 = sqrt(sig1**2+sig2**2)
    sigma = log(10**sigma_10)
    events_num = Df.shape[1]
    sigma = tile(sigma,(1,events_num,1))
##    print sigma_10
##
    return (logSa, sigma)

Atkinson_2003_interface_magnitude_type = 'Mw'
Atkinson_2003_interface_distance_type = 'Rupture'
##    
    # Interslab Events Coefficients

coef_it = array([(0,0.0400000000000000,0.100000000000000,0.200000000000000,0.400000000000000,1,2,3.03030303030303),
    (2.99100000000000,2.87530000000000,2.77890000000000,2.66380000000000,2.52490000000000,2.14420000000000,2.19070000000000,2.30100000000000),
    (3.14000000000000,3.05000000000000,2.95000000000000,2.84000000000000,2.58000000000000,2.18000000000000,2.14000000000000,2.27000000000000),
    (2.79000000000000,2.60000000000000,2.50000000000000,2.54000000000000,2.50000000000000,2.18000000000000,2.33000000000000,2.36000000000000),
    (0.0352500000000000,0.0705200000000000,0.0984100000000000,0.123860000000000,0.147700000000000,0.134500000000000,0.0714800000000000,0.0223700000000000),
    (0.00759000000000000,0.0100400000000000,0.00974000000000000,0.00884000000000000,0.00728000000000000,0.00521000000000000,0.00224000000000000,0.000120000000000000),
    (-0.00206000000000000,-0.00278000000000000,-0.00287000000000000,-0.00280000000000000,-0.00235000000000000,-0.00110000000000000,0,0),
    (0.190000000000000,0.150000000000000,0.150000000000000,0.150000000000000,0.130000000000000,0.100000000000000,0.100000000000000,0.100000000000000),
    (0.240000000000000,0.200000000000000,0.230000000000000,0.270000000000000,0.370000000000000,0.300000000000000,0.250000000000000,0.250000000000000),
    (0.290000000000000,0.200000000000000,0.200000000000000,0.250000000000000,0.380000000000000,0.550000000000000,0.400000000000000,0.360000000000000),
    (0.230000000000000,0.260000000000000,0.270000000000000,0.280000000000000,0.290000000000000,0.340000000000000,0.340000000000000,0.360000000000000),
    (0.200000000000000,0.220000000000000,0.250000000000000,0.250000000000000,0.250000000000000,0.280000000000000,0.290000000000000,0.310000000000000),
    (0.110000000000000,0.140000000000000,0.100000000000000,0.130000000000000,0.150000000000000,0.190000000000000,0.180000000000000,0.180000000000000)])
Atkinson_2003_interface_coefficient = coef_it[1:10,:]
Atkinson_2003_interface_coefficient_period = coef_it[0]
Atkinson_2003_interface_sigma_coefficient = coef_it[11:13,:]
Atkinson_2003_interface_sigma_coefficient_period = coef_it[0]

Atkinson_2003_interface_PGA_coefficient = coef_it[1:10,0]

Atkinson_2003_interface_interpolation = linear_interpolation

Atkinson_2003_interface_uses_Vs30 = True

ground_motion_init['Atkinson_2003_interface'] = [Atkinson_2003_interface_distribution,
                              Atkinson_2003_interface_magnitude_type,
                              Atkinson_2003_interface_distance_type,

                              Atkinson_2003_interface_coefficient,
                              Atkinson_2003_interface_coefficient_period,
                              Atkinson_2003_interface_interpolation,
                          
                              Atkinson_2003_interface_sigma_coefficient,
                              Atkinson_2003_interface_sigma_coefficient_period,
                              Atkinson_2003_interface_interpolation,
                          
                              Atkinson_2003_interface_uses_Vs30]
   
    
########################  Start of Zhao et al model (Zhao_2006_intraslab)  ###########################
# Zhao model for slab events (Zt = 0)

######
# The model function, from [1] page 1021.
######

def Zhao_2006_intraslab_distribution(**kwargs): #T,M,h,Df,Zt,Vs30,Zl):

    
    # get args
    T = kwargs['periods']
    M = kwargs['mag']
    x = kwargs['distance']
    h = kwargs['depth']
    Vs30 = kwargs['Vs30']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

##    print shape(T)
##    print shape(M)
##    print shape(x)
##    print shape(h)
##    print shape(Vs30)
##    print shape(coefficient)
    # unpack coefficients
    (a,b,c,d,e,Ss,Ssl,CH,C1,C2,C3,C4,Pst,Qst,Wst) = coefficient
    
    (s_t,t_s) = sigma_coefficient

    # massage Vs30 shape
    Vs30 = array(Vs30) + zeros(CH.shape)

    # Preliminary Computations
    h = where (h>=125,125,h)

    hc = zeros(shape(h))+15

    delh = zeros(shape(h))

    delh = where(h>=hc,1,delh)

    Mc = zeros(shape(M))+6.5

    lnS_MS = Pst*(M - Mc) + Qst*((M - Mc)**2) + Wst
##    print lnS_MS
    SS = Ss
    SSL = Ssl

    CK = zeros(shape(C1))

    CK = where(Vs30>=1100,CH,CK)
    CK = where(logical_and(Vs30>600,Vs30<1100),C1,CK)
    CK = where(logical_and(Vs30>300,Vs30<=600),C2,CK)
    CK = where(logical_and(Vs30>=200,Vs30<=300),C3,CK)
    CK = where(Vs30<=200,C4,CK)
##    print Vs30,CK
##    print type(Vs30)
    r = x + c*exp(d*M)
    
##    print r
    lnY = a*M + b*x - log(r) + e*(h-hc)*delh + SS + SSL*log(x) + CK + lnS_MS #% Log Sa in cm/s^2
##    print lnY
    sigma = sqrt(s_t**2 + t_s**2)

    Sa = exp (lnY)/981 #% Median Sa in g
    logSa = log(Sa)
##    print Sa
##    print shape(Sa)
##    print logSa.shape

    events_num = x.shape[1]
    sigma = tile(sigma,(1,events_num,1))



##    print 'Zhao.shape=%s' % str(logSa.shape)
##    print 'Zhao_sig.shape = %s' % str(sigma.shape)
    return(logSa,sigma)

Zhao_2006_intraslab_magnitude_type = 'Mw'
Zhao_2006_intraslab_distance_type = 'Rupture'

##    
    # Interslab Events Coefficients

coef = array([(1.10100000000000,1.07600000000000,1.11800000000000,1.13400000000000,1.14700000000000,1.14900000000000,1.16300000000000,1.20000000000000,1.25000000000000,1.29300000000000,1.33600000000000,1.38600000000000,1.43300000000000,1.47900000000000,1.55100000000000,1.62100000000000,1.69400000000000,1.74800000000000,1.75900000000000,1.82600000000000,1.82500000000000),
(-0.00564000000000000,-0.00671000000000000,-0.00787000000000000,-0.00722000000000000,-0.00659000000000000,-0.00590000000000000,-0.00520000000000000,-0.00422000000000000,-0.00338000000000000,-0.00282000000000000,-0.00258000000000000,-0.00242000000000000,-0.00232000000000000,-0.00220000000000000,-0.00207000000000000,-0.00224000000000000,-0.00201000000000000,-0.00187000000000000,-0.00147000000000000,-0.00195000000000000,-0.00237000000000000),
(0.00550000000000000,0.00750000000000000,0.00900000000000000,0.0100000000000000,0.0120000000000000,0.0140000000000000,0.0150000000000000,0.0100000000000000,0.00600000000000000,0.00300000000000000,0.00250000000000000,0.00220000000000000,0.00200000000000000,0.00200000000000000,0.00200000000000000,0.00200000000000000,0.00250000000000000,0.00280000000000000,0.00320000000000000,0.00400000000000000,0.00500000000000000),
(1.08000000000000,1.06000000000000,1.08300000000000,1.05300000000000,1.01400000000000,0.966000000000000,0.934000000000000,0.959000000000000,1.00800000000000,1.08800000000000,1.08400000000000,1.08800000000000,1.10900000000000,1.11500000000000,1.08300000000000,1.09100000000000,1.05500000000000,1.05200000000000,1.02500000000000,1.04400000000000,1.06500000000000),
(0.0141200000000000,0.0146300000000000,0.0142300000000000,0.0150900000000000,0.0146200000000000,0.0145900000000000,0.0145800000000000,0.0125700000000000,0.0111400000000000,0.0101900000000000,0.00979000000000000,0.00944000000000000,0.00972000000000000,0.0100500000000000,0.0100300000000000,0.00928000000000000,0.00833000000000000,0.00776000000000000,0.00644000000000000,0.00590000000000000,0.00510000000000000),
(2.60700000000000,2.76400000000000,2.15600000000000,2.16100000000000,1.90100000000000,1.81400000000000,2.18100000000000,2.43200000000000,2.62900000000000,2.70200000000000,2.65400000000000,2.48000000000000,2.33200000000000,2.23300000000000,2.02900000000000,1.58900000000000,0.966000000000000,0.789000000000000,1.03700000000000,0.561000000000000,0.225000000000000),
(-0.528000000000000,-0.551000000000000,-0.420000000000000,-0.431000000000000,-0.372000000000000,-0.360000000000000,-0.450000000000000,-0.506000000000000,-0.554000000000000,-0.575000000000000,-0.572000000000000,-0.540000000000000,-0.522000000000000,-0.509000000000000,-0.469000000000000,-0.379000000000000,-0.248000000000000,-0.221000000000000,-0.263000000000000,-0.169000000000000,-0.120000000000000),
(0.293000000000000,0.939000000000000,1.49900000000000,1.46200000000000,1.28000000000000,1.12100000000000,0.852000000000000,0.365000000000000,-0.207000000000000,-0.705000000000000,-1.14400000000000,-1.60900000000000,-2.02300000000000,-2.45100000000000,-3.24300000000000,-3.88800000000000,-4.78300000000000,-5.44400000000000,-5.83900000000000,-6.59800000000000,-6.75200000000000),
(1.11100000000000,1.68400000000000,2.06100000000000,1.91600000000000,1.66900000000000,1.46800000000000,1.17200000000000,0.655000000000000,0.0710000000000000,-0.429000000000000,-0.866000000000000,-1.32500000000000,-1.73200000000000,-2.15200000000000,-2.92300000000000,-3.54800000000000,-4.41000000000000,-5.04900000000000,-5.43100000000000,-6.18100000000000,-6.34700000000000),
(1.34400000000000,1.79300000000000,2.13500000000000,2.16800000000000,2.08500000000000,1.94200000000000,1.68300000000000,1.12700000000000,0.515000000000000,-0.00300000000000000,-0.449000000000000,-0.928000000000000,-1.34900000000000,-1.77600000000000,-2.54200000000000,-3.16900000000000,-4.03900000000000,-4.69800000000000,-5.08900000000000,-5.88200000000000,-6.05100000000000),
(1.35500000000000,1.74700000000000,2.03100000000000,2.05200000000000,2.00100000000000,1.94100000000000,1.80800000000000,1.48200000000000,0.934000000000000,0.394000000000000,-0.111000000000000,-0.620000000000000,-1.06600000000000,-1.52300000000000,-2.32700000000000,-2.97900000000000,-3.87100000000000,-4.49600000000000,-4.89300000000000,-5.69800000000000,-5.87300000000000),
(1.42000000000000,1.81400000000000,2.08200000000000,2.11300000000000,2.03000000000000,1.93700000000000,1.77000000000000,1.39700000000000,0.955000000000000,0.559000000000000,0.188000000000000,-0.246000000000000,-0.643000000000000,-1.08400000000000,-1.93600000000000,-2.66100000000000,-3.64000000000000,-4.34100000000000,-4.75800000000000,-5.58800000000000,-5.79800000000000),
(0.139200000000000,0.163600000000000,0.169000000000000,0.166900000000000,0.163100000000000,0.158800000000000,0.154400000000000,0.146000000000000,0.138100000000000,0.130700000000000,0.123900000000000,0.117600000000000,0.111600000000000,0.106000000000000,0.0933000000000000,0.0821000000000000,0.0628000000000000,0.0465000000000000,0.0322000000000000,0.00830000000000000,-0.0117000000000000),
(0.158400000000000,0.193200000000000,0.205700000000000,0.198400000000000,0.185600000000000,0.171400000000000,0.157300000000000,0.130900000000000,0.107800000000000,0.0878000000000000,0.0705000000000000,0.0556000000000000,0.0426000000000000,0.0314000000000000,0.00930000000000000,-0.00620000000000000,-0.0235000000000000,-0.0287000000000000,-0.0261000000000000,-0.00650000000000000,0.0246000000000000),
(-0.0529000000000000,-0.0841000000000000,-0.0877000000000000,-0.0773000000000000,-0.0644000000000000,-0.0515000000000000,-0.0395000000000000,-0.0183000000000000,-0.000800000000000000,0.0136000000000000,0.0254000000000000,0.0352000000000000,0.0432000000000000,0.0498000000000000,0.0612000000000000,0.0674000000000000,0.0692000000000000,0.0622000000000000,0.0496000000000000,0.0150000000000000,-0.0268000000000000),
(0.604000000000000,0.640000000000000,0.694000000000000,0.702000000000000,0.692000000000000,0.682000000000000,0.670000000000000,0.659000000000000,0.653000000000000,0.653000000000000,0.652000000000000,0.647000000000000,0.653000000000000,0.657000000000000,0.660000000000000,0.664000000000000,0.669000000000000,0.671000000000000,0.667000000000000,0.647000000000000,0.643000000000000),
(0.321000000000000,0.378000000000000,0.420000000000000,0.372000000000000,0.324000000000000,0.294000000000000,0.284000000000000,0.278000000000000,0.272000000000000,0.285000000000000,0.290000000000000,0.299000000000000,0.289000000000000,0.286000000000000,0.277000000000000,0.282000000000000,0.300000000000000,0.292000000000000,0.274000000000000,0.281000000000000,0.296000000000000)])

Zhao_2006_intraslab_coefficient = coef[0:15,:]
Zhao_2006_intraslab_coefficient_period = array([0,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.25,1.5,2,2.5,3,4,5])
Zhao_2006_intraslab_sigma_coefficient = coef[15:17,:]
Zhao_2006_intraslab_sigma_coefficient_period = array([0,0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.25,1.5,2,2.5,3,4,5])

Zhao_2006_intraslab_interpolation = linear_interpolation

Zhao_2006_intraslab_uses_Vs30 = True

ground_motion_init['Zhao_2006_intraslab'] = [Zhao_2006_intraslab_distribution,
                              Zhao_2006_intraslab_magnitude_type,
                              Zhao_2006_intraslab_distance_type,

                              Zhao_2006_intraslab_coefficient,
                              Zhao_2006_intraslab_coefficient_period,
                              Zhao_2006_intraslab_interpolation,
                          
                              Zhao_2006_intraslab_sigma_coefficient,
                              Zhao_2006_intraslab_sigma_coefficient_period,
                              Zhao_2006_intraslab_interpolation,
                          
                              Zhao_2006_intraslab_uses_Vs30]
    


#########

Abrahamson_Silva_1997_coefficient_period = [5, 4, 3, 2, 1.5, 1, 0.85, 0.75, 0.6, 0.5, 0.46, 0.4, 0.36,
                                            0.3, 0.24, 0.2, 0.17, 0.15, 0.12, 0.1,
                                            0.09, 0.075, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01]

Abrahamson_Silva_1997_coefficient = asarray([
        # c4, a1, a2, a3, a4, a5, a6, a9, a10, a11, a12, a13, c1, c5, n
        [3.5, -1.46, 0.512, -0.725, -0.144, 0.4, -0.2, 0, 0.664, 0.04, -0.215, 0.17, 6.4, 0.03, 2], 
        [3.5, -1.13, 0.512, -0.725, -0.144, 0.4, -0.2, 0.039, 0.64, 0.04, -0.1956, 0.17, 6.4, 0.03, 2], 
        [3.5, -0.69, 0.512, -0.725, -0.144, 0.4, -0.156, 0.089, 0.63, 0.04, -0.1726, 0.17, 6.4, 0.03, 2], 
        [3.5, -0.15, 0.512, -0.725, -0.144, 0.4, -0.094, 0.16, 0.61, 0.04, -0.14, 0.17, 6.4, 0.03, 2], 
        [3.55, 0.26, 0.512, -0.7721, -0.144, 0.438, -0.049, 0.21, 0.6, 0.04, -0.12, 0.17, 6.4, 0.03, 2], 
        [3.7, 0.828, 0.512, -0.8383, -0.144, 0.49, 0.013, 0.281, 0.423, 0, -0.102, 0.17, 6.4, 0.03, 2], 
        [3.81, 1.02, 0.512, -0.8648, -0.144, 0.512, 0.038, 0.309, 0.37, -0.028, -0.0927, 0.17, 6.4, 0.03, 2], 
        [3.9, 1.16, 0.512, -0.8852, -0.144, 0.528, 0.057, 0.331, 0.32, -0.05, -0.0862, 0.17, 6.4, 0.03, 2], 
        [4.12, 1.428, 0.512, -0.9218, -0.144, 0.557, 0.091, 0.37, 0.194, -0.089, -0.074, 0.17, 6.4, 0.03, 2], 
        [4.3, 1.615, 0.512, -0.9515, -0.144, 0.581, 0.119, 0.37, 0.085, -0.121, -0.0635, 0.17, 6.4, 0.03, 2], 
        [4.38, 1.717, 0.512, -0.9652, -0.144, 0.592, 0.132, 0.37, 0.02, -0.136, -0.0594, 0.17, 6.4, 0.03, 2], 
        [4.52, 1.86, 0.512, -0.988, -0.144, 0.61, 0.154, 0.37, -0.065, -0.16, -0.0518, 0.17, 6.4, 0.03, 2], 
        [4.62, 1.955, 0.512, -1.0052, -0.144, 0.61, 0.17, 0.37, -0.123, -0.173, -0.046, 0.17, 6.4, 0.03, 2], 
        [4.8, 2.114, 0.512, -1.035, -0.144, 0.61, 0.198, 0.37, -0.219, -0.195, -0.036, 0.17, 6.4, 0.03, 2], 
        [4.97, 2.293, 0.512, -1.079, -0.144, 0.61, 0.232, 0.37, -0.35, -0.223, -0.0238, 0.17, 6.4, 0.03, 2], 
        [5.1, 2.406, 0.512, -1.115, -0.144, 0.61, 0.26, 0.37, -0.445, -0.245, -0.0138, 0.17, 6.4, 0.03, 2], 
        [5.19, 2.43, 0.512, -1.135, -0.144, 0.61, 0.26, 0.37, -0.522, -0.265, -0.004, 0.17, 6.4, 0.03, 2], 
        [5.27, 2.407, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.577, -0.28, 0.005, 0.17, 6.4, 0.03, 2], 
        [5.39, 2.272, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.591, -0.28, 0.018, 0.17, 6.4, 0.03, 2], 
        [5.5, 2.16, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.598, -0.28, 0.028, 0.17, 6.4, 0.03, 2], 
        [5.54, 2.1, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.609, -0.28, 0.03, 0.17, 6.4, 0.03, 2], 
        [5.58, 2.037, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.628, -0.28, 0.03, 0.17, 6.4, 0.03, 2], 
        [5.6, 1.94, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.665, -0.28, 0.03, 0.17, 6.4, 0.03, 2], 
        [5.6, 1.87, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.62, -0.267, 0.028, 0.17, 6.4, 0.03, 2], 
        [5.6, 1.78, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.555, -0.251, 0.0245, 0.17, 6.4, 0.03, 2], 
        [5.6, 1.69, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.47, -0.23, 0.0143, 0.17, 6.4, 0.03, 2], 
        [5.6, 1.64, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.417, -0.23, 0, 0.17, 6.4, 0.03, 2], 
        [5.6, 1.64, 0.512, -1.145, -0.144, 0.61, 0.26, 0.37, -0.417, -0.23, 0, 0.17, 6.4, 0.03, 2]
        ]).T

Abrahamson_Silva_1997_sigma_coefficient = asarray([
        # b5, b6
        [0.89, 0.087], 
        [0.88, 0.092], 
        [0.87, 0.097], 
        [0.85, 0.105], 
        [0.84, 0.11], 
        [0.83, 0.118], 
        [0.82, 0.121], 
        [0.81, 0.123], 
        [0.81, 0.127], 
        [0.8, 0.13], 
        [0.8, 0.132], 
        [0.79, 0.135], 
        [0.79, 0.135], 
        [0.78, 0.135], 
        [0.77, 0.135], 
        [0.77, 0.135], 
        [0.76, 0.135], 
        [0.75, 0.135], 
        [0.75, 0.135], 
        [0.74, 0.135], 
        [0.74, 0.135], 
        [0.73, 0.135], 
        [0.72, 0.135], 
        [0.71, 0.135], 
        [0.71, 0.135], 
        [0.7, 0.135], 
        [0.7, 0.135], 
        [0.7, 0.135]]).T



Abrahamson_Silva_1997_uses_Vs30=True
Abrahamson_Silva_1997_magnitude_type = 'Mw'
Abrahamson_Silva_1997_distance_type = 'Rupture'


def Abrahamson_Silva_1997_distribution(dist_object,
                                       mag,
                                       coefficient,
                                       sigma_coefficient,
                                       depth_to_top,
                                       fault_type, Vs30,
                                       dip, width,
                                       periods,
                                       depth=None,
                                       distance=None,
                                       Z25=None,
                                       Fhw=0, # FIXME Fhw is only ever passed in from test suite
                                       **kwargs):
    """
    Abrahamson and Silva (1997, Seismological Research Letters, vol 68, num 1, pp 94-127)
    Adapted from OpenSHA Java implementation.
    """
    assert len(periods) == coefficient.shape[3]
    assert len(periods) == sigma_coefficient.shape[3]
    
    # According to Trevor Allen, Vs30 > 360 indicates rock or shallow soil
    deep_soil = where(Vs30[:, newaxis, newaxis] > 360, 0, 1)
    
    c4, a1, a2, a3, a4, a5, a6, a9, a10, a11, a12, a13, c1, c5, n = coefficient
    b5, b6 = sigma_coefficient
    # c4 .. n, b5, b6 shape is [1, 1, periods]

    F_map = zeros(max(ground_motion_misc.FaultTypeDictionary.values()) + 1)
    F_map[[ground_motion_misc.FaultTypeDictionary[t] for t in
           ('reverse', 'normal', 'strike_slip')]] = (1.0, 0.0, 0.5)
    F = F_map[fault_type] # [sites, events, 1]

    # FIXME This use of where() everywhere is unfortunate, but might
    # be the only way of doing all this conditional arithmetic in
    # numpy. numpy.piecewise() is the closest thing to true conditional
    # evaluation of functions in numpy, but it doesn't pass the
    # element index info to the functions it calls - all they ever see
    # is a 1D array regardless of the shape of the input - so isn't
    # generally usable here. The "where()" approach leads to a lot of
    # arithmetic that is simply thrown away. Once again, numpy is the
    # wrong tool for this job.
    
    f3 = where(mag <= 5.8, a5, a6) #  [sites, events, peiods]
    f3 = where(logical_and(mag > 5.8,  mag < c1),
               # Note: the 1997 paper has this as just (a5 + (a6 - a5)
               # * / (c1 - 5.8)), but the OpenSHA java version has the
               # (mag-5.8) term which looks right as this makes the
               # function continuous.
               a5 + (a6 - a5) * (mag - 5.8) / (c1 - 5.8),
               f3)

    fHWM = (mag - 5.5).clip(0.0, 1.0)
    Rrup = dist_object.Rupture[:,:,newaxis] # [sites, events, 1] 
    fHWRrup = zeros(Rrup.shape[0:2] + (len(periods),)) # [sites, events, periods]
    fHWRrup = where(logical_and(Rrup > 4,  Rrup <= 8),
                    a9 * (Rrup - 4.0) / 4.0,
                    fHWRrup)
    fHWRrup = where(logical_and(Rrup > 8, Rrup <= 18),
                    a9,
                    fHWRrup)
    fHWRrup = where(logical_and(Rrup  > 18,  Rrup <= 25),
                    a9 * (1 - (Rrup - 18) / 7),
                    fHWRrup)
    
    f4 =  fHWM * fHWRrup

    R = sqrt(Rrup **2 + c4**2)
    f1 = (a1 + where(mag <=c1, a2, a4) * (mag - c1) + a12 * (8.5 - mag)**n +
          log(R) * (a3 + a13 * (mag - c1)))    
    rockMeanPGA = f1 + F * f3 + Fhw * f4
    f5 = a10 + a11 * log(exp(rockMeanPGA) + c5)
    log_mean = rockMeanPGA + deep_soil * f5
    
    sd = b5 - b6 * (mag - 5.0) # [site, event, period]
    sd = where(mag <  5.0, b5, sd)
    sd = where(mag >= 7.0,  b5 - 2 * b6, sd)

    return log_mean, sd


Abrahamson_Silva_1997_args = [Abrahamson_Silva_1997_distribution,
                              Abrahamson_Silva_1997_magnitude_type,
                              Abrahamson_Silva_1997_distance_type,
                              
                              Abrahamson_Silva_1997_coefficient,
                              Abrahamson_Silva_1997_coefficient_period,
                              linear_interpolation,

                              Abrahamson_Silva_1997_sigma_coefficient,
                              Abrahamson_Silva_1997_coefficient_period,
                              linear_interpolation,
                              
                              Abrahamson_Silva_1997_uses_Vs30]


ground_motion_init['Abrahamson_Silva_1997'] = Abrahamson_Silva_1997_args
