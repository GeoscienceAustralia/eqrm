"""
 Title: gound_motion_initerface.py
 
  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, duncan.gray@ga.gov.au
           
  Description:
Ground motion functions that have not found a good home

  Version: $Revision: 914 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-04-01 11:11:47 +1100 (Wed, 01 Apr 2009) $
  
  Copyright 2007 by Geoscience Australia
"""

from scipy import asarray
from interp import interp

def linear_interpolation(new_period,coefficients,old_period):
    """
    linearly interpolate (or extrapolate) coefficients as a function of period
    """
    new_c=[]
    for c in coefficients:
        new_c.append(interp(new_period,c,old_period,
                            extrapolate_high=False,extrapolate_low=False))
    new_c=asarray(new_c)
    return new_c


def Australian_standard_model(periods):
    """
    FIXME: This needs a reference and more of an explanation
    """
    
    T1=0.1
    T2=0.3
    T3=0.7
    T4=3.0
    
    P1=1.0
    P2=1.92
    P3=0.82
    P4=0.045

    b1 = (periods<=T1)
    b2 = (periods>T1) * (periods<=T2)
    b3 = (periods>T2) * (periods<=T3)
    b4 = (periods>T3)
    
    S1 = P1+(P2-P1)/T1*periods #linear
    
    periods=periods-(1*(periods==0.0)) # get rid of div0 errors
    # this comes after the S1 calculation, so it doesn't mess up S1
    
    S2 = P2+0*periods # flat
    S3 = (P3/periods)*T3 # 1/T
    S4 = (P4/(periods*periods))*(T4*T4); # 1/T^2

    c = (b1*S1 + b2*S2 + b3*S3 + b4*S4)
    return c
    
def Australian_standard_model_interpolation(new_period,c,old_period):
    """
    Scale c to the Australian standard model at new_period.

    old_period is not used, but is part of the interpolation interface.

    FIXME: What is c?
    """
    new_period=asarray(new_period)
    c=asarray(c)
    new_c=Australian_standard_model(new_period)*c
    return new_c

