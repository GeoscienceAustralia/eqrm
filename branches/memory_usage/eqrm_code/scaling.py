"""

  Author:  Duncan Gray, duncan.gray@ga.gov.au
  
  Title: scaling.py

  Description: The interface to the scaling functions.

  Use the two functions;
    calc_area
    calc_length
    
  to calculate the area or the length, using the selected scaling rule.
  The rule to use is usaully defined in an xml file, along with the faulting
  type.

  
  
  Version: $Revision: 995 $
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-06-30 11:51:34 +1000 (Tue, 30 Jun 2009) $

  Copyright 2007 by Geoscience Australia
"""

from eqrm_code import scaling_functions
import string
import copy

NAME_BEGINNING = {'WEL':'Wells_and_Coppersmith_94',
                  'MOD':'modified_Wells_and_Coppersmith_94'}
def scaling_calc_rup_area(Mw, scaling_dic):
    """
    Calculate the rupture area, using a supplied scaling rule, given an Mw and
    various other parameters.
    
    parameters:
    Mw: magnitudes of the ruptures
    scaling_dic: a dictionary with various scaling parameters;
      scaling_rule: The name of the scaling rule to use. Currently only
        'Wells_and_Coppersmith_94' or 'modified_Wells_and_Coppersmith_94'.
        'Wells_and_Coppersmith_94' needs the key 'scaling_fault_type' defined.
    """
    key = string.upper(scaling_dic['scaling_rule'][:3])
    if NAME_BEGINNING.has_key(key):
        scaling_dic['scaling_rule'] = NAME_BEGINNING[key]
    func_name = scaling_dic['scaling_rule'] + '_rup_area'
    
    scaling_dic['Mw'] = Mw
    func_pointer = getattr(scaling_functions, func_name)
    rup_area = apply(func_pointer, [], scaling_dic)
    return rup_area

def scaling_calc_rup_width(Mw, scaling_dic, dip, rup_area=None,
                           max_rup_width=None):
    
    """
    Calculate the rupture width, using a supplied scaling rule,
    given an Mw and various other parameters.
    
    parameters:
    dip: Not all the scaling rules use dip, but some do, so it has to be
      used at the interface.
    Mw: magnitudes of the ruptures
    scaling_dic: a dictionary with various scaling parameters;
      scaling_rule: The name of the scaling rule to use. Currently only
        'Wells_and_Coppersmith_94' or 'modified_Wells_and_Coppersmith_94'.
        'Wells_and_Coppersmith_94' needs the key 'scaling_fault_type' defined.
    rup_area: The rupture area, km2
    max_rup_width: The maximum width possible, km.
        
    """
    func_name = scaling_dic['scaling_rule'] + '_rup_width'
    para_dic = copy.copy(scaling_dic)
    para_dic['Mw'] = Mw
    para_dic['dip'] = dip
    para_dic['area'] = rup_area
    para_dic['max_rup_width'] = max_rup_width
    func_pointer = getattr(scaling_functions, func_name)
    rup_width = apply(func_pointer, [], para_dic)
    return rup_width

