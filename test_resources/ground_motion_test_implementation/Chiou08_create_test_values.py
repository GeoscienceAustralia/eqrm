#!/usr/bin/env python

"""A program to generate test data from BooreFTN output data.

Creates required python for test_ground_motion_specification.py.
"""

import re
import math
import numpy

# pattern string used to split fields seperated by 1 or more spaces
SpacesPatternString = ' +'

# generate 're' pattern for 'any number of spaces'
SpacesPattern = re.compile(SpacesPatternString)


def get_sets(data):
    """Read data rows and return sorted unique lists of:
        T, Mw, Rrup, Ztor, Vs30
    """

#Event_range = ((4.0, 0.0, 0), (5.5, 0.0, 0), (7.0, 0.0, 0),
#               (4.0, 5.0, 0), (5.5, 5.0, 0), (7.0, 5.0, 0),
#               (4.0, 10.0, 0), (5.5, 10.0, 0), (7.0, 10.0, 0))  # (Mw, Ztor, Fhw)
#Site_range = ((5, 300), (25, 300), (100, 300))                  # (Rjb, Vs30)

    T_set = set([])
#    Event_set = set([])
    Mw_set = set([])
    Ztor_set = set([])
#    Site_set = set([])
    Rrup_set = set([])
    Vs30_set = set([])

    for row in data:
        (T, Mw, Rrup, Ztor, Vs30, _, _) = row
#        Event_key = (Mw, Ztor)
#        Site_key = (Rrup, Vs30)
#
        T_set.add(T)
#        Event_set.add(Event_key)
#        Site_set.add(Site_key)

        Mw_set.add(Mw)
        Rrup_set.add(Rrup)
        Ztor_set.add(Ztor)
        Vs30_set.add(Vs30)

    T_result = list(T_set); T_result.sort()
#    Event_result = list(Event_set); Event_result.sort()
#    Site_result = list(Site_set); Site_result.sort()

    Mw_result = list(Mw_set); Mw_result.sort()
    Rrup_result = list(Rrup_set); Rrup_result.sort()
    Ztor_result = list(Ztor_set); Ztor_result.sort()
    Vs30_result = list(Vs30_set); Vs30_result.sort()

    return (T_result, Mw_result, Rrup_result, Ztor_result, Vs30_result)
#    return (T_result, Event_result, Site_result)

def read_file(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    lines = lines[6:]

    result = []
    for line in lines:
        line = line.strip()
        if line:
            fields = SpacesPattern.split(line)
            row = (fields[0], fields[1], fields[8], fields[20], fields[21], fields[45], fields[50])
            row = map(float, row)
            result.append(row)

    return result

def main():
    filename = 'Chiou08.out'
    data = read_file(filename)

    # process rows of data
    (T_list, Mw_list, Rrup_list, Ztor_list, Vs30_list) = get_sets(data)
#    (T_list, Event_list, Site_list) = get_sets(data)

    num_periods = len(T_list)
#    num_events = len(Event_list)
#    num_sites = len(Site_list)
    num_events = len(Mw_list)
    num_sites = len(Rrup_list)

    # output initial part of test data
    print('# num_periods = %d' % num_periods)
    print("test_data['Chiou08_test_period'] = %s" % str(T_list))
    print('')

    print('# num_events = %d' % num_events)
    print("test_data['Chiou08_test_magnitude'] = %s" % str(Mw_list))
    print('')

    print('# num_sites = %d' % num_sites)
    print('tmp = zeros((%d,%d)) # initialize an array: (num_sites, num_events)'
          % (num_sites, num_events))
    for i in range(len(Rrup_list)):
        d = '%5.1f' % Rrup_list[i]
        d_str = ''
        for j in range(len(Mw_list)):
            d_str += d + ', '
        d_str = d_str[:-2]
        print('tmp[%d,:] = [%s] # distance - site %d & all %d events'
              % (i, d_str, i+1, len(Mw_list)))
    print("test_data['Chiou08_test_distance'] = tmp")
    print('')
        
    print('# num_events = %d' % num_events)
    print("test_data['Chiou08_test_depth_to_top'] = %s" % str(Ztor_list))
    print('')

    print('# num_sites = %d' % num_sites)
    print("test_data['Chiou08_test_vs30'] = %.1f" % Vs30_list[0])
    print('')

    print("# mean values, in 'g'")
    print('tmp = zeros((%d,%d,%d))    # (num_sites, num_events, num_periods)'
          % (num_sites, num_events, num_periods))
    for row in data:
        (T, Mw, Rrup, Ztor, Vs30, mean, sigma) = row
        T_index = T_list.index(T)
        Mw_index = Mw_list.index(Mw)
        Rrup_index = Rrup_list.index(Rrup)
        Ztor_index = Ztor_list.index(Ztor)
        Vs30_index = Vs30_list.index(Vs30)

        print('tmp[%d,%d,%d] = %9.3E # Rrup=%5.1f, Mw=%.1f, T=%4.2f'
              % (Rrup_index, Mw_index, T_index, mean, Rrup, Mw, T))
    print("test_data['Chiou08_test_mean'] = tmp")
    print('')

    print("# sigma values, in 'g'")
    print('tmp = zeros((%d,%d,%d))    # (num_sites, num_events, num_periods)'
          % (num_sites, num_events, num_periods))
    for row in data:
        (T, Mw, Rrup, Ztor, Vs30, mean, sigma) = row
        T_index = T_list.index(T)
        Mw_index = Mw_list.index(Mw)
        Rrup_index = Rrup_list.index(Rrup)
        Ztor_index = Ztor_list.index(Ztor)
        Vs30_index = Vs30_list.index(Vs30)
        print('tmp[%d,%d,%d] = %9.3E # Rrup=%5.1f, Mw=%.1f, T=%4.2f'
              % (Rrup_index, Mw_index, T_index, sigma, Rrup, Mw, T))
    print("test_data['Chiou08_test_sigma'] = tmp")
    print('')

    print('del tmp')

if __name__ == '__main__':
    main()
