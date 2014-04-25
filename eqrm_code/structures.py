"""
 Title: structures.py

  Author:  Peter Row, peter.row@ga.gov.au
           Duncan Gray, duncan.gray@ga.gov.au

  Description: Classes and functions for holding structure information.

  Version: $Revision: 1716 $
  ModifiedBy: $Author: rwilson $
  ModifiedDate: $Date: 2010-06-18 13:58:01 +1000 (Fri, 18 Jun 2010) $

  Copyright 2007 by Geoscience Australia
"""


from os.path import join
from scipy import where, array, asarray, allclose, sum
import numpy as np
import copy

from eqrm_code.csv_interface import csv_to_arrays, csv2dict
from eqrm_code.sites import Sites
from eqrm_code.building_params_from_csv import building_params_from_csv
from eqrm_code.util import determine_eqrm_path
from eqrm_code.damage_model import Damage_model


attribute_conversions = {'LATITUDE': float,
                         'LONGITUDE': float,
                         'STRUCTURE_CLASSIFICATION': str,
                         'HAZUS_STRUCTURE_CLASSIFICATION': str,
                         'STRUCTURE_CATEGORY': str,
                         'CONTENTS_COST_DENSITY': float,
                         'BUILDING_COST_DENSITY': float,
                         'FLOOR_AREA': float,
                         'SURVEY_FACTOR': float,
                         'FCB_USAGE': int,
                         'HAZUS_USAGE': str,
                         'BID': int,
                         'POSTCODE': int,
                         'SUBURB': str,
                         'SITE_CLASS': str,
                         'PRE1989': int}


