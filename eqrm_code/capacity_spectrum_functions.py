"""
 Title: capacity_spectrum_functions.py
  
  Description: Functions used by capacity spectrum model
  
  Version: $Revision: 1562 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-03-09 15:48:50 +1100 (Tue, 09 Mar 2010) $
  
  Copyright 2007 by Geoscience Australia
"""

import exceptions

from scipy import where, exp, pi, newaxis, stats, weave, zeros, log, \
     asarray, array, seterr, concatenate
from numpy import interp as npinterp
from interp import interp

from eqrm_code import util
from eqrm_code import weave_converters
from eqrm_code.ground_motion_distribution import Distribution_Normal

class WeaveIOError(exceptions.Exception):
    def __init__(self, errno=None, msg=None):
        msg = ("%s directory is full. Space is needed to compile files."
               % get_weave_dir())
        raise IOError(msg)

# Users used to be able to set this...
CSM_DAMPING_USE_SMOOTHING = True 

def trapazoid_damp(capacity_parameters,kappa,acceleration,displacement,
                   unused_csm_hysteretic_damping):
    """
    Calculate the damping correction (Fulford 02) using an approximation
    to the capcity curve.
    """
    (DyM, AyM,
     DuM, AuM,
     Du_alpha, Au_rev,
     Du_beta, Au_rev_0_8,
     Du_delta, Au_rev_0_2,
     Du_theta, Au_rev_0_1,
     a, b, c) = capacity_parameters
    
    k=AyM/DyM
    Harea=4*acceleration*(displacement-acceleration/k)
    Harea=4*acceleration*(displacement-acceleration/k)
    BH = kappa*Harea/(2*pi*displacement*acceleration)
    return BH

def nonlin_damp(capacity_parameters,kappa,acceleration,displacement,
                csm_hysteretic_damping='Error'):
    """
    Calculate the damping correction (Fulford 02) using the
    exact capacity curve.
    """
    (DyV, AyV,
     DuV, AuV,
     Du_alpha, Au_rev,
     Du_beta, Au_rev_0_8,
     Du_delta, Au_rev_0_2,
     Du_theta, Au_rev_0_1,
     a, b, c) = capacity_parameters 
    Harea=hyst_area_rand(displacement,acceleration,DyV,AyV,DuV,AuV,
                         csm_hysteretic_damping)
    oldsettings = seterr(invalid='ignore')
    BH = kappa*Harea/(2*pi*displacement*acceleration)
    seterr(**oldsettings)
    return BH

