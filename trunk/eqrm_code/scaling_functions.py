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


from scipy import vectorize, sqrt, sin, minimum, pi, array, tile, where

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
    f = where(Mw > 5.5, sqrt(sqrt(1+2*(Mw-5.5)*sin(dip*pi/180.)))**-1, 1.0)
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