class Structures(Sites):

    def __init__(self,
                 latitude,
                 longitude,
                 building_parameters,
                 **attributes):
        """Create an object holding all Structures data.

        Inherits from Sites which handles lat, lon and attributes.  Structures
        adds the 'building_parameters' attribute which must be handled
        specially.  Compare this with the handling of 'extra' classification
        data in the Bridges class.

        TODO: make extra data here be handled in a similar way as in Bridges?
        """

        # inherit setup from Sites, add building parameters
        Sites.__init__(self, latitude, longitude, **attributes)
        self.building_parameters = building_parameters

    @classmethod
    def from_csv(cls,
                 sites_filename,
                 building_classification_tag,
                 damage_extent_tag,
                 default_input_dir,
                 input_dir=None,
                 eqrm_dir=None,
                 buildings_usage_classification='HAZUS',
                 use_refined_btypes=True,
                 force_btype_flag=False,
                 determ_btype=None,
                 determ_buse=None,
                 loss_aus_contents=0):
        """Read structures data from a file.
        Extract strucuture parameters from building_parameters_table.

        parameters
          sites_filename is actually a file handle

            - some parameters depend on structure classification (hazus or
              refined hazus, depending on use_refined_btypes)

            - some parameters depend on usage (fcb or hazus, depending on
              use_fcb_usage)

            - force_btype_flag will force all buildings to be of type
              determ_btype, and usage determ_buse.

              See page 11 of the tech manual to understand the flags

              refined_btypes = Edwards building classification
        """

        if eqrm_dir is None:
            eqrm_dir = determine_eqrm_path(__file__)

        if force_btype_flag:
            raise NotImplementedError
        sites_dict = csv_to_arrays(sites_filename, **attribute_conversions)

        latitude = sites_dict.pop("LATITUDE")
        longitude = sites_dict.pop("LONGITUDE")

        # create copy of attributes
        attributes = copy.copy(sites_dict)

        # Do we use refined_btypes or hazus btypes?
        if not use_refined_btypes:
            attributes['STRUCTURE_CLASSIFICATION'] = \
                attributes['HAZUS_STRUCTURE_CLASSIFICATION']

        # building_parameters_table has alot of info read in from
        # varrious files in resources data.
        # it is a dic, when the key signifies what the info is about, eg
        # height, ductility.  The index of the data represents the structure
        # classification, which is stored in
        # building_parameters_table['structure_classification']
        building_parameters_table = \
            building_params_from_csv(building_classification_tag,
                                     damage_extent_tag,
                                     default_input_dir=default_input_dir,
                                     input_dir=input_dir)

        # get index that maps attributes ->
        #    building_parameters_table (joined by 'structure_classification')
        structure_classification = attributes['STRUCTURE_CLASSIFICATION']
        building_parameter_index = \
            get_index(
                building_parameters_table['structure_classification'],
                structure_classification)

        # Now extract building_parameters from the table,
        # using building_parameter_index
        building_parameters = {}
        for key in building_parameters_table.keys():
            building_parameters[key] = \
                building_parameters_table[key][building_parameter_index]

        # Get non-structural drift thesholds (depending on whether or not
        # they are residential)
        # extract usage dependent parameters
        if buildings_usage_classification is 'HAZUS':
            usages = attributes['HAZUS_USAGE']
            is_residential = (array([(usage[0:4] in ['RES1', 'RES2', 'RES3'])
                                     for usage in usages]))
        elif buildings_usage_classification is 'FCB':
            usages = attributes['FCB_USAGE']
            is_residential = ((usages <= 113) + (usages == 131))
        else:
            msg = ('b_usage_type_flat = ' + str(buildings_usage_classification)
                   + " not 'FCB' or 'HAZUS'")
            raise ValueError(msg)

        is_residential.shape = (-1, 1)  # reshape so it can be broadcast
        nr = building_parameters['non_residential_drift_threshold']
        r = building_parameters['residential_drift_threshold']
        drift_threshold = r * is_residential + nr * (1 - is_residential)
        building_parameters['drift_threshold'] = drift_threshold

        is_residential.shape = (-1,)
        if loss_aus_contents == 1:
            attributes['CONTENTS_COST_DENSITY'] *= \
                (is_residential * 0.6 + (is_residential - 1)
                 * 1.0)  # reduce contents

        rcp = build_replacement_ratios(usages, buildings_usage_classification)
        building_parameters['structure_ratio'] = rcp['structural']
        building_parameters['nsd_d_ratio'] = \
            rcp['nonstructural drift sensitive']
        building_parameters['nsd_a_ratio'] = \
            rcp['nonstructural acceleration sensitive']

        # create structures:
        return cls(latitude, longitude, building_parameters, **attributes)

    def cost_breakdown(self, ci=None):
        """Work-out the 3 building costs plus contents cost.

        ci  regional cost index multiplier
        """

        # FIXME Most of this can be precomputed.
        floor_area = self.attributes['FLOOR_AREA']
        structure_cost = self.attributes['BUILDING_COST_DENSITY'] * floor_area
        contents_cost = self.attributes['CONTENTS_COST_DENSITY'] * floor_area

        structure_cost *= self.attributes['SURVEY_FACTOR']
        contents_cost *= self.attributes['SURVEY_FACTOR']

        if ci is not None:
            structure_cost *= ci
            contents_cost *= ci
        structure_ratio = self.building_parameters['structure_ratio']
        nsd_d_ratio = self.building_parameters['nsd_d_ratio']
        nsd_a_ratio = self.building_parameters['nsd_a_ratio']
        total_costs = (structure_ratio * structure_cost,
                       nsd_d_ratio * structure_cost,
                       nsd_a_ratio * structure_cost,
                       contents_cost)
        return total_costs

    def calc_total_loss(self, SA, eqrm_flags, event_set_Mw):
        """
        Calculate the economic loss and damage state at a site.

        eqrm_flags        high level controlling object
        SA                 array of Spectral Acceleration, in g, with axis;
                               sites, events, periods
                           the site axis usually has a size of 1
        event_set_Mw       array of Mw, 1D, dimension (events)
                           (used only by buildings)

        Returns a tuple (total_loss, damage_model) where:
          total_loss    a 4 long list of dollar loss.  The loss categories are;
                        (structure_loss, nsd_loss, accel_loss, contents_loss)
                        These dollar losses have the dimensions of;
                        (site, event)
          damage_model  an instance of the damage model.
                        used in risk.py to get damage states.
        """
        # note: damage_model has an object called capacity_spectrum_model
        #       buried inside, which will now calculate capacity curves
        #       parameters
        # csm_params are parameters for the capacity_spectrum_model
        csm_params = {'csm_damping_regimes':
                      eqrm_flags.csm_damping_regimes,
                      'csm_damping_modify_Tav':
                      eqrm_flags.csm_damping_modify_Tav,
                      'csm_damping_use_smoothing':
                      eqrm_flags.csm_damping_use_smoothing,
                      'rtol':
                      eqrm_flags.csm_SDcr_tolerance_percentage / 100.0,
                      'csm_damping_max_iterations':
                      eqrm_flags.csm_damping_max_iterations,
                      'sdtcap':  # FIXME sdt -> std
                      eqrm_flags.csm_standard_deviation,
                      'csm_use_variability':
                      eqrm_flags.csm_use_variability,
                      'csm_variability_method':
                      eqrm_flags.csm_variability_method,
                      'csm_hysteretic_damping':
                      eqrm_flags.csm_hysteretic_damping,
                      'atten_override_RSA_shape':
                      eqrm_flags.atten_override_RSA_shape,
                      'atten_cutoff_max_spectral_displacement':
                      eqrm_flags.atten_cutoff_max_spectral_displacement,
                      'loss_min_pga': eqrm_flags.loss_min_pga}

        damage_model = Damage_model(self, SA, eqrm_flags.atten_periods,
                                    event_set_Mw,
                                    eqrm_flags.csm_use_variability,
                                    float(eqrm_flags.csm_standard_deviation),
                                    csm_params=csm_params)

        # Note, aggregate slight, medium, critical damage
        # Compute building damage and loss (LOTS done here!)
        total_loss = \
            damage_model.aggregated_building_loss(
                ci=eqrm_flags.loss_regional_cost_index_multiplier,
                loss_aus_contents=eqrm_flags.loss_aus_contents)

        return (total_loss, damage_model)

    def __getitem__(self, key):
        """Get single indexed entry from a Structures object."""

        # if 'key' is naked int, make a list
        if isinstance(key, int):
            key = [key]

        # get indexed .attributes
        attributes = {}
        for k in self.attributes.keys():
            attributes[k] = self.attributes[k][key]

        # and indexed .building_parameters
        building_parameters = {}
        for k in self.building_parameters.keys():
            building_parameters[k] = self.building_parameters[k][key]

        # create shiny new Structures object with this single structure
        return Structures(self.latitude[key], self.longitude[key],
                          building_parameters, **attributes)

    def join(self, other):
        """Join data from a Structures object with some other object.

        Just call the parent join(), copying self.attributes to result.
        Also extend the .building_parameters dictionary elements to new length.
        We must return a Structures object to include Structures methods.
        """

        # do the vanilla data join from the parent class (Sites)
        joined = super(Structures, self).join(other)

        # extend .building_parameters dictionary entries to new joined length
        # this is to allow .__getitem__() above to work on the join result
        new_building_parameters = copy.copy(self.building_parameters)
        new_len = len(joined)
        for k in new_building_parameters.keys():
            new_shape = list(new_building_parameters[k].shape)
            new_shape[0] = new_len
            new_building_parameters[k] = np.resize(
                new_building_parameters[k],
                new_shape)

        # return joined Structures object with .building_parameters from self
        return Structures(joined.latitude, joined.longitude,
                          new_building_parameters, **joined.attributes)


