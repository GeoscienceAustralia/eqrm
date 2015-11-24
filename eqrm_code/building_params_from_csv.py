""" Read in several building parameter files.

 Title: building_params_from_csv.py

  Description: Read in a building parameter file, such as
  building_parameters_workshop_3.

  Version: $Revision: 1133 $
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-09-16 17:34:02 +1000 (Wed, 16 Sep 2009) $

"""

from scipy import array, asarray, newaxis

from eqrm_code.csv_interface import csv_to_arrays
from eqrm_code.util import get_local_or_default

# ie bp=building_params_from_csv('building_parameters_workshop_3')


def building_params_from_csv(building_classification_tag,
                             damage_extent_tag,
                             default_input_dir,
                             input_dir=None):
    """create building parameters dictionary
    This loads the building_parameters_workshop file, as well
    as other building related files that are hard-coded in this function.

    Args:
      csv_name: The name of the parameter file with the _params.csv
      part removed, eg building_parameters_workshop_3
      main_dir: the python_eqrm directory

    Returns:
      A dict with the parameter info.
    """

    # Get the data out of _params.csv
    attribute_conversions = {}
    attribute_conversions['structure_class'] = str
    attribute_conversions['structure_classification'] = str
    for name in ['design_strength', 'height', 'natural_elastic_period',
                 'fraction_in_first_mode', 'height_to_displacement',
                 'yield_to_design', 'ultimate_to_yield', 'ductility',
                 'damping_s', 'damping_m', 'damping_l', 'damping_Be',
                 'structural_damage_slight', 'structural_damage_moderate',
                 'structural_damage_extreme', 'structural_damage_complete']:
        attribute_conversions[name] = float
    fid = get_local_or_default(
        'building_parameters%s.csv' % building_classification_tag,
        default_input_dir,
        input_dir)

    #file_location = join(default_input_dir, csv_name+'_params.csv')
    building_parameters = csv_to_arrays(fid, **attribute_conversions)

    # Get the data out of _non_structural_damage_params.csv
    attribute_conversions = {}
    for name in ['non_residential_drift_threshold',
                 'residential_drift_threshold', 'acceleration_threshold']:
        attribute_conversions[name] = float
    fid = get_local_or_default('damage_extent%s.csv' % damage_extent_tag,
                               default_input_dir,
                               input_dir)
    building_nsd_parameters = csv_to_arrays(fid, **attribute_conversions)

    for name in ['non_residential_drift_threshold',
                 'residential_drift_threshold',
                 'acceleration_threshold']:
        building_parameters[name] = building_nsd_parameters[name][newaxis, :]

    # transform the data:
    #     turn height from feet to mm
    #     multiply drift damage by height
    # return building_parameters
    cvt_in2mm = 25.40
    # Conversion for structural damage
    # building height: convert feet to inches to mm
    building_parameters['height'] *= 12 * cvt_in2mm
    height_to_displacement = building_parameters['height_to_displacement']
    height = building_parameters['height']

    # setup damage state median thresholds (also feet -> mm)
    structural_damage_slight = building_parameters.pop(
        'structural_damage_slight')
    structural_damage_moderate = building_parameters.pop(
        'structural_damage_moderate')
    structural_damage_extreme = building_parameters.pop(
        'structural_damage_extreme')
    structural_damage_complete = building_parameters.pop(
        'structural_damage_complete')
    structural_damage_threshold = asarray((structural_damage_slight,
                                           structural_damage_moderate,
                                           structural_damage_extreme,
                                           structural_damage_complete))
    try:
        structural_damage_threshold = structural_damage_threshold.swapaxes(0, 1)
    except ValueError:  # to avoid error with numpy version > 1.10.1
        pass

    structural_damage_threshold = structural_damage_threshold * (
        (height_to_displacement * height)[:, newaxis])
    building_parameters[
        'structural_damage_threshold'] = structural_damage_threshold

    # setup damage state median thresholds (also feet -> inches)
    non_residential_drift_threshold = building_parameters[
        'non_residential_drift_threshold']
    non_residential_drift_threshold = non_residential_drift_threshold * (
        (height_to_displacement * height)[:, newaxis])

    building_parameters[
        'non_residential_drift_threshold'] = non_residential_drift_threshold

    residential_drift_threshold = building_parameters[
        'residential_drift_threshold']
    residential_drift_threshold = residential_drift_threshold * (
        (height_to_displacement * height)[:, newaxis])
    building_parameters[
        'residential_drift_threshold'] = residential_drift_threshold

    # expand acceleleration_threshold to be the same size as the rest.
    acceleration_threshold = building_parameters['acceleration_threshold']
    acceleration_threshold = acceleration_threshold + 0 * height[:, newaxis]
    building_parameters['acceleration_threshold'] = acceleration_threshold

    return building_parameters


def matlab_to_array(f):
    answer = [[float(v) for v in line.split(' ') if not v == '']
              for line in f if not line.strip(' ') == '']
    answer = array(answer)
    return answer
