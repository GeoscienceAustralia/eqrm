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
    'gound_motion_init' (sic) with the model name as key.

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
            mag                event magnitude
            distance           distance of the site from the event
            coefficient        an array of model coefficients
            sigmacoefficient   an array of model sigma coefficients
            depth              depth of the event

        Most of these parameters will be numpy arrays.

        The shapes of each parameter are:
            mag.shape = (site, events, 1)
            distance.shape = (site, events, 1)
            coefficient.shape = (num_coefficients, 1, 1, num_periods)
            sigmacoefficient.shape = (num_sigmacoefficients, 1, 1, num_periods)
            depth.shape = (site, events, 1)

        Note that the 'site' dimension above is currently 1.
"""

import math
from copy import  deepcopy
from scipy import where, sqrt, array, asarray, exp, log, newaxis, zeros, \
     log10, isfinite, weave, ones, shape, reshape
 
from eqrm_code.ground_motion_misc import linear_interpolation, \
     Australian_standard_model, Australian_standard_model_interpolation

from eqrm_code import util 


LOG10E = 0.43429448190325182

# A dictionary of all the info specified bellow.
# This is used by ground_motion_specification.
gound_motion_init = {}

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
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    num_periods=coefficient.shape[3]
    assert coefficient.shape==(6,1,1,num_periods)
    assert sigma_coefficient.shape==(2,1,1,num_periods)
    c1,c2,c4,c6,c7,c10=coefficient
    model_sigma,regression_sigma=sigma_coefficient
    log_mean=c1+c2*mag+log((distance+exp(c4))**(c6+c7*mag))+c10*(mag-6.0)**2
    log_sigma=(model_sigma+regression_sigma)
    return log_mean,log_sigma


Allen_magnitude_type='Mw'
Allen_distance_type='Hypocentral'

Allen_args=[
    Allen_distribution,
    Allen_magnitude_type,
    Allen_distance_type,
    
    Allen_coefficient,
    Allen_coefficient_period,
    Allen_interpolation,
    
    Allen_sigma_coefficient,
    Allen_sigma_coefficient_period,
    Allen_interpolation]

gound_motion_init['Allen'] = Allen_args

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
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    num_periods=coefficient.shape[3]
    assert coefficient.shape==(3,1,1,num_periods)
    assert sigma_coefficient.shape==(2,1,1,num_periods)
    # mag.shape (site, events, 1)
    # distance.shape (site, events, 1)
    
    a,b,c=coefficient
    log_sigma=sigma_coefficient[0]
    log_mean=a+b*mag-c*log(distance)
    return log_mean,log_sigma


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

Gaull_1990_WA_args=[
    Gaull_1990_WA_distribution,
    Gaull_1990_WA_magnitude_type,
    Gaull_1990_WA_distance_type,
    
    Gaull_1990_WA_coefficient,
    Gaull_1990_WA_coefficient_period,
    Gaull_1990_WA_coefficient_interpolation,
    
    Gaull_1990_WA_sigma_coefficient,
    Gaull_1990_WA_sigma_coefficient_period,
    Gaull_1990_WA_sigma_coefficient_interpolation]

gound_motion_init['Gaull_1990_WA'] = Gaull_1990_WA_args

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

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    c1,c2,c3,c4,c5,c6,c7=coefficient
    d1,d2,d3,f1,f2,e1,e2=sigma_coefficient
    
    Rm=sqrt(distance**2+c7**2)
    log_Rm=log(Rm)
    log_100 = 4.60517018599 
    log_mean=c1+c2*(mag-6.0)+c3*((mag-6.0)**2)-c4*log_Rm\
              -(c5-c4)*where((log_Rm-log_100)>0,(log_Rm-log_100),0)-c6*Rm
    del log_Rm

    log_sigma_aleatory1=(mag<=5)*(d1)
    log_sigma_aleatory1+=(5<mag)*(mag<=5.5)*(d1+(d2-d1)*(mag-5)/0.5)
    log_sigma_aleatory1+=(5.5<mag)*(mag<=8)*(d2+(d3-d2)*(mag-5.5)/2.5)
    log_sigma_aleatory1+=(8<mag)*(d3)
    # getting the aleatory (mag part) sigma
    log_sigma_aleatory2=(distance<=5)*(f1)
    log_sigma_aleatory2+=(5<distance)*(distance<=20)*(f1+(f2-f1)* \
                                                      (distance-5)/15)
    log_sigma_aleatory2+=(20<distance)*f2
    # getting the aleatory (distance part) sigma
    ##log_epistemic=e1+e2*(mag-6)
    # getting model uncertainty
    ###log_sigma=sqrt(log_epistemic**2+log_sigma_aleatory1**2\
    ###               +log_sigma_aleatory2**2)
    log_sigma=sqrt(log_sigma_aleatory1**2+
                   log_sigma_aleatory2**2)                  
    return log_mean,log_sigma

def Toro_1997_midcontinent_distribution(**kwargs):

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    #print "coefficient", coefficient                    
    num_sites,num_events=distance.shape[0:2]
    num_periods=coefficient.shape[3]
    assert coefficient.shape==(7,1,1,num_periods)
    #assert sigma_coefficient.shape==(7,1,1,num_periods)
    assert mag.shape==(1,num_events,1)
    assert distance.shape==(num_sites,num_events,1)
    log_mean=zeros((num_sites,num_events,num_periods),dtype=float)
    #log_sigma=zeros((num_sites,num_events,num_periods),dtype=float)
    log_sigma=0.0 # who cares - I think the python bit is fast enough.

    coefficient=coefficient[:,0,0,:]
    mag=mag[0,:,0]
    distance=distance[:,:,0]
    
    code="""
    double c1,c2,c3,c4,c5,c6,c7;
    double m,d;
    double Rm,log_Rm,log_Rm_100;
    for (int i=0; i<num_sites; ++i){
        for (int j=0; j<num_events; ++j){
            m=mag(j);
            d=distance(i,j);
            
            for (int k=0;k<num_periods;++k){
                c1=coefficient(0,k);
                c2=coefficient(1,k);
                c3=coefficient(2,k);
                c4=coefficient(3,k);
                c5=coefficient(4,k);
                c6=coefficient(5,k);
                c7=coefficient(6,k);
                
                Rm=sqrt(d*d+c7*c7);
                log_Rm=log(Rm);
                log_Rm_100=log_Rm-log(100);
                
                if (log_Rm_100<0.0){
                    log_Rm_100=0.0;
                }                   
                log_mean(i,j,k)=c1+c2*(m-6.0)+c3*((m-6.0)*(m-6.0))
                               -c4*log_Rm-(c5-c4)*log_Rm_100-c6*Rm;
            }       
        }
    }
    return_val = 0;
    """
    try:
        weave.inline(code,
                     ['num_sites','num_events','num_periods',
                      'coefficient','sigma_coefficient',
                      'mag','log_mean','distance','log_sigma'],
                     type_converters=weave.converters.blitz,
                     compiler='gcc')   
    except IOError:
        raise util.WeaveIOError 
    
    coefficient=coefficient[:,newaxis,newaxis,:]
    mag=mag[newaxis,:,newaxis]
    distance=distance[:,:,newaxis]
    
    d1,d2,d3,f1,f2,e1,e2=sigma_coefficient
    log_sigma_aleatory1=(mag<=5)*(d1)
    log_sigma_aleatory1+=(5<mag)*(mag<=5.5)*(d1+(d2-d1)*(mag-5)/0.5)
    log_sigma_aleatory1+=(5.5<mag)*(mag<=8)*(d2+(d3-d2)*(mag-5.5)/2.5)
    log_sigma_aleatory1+=(8<mag)*(d3)
    # getting the aleatory (mag part) sigma
    log_sigma_aleatory2=(distance<=5)*(f1)
    log_sigma_aleatory2+=(5<distance)*(distance<=20)*(f1+(f2-f1)* \
                                                      (distance-5)/15)
    log_sigma_aleatory2+=(20<distance)*f2
    # getting the aleatory (distance part) sigma
    ##log_epistemic=e1+e2*(mag-6)
    # getting model uncertainty
    ###log_sigma=sqrt(log_epistemic**2+log_sigma_aleatory1**2\
    ###               +log_sigma_aleatory2**2)
    log_sigma=sqrt(log_sigma_aleatory1**2+
                   log_sigma_aleatory2**2)
    
    return log_mean,log_sigma

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

Toro_1997_midcontinent_args=[
    Toro_1997_midcontinent_distribution,
    Toro_1997_midcontinent_magnitude_type,
    Toro_1997_midcontinent_distance_type,
    
    Toro_1997_midcontinent_coefficient,
    Toro_1997_midcontinent_coefficient_period,
    Toro_1997_midcontinent_interpolation,
    
    Toro_1997_midcontinent_sigma_coefficient,
    Toro_1997_midcontinent_coefficient_period,
    Toro_1997_midcontinent_sigma_coefficient_interpolation]

gound_motion_init['Toro_1997_midcontinent'] = Toro_1997_midcontinent_args

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
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
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

    log_sigma=sigma_coefficient[0]
    return log_mean,log_sigma

AllenSEA06_args=[
    AllenSEA06_distribution,
    AllenSEA06_magnitude_type,
    AllenSEA06_distance_type,
    
    AllenSEA06_coefficient,
    AllenSEA06_coefficient_period,
    AllenSEA06_interpolation,
    
    AllenSEA06_sigma_coefficient,
    AllenSEA06_sigma_coefficient_period,
    AllenSEA06_sigma_coefficient_interpolation]

gound_motion_init['AllenSEA06'] = AllenSEA06_args

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

def Atkinson_Boore_97_distribution_python(mag,distance,coefficient,
                                   sigma_coefficient,depth):
    c1,c2,c3,c4=coefficient
    log_mean = c1+c2*(mag-6)+c3*(mag-6)**2-log(distance)-c4*distance         
    log_sigma=sigma_coefficient[0]
    return log_mean,log_sigma

def Atkinson_Boore_97_distribution(**kwargs):

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    num_sites,num_events=distance.shape[0:2]
    num_periods=coefficient.shape[3]
    assert coefficient.shape==(4,1,1,num_periods)
    assert sigma_coefficient.shape==(1,1,1,num_periods)
    assert mag.shape==(1,num_events,1)
    assert distance.shape==(num_sites,num_events,1)
    log_mean=zeros((num_sites,num_events,num_periods),dtype=float)
    log_sigma=zeros((num_sites,num_events,num_periods),dtype=float)

    coefficient=coefficient[:,0,0,:]
    sigma_coefficient=sigma_coefficient[0,0,0,:]
    mag=mag[0,:,0]
    distance=distance[:,:,0]
    code="""
    double c1,c2,c3,c4;
    double s;
    double m,d;
    for (int i=0; i<num_sites; ++i){
        for (int j=0; j<num_events; ++j){
            m=mag(j);
            d=distance(i,j);
            for (int k=0;k<num_periods;++k){
                c1=coefficient(0,k);
                c2=coefficient(1,k);
                c3=coefficient(2,k);
                c4=coefficient(3,k);
                
                log_mean(i,j,k) = c1+c2*(m-6)+(c3*(m-6)*(m-6))-log(d)-c4*d;
                
                s=sigma_coefficient(k);
                log_sigma(i,j,k)=s;                
            }       
        }
    }
    return_val = 0;
    """
    try:
        weave.inline(code,
                     ['num_sites','num_events','num_periods',
                      'coefficient','sigma_coefficient',
                      'mag','log_mean','distance','log_sigma'],
                     type_converters=weave.converters.blitz,
                     compiler='gcc')     
    except IOError:
        raise util.WeaveIOError 
  
    return log_mean,log_sigma

Atkinson_Boore_97_distance_type='Rupture'
Atkinson_Boore_97_magnitude_type='Mw'

Atkinson_Boore_97_args=[
    Atkinson_Boore_97_distribution,
    Atkinson_Boore_97_magnitude_type,
    Atkinson_Boore_97_distance_type,
    
    Atkinson_Boore_97_coefficient,
    Atkinson_Boore_97_coefficient_period,
    Atkinson_Boore_97_interpolation,
    
    Atkinson_Boore_97_sigma_coefficient,
    Atkinson_Boore_97_sigma_coefficient_period,
    Atkinson_Boore_97_sigma_coefficient_interpolation
    ]


gound_motion_init['Atkinson_Boore_97'] = Atkinson_Boore_97_args


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
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    
    F=1.0
    
    # R = RrupMatrix + c7.*exp(c8.*MagMatrix);
    # lnSA(ind,:) = c1*F + c2 + c3.*MagMatrix + c4.*(8.5-MagMatrix).^(2.5) ...
    #   +c5.*log(R)+ c6.*log(RrupMatrix+2);
    #if not (mag<8.5).all():
    #    raise ValueError('Sadigh 97 is not valid for magnitude > 8.5')
        
    c_less65=coefficient[:8]
    c_less65=c_less65+mag*0 # expand it to size of mag
    
    c_more65=coefficient[8:]
    c_more65=c_more65+mag*0 # expand it to size of mag

    coefficient=where((mag+c_less65*0)>6.5,c_more65,c_less65)
    
    c1,c2,c3,c4,c5,c6,c7,c8=coefficient
    R = distance + c7*exp(c8*mag)
    
    log_mean = (c1*F + c2 + c3*mag + c4*(8.5-mag)**(2.5)
                +c5*log(R)+ c6*log(distance+2))

    s1,s2,s3=sigma_coefficient
    
    log_sigma=where((mag+0*s1)>7.21,s3+0*mag,s1-s2*mag)
    assert isfinite(log_mean).all()
    return log_mean,log_sigma

def Sadigh_97_distribution(**kwargs):

    """
    distance is a 3D array. First D is sites, second dimension is events,
    third can only have one value.
    """
    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']

    
    num_sites,num_events=distance.shape[0:2]
    num_periods=coefficient.shape[3]
    assert coefficient.shape==(16,1,1,num_periods)
    assert sigma_coefficient.shape==(3,1,1,num_periods)
    assert mag.shape==(1,num_events,1)
    assert distance.shape==(num_sites,num_events,1)
    log_mean=zeros((num_sites,num_events,num_periods),dtype=float)
    log_sigma=zeros((num_sites,num_events,num_periods),dtype=float)

    coefficient=coefficient[:,0,0,:]
    sigma_coefficient=sigma_coefficient[:,0,0,:]
    mag=mag[0,:,0]
    distance=distance[:,:,0]
    code="""
    double F;
    double c1,c2,c3,c4,c5,c6,c7,c8;
    double s1,s2,s3;
    double m,d;
    double R;
    F=1.0;
    int c_offset;
    for (int i=0; i<num_sites; ++i){
        for (int j=0; j<num_events; ++j){
            m=mag(j);
            d=distance(i,j);
            
            if (m>6.5){
                c_offset=8;
            }
            else{
                c_offset=0;
            }
            for (int k=0;k<num_periods;++k){
                c1=coefficient((0+c_offset),k);
                c2=coefficient((1+c_offset),k);
                c3=coefficient((2+c_offset),k);
                c4=coefficient((3+c_offset),k);
                c5=coefficient((4+c_offset),k);
                c6=coefficient((5+c_offset),k);
                c7=coefficient((6+c_offset),k);
                c8=coefficient((7+c_offset),k);
                
                R = d + c7*exp(c8*m);
                log_mean(i,j,k) = c1*F + c2 + c3*m+ c4*pow((8.5-m),2.5)
                                  +c5*log(R)+ c6*log(d+2.0);
                s1=sigma_coefficient(0,k);
                s2=sigma_coefficient(1,k);
                s3=sigma_coefficient(2,k);
                
                if (m>7.21){
                    log_sigma(i,j,k)=s3;
                }
                else{
                    log_sigma(i,j,k)=s1-s2*m;
                }
            }       
        }
    }
    return_val = 0;
    """
    try:
        weave.inline(code,
                     ['num_sites','num_events','num_periods',
                      'coefficient','sigma_coefficient',
                      'mag','log_mean','distance','log_sigma'],
                     type_converters=weave.converters.blitz,
                     compiler='gcc')   
    except IOError:
        raise util.WeaveIOError 

    assert isfinite(log_mean).all()
    return log_mean,log_sigma

Sadigh_97_distance_type='Rupture'
Sadigh_97_magnitude_type='Mw'

Sadigh_97_args=[
    Sadigh_97_distribution,
    Sadigh_97_magnitude_type,
    Sadigh_97_distance_type,
    
    Sadigh_97_coefficient,
    Sadigh_97_coefficient_period,
    Sadigh_97_interpolation,
    
    Sadigh_97_sigma_coefficient,
    Sadigh_97_sigma_coefficient_period,
    Sadigh_97_sigma_coefficient_interpolation]

gound_motion_init['Sadigh_97'] = Sadigh_97_args


#***************  End of Sadigh_97 MODEL  ************


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

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    depth = kwargs['depth']
  
    c1,c2,c3,Z_t=coefficient

    # Z_t=0.0 for interface earthquakes
    # Z_t=1 for intraslab earthquakes

    use_dist=(distance<10)
    use_dist=use_dist*1.0
    use_dist2=(1-use_dist)
    distance=distance*use_dist2+10*use_dist
    #print distance
    #print mag
    #print depth
    #print Z_t
    log_mean=0.2418+1.414*mag+c1+c2*((10.0-mag)**3)+c3* \
              log(distance+1.7818*exp(0.554*mag))+0.00607*depth+0.3846*Z_t
    s1,s2=sigma_coefficient
    #print log_mean
    use_m=(mag<8)
    use_m=use_m*1.0
    use_n=(1-use_m)
    log_sigma=s1+s2*mag*use_m+s2*8*use_n #SD uses magnitude=8 for magnitude>8
    #print log_sigma
    assert isfinite(log_mean).all()
    return log_mean,log_sigma

Youngs_97_distance_type='Rupture'
Youngs_97_magnitude_type='Mw'

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
    Youngs_97_sigma_coefficient_interpolation]

gound_motion_init['Youngs_97_interface'] = Youngs_97_interface_args

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
    Youngs_97_sigma_coefficient_interpolation]

gound_motion_init['Youngs_97_intraslab'] = Youngs_97_intraslab_args

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
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
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

Combo_Sadigh_Youngs_M8_args=[
    Combo_Sadigh_Youngs_M8_distribution_python,
    Youngs_97_magnitude_type,
    Youngs_97_distance_type,
    
    Combo_Sadigh_Youngs_M8_coeff,
    Sadigh_97_coefficient_period,
    linear_interpolation,  
 
    Combo_Sadigh_Youngs_M8_sigma_coeff,
    Sadigh_97_sigma_coefficient_period,
    linear_interpolation]

gound_motion_init['Combo_Sadigh_Youngs_M8'] = Combo_Sadigh_Youngs_M8_args

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
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
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
    #print distance
    #print mag
    #print depth
    #print Z_t
    log_mean=0.2418+1.414*mag+c1+c2*((10.0-mag)**3)+c3* \
              log(distance+1.7818*exp(0.554*mag))+0.00607*depth+0.3846*Z_t
    s1,s2=sigma_coefficient
    #print log_mean
    use_m=(mag<8)
    use_m=use_m*1.0
    use_n=(1-use_m)
    log_sigma=s1+s2*mag*use_m+s2*8*use_n #SD uses magnitude=8 for magnitude>8
    #print log_sigma
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

gound_motion_init['Youngs_97'] = Youngs_97_args

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
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
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

Combo_Sadigh_Youngs_M8_args=[
    Combo_Sadigh_Youngs_M8_distribution_python,
    Youngs_97_magnitude_type,
    Youngs_97_distance_type,    
    Combo_Sadigh_Youngs_M8_coeff,
    Sadigh_97_coefficient_period,
    linear_interpolation,   
    Combo_Sadigh_Youngs_M8_sigma_coeff,
    Sadigh_97_sigma_coefficient_period,
    linear_interpolation]

gound_motion_init['Combo_Sadigh_Youngs_M8'] = Combo_Sadigh_Youngs_M8_args

#***************  End of Combo_Sadigh_Youngs_M8 MODEL  ************
"""

