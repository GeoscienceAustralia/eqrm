"""
 Title: capacity_spectrum_model.py
  
  Description: Used to model the building damage.
  
  Version: $Revision: 1562 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-03-09 15:48:50 +1100 (Tue, 09 Mar 2010) $
  
  Copyright 2007 by Geoscience Australia
"""

from scipy import newaxis, where

from eqrm_code.util import dict2csv      
from eqrm_code.equivalent_linear_solver import solve
from eqrm_code.capacity_spectrum_functions import \
     calculate_capacity_parameters, \
     calculate_kappa, undamped_response, calculate_corner_periods, \
     calculate_reduction_factors, calculate_updated_demand, \
     calculate_capacity, nonlin_damp, CSM_DAMPING_USE_SMOOTHING

CSM_DAMPING_REGIMES_USE_ALL = 0
CSM_DAMPING_REGIMES_USE_RA_RV = 1
CSM_DAMPING_REGIMES_USE_RV = 2

CSM_DAMPING_MODIFY_TAV = True # TRUE 0 
CSM_DAMPING_DO_NOT_MODIFY_TAV = False # FALSE 1


class Capacity_spectrum_model(object):
    def __init__(self,
                 periods=None,
                 magnitudes=None,
                 building_parameters=None,
                 atten_rescale_curve_from_pga=None,
                 atten_cutoff_max_spectral_displacement=False,
                 loss_min_pga=0.0,
                 csm_damping_regimes=CSM_DAMPING_REGIMES_USE_ALL,
                 csm_damping_modify_Tav=CSM_DAMPING_MODIFY_TAV,
                 csm_damping_use_smoothing=CSM_DAMPING_USE_SMOOTHING,
                 csm_hysteretic_damping='Error',
                 rtol=.01,
                 csm_damping_max_iterations=7,
                 sdtcap=.3,
                 csm_use_variability=False,
                 csm_variability_method=1):
        """
Usage:

capacity_spectrum_model=Capacity_spectrum_model(
    periods,magnitudes,building_parameters,structure_indicies,
    cutoff_at_max=False,
    smooth_damping=True)
    
There are additional parameters that may be set (examples below).


# set up parameters in capacity model (optional, can be changed after __init__)
capacity_spectrum_model.use_displacement_corner_period=True
capacity_spectrum_model.damp_corner_periods=True
capacity_spectrum_model.use_exact_area=True
capacity_spectrum_model.rtol=0.01
capacity_spectrum_model.csm_damping_max_iterations=7

To get the building response, call: csm.building_response(self,site_key,SA)

periods,magnitudes,building_parameters,Btypes,cutoff_at_max and smooth_damping
should NOT be set after initialization - read __init__ for reasons.
        Set up derived parameters (the capacity curve parameters,
        and the damping parameter kappa), calculate the initial
        response, and remember periods.
        """
        self.sdtcap=sdtcap
        self.periods=periods
        self.magnitudes=magnitudes


        self.csm_damping_regimes=csm_damping_regimes
        self.csm_damping_modify_Tav=csm_damping_modify_Tav
        self.csm_damping_use_smoothing=csm_damping_use_smoothing
        self.csm_hysteretic_damping=csm_hysteretic_damping
        self.rtol=rtol
        self.csm_damping_max_iterations=csm_damping_max_iterations

        self.csm_use_variability=csm_use_variability
        self.csm_variability_method=csm_variability_method

        self.atten_rescale_curve_from_pga=atten_rescale_curve_from_pga
        self.atten_cutoff_max_spectral_displacement=atten_cutoff_max_spectral_displacement
        self.loss_min_pga=loss_min_pga

        # get values for all sites.
        # Other methods will set self.capacity_parameters
        # for specific sites from self.all_capacity_parameters[site_index]
        # using self.set_building_type_index(index)
        
        self.capacity_parameters=self._calculate_parameters(
            building_parameters,magnitudes)
        
        self.kappa=self._calculate_kappa(building_parameters,magnitudes)
        self.kappa=self.kappa[:,:,newaxis]
        
        self.initial_damping=building_parameters['damping_Be'][
            :,newaxis,newaxis]

    def building_response(self,SA):
        """Use the equivilant linear solver to solve 
        """
        rtol,maxits=self.rtol,self.csm_damping_max_iterations
        periods=self.periods
        magnitudes=self.magnitudes
        # building_parameters should already be compressed, or expanded.
        if True:
            # TODO: Allow hazus and aus standard response curves.
            # TODO: Allow cutoff after max.
            SA,surface_displacement=undamped_response(
                SA,periods,
                self.atten_rescale_curve_from_pga,
                self.atten_cutoff_max_spectral_displacement,
                self.loss_min_pga,
                magnitude=magnitudes)
            self.undamped_response=SA,surface_displacement
        else: raise ValueError
        self.corner_periods=calculate_corner_periods(periods,SA,magnitudes)
        
        # set up initial conditions:
        update_function=self.updated_response
        SA,SD,SAcap=self._damped_response(non_linear_damping=0)
        assert len(SA.shape)==3

        # Let's write SA, SD and SAcap out in a file.
        if False: # Note, this is a hack.  For one event, one site examples
            attribute_dic = {'SA(g)':SA.tolist()[0][0],
                             'SD(mm)':SD.tolist()[0][0],
                             'SAcap(g)':SAcap.tolist()[0][0]}
            title_index_dic = {'SA(g)':0,
                             'SD(mm)':1,
                             'SAcap(g)':2} 
            dict2csv('csm_internal.csv', title_index_dic, attribute_dic)
        #print "self.capacity_parameters", self.capacity_parameters
        #print "SAcap.tolist()[0][0]", SAcap.tolist()[0][0]
        #print "SA.tolist()[0][0]", SA.tolist()[0][0]
        #print "SD.tolist()[0][0]", SD.tolist()[0][0]
        # now solve
        SD_building,non_convergant = solve(SA,SD,SAcap,update_function,
                                           rtol=rtol,maxits=maxits)
        SA_building=calculate_capacity(SD_building[:,:,newaxis],
                                       self.capacity_parameters)
        assert SA_building.shape[-1]==1 # should not have periods
        assert len(SA_building.shape)==3 # should not have periods
        assert len(SD_building.shape)==2 # should not have periods
        SA_building=SA_building[...,0] # collapse out periods
        #print "cap_spec_mod SA_building,SD_building", SA_building,SD_building
        return SA_building,SD_building
    
    def updated_response(self,displacement):
        """
        Calculate the updated response for a given displacement
        """
        # get the non-linear damping offset:
        if not len(displacement.shape)==2:
            print displacement
            raise ValueError
        non_linear_damping=self._non_linear_damping(displacement)
        SA,SD,SAcap=self._damped_response(non_linear_damping)
        if self.csm_hysteretic_damping==0: # Not used. Check logic.
            print "!!!!!!!!!!!!!!!!!!!!!!!!"
            import sys
            sys.exit()
            exit_flag=True
        else:
            exit_flag= not (non_linear_damping>0).any()
        return SA,SD,SAcap,exit_flag

    def _non_linear_damping(self,displacement):
        if self.csm_hysteretic_damping==0:  # Not used. Check logic.
            print "!!!!!!!!!!!!!!!!!!!!!!!!"
            import sys
            sys.exit()
            return 0.0
        else:
            # Calculate the acceleration of the intersect point.
            displacement=displacement[:,:,newaxis]
            acceleration=calculate_capacity(displacement,
                                            self.capacity_parameters)
            assert acceleration.shape[-1]==1 # should not have periods
            # Get the right damping function.
            if self.csm_hysteretic_damping is 'trapeziodal':
                damping_function=trapazoid_damp   
            else:
                damping_function=nonlin_damp
                
            SA,SD=acceleration,displacement
            # calculate damping
            damping=damping_function(self.capacity_parameters,
                                     self.kappa,SA,SD,self.csm_hysteretic_damping)
            damping[where(SA<0.00000000001)]=0
            return damping
    
    def _damped_response(self,non_linear_damping=0.0):        
        SA0,SD0=self.undamped_response # retrieve undamped response
        assert len(SA0.shape)==3
        initial_damping=self.initial_damping # get initial damping
        damping_factor=non_linear_damping+initial_damping
        # get the reduction factors:
        Ra,Rv,Rd=calculate_reduction_factors(damping_factor)
        
        # maybe treat displacement sensitive as velocity sensitive:
        if self.csm_damping_regimes == CSM_DAMPING_REGIMES_USE_ALL:
            pass
        elif self.csm_damping_regimes == CSM_DAMPING_REGIMES_USE_RA_RV:
             Rd=Rv
        elif self.csm_damping_regimes == CSM_DAMPING_REGIMES_USE_RV:
             Ra=Rv
             Rd=Rv
        else:
            raise ValueError

        TAV,TVD=self.corner_periods # get corner periods
        assert len(TAV.shape)==2
        assert len(TVD.shape)==2     
        # damp the corner periods is flag is set:
        # (note this does not affect the original corner periods)
        assert Ra.shape[-1]==1
        assert Rv.shape[-1]==1
        assert len(Ra.shape)==3
        assert len(Rv.shape)==3
        if self.csm_damping_modify_Tav==CSM_DAMPING_MODIFY_TAV:
            #print 'damping',damping_factor
            #print 'TAV',TAV[:,0:5]
            #print 'Ra,Rv',Ra[:,0:5],Rv[:,0:5]
            TAV=TAV*(Ra[:,:,0]/Rv[:,:,0])
            #print 'TAV',TAV[:,0:5]

        periods=self.periods
        
        # update SA:  
        SA,SD=calculate_updated_demand(periods,SA0,SD0,Ra,Rv,Rd,TAV,TVD,
                                       csm_damping_use_smoothing=self.csm_damping_use_smoothing)
        # update capacity:
        SAcap=calculate_capacity(SD,self.capacity_parameters)
        return SA,SD,SAcap
        
    def _calculate_parameters(self,building_parameters,magnitude,
                              building_type_index=None):
        """
        Calculate the derived parameters
        """
        number_events=len(magnitude)

        if building_type_index is None:
            building_type_index=slice(None)
            
        # get some constants and expand to the
        # size of ground motion ([sites,mag,periods])
        #print "building_parameters['design_strength']", building_parameters['design_strength']
        C=building_parameters['design_strength'][:,newaxis,newaxis]
        T=building_parameters['natural_elastic_period'][:,newaxis,newaxis]
        a1=building_parameters['fraction_in_first_mode'][:,newaxis,newaxis]
        a2=building_parameters['height_to_displacement'][:,newaxis,newaxis]
        y=building_parameters['yield_to_design'][:,newaxis,newaxis]
        Lambda=building_parameters['ultimate_to_yield'][:,newaxis,newaxis]
        u=building_parameters['ductility'][:,newaxis,newaxis]

        sdtcap=self.sdtcap
        csm_use_variability=self.csm_use_variability
        csm_variability_method=self.csm_variability_method

        # calculate capacity curve parameters from building parameters:
        params=calculate_capacity_parameters(C,
                                             T,a1,a2,y,Lambda,u,
                                             sdtcap=sdtcap,
                                             number_events=number_events,
                                             csm_use_variability=csm_use_variability,
                                             csm_variability_method=csm_variability_method)
        # note: params=Dy,Ay,Du,Au,aa,bb,cc
        #print "_calculate_parameters params", params
        return params
    
    def _calculate_kappa(self,building_parameters,magnitude):
        
        ###if building_type_index is None:
        ###    building_type_index=slice(None)
            
        damping_s=building_parameters['damping_s'][:,newaxis]
        damping_m=building_parameters['damping_m'][:,newaxis]
        damping_l=building_parameters['damping_l'][:,newaxis]
        magnitude=magnitude[newaxis,:]
        assert len(magnitude.shape)==2
        # blow up magnitude to [sites,events,sample]
        kappa = calculate_kappa(magnitude,damping_s,damping_m,damping_l)
        return kappa
