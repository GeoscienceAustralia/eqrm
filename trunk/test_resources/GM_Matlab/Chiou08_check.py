#!/usr/bin/env python

"""A simplistic implementation of Chiou08.

Should be as different from code in ground_motion_interface.py
as possible.
"""

import math


# Chiou08_Table2 = array([
# #  C1       C1a      C1b     Cn     CM      C5      C6      C7      C7a     C9      C9a      C10     Cgamma1   Cgamma2
# [-1.2687,  0.1,    -0.2550, 2.996, 4.1840, 6.1600, 0.4893, 0.0512, 0.0860, 0.7900, 1.5005, -0.3218, -0.00804, -0.00785],   # pga
# [-1.2687,  0.1,    -0.2550, 2.996, 4.1840, 6.1600, 0.4893, 0.0512, 0.0860, 0.7900, 1.5005, -0.3218, -0.00804, -0.00785],   # 0.01
# [-1.2515,  0.1,    -0.2550, 3.292, 4.1879, 6.1580, 0.4892, 0.0512, 0.0860, 0.8129, 1.5028, -0.3323, -0.00811, -0.00792],   # 0.02
# [-1.1744,  0.1,    -0.2550, 3.514, 4.1556, 6.1550, 0.4890, 0.0511, 0.0860, 0.8439, 1.5071, -0.3394, -0.00839, -0.00819],   # 0.03
# [-1.0671,  0.1,    -0.2550, 3.563, 4.1226, 6.1508, 0.4888, 0.0508, 0.0860, 0.8740, 1.5138, -0.3453, -0.00875, -0.00855],   # 0.04
# [-0.9464,  0.1,    -0.2550, 3.547, 4.1011, 6.1441, 0.4884, 0.0504, 0.0860, 0.8996, 1.5230, -0.3502, -0.00912, -0.00891],   # 0.05
# [-0.7051,  0.1,    -0.2540, 3.448, 4.0860, 6.1200, 0.4872, 0.0495, 0.0860, 0.9442, 1.5597, -0.3579, -0.00973, -0.00950],   # 0.075
# [-0.5747,  0.1,    -0.2530, 3.312, 4.1030, 6.0850, 0.4854, 0.0489, 0.0860, 0.9677, 1.6104, -0.3604, -0.00975, -0.00952],   # 0.1
# [-0.5309,  0.1,    -0.2500, 3.044, 4.1717, 5.9871, 0.4808, 0.0479, 0.0860, 0.9660, 1.7549, -0.3565, -0.00883, -0.00862],   # 0.15
# [-0.6352,  0.1,    -0.2449, 2.831, 4.2476, 5.8699, 0.4755, 0.0471, 0.0860, 0.9334, 1.9157, -0.3470, -0.00778, -0.00759],   # 0.2
# [-0.7766,  0.1,    -0.2382, 2.658, 4.3184, 5.7547, 0.4706, 0.0464, 0.0860, 0.8946, 2.0709, -0.3379, -0.00688, -0.00671],   # 0.25
# [-0.9278,  0.0999, -0.2313, 2.505, 4.3844, 5.6527, 0.4665, 0.0458, 0.0860, 0.8590, 2.2005, -0.3314, -0.00612, -0.00598],   # 0.3
# [-1.2176,  0.0997, -0.2146, 2.261, 4.4979, 5.4997, 0.4607, 0.0445, 0.0850, 0.8019, 2.3886, -0.3256, -0.00498, -0.00486],   # 0.4
# [-1.4695,  0.0991, -0.1972, 2.087, 4.5881, 5.4029, 0.4571, 0.0429, 0.0830, 0.7578, 2.5000, -0.3189, -0.00420, -0.00410],   # 0.5
# [-1.9278,  0.0936, -0.1620, 1.812, 4.7571, 5.2900, 0.4531, 0.0387, 0.0690, 0.6788, 2.6224, -0.2702, -0.00308, -0.00301],   # 0.75
# [-2.2453,  0.0766, -0.1400, 1.648, 4.8820, 5.2480, 0.4517, 0.0350, 0.0450, 0.6196, 2.6690, -0.2059, -0.00246, -0.00241],   # 1.0
# [-2.7307,  0.0022, -0.1184, 1.511, 5.0697, 5.2194, 0.4507, 0.0280, 0.0134, 0.5101, 2.6985, -0.0852, -0.00180, -0.00176],   # 1.5
# [-3.1413, -0.0591, -0.1100, 1.470, 5.2173, 5.2099, 0.4504, 0.0213, 0.0040, 0.3917, 2.7085,  0.0160, -0.00147, -0.00143],   # 2.0
# [-3.7413, -0.0931, -0.1040, 1.456, 5.4385, 5.2040, 0.4501, 0.0106, 0.0010, 0.1244, 2.7145,  0.1876, -0.00117, -0.00115],   # 3.0
# [-4.1814, -0.0982, -0.1020, 1.465, 5.5977, 5.2020, 0.4501, 0.0041, 0,      0.0086, 2.7164,  0.3378, -0.00107, -0.00104],   # 4.0
# [-4.5187, -0.0994, -0.1010, 1.478, 5.7276, 5.2010, 0.4500, 0.0010, 0,      0,      2.7172,  0.4579, -0.00102, -0.00099],   # 5.0
# [-5.1224, -0.0999, -0.1010, 1.498, 5.9891, 5.2000, 0.4500, 0,      0,      0,      2.7177,  0.7514, -0.00096, -0.00094],   # 7.5
# [-5.5872, -0.1,    -0.1000, 1.502, 6.1930, 5.2000, 0.4500, 0,      0,      0,      2.7180,  1.1856, -0.00094, -0.00091]])  # 10.0
# 
# Chiou08_Table3 = array([
# # phi1     phi2     phi3      phi4      phi5    phi6      phi7    phi8
# [-0.4417, -0.1417, -0.007010, 0.102151, 0.2289, 0.014996, 580.0,  0.0700],  # pga
# [-0.4417, -0.1417, -0.007010, 0.102151, 0.2289, 0.014996, 580.0,  0.0700],  # 0.01
# [-0.4340, -0.1364, -0.007279, 0.108360, 0.2289, 0.014996, 580.0,  0.0699],  # 0.02
# [-0.4177, -0.1403, -0.007354, 0.119888, 0.2289, 0.014996, 580.0,  0.0701],  # 0.03
# [-0.4000, -0.1591, -0.006977, 0.133641, 0.2289, 0.014996, 579.9,  0.0702],  # 0.04
# [-0.3903, -0.1862, -0.006467, 0.148927, 0.2290, 0.014996, 579.9,  0.0701],  # 0.05
# [-0.4040, -0.2538, -0.005734, 0.190596, 0.2292, 0.014996, 579.6,  0.0686],  # 0.075
# [-0.4423, -0.2943, -0.005604, 0.230662, 0.2297, 0.014996, 579.2,  0.0646],  # 0.1
# [-0.5162, -0.3113, -0.005845, 0.266468, 0.2326, 0.014988, 577.2,  0.0494],  # 0.15
# [-0.5697, -0.2927, -0.006141, 0.255253, 0.2386, 0.014964, 573.9, -0.0019],  # 0.2
# [-0.6109, -0.2662, -0.006439, 0.231541, 0.2497, 0.014881, 568.5, -0.0479],  # 0.25
# [-0.6444, -0.2405, -0.006704, 0.207277, 0.2674, 0.014639, 560.5, -0.0756],  # 0.3
# [-0.6931, -0.1975, -0.007125, 0.165464, 0.3120, 0.013493, 540.0, -0.0960],  # 0.4
# [-0.7246, -0.1633, -0.007435, 0.133828, 0.3610, 0.011133, 512.9, -0.0998],  # 0.5
# [-0.7708, -0.1028, -0.008120, 0.085153, 0.4353, 0.006739, 441.9, -0.0765],  # 0.75
# [-0.7990, -0.0699, -0.008444, 0.058595, 0.4629, 0.005749, 391.8, -0.0412],  # 1.0
# [-0.8382, -0.0425, -0.007707, 0.031787, 0.4756, 0.005544, 348.1,  0.0140],  # 1.5
# [-0.8663, -0.0302, -0.004792, 0.019716, 0.4785, 0.005521, 332.5,  0.0544],  # 2.0
# [-0.9032, -0.0129, -0.001828, 0.009643, 0.4796, 0.005517, 324.1,  0.1232],  # 3.0
# [-0.9231, -0.0016, -0.001523, 0.005379, 0.4799, 0.005517, 321.7,  0.1859],  # 4.0
# [-0.9222,  0.0000, -0.001440, 0.003223, 0.4799, 0.005517, 320.9,  0.2295],  # 5.0
# [-0.8346,  0.0000, -0.001369, 0.001134, 0.4800, 0.005517, 320.3,  0.2660],  # 7.5
# [-0.7332,  0.0000, -0.001361, 0.000515, 0.4800, 0.005517, 320.1,  0.2682]]) # 10.0
#
# Chiou08_Table4 = array([
#  tau1    tau2    sigma1  sigma2  sigma3  sigma4
# [0.3437, 0.2637, 0.4458, 0.3459, 0.8000, 0.0663],  # pga
# [0.3437, 0.2637, 0.4458, 0.3459, 0.8000, 0.0663],  # 0.01
# [0.3471, 0.2671, 0.4458, 0.3459, 0.8000, 0.0663],  # 0.02
# [0.3603, 0.2803, 0.4535, 0.3537, 0.8000, 0.0663],  # 0.03
# [0.3718, 0.2918, 0.4589, 0.3592, 0.8000, 0.0663],  # 0.04
# [0.3848, 0.3048, 0.4630, 0.3635, 0.8000, 0.0663],  # 0.05
# [0.3878, 0.3129, 0.4702, 0.3713, 0.8000, 0.0663],  # 0.075
# [0.3835, 0.3152, 0.4747, 0.3769, 0.8000, 0.0663],  # 0.1
# [0.3719, 0.3128, 0.4798, 0.3847, 0.8000, 0.0612],  # 0.15
# [0.3601, 0.3076, 0.4816, 0.3902, 0.8000, 0.0530],  # 0.2
# [0.3522, 0.3047, 0.4815, 0.3946, 0.7999, 0.0457],  # 0.25
# [0.3438, 0.3005, 0.4801, 0.3981, 0.7997, 0.0398],  # 0.3
# [0.3351, 0.2984, 0.4758, 0.4036, 0.7988, 0.0312],  # 0.4
# [0.3353, 0.3036, 0.4710, 0.4079, 0.7966, 0.0255],  # 0.5
# [0.3429, 0.3205, 0.4621, 0.4157, 0.7792, 0.0175],  # 0.75
# [0.3577, 0.3419, 0.4581, 0.4213, 0.7504, 0.0133],  # 1.0
# [0.3769, 0.3703, 0.4493, 0.4213, 0.7136, 0.0090],  # 1.5
# [0.4023, 0.4023, 0.4459, 0.4213, 0.7035, 0.0068],  # 2.0
# [0.4406, 0.4406, 0.4433, 0.4213, 0.7006, 0.0045],  # 3.0
# [0.4784, 0.4784, 0.4424, 0.4213, 0.7001, 0.0034],  # 4.0
# [0.5074, 0.5074, 0.4420, 0.4213, 0.7000, 0.0027],  # 5.0
# [0.5328, 0.5328, 0.4416, 0.4213, 0.7000, 0.0018],  # 7.5
# [0.5542, 0.5542, 0.4414, 0.4213, 0.7000, 0.0014]]) # 10.0


