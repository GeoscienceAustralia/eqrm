"""
Classes and functions for holding bridge information.
 
Copyright 2010 by Geoscience Australia
"""


import copy

from eqrm_code.csv_interface import csv_to_arrays
from eqrm_code.sites import Sites
from eqrm_code.damage_model import Bridge_damage_model
from eqrm_code.bridge_damage import choose_random_state
from eqrm_code.bridge_time_complete import time_to_complete
from eqrm_code.util import find_bridge_sa_indices


# data columns expected in a BRIDGE data file
attribute_conversions = {'BID': int,
                         'LONGITUDE': float,
                         'LATITUDE': float,
                         'STRUCTURE_CLASSIFICATION': str,
                         'STRUCTURE_CATEGORY': str,
                         'SKEW': float,
                         'SPAN': int,
                         'SITE_CLASS': str}


class Bridges(Sites):
    """An object holding bridges data.

    Actually get a Bridges object by: Bridges.from_csv(...)
    """

    def __init__(self, latitude, longitude, **attributes): 
        """Contruct a Bridges object.

        latitude    a vector (tuple, list, ...) of latitude values
        longitude   a vector (tuple, list, ...) of longitude values
        attributes  a dictionary of bridge attributes
        """

        Sites.__init__(self, latitude, longitude, **attributes)


    @classmethod
    def from_csv(cls, file):
        """Construct Bridges instance from csv file.

        file                   open file handle for site data
        attribute_conversions  dictionary defining required data from file and
                               format of the data
        use:
            X = Bridges.from_csv('blg_wr.csv', PEOPLE=float,
                                 WALLS=str, ROOF_TYPE=str)
        or:
            d = {'PEOPLE': float, 'WALLS': str, 'ROOF_TYPE': str}
            X = Bridges.from_csv('blg_wr.csv', **d)
        """
        
        # read in data from file
        bridges_dict = csv_to_arrays(file, **attribute_conversions)

        # remove lat&lon from attributes dictionary
        latitude = bridges_dict.pop("LATITUDE")
        longitude = bridges_dict.pop("LONGITUDE")

        # copy remaining attributes - don't need user changes reflected
        attributes = copy.copy(bridges_dict)

        # call class constructor
        return cls(latitude, longitude, **attributes)

    def calc_total_loss(self, SA, eqrm_flags, event_set_Mw):
        """
        Calculate the economic loss and damage state at a site.
    
        eqrm_flags      high level controlling object
        SA              array of Spectral Acceleration, in g, with axis;
                               sites, events, periods
                           the site axis usually has a size of 1
    
        Returns a tuple (total_loss, damage_model) where:
          total_loss    a 4 long list of dollar loss.  The loss categories are;
                        (structure_loss, nsd_loss, accel_loss, contents_loss)
                        These dollar losses have the dimensions of;
                        (site, event)
          damage_model  an instance of the damage model.
                        used in risk.py to get damage states.
        """        
        # get indices of SA periods 0.3 and 1.0
        sa_indices = find_bridge_sa_indices(eqrm_flags.atten_periods)
        # until we *have* a eqrm_flags.bridge_model value, pass None for model
        damage_model = Bridge_damage_model(self, None, SA,
                                           eqrm_flags.atten_periods,
                                           sa_indices)
        states = damage_model.get_states()    # to set up self.structure_state
        state = choose_random_state(states[0])
        total_loss = damage_model.aggregated_loss()

        if eqrm_flags.bridges_functional_percentages is not None:
            # calculate days to complete for each bridge
            days_to_complete = time_to_complete(eqrm_flags.bridges_functional_percentages,
                                                state)
        else:
            days_to_complete = None
                
    
        return (total_loss, damage_model, days_to_complete)

    def __getitem__(self, key):
        """Get single indexed entry from a Bridges object."""

        # if 'key' is naked int, make a list
        if isinstance(key, int):
            key = [key]

        # get indexed .attributes
        attributes = {}
        for k in self.attributes.keys():
            attributes[k] = self.attributes[k][key]

        # get final Sites object
        return Bridges(self.latitude[key], self.longitude[key],
                       **attributes)


