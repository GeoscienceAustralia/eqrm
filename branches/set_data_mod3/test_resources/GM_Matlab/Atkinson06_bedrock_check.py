#!/usr/bin/env python

"""A simple script to work out Atkinson06 bedrock calculations 'by hand'"""

import math


######
# global values
######    

ln_factor = math.log10(math.e)
g_factor = math.log(9.80665*100)

######
# various equations from the Atkinson paper
######

def eqn_5(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, M, Rcd, S):
    R0 = 10.0
    R1 = 70.0
    R2 = 140.0

    F0 = max(math.log10(R0/Rcd), 0.0)
    F1 = min(math.log10(Rcd), math.log10(R1))
    F2 = max(math.log10(Rcd/R2), 0.0)

    return c1 + c2*M + c3*M*M + (c4 + c5*M)*F1 + (c6 + c7*M)*F2 + \
               (c8 + c9*M)*F0 + c10*Rcd + S

# the following functions are used to run the various scenarios
def same(prefix, value, expected, atol=0.01, rtol=0.01):
    delta = abs(expected - value)
    if delta <= (atol+rtol*abs(value)):
#    if delta <= rtol:
        print('%s: OK (%f)' % (prefix, value))
    else:
        print('%s: Value %.4f not same as expected: %.4f (delta=%f)'
              % (prefix, value, expected, delta))

def check_scenario(period, distance, magnitude, expected_logPSA,
                   c1, c2, c3, c4, c5, c6, c7, c8, c9, c10):
    """Run base bedrock known case and soil for various vs30"""

    # run known bedrock case, compare with expected_logPSA
    S = 0.0
    logPSA = eqn_5(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10,
                   magnitude, distance, S)

    same('bedrock, logPSA (period=%.1f, distance=%.1f, M=%.1f)'
         % (period, distance, magnitude),
         logPSA, expected_logPSA, atol=5.0e-2, rtol=5.0e-3)

######
# period = 0.0, distance = 2.0, magnitude = 7.5
######

period = 0.0
distance = 2.0
magnitude = 7.5

c1 = 9.07E-01
c2 = 9.83E-01
c3 = -6.60E-02
c4 = -2.70E+00
c5 = 1.59E-01
c6 = -2.80E+00
c7 = 2.12E-01
c8 = -3.01E-01
c9 = -6.53E-02
c10 = -4.48E-04

expected_logPSA = 3.54		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.0, distance = 10.0, magnitude = 7.5
######

period = 0.0
distance = 10.0
magnitude = 7.5

c1 = 9.07E-01
c2 = 9.83E-01
c3 = -6.60E-02
c4 = -2.70E+00
c5 = 1.59E-01
c6 = -2.80E+00
c7 = 2.12E-01
c8 = -3.01E-01
c9 = -6.53E-02
c10 = -4.48E-04

expected_logPSA = 3.08		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.0, distance = 100.0, magnitude = 7.5
######

period = 0.0
distance = 100.0
magnitude = 7.5

c1 = 9.07E-01
c2 = 9.83E-01
c3 = -6.60E-02
c4 = -2.70E+00
c5 = 1.59E-01
c6 = -2.80E+00
c7 = 2.12E-01
c8 = -3.01E-01
c9 = -6.53E-02
c10 = -4.48E-04

expected_logPSA = 1.75		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.0, distance = 300.0, magnitude = 7.5
######

period = 0.0
distance = 300.0
magnitude = 7.5

c1 = 9.07E-01
c2 = 9.83E-01
c3 = -6.60E-02
c4 = -2.70E+00
c5 = 1.59E-01
c6 = -2.80E+00
c7 = 2.12E-01
c8 = -3.01E-01
c9 = -6.53E-02
c10 = -4.48E-04

expected_logPSA = 1.29		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 2.0, magnitude = 7.5
######

period = 0.2
distance = 2.0
magnitude = 7.5

c1 = -6.15e-1
c2 = 1.23e+0
c3 = -7.89e-2
c4 = -2.09e+0
c5 = 1.31e-1
c6 = -1.12e+0
c7 = 6.79e-2
c8 = 6.06e-1
c9 = -1.46e-1
c10 = -1.13e-3

