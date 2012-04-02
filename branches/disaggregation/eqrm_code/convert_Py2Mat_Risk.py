#!/usr/bin/env python

"""
Read all python data files into memory.
Returns a python object with attributes for each
file dataset:
    obj.ecbval2
    obj.rjb
    obj.aus_mag
    obj.nu
    obj.latitude
    obj.longitude
    obj.pre1989
    obj.postcode
    obj.site_class
    obj.suburb
    obj.survey_factor
    obj.structure_classification
    obj.hazus_structure_classification
    obj.bid
    obj.fcb_usage
    obj.hazus_usage

The attributes are either lists or numpy 1D arrays.

Copyright 2007 by Geoscience Australia

"""


import os
import numpy as num
import re

import eqrm_code.eqrm_filesystem as eqrm_filesystem
import eqrm_code.util as util


# we should get this from a parameter (file or *.py)
SiteLoc = 'newc'

# result object
class Result(object):
    pass


# get regular expression to parse line delimited by whitespace or commas
SplitPattern = re.compile(' +| *, *')


def process_file(filename, line_handler, skip=0):
    """Load a data file and call a handler for each line.
    Handler returns an object that is appended to a result list.

    filename      is the path to the file to open
    line_handler  a line handler function
    skip          the number of header lines to skip

    Ignore all blank lines and those starting with '%' or '#'.

    Values in the line may be separated by whitespace or commas.
    """

    # get data from file
    fd = open(filename, 'r')
    lines = fd.readlines()
    fd.close()

    # skip header lines
    if skip > 0:
        lines = lines[skip:]

    # start collecting rows
    result = []
    for line in lines:
        line = line.strip()

        # ignore blank or comment lines
        if line == '' or line[0] in '%#':
            continue

        # split line into fields, append to result
        if line:
            data = line_handler(SplitPattern.split(line))
            result.append(data)

    return result


def load_data(filename):
    """Load a data file of MxN float values into a numpy array.

    Ignore all blank lines and those starting with '%' or '#'.

    Values in the line may be separated by whitespace or commas.
    """

    def handler(fields):
        return [float(f) for f in fields]
        
    result = process_file(filename, handler)

    return num.array(result)


def load_btype_index(filename):
    """Load a building type index file into an Nx1 list of strings.

    Ignore all blank lines and those starting with '%' or '#'.
    """

    def handler(fields):
        return fields[0]
        
    result = process_file(filename, handler)

    return result


def load_usage_index(filename):
    """Load a building usage index file into an Nx1 list of strings.

    Ignore all blank lines and those starting with '%' or '#'.
    """

    def handler(fields):
        return fields[0]
        
    result = process_file(filename, handler)

    return result


def load_suburb_index(filename):
    """Load a suburb file into an Nx1 list of strings.

    Ignore all blank lines and those starting with '%' or '#'.
    """

    def handler(fields):
        return fields[0]
        
    result = process_file(filename, handler)

    return result


def load_struct_data(filename):
    """Load a data file of structure values into arrays.

    Ignore all blank lines and those starting with '%' or '#'.

    Values in the line may be separated by whitespace or commas.
    """

    def handler(fields):
        (b_lat, b_lon, b_post89, b_postcode, b_soil, str_suburb, b_survfact,
         str_btype, str_haztype, b_ufi, fcb_usage, hazus_usage) = fields

        # replace underlines in suburb name with spaces
        str_suburb = str_suburb.replace('_', ' ')

        return [float(b_lat), float(b_lon), int(b_post89), int(b_postcode),
                b_soil, str_suburb, float(b_survfact), str_btype,
                str_haztype, float(b_ufi), float(fcb_usage), hazus_usage]
        
    result = process_file(filename, handler, skip=1)

    return result


def convert_btype_to_btypeindex(saved_struct, default_data):
    """Convert btype column in saved_struct to btype INDEX.

    saved_struct  list of lists: [..., btype, ...]
    default_data  path to data directory
    """

    index_file = os.path.join(default_data, 'textbtypes.txt')
    index_data = load_btype_index(index_file)

    for row in saved_struct:
        try:
            row[7] = index_data.index(row[7])
        except ValueError, e:
            msg = ("Field 7 (%s) doesn't exist in BTypes file %s!?"
                   % (row[7], index_file))
            raise RuntimeError(msg)


def convert_uses_to_usesindex(saved_struct, default_data):
    """Convert hazus_usage column in saved_struct to hazus_usage INDEX.

    saved_struct  list of lists: [..., btype, ...]
    default_data  path to data directory
    """

    index_file = os.path.join(default_data, 'textbtypes.txt')
    index_data = load_btype_index(index_file)

    for row in saved_struct:
        try:
            row[11] = index_data.index(row[11])
        except ValueError, e:
            msg = ("Field 11 (%s) doesn't exist in BTypes file %s!?"
                   % (row[11], index_file))
            raise RuntimeError(msg)