#***************  Start of Boore_08 MODEL  ************
# This is what the coefficients are;
# %T c1 c2 c3 h e1 e2 e3 e4 e5 e6 e7 mh sig tu sigtu tm sigtm blin b1 b2
# PGV -0.87370 0.10060 -0.00334 2.54 5.00121 5.04727 4.63188 5.08210 0.18322 -0.12736 0.00000 8.50 0.500 0.286 0.576 0.256 0.560 -0.600 -0.500 -0.06

# The axis for this are wrong
# This is period, coefficient
# It has to be coefficient, period
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

def Boore_08_distribution(**kwargs):
    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    vs30 = kwargs['vs30']

    if vs30 is None:
        raise Exception, "vs30 value unknown"       
        
    # An expensive way of showing what the dimensions must be?
    num_sites,num_events=distance.shape[0:2]
    num_periods=coefficient.shape[3]
    assert coefficient.shape==(20,1,1,num_periods)
    #assert sigma_coefficient.shape==(3,1,1,num_periods)
    assert mag.shape==(1,num_events,1) # (num_sites,num_events,1)?
    assert distance.shape==(num_sites,num_events,1)

    c1, c2, c3, h, e1, e2, e3, e4, e5, e6, e7 = coefficient[:11]
    mh, sig, tu, sigtu, tm, sigtm, blin, b1, b2 = coefficient[11:]

    c1_pga, c2_pga, c3_pga, h_pga = Boore_08_coefficient_raw[PGA_BA08][0:4]
    e1_pga, e2_pga, e3_pga, e4_pga = Boore_08_coefficient_raw[PGA_BA08][4:8]
    e5_pga, e6_pga, e7_pga = Boore_08_coefficient_raw[PGA_BA08][8:11]
    mh_pga, sig_pga = Boore_08_coefficient_raw[PGA_BA08][11:13]
    tu_pga, sigtu_pga = Boore_08_coefficient_raw[PGA_BA08][13:15]
    tm_pga, sigtm_pga, blin_pga = Boore_08_coefficient_raw[PGA_BA08][15:18]
    b1_pga, b2_pga = Boore_08_coefficient_raw[PGA_BA08][18:20]
    fd = fd_Boore_08(c1, c2, c3, distance, h, mag)
    fd_pga = fd_Boore_08(c1_pga, c2_pga, c3_pga, distance, h, mag)  

    fm = fm_Boore_08(e1, e5, e6, e7, mag, mh)
    fm_pga = fm_Boore_08(e1_pga, e5_pga, e6_pga, e7_pga, mag, mh_pga)
    
    bnl = bnl_Boore_08(b1, b2, vs30)

    pga4nl = exp(fd_pga + fm_pga)
    #print "gmi pga4nl", pga4nl

    fs = fs_Boore_08(blin, pga4nl, bnl, vs30)
    
    log_mean = fd + fm + fs    # BA08 (1)
    
    log_sigma = ones((log_mean.shape))*sigtu
    return log_mean,log_sigma