def get_index(key_order, desired_keys):
    """This is used to map from a usage string/int to an index int.
    eg. FCB usage of 111 is 1.
    HAZUS_USAGE of RES1 is 1.
    These values are then used in tables to determine non_structural
    drift ratio

    Input: 2 arrays, one of which contains a unique list
    of keys in a canononical order:
        key_order = known_pets = ['cat','dog','hamster']

    the other contains a list of keys in a desired_keys:
        desired_keys = my_pets = ['cat','dog','cat']

    returns a list of indexes such that:
        key_order[answer]=desired_keys

    Why:
        If I have another array in the same order as key_order:
           weight=[2,3,0.5]
        then:
            weight[answer]=[weight[where(key_order==key)]
                            for key in desired_keys]

    This should offer a speedup if a lot of fields (ie weight,
    food, licence number ...) are to be looked up.

    The other option is to ask the user to know what the
    indexes will be, but this can get problematic if new keys
    are added (ie new_known_pets=['cat','dog','python','hamster'])
    """

    # Ceate a mapping, {name -> number}
    key_to_index = {}
    for (index, key) in enumerate(key_order):
        # check uniqueness
        assert key not in key_to_index
        key_to_index[key] = index

    # Map desired names to numbers
    return array([key_to_index[key] for key in desired_keys])


