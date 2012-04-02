#!/usr/bin/env python

"""A program to take the output from the FORTRAN program and make
unittest code for Campbell08."""

import sys
import re
import numpy
import math

# pattern string used to split fields seperated by 1 or more spaces
SpacesPatternString = ' +'

# generate 're' pattern for 'any number of spaces'
SpacesPattern = re.compile(SpacesPatternString)

if len(sys.argv) != 2:
    print('usage: %s <CTL_output>' % sys.argv[0])
    sys.exit(10)

CTL_data_file = sys.argv[1]


Num_CTL_headers = 6
CTL_fields = {'T': 0,    # field name, index
              'M': 1,
              'Rjb': 4,
              'Rrup': 8,  # actually Rrup_use
              'Rake': 14,
              'Dip': 16,
              'Ztor': 19,
              'Vs30': 21,
              'Z25': 26,
              'Sa': 40,
              'sigma': 44}


def rake_to_fault_type(rake):
    if (-120.0 <= rake) and (rake <= -60.0):
        return (1, 'normal')
    if (0.0 <= rake <= 30.0) or (150.0 <= rake <= 180.0):
        return (2, 'strike slip')

    return (0, 'reverse')



def read_file(filename, num_headers, field_dict):
    """Read the python and return a list of values from the file."""

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    # strip header lines
    lines = lines[num_headers:]

    # step through lines, picking up required fields
    result = []
    for line in lines:
        line = line.strip()
        if line:
            fields = SpacesPattern.split(line)
            for key in CTL_fields:
                exec_str = '%s = %s' % (key, fields[field_dict[key]])
                #                print('exec_str: %s' % exec_str)
                try:
                    exec(exec_str)
                except NameError:
                    print('exec_str=%s' % exec_str)
                    print('field index=%d' % field_dict[key])
                    sys.exit(0)
            result.append((T, M, Rjb, Rrup, Rake, Dip, Ztor, Vs30, Z25, Sa, sigma))

    return result