def fd_Boore_08(c1, c2, c3, distance, h, mag):  
    mref = 4.5  
    rref = 1.0 # km     
    r = sqrt(distance**2 + h**2) # BA08 (4)
    fd = (c1 + c2*(mag - mref))* log(r/rref) + c3*(r - rref) # BA08 (4)
    return fd

def fm_Boore_08(e1, e5, e6, e7, mag, mh):
    
    mag = asarray(mag)
    # Note, no distance, so it is the same for all sites.
    # Cache to speed this.

    # BA08 (5a) & (5b) mod.
    # Note the ( + 0*e1) is to get the index shape correct.
    fm = where(mag + 0*e1<= mh,
               e1 + e5*(mag - mh) + e6*(mag - mh)**2,
               e1 + e7*(mag - mh)) 
    # *u + e2*ss + e3*ns + e4*rs for future work
               
    return fm

# def memoize(function):
#     b1 = None
#     b2 = 'hear'
#     vs30 = None
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
def bnl_Boore_08(b1, b2, vs30):
    # Should memoize the answer.
    vs30 = float(vs30)
    # get bnl   
    if vs30 <= V1_BOORE_08:
        bnl = b1  # BA08 (13a)
    elif vs30 <= V2_BOORE_08:
        # BA08 (13b)
        bnl = (b1-b2)*log(vs30/V2_BOORE_08)*RECIP_LOG_V1_DIV_V2 + b2
    elif vs30 < VREF_BOORE_08:   
        bnl = b2*log(vs30/VREF_BOORE_08)*RECIP_LOG_V2_DIV_VREF  # BA08 (13c)
    else:
        bnl = 0.0    # BA08 (13d)
    return bnl
 