######
# Globals
######

C2 = 1.06
C3 = 3.45
C4 = -2.1
C4a = -0.5
Crb = 50.0
Chm = 3.0
Cgamma3 = 4.0
eta = 0.0
sigma = 0.0

Tolerance = 0.1

######
# The Choiu equations
######

def eqn_13a(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, delta, tab2_coeffs):
    # unpack table2 coefficients
    (C1, C1a, C1b, Cn, CM, C5, C6, C7, C7a, C9, C9a, C10, Cgamma1, Cgamma2) = tab2_coeffs

    # convert delta degrees to radians
    delta_rad = math.pi*delta/180.0

    t1 = C1 + (C1a*Frv + C1b*Fnm + C7*(Ztor-4.0))*(1-AS) + (C10 + C7a*(Ztor-4.0))*AS
    t2 = C2*(M-6.0) + ((C2-C3)/Cn)*math.log(1 + math.exp(Cn*(CM-M)))
    t3 = C4*math.log(Rrup + C5*math.cosh(C6*max(M-Chm, 0)))
    t4 = (C4a-C4)*math.log(math.sqrt(Rrup*Rrup + Crb*Crb))
    t5 = (Cgamma1 + Cgamma2/math.cosh(max(M-Cgamma3, 0)))*Rrup
    t6 = C9*Fhw*math.tanh(Rx*math.cos(delta_rad)*math.cos(delta_rad)/C9a)*(1-math.sqrt(Rjb*Rjb+Ztor*Ztor)/(Rrup+0.001))

    return t1 + t2 + t3 + t4 + t5 + t6