def convert_suburb_to_suburbindex(saved_struct, default_data):
    """Convert suburb column in saved_struct to suburb INDEX.

    saved_struct  list of lists: [..., btype, ...]
    default_data  path to data directory
    """

    index_file = os.path.join(default_data, 'suburb_postcode.csv')
    index_data = load_suburb_index(index_file)

    for row in saved_struct:
        try:
            row[5] = index_data.index(row[5])
        except ValueError, e:
            msg = ("Field 5 (%s) doesn't exist in Postcodes file %s!?"
                   % (row[5], index_file))
            raise RuntimeError(msg)


def obsolete_convert_Py2Mat_Risk(site_tag, datadir, param_t, default_data=None):
    """Get python data as attributes of object.

    site_tag     Site Location (?) should get from PARAM_T (whatever *that* is)
    datadir      path to directory containing data
    param_t      name of the PARAM_T file
    default_data path to default data directory

    Returns a data object.  See module docstring.
    """

    # get EQRM root path
    eqrm_path = util.determine_eqrm_path()

    # handle missing default_data
    if default_data is None:
        default_data = os.path.join(eqrm_path,
                                    eqrm_filesystem.Resources_Data_Path)

    # easy stuff
    saved_ecbval2_file = os.path.join(eqrm_path,
                                      eqrm_filesystem.Demo_Output_ProbRisk_Path,
                                      site_tag + '_bval.txt')
    saved_ecbval2 = load_data(saved_ecbval2_file)
    saved_ecbval2 = num.array(saved_ecbval2).flat[:]    # make a row vector

    saved_rjb_file = os.path.join(eqrm_path,
                                  eqrm_filesystem.Demo_Output_ProbRisk_Path,
                                  site_tag + '_distance_rjb.txt')
    saved_rjb = load_data(saved_rjb_file)
    saved_rjb = saved_rjb.transpose()

    # get loss values - note: we only do contents+building
    saved_ecloss_file = os.path.join(eqrm_path,
                                     eqrm_filesystem.Demo_Output_ProbRisk_Path,
                                     site_tag + '_total_building_loss.txt')
    saved_ecloss = load_data(saved_ecloss_file)
    saved_ecloss = saved_ecloss[1:]     # strip building ID row
    saved_ecloss = saved_ecloss.transpose()

    # get aus_mag and nu data
    tmp1_file = os.path.join(eqrm_path,
                             eqrm_filesystem.Demo_Output_ProbRisk_Path,
                             site_tag + '_event_set.txt')
    tmp1 = load_data(tmp1_file)
    nu = tmp1[:,8]
    aus_mag = tmp1[:,9]

    # structure information
    saved_struct_file = os.path.join(eqrm_path,
                                     eqrm_filesystem.Demo_Output_ProbRisk_Path,
                                     site_tag + '_structures.txt')
    print('saved_struct_file=%s' % saved_struct_file)
    saved_struct = load_struct_data(saved_struct_file)
    # convert certain fields in-situ
    convert_btype_to_btypeindex(saved_struct, default_data)
    convert_uses_to_usesindex(saved_struct, default_data)
    convert_suburb_to_suburbindex(saved_struct, default_data)

    # create result object, add data attributes
    result = Result()
    
    result.ecbval2 = num.array(saved_ecbval2)
    result.ecloss = num.array(saved_ecloss)
    result.rjb = num.array(saved_rjb)
    result.aus_mag = num.array(aus_mag)
    result.nu = num.array(nu)

    # convert structures array to lists, add to data attributes
    result.latitude = num.array([x[0] for x in saved_struct])
    result.longitude = num.array([x[1] for x in saved_struct])
    result.pre1989 = [x[2] for x in saved_struct]
    result.postcode = num.array([x[3] for x in saved_struct])
    result.site_class = [x[4] for x in saved_struct]
    result.suburb = [x[5] for x in saved_struct]
    result.survey_factor = num.array([x[6] for x in saved_struct])
    result.structure_classification = [x[7] for x in saved_struct]
    result.hazus_structure_classification = [x[8] for x in saved_struct]
    result.bid = num.array([x[9] for x in saved_struct])
    result.fcb_usage = num.array([x[10] for x in saved_struct])
    result.hazus_usage = [x[11] for x in saved_struct]

    return result


if __name__ == '__main__':
    import pprint as pp
    
    result = convert_Py2Mat_Risk(SiteLoc, None, None)

    print('result.ecbval2: %s' % str(num.shape(result.ecbval2)))
    pp.pprint(result.ecbval2)
    print('result.ecloss: %s' % str(num.shape(result.ecloss)))
    pp.pprint(result.ecloss)
    print('result.rjb: %s' % str(num.shape(result.rjb)))
    pp.pprint(result.rjb)
    print('result.aus_mag: %s' % str(num.shape(result.aus_mag)))
    pp.pprint(result.aus_mag)
    print('result.nu: %s' % str(num.shape(result.nu)))
    pp.pprint(result.nu)
    print('result.structures:')
    pp.pprint(result.structures)
