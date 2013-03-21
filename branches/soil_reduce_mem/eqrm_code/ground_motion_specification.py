"""
 Title: ground_motion_specification.py
 
  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, duncan.gray@ga.gov.au
           
  Description:  Specifies a ground motion model.

  Version: $Revision: 1005 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-07-08 16:21:56 +1000 (Wed, 08 Jul 2009) $
  
  Copyright 2007 by Geoscience Australia
"""

from scipy import allclose, asarray

from eqrm_code.ground_motion_interface import ground_motion_init

class Ground_motion_specification(object):
    """
    A specification class.
    
    This class determines the level of motion observed at a distance
    from an event given a event magnitude and depth. The level of
    motion is defined as the responce spectral acceleration (RSA), in
    units of g.  The distribution function is called to determine the
    RSA.
    
    Additionally, given an array of periods, calculate the coefficients and
    sigma coefficients for the periods.

    The specific information of each ground motion model is specified in
    ground_motion_interface.
    
    """
    
    def __init__(self, ground_motion_model_name):
        try:
            gm_args = ground_motion_init[ground_motion_model_name]
        except KeyError:
            raise KeyError, \
                  'Invalid ground motion model name: %s' \
                  %ground_motion_model_name
        self._set_interface_values(*gm_args)
        self.ground_motion_model_name = ground_motion_model_name
        
    def _set_interface_values(self,distribution,magnitude_type,
                              distance_types,
                              coefficient,coefficient_period,
                              coefficient_interpolation,
                              sigma_coefficient,sigma_coefficient_period,
                              sigma_coefficient_interpolation,
                              uses_Vs30):
        
        self.distribution = distribution
        self.magnitude_type = magnitude_type
        self.distance_types = distance_types
        
        self.coefficient = asarray(coefficient)
        self.coefficient_period = asarray(coefficient_period)
        self.coefficient_interpolation = coefficient_interpolation
        
        self.sigma_coefficient = asarray(sigma_coefficient)
        self.sigma_coefficient_period = asarray(sigma_coefficient_period)
        self.sigma_coefficient_interpolation = sigma_coefficient_interpolation

        self.uses_Vs30 = uses_Vs30
           
    
    def calc_coefficient(self, periods):
        return self.coefficient_interpolation(periods,
                                       self.coefficient,
                                       self.coefficient_period)


    def calc_sigma_coefficient(self, periods):
        return self.sigma_coefficient_interpolation(periods,
                                       self.sigma_coefficient,
                                       self.sigma_coefficient_period)
