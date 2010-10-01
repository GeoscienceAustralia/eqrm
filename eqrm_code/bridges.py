"""
Classes and functions for holding bridge information.
 
Copyright 2010 by Geoscience Australia
"""


import copy

import structures
from eqrm_code.csv_interface import csv_to_arrays


# We expect users to provide something like:
#attribute_conversions = {'BID': int,
#                         'LATITUDE': float,
#                         'LONGITUDE': float,
#                         'STRUCTURE_CLASSIFICATION': str,
#                         'STRUCTURE_CATEGORY': str,
#                         'SKEW': float,
#                         'SPAN': int,
#                         'SITE_CLASS': str}


class Bridges(structures.Structures):
    """An object holding bridges data.

    Actually get a Bridges object by: Bridges.from_csv(...)
    """

    def __init__(self, latitude, longitude, **attributes): 
        """Contruct a Bridges object.

        latitude    a vector (tuple, list, ...) of latitude values
        longitude   a vector (tuple, list, ...) of longitude values
        attributes  a dictionary of bridge attributes
        """

        # latitude, longitude & attributes saved by Structures.__init__()
        structures.Structures.__init__(self, latitude, longitude, {},
                                       **attributes)


    @classmethod
    def from_csv(cls, file, **attribute_conversions):
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

        # force lat & lon - required columns
        attribute_conversions["LATITUDE"] = float
        attribute_conversions["LONGITUDE"] = float

        # read in data from file
        bridges_dict = csv_to_arrays(file, **attribute_conversions)

        # remove lat&lon from attributes dictionary
        latitude = bridges_dict.pop("LATITUDE")
        longitude = bridges_dict.pop("LONGITUDE")

        # copy remaining attributes - don't need user changes reflected
        attributes = copy.copy(bridges_dict)

        # call class constructor
        return cls(latitude, longitude, **attributes)


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

