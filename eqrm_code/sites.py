"""
 Title: sites.py

  Author:  Peter Row, peter.row@ga.gov.au

  Description: Create a data structure to handle site data e.g.
  latitude, longitude and other attributes.

  Version: $Revision: 1700 $
  ModifiedBy: $Author: rwilson $
  ModifiedDate: $Date: 2010-06-16 16:42:33 +1000 (Wed, 16 Jun 2010) $

  Copyright 2007 by Geoscience Australia
"""

######
# A Sites object has three attributes:
#     .latitude    a vector of latitude values, one per site
#     .longitude   a vector of longitude values, one per site
#     .attributes  a dictionary of attributes names, each keying to
#                  a vector of attribute values
#
# Each vector is the same length as all the others and site 'i' values
# are latitude[i], longitude[i], attribute1[i], attribute2[i], ...
######


import copy
from scipy import array, asarray
import numpy as np

from eqrm_code.distances import Distances
from eqrm_code.csv_interface import csv_to_arrays
from eqrm_code.projections import azimuthal_orthographic as projection


class Sites(object):
    """An object to hold site data."""

    def __init__(self, latitude, longitude, **attributes):
        """Create a Sites object to handle multiple site data.

        latitude    latitude of sites (vector)
        longitude   longitude of sites (vector)
        attributes  dictionary of site attributes (vectors of data)
        """

        self.latitude = asarray(latitude)
        self.longitude = asarray(longitude)
        self.attributes = attributes

        assert(len(self.latitude) == len(self.longitude))
        for key in self.attributes:
            assert(len(self.latitude) == len(self.attributes[key]))

    @classmethod
    def from_csv(cls, file, **attribute_conversions):
        """Construct Site instance from csv file.

        file                   open file handle for site data
        attribute_conversions  dictionary defining required data from file and
                               format of the data
        use:
            X = Sites.from_csv('blg_wr.csv', PEOPLE=float,
                               WALLS=str, ROOF_TYPE=str)
        or:
            d = {'PEOPLE': float, 'WALLS': str, 'ROOF_TYPE': str}
            X = Sites.from_csv('blg_wr.csv', **d)
        """

        # force lat & lon - required attributes
        attribute_conversions["LATITUDE"] = float
        attribute_conversions["LONGITUDE"] = float

        # read in data from file
        sites_dict = csv_to_arrays(file, **attribute_conversions)

        # remove lat&lon from attributes dictionary
        latitude = sites_dict.pop("LATITUDE")
        longitude = sites_dict.pop("LONGITUDE")

        # copy remaining attributes - don't need user changes reflected
        attributes = copy.copy(sites_dict)

        # call class constructor
        return cls(latitude, longitude, **attributes)

    def __len__(self):
        """Make len() return number of sites."""

        return int(self.latitude.shape[0])

    def __getitem__(self, key):
        """Allow indexing/slicing of Sites object - return new Sites object."""

        if isinstance(key, int):
            key = [key]
        attributes = {}
        for k in self.attributes.keys():
            attributes[k] = self.attributes[k][key]

        return Sites(self.latitude[key], self.longitude[key], **attributes)

    def set_vs30(self, site_class2vs30):
        """Given a mapping from site_class to vs30, calculate the vs30 values
        for all of the sites.

        site_class2vs30    dictionary of 'site_class' and 'vs30' keys
        """
        # Calculate a vs30 value
        vs30_list = []
        for site_class in self.attributes['SITE_CLASS']:
            try:
                vs30_list.append(site_class2vs30[site_class])
            except KeyError:
                # FIXME The site class 2 VS30 mapping does not cover all
                # site classes.
                raise KeyError
        self.attributes['VS30'] = array(vs30_list)

    #FIXME consider moving to event set
    def distances_from_event_set(self, event_set, event_set_trace_starts=True):
        """
        The distance from self.sites to event_set.centroids.
        A big array-like object.
        """

        if event_set_trace_starts:
            return Distances(self.latitude,
                             self.longitude,
                             event_set.rupture_centroid_lat,
                             event_set.rupture_centroid_lon,
                             event_set.length,
                             event_set.azimuth,
                             event_set.width,
                             event_set.dip,
                             event_set.depth,
                             projection,
                             trace_start_lat=event_set.trace_start_lat,
                             trace_start_lon=event_set.trace_start_lon,
                             trace_start_x=event_set.trace_start_x,
                             trace_start_y=event_set.trace_start_y)
        else:
            return Distances(self.latitude,
                             self.longitude,
                             event_set.rupture_centroids_lat,
                             event_set.rupture_centroids_lon,
                             event_set.lengths,
                             event_set.azimuths,
                             event_set.widths,
                             event_set.dips,
                             event_set.depths,
                             projection)

    def join(self, other):
        """Method used to join two Sites objects.

        self   the first Sites object
        other  the other Sites object

        Returns a new Sites object containing both 'self' and 'other' data.
        The notional result is:

             lat  lon      attributes
             vvv  vvv  vvvvvvvvvvvvvvvvvvvvvvvvv

             +-+  +-+  +-+-+-------------------+
           > |.|  |.|  |.|.|.........|         |
         s > |.|  |.|  |.|.|.........|         |
         e > |.|  |.|  |.|.|..self...|   NaN   |
         l > |.|  |.|  |.|.|.........|         |
         f > |.|  |.|  |.|.|.........|         |
             +-+  +-+  +-+-+---------+---------+
         o > |.|  |.|  |.|.|         |.........|
         t > |.|  |.|  |.|.|         |.........|
         h > |.|  |.|  |.|.|   NaN   |..other..|
         e > |.|  |.|  |.|.|         |.........|
         r > |.|  |.|  |.|.|         |.........|
             +-+  +-+  +-+-+-------------------+

                       ^^^^^
                    common attributes

        where the lon & lat vectors are just concatenated.
        The common attributes are concatenated.
        The remaining attribute vectors are made final length with NaN in
        positions with no data.
        """

        # combine the lat&lon vectors
        new_lat = np.concatenate((self.latitude, other.latitude))
        new_lon = np.concatenate((self.longitude, other.longitude))

        # start new attributes dictionary, add in common attributes
        self_len = len(self.latitude)
        other_len = len(other.latitude)
        new_attr = {}
        common = []				# holds common column names
        for key in self.attributes:
            if key in other.attributes:
                common.append(key)		# remember what is common
                new_attr[key] = np.concatenate((self.attributes[key],
                                                other.attributes[key]))

        # now combine other *non-common* attribute vectors
        # first 'self' attributes
        for key in self.attributes:
            if key not in common:
                 new_attr[key] = np.concatenate((self.attributes[key], 
                                                 np.array([np.nan]*other_len)))
        # then 'other' attributes
        for key in other.attributes:
            if key not in common:
                 new_attr[key] = np.concatenate((np.array([np.nan]*self_len),
                                                 other.attributes[key]))

        return Sites(new_lat, new_lon, **new_attr)


# this sub-samples sites and is used if use_site_indexes>1
def truncate_sites_for_test(use_site_indexes, sites, site_indexes):
    """
    sitess are Site objects
    site_indexes is an array
    """
    # note: sites can be sliced like an array:
    #bad_blg=array([24, 25, 27, 29, 30, 53, 63, 77, 78, 82, 83, 85, 91, 97])-1
    #bad_blg=array([24, 25, 26, 27])-1
    #all_sites=all_sites[bad_blg]
    if use_site_indexes is True:
        site_ind = site_indexes
        return sites[site_ind-1] # -1 offset to match matlab
    else:
        return sites