expected_logPSA = 3.48		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 10.0, magnitude = 7.5
######

period = 0.2
distance = 10.0
magnitude = 7.5

c1 = -6.15e-1
c2 = 1.23e+0
c3 = -7.89e-2
c4 = -2.09e+0
c5 = 1.31e-1
c6 = -1.12e+0
c7 = 6.79e-2
c8 = 6.06e-1
c9 = -1.46e-1
c10 = -1.13e-3

expected_logPSA = 3.05		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 100.0, magnitude = 7.5
######

period = 0.2
distance = 100.0
magnitude = 7.5

c1 = -6.15e-1
c2 = 1.23e+0
c3 = -7.89e-2
c4 = -2.09e+0
c5 = 1.31e-1
c6 = -1.12e+0
c7 = 6.79e-2
c8 = 6.06e-1
c9 = -1.46e-1
c10 = -1.13e-3

expected_logPSA = 2.00		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 300.0, magnitude = 7.5
######

period = 0.2
distance = 300.0
magnitude = 7.5

c1 = -6.15e-1
c2 = 1.23e+0
c3 = -7.89e-2
c4 = -2.09e+0
c5 = 1.31e-1
c6 = -1.12e+0
c7 = 6.79e-2
c8 = 6.06e-1
c9 = -1.46e-1
c10 = -1.13e-3

expected_logPSA = 1.55		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 2.0, magnitude = 7.5
######

period = 1.0
distance = 2.0
magnitude = 7.5

c1 = -5.27e+0
c2 = 2.26e+0
c3 = -1.48e-1
c4 = -2.07e+0
c5 = 1.50e-1
c6 = -8.13e-1
c7 = 4.67e-2
c8 = 8.26e-1
c9 = -1.62e-1
c10 = -4.86e-4

expected_logPSA = 2.83		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 10.0, magnitude = 7.5
######

period = 1.0
distance = 10.0
magnitude = 7.5

c1 = -5.27e+0
c2 = 2.26e+0
c3 = -1.48e-1
c4 = -2.07e+0
c5 = 1.50e-1
c6 = -8.13e-1
c7 = 4.67e-2
c8 = 8.26e-1
c9 = -1.62e-1
c10 = -4.86e-4

expected_logPSA = 2.41		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 100.0, magnitude = 7.5
######

period = 1.0
distance = 100.0
magnitude = 7.5

c1 = -5.27e+0
c2 = 2.26e+0
c3 = -1.48e-1
c4 = -2.07e+0
c5 = 1.50e-1
c6 = -8.13e-1
c7 = 4.67e-2
c8 = 8.26e-1
c9 = -1.62e-1
c10 = -4.86e-4

expected_logPSA = 1.56		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 300.0, magnitude = 7.5
######

period = 1.0
distance = 300.0
magnitude = 7.5

c1 = -5.27e+0
c2 = 2.26e+0
c3 = -1.48e-1
c4 = -2.07e+0
c5 = 1.50e-1
c6 = -8.13e-1
c7 = 4.67e-2
c8 = 8.26e-1
c9 = -1.62e-1
c10 = -4.86e-4

expected_logPSA = 1.32		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 2.0, distance = 2.0, magnitude = 7.5
######

period = 2.0
distance = 2.0
magnitude = 7.5

c1 = -6.18e+0
c2 = 2.30e+0
c3 = -1.44e-1
c4 = -2.22e+0
c5 = 1.77e-1
c6 = -9.37e-1
c7 = 7.07e-2
c8 = 9.52e-1
c9 = -1.77e-1
c10 = -3.22e-4

expected_logPSA = 2.45		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 2.0, distance = 10.0, magnitude = 7.5
######

period = 2.0
distance = 10.0
magnitude = 7.5

c1 = -6.18e+0
c2 = 2.30e+0
c3 = -1.44e-1
c4 = -2.22e+0
c5 = 1.77e-1
c6 = -9.37e-1
c7 = 7.07e-2
c8 = 9.52e-1
c9 = -1.77e-1
c10 = -3.22e-4