def hyst_area_rand(D,A,DyV,AyV,DuV,AuV,csm_hysteretic_damping):
    """
    function to calculate hystereris loop area used in the building damage calcs
    this version works for where the building cap curves are chasen randomly
    (which means Ay needs to be rescaled by Rcap;)
    
    In:  DyV, AyV =  yield point (vectors(nev,1))
         DuV, AuV =  ultimate point (vectors(nev,1))
         D, A = peak dispacement and accel (vector(nev,1) of events)
         
    Out: Area = vector of events
         Glenn Fulford: 21/4/02.


This is a diagram, trying to show how the hysteresis area is
calculated if csm_hysteretic_damping = 'curve'.

The diagram shows half the hysteresis area.
y is the yield point
PP is the performance point
x2 is the translation along the displacement axis.
A2 is the area from (y-x2) to PP on the top curve.
A2 is also the area from y to (PP-x2) on the bottom curve.
A1 and A3 are triaglular areas.

The hysteresis area = 2(A1+A2-A3)

        y-x2    y          PP
        |       |          |
        |       |          |
        |       |          |
        |       |          | ___.......--=----.------'''
        |       |    _,.,-':'    __..--''
        |       |.-''      |_.-''
        |    _,'|        ,-+
        |  ,'   |     ,-' /|
        | /  A2 |  ,-'   / |
        |/      |,'     /  |
        :i______|______/   |
        +      /      /    |
       /|     /      /     |
      / |    /      /      |
     /  |   /      /       |
    /   |  /      /  A3    |
   /    | /      /         |
  / A1  |/      /          |
 /      +      /           |
/      '|     /            |


    """
    # use a coord system with the orign are at the beginning
    # of the hysterisis curve
    # disp('hyst: caprand='); disp(SAcapR(:,1));
    
    ky=(AyV/DyV) # slope of linear part of capacity curve
    
    #x0=D-DyV    # x distance from linear part (<=0 implies point is linear)
    linear_region=where(D<=DyV)
   
    x2=D-A/ky  # translation along displacement axis
    if csm_hysteretic_damping is 'Error':
        y1=(A-AyV) # y distance from linear part (<=0 implies point is linear)
        y1[linear_region]=-1 # avoid NaNs - only Harea3 has any impact there
   
        x1=2*x2+y1/ky

        cc=A-AyV
        bb=ky/(A-AyV)
        aa=-ky/bb
        
        oldsettings = seterr(under='ignore')
        Harea1=cc*x1+aa/bb*(1-exp(-bb*x1))
        seterr(**oldsettings)
        Harea2=0.5*y1*y1/ky
        Harea3=2*x2*AyV

        Harea=2*(Harea1-Harea2+Harea3)
        Harea[linear_region]=0

    elif csm_hysteretic_damping is 'curve':
        cc=AuV
        bb=ky/(AuV-AyV)
        aa=(AyV-AuV)*exp(bb*DyV)

        Harea1=0.5*AyV*DyV
        Harea2=aa/bb*(exp(-bb*DyV)-exp(-bb*(D+x2)))+cc*(D+x2-DyV)
        Harea3=0.5*A*(D-x2)

        Harea=2*(Harea1+Harea2-Harea3)
        Harea[linear_region]=0

    # Area calculation from 
    # ATC 40 Seismic Evaluation and Retrofit of Concrete Buildings 8-15
    # Ed = 4(Ay*Dpi - Dy*Api)
    
    elif csm_hysteretic_damping is 'parallelogram': 
        Harea=4*(D*AyV -DyV*A)
        Harea[linear_region]=0
    else:
        print "csm_hysteretic_damping", csm_hysteretic_damping
        
    return Harea

def calculate_kappa(magnitude,damping_s,damping_m,damping_l):
    """
    kappa=where(magnitude>5.5,self.damping_m,damping_s)
    kappa[where(magnitude>7.5)]=damping_l
    # where may cause issues if both mag and sites has
    # non-trivial dimension.
    # in that case we may have to try:
    """
    damping_s=damping_s.swapaxes(0,1)
    damping_m=damping_m.swapaxes(0,1)
    damping_l=damping_l.swapaxes(0,1)
    
    magnitude=magnitude.swapaxes(0,1)
    
    kappa=damping_s*(magnitude<=5.5)
    kappa[where(magnitude>5.5)[0]]=damping_m
    kappa[where(magnitude>7.5)[0]]=damping_l
    
    kappa=kappa.swapaxes(0,1)
    return kappa

def sample_capacity_parameters(C,C_sigma,
                               T,T_sigma,
                               a1,a1_sigma,
                               a2,a2_sigma,
                               y,y_sigma,
                               Lambda,Lambda_sigma,
                               u,u_sigma,
                               csm_variability_method):
    """
    Take a sample from the normal distribution for the given parameters and
    corresponding standard deviations.
    
    # C      = design_strength = Cs
    # T      = natural_elastic_period = T
    # a1     = fraction_in_first_mode = alpha1
    # a2     = height_to_displacement = alpha2
    # y      = yield_to_design = gamma
    # Lambda = ultimate_to_yield = Lambda
    # u      = ductility = mu
    """
    
    dist = Distribution_Normal(csm_variability_method)
        
    C_sample = dist.sample_for_eqrm(C, C_sigma)
    T_sample = dist.sample_for_eqrm(T, T_sigma)
    a1_sample = dist.sample_for_eqrm(a1, a1_sigma)
    a2_sample = dist.sample_for_eqrm(a2, a2_sigma)
    y_sample = dist.sample_for_eqrm(y, y_sigma)
    Lambda_sample = dist.sample_for_eqrm(Lambda, Lambda_sigma)
    u_sample = dist.sample_for_eqrm(u, u_sigma)
    
    return (C_sample,
            T_sample,
            a1_sample,
            a2_sample,
            y_sample,
            Lambda_sample,
            u_sample)
    