def eqn_13b(Yref, Vs30, Z1, tab3_coeffs):
    # unpack table 3 coefficients
    (phi1, phi2, phi3, phi4, phi5, phi6, phi7, phi8) = tab3_coeffs

    t1 = math.log(Yref) + phi1*min(math.log(Vs30/1130.0), 0)
    t2 = phi2*(math.exp(phi3*(min(Vs30, 1130.0)-360.0))-math.exp(phi3*(1130.0-360.0)))*math.log((Yref*math.exp(eta)+phi4)/phi4)
    t3 = phi5*(1-1/math.cosh(phi6*max(0, Z1-phi7))) + phi8/math.cosh(0.15*max(0,Z1-15.0))
    t4 = eta + sigma

    return t1 + t2 + t3 + t4

def eqn_13(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs):
    lnYref = eqn_13a(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, delta, tab2_coeffs)

    Yref = math.exp(lnYref)
    Z1 = math.exp(28.5 - (3.82/8.0)*math.log(math.pow(Vs30, 8) + math.pow(378.7, 8)))

    return eqn_13b(Yref, Vs30, Z1, tab3_coeffs)

def eqn_19(M, tab4_coeffs):
    (tau1, tau2, sigma1, sigma2, sigma3, sigma4) = tab4_coeffs

    return tau1 + ((tau2-tau1)/2)*(min(max(M, 5), 7) - 5)