def fs_Boore_08(blin, pga4nl, bnl, vs30):
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
    flin = blin * log(vs30/VREF_BOORE_08)   # BA08 (7)

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

Boore_08_args=[
    Boore_08_distribution,
    Boore_08_magnitude_type,
    Boore_08_distance_type,
    
    Boore_08_coefficient,
    Boore_08_coefficient_period,
    Boore_08_interpolation,
    
    Boore_08_sigma_coefficient,
    Boore_08_sigma_coefficient_period,
    Boore_08_sigma_coefficient_interpolation]

gound_motion_init['Boore_08'] = Boore_08_args

#***************  End of Boore_08 MODEL  ************


#***************  START COMMON_SOMMERVILLE BLOCK  ************

Somerville_interpolation=linear_interpolation

Somerville_sigma_coefficient_interpolation=linear_interpolation

def Somerville_distribution(**kwargs):

    # This function is called in Ground_motion_calculator.distribution_function
    # The usual parameters passed are
    # mag, distance, coefficient, sigma_coefficient, depth,  vs30
    mag = kwargs['mag']
    distance = kwargs['distance']
    coefficient = kwargs['coefficient']
    sigma_coefficient = kwargs['sigma_coefficient']
    depth = kwargs['depth']
    
    # An expensive way of showing what the dimensions must be?
    num_sites,num_events=distance.shape[0:2]
    num_periods=coefficient.shape[3]
    assert coefficient.shape==(8,1,1,num_periods)
    #assert sigma_coefficient.shape==(3,1,1,num_periods)
    assert mag.shape==(1,num_events,1) # (num_sites,num_events,1)?
    assert distance.shape==(num_sites,num_events,1)