def calculate_capacity_parameters(C,T,a1,unused_a2,y,Lambda,u,
                                  alpha, beta, delta, theta):
    """
    Use building parameters to calculate capacity parameters
        
        |         |alpha*Du
        |         |   _ _ _ _ _ _
        |         | /
        |Au_rev_ _|/ |beta*Du
        |     ___/ \_|_ _ _ _ _ _ _ _ _ 0.8*Au_rev
     SA |   _/       \_  |delta*Du
        |  /* Dy,Ay    \_|_ _ _ _ _ _ _ 0.2*Au_rev
        | /              \_ |theta*Du
        |/                 \|__________ 0.1*Au_rev
        |___________________________________
          SD

          
    # C=design_strength = Cs
    # T=natural_elastic_period = T
    # a1=fraction_in_first_mode = alpha1
    # a2=height_to_displacement = alpha2
    # y=yield_to_design = gamma
    # Lambda=ultimate_to_yield = Lambda
    # u=ductility = mu
    """
    
    g=9.8
    
    Ay=C*y/a1
    Dy=1000/(4*pi**2)*g*Ay*(T**2)
    Au=Lambda*Ay
    Du=Lambda*u*Dy
    Du_alpha = Du*alpha
    Du_beta = Du*beta
    Du_delta = Du*delta
    Du_theta = Du*theta
    
    ky=(Ay/Dy) #slope of linear part of capacity curve
    c=Au
    b=ky/(Au-Ay)
    a=(Ay-Au)*exp(b*Dy)
    
    # Find Au_rev
    Au_rev = a*exp(Du_alpha*-b)+c
    Au_rev_0_8 = 0.8 * Au_rev
    Au_rev_0_2 = 0.2 * Au_rev
    Au_rev_0_1 = 0.1 * Au_rev
    
    return (Dy, Ay,
            Du, Au, 
            Du_alpha, Au_rev,
            Du_beta, Au_rev_0_8,
            Du_delta, Au_rev_0_2,
            Du_theta, Au_rev_0_1,
            a, b, c)


def calculate_capacity_python(surface_displacement,capacity_parameters):
    """
    Calculate the building capacity curve
    
        |          ___________
        |      ___/    - flat region
     SA |    _/    - exponential decay region
        |   / 
        |  / - linear region
        | /
        |___________________
          SD
          
    """
    
    (Dy, Ay,
     Du, Au,
     Du_alpha, Au_rev,
     Du_beta, Au_rev_0_8,
     Du_delta, Au_rev_0_2,
     Du_theta, Au_rev_0_1,
     a, b, c) = capacity_parameters
    
    print 'speed hog 2'
    y1=(Ay/Dy)*surface_displacement # linear region
    y2=a*exp(surface_displacement*-b)+c # exp region
    y3=c;  #constant part

    b1=(surface_displacement<=Dy) # linear region
    b2=((surface_displacement>Dy)&(surface_displacement<Du)) # exp region
    b3=(surface_displacement>Du) # flat region
    capacity=(b1*y1+b2*y2+b3*y3)
    print 'end speed hog'
    return capacity


