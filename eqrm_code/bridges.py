"""
Classes and functions for holding bridge information.
 
Copyright 2010 by Geoscience Australia
"""


from eqrm_code.sites import Sites


# We expect users to provide something like:
#attribute_conversions = {'BID': int,
#                         'LATITUDE': float,
#                         'LONGITUDE': float,
#                         'STRUCTURE_CLASSIFICATION': str,
#                         'STRUCTURE_CATEGORY': str,
#                         'SKEW': float,
#                         'SPAN': int,
#                         'SITE_CLASS': str}


class Bridges(Sites):
    """An object holding bridges data.

    Actually get a Bridges object by: Bridges.from_csv(...)
    This is done this way and not the traditional way for some reason!?
    """

    def __init__(self, latitude, longitude, **attributes): 
        """Contruct a Bridges object.

        latitude    a vector (tuple, list, ...) of latitude values
        longitude   a vector (tuple, list, ...) of longitude values
        attributes  a dictionary of bridge attributes
        """

        # latitude, longitude & attributes saved by Sites.__init__()
        Sites.__init__(self, latitude, longitude, **attributes)


    # .from_csv() and .__get_item__() inherited from Sites class
    # .__init__() is same as in Sites class, but we must have *some* code here!