def write_code(cases):
    """For each case, write unittest code."""

    # set main code indent
    indent = ' ' * 8

    # write test file header
    print('''#!/usr/bin/env python

import unittest
from scipy import array, allclose
from eqrm_code.ground_motion_specification import Ground_motion_specification
from eqrm_code.ground_motion_interface import *

class Dist_Obj(object):
    def __init__(self, Rjb, Rrup):
        self.Rupture = Rrup
        self.Joyner_Boore = Rjb

class Test_Campbell08(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Campbell08(self):''')

    print('%sc_tab = array([' % indent)
    print('''
#T(s)  c0     c1     c2     c3     c4    c5   c6   c7     c8    c9     c10   c11   c12    k1   k2    k3    c    n    s_lny t_lny s_lnAF c_lny rho 
[ 0.0, -1.715,0.500,-0.530,-0.262,-2.118,0.17,5.60,0.280,-0.120,0.490, 1.058,0.040,0.610, 865,-1.186,1.839,1.88,1.18,0.478,0.219,0.300, 0.166,1.000], 
[0.010,-1.715,0.500,-0.530,-0.262,-2.118,0.17,5.60,0.280,-0.120,0.490, 1.058,0.040,0.610, 865,-1.186,1.839,1.88,1.18,0.478,0.219,0.300, 0.166,1.000], 
[0.020,-1.680,0.500,-0.530,-0.262,-2.123,0.17,5.60,0.280,-0.120,0.490, 1.102,0.040,0.610, 865,-1.219,1.840,1.88,1.18,0.480,0.219,0.300, 0.166,0.999], 
[0.030,-1.552,0.500,-0.530,-0.262,-2.145,0.17,5.60,0.280,-0.120,0.490, 1.174,0.040,0.610, 908,-1.273,1.841,1.88,1.18,0.489,0.235,0.300, 0.165,0.989], 
[0.050,-1.209,0.500,-0.530,-0.267,-2.199,0.17,5.74,0.280,-0.120,0.490, 1.272,0.040,0.610,1054,-1.346,1.843,1.88,1.18,0.510,0.258,0.300, 0.162,0.963], 
[0.075,-0.657,0.500,-0.530,-0.302,-2.277,0.17,7.09,0.280,-0.120,0.490, 1.438,0.040,0.610,1086,-1.471,1.845,1.88,1.18,0.520,0.292,0.300, 0.158,0.922], 
[0.10, -0.314,0.500,-0.530,-0.324,-2.318,0.17,8.05,0.280,-0.099,0.490, 1.604,0.040,0.610,1032,-1.624,1.847,1.88,1.18,0.531,0.286,0.300, 0.170,0.898], 
[0.15, -0.133,0.500,-0.530,-0.339,-2.309,0.17,8.79,0.280,-0.048,0.490, 1.928,0.040,0.610, 878,-1.931,1.852,1.88,1.18,0.532,0.280,0.300, 0.180,0.890], 
[0.20, -0.486,0.500,-0.446,-0.398,-2.220,0.17,7.60,0.280,-0.012,0.490, 2.194,0.040,0.610, 748,-2.188,1.856,1.88,1.18,0.534,0.249,0.300, 0.186,0.871], 
[0.25, -0.890,0.500,-0.362,-0.458,-2.146,0.17,6.58,0.280, 0.000,0.490, 2.351,0.040,0.700, 654,-2.381,1.861,1.88,1.18,0.534,0.240,0.300, 0.191,0.852], 
[0.30, -1.171,0.500,-0.294,-0.511,-2.095,0.17,6.04,0.280, 0.000,0.490, 2.460,0.040,0.750, 587,-2.518,1.865,1.88,1.18,0.544,0.215,0.300, 0.198,0.831], 
[0.40, -1.466,0.500,-0.186,-0.592,-2.066,0.17,5.30,0.280, 0.000,0.490, 2.587,0.040,0.850, 503,-2.657,1.874,1.88,1.18,0.541,0.217,0.300, 0.206,0.785], 
[0.50, -2.569,0.656,-0.304,-0.536,-2.041,0.17,4.73,0.280, 0.000,0.490, 2.544,0.040,0.883, 457,-2.669,1.883,1.88,1.18,0.550,0.214,0.300, 0.208,0.735], 
[0.75, -4.844,0.972,-0.578,-0.406,-2.000,0.17,4.00,0.280, 0.000,0.490, 2.133,0.077,1.000, 410,-2.401,1.906,1.88,1.18,0.568,0.227,0.300, 0.221,0.628], 
[1.00, -6.406,1.196,-0.772,-0.314,-2.000,0.17,4.00,0.255, 0.000,0.490, 1.571,0.150,1.000, 400,-1.955,1.929,1.88,1.18,0.568,0.255,0.300, 0.225,0.534], 
[1.50, -8.692,1.513,-1.046,-0.185,-2.000,0.17,4.00,0.161, 0.000,0.490, 0.406,0.253,1.000, 400,-1.025,1.974,1.88,1.18,0.564,0.296,0.300, 0.222,0.411], 
[2.00, -9.701,1.600,-0.978,-0.236,-2.000,0.17,4.00,0.094, 0.000,0.371,-0.456,0.300,1.000, 400,-0.299,2.019,1.88,1.18,0.571,0.296,0.300, 0.226,0.331], 
[3.00,-10.556,1.600,-0.638,-0.491,-2.000,0.17,4.00,0.000, 0.000,0.154,-0.820,0.300,1.000, 400, 0.000,2.110,1.88,1.18,0.558,0.326,0.300, 0.229,0.289], 
[4.00,-11.212,1.600,-0.316,-0.770,-2.000,0.17,4.00,0.000, 0.000,0.000,-0.820,0.300,1.000, 400, 0.000,2.200,1.88,1.18,0.576,0.297,0.300, 0.237,0.261], 
[5.00,-11.684,1.600,-0.070,-0.986,-2.000,0.17,4.00,0.000, 0.000,0.000,-0.820,0.300,1.000, 400, 0.000,2.291,1.88,1.18,0.601,0.359,0.300, 0.237,0.200], 
[7.50,-12.505,1.600,-0.070,-0.656,-2.000,0.17,4.00,0.000, 0.000,0.000,-0.820,0.300,1.000, 400, 0.000,2.517,1.88,1.18,0.628,0.428,0.300, 0.271,0.174], 
[10.0,-13.087,1.600,-0.070,-0.422,-2.000,0.17,4.00,0.000, 0.000,0.000,-0.820,0.300,1.000, 400, 0.000,2.744,1.88,1.18,0.667,0.485,0.300, 0.290,0.174], 
[-1.0,  0.954,0.696,-0.309,-0.019,-2.016,0.17,4.00,0.245, 0.000,0.358, 1.694,0.092,1.000, 400,-1.955,1.929,1.88,1.18,0.484,0.203,0.300, 0.190,0.691], 
[-2.0, -5.270,1.600,-0.070, 0.000,-2.000,0.17,4.00,0.000, 0.000,0.000,-0.820,0.300,1.000, 400, 0.000,2.744,1.88,1.18,0.667,0.485,0.300, 0.290,0.174], 
])''')
    print('')
 
    print('%s# generate coefficients for varying periods ' % indent)
    print('%sc_dict = {} ' % indent)
    print("%speriods = [('0.01', 1), ('0.20', 8), ('1.00', 14), ('3.00', 17)]" % indent)
    print('%sfor (T, i) in periods:' % indent)
    print('%s    c = array(c_tab[i][1:19])' % indent)
    print('%s    c.shape = (-1, 1, 1, 1)' % indent)
    print('%s    c_dict[T] = c' % indent)
    print('')
    print('%s# generate sigma coefficients for varying periods' % indent)
    print('%ss_dict = {}' % indent)
    print("%speriods = [('0.01', 1), ('0.20', 8), ('1.00', 14), ('3.00', 17)]" % indent)
    print('%sfor (T, i) in periods:' % indent)
    print('%s    s = array(c_tab[i][19:])' % indent)
    print('%s    s.shape = (-1, 1, 1, 1)' % indent)
    print('%s    s_dict[T] = s' % indent)
    print('')

    # now write body of tests
    print('%s# now run all tests' % indent)
    print("%smodel_name = 'Campbell08'" % indent)
    print('%smodel = Ground_motion_specification(model_name)' % indent)
    print('')

    print('%satol = 8.0E-5' % indent)
    print('%srtol = 9.0E-5' % indent)
    print('')

    for (i, case) in enumerate(cases):
        (T, M, Rjb, Rrup, Rake, Dip, Ztor, Vs30, Z25, Sa, sigma) = case
        log_Sa = math.log(Sa)

        # convert Rake value to fault_type
        (fault_type, fault_name) = rake_to_fault_type(Rake)

        print('%s# test %d: rake=%f, fault_type=%d (%s)' % (indent, i, Rake, fault_type, fault_name))
        print('%s# T=%.2f, M=%.1f, Rjb=%.1f, Rrup=%.1f, Vs30=%.1f' % (indent, T, M, Rjb, Rrup, Vs30))
        print('%speriods = array([[[%f]]])' % (indent, T))
        print('%sdist_obj = Dist_Obj(array([[%f]]), array([[%f]]))' % (indent, Rjb, Rrup))
        print('%sDip = array([[[%f]]])' % (indent, Dip))
        print('%sZtor = array([[[%f]]])' % (indent, Ztor))
        print('%sM = array([[[%f]]])' % (indent, M))
        print('%sVs30 = array([%f])' % (indent, Vs30))
        print('%sZ25 = array([%f])' % (indent, Z25))
        print('%sfault_type = array([[[%d]]])' % (indent, fault_type))
        print("%scoefficient = c_dict['%.2f']" % (indent, T))
        print("%ssigma_coefficient = s_dict['%.2f']" % (indent, T))
        print('%s(log_mean, sigma) = model.distribution(periods=periods, depth_to_top=Ztor, dip=Dip, fault_type=fault_type, mag=M, dist_object=dist_obj, Vs30=Vs30, Z25=Z25,\n'
              '%s   coefficient=coefficient, sigma_coefficient=sigma_coefficient)'
              % (indent, indent))
        print("%smsg1 = 'log_mean: T=%.2f, M=%.1f, Rjb=%.1f, Rrup=%.1f, dip=%.1f, Ztor=%.1f, Vs30=%.1f: got=%%s, expected=[[[%f]]]' %% str(log_mean)"
              % (indent, T, M, Rjb, Rrup, Dip, Ztor, Vs30, log_Sa))
        print("%smsg2 = 'abs_delta=%%f, rel_delta=%%f' %% (abs(log_mean-%f), abs((log_mean-%f)/log_mean))" % (indent, log_Sa, log_Sa))
        print("%sself.failUnless(allclose(log_mean, array([[[%f]]]), atol=atol, rtol=rtol), msg1+'\\n'+msg2)" % (indent, log_Sa))
        print("%smsg1 = 'sigma: T=%.2f, M=%.1f, Rjb=%.1f, Rrup=%.1f, Vs30=%.1f: got=%%s, expected=[[[%f]]]' %% str(sigma)" % (indent, T, M, Rjb, Rrup, Vs30, sigma))
        print("%smsg2 = 'abs_delta=%%f, rel_delta=%%f' %% (abs(sigma-%f), abs((sigma-%f)/sigma))" % (indent, sigma, sigma))
        print("%sself.failUnless(allclose(sigma, array([[[%f]]]), atol=atol, rtol=rtol), msg1+'\\n'+msg2)" % (indent, sigma))
        print('')

    # write file footer
    print('''################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Campbell08, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)''')


ctl_data = read_file(CTL_data_file, Num_CTL_headers, CTL_fields)

write_code(ctl_data)