def build_par_file(buildpars_flag):
    # Build lookup table for building parameters
    buildpars_map = {0: 'building_parameters_workshop_1',
                     1: 'building_parameters_workshop',
                     2: 'building_parameters_hazus',
                     3: 'building_parameters_workshop_2',
                     4: 'building_parameters_workshop_3'}

    # create links to required building parameters
    if isinstance(buildpars_flag, str):
        buildpars = 'building_parameters_' + buildpars_flag
    else:
        buildpars = buildpars_map[buildpars_flag]

    return buildpars


def build_replacement_ratios(usage_per_struct, buildings_usage_classification):
    """Return an array of the building components replacement cost ratios.
    shape (# of buildings, 3 (# of components in a structure))

    A structure has 3 components;
      structural
      nonstructural acceleration sensitive
      nonstructural drift sensitive

    The ratio of the replacement cost for each component differs for
    different usage types.

    Also, there are two scales of usage types;
      Functional classification of buildings (FCB)(ABS usage)
      HAZUS usage

    Parameters:
      usage_per_struct: An array, shape (# of buildings) of usage
        values for each structure.
      buildings_usage_classification: The usage scale used.

    Return:
      A dictionary of cost ratios for the strucutures.
      The keys are the structural components;
        'structural', 'nonstructural drift sensitive',
        'nonstructural acceleration sensitive'

    Note: This should only be used once, since it is loading a file.
    """

    usage_column = 'Functional classification of buildings (ABS usage)'
    components = ['structural', 'nonstructural drift sensitive',
                  'nonstructural acceleration sensitive']
    convert = {}

    # extract usage dependent parameters
    if buildings_usage_classification is 'HAZUS':  # HAZUS_USAGE
        file = 'replacement_cost_ratios_wrt_HAZUS_Usage.csv'
    elif buildings_usage_classification is 'FCB':  # FCB_USAGE
        file = 'replacement_cost_ratios_wrt_FCB_Usage.csv'
        convert[usage_column] = int
    else:
        msg = ('b_usage_type_flat = ' + str(buildings_usage_classification)
               + ' not "FCB" or "HAZUS"')
        raise ValueError(msg)

    for comp in components:
        convert[comp] = float

    root_dir = determine_eqrm_path()
    data_dir = join(root_dir, 'resources', 'data')
    (att_dic, _) = csv2dict(join(data_dir, file), convert=convert)

    # This way does not have an assert
    # Build a dict with
    # key (usage, component), value = cost ratio
#     cost_ratios = {}
#     for comp in components:
#         tmp = {}
#         for i,usage in enumerate(att_dic[usage_column]):
#             tmp[usage] = att_dic[comp][i]
#         cost_ratios[comp] = tmp

#     replacement_cost_ratios = {}
#     for comp in components:
#         this_cost_ratios = cost_ratios[comp]
#         tmp = [this_cost_ratios[usage] for usage in usage_per_struct]
#         replacement_cost_ratios[comp] = array(tmp)

    cost_ratios = {}
    for (i, usage) in enumerate(att_dic[usage_column]):
        cost_ratios[usage] = [att_dic[components[0]][i],
                              att_dic[components[1]][i],
                              att_dic[components[2]][i]]

    rcp_array = asarray([cost_ratios[usage] for usage in usage_per_struct])
    assert allclose(sum(rcp_array), rcp_array.shape[0], 0.0000001)

    replacement_cost_ratios = {}
    for (i, comp) in enumerate(components):
        replacement_cost_ratios[comp] = rcp_array[:, i]

    return replacement_cost_ratios
