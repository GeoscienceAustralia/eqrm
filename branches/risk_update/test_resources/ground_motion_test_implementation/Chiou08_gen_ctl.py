#!/usr/bin/env python

"""A simple program to generate CTL data for testing Chiou08."""


import math


# precalculate constants for convert_Vs30_to_Z10()
Ch_378_7_pow_8 = math.pow(378.7, 8)
Ch_3_82_div_8 = 3.82/8.0

def convert_Vs30_to_Z10(Vs30):
    """Convert a Vs30 value to an estimated V1.0 value.
    
    This function will handle both scalar and scipy array values of Z10.

    Formula taken from equation (1) of:
    Chiou.B.S.-J., Youngs R.R., 2008 An NGA Model for the Average Horizontal
    Component of Peak Ground Motion and Response Spectra, 
    Earthquake Spectra 24, 173-215. 
    """
    
    return math.exp(28.5 - Ch_3_82_div_8*math.log(math.pow(Vs30, 8) + Ch_378_7_pow_8))


def convert_Z10_to_Z25(Z10):
    """Convert a Z1.0 value to a Z2.5 value.
    
    This function will handle both scalar and scipy array values of Z10.

    Formula taken from equation (6.3) of:
    Campbell-Bozorgnia NGA Ground Motion Relations for the Geometric Mean
    Horizontal Component of Peak and Spectral Ground Motion Parameters.
    Kenneth W. Campbell and Yousef Bozorgnia, PEER 2007/02. 
    """
    
    return 0.519 + 3.595*Z10

# parameter ranges
T_range = (0.01, 1.0, 3.0)

Event_range = ((4.0, 0.0, 0), (5.5, 0.0, 0), (7.0, 0.0, 0)) # (Mw, Ztor, Fhw)
Site_range = ((5, 300), (25, 300), (100, 300))                 # (Rjb, Vs30)
#Event_range = ((4.0, 0.0, 0), (5.5, 0.0, 0), (7.0, 0.0, 0),
#               (4.0, 5.0, 0), (5.5, 5.0, 0), (7.0, 5.0, 0),
#               (4.0, 10.0, 0), (5.5, 10.0, 0), (7.0, 10.0, 0))	# (Mw, Ztor, Fhw)
#Site_range = ((5, 300), (25, 300), (100, 300))			# (Rjb, Vs30)

# constant parameters
FAS = 0
Rake = -1
Zhyp = -1
Az = -1
Rrup = -1
Dip = 90
W = 10.0

# write CTL rows
print('!T        Mw        Fhw       Az        Rjb       Rrup       Zhyp      Rake      Dip       W         Ztor      Vs30      Z10       Z25       FAS')

for T in T_range:
    for E in Event_range:
        (Mw, Ztor, Fhw) = E
        for S in Site_range:
            (Rjb, Vs30) = S
            Z10 = convert_Vs30_to_Z10(Vs30)
            Z25 = convert_Z10_to_Z25(Z10)
            print('%9.3e %9.3e %-9d %-9d %-9d %-9d %-9d %-9d %9.3e %9.3e %9.3e %-9d %-9d %-9d %-9d'
                  % (T, Mw, Fhw, Az, Rjb, Rrup, Zhyp, Rake, Dip, W, Ztor, Vs30, Z10, Z25, FAS))

