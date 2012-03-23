"""

  Author:  Duncan Gray, duncan.gray@ga.gov.au
  
  Title: scaling_functions.py

  Description: Calculations focusing on converting Mw to rupture event area
  or width.  This is where the scaling functions are kept.
  
  Note, these functions except **kwargs so parameters that are needed for
  some scaling rules, but not others, ccan be passed in.
  
  Version: $Revision: 995 $
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-06-30 11:51:34 +1000 (Tue, 30 Jun 2009) $

  Copyright 2007 by Geoscience Australia
"""

import numpy as np
from scipy import vectorize, sqrt, sin, minimum, pi, array, tile, where, \
    log10

################  modified_Wells_and_Coppersmith_94  ############################

def modified_Wells_and_Coppersmith_94_rup_area(Mw, **kwargs):
    """
    returns: the rupture area, km2.
    """
    return 10.**(Mw-4.02)

def modified_Wells_and_Coppersmith_94_rup_width(dip, Mw, area, max_rup_width,
                                                **kwargs):
    """    
    # FIXME This function needs a reference.
    
    parameters:
      area: the rupture area, km2
    
    returns:
      the rupture width, km.
    """
    # This is to avoid complex numbers,
    # Which effect the type of width e.g. end up with  1.00000000+0.j madness.
    Mw_mod = where(Mw <= 5.5, 5.5, Mw)  
    f = where(Mw > 5.5, sqrt(sqrt(1+2*(Mw_mod-5.5)*sin(dip*pi/180.)))**-1, 1.0)
    
    width = f*sqrt(area)
    if max_rup_width is not None:
        return minimum(f*sqrt(area),max_rup_width)
    else:
        return f*sqrt(area)


def Wells_and_Coppersmith_94_rup_area(Mw, **kwargs):
    """Calculate the rupture area.

    parameters:
    Mw: magnitudes of the ruptures
    scaling_fault_type from kwargs: fault type eg 'reverse'

    returns: the rupture area, km2.
    """
    fault_type = kwargs['scaling_fault_type']
    if fault_type == "normal":
        area = 10**(-2.87+0.82*Mw)
    elif fault_type == "reverse":
        area = 10**(-3.99+0.98*Mw)
    elif fault_type== "strike_slip":
        area = 10**(-3.42+0.90*Mw)
    elif fault_type== "unspecified":
        area = 10**(-3.497+0.91*Mw)
    else:
        area = 10**(-3.497+0.91*Mw)
    return area

    
def Wells_and_Coppersmith_94_rup_width(Mw, **kwargs):
    """Calculate the rupture width.

    parameters:
    Mw: magnitudes of the ruptures
    scaling_fault_type from kwargs: fault type eg 'reverse'

    returns: the rupture area, km2.
    """
    fault_type = kwargs['scaling_fault_type']
    if fault_type == "normal":
        widthWC = 10**(-1.14+(0.35*Mw))
    elif fault_type == "reverse":
        widthWC = 10**(-1.61+(0.41*Mw))
    elif fault_type== "strike_slip":
        widthWC = 10**(-0.76+(0.27*Mw))
    elif fault_type== "unspecified":
        widthWC = 10**(-1.01+(0.32*Mw))
    else:
        widthWC = 10**(-1.01+(0.32*Mw))
    return widthWC

    
def Leonard_SCR_rup_area(Mw, **kwargs):
    """
    From:
    Earthquake Fault Scaling; Self-Consistent relating of Rupture lenght
    width, average Displacement.
    Author: Mark Leonard
    
    returns: the rupture area, km2.
    """
    return 10.**(Mw-4.183333333333333333)
    

def Leonard_SCR_rup_width(dip, Mw, area, max_rup_width,
                                                **kwargs):
    """
    From:
    Earthquake Fault Scaling; Self-Consistent relating of Rupture lenght
    width, average Displacement.
    Author: Mark Leonard
    
    parameters:
      area: the rupture area, km2
    
    returns:
      the rupture width, km.
    """
    
    # First the Length is calculated
    e, f = Leonard_SCR_constants(Mw)
    length = 10.**(e*Mw + f) # length is in km
    if area is None:
        area = Leonard_SCR_rup_area(Mw)
    width = area/length
       
    if max_rup_width is not None:
        return minimum(width,max_rup_width)
    else:
        return width
        
        
def Leonard_SCR_constants(Mw):
    """
    From:
    Earthquake Fault Scaling; Self-Consistent relating of Rupture length
    width, average Displacement.
    Author: Mark Leonard
    
    returns:
      e, f - constants used to calculate the rupture length.
      
    """
    # Scale it
    a = where(Mw >  4.975, 2.5, 3.0)
    b = where(Mw >  4.975, 8.08, 6.39)
    
    d = 1.5
    c = 6.07
    
    e =d/a
    f = (d*c-b)/a - 3.0
    
    return e, f


def PEER_rup_area(Mw, **kwargs):
    """
    Returns 1 km^2 to standardise on area for replication of results from 
    Verification of Probabalistic Seismic Hazard Analysis Computer Programs
    Thomas et al. (2010)
    Pacific Earthquake Engineering Research Center (PEER)
    """
    return 1.
    

def PEER_rup_width(dip, Mw, area, max_rup_width, **kwargs):
    """
    Returns 1 km to standardise on area for replication of results from 
    Verification of Probabalistic Seismic Hazard Analysis Computer Programs
    Thomas et al. (2010)
    Pacific Earthquake Engineering Research Center (PEER)
    """
    return 1.