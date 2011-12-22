#!/usr/bin/env python

"""A program to take the output from the FORTRAN program and make
unittest code for Abrahamson08."""

# FIXME Why not just write a test suite method incorporating a loop?
# Why write python that writes python?

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
              'Rx': 9,
              'Fhw': 13,
              'Rake': 14,
              'Dip': 16,
              'width': 18,
              'Ztor': 20,
              'Vs30': 21,
              'Z10': 23,
              'Sa': 28,
              'sigma': 32}	# estimated Vs30


def rake_to_fault_type(rake):
    """Use Boore FTN mapping for AS08"""

    if -120.0 <= rake <= -60.0:
        return (1, 'normal')
    if 30.0 <= rake <= 150.0:
        return (0, 'reverse')
    return (2, 'strike slip')


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
            result.append((T, M, Rjb, Rrup, Rx, Fhw, Rake, Dip, width, Ztor, Vs30, Z10, Sa, sigma))

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
    def __init__(self, Rjb, Rrup, Rx):
        self.Rupture = Rrup
        self.Joyner_Boore = Rjb
        self.Horizontal = Rx

class Test_Abrahamson08(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Abrahamson08(self):''')

    print('%sc_tab = array([' % indent)
    print('''
#T(s)  c1   c4  a3     a4     a5    n    c    c2    VLIN   b      a1      a2      a8      a10    a12     a13    a14     a15     a16     a18    s1est s2est s1mea s2mea s3    s4    rho
[0.010,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 865.1,-1.186, 0.8110,-0.9679,-0.0372, 0.9445,0.0000,-0.0600,1.0800,-0.3500, 0.9000,-0.0067,0.590,0.470,0.576,0.453,0.420,0.300,1.000],
[0.020,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 865.1,-1.219, 0.8550,-0.9774,-0.0372, 0.9834,0.0000,-0.0600,1.0800,-0.3500, 0.9000,-0.0067,0.590,0.470,0.576,0.453,0.420,0.300,1.000],
[0.030,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 907.8,-1.273, 0.9620,-1.0024,-0.0372, 1.0471,0.0000,-0.0600,1.1331,-0.3500, 0.9000,-0.0067,0.605,0.478,0.591,0.461,0.462,0.305,0.991],
[0.040,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 994.5,-1.308, 1.0370,-1.0289,-0.0315, 1.0884,0.0000,-0.0600,1.1708,-0.3500, 0.9000,-0.0067,0.615,0.483,0.602,0.466,0.492,0.309,0.982],
[0.050,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0,1053.5,-1.346, 1.1330,-1.0508,-0.0271, 1.1333,0.0000,-0.0600,1.2000,-0.3500, 0.9000,-0.0076,0.623,0.488,0.610,0.471,0.515,0.312,0.973],
[0.075,6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0,1085.7,-1.471, 1.3750,-1.0810,-0.0191, 1.2808,0.0000,-0.0600,1.2000,-0.3500, 0.9000,-0.0093,0.630,0.495,0.617,0.479,0.550,0.317,0.952],
[0.10, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0,1032.5,-1.624, 1.5630,-1.0833,-0.0166, 1.4613,0.0000,-0.0600,1.2000,-0.3500, 0.9000,-0.0093,0.630,0.501,0.617,0.485,0.550,0.321,0.929],
[0.15, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 877.6,-1.931, 1.7160,-1.0357,-0.0254, 1.8071,0.0181,-0.0600,1.1683,-0.3500, 0.9000,-0.0093,0.630,0.509,0.616,0.491,0.550,0.326,0.896],
[0.20, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 748.2,-2.188, 1.6870,-0.9700,-0.0396, 2.0773,0.0309,-0.0600,1.1274,-0.3500, 0.9000,-0.0083,0.630,0.514,0.614,0.495,0.520,0.329,0.874],
[0.25, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 654.3,-2.381, 1.6460,-0.9202,-0.0539, 2.2794,0.0409,-0.0600,1.0956,-0.3500, 0.9000,-0.0069,0.630,0.518,0.612,0.497,0.497,0.332,0.856],
[0.30, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 587.1,-2.518, 1.6010,-0.8974,-0.0656, 2.4201,0.0491,-0.0600,1.0697,-0.3500, 0.9000,-0.0057,0.630,0.522,0.611,0.499,0.479,0.335,0.841],
[0.40, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 503.0,-2.657, 1.5110,-0.8677,-0.0807, 2.5510,0.0619,-0.0600,1.0288,-0.3500, 0.8423,-0.0039,0.630,0.527,0.608,0.501,0.449,0.338,0.818],
[0.50, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 456.6,-2.669, 1.3970,-0.8475,-0.0924, 2.5395,0.0719,-0.0600,0.9971,-0.3191, 0.7458,-0.0025,0.630,0.532,0.606,0.504,0.426,0.341,0.783],
[0.75, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 410.5,-2.401, 1.1370,-0.8206,-0.1137, 2.1493,0.0800,-0.0600,0.9395,-0.2629, 0.5704, 0.0000,0.630,0.539,0.602,0.506,0.385,0.346,0.680],
[1.00, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0,-1.955, 0.9150,-0.8088,-0.1289, 1.5705,0.0800,-0.0600,0.8985,-0.2230, 0.4460, 0.0000,0.630,0.545,0.594,0.503,0.350,0.350,0.607],
[1.50, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0,-1.025, 0.5100,-0.7995,-0.1534, 0.3991,0.0800,-0.0600,0.8409,-0.1668, 0.2707, 0.0000,0.615,0.552,0.566,0.497,0.350,0.350,0.504],
[2.00, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0,-0.299, 0.1920,-0.7960,-0.1708,-0.6072,0.0800,-0.0600,0.8000,-0.1270, 0.1463, 0.0000,0.604,0.558,0.544,0.491,0.350,0.350,0.431],
[3.00, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-0.2800,-0.7960,-0.1954,-0.9600,0.0800,-0.0600,0.4793,-0.0708,-0.0291, 0.0000,0.589,0.565,0.527,0.500,0.350,0.350,0.328],
[4.00, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-0.6390,-0.7960,-0.2128,-0.9600,0.0800,-0.0600,0.2518,-0.0309,-0.1535, 0.0000,0.578,0.570,0.515,0.505,0.350,0.350,0.255],
[5.00, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-0.9360,-0.7960,-0.2263,-0.9208,0.0800,-0.0600,0.0754, 0.0000,-0.2500, 0.0000,0.570,0.587,0.510,0.529,0.350,0.350,0.200],
[7.50, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-1.5270,-0.7960,-0.2509,-0.7700,0.0800,-0.0600,0.0000, 0.0000,-0.2500, 0.0000,0.611,0.618,0.572,0.579,0.350,0.350,0.200],
[10.0, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0, 0.000,-1.9930,-0.7960,-0.2683,-0.6630,0.0800,-0.0600,0.0000, 0.0000,-0.2500, 0.0000,0.640,0.640,0.612,0.612,0.350,0.350,0.200],
[ 0.0, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 865.1,-1.186, 0.8040,-0.9679,-0.0372, 0.9445,0.0000,-0.0600,1.0800,-0.3500, 0.9000,-0.0067,0.590,0.470,0.576,0.453,0.470,0.300,1.000],
[-1.0, 6.75,4.5,0.265,-0.231,-0.398,1.18,1.88,50.0, 400.0,-1.955, 5.7578,-0.9046,-0.1200, 1.5390,0.0800,-0.0600,0.7000,-0.3900, 0.6300, 0.0000,0.590,0.470,0.576,0.453,0.420,0.300,0.740],
])''')
    print('')
 
    print('%s# generate coefficients for varying periods ' % indent)
    print('%sc_dict = {} ' % indent)
    print("%speriods = [('0.01', 0), ('0.20', 8), ('1.00', 14), ('3.00', 17)]" % indent)
    print('%sfor (T, i) in periods:' % indent)
    print('%s    c = array(c_tab[i][1:21])' % indent)
    print('%s    c.shape = (-1, 1, 1, 1)' % indent)
    print('%s    c_dict[T] = c' % indent)
    print('')
    print('%s# generate sigma coefficients for varying periods' % indent)
    print('%ss_dict = {}' % indent)
    print("%speriods = [('0.01', 0), ('0.20', 8), ('1.00', 14), ('3.00', 17)]" % indent)
    print('%sfor (T, i) in periods:' % indent)
    print('%s    s = array(c_tab[i][21:])' % indent)
    print('%s    s.shape = (-1, 1, 1, 1)' % indent)
    print('%s    s_dict[T] = s' % indent)
    print('')

    # now write body of tests
    print('%s# now run all tests' % indent)
    print("%smodel_name = 'Abrahamson08'" % indent)
    print('%smodel = Ground_motion_specification(model_name)' % indent)
    print('')

    print('%satol = 4.0E-5' % indent)
    print('%srtol = 2.0E-5' % indent)
    print('')

    for (i, case) in enumerate(cases):
        (T, M, Rjb, Rrup, Rx, Fhw, Rake, Dip, width, Ztor, Vs30, Z10, Sa, sigma) = case

        log_Sa = math.log(Sa)

        # convert Rake value to fault_type
        (fault_type, fault_name) = rake_to_fault_type(Rake)

        print('%s# test %d: rake=%f, Fhw=%d, fault_type=%d (%s)' % (indent, i, Rake, Fhw, fault_type, fault_name))
        print('%s# T=%.2f, M=%.1f, Rjb=%.1f, Rrup=%.1f, Vs30=%.1f, Sa=%f' % (indent, T, M, Rjb, Rrup, Vs30, Sa))
        print('%speriods = array([%f])' % (indent, T))
        print('%sdist_obj = Dist_Obj(array([[%f]]), array([[%f]]), array([[%f]]))' % (indent, Rjb, Rrup, Rx))
        print('%sDip = array([[[%f]]])' % (indent, Dip))
        print('%swidth= array([[[%f]]])' % (indent, width))
        print('%sZtor = array([[[%f]]])' % (indent, Ztor))
        print('%sM = array([[[%f]]])' % (indent, M))
        print('%sVs30 = array([%f])' % (indent, Vs30))
        print('%sZ10 = array([%f])' % (indent, Z10))
        print('%sFhw = array([%d])' % (indent, Fhw))
        print('%sfault_type = array([[[%d]]])' % (indent, fault_type))
        print("%scoefficient = c_dict['%.2f']" % (indent, T))
        print("%ssigma_coefficient = s_dict['%.2f']" % (indent, T))
        print('%s(log_mean, sigma) = model.distribution(periods=periods, depth_to_top=Ztor, dip=Dip, fault_type=fault_type, mag=M, dist_object=dist_obj, Vs30=Vs30, Z10=Z10,\n'
              '%s   Fhw=Fhw, width=width, coefficient=coefficient, sigma_coefficient=sigma_coefficient)'
              % (indent, indent))
        print("%smsg1 = 'log_mean: T=%.2f, M=%.1f, Rjb=%.1f, Rrup=%.1f, Rx=%.1f, dip=%.1f, Ztor=%.1f, Vs30=%.1f: got=%%s, expected=[[[%f]]]' %% str(log_mean)"
              % (indent, T, M, Rjb, Rrup, Rx, Dip, Ztor, Vs30, log_Sa))
        print("%smsg2 = 'Test %d:  abs_delta=%%f, rel_delta=%%f' %% (abs(log_mean-%f), abs((log_mean-%f)/log_mean))" % (indent, i, log_Sa, log_Sa))
        print("%sself.failUnless(allclose(log_mean, array([[[%f]]]), atol=atol, rtol=rtol), msg1+'\\n'+msg2)" % (indent, log_Sa))
        print("%smsg1 = 'sigma: T=%.2f, M=%.1f, Rjb=%.1f, Rrup=%.1f, Vs30=%.1f: got=%%s, expected=[[[%f]]]' %% str(sigma)" % (indent, T, M, Rjb, Rrup, Vs30, sigma))
        print("%smsg2 = 'Test %d:  abs_delta=%%f, rel_delta=%%f' %% (abs(sigma-%f), abs((sigma-%f)/sigma))" % (indent, i, sigma, sigma))
        print("%sself.failUnless(allclose(sigma, array([[[%f]]]), atol=atol, rtol=rtol), msg1+'\\n'+msg2)" % (indent, sigma))
        print('')

    # write file footer
    print('''################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Abrahamson08, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)''')


ctl_data = read_file(CTL_data_file, Num_CTL_headers, CTL_fields)

write_code(ctl_data)