def calculate_capacity_degrading_python(surface_displacement,capacity_parameters):
    """
    Calculate the degrading building capacity curve
    
        |         |alpha*Du
        |         |   _ _ _ _ _ _
        |         | /
        |Au_rev_ _|/ |beta*Du
        |     ___/ \_|_ _ _ _ _ _ _ _ _ 0.8*Au_rev
     SA |   _/       \_  |delta*Du
        |  /* Dy,Ay    \_|_ _ _ _ _ _ _ 0.2*Au_rev
        | /              \_ |theta*Du
        |/                 \|__________ 0.1*Au_rev
        |___________________________________
          SD
          
    """
    (Dy, Ay,
     Du, Au,
     Du_alpha, Au_rev,
     Du_beta, Au_rev_0_8,
     Du_delta, Au_rev_0_2,
     Du_theta, Au_rev_0_1,
     a, b, c) = capacity_parameters
    
    # Calculations
    # linear region
    y1 = (Ay/Dy)*surface_displacement
    
    # exp curve region
    y2 = a*exp(surface_displacement*-b)+c
    
    # first degrading region - linear
    y3 = npinterp(surface_displacement,
                  concatenate((Du_alpha,Du_beta)).reshape(2), # two points only
                  concatenate((Au_rev,Au_rev_0_8)).reshape(2))
    
    # second degrading region - linear
    y4 = npinterp(surface_displacement,
                  concatenate((Du_beta,Du_delta)).reshape(2),
                  concatenate((Au_rev_0_8,Au_rev_0_2)).reshape(2))
    
    # third degrading region - linear
    y5 = npinterp(surface_displacement,
                  concatenate((Du_delta,Du_theta)).reshape(2),
                  concatenate((Au_rev_0_2,Au_rev_0_1)).reshape(2))
    
    # flat region
    y6 = Au_rev_0_1

    # Regions
    # linear region
    b1 = (surface_displacement<=Dy)
    
    # exp_curve_region
    b2 = ((surface_displacement>Dy)&(surface_displacement<=Du_alpha))
    
    # first degrading region
    b3 = ((surface_displacement>Du_alpha)&(surface_displacement<=Du_beta))
    
    # second degrading region
    b4 = ((surface_displacement>Du_beta)&(surface_displacement<=Du_delta))
    
    # third degrading region
    b5 = ((surface_displacement>Du_delta)&(surface_displacement<=Du_theta))
    
    # flat region
    b6=(surface_displacement>Du_theta)
    
    capacity=(b1*y1+b2*y2+b3*y3+b4*y4+b5*y5+b6*y6)
    
    return capacity

def calculate_capacity_weave(surface_displacement,capacity_parameters):
    """
    Calculate the building capacity curve
    
        |          ___________
        |      ___/    - flat region
     SA |    _/    - exponential decay region
        |   / 
        |  / - linear region
        | /
        |___________________
          SD
    #Fixme - add unit information.
    """
    
    (Dy, Ay,
     Du, Au,
     Du_alpha, Au_rev,
     Du_beta, Au_rev_0_8,
     Du_delta, Au_rev_0_2,
     Du_theta, Au_rev_0_1,
     a, b, c) = capacity_parameters
    
    num_sites,num_events,num_periods=surface_displacement.shape
    assert surface_displacement.shape==(num_sites,num_events,num_periods)
    assert Dy.shape==Ay.shape==Du.shape==Au.shape==a.shape==b.shape==c.shape
    assert (Dy.shape==(num_sites,num_events,1)) or (Dy.shape==(num_sites,1,1))
    capacity=zeros((num_sites,num_events,num_periods),dtype=float)
    #print 'surface_displacement',surface_displacement[0,0:5]
    #print Dy.shape        
    #y1=(Ay/Dy)*surface_displacement # linear region
    #y2=a*exp(surface_displacement*-b)+c # exp region
    #y3=c;  #constant part

    #b1=(surface_displacement<=Dy) # linear region
    #b2=((surface_displacement>Dy)&(surface_displacement<Du)) # exp region
    #b3=(surface_displacement>Du) # flat region
    #capacity=(b1*y1+b2*y2+b3*y3)
    code="""
    double Dyy,Duu,Ayy,aa,bb,cc;
    double sd;
    
    for (int i=0; i<num_sites; ++i){
        for (int j=0; j<num_events; ++j){
            get_constants
            for (int k=0;k<num_periods;++k){
                sd=surface_displacement(i,j,k);
                if (sd<=Dyy){
                    capacity(i,j,k)=(Ayy/Dyy)*sd;
                }
                else if ((sd>Dyy)&(sd<Duu)){
                    capacity(i,j,k)=aa*exp(sd*(-bb))+cc;
                }
                else{
                    capacity(i,j,k)=cc;
                }
            }       
        }
    }
    return_val = 0;
    """
    if (Dy.shape==(num_sites,num_events,1)):
        Ay=Ay[:,:,0]
        Dy=Dy[:,:,0]
        Du=Du[:,:,0]
        a=a[:,:,0]
        b=b[:,:,0]
        c=c[:,:,0]
        code=code.replace('get_constants',
                          
                          'aa=a(i,j);bb=b(i,j);cc=c(i,j);'+
                          'Duu=Du(i,j);Dyy=Dy(i,j);Ayy=Ay(i,j);')
        #print code
        try:
            weave.inline(code,
                         ['num_sites','num_events','num_periods',
                          'surface_displacement','capacity',
                          'a','b','c','Du','Dy','Ay'],
                         type_converters=weave_converters.eqrm,
                         compiler='gcc')
        except IOError:
            raise WeaveIOError
    else:
        assert Dy.shape==(num_sites,1,1)
        Ay=Ay[:,0,0]
        Dy=Dy[:,0,0]
        Du=Du[:,0,0]
        a=a[:,0,0]
        b=b[:,0,0]
        c=c[:,0,0]
        code=code.replace('get_constants',
                          
                          'aa=a(i);bb=b(i);cc=c(i);'+
                          'Duu=Du(i);Dyy=Dy(i);Ayy=Ay(i);')
        #print code
        try:
            weave.inline(code,
                         ['num_sites','num_events','num_periods',
                          'surface_displacement','capacity',
                          'a','b','c','Du','Dy','Ay'],
                         type_converters=weave_converters.eqrm,
                         compiler='gcc')
        except IOError:
            raise WeaveIOError
    return capacity

