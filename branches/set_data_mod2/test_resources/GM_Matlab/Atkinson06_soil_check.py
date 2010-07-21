#!/usr/bin/env python

"""A simple script to work out Atkinson06 soil calculations 'by hand'"""

import math


######
# global values
######    

pgaBC = 70.0

V1 = 180.0
V2 = 300.0
Vref = 760.0

######
# various equations from the Atkinson paper
######

def eqn_8a(B1, B2, V30, V1, V2):
    return B1

def eqn_8b(B1, B2, V30, V1, V2):
    return (B1-B2)*math.log(V30/V2)/math.log(V1/V2) + B2

def eqn_8c(B1, B2, V30, V1, V2):
    return B2 * math.log(V30/Vref)/math.log(V2/Vref)

def eqn_8d(B1, B2, V30, V1, V2):
    return 0.0

def eqn_8(B1, B2, V30, V1, V2):
    if V30 <= V1:
        Bnl = eqn_8a(B1, B2, V30, V1, V2)
    elif V1 < V30 <= V2:
        Bnl = eqn_8b(B1, B2, V30, V1, V2)
    elif V2 < V30 < Vref:
        Bnl = eqn_8c(B1, B2, V30, V1, V2)
    elif V30 > Vref:
        Bnl = eqn_8d(B1, B2, V30, V1, V2)
    else:
        msg = 'Error in eqn_8()'
        raise RuntimeError(msg)

    return Bnl

def eqn_7a(Blin, V30, Vref, Bnl, pgaBC):
    return math.log10(math.exp(Blin*math.log(V30/Vref) + Bnl*math.log(60.0/100.0)))

def eqn_7b(Blin, V30, Vref, Bnl, pgaBC):
    return math.log10(math.exp(Blin*math.log(V30/Vref) + Bnl*math.log(pgaBC/100.0)))

def eqn_7(Blin, V30, Vref, Bnl, pgaBC):
    if pgaBC <= 60.0:
        return eqn_7a(Blin, V30, Vref, Bnl, pgaBC)
    else:
        return eqn_7b(Blin, V30, Vref, Bnl, pgaBC)

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
def same(prefix, value, expected, rtol=0.01):
    delta = abs(expected - value)/expected
    if delta <= rtol:
        print('%s: OK' % prefix)
    else:
        print('%s: Value %.4f not same as expected: %.4f'
              % (prefix, value, expected))

def check_scenario(period, distance, magnitude, expected_logPSA,
                   c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2):
    """Run base bedrock known case and soil for various V30"""

    # run known bedrock case, compare with expected_logPSA
    S = 0.0
    logPSA = eqn_5(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10,
                   magnitude, distance, S)

    same('bedrock, logPSA (period=%.1f, distance=%.1f, M=%.1f)'
         % (period, distance, magnitude),
         logPSA, expected_logPSA, rtol=3.0e-2)

    # do 3 V30 values in [200, 800]
    for V30 in (200.0, 400.0, 800.0):
        Bnl = eqn_8(B1, B2, V30, V1, V2)
        S = eqn_7(Blin, V30, Vref, Bnl, pgaBC)
        logPSA = eqn_5(c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, magnitude, distance, S)
        print('scenario, V30=%.1f, S=%f, logPSA=%f' % (V30, S, logPSA))

######
# case 1: period = 0.2, distance = 100.0, magnitude = 7.5
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

Blin = -0.306
B1 = -0.521
B2 = -0.185

expected_logPSA = 2.00e+0	# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 2: period = 0.2, distance = 10.0, magnitude = 7.5
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

Blin = -0.306
B1 = -0.521
B2 = -0.185

expected_logPSA = 3.05e+0		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 3: period = 0.2, distance = 2.0, magnitude = 7.5
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

Blin = -0.306
B1 = -0.521
B2 = -0.185

expected_logPSA = 3.48e+0		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 4: period = 1.0, distance = 100.0, magnitude = 7.5
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

Blin = -0.7
B1 = -0.44
B2 = 0.0

expected_logPSA = 1.56		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 5: period = 1.0, distance = 10.0, magnitude = 7.5
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

Blin = -0.7
B1 = -0.44
B2 = 0.0

expected_logPSA = 2.41		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 6: period = 1.0, distance = 2.0, magnitude = 7.5
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

Blin = -0.7
B1 = -0.44
B2 = 0.0

expected_logPSA = 2.83		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 7: period = 2.0, distance = 100.0, magnitude = 7.5
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

Blin = -0.730
B1 = -0.375
B2 = 0.0

expected_logPSA = 1.30		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 8: period = 2.0, distance = 10.0, magnitude = 7.5
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

Blin = -0.730
B1 = -0.375
B2 = 0.0

expected_logPSA = 2.09		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 9: period = 2.0, distance = 2.0, magnitude = 7.5
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

Blin = -0.730
B1 = -0.375
B2 = 0.0

expected_logPSA = 2.45		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 10: period = 0.2, distance = 100.0, magnitude = 5.5
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

Blin = -0.306
B1 = -0.521
B2 = -0.185

expected_logPSA = 1.10e+0	# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 11: period = 0.2, distance = 10.0, magnitude = 5.5
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

Blin = -0.306
B1 = -0.521
B2 = -0.185

expected_logPSA = 2.37e+0		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 12: period = 0.2, distance = 2.0, magnitude = 5.5
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

Blin = -0.306
B1 = -0.521
B2 = -0.185

expected_logPSA = 3.20e+0		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 13: period = 1.0, distance = 100.0, magnitude = 5.5
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

Blin = -0.7
B1 = -0.44
B2 = 0.0

expected_logPSA = 0.33		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 14: period = 1.0, distance = 10.0, magnitude = 5.5
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

Blin = -0.7
B1 = -0.44
B2 = 0.0

expected_logPSA = 1.45		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 15: period = 1.0, distance = 2.0, magnitude = 5.5
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

Blin = -0.7
B1 = -0.44
B2 = 0.0

expected_logPSA = 2.29		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 16: period = 2.0, distance = 100.0, magnitude = 5.5
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

Blin = -0.730
B1 = -0.375
B2 = 0.0

expected_logPSA = -0.22		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 17: period = 2.0, distance = 10.0, magnitude = 5.5
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

Blin = -0.730
B1 = -0.375
B2 = 0.0

expected_logPSA = 0.87		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

######
# case 18: period = 2.0, distance = 2.0, magnitude = 5.5
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

Blin = -0.730
B1 = -0.375
B2 = 0.0

expected_logPSA = 1.72		# bedrock result

check_scenario(period, distance, magnitude, expected_logPSA,
               c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, Blin, B1, B2)

