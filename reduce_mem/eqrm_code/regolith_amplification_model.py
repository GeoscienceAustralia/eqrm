"""
 Title: regolith_amplification_model.py
 
  Author:   Peter Row, peter.row@ga.gov.au
             
  Description: 
 
  Version: $Revision: 914 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-04-01 11:11:47 +1100 (Wed, 01 Apr 2009) $
  
  Copyright 2007 by Geoscience Australia
"""
from scipy import asarray, exp, indices, minimum, maximum, zeros, array, log, \
     r_, where, weave, arange

from eqrm_code.xml_interface import Xml_Interface
from eqrm_code.interp import interp
from eqrm_code.csv_interface import csv2dict
from eqrm_code import util
from eqrm_code import weave_converters

class Regolith_amplification_model(object):
    """
    """
    # inherit just for the interpolation methods
    # should subclass - GM(subclass), RA(subclass)
    
    def __init__(self, pga_bins, moment_magnitude_bins, periods,
                 log_amplifications, log_stds):

        pga_bins=asarray(pga_bins)
        moment_magnitude_bins=asarray(moment_magnitude_bins)
        periods=asarray(periods)
        for site_class in log_amplifications.keys():
            log_amplifications[site_class]=asarray(
                log_amplifications[site_class])            
            log_stds[site_class]=asarray(log_stds[site_class])        
        
        self.pga_bins = pga_bins
        self.moment_magnitude_bins = moment_magnitude_bins
        self.periods = periods
        self.log_amplifications = log_amplifications
        self.log_stds = log_stds

        # check that periods is increasing
        try: assert (self.periods.argsort()==r_[0:len(self.periods)]).all()
        except:
            self.periods=self.periods[::-1] # reverse self.periods            
            assert (self.periods.argsort()==r_[0:len(self.periods)]).all()
            for site_class in self.log_amplifications.keys():
                log_amp=self.log_amplifications[site_class]
                self.log_amplifications[site_class]=log_amp[:,:,::-1]
                # reverse log amplifications
                
                self.log_stds[site_class]=self.log_stds[site_class][:,:,::-1]
                # reverse log standard deviations


    def distribution(self,ground_motion,site_classes,
                     Mw,event_periods,
                     event_activity=None):
        """
        Calculate the distribution of surface motion, given log of ground
        (bedrock) motion, site classes of events, event magnitudes,
        and event periods.

        ground_motion: ndarray [site, event, period]

        returns:  (log_mean, log_sigma). ndarrays with same shape as ground_motion

        
        Implementation:
        bin all the pga and magnitudes
        loop over the models site classes:
            get the amplification this site_class
            get the indices of the sites that fall in the current site_class   
            get the gm, pga, and mag for the sites in this site_class
            interpolate model amplification and std, then take the amp factors
              ... and std from the right bins in the interpolated model

        Dimension of final distribution = [ground_motion_samples]*[sites]*...
        
        If you sample it, it will return
        [samples * ground_motion_samples]*[sites]*...

        parameters:
          event_activity: Being phased out of here.  Don't use.
          Don't clean up though, just incase we need to spawn.
        """
        if not Mw.size == ground_motion.shape[1]:
            raise ValueError
        
        # bin all the pga and magnitudes
        event_pga_bins_indices = self._bin_indices(ground_motion[:,:,0],
                                                   self.pga_bins)
        event_mag_bins_indices = self._bin_indices(Mw,
                                                   self.moment_magnitude_bins)

        # initialise mean and sigma
        log_amplification=zeros(ground_motion.shape,dtype=float)
        log_sigma=zeros(ground_motion.shape,dtype=float)
        
        for site_class in self.log_amplifications.keys():
            # interpolate model amplification and std, then take the amp
            #  factors and std from the right bins in the interpolated model

            log_amp=interp(event_periods,self.log_amplifications[site_class],
                           self.periods,axis=2)
            
            log_stds=interp(event_periods,self.log_stds[site_class],
                            self.periods,axis=2)
            

            num_periods=len(event_periods)
            num_events=len(Mw)
            num_sites=len(site_classes)
            try:
                in_zone = [s==site_class for s in site_classes]
                in_zone=array(in_zone)*1 # upcast from boolean
                code = """
                int m,n;
                for (int i=0; i<num_sites; ++i){
                    if (in_zone(i)==1){
                        for (int j=0; j<num_events; ++j){
                            m=event_mag_bins_indices(j);
                            n=event_pga_bins_indices(i,j);
                            for (int k=0; k<num_periods; ++k){
                                log_amplification(i,j,k)=log_amp(m,n,k);
                                log_sigma(i,j,k)=log_stds(m,n,k);
                            }
                        }
                    }
                }
                return_val = 0;
                """
                try:
                    weave.inline(code,
                                 ['event_pga_bins_indices',
                                  'event_mag_bins_indices',
                                  'log_amp', 'log_stds',
                                  'log_amplification', 'log_sigma',
                                  'num_sites','num_events',
                                  'num_periods',
                                  'in_zone'],
                                 type_converters=weave_converters.eqrm,
                                 compiler='gcc')
                except IOError:
                    raise util.WeaveIOError 

                    
            
            except:
                print "No gcc found. Running Regolith_amplification_model.\
                distribution_function in pure python"
                for i in range(num_sites):
                    if site_classes[i]==site_class:
                        for j in range(num_events):  
                            m=event_mag_bins_indices[j]
                            n=event_pga_bins_indices[i,j] 
                            for k in range(num_periods):
                                log_amplification[i,j,k]=log_amp[m,n,k]
                                log_sigma[i,j,k]=log_stds[m,n,k]
                                
        log_mean=log(ground_motion)+log_amplification
        return  log_mean, log_sigma
    

    def _bin_indices(self, values, bin_points):
        """
        Returns the index in points that is closest to value for
         each value in values. 
        """
        # get the midpoints
        midpoints = (bin_points[1:]+bin_points[:-1])/2
        
        # bin_indices = i such that bin_points[i-1] < values <= bin_points[i]
        # except:
        # bin_indices = len(bin_points) if values < bin_points
        # bin_indices =  0 if values <= bin_points
        bin_indices = midpoints.searchsorted(values)
        return bin_indices

 
    @classmethod  
    def from_xml(cls, filename):
        """
        """
        
        paras = amplification_model_parameters_from_xml(filename)
        pga_bins,moment_magnitude_bins,periods,log_amplifications,log_stds=paras
        
        model = cls(pga_bins,moment_magnitude_bins,periods,
                    log_amplifications,log_stds)
        return model

    
