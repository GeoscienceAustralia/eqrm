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

def do_collapse_logic_tree(data, event_num, weights,
                           THE_PARAM_T, use_C=True):
    """
    Collapse data, such as when several events are used to repressent
    one event.
    
    Data is the array to be collapsed (eg ground_motion or loss)

    """
    if len(data.shape) >= 4:
        # Assume the extra dimension is the ground motion model
        if THE_PARAM_T.atten_collapse_Sa_of_atten_models is True:
            new_data = _collapse_att_model_dimension(data,
                                                     weights)
        else:       
            new_data = data 
            
    else:
        
        # if there is only one attenuation model.
        no_attn_collapse = (
            (len(weights) == 1) or
            THE_PARAM_T.atten_collapse_Sa_of_atten_models is False)
        
        if no_attn_collapse:        
            new_data = data 
        else:
            weights = asarray(weights)
            num_of_att_models = int(len(event_num)/(max(event_num) + 1))
            new_data = _collapse_att_model_results(data,
                                                   weights,
                                                   num_of_att_models)
            
    return new_data, None, None

def _collapse_att_model_results(data, weights, num_of_att_models):
    """
    Collapse the data so it does not have an attenuation model dimension.
    To collapse it, multiply the data by the weights and sum.

    The data will not actually have an explicit attenuation model dimension.
    The second dimension is event*attenuation model.  The data is grouped
    results per event for the first att' model, then the second att' model ect.
    
    Data has 3 dimensions; (site, events*attenuation models, periods)
    Site is 1.
    
    What the data is changes. Sometimes its SA, sometimes it's cost.
    
    """
    first_axis = data.shape[0]
    last_axis = data.shape[2]
    
    weights.shape = (1, -1, 1)
    weighted_data = data*weights 
    weighted_data.shape = (first_axis, num_of_att_models, -1, last_axis) 
    sum = scipy.sum(weighted_data, 1)
    
    return sum
        
def _collapse_att_model_dimension(data, weights):
    """
    Collapse the data so it does not have an attenuation model dimension.
    To collapse it, multiply the data by the weights and sum.

    Parameters:
      data:  4 or more dimensions; with ground motion model being the
        third last dimension e.g.
      (ground motion model, site, events, periods)
      (spawn, ground motion model, site, events, periods)
        Site is 1. What the data is changes. Sometimes its SA, sometimes
        it's cost.
      weights: The weight to apply to each ground motion model 'layer'
    
    """
    new_weight_shape = ones((data.ndim))
    gmm_index_from_end = -4
    gmm_index_from_start = data.ndim - 4
    new_weight_shape[gmm_index_from_end] = -1
    weighted_data = data * reshape(weights, new_weight_shape) 
    sum = scipy.sum(weighted_data, gmm_index_from_start)
    
    return sum    

    
def collapse_att_model(data, weights, do_collapse):
    """
    
    If do_collapse is True, collapse the data so the attenuation model
    dimension length is one.  To collapse it, multiply the data by the
    weights and sum, across the ground motion model dimension.

    Parameters:
      data:  5 dimensions; 
      (spawn, ground motion model, site, events, periods)
        Site is 1. What the data is changes. Sometimes its SA, sometimes
        it's cost.
      weights: The weight to apply to each ground motion model 'layer'
    
    """
    if do_collapse:
        new_data_shape = data.shape
        new_weight_shape = ones((data.ndim))
        gmm_index_from_end = -4
        gmm_index_from_start = data.ndim - 4
        new_weight_shape[gmm_index_from_end] = -1

        # the new data shape will be just like data,
        # but the length of the gmm dimension will be 1.
        new_data_shape = list(data.shape)
        new_data_shape[gmm_index_from_end] = 1
        
        weighted_data = data * reshape(weights, new_weight_shape) 
        data = scipy.sum(weighted_data, gmm_index_from_start)

        # Put the gmm dimension back
        data = data.reshape(new_data_shape)

    
    return data


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
'''
	print 'hack'
	if hack[0]==3*3:
            print 'HACK',hack[0]
            r_nu_f = open('r_nu.txt','w')
            r_nu_f.write('\n'.join([' '.join([str(float(f)) for f in line])
                                   for line in [r_nu]]))
            r_nu_f.close()

            sa_f = open('sa.txt','w')
            sa_f.write('\n'.join([' '.join([str(float(f)) for f in line])
                                   for line in sa]))
            sa_f.close()

            hzd_file = open('hzd.txt','w')
            hzd_file.write('\n'.join([' '.join([str(float(f)) for f in line])
                                   for line in [hzd]]))
            hzd_file.close()
            
            cumnu_file = open('cumnu.txt','w')
            cumnu_file.write('\n'.join([' '.join([str(float(f)) for f in line])
                                   for line in [cumnu]]))
            cumnu_file.close()
            
            trghzd_rock_pga_file = open('trghzd_rock_pga.txt','w')
            trghzd_rock_pga_file.write('\n'.join([' '.join([str(float(f)) for f in line])
                                   for line in [trghzd_rock_pga]]))
            trghzd_rock_pga_file.close()
            raise
        else: hack[0]+=1     '''   

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