#     print "num_sites", num_sites
#     print "num_events",num_events 
#     print "num_periods", num_periods

    log_mean = Somerville_log_mean(coefficient, mag, distance)
    log_sigma=sigma_coefficient[0]
    assert isfinite(log_mean).all()
    return log_mean,log_sigma

def Somerville_log_mean(coefficient, mag, distance):
    #print "coefficient", coefficient
    c1, c2, c3, c4, c5, c6, c7, c8 = coefficient
    m1 = 6.4
    mag = asarray(mag)
    distance = asarray(distance)
    #print "t distance", distance
    ln_R = log((distance**2 + 36.0)**0.5)
    #print "t ln_R", ln_R
    
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
    #print "c6", c6
    T6 = where(distance + 0*c6 < 50.0,
               0,
               c6*(ln_R-ln_R1))
#     print "c3", c3
#     print "ln_R1", ln_R1
#     print "ln_R", ln_R
#     print "distance", distance
#     print "c3*ln_R", c3*ln_R
#     print "c3*ln_R1", c3*ln_R1
    T3 = where(distance + 0*c3 < 50.0,
               c3*ln_R,
               c3*ln_R1)
    log_mean = c1 + T2 + T3 + c4*mag_neg_m1*ln_R + c5*distance + T6 + \
               c8*(8.5 - mag)**2
    return log_mean

Somerville_distance_type='Joyner_Boore'
Somerville_magnitude_type='Mw'

#***************  END COMMON_SOMMERVILLE BLOCK  ************