def amplification_model_parameters_from_xml(filename):
    """
    load an xml amplitfication model from file.

    return pga,moment_magnitude,periods,log_amplifications,log_stds
    """
    xml_model=Xml_Interface(filename=filename)
    moment_magnitude_bins= \
                       asarray(xml_model['moment_magnitude_bins'][0].array[0])
    pga_bins=asarray(xml_model['pga_bins'][0].array[0])
    periods=asarray(xml_model['periods'][0].array[0])

    log_amplifications = {}
    log_stds = {}
    for xml_site_class in xml_model['site_class']:
        
        log_amplification=zeros((len(moment_magnitude_bins),
                                 len(pga_bins),len(periods)),
                                dtype=float)
        log_std=zeros((len(moment_magnitude_bins),
                       len(pga_bins),len(periods)),
                      dtype=float)
        
        site_class=xml_site_class.attributes['class']
        for i in range(len(xml_site_class['moment_magnitude'])):
            xml_moment_magnitude=xml_site_class['moment_magnitude'][i]
            for j in range(len(xml_moment_magnitude['pga'])):
                xml_pga=xml_moment_magnitude['pga'][j]
                xml_log_amplification=xml_pga['log_amplification'][0]
                log_amplification[i,j,:]=xml_log_amplification.array[0]
                
                xml_log_std=xml_pga['log_std'][0]
                log_std[i,j,:]=xml_log_std.array[0]                
        assert not site_class in log_amplifications # assert no duplicates
        log_amplifications[site_class]=log_amplification
        log_stds[site_class]=log_std

    return pga_bins,moment_magnitude_bins,periods,log_amplifications,log_stds