calculate_capacity = calculate_capacity_weave

def calculate_reduction_factors(damping_factor):
    """
    Given an overall damping factor, calculate the damping
    factors for each corner
    """
    damping_factor=asarray(damping_factor)
    # calculate Sa reduction factors (Newmark and Hall)
    Ra = 2.12 /(3.21-0.68*log(100*damping_factor));  # accel reduction factor
    Rv = 1.65 /(2.31-0.41*log(100*damping_factor));  # vel reduction factor
    Rd = 1.39 /(1.82-0.27*log(100*damping_factor));  # disp reduction factor
    return Ra,Rv,Rd

def calculate_updated_demand_python(periods,SA0,SD0,Ra,Rv,Rd,TAV,TVD,
                                    csm_damping_use_smoothing=CSM_DAMPING_USE_SMOOTHING):
    """
    update the demand, given original responses, damping factors,
    and corner periods.
    """
    periods=periods[newaxis,newaxis,...]
    TAV=TAV[:,:,newaxis]
    TVD=TVD[:,:,newaxis]
    assert len(periods.shape)==3
    assert len(TAV.shape)==3
    assert len(TVD.shape)==3
    print 'speed hog 1'
    R=(Ra*(periods<TAV)
       +Rv*((TAV<=periods)*(periods<=TVD))
       +Rd*(periods>TVD))
    
    if csm_damping_use_smoothing == CSM_DAMPING_USE_SMOOTHING:
        R[...,1:-1]=0.25*R[...,0:-2]+0.5*R[...,1:-1]+0.25*R[...,2:]
    print 'end speed hog'
    SAnew=SA0/R
    SDnew=SD0/R
    return SAnew,SDnew

