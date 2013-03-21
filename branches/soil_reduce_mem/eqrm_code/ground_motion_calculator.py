"""
 Title: ground_motion_calculator.py

  Description: Classes that calculate the bed rock response spectral
  acceleration. These classes rely on ground_motion_specification. It
  is called by analysis.py


  Version: $Revision: 1666 $
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2010-05-10 23:21:10 +1000 (Mon, 10 May 2010) $
"""
from scipy import asarray, alltrue, newaxis, ndarray, allclose, isfinite, \
     zeros, concatenate, absolute, array

from eqrm_code.ground_motion_specification import Ground_motion_specification

class Ground_motion_calculator(object):
    """Ground_motion_calculator instances are used to calculate the ground
    motion given a ground motion specifiction.

    Attributes:
      GM_spec: instance of Ground_motion_specification
      coefficient:   ground motion coefficient for the given periods
      sigma_coefficient:  ground motion sigma coefficient for the given periods
      periods:  the periods
    """

    def __init__(self, ground_motion_model_name, periods):
        """
        Args:
        ground_motion_model_name: A string, naming the ground motion model
        periods: The periods that will be used for this simulation.  Used
          to calculate coefficient and sigma_coefficient.

        RESIZING NOTES
        Adding lots of extra dimensions.

        'distance' had dimension [site]*[events]
        'magnitude' had dimension [events]
        'coefficient' had dimension [number of coefficients]*[Period]
        'sigma_coefficient' had dimension [number of coefficients]*[Period]

        Now 'distance' and 'magnitude' have dimension:
        [bonus dimension!]*[site]*[events]

        once 'coefficient' and 'sigma_coefficient are unpacked (ie
        c1,c2,c4,c6,c7,c10=c), they have dimension:
        [bonus dimension!]*[site]*[events]

        Note that some of these dimensions are degenerate (newaxises),
        such as [site] for 'magnitude'.

        newaxis is used to broadcast arrays into higher dimensions:
        a=array([1,2,3])
        b=array([0,1])
        a=a[...,newaxis]
        print a
        >[[1]
        > [2]
        > [3]]

        # if a is added to a 1D array of length n; a will act as:
        #    [[1, 1, ... (n times],
        #     [2, 2, ... (n times],
        #     [3, 3, ... (n times]]
        # (this is just broadcasting rules)

        a+b
        >array([[1, 2],
        >       [2, 3],
        >       [3, 4]])

        Note that all [bonus dimensions] are degenerate.
        They are there because once the distribution is sampled,
        I want it to maintain the same number of dimension. I don't
        want it to add an extra dimension for the spawnings. If that
        happens, then it is hard to address futher samplings (from
        soil) or multi-models in a uniform manner.

        so ground_motion_from_toro =[gmd_torro]
        sampled ground_motion_from_toro = [gmd1,gmd2,gmd3, ... (n samples)]
        Uniform behaviour.
        """

        self.GM_spec = Ground_motion_specification(ground_motion_model_name)

        periods = asarray(periods)
        # calc the coefficient and sigma_coefficient for the input periods
        coefficient = self.GM_spec.calc_coefficient(periods)
        sigma_coefficient = self.GM_spec.calc_sigma_coefficient(periods)

        # Adding extra dimensions.
        self.coefficient = coefficient[:,newaxis,newaxis,:]
        self.sigma_coefficient = sigma_coefficient[:,newaxis,newaxis,:]


    def distribution_function(self, dist_object, dist_types, mag_dict,
                              periods=None, depth=None, depth_to_top=None, 
                              fault_type=None, Vs30=None, mag_type=None,
                              Z25=None, dip=None, width=None,
                              event_activity=None):
        """
        dist_object must give distance info if dist_object.distance(dist_type)
        is called.  The distance info must be an array.

        Returns:
          log_mean - dimensions are 
          log_sigma

        FIXME: Why should we let depth be None?
        """

        # dist_type and mag_type are attributes of self.GM_spec
        # we shouldn't pass them around.

        distances = {}
        for dist_type in dist_types:
            distances[dist_type] = dist_object.distance(dist_type)
        
        mag = mag_dict[mag_type]

        if depth is not None:
            depth = asarray(depth)

        (mag, depth, depth_to_top, fault_type,
         dip, width) = self.resize_mag_depth(mag, depth, depth_to_top,
                                             fault_type, dip, width)
        for dist_type in dist_types:
            distances[dist_type] = self.resize_dist(distances[dist_type], 
                                                    mag.size)

        # This is calling the distribution functions described in the
        # ground_motion_interface module.
        # We add the new 'dist_object' parameter to cater to models that
        # require more than one distance.  Once all existing models use
        # the new parameter we can remove the 'distance' parameter.
        distribution_args = {'mag': mag,
                             'coefficient': self.coefficient,
                             'sigma_coefficient': self.sigma_coefficient,
                             'depth': depth,
                             'depth_to_top': depth_to_top,
                             'fault_type': fault_type,
                             'Vs30': Vs30,
                             'Z25': Z25,
                             'dip': dip,
                             'width': width,
                             'periods': periods}
        for dist_type in dist_types:
            distribution_args[dist_type] = distances[dist_type]
        
        (log_mean, log_sigma) = self.GM_spec.distribution(**distribution_args)

        # FIXME when will this fail?  Maybe let it fail then?
        # If it does not fail here it fails in analysis.py"
        #, line 427, in main
        # assert isfinite(bedrock_SA).all()
        # example of log_mean when this failed log_mean [[[ NaN  NaN  NaN]]]
        # An Mw of 0.0 caused it.
        # this is a good place to catch this error
        assert isfinite(log_mean).all()
        assert isfinite(log_sigma).all()

        return (log_mean, log_sigma)

    def resize_mag_depth(self, mag, depth, depth_to_top, fault_type, dip, width):
        """
        Warning, Toro_1997_midcontinent_distribution assumes
        that this occurs.  So if resizing is changed,
        Toro_1997_midcontinent_distribution needs to be changed as well
        """

        if mag.size == 1:
            mag = mag.reshape([1])
            if depth is not None:
                depth = depth.reshape([1]) # Don't know if we have to do this
            if depth_to_top is not None:
                depth_to_top = depth_to_top.reshape([1])
            if fault_type is not None:
                fault_type = fault_type.reshape([1])

        # resize depth, depth_to_top, etc
        if depth is not None:
            depth = depth[newaxis,:,newaxis]
            # collapsed arrays are a bad idea...

        if depth_to_top is not None:
            depth_to_top = array(depth_to_top)[newaxis,:,newaxis]

        if fault_type is not None:
            fault_type = array(fault_type)[newaxis,:,newaxis]

        if dip is not None:
            dip = array(dip)[newaxis,:,newaxis]

        if width is not None:
            width = array(width)[newaxis,:,newaxis]

        assert len(mag.shape) == 1

        mag = mag[newaxis,:,newaxis]

        return (mag, depth, depth_to_top, fault_type, dip, width)

    def resize_dist(self, dist, mag_size):
        """
        Warning, Toro_1997_midcontinent_distribution assumes
        that this occurs.  So if resizing is changed,
        Toro_1997_midcontinent_distribution needs to be changed as well
        """
        # [4.5,5.5,6.0] => site * mag * T
        assert len(dist.shape)<3
        if not len(dist.shape)==2:
            # if distances is collapsed
            if dist.size==1:
                # if distances is size 1
                dist=dist.reshape((1,1))
            else:
                assert len(dist.shape)==1
                if mag_size>1:
                    assert dist.size==mag_size
                    # therefore distance is 1 site * n magnitudes
                    dist=dist.reshape((1,mag_size))
                else:
                    # therefore distance is n site * 1 magnitudes
                    dist=dist.reshape((dist.size,1))
        # collapsed arrays are a bad idea...

        dist=dist[:,:,newaxis]
        # [[30.0,35.0],[45.0,20.0]]=> [site*mag] * T

        return dist


