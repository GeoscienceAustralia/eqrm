#!/usr/bin/env python

"""Create the bottom-most part of a CTL file to test Boore_08.

Writes the parameters to stdout.  Add the output to a CTL file.
Don't forget to change directory/file data in the CTL file!
"""

import math


def convert_Vs30_to_Z25(Vs30):
    """Conversion from nga_gm_tmr.for

    Vs30 is in m/s.  Result Z25 in km.
    """

    if Vs30 < 180.0:
        Z10 = math.exp(6.745)
    elif Vs30 > 500.0:
        Z10 = math.exp(5.394 - 4.48*math.log(Vs30/500.0))
    else:
        Z10 = math.exp(6.745 - 1.35*math.log(Vs30/180.0))

    Z25 = 0.519 + 3.595*(Z10/1000.0)

    return Z25



T_range = [0.01, 0.2, 1.0, 3.0]
M_range = [4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
R_range = [5.0, 10.0, 25.0, 50.0, 100.0, 200.0]
Rake_range = [-90.0, 140.0, 0.0]	# strike-slip, reverse, normal
Dip_range = [90.0, 45.0]
Vs30_range = [200.0, 400.0, 600.0, 800.0, 1000.0]
Az_range = [-90.0, 90.0]

Fhw = -1
Zhyp = -1
W = 20.0
Ztor = 10.0
Z10 = -1
FAS = 0

print('!T        Mw        Fhw       Az        Rjb       Rrup       Zhyp     Rake      Dip       W         Ztor      Vs30      Z10       Z25       FAS')

for T in T_range:
    for M in M_range:
        for R in R_range:
            for Rake in Rake_range:
                for Dip in Dip_range:
                    for Vs30 in Vs30_range:
                        for Az in Az_range:
                            Z25 = convert_Vs30_to_Z25(Vs30) * 1000.0 # need m
                            print('%9.3e %9.3e %-9d %-9d %9.3e %9.3e %-9d %9.3e %9.3e %9.3e %9.3e %9.3e %-9d %9.3e %-9d '
                                  % (T, M, Fhw, Az, R, R, Zhyp, Rake, Dip, W, Ztor, Vs30, Z10, Z25, FAS))