def eqn_20(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab4_coeffs):
    (tau1, tau2, sigma1, sigma2, sigma3, sigma4) = tab4_coeffs

    NL = eqn_20a(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab4_coeffs)
    sigma = (sigma1 + ((sigma2-sigma1)/2)*(min(max(M, 5), 7)-5) + sigma4*AS)*math.sqrt((sigma3*Finferred + 0.7*Fmeasured)+(1+NL)*(1+NL))

def eqn_20a(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab4_coeffs):
    return 0

def eqn_21(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab4_coeffs):
#    NL0 = 0
#    tau = eqn_19(M, tab4_coeffs)
#    Enl0 = 0
#
#    return math.sqrt((1_NL0)*(1+NL0)*tau*tau+Enl0*Enl0)
    return 0

######
# handle doing one estimate
######

def estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected):
    lnY = eqn_13(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs)
    g = math.exp(lnY)
    tol = abs(g-expected)/max(g, expected)
    flag = ' ' if tol < Tolerance else '*'
    print('period=%.2f, Vs30=%.1f, Rx=%5.1f, M=%.1f\tlnY=%f\tg=%f, expected=%f, tol=%.2f%s'
          % (period, Vs30, Rx, M, lnY, g, expected, tol, flag))

def estimate_sigma(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab4_coeffs, expected):
#    Et = eqn_21(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab4_coeffs)
#    g = math.exp(lnY)
#    tol = abs(g-expected)/max(g, expected) 
#    flag = ' ' if tol < Tolerance else '*'
#    print('period=%.2f, Vs30=%.1f, Rx=%5.1f, M=%.1f\tlnY=%f\tg=%f, expected=%f, tol=%.2f%s'
#          % (period, Vs30, Rx, M, lnY, g, expected, tol, flag))
    pass