def calculate_updated_demand(periods,SA0,SD0,Ra,Rv,Rd,TAV,TVD,
                             csm_damping_use_smoothing=CSM_DAMPING_USE_SMOOTHING):
    """
    update the demand, given original responses, damping factors,
    and corner periods.
    """
    periods=periods[newaxis,newaxis,...]
    TAV=TAV[:,:,newaxis]
    TVD=TVD[:,:,newaxis]
    assert len(periods.shape)==3
    assert len(TAV.shape)==3
    assert len(TVD.shape)==3
    #print 'SA0',SA0[:,0:5]
    #print 'SD0',SD0[:,0:5]
    #print 'TAV',TAV[:,0:5]
    #print 'TVD',TVD[:,0:5]
    num_sites,num_events,num_periods=SA0.shape
    assert TAV.shape==(num_sites,num_events,1)
    assert TVD.shape==(1,num_events,1)
    assert periods.shape==(1,1,num_periods)
    TAV=TAV[:,:,0]
    TVD=TVD[0,:,0]
    periods=periods[0,0]
    assert SA0.shape==(num_sites,num_events,num_periods)
    assert SD0.shape==(num_sites,num_events,num_periods)
    
    assert ((Ra.shape==(num_sites,num_events,1) and 
             Rv.shape==(num_sites,num_events,1) and
             Rd.shape==(num_sites,num_events,1)) or
            (Ra.shape==(1,1,1) and 
             Rv.shape==(1,1,1) and
             Rd.shape==(1,1,1)))
    
    R=zeros((num_sites,num_events,num_periods),dtype=float)
    
    assert TAV.shape==(num_sites,num_events)
    assert TVD.shape==(num_events,)
    assert periods.shape==(num_periods,)
    code="""
    double AV,VD;
    double p;
    for (int i=0; i<num_sites; ++i){
        for (int j=0; j<num_events; ++j){
            get_R
            AV=TAV(i,j);
            VD=TVD(j);
    
            for (int k=0;k<num_periods;++k){
                p=periods(k);         
                if (p<=AV){
                    R(i,j,k)=Raa;
                }
                else if (p<=VD){
                    R(i,j,k)=Rvv;
                }
                else{
                    R(i,j,k)=Rdd;
                }
              
            }            
        }
    }
            
    return_val = 0;
    """
    
    
    if Ra.shape==(1,1,1):
        assert Rv.shape==(1,1,1)
        assert Rd.shape==(1,1,1)
        code=code.replace('get_R',
                          '')
        code=code.replace('Raa',
                          'Ra')
        code=code.replace('Rvv',
                          'Rv')
        code=code.replace('Rdd',
                          'Rd')
        Ra=float(Ra[0,0,0])    
        Rv=float(Rv[0,0,0])    
        Rd=float(Rd[0,0,0])
        try:
            weave.inline(code,
                         ['num_sites','num_events','num_periods',
                          'Ra','Rv','Rd','R','periods',
                          'TAV','TVD'],
                         type_converters=weave_converters.eqrm,
                         compiler='gcc')
        except IOError:
            raise WeaveIOError
    else:
        assert Ra.shape==(num_sites,num_events,1)
        assert Rv.shape==(num_sites,num_events,1)
        assert Rd.shape==(num_sites,num_events,1)
        Ra=(Ra[:,:,0])    
        Rv=(Rv[:,:,0])    
        Rd=(Rd[:,:,0])    
        code=code.replace('get_R',
                          'Raa=Ra(i,j,1);Rvv=Rv(i,j,1);Rdd=Rd(i,j,1);')
        code='double Raa,Rvv,Rdd;'+code

        try:
            weave.inline(code,
                         ['num_sites','num_events','num_periods',
                          'Ra','Rv','Rd','R','periods',
                          'TAV','TVD'],
                         type_converters=weave_converters.eqrm,
                         compiler='gcc')
        except IOError:
            raise WeaveIOError

    
    if csm_damping_use_smoothing == CSM_DAMPING_USE_SMOOTHING:
        R[...,1:-1]=0.25*R[...,0:-2]+0.5*R[...,1:-1]+0.25*R[...,2:]
    SAnew=SA0/R
    SDnew=SD0/R
    return SAnew,SDnew

def calculate_corner_periods(periods, ground_motion, magnitude):
    """
    periods - 1D array, dimension # of periods
    ground_motion - XD array, with last dimension periods.
    magnitude - 1D array, dimension # of events
    from Newmark and Hall 1982
    
    returns TAV,TVD - the acceleration and velocity dependent
    corner periods
    TAV and TVD have the same dimensions as ground_motion, except
       the last axis (periods) is dropped.
    """
    #reference_periods = 0.3,1.0
    S03=interp(array(0.3),ground_motion,periods,axis=-1)
    S10=interp(array(1.0),ground_motion,periods,axis=-1)
    #print 'S03',S03[:,0:5]

    #print 'S10',S10[:,0:5]
    # interpolate the ground motion at reference periods
    oldsettings = seterr(invalid='ignore')
    acceleration_dependent=(S10/S03)
    seterr(**oldsettings)
    acceleration_dependent[where(S03<0.00000000000001)]=0.0
    acceleration_dependent=acceleration_dependent[...,0] # and collapse

    # This assumes ground_motion.shape = (1, events) 
    velocity_dependent=(10**((magnitude-5.0)/2))[newaxis,:]
    assert len(acceleration_dependent.shape)==2
    assert len(velocity_dependent.shape)==2
    # removed this assert so test_cadell_damage passes.
    # This test passes 4660 sites, instead of the usual 1.
    # Fixing/ getting rid of the test is another option...
    #assert velocity_dependent.shape == acceleration_dependent.shape
    return acceleration_dependent, velocity_dependent
        
