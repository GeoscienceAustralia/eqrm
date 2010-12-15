#!/usr/bin/env python

"""A simple script to work out Atkinson06 BC boundary bedrock calculations."""

import math


######
# global values
######    

V1 = 180.0
V2 = 300.0
Vref = 760.0

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

def check_scenario(period, distance, magnitude,
                   c1, c2, c3, c4, c5, c6, c7, c8, c9, c10):
    """Run base bedrock known case and soil for various Vs30"""

    # run known bedrock case, compare with expected_logPSA
    S = 0.0
    logPSA = eqn_5(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10,
                   magnitude, distance, S)
    lng = logPSA/ln_factor-g_factor
    g = math.exp(lng)

    print('period=%.1f, distance=%.1f, M=%.1f,\t logPSA=%f (g: %f)'
          % (period, distance, magnitude, logPSA, g))

######
# Coefficients for period 0.2s
######

c1 = -3.06E-01
c2 = 1.16E+00
c3 = -7.21E-02
c4 = -2.04E+00
c5 = 1.22E-01
c6 = -1.15E+00
c7 = 7.38E-02
c8 = 5.08E-01
c9 = -1.43E-01
c10 = -1.14E-03

######
# period = 0.2, distance = 300.0, magnitude = 7.5
######

period = 0.2
distance = 300.0
magnitude = 7.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 100.0, magnitude = 7.5
######

period = 0.2
distance = 100.0
magnitude = 7.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 10.0, magnitude = 7.5
######

period = 0.2
distance = 10.0
magnitude = 7.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 300.0, magnitude = 5.5
######

period = 0.2
distance = 300.0
magnitude = 5.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 100.0, magnitude = 5.5
######

period = 0.2
distance = 100.0
magnitude = 5.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 0.2, distance = 10.0, magnitude = 5.5
######

period = 0.2
distance = 10.0
magnitude = 5.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# Coefficients for period 1.0s
######

c1 = -5.06E+00
c2 = 2.23E+00
c3 = -1.45E-01
c4 = -2.03E+00
c5 = 1.41E-01
c6 = -8.74E-01
c7 = 5.41E-02
c8 = 7.92E-01
c9 = -1.70E-01
c10 = -4.89E-04

######
# period = 1.0, distance = 300.0, magnitude = 7.5
######

period = 1.0
distance = 300.0
magnitude = 7.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 100.0, magnitude = 7.5
######

period = 1.0
distance = 100.0
magnitude = 7.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 10.0, magnitude = 7.5
######

period = 1.0
distance = 10.0
magnitude = 7.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 300.0, magnitude = 5.5
######

period = 1.0
distance = 300.0
magnitude = 5.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 100.0, magnitude = 5.5
######

period = 1.0
distance = 100.0
magnitude = 5.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

######
# period = 1.0, distance = 10.0, magnitude = 5.5
######

period = 1.0
distance = 10.0
magnitude = 5.5

check_scenario(period, distance, magnitude,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10)