######
# Handle various cases
######

# constants for 'reverse' case, rock
Frv = 1
Fnm = 0
Fhw = 0

Ztor = 0.0		# rupture touches surface
AS = 0			# not aftershock case

delta = 90		# vertical strike-slip fault

print('Chiou08')
print('Frv=%d, Fnm=%d, Fhw=%d' % (Frv, Fnm, Fhw))
Vs30 = 520.0		# from figure 19, page 206
print('Rock, delta=%d %s' % (delta, '*' * 80))

# period = 0.01, M=5.5
period = 0.01
M = 5.5
tab2_coeffs = [-1.2687,  0.1,    -0.2550, 2.996, 4.1840, 6.1600, 0.4893, 0.0512, 0.0860, 0.7900, 1.5005, -0.3218, -0.00804, -0.00785]
tab3_coeffs = [-0.4417, -0.1417, -0.007010, 0.102151, 0.2289, 0.014996, 580.0,  0.0700]

Rrup = Rjb = Rx = 5.0
expected = 0.25

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.065

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.0062

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

# period = 0.01, M=7.5
M = 7.5

Rrup = Rjb = Rx = 5.0
expected = 0.49

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.21

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.048

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)


print('-' * 95)


# period = 0.2, M=5.5
period = 0.2
M = 5.5
tab2_coeffs = [-0.6352,  0.1,    -0.2449, 2.831, 4.2476, 5.8699, 0.4755, 0.0471, 0.0860, 0.9334, 1.9157, -0.3470, -0.00778, -0.00759]
tab3_coeffs = [-0.5697, -0.2927, -0.006141, 0.255253, 0.2386, 0.014964, 573.9, -0.0019]

Rrup = Rjb = Rx = 5.0
expected = 0.60

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.14

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.014

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

# period = 0.2, M=7.5
M = 7.5

Rrup = Rjb = Rx = 5.0
expected = 1.3

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.5

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.10

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)


print('-' * 95)


# period = 1.0, M=5.5
period = 1.0
M = 5.5
tab2_coeffs = [-2.2453,  0.0766, -0.1400, 1.648, 4.8820, 5.2480, 0.4517, 0.0350, 0.0450, 0.6196, 2.6690, -0.2059, -0.00246, -0.00241]
tab3_coeffs = [-0.7990, -0.0699, -0.008444, 0.058595, 0.4629, 0.005749, 391.8, -0.0412]

Rrup = Rjb = Rx = 5.0
expected = 0.11

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.031

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.0051

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

# period = 0.2, M=7.5
M = 7.5

Rrup = Rjb = Rx = 5.0
expected = 0.50

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.19

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.05

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)


print('-' * 95)


# period = 3.0, M=5.5
period = 3.0
M = 5.5
tab2_coeffs = [-3.7413, -0.0931, -0.1040, 1.456, 5.4385, 5.2040, 0.4501, 0.0106, 0.0010, 0.1244, 2.7145,  0.1876, -0.00117, -0.00115]
tab3_coeffs = [-0.9032, -0.0129, -0.001828, 0.009643, 0.4796, 0.005517, 324.1,  0.1232]