expected_logPSA = 2.09		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 2.0, distance = 100.0, magnitude = 7.5
######

period = 2.0
distance = 100.0
magnitude = 7.5

c1 = -6.18e+0
c2 = 2.30e+0
c3 = -1.44e-1
c4 = -2.22e+0
c5 = 1.77e-1
c6 = -9.37e-1
c7 = 7.07e-2
c8 = 9.52e-1
c9 = -1.77e-1
c10 = -3.22e-4

expected_logPSA = 1.30		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 2.0, distance = 300.0, magnitude = 7.5
######

period = 2.0
distance = 300.0
magnitude = 7.5

c1 = -6.18e+0
c2 = 2.30e+0
c3 = -1.44e-1
c4 = -2.22e+0
c5 = 1.77e-1
c6 = -9.37e-1
c7 = 7.07e-2
c8 = 9.52e-1
c9 = -1.77e-1
c10 = -3.22e-4

expected_logPSA = 1.08		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.0, distance = 2.0, magnitude = 5.5
######

period = 0.0
distance = 2.0
magnitude = 5.5

c1 = 9.07E-01
c2 = 9.83E-01
c3 = -6.60E-02
c4 = -2.70E+00
c5 = 1.59E-01
c6 = -2.80E+00
c7 = 2.12E-01
c8 = -3.01E-01
c9 = -6.53E-02
c10 = -4.48E-04

expected_logPSA = 3.30		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.0, distance = 10.0, magnitude = 5.5
######

period = 0.0
distance = 10.0
magnitude = 5.5

c1 = 9.07E-01
c2 = 9.83E-01
c3 = -6.60E-02
c4 = -2.70E+00
c5 = 1.59E-01
c6 = -2.80E+00
c7 = 2.12E-01
c8 = -3.01E-01
c9 = -6.53E-02
c10 = -4.48E-04

expected_logPSA = 2.49		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.0, distance = 100.0, magnitude = 5.5
######

period = 0.0
distance = 100.0
magnitude = 5.5

c1 = 9.07E-01
c2 = 9.83E-01
c3 = -6.60E-02
c4 = -2.70E+00
c5 = 1.59E-01
c6 = -2.80E+00
c7 = 2.12E-01
c8 = -3.01E-01
c9 = -6.53E-02
c10 = -4.48E-04

expected_logPSA = 0.89		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.0, distance = 300.0, magnitude = 5.5
######

period = 0.0
distance = 300.0
magnitude = 5.5

c1 = 9.07E-01
c2 = 9.83E-01
c3 = -6.60E-02
c4 = -2.70E+00
c5 = 1.59E-01
c6 = -2.80E+00
c7 = 2.12E-01
c8 = -3.01E-01
c9 = -6.53E-02
c10 = -4.48E-04

expected_logPSA = 0.27		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 2.0, magnitude = 5.5
######

period = 0.2
distance = 2.0
magnitude = 5.5

c1 = -6.15e-1
c2 = 1.23e+0
c3 = -7.89e-2
c4 = -2.09e+0
c5 = 1.31e-1
c6 = -1.12e+0
c7 = 6.79e-2
c8 = 6.06e-1
c9 = -1.46e-1
c10 = -1.13e-3

expected_logPSA = 3.20		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 10.0, magnitude = 5.5
######

period = 0.2
distance = 10.0
magnitude = 5.5

c1 = -6.15e-1
c2 = 1.23e+0
c3 = -7.89e-2
c4 = -2.09e+0
c5 = 1.31e-1
c6 = -1.12e+0
c7 = 6.79e-2
c8 = 6.06e-1
c9 = -1.46e-1
c10 = -1.13e-3

expected_logPSA = 2.37		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 100.0, magnitude = 5.5
######

period = 0.2
distance = 100.0
magnitude = 5.5

c1 = -6.15e-1
c2 = 1.23e+0
c3 = -7.89e-2
c4 = -2.09e+0
c5 = 1.31e-1
c6 = -1.12e+0
c7 = 6.79e-2
c8 = 6.06e-1
c9 = -1.46e-1
c10 = -1.13e-3

