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

        # FIXME: seems like double dipping
        #assert isinstance(periods,ndarray)
        periods=asarray(periods)
        # calc the coefficient and sigma_coefficient for the input periods
        coefficient = self.GM_spec.calc_coefficient(periods)
        sigma_coefficient = self.GM_spec.calc_sigma_coefficient(periods)

        # Adding extra dimensions.
        self.coefficient = coefficient[:,newaxis,newaxis,:]
        self.sigma_coefficient = sigma_coefficient[:,newaxis,newaxis,:]


    def distribution_function(self, dist_object, mag_dict, depth=None,
                              depth_to_top=None, faulting_type=None, vs30=None,
                              dist_type=None, mag_type=None, Z25=None, dip=None,
                              event_activity=None, event_id=None):
        """
        dist_object must give distance info if dist_object.distance(dist_type)
        is called.  The distance info must be an array.

        Returns:
          A Log_normal_distribution

        FIXME: Why should we let depth be None?
        """
        # dist_type and mag_type are attributes of self.GM_spec
        # we shouldn't pass them around.

        dist = dist_object.distance(dist_type)
        mag = mag_dict[mag_type]

        if depth is not None:
            depth = asarray(depth)

        (mag, depth, depth_to_top,
         faulting_type) = self.resize_mag_depth(mag, depth, depth_to_top,
                                                faulting_type)
        dist = self.resize_dist(dist, mag.size)

        # This is calling the distribution functions described in the
        # ground_motion_interface module.
        # We add the new 'dist_object' parameter to cater to models that
        # require more than one distance.  Once all existing models use
        # the new parameter we can remove the 'distance' parameter.
        (log_mean, log_sigma) = \
            self.GM_spec.distribution(dist_object=dist_object,
                                      mag=mag, distance=dist,
                                      coefficient=self.coefficient,
                                      sigma_coefficient=self.sigma_coefficient,
                                      depth=depth, depth_to_top=depth_to_top,
                                      faulting_type=faulting_type, vs30=vs30,
                                      Z25=Z25, dip=dip)

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

    def resize_mag_depth(self, mag, depth, depth_to_top, faulting_type):
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
            if faulting_type is not None:
                faulting_type = faulting_type.reshape([1])

        # resize depth, depth_to_top, etc
        if depth is not None:
            depth = depth[newaxis,:,newaxis]
            # collapsed arrays are a bad idea...

        if depth_to_top is not None:
            depth_to_top = array(depth_to_top)[newaxis,:,newaxis]

        if faulting_type is not None:
            faulting_type = array(faulting_type)[newaxis,:,newaxis]

        assert len(mag.shape) == 1

        mag = mag[newaxis,:,newaxis]

        return (mag, depth, depth_to_top, faulting_type)

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
      log_normal_distribution: a log_normal_distribution instance.
    """

    def __init__(self, ground_motion_model_names, periods, model_weights,
                 log_normal_distribution=None):
        # Should do this just once, when the para values are first verified.
        # The -ve value means 'the logic tree is not collapsed'
        self.model_weights=asarray(model_weights)
        if not allclose(1,self.model_weights.sum()):
            print 'model_weights,',-self.model_weights
            raise ValueError('abs(self.model_weights) did not sum to 1!')

        self.GM_models = []
        for GM_model_name in ground_motion_model_names:
            self.GM_models.append(Ground_motion_calculator(GM_model_name,
                                                           periods))
        self.log_normal_distribution = log_normal_distribution

    def distribution(self, sites, event_set, event_activity=None,
                     event_id=None):
        # get distances, etc
        distances = sites.\
                    distances_from_event_set(event_set,
                                             event_set_trace_starts=True)
        magnitudes = {'Mw': event_set.Mw, 'ML': event_set.ML}
        vs30 = sites.attributes.get('VS30', None)

        results=self._distribution_function(
            distances,
            magnitudes,
            depth=event_set.depth,
            depth_to_top=event_set.depth_to_top,
            faulting_type=event_set.faulting_type,
            vs30=vs30, Z25=None, dip=None,
            event_activity=event_activity,
            event_id=event_id)
        self.log_normal_distribution.set_log_mean_log_sigma_etc(*results)
        _, _, log_mean_array, log_sigma_array = results
        return self.log_normal_distribution, log_mean_array, log_sigma_array


    def _distribution_function(self, dist_object, mag_dict, depth=None,
                               depth_to_top=None, faulting_type=None,
                               vs30=None, Z25=None, dip=None,
                               event_activity=None, event_id=None):
        """
        The event_activity and event_id are not used currently.
        But if we spawn they will be.

        returning values
          log_mean_array the log_mean values
            dimensions (GM_model, sites, events, periods)
          log_sigma_array the log_sigma values
            dimensions (GM_model, sites, events, periods)
        """

        # This is where spawning occured.  Though it never worked.
        #log_mean_array = zeros((len(self.GM_models), ))
        multi_log_mean = []
        multi_log_sigma = []
        for mod_i, GM_model in enumerate(self.GM_models):
            (log_mean, log_sigma) = GM_model.distribution_function(
                dist_object, mag_dict,
                depth=depth, depth_to_top=depth_to_top,
                faulting_type=faulting_type, vs30=vs30,
                Z25=Z25, dip=dip,
                dist_type=GM_model.GM_spec.distance_type,
                mag_type=GM_model.GM_spec.magnitude_type)
            if mod_i == 0:
                log_mean_array = log_mean[:,newaxis]
                log_sigma_array = log_sigma[:,newaxis]
            else:
                new_axis = len(log_mean.shape)
                #concatenate((log_mean_array, log_mean[:,newaxis]),
                          #  axis=new_axis)
                #concatenate((log_sigma_array, log_sigma[:,newaxis]),
                 #           axis=new_axis)
                
            multi_log_mean.append(log_mean)
            multi_log_sigma.append(log_sigma)

        # dimensions of log_mean and log_sigma are (sites, events, periods)
        # note, sites is currently always 1.
        
        # FIXME Do we need to do this? Yes!
        # make multi_log_sigma all the same shape
        sigma_shape = [log_sigma.shape for log_sigma in multi_log_sigma]
        max_sigma_shape = []
        for i in range(len(sigma_shape[0])):
            max_sigma_shape.append(max([shape[i] for shape in sigma_shape]))
        max_sigma_shape = tuple(max_sigma_shape)
        max_sigma_array = zeros(max_sigma_shape)
        multi_log_sigma = [log_sigma+max_sigma_array
                           for log_sigma in multi_log_sigma]
        # End of code to make sigma all the same shape

        log_mean = concatenate(multi_log_mean,axis=1)
        log_sigma = concatenate(multi_log_sigma,axis=1)

        # The event_activity is used by save_event_set
        #print "Multiple_ground_motion_cal event_activity", event_activity
        #print "Multiple_ground_motion_calculator event_ids", event_ids
        return (log_mean, log_sigma, log_mean_array, log_sigma_array)