Rrup = Rjb = Rx = 5.0
expected = 0.019

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.0043

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.0007

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

# period = 0.2, M=7.5
M = 7.5

Rrup = Rjb = Rx = 5.0
expected = 0.123

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.051

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.015

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)


print('=' * 95)


# period = 0.01, M=5.5
period = 0.01
M = 5.5
tab4_coeffs = [0.3437, 0.2637, 0.4458, 0.3459, 0.8000, 0.0663]  # 0.01

Rrup = Rjb = Rx = 5.0
expected = 0.25

estimate_sigma(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab4_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.065

estimate_sigma(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab4_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.0062

estimate_sigma(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab4_coeffs, expected)









Vs30 = 310.0		# from figure 19, page 206
print('Soil, delta=%d %s' % (delta, '*' * 80))

# period = 0.01, M=5.5
period = 0.01
M = 5.5
tab2_coeffs = [-1.2687,  0.1,    -0.2550, 2.996, 4.1840, 6.1600, 0.4893, 0.0512, 0.0860, 0.7900, 1.5005, -0.3218, -0.00804, -0.00785]
tab3_coeffs = [-0.4417, -0.1417, -0.007010, 0.102151, 0.2289, 0.014996, 580.0,  0.0700]

Rrup = Rjb = Rx = 5.0
expected = 0.29

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.081

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.008

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

# period = 0.01, M=7.5
M = 7.5

Rrup = Rjb = Rx = 5.0
expected = 0.49

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.23

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.059

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)


print('-' * 95)


# period = 0.2, M=5.5
period = 0.2
M = 5.5
tab2_coeffs = [-0.6352,  0.1,    -0.2449, 2.831, 4.2476, 5.8699, 0.4755, 0.0471, 0.0860, 0.9334, 1.9157, -0.3470, -0.00778, -0.00759]
tab3_coeffs = [-0.5697, -0.2927, -0.006141, 0.255253, 0.2386, 0.014964, 573.9, -0.0019]

Rrup = Rjb = Rx = 5.0
expected = 0.60

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.19

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.019

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

# period = 0.2, M=7.5
M = 7.5

Rrup = Rjb = Rx = 5.0
expected = 1.0

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.53

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.13

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)


print('-' * 95)


# period = 1.0, M=5.5
period = 1.0
M = 5.5
tab2_coeffs = [-2.2453,  0.0766, -0.1400, 1.648, 4.8820, 5.2480, 0.4517, 0.0350, 0.0450, 0.6196, 2.6690, -0.2059, -0.00246, -0.00241]
tab3_coeffs = [-0.7990, -0.0699, -0.008444, 0.058595, 0.4629, 0.005749, 391.8, -0.0412]

Rrup = Rjb = Rx = 5.0
expected = 0.19

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.05

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.0073

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

# period = 0.2, M=7.5
M = 7.5

Rrup = Rjb = Rx = 5.0
expected = 0.60

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.28

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.078

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)


print('-' * 95)


# period = 3.0, M=5.5
period = 3.0
M = 5.5
tab2_coeffs = [-3.7413, -0.0931, -0.1040, 1.456, 5.4385, 5.2040, 0.4501, 0.0106, 0.0010, 0.1244, 2.7145,  0.1876, -0.00117, -0.00115]
tab3_coeffs = [-0.9032, -0.0129, -0.001828, 0.009643, 0.4796, 0.005517, 324.1,  0.1232]

Rrup = Rjb = Rx = 5.0
expected = 0.03

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.0073

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.0012

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

# period = 0.2, M=7.5
M = 7.5

Rrup = Rjb = Rx = 5.0
expected = 0.2

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 20.0
expected = 0.08

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)

Rrup = Rjb = Rx = 100.0
expected = 0.023

estimate(M, Rrup, Ztor, Rjb, Rx, Frv, Fnm, AS, Vs30, delta, tab2_coeffs, tab3_coeffs, expected)



print('#' * 95)