def load_site_class2Vs30(file_name):
    """
    Load the data used to convert a site class to a Vs30 value.
    args:
      file_name: The file to be opened, with extension, or
                 a file handle.
      
    Return:
      class2Vs30_dict: A dic of 'site_class' and 'Vs30' keys.

    Raises:
      IOError if the file is not present or the file does not have
        site_class and Vs30 in the header.
    """
    csv_columns_dict, _ = csv2dict(file_name, ('vs30', 'site_class'),
                                   convert={'vs30':float})
    
    site_class2Vs30_dict = {}
    for siteclass, Vs30 in map(None, csv_columns_dict['site_class'],
                               csv_columns_dict['vs30']):
        site_class2Vs30_dict[siteclass] = Vs30
    return site_class2Vs30_dict
    
def load_site_class2Vs30_old(file_name):
    """
    Load the data used to convert a site class to a Vs30 value.
    Return:
      class2Vs30_dict: A dic of 'site_class' and 'Vs30' keys.

    Raises:
      IOError if the file is not present or the file does not have
        site_class and Vs30 in the header.
    """
    from eqrm_code.csv_interface import csv2dict
    csv_columns_dict = csv_to_arrays(file_name, ('Vs30', 'site_class'))
    
    site_class2Vs30_dict = {}
    for siteclass, Vs30 in map(None, csv_columns_dict['site_class'],
                               csv_columns_dict['Vs30']):
        site_class2Vs30_dict[siteclass] = Vs30
    return site_class2Vs30_dict


def get_soil_SA(bedrock_SA, site_classes, Mw, atten_periods,
                soil_amplification_model, amp_distribution,
                ground_motion_calc, event_set, sites, distances,
                ground_motion_distribution):
    """
    Determine the soil_SA.

    Parameters:
      bedrock_SA - spectral acceleration, in g. dimensions
        [spawn, GM_model, rec_model, site, event, period]
      site_classes dimensions (site) = 1
      Mw - dimensions (events)
      atten_periods dimension (periods)
      amp_distribution - an instance of Distribution_Log_Normal.
      ground_motion_calc  - an instance of Multiple_ground_motion_calculator
      event_set - needed if a gmm has to be called
      sites - needed if a gmm has to be called

    Returns: array with the same shape as bedrock_SA
    """
    spawn_axis = 0
    GM_model_axis = 1
    rec_model_axis = 2
    assert  bedrock_SA.shape[GM_model_axis] == len(
        ground_motion_calc.GM_models)

    soil_SA_new = zeros(bedrock_SA.shape)
    for i_gmm, gmm in enumerate(ground_motion_calc.GM_models):
        if gmm.GM_spec.uses_Vs30 is True:
            log_mean, log_sigma = ground_motion_calc.distribution(
                sites, event_set, distances,
                GM_models=[gmm])
            sub_soil_SA = ground_motion_distribution.ground_motion_sample(
                log_mean, log_sigma)
            assert sub_soil_SA.ndim == 6
            soil_SA_new[:,i_gmm,:,:,:,:] = sub_soil_SA[:,0,:,:,:,:]
        else:
            for i_spawn in arange(bedrock_SA.shape[spawn_axis]):
                for i_rm in arange(bedrock_SA.shape[rec_model_axis]):
                    log_mean, log_sigma = soil_amplification_model.distribution(
                        bedrock_SA[i_spawn, i_gmm, i_rm, :],
                        site_classes,
                        Mw,
                        atten_periods)
                    # No variability in the period axis
                    var_in_last_axis = False 
                    sub_soil_SA = amp_distribution.sample_for_eqrm(log_mean, log_sigma,
                                                                   var_in_last_axis)

                    assert sub_soil_SA.ndim == 3 # site, event, period
                    soil_SA_new[i_spawn, i_gmm, i_rm, :,:,:] = sub_soil_SA
    return soil_SA_new