#***************  Start of Somerville_Yilgarn MODEL  ************
# dimension = (period, coeffiecient)
Somerville_Yilgarn_coefficient_raw = array([
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
Somerville_Yilgarn_coefficient = Somerville_Yilgarn_coefficient_raw.transpose()

Somerville_Yilgarn_sigma_coefficient=[[
    0.5513, 0.5512, 0.551, 0.5508 ,0.5509, 0.551, 0.5514, 0.5529, 0.5544,
    0.5558, 0.5583, 0.5602, 0.5614, 0.5636, 0.5878, 0.6817, 0.8514,
    0.8646, 0.8424, 0.8225, 0.8088, 0.7808, 0.7624
    ]]

Somerville_Yilgarn_coefficient_period=[
    0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3003,
   0.4, 0.5, 0.75, 1., 1.4993, 2., 3.003, 4., 5., 7.5019, 10.,]

Somerville_Yilgarn_sigma_coefficient_period=[
   0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3003,
   0.4, 0.5, 0.75, 1., 1.4993, 2., 3.003, 4., 5., 7.5019, 10.,]
#print "len(Somerville_Yilgarn_sig_coefficient)", len(Somerville_Yilgarn_sigma_coefficient)
#print "len(Somerville_Yilgarn_sigma_coefficient_period)", len(Somerville_Yilgarn_sigma_coefficient_period)


Somerville_Yilgarn_args=[
    Somerville_distribution,
    Somerville_magnitude_type,
    Somerville_distance_type,
    
    Somerville_Yilgarn_coefficient,
    Somerville_Yilgarn_coefficient_period,
    Somerville_interpolation,
    
    Somerville_Yilgarn_sigma_coefficient,
    Somerville_Yilgarn_sigma_coefficient_period,
    Somerville_sigma_coefficient_interpolation]

gound_motion_init['Somerville_Yilgarn'] = Somerville_Yilgarn_args
#***************  End of Somerville_Yilgarn MODEL   ************
#***************  Start of Somerville_Non_Cratonic MODEL   ************
# dimension = (period, coeffiecient)
Somerville_Non_Cratonic_coefficient_raw = array([
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
Somerville_Non_Cratonic_coefficient = Somerville_Non_Cratonic_coefficient_raw.transpose()

Somerville_Non_Cratonic_sigma_coefficient=[[
    0.5513, 0.5512, 0.551, 0.5508 ,0.5509, 0.551, 0.5514, 0.5529, 0.5544,
    0.5558, 0.5583, 0.5602, 0.5614, 0.5636, 0.5878, 0.6817, 0.8514,
    0.8646, 0.8424, 0.8225, 0.8088, 0.7808, 0.7624
    ]]

Somerville_Non_Cratonic_coefficient_period=[
    0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3003,
   0.4, 0.5, 0.75, 1., 1.4993, 2., 3.003, 4., 5., 7.5019, 10.,]

Somerville_Non_Cratonic_sigma_coefficient_period=[
   0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3003,
   0.4, 0.5, 0.75, 1., 1.4993, 2., 3.003, 4., 5., 7.5019, 10.,]

Somerville_Non_Cratonic_args=[
    Somerville_distribution,
    Somerville_magnitude_type,
    Somerville_distance_type,
    
    Somerville_Non_Cratonic_coefficient,
    Somerville_Non_Cratonic_coefficient_period,
    Somerville_interpolation,
    
    Somerville_Non_Cratonic_sigma_coefficient,
    Somerville_Non_Cratonic_sigma_coefficient_period,
    Somerville_sigma_coefficient_interpolation]

gound_motion_init['Somerville_Non_Cratonic'] = Somerville_Non_Cratonic_args
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
        with a Combined Green's Function and Stochastic Approach",
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
    log_sigma = sigma_coefficient[0]

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

Liang_2008_args = [Liang_2008_distribution,
                   Liang_2008_magnitude_type,
                   Liang_2008_distance_type,
                   Liang_2008_coefficient,
                   Liang_2008_coefficient_period,
                   Liang_2008_interpolation,
                   Liang_2008_sigma_coefficient,
                   Liang_2008_sigma_coefficient_period,
                   Liang_2008_interpolation]

gound_motion_init['Liang_2008'] = Liang_2008_args

##########################  End of Liang_2008 model  ###########################

#################  Start of Atkinson06 bedrock & soil models  ##################

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

    # check we have the right shapes
    num_periods = coefficient.shape[3]
    msg = ('Expected coefficient.shape %s, got %s'
           % (str((13, 1, 1, num_periods)), str(coefficient.shape)))
    assert coefficient.shape == (13, 1, 1, num_periods), msg

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

    log_mean = c1 + c2*M + c3*M*M + (c4 + c5*M)*f1 + (c6 + c7*M)*f2 + \
                   (c8 + c9*M)*f0 + c10*Rcd + S
    log_sigma = sigma_coefficient[0]

    return (log_mean, log_sigma)

def Atkinson06_bedrock_distribution(**kwargs):
    """The Atkinson06_bedrock model function.

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

    # get result in log10(cm/s/s)
    (log_mean, log_sigma) = Atkinson06_basic(S=0.0, **kwargs)

    # convert to g and natural log
    log_mean = log_mean/Log102Ln - LnCmss2Lng
    log_sigma = log_sigma/Log102Ln - LnCmss2Lng

    return (log_mean, log_sigma)

# constants for S calculations
Atkinson06_Vref = 760.0
Atkinson06_V2 = 300.0
Atkinson06_V1 = 180.0
Atkinson06_logV1divV2 = math.log(Atkinson06_V1 / Atkinson06_V2)
Atkinson06_logV2divVref = math.log(Atkinson06_V2 / Atkinson06_Vref)

def Atkinson06_calcS(pgaBC, **kwargs):
    """Calculate the S parameter for soil.

    pgaBC   the pgaBC value to use
    kwargs  dictionary of parameters, expect:
                coefficient, vs30
    """

    # get args
    coefficient = kwargs['coefficient']
    vs30 = kwargs['vs30']

    # check we have the right shapes
    num_periods = coefficient.shape[3]
    assert coefficient.shape == (13, 1, 1, num_periods)

    # get the Blin, B1 and B2 coefficients.
    (Blin, B1, B2) = coefficient[-3:]

    # get the Bnl array from eqns 8A, 8B, 8C, 8D, page 2200.
    # we do this by calculating 4 arrays for each of 8A, 8b, 8C and 8D
    # and then filling appropriate elements of resultant Bnl.
    BnlA = B1
    BnlB = (B1 - B2) * log(vs30/Atkinson06_V2) / Atkinson06_logV1divV2 + B2
    BnlC = B2 * log(vs30/Atkinson06_Vref) / Atkinson06_logV2divVref
    Bnl = 0.0

    # TODO: TEST IF where(x < A <= y, ?, ??) FASTER
    Bnl = where(vs30 <= Atkinson06_Vref, BnlC, Bnl)
    Bnl = where(vs30 <= Atkinson06_V2, BnlB, Bnl)
    Bnl = where(vs30 <= Atkinson06_V1, BnlA, Bnl)

    # limit element-wise pgaBC values to be >= 60
    pgaBC = where(pgaBC < 60.0, 60.0, pgaBC)

    # return the S value
    return log10(exp(Blin*log(vs30/Atkinson06_Vref) + Bnl*log(pgaBC/100)))

def Atkinson06_soil_distribution(**kwargs):
    """The Atkinson06_soil model function.

    kwargs  dictionary of parameters, expect:
                mag, distance, coefficient, sigma_coefficient, vs30

    This function just calls Atkinson06_basic() with a computed S value
    and converts the result to ln g.
    """

    # get required kwarg values, check shapes
    try:
        mag = kwargs['mag']
        distance = kwargs['distance']
        coefficient = kwargs['coefficient']
        sigma_coefficient = kwargs['sigma_coefficient']
        vs30 = kwargs['vs30']
    except KeyError, e:
        print('kwargs dictionary to Atkinson06_soil_distribution() '
              'is missing a parameter: %s' % e)
        raise

    num_periods = coefficient.shape[3]
    assert coefficient.shape == (13, 1, 1, num_periods)
    assert sigma_coefficient.shape == (2, 1, 1, num_periods)

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

    return (log_mean, log_sigma)


Atkinson06_magnitude_type = 'Mw'
Atkinson06_distance_type = 'Rupture'

# dimension = (#periods, #coefficients)
# data from tables 6 and 8, last three columns from table 8
#               c1        c2         c3         c4        c5      
#                   c6        c7         c8         c9         c10
#                        Blin     B1       B2
tmp = array([[-5.41E+00, 1.71E+00, -9.01E-02, -2.54E+00, 2.27E-01,
                  -1.27E+00, 1.16E-01,  9.79E-01, -1.77E-01, -1.76E-04,
                       -0.752,  -0.300,   0.000],	#5.00
             [-5.79E+00, 1.92E+00, -1.07E-01, -2.44E+00, 2.11E-01,
                  -1.16E+00, 1.02E-01,  1.01E+00, -1.82E-01, -2.01E-04,
                       -0.745,  -0.310,   0.000],	#4.00
             [-6.04E+00, 2.08E+00, -1.22E-01, -2.37E+00, 2.00E-01,
                  -1.07E+00, 8.95E-02,  1.00E+00, -1.80E-01, -2.31E-04,
                       -0.740,  -0.330,   0.000],	#3.13
             [-6.17E+00, 2.21E+00, -1.35E-01, -2.30E+00, 1.90E-01,
                  -9.86E-01, 7.86E-02,  9.68E-01, -1.77E-01, -2.82E-04,
                       -0.736,  -0.350,   0.000],	#2.50
             [-6.18E+00, 2.30E+00, -1.44E-01, -2.22E+00, 1.77E-01,
                  -9.37E-01, 7.07E-02,  9.52E-01, -1.77E-01, -3.22E-04,
                       -0.730,  -0.375,   0.000],	#2.00
             [-6.04E+00, 2.34E+00, -1.50E-01, -2.16E+00, 1.66E-01,
                  -8.70E-01, 6.05E-02,  9.21E-01, -1.73E-01, -3.75E-04,
                       -0.726,  -0.395,   0.000],	#1.60
             [-5.72E+00, 2.32E+00, -1.51E-01, -2.10E+00, 1.57E-01,
                  -8.20E-01, 5.19E-02,  8.56E-01, -1.66E-01, -4.33E-04,
                       -0.714,  -0.397,   0.000],	#1.25
             [-5.27E+00, 2.26E+00, -1.48E-01, -2.07E+00, 1.50E-01,
                  -8.13E-01, 4.67E-02,  8.26E-01, -1.62E-01, -4.86E-04,
                       -0.700,  -0.440,   0.000],	#1.00
             [-4.60E+00, 2.13E+00, -1.41E-01, -2.06E+00, 1.47E-01,
                  -7.97E-01, 4.35E-02,  7.75E-01, -1.56E-01, -5.79E-04,
                       -0.690,  -0.465,  -0.002],	#0.794
             [-3.92E+00, 1.99E+00, -1.31E-01, -2.05E+00, 1.42E-01,
                  -7.82E-01, 4.30E-02,  7.88E-01, -1.59E-01, -6.95E-04,
                       -0.670,  -0.480,  -0.031],	#0.629
             [-3.22E+00, 1.83E+00, -1.20E-01, -2.02E+00, 1.34E-01,
                  -8.13E-01, 4.44E-02,  8.84E-01, -1.75E-01, -7.70E-04,
                       -0.600,  -0.495,  -0.060],	#0.500
             [-2.44E+00, 1.65E+00, -1.08E-01, -2.05E+00, 1.36E-01,
                  -8.43E-01, 4.48E-02,  7.39E-01, -1.56E-01, -8.51E-04,
                       -0.500,  -0.508,  -0.095],	#0.397
             [-1.72E+00, 1.48E+00, -9.74E-02, -2.08E+00, 1.38E-01,
                  -8.89E-01, 4.87E-02,  6.10E-01, -1.39E-01, -9.54E-04,
                       -0.445,  -0.513,  -0.130],	#0.315
             [-1.12E+00, 1.34E+00, -8.72E-02, -2.08E+00, 1.35E-01,
                  -9.71E-01, 5.63E-02,  6.14E-01, -1.43E-01, -1.06E-03,
                       -0.390,  -0.518,  -0.160],	#0.251
             [-6.15E-01, 1.23E+00, -7.89E-02, -2.09E+00, 1.31E-01,
                  -1.12E+00, 6.79E-02,  6.06E-01, -1.46E-01, -1.13E-03,
                       -0.306,  -0.521,  -0.185],	#0.199
             [-1.46E-01, 1.12E+00, -7.14E-02, -2.12E+00, 1.30E-01,
                  -1.30E+00, 8.31E-02,  5.62E-01, -1.44E-01, -1.18E-03,
                       -0.280,  -0.528,  -0.185],	#0.158
             [ 2.14E-01, 1.05E+00, -6.66E-02, -2.15E+00, 1.30E-01,
                  -1.61E+00, 1.05E-01,  4.27E-01, -1.30E-01, -1.15E-03,
                       -0.260,  -0.560,  -0.140],	#0.125
             [ 4.80E-01, 1.02E+00, -6.40E-02, -2.20E+00, 1.27E-01,
                  -2.01E+00, 1.33E-01,  3.37E-01, -1.27E-01, -1.05E-03,
                       -0.250,  -0.595,  -0.132],	#0.100
             [ 6.91E-01, 9.97E-01, -6.28E-02, -2.26E+00, 1.25E-01,
                  -2.49E+00, 1.64E-01,  2.14E-01, -1.21E-01, -8.47E-04,
                       -0.232,  -0.637,  -0.117],	#0.079
             [ 9.11E-01, 9.80E-01, -6.21E-02, -2.36E+00, 1.26E-01,
                  -2.97E+00, 1.91E-01,  1.07E-01, -1.17E-01, -5.79E-04,
                       -0.249,  -0.642,  -0.105],	#0.063
             [ 1.11E+00, 9.72E-01, -6.20E-02, -2.47E+00, 1.28E-01,
                  -3.39E+00, 2.14E-01, -1.39E-01, -9.84E-02, -3.17E-04,
                       -0.286,  -0.643,  -0.105],	#0.050
             [ 1.26E+00, 9.68E-01, -6.23E-02, -2.58E+00, 1.32E-01,
                  -3.64E+00, 2.28E-01, -3.51E-01, -8.13E-02, -1.23E-04,
                       -0.314,  -0.609,  -0.105],	#0.040
             [ 1.44E+00, 9.59E-01, -6.28E-02, -2.71E+00, 1.40E-01,
                  -3.73E+00, 2.34E-01, -5.43E-01, -6.45E-02, -3.23E-05,
                       -0.322,  -0.618,  -0.108],	#0.031
             [ 1.52E+00, 9.60E-01, -6.35E-02, -2.81E+00, 1.46E-01,
                  -3.65E+00, 2.36E-01, -6.54E-01, -5.50E-02, -4.85E-05,
                       -0.330,  -0.624,  -0.115],	#0.025
             [ 9.07E-01, 9.83E-01, -6.60E-02, -2.70E+00, 1.59E-01,
                  -2.80E+00, 2.12E-01, -3.01E-01, -6.53E-02, -4.48E-04,
                       -0.361,  -0.641,  -0.144],	#0.010
             [ 9.07E-01, 9.83E-01, -6.60E-02, -2.70E+00, 1.59E-01,
                  -2.80E+00, 2.12E-01, -3.01E-01, -6.53E-02, -4.48E-04,
                       -0.361,  -0.641,  -0.144]])	#0.000
# convert to dim = (#coefficients, #periods)
Atkinson06_coefficient = tmp.transpose()
Atkinson06_coefficient_pga = reshape(Atkinson06_coefficient[:,-1], (-1,1,1,1))
del tmp

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

gound_motion_init['Atkinson06_bedrock'] = [Atkinson06_bedrock_distribution,
                                           Atkinson06_magnitude_type,
                                           Atkinson06_distance_type,
                                           Atkinson06_coefficient,
                                           Atkinson06_coefficient_period,
                                           Atkinson06_interpolation,
                                           Atkinson06_sigma_coefficient,
                                           Atkinson06_sigma_coefficient_period,
                                           Atkinson06_interpolation]

gound_motion_init['Atkinson06_soil'] = [Atkinson06_soil_distribution,
                                        Atkinson06_magnitude_type,
                                        Atkinson06_distance_type,
                                        Atkinson06_coefficient,
                                        Atkinson06_coefficient_period,
                                        Atkinson06_interpolation,
                                        Atkinson06_sigma_coefficient,
                                        Atkinson06_sigma_coefficient_period,
                                        Atkinson06_interpolation]

##################  End of Atkinson06 bedrock & soil models  ###################

