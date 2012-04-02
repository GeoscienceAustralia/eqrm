"""
 Title: exceedance_curve.py
  
  Author:  Peter Row, peter.row@ga.gov.au


  Description: Functions for collapsing logic trees. 

  Version: $Revision: 1562 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-03-09 15:48:50 +1100 (Tue, 09 Mar 2010) $
"""
from numpy import NaN
import scipy
from scipy import allclose, isfinite, array, newaxis, zeros, ndarray, \
     asarray, where, concatenate, allclose, reshape, ones

def _collapse_att_model_dimension(data, weights):
    """
    Collapse the data so it does not have an attenuation model dimension.
    To collapse it, multiply the data by the weights and sum.

    This assumes the same ground motion model weights are applied to
    all of the data.  

    Parameters:
      data: With dimensions 5 or more;
      The 5th last dimension is ground motion model.
      e.g. (spawn, max ground motion model, rec_model, site, events, periods) OR
      (max ground motion model, rec_model, site, events, periods)
        Site is 1. What the data is changes. Sometimes its SA, sometimes
        it's cost.
      weights: The weight to apply to each ground motion model 'layer'
       1D, dimension (gmm)

       max gmm >= gmm

    Returns
    sum : same dimensions as weight without the gmm dimension.
    """
    assert data.ndim > 4
    # The lenght of weight can be less than the max gmm dimension in data.
    weighted_data = (data[..., 0:len(weights), :, :, :, :] *
                     asarray(weights)[:, newaxis, newaxis, newaxis, newaxis])
    # numpy.sum() allows -ve axis. See
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html#numpy.sum
    return scipy.sum(weighted_data, -5)

    
def collapse_att_model(data, weights, do_collapse):
    """
    
    If do_collapse is True, collapse the data so the attenuation model
    dimension length is one.  To collapse it, multiply the data by the
    weights and sum, across the ground motion model dimension.

    This assumes the same ground motion model weights are applied to
    all of the data.

    Parameters:
      data:  6 dimensions; 
      (spawn, ground motion model, rec_model, site, events, periods)
        Site is 1. What the data is changes. Sometimes its SA, sometimes
        it's cost.
      weights: The weight to apply to each ground motion model 'layer'
               1D, dimension (gmm)

    Returns: array with same rank and dimensions as data except GMM
    axis will be 1 if do_collapse
    """
    if do_collapse:
        # Collapse and put the gmm dimension back
        return _collapse_att_model_dimension(data, weights)[..., newaxis, :, :, :, :]
    return data

def collapse_source_gmms(data, source_model, do_collapse):
    """
    Given data with a ground motion model dimension (gmm),
    collapse this dimension, applying the weights in source_model.

    THE SECOND LAST AXIS IS ASSUMED TO BE EVENT
    THE 5th LAST AXIS IS ASSUMED TO BE GMM
    
    parameters:
      data - an array of values (e.g. cost).  One of the dimensions is gmm. An example of
             the dimensions are (spawn, ground motion model, site, events, periods)
      source_model - An interable object that iterates over Source instances.
      do_collapse - If True, collapse the ground motion model dimension.

    returns:
      data - the dimensions will still be the same as the input data.  If do_collapse is
             True the gmm dimension will be 1, and the data has been collapsed.
    """
    if not do_collapse:
        return data
    assert data.ndim > 5
    for source in source_model:
        event_ind = source.get_event_set_indexes()
        col_data = collapse_att_model(data[...,event_ind, :],
                                      source.atten_model_weights, do_collapse)
        data[...,0:1,:,:,event_ind, :] = col_data

        # Erase the data that has been weighted.
        weight_length = len(source.atten_model_weights)
        data[...,1:weight_length,:,:,event_ind, :] = 0.0

    # Check here that all values have been collapsed.
    assert scipy.sum(data[...,1:,:,:,:,:]) == 0.0
    
    return data[...,0:1,:,:,:,:]

def hzd_do_value(sa, r_nu, rtrn_rte): #,hack=[0]):
    """
    INPUTS:
    sa       [vector (nx1)] response spectral accelerations
    r_nu     [vector (nx1)] event activity for the corresponding element
    in sa
    rtrn_rte  [vector (mx1)] return rates of interest.
    
    OUTPUTS:
    hzd       [vector (1xm)] hazard value for each return rate
    """
    #n_rte = length(rtrn_rte);
    assert isfinite(sa).all()
    # (SAbedrock(:,I1), GET_EVNTDB_ESS_T.r_nu(Haznull));
    hzd,cumnu = _rte2cumrte(sa,r_nu) 
    assert isfinite(hzd).all()
    trghzd_rock_pga	= _get_rskgvnrte(hzd, cumnu, rtrn_rte)
    assert isfinite(trghzd_rock_pga).all()
    hzd = trghzd_rock_pga	
    return hzd


def _rte2cumrte(each_risk,each_rte):
    if not each_risk.shape[-1]==each_rte.shape[-1]:
        s='risk shape = '+str(each_risk.shape)
        s+=' rte shape = '+str(each_rte.shape) 
        raise ValueError('risk and rte must be the same length! '+s)
    each_risk=each_risk.ravel()
    risk_order=(-each_risk).argsort()
    rsk=each_risk[risk_order]
    cumrte=each_rte[risk_order].cumsum()
    return rsk,cumrte


def _get_rskgvnrte(rsk,cumrte,trgrte):
    #from numpy import NaN,zeros,isfinite,allclose
    n_trg=len(trgrte)
    n_rsk=len(rsk)
    trgrsk=zeros((n_trg,),dtype=float)
    for i in range(n_trg):
        # default to 0 (will return 0 if desired return period is
        # too short for the simulation.
        trgrsk[i]=0
        ihgh=cumrte.searchsorted(trgrte[i])
        # returns j such that cumrte[j-1] < trgrsk[i] <= cumrte[j]
        # returns len(cumrte) if max(cumrte) < trgrsk[i]
        # returns 0 if trgrsk[i] <= min(cumrte) - Note this won't happen
        if ihgh<len(cumrte): 
            if ihgh>0:
                # Linear interpolation between rsk[ihgh] and rsk[ihgh-1]
                # at x = cumrte[ihgh] and cumrte[ihgh-1]
                trgrsk[i]=rsk[ihgh-1]+((rsk[ihgh]-rsk[ihgh-1])*
                                       (cumrte[ihgh]-trgrte[i])/
                                       (cumrte[ihgh]-cumrte[ihgh-1]))
            else:
                trgrsk[i]=rsk[ihgh]
            # end if
        #end if
    #end for
    return trgrsk