expected_logPSA = 1.10		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 300.0, magnitude = 5.5
######

period = 0.2
distance = 300.0
magnitude = 5.5

c1 = -6.15e-1
c2 = 1.23e+0
c3 = -7.89e-2
c4 = -2.09e+0
c5 = 1.31e-1
c6 = -1.12e+0
c7 = 6.79e-2
c8 = 6.06e-1
c9 = -1.46e-1
c10 = -1.13e-3

expected_logPSA = 0.63		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 2.0, magnitude = 5.5
######

period = 1.0
distance = 2.0
magnitude = 5.5

c1 = -5.27e+0
c2 = 2.26e+0
c3 = -1.48e-1
c4 = -2.07e+0
c5 = 1.50e-1
c6 = -8.13e-1
c7 = 4.67e-2
c8 = 8.26e-1
c9 = -1.62e-1
c10 = -4.86e-4

expected_logPSA = 2.29		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 10.0, magnitude = 5.5
######

period = 1.0
distance = 10.0
magnitude = 5.5

c1 = -5.27e+0
c2 = 2.26e+0
c3 = -1.48e-1
c4 = -2.07e+0
c5 = 1.50e-1
c6 = -8.13e-1
c7 = 4.67e-2
c8 = 8.26e-1
c9 = -1.62e-1
c10 = -4.86e-4

expected_logPSA = 1.45		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 100.0, magnitude = 5.5
######

period = 1.0
distance = 100.0
magnitude = 5.5

c1 = -5.27e+0
c2 = 2.26e+0
c3 = -1.48e-1
c4 = -2.07e+0
c5 = 1.50e-1
c6 = -8.13e-1
c7 = 4.67e-2
c8 = 8.26e-1
c9 = -1.62e-1
c10 = -4.86e-4

expected_logPSA = 0.33		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 300.0, magnitude = 5.5
######

period = 1.0
distance = 300.0
magnitude = 5.5

c1 = -5.27e+0
c2 = 2.26e+0
c3 = -1.48e-1
c4 = -2.07e+0
c5 = 1.50e-1
c6 = -8.13e-1
c7 = 4.67e-2
c8 = 8.26e-1
c9 = -1.62e-1
c10 = -4.86e-4

expected_logPSA = 0.06		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 2.0, distance = 2.0, magnitude = 5.5
######

period = 2.0
distance = 2.0
magnitude = 5.5

c1 = -6.18e+0
c2 = 2.30e+0
c3 = -1.44e-1
c4 = -2.22e+0
c5 = 1.77e-1
c6 = -9.37e-1
c7 = 7.07e-2
c8 = 9.52e-1
c9 = -1.77e-1
c10 = -3.22e-4

expected_logPSA = 1.72		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 2.0, distance = 10.0, magnitude = 5.5
######

period = 2.0
distance = 10.0
magnitude = 5.5

c1 = -6.18e+0
c2 = 2.30e+0
c3 = -1.44e-1
c4 = -2.22e+0
c5 = 1.77e-1
c6 = -9.37e-1
c7 = 7.07e-2
c8 = 9.52e-1
c9 = -1.77e-1
c10 = -3.22e-4

expected_logPSA = 0.87		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 2.0, distance = 100.0, magnitude = 5.5
######

period = 2.0
distance = 100.0
magnitude = 5.5

c1 = -6.18e+0
c2 = 2.30e+0
c3 = -1.44e-1
c4 = -2.22e+0
c5 = 1.77e-1
c6 = -9.37e-1
c7 = 7.07e-2
c8 = 9.52e-1
c9 = -1.77e-1
c10 = -3.22e-4

expected_logPSA = -0.22		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 2.0, distance = 300.0, magnitude = 5.5
######

period = 2.0
distance = 300.0
magnitude = 5.5

c1 = -6.18e+0
c2 = 2.30e+0
c3 = -1.44e-1
c4 = -2.22e+0
c5 = 1.77e-1
c6 = -9.37e-1
c7 = 7.07e-2
c8 = 9.52e-1
c9 = -1.77e-1
c10 = -3.22e-4

expected_logPSA = -0.50		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