class Multiple_ground_motion_calculator(object):
    """Multiple Ground_motion_calculator instances are used to
    calculate the ground motion given one or more ground motion models.

    Attributes:
      model_weights: The weight assossicated with each model (array)
      GM_models: a list of Ground_motion_calculator instances.
    """

    def __init__(self, ground_motion_model_names, periods, model_weights):
        self.periods = periods

        # Should do this just once, when the para values are first verified.
        # The -ve value means 'the logic tree is not collapsed'
        self.model_weights = asarray(model_weights)
        if not allclose(1,self.model_weights.sum()):
            print 'model_weights,',-self.model_weights
            raise ValueError('abs(self.model_weights) did not sum to 1!')

        self.GM_models = []
        for GM_model_name in ground_motion_model_names:
            self.GM_models.append(Ground_motion_calculator(GM_model_name,
                                                           periods))

    def distribution(self, sites, event_set, distances, event_activity=None,
                     Vs30=None, GM_models=None):
        """
        Calculate the ground motion shaking at a site, given an array of
        events.

        sites
        event_set, an event_set object.  The shape of the attributes of this
          instance will be equal to the shape of the returned arrays.
        Vs30 - the Vs30 value used if the gmm needs it.  If none is given the
          site Vs30 value is used.

        returns:
          *_extend_GM has shape of (GM_model, sites, events, periods)
        """

        # get distances, etc
        magnitudes = {'Mw': event_set.Mw, 'ML': event_set.ML}
        if Vs30 is None:
            Vs30 = sites.attributes.get('Vs30', None)

        log_mean_extend_GM, log_sigma_extend_GM = self._distribution_function(
            distances, magnitudes,
            depth=event_set.depth,
            depth_to_top=event_set.depth_to_top,
            fault_type=event_set.fault_type,
            Vs30=Vs30, Z25=None, dip=event_set.dip,
            width=event_set.width,
            event_activity=event_activity,
            periods=self.periods,
            GM_models=GM_models)

        return log_mean_extend_GM, log_sigma_extend_GM

    
    def _distribution_function(self, dist_object, mag_dict, periods=None,
                               depth=None, depth_to_top=None,
                               fault_type=None, Vs30=None, Z25=None,
                               dip=None, width=None,
                               event_activity=None,
                               GM_models=None):
        """
        The event_activity not used currently.
        But if we spawn they will be.

        returning values
          log_mean_extend_event the log_mean values
            dimensions (sites, events * GM_model, periods)
          log_sigma_extend_GM the log_sigma values
            dimensions (sites, events * GM_model, periods)
        """
        if GM_models is None:
            GM_models = self.GM_models
        for mod_i, GM_model in enumerate(GM_models):
            (log_mean, log_sigma) = GM_model.distribution_function(
                dist_object, GM_model.GM_spec.distance_types,
                mag_dict, periods=periods,
                depth=depth, depth_to_top=depth_to_top,
                fault_type=fault_type, Vs30=Vs30,
                Z25=Z25, dip=dip, width=width,
                mag_type=GM_model.GM_spec.magnitude_type)
            if mod_i == 0:
                log_mean_extend_GM = log_mean[newaxis,:]
                log_sigma_extend_GM = log_sigma[newaxis,:]
            else:
                new_axis = 0
                event_axis = 1
                log_mean_extend_GM = concatenate(
                    (log_mean_extend_GM, log_mean[newaxis, :]),
                    axis=new_axis)
                
                log_sigma_extend_GM = concatenate(
                    (log_sigma_extend_GM, log_sigma[newaxis, :]),
                    axis=new_axis)
        
        return log_mean_extend_GM, log_sigma_extend_GM