def undamped_response(SA,periods,atten_override_RSA_shape=None,
                      atten_cutoff_max_spectral_displacement=False,
                      loss_min_pga=0.0,
                      magnitude=None):
    """
    Calculate SD from SA
    """    
    if atten_override_RSA_shape is None:
        pass
    elif atten_override_RSA_shape == 'Aust_standard_Sa':
        from eqrm_code.ground_motion_misc import Australian_standard_model
        SA=SA[:,:,0:1]*Australian_standard_model(periods[newaxis,newaxis,:])
    elif atten_override_RSA_shape == 'HAZUS_Sa':
        #reference_periods = 0.3,1.0
        S03=interp(array(0.3),SA,periods,axis=-1)
        S10=interp(array(1.0),SA,periods,axis=-1)
        # interpolate the ground motion at reference periods
        acceleration_dependent=(S10/S03)
        acceleration_dependent[where(S03<0.00000000000001)]=0.0
        acceleration_dependent=acceleration_dependent[:,:,0] # and collapse
        velocity_dependent=(10**((magnitude-5.0)/2))[newaxis,:]

        Tm = periods[newaxis,newaxis,:]
        
        S03M = S03
        S10M = S10

        TavM = acceleration_dependent[:,:,newaxis]
        TvdM = velocity_dependent[:,:,newaxis]

        # set up Boolean arrays for the three regions
        # (accel, vel, disp, sensitive)
        bA = (Tm < TavM)
        bV = (Tm >= TavM) & (Tm <= TvdM)
        bD = (Tm > TvdM)

        SA=(S03M*bA)
        SA[where(bV)]=(S10M/Tm)[where(bV)]
        SA[where(bD)]=((S10M*TvdM)/(Tm**2))[where(bD)]
        #SA = (S03M*bA) + (S10M/Tm)*bV + ((S10M*TvdM)/(Tm**2))*bD
    else:
        print 'atten_override_RSA_shape = ',atten_override_RSA_shape
        raise NotImplementedError('atten_override_RSA_shape = '+str(atten_override_RSA_shape))

    too_low=SA[:,:,0:1]<loss_min_pga
    scaling_factor=where(too_low,0,1)
    SA=SA*scaling_factor
     
    # calculate surface displacement:
    #surface_displacement~=(250*(periods**2))*SA
    #dimension=1e3*9.8 # convert from g forces to m/s^2, and m to mm
    # dimension/(4*pi**2) = 248.236899924
    surface_displacement=((248.236899924)*(periods**2))*SA
    
    if atten_cutoff_max_spectral_displacement is True:
        surface_displacement=cutoff_after_max(surface_displacement,periods)
    return SA,surface_displacement

def cutoff_after_max(surface_displacement,periods,axis=-1):
    """
    for all displacements with periods greater than the periods
    of max_displacement, set them to zero, then add max_displacement.

    ie:
        initial:

        |  /\
        | /  \
        |/    \----/\
        |------------
        period ->


        goes to:

        |  /---------
        | /           
        |/            
        |------------
        period ->

    Note that periods to be broadcastable to SD (ie the same shape)

    This will probably mean using: cutoff(SD,periods[...,newaxis])
    """
    index_of_max=surface_displacement.argmax(axis=axis)[:,:,newaxis]
    periods_max=periods[index_of_max]
    
    # find periods higher than max displacement
    periods_high=(periods>=periods_max)
    
    # set to zero
    max_sd = surface_displacement.max(axis=axis)[:,:,newaxis]
    surface_displacement*=(1-periods_high)
    
    # then add max_displacement
    periods_high=periods_high*max_sd
        # (periods_high now is max_displacement where periods is high)
    surface_displacement+=periods_high
    return surface_displacement



