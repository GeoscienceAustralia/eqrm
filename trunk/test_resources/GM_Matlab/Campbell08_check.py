#!/usr/bin/env python

"""A simplistic implementation of Campbell08.

Should be as different from code in ground_motion_interface.py
as possible.

The mean values are compared with values from the paper.
The sigma values are compared with values from opensha.org.
"""

import sys
import math

# table 2
# #  C0     C1      C2      C3      C4     C5     C6    C7      C8     C9      C10    C11    C12     K1    K2     K3
# [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839] # 0.010
# [ -1.680, 0.500, -0.530, -0.262, -2.123, 0.170, 5.60, 0.280, -0.120, 0.490,  1.102, 0.040, 0.610,  865, -1.219, 1.840] # 0.020
# [ -1.552, 0.500, -0.530, -0.262, -2.145, 0.170, 5.60, 0.280, -0.120, 0.490,  1.174, 0.040, 0.610,  908, -1.273, 1.841] # 0.030
# [ -1.209, 0.500, -0.530, -0.267, -2.199, 0.170, 5.74, 0.280, -0.120, 0.490,  1.272, 0.040, 0.610, 1054, -1.346, 1.843] # 0.050
# [ -0.657, 0.500, -0.530, -0.302, -2.277, 0.170, 7.09, 0.280, -0.120, 0.490,  1.438, 0.040, 0.610, 1086, -1.471, 1.845] # 0.075
# [ -0.314, 0.500, -0.530, -0.324, -2.318, 0.170, 8.05, 0.280, -0.099, 0.490,  1.604, 0.040, 0.610, 1032, -1.624, 1.847] # 0.10
# [ -0.133, 0.500, -0.530, -0.339, -2.309, 0.170, 8.79, 0.280, -0.048, 0.490,  1.928, 0.040, 0.610,  878, -1.931, 1.852] # 0.15
# [ -0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
# [ -0.890, 0.500, -0.362, -0.458, -2.146, 0.170, 6.58, 0.280,  0.000, 0.490,  2.351, 0.040, 0.700,  654, -2.381, 1.861] # 0.25
# [ -1.171, 0.500, -0.294, -0.511, -2.095, 0.170, 6.04, 0.280,  0.000, 0.490,  2.460, 0.040, 0.750,  587, -2.518, 1.865] # 0.30
# [ -1.466, 0.500, -0.186, -0.592, -2.066, 0.170, 5.30, 0.280,  0.000, 0.490,  2.587, 0.040, 0.850,  503, -2.657, 1.874] # 0.40
# [ -2.569, 0.656, -0.304, -0.536, -2.041, 0.170, 4.73, 0.280,  0.000, 0.490,  2.544, 0.040, 0.883,  457, -2.669, 1.883] # 0.50
# [ -4.844, 0.972, -0.578, -0.406, -2.000, 0.170, 4.00, 0.280,  0.000, 0.490,  2.133, 0.077, 1.000,  410, -2.401, 1.906] # 0.75
# [ -6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
# [ -8.692, 1.513, -1.046, -0.185, -2.000, 0.170, 4.00, 0.161,  0.000, 0.490,  0.406, 0.253, 1.000,  400, -1.025, 1.974] # 1.5
# [ -9.701, 1.600, -0.978, -0.236, -2.000, 0.170, 4.00, 0.094,  0.000, 0.371, -0.456, 0.300, 1.000,  400, -0.299, 2.019] # 2.0
# [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
# [-11.212, 1.600, -0.316, -0.770, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.200] # 4.0
# [-11.684, 1.600, -0.070, -0.986, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.291] # 5.0
# [-12.505, 1.600, -0.070, -0.656, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.517] # 7.5
# [-13.087, 1.600, -0.070, -0.422, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # 10.0
# [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839] # PGA
# [  0.954, 0.696, -0.309, -0.019, -2.016, 0.170, 4.00, 0.245,  0.000, 0.358,  1.694, 0.092, 1.000,  400, -1.955, 1.929] # PGV
# [ -5.270, 1.600, -0.070,  0.000, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # PGD

# table 3
#ElnY   TlnY   Ec     Et     Earb   rho
# [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # 0.010
# [0.480, 0.219, 0.166, 0.528, 0.553, 0.999] # 0.020
# [0.489, 0.235, 0.165, 0.543, 0.567, 0.989] # 0.030
# [0.510, 0.258, 0.162, 0.572, 0.594, 0.963] # 0.050
# [0.520, 0.292, 0.158, 0.596, 0.617, 0.922] # 0.075
# [0.531, 0.286, 0.170, 0.603, 0.627, 0.898] # 0.10
# [0.532, 0.280, 0.180, 0.601, 0.628, 0.890] # 0.15
# [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
# [0.534, 0.240, 0.191, 0.585, 0.616, 0.852] # 0.25
# [0.544, 0.215, 0.198, 0.585, 0.618, 0.831] # 0.30
# [0.541, 0.217, 0.206, 0.583, 0.618, 0.785] # 0.40
# [0.550, 0.214, 0.208, 0.590, 0.626, 0.735] # 0.50
# [0.568, 0.227, 0.221, 0.612, 0.650, 0.628] # 0.75
# [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
# [0.564, 0.296, 0.222, 0.637, 0.675, 0.411] # 1.5
# [0.571, 0.296, 0.226, 0.643, 0.682, 0.331] # 2.0
# [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0
# [0.576, 0.297, 0.237, 0.648, 0.690, 0.261] # 4.0
# [0.601, 0.359, 0.237, 0.700, 0.739, 0.200] # 5.0
# [0.628, 0.428, 0.271, 0.760, 0.807, 0.174] # 7.5
# [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # 10.0
# [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
# [0.484, 0.203, 0.190, 0.525, 0.558, 0.691] # PGV
# [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # PGD

######
# Globals
######

C = 1.88		# table 2, page 148
N = 1.18

ElnAF = 0.3		# page 150
ElnPGA = 0.478		# ElnY for PGA, table 3, page 149

Tolerance = 0.10

# constant values
Ztor = 0.0
Frv = 0
Fnm = 0
delta = 90.0

PGA_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839] # PGA
PGA_sigma_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA

# this value assumed in the paper
Z25 = 2.0

######
# Code mimicing the FORTRAN
######

def CB08_MODEL(period, M, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs):
    """This code mimics the code in CB08_MODEL.FOR.

    The major difference is that here we pass in the coefficient arrays specific
    to the period.  The PGA coefficients are globals.
    """

    # unpack table 2 coefficients and PGA coefficients
    (C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,K1,K2,K3) = tab2_coeffs
    (pC0,pC1,pC2,pC3,pC4,pC5,pC6,pC7,pC8,pC9,pC10,pC11,pC12,pK1,pK2,pK3) = PGA_coeffs

    # unpack table 3 coefficients and PGA coefficients
    (ElnY, taulnY, EC, ET, EArb, rho) = tab3_coeffs
    (pElnY, ptaulnY, pEC, pET, pEArb, prho) = PGA_sigma_coeffs
    # NOTE: ET, pET, EArb, pEArb aren't used in this code

    ######
    # Calculate the rock PGA
    ######

    # magnitude term
    if M <= 5.5:
        Fmag = pC0 + pC1*M
    elif M <= 6.5:
        Fmag = pC0 + pC1*M + pC2*(M-5.5)
    else:
        Fmag = pC0 + pC1*M + pC2*(M-5.5) + pC3*(M-6.5)

    # distance term
    R = math.sqrt(Rrup*Rrup + pC6*pC6)
    Fdis = (pC4 + pC5*M)*math.log(R)

    # style-of-faulting term
    if Ztor < 1.0:
        Ffltz = Ztor
    else:
        Ffltz = 1.0

    Fflt = pC7*Frv*Ffltz + pC8*Fnm

    # hanging wall term
    if Rjb == 0.0:
        Fhngr = 1.0
    elif Ztor < 1.0:
        Rmax = max(Rrup, math.sqrt(Rjb*Rjb+1.0))
        Fhngr = (Rmax - Rjb)/Rmax
    else:
        Fhngr = (Rrup - Rjb)/Rrup

    if M <= 6.0:
        Fhngm = 0.0
    elif M < 6.5:
        Fhngm = 2.0*(M-6.0)
    else:
        Fhngm = 1.0

    if Ztor >= 20.0:
        Fhngz = 0.0
    else:
        Fhngz = (20.0 - Ztor)/20.0

    if delta <= 70.0:
        Fhngd = 1.0
    else:
        Fhngd = (90.0 - delta)/20.0

    Fhng = pC9*Fhngr*Fhngm*Fhngz*Fhngd

    # shallow site response term (Vs30 = 1100)
    Fsite = (pC10 + pK2*N)*math.log(1100.0/pK1)

    # basin response term
    if Z25 < 1.0:
        Fsed = pC11*(Z25 - 1.0)
    elif Z25 <= 3.0:
        Fsed = 0.0
    else:
        Fsed = pC12*pK3*math.exp(-0.75)*(1.0 - math.exp(-0.25*(Z25-3.0)))

    # PGA on rock
    A1100 = math.exp(Fmag + Fdis + Fflt + Fhng + Fsite + Fsed)

    # PGA on local site conditions
    PGA = math.exp(math.log(A1100) - Fsite)
    if Vs30 < pK1:
        Fsite = pC10*math.log(Vs30/pK1) + pK2*(math.log(A1100+C*math.pow((Vs30/pK1), N)) - math.log(A1100+C))
    elif Vs30 < 1100.0:
        Fsite = (pC10 + pK2*N)*math.log(Vs30/pK1)
    else:
        Fsite = (pC10 + pK2*N)*math.log(1100.0/pK1)
    PGA = math.exp(math.log(PGA) + Fsite)

    # standard deviation of ln PGA
    slnPGA = pElnY
    tlnPGA = ptaulnY

    ######
    # Now calculate the strong motion parameter
    ######

    # magnitude term
    if M <= 5.5:
        Fmag = C0 + C1*M
    elif M <= 6.5:
        Fmag = C0 + C1*M + C2*(M-5.5)
    else:
        Fmag = C0 + C1*M + C2*(M-5.5) + C3*(M-6.5)

    # distance term
    R = math.sqrt(Rrup*Rrup + C6*C6)
    Fdis = (C4 + C5*M)*math.log(R)

    # style-of-faulting term
    if Ztor < 1.0:
        Ffltz = Ztor
    else:
        Ffltz = 1.0

    Fflt = C7*Frv*Ffltz + C8*Fnm

    # hanging wall term
    if Rjb == 0.0:
        Fhngr = 1.0
    elif Ztor < 1.0:
        Rmax = max(Rrup, math.sqrt(Rjb*Rjb+1.0))
        Fhngr = (Rmax - Rjb)/Rmax
    else:
        Fhngr = (Rrup - Rjb)/Rrup

    if M <= 6.0:
        Fhngm = 0.0
    elif M < 6.5:
        Fhngm = 2.0*(M-6.0)
    else:
        Fhngm = 1.0

    if Ztor >= 20.0:
        Fhngz = 0.0
    else:
        Fhngz = (20.0 - Ztor)/20.0

    if delta <= 70.0:
        Fhngd = 1.0
    else:
        Fhngd = (90.0 - delta)/20.0

    Fhng = C9*Fhngr*Fhngm*Fhngz*Fhngd

    # shallow site response term (Vs30 = 1100)
    if Vs30 < K1:
        #Fsite = C10*math.log(Vs30/K1) + K2*(math.log(A1100+C*math.pow((Vs30/K1), N))) - math.log(A1100+C)
        Fsite = C10*math.log(Vs30/K1) + K2*(math.log(A1100+C*math.pow((Vs30/K1), N)) - math.log(A1100+C))
    elif Vs30 < 1100.0:
        Fsite = (C10 + K2*N)*math.log(Vs30/K1)
    else:
        Fsite = (C10 + K2*N)*math.log(1100.0/K1)

    # basin response term
    if Z25 < 1.0:
        Fsed = C11*(Z25 - 1.0)
    elif Z25 <= 3.0:
        Fsed = 0.0
    else:
        Fsed = C12*K3*math.exp(-0.75)*(1.0 - math.exp(-0.25*(Z25-3.0)))

    # calculate ground motion parameter
    Y = math.exp(Fmag + Fdis + Fflt + Fhng + Fsite + Fsed)

    # check if Y < PGA at short periods
    if (period <= 0.25) and (Y < PGA):
        Y = PGA

    ######
    # calculate aleatory uncertainty
    ######

    # linearized relationship between Fsite and ln(PGA)
    if Vs30 < K1:
        alpha = K2*A1100*(1.0/(A1100+C*math.pow((Vs30/K1), N)) - 1.0/(A1100+C))
    else:
        alpha = 0.0

    # intra-event standard deviation at base of site profile
    slnYB = math.sqrt(ElnY*ElnY - ElnAF*ElnAF)
    slnAB = math.sqrt(slnPGA*slnPGA - ElnAF*ElnAF)

    # standard deviation of geometric mean of ln(Y)
    sigma = math.sqrt(slnYB*slnYB + ElnAF*ElnAF + alpha*alpha*slnAB*slnAB + 2.0*alpha*rho*slnYB*slnAB)
    tau = taulnY
    sig = math.sqrt(sigma*sigma + tau*tau)

    # standard deviation of arbitrary horizontal component of ln(Y)
    sigarb = math.sqrt(sig*sig + EC*EC)

    return (math.log(Y), math.log(sigma), tau, sig, sigarb)

######
# The Campbell08 equation(s) from the paper
######

def eqn_1(M, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs):
    Fmag = eqn_2(M, tab2_coeffs)
    Fdis = eqn_3(M, Rrup, tab2_coeffs)
    Fflt = eqn_4(Ztor, tab2_coeffs)
    Fhng = eqn_6(M, Rrup, Rjb, Ztor, delta, tab2_coeffs)
    Fsite = eqn_11(M, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs)
    Fsed = eqn_12(M, Rrup, Rjb, Vs30, tab2_coeffs)

    sigma = eqn_16(M, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs)

    return (Fmag + Fdis + Fflt + Fhng + Fsite + Fsed, math.log(sigma))

def eqn_2(M, tab2_coeffs):
    # unpack table 2 coefficients
    (C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,K1,K2,K3) = tab2_coeffs
    
    if M <= 5.5:
        return C0 + C1*M
    if M <= 6.5:
        return C0 + C1*M + C2*(M-5.5)
    return C0 + C1*M + C2*(M-5.5) + C3*(M-6.5)

def eqn_3(M, Rrup, tab2_coeffs):
    # unpack table 2 coefficients
    (C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,K1,K2,K3) = tab2_coeffs

    return (C4 + C5*M)*math.log(math.sqrt(Rrup*Rrup + C6*C6))

def eqn_4(Ztor, tab2_coeffs):
    # unpack table 2 coefficients
    (C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,K1,K2,K3) = tab2_coeffs

    Ffltz = eqn_5(Ztor)

    return C7*Frv*Ffltz + C8*Fnm

def eqn_5(Ztor):
    if Ztor < 1.0:
        return Ztor
    return 1.0

def eqn_6(M, Rrup, Rjb, Ztor, delta, tab2_coeffs):
    # unpack table 2 coefficients
    (C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,K1,K2,K3) = tab2_coeffs

    Fhngr = eqn_7(Rrup, Rjb, Ztor)
    Fhngm = eqn_8(M)
    Fhngz = eqn_9(Ztor)
    Fhngdelta = eqn_10(delta)

    return C9*Fhngr*Fhngm*Fhngz*Fhngdelta

def eqn_7(Rrup, Rjb, Ztor):
    if Rjb < 1.0e-5:		# test for very small, not 0
        return 1.0
    if Ztor < 1.0:
        Rjb2_1 = math.sqrt(Rjb*Rjb+1)
        return (max(Rrup, Rjb2_1) - Rjb) / max(Rrup, Rjb2_1)
    return (Rrup-Rjb)/Rrup

def eqn_8(M):
    if M <= 6.0:
        return 0.0
    if M < 6.5:
        return 2*(M-6.0)
    return 1.0

def eqn_9(Ztor):
    if Ztor >= 20.0:
        return 0.0
    return (20.0-Ztor)/20.0

def eqn_10(delta):
    if delta <= 70.0:
        return 1.0
    return (90.0-delta)/20.0

def eqn_11(M, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs):
    # unpack table 2 coefficients
    (C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,K1,K2,K3) = tab2_coeffs

    tmp = Vs30/K1
    if Vs30 < K1:
        A1100 = eqn_A1100(M, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs)
        return C10*math.log(tmp) + K2*(math.log(A1100 + C*math.pow(tmp, N))-math.log(A1100+C))
    if Vs30 < 1100:
        return (C10+K2*N)*math.log(tmp)
    return (C10+K2*N)*math.log(1100.0/K1)

def eqn_12(M, Rrup, Rjb, Vs30, tab2_coeffs):
    # unpack table 2 coefficients
    (C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,K1,K2,K3) = tab2_coeffs

    if Z25 < 1.0:
        return C11*(Z25-1.0)
    if Z25 <= 3.0:
        return 0
    return C12*K3*math.exp(-0.75)*(1 - math.exp(-0.25*(Z25-3.0)))

def eqn_14(taulnY):
    return taulnY

def eqn_15(ElnYB, ElnAB, alpha, rho):
    return math.sqrt(ElnYB*ElnYB + ElnAF*ElnAF + alpha*alpha*ElnAB*ElnAB + 2*alpha*rho*ElnYB*ElnAB)

def eqn_16(M, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs):
    # unpack table 3 coeffs
    (ElnY, taulnY, EC, ET, EArb, rho) = tab3_coeffs

    ElnYB = math.sqrt(ElnY*ElnY - ElnAF*ElnAF)		# page 147
    ElnAB = math.sqrt(ElnPGA*ElnPGA - ElnAF*ElnAF)	# page 147

    alpha = eqn_17(M, Rrup, Rjb, Ztor, delta, Vs30, tab2_coeffs, tab3_coeffs)

    # calculate sigma, return log(sigma)
    sigma = eqn_15(ElnYB, ElnAB, alpha, rho)
    tau = eqn_14(taulnY)

    return math.sqrt(sigma*sigma + tau*tau)

def eqn_17(M, Rrup, Rjb, Ztor, delta, Vs30, tab2_coeffs, tab3_coeffs):
    # unpack table 2 coefficients
    (C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,K1,K2,K3) = tab2_coeffs

    if Vs30 >= K1:
        return 0.0

    A1100 = eqn_A1100(M, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs)

    tmp1 = 1/(A1100+C*math.pow(Vs30/K1, N))
    tmp2 = 1/(A1100+C)
    alpha = K2*A1100*(tmp1 - tmp2)
    return alpha

def eqn_A1100(M, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs):
    """Perform eqn 1 with PGA data, Vs30=1100.0"""

    (result, _) = eqn_1(M, Rrup, Rjb, Ztor, 1100.0, delta, PGA_coeffs, PGA_sigma_coeffs)
    result = math.exp(result)

    return result

def eqn_page147(A1100, Fsite, tab2_coeffs, tab3_coeffs):
    # implement the limit of PSA for short periods on page 147, paragraph 2
    (C0,C1,C2,C3,C4,C5,C6,C7,C8,C9,C10,C11,C12,K1,K2,K3) = tab2_coeffs

    # get PGA rock - remove site component
    pga = math.exp(math.log(A1100) - Fsite)

    # compute site response using Vs30 supplied
    Fsite = eqn_11(M, Rrup, Rjb, Ztor, Vs30, delta, PGA_coeffs, PGA_sigma_coeffs)

    pga = math.exp(math.log(pga) + Fsite)

    return pga

######
# handle doing one estimate (log_mean or log_sigma)
######

def estimate(period, Mw, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs, expected):
    #(lnY, lnE) = eqn_1(Mw, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs)
    (lnY, lnE) = CB08_MODEL(period, Mw, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs)
    g = math.exp(lnY)
    sigma = math.exp(lnE)
    tol = abs(g-expected)/max(g, expected)
    flag = ' ' if tol <= Tolerance else '*'
    print('period=%5.2f, Z25=%3.1f, Rrup=%5.1f, Rjb=%5.1f, del=%f, M=%.1f, lnY=%8.4f\tg=%7.5f, expected=%7.5f, tol=%.2f%s'
          % (period, Z25, Rrup, Rjb, (Rrup-Rjb)/Rrup, Mw, lnY, g, expected, tol, flag))
#          % (period, Z25, Rrup, Rjb, Mw, lnY, lnE, sigma, g, expected, tol, flag))

def estimate_sigma(period, Mw, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs, expected):
    #(lnY, lnE) = eqn_1(Mw, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs)
    (lnY, lnE) = CB08_MODEL(period, Mw, Rrup, Rjb, Ztor, Vs30, delta, tab2_coeffs, tab3_coeffs)
    g = math.exp(lnY)
    sigma = math.exp(lnE)
    tol = abs(sigma-expected)/max(sigma, expected)
    flag = ' ' if tol <= Tolerance else '*'
    print('period=%5.2f, Z25=%3.1f, Rrup=%5.1f, Rjb=%5.1f, M=%.1f, Vs30=%6.1f, g=%6.4f\tsigma=%7.5f, expected sigma=%7.5f, tol=%.2f%s'
          % (period, Z25, Rrup, Rjb, Mw, Vs30, g, sigma, expected, tol, flag))

######
# Handle various cases
######

# cases from the CB08_MODEL.FOR program, limited for testing
Rrup_M5 = [5.0, 10.0, 15.0, 30.0, 50.0, 100.0, 200.0]
Rrup_M7 = [5.0, 10.0, 15.0, 30.0, 50.0, 100.0, 200.0]
Rjb_M5_SS = [0.0, 8.7, 14.1, 29.6, 49.7, 99.9, 199.9]
Rjb_M5_RV = [0.0, 7.0, 13.2, 29.1, 49.5, 99.7, 199.9]
Rjb_M7_SS = [5.0, 10.0, 15.0, 30.0, 50.0, 100.0, 200.0]
Rjb_M7_RV = [0.0, 0.0, 6.2, 26., 47.7, 98.9, 199.4]
Per = [0.01, 0.2, 1.0, 3.0]


# coefficient lists for different periods
tab2_001 = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
tab3_001 = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
tab2_020 = [ -0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
tab3_020 = [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
tab2_100 = [ -6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
tab3_100 = [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
tab2_300 = [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
tab3_300 = [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0

tab2_per = [tab2_001, tab2_020, tab2_100, tab2_300]
tab3_per = [tab3_001, tab3_020, tab3_100, tab3_300]

# strike/slip faulting

Frv = 0.0
Fnm = 0.0
delta = 90.0
Vs30 = 760.0
Z25 = 2.0

for (pi, period) in enumerate(Per):
    Mw = 5.0
    Ztor = 5.0
    Fltype = 'SS'
    tab2 = tab2_per[pi]
    tab3 = tab3_per[pi]
    print('\nT=%6.3f Mw=%.1f Flt=%s Frv=%.1f Fnm=%.1f Ztor=%4.1f Dip=%4.1f Vs30=%6.1f Z25=%4.1f\n'
          % (period, Mw, Fltype, Frv, Fnm, Ztor, delta, Vs30, Z25))
    print(' Rrup       Rjb        Y          Sigma      Tau        SigT       SigArb')
    for i in range(7):
        (lnY, lnE, tau, sig, sigarb) = CB08_MODEL(period, Mw, Rrup_M5[i], Rjb_M5_SS[i], Ztor, Vs30, delta, tab2, tab3)
        print(' %6.4E %6.4E %6.4E %6.4E %6.4E %6.4E %6.4E'
              % (Rrup_M5[i], Rjb_M5_SS[i], math.exp(lnY), math.exp(lnE), tau, sig, sigarb))

    Mw = 7.0
    Ztor = 0.0
    Fltype = 'SS'
    print('\nT=%6.3f Mw=%.1f Flt=%s Frv=%.1f Fnm=%.1f Ztor=%4.1f Dip=%4.1f Vs30=%6.1f Z25=%4.1f\n'
          % (period, Mw, Fltype, Frv, Fnm, Ztor, delta, Vs30, Z25))
    print(' Rrup       Rjb        Y          Sigma      Tau        SigT       SigArb')
    for i in range(7):
        (lnY, lnE, tau, sig, sigarb) = CB08_MODEL(period, Mw, Rrup_M7[i], Rjb_M7_SS[i], Ztor, Vs30, delta, tab2, tab3)
        print(' %6.4E %6.4E %6.4E %6.4E %6.4E %6.4E %6.4E'
              % (Rrup_M7[i], Rjb_M7_SS[i], math.exp(lnY), math.exp(lnE), tau, sig, sigarb))

# reverse faulting

Frv = 1.0
Fnm = 0.0
delta = 45.0
Vs30 = 760.0
Z25 = 2.0

for (pi, period) in enumerate(Per):
    Mw = 5.0
    Ztor = 5.0
    Fltype = 'RV'
    tab2 = tab2_per[pi]
    tab3 = tab3_per[pi]
    print('\nT=%6.3f Mw=%.1f Flt=%s Frv=%.1f Fnm=%.1f Ztor=%4.1f Dip=%4.1f Vs30=%6.1f Z25=%4.1f\n'
          % (period, Mw, Fltype, Frv, Fnm, Ztor, delta, Vs30, Z25))
    print(' Rrup       Rjb        Y         Sigma     Tau        SigT       SigArb')
    for i in range(7):
        (lnY, lnE, tau, sig, sigarb) = CB08_MODEL(period, Mw, Rrup_M5[i], Rjb_M5_RV[i], Ztor, Vs30, delta, tab2, tab3)
        print(' %6.4E %6.4E %6.4E %6.4E %6.4E %6.4E %6.4E'
              % (Rrup_M5[i], Rjb_M5_RV[i], math.exp(lnY), math.exp(lnE), tau, sig, sigarb))

    Mw = 7.0
    Ztor = 0.0
    Fltype = 'RV'
    print('\nT=%6.3f Mw=%.1f Flt=%s Frv=%.1f Fnm=%.1f Ztor=%4.1f Dip=%4.1f Vs30=%6.1f Z25=%4.1f\n'
          % (period, Mw, Fltype, Frv, Fnm, Ztor, delta, Vs30, Z25))
    print(' Rrup       Rjb        Y         Sigma     Tau        SigT       SigArb')
    for i in range(7):
        (lnY, lnE, tau, sig, sigarb) = CB08_MODEL(period, Mw, Rrup_M7[i], Rjb_M7_RV[i], Ztor, Vs30, delta, tab2, tab3)
        print(' %6.4E %6.4E %6.4E %6.4E %6.4E %6.4E %6.4E'
              % (Rrup_M7[i], Rjb_M7_RV[i], math.exp(lnY), math.exp(lnE), tau, sig, sigarb))

        
sys.exit(0)

###################################################################################################
# Code here is old - could still be used to check against opensha.org
###################################################################################################

Vs30 = 760.0

print('Campbell08 model: Ztor=%.1f, Vs30=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Vs30, Frv, Fnm, delta))
print('Tolerance limit=%.2f, tolerance=abs(computed-expected)/'
      'max(computed, expected)'
      % Tolerance)
print('*' * 102)


# period = PGA (0.01), M=5.0, R=2.0km
period = 0.01
Rrup = Rjb = 2.0
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.0
expected = 2.2e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=2.0km
M = 7.0
#expected = 4.3e-1
expected = 4.4e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 1.0e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=10.0km
M = 7.0
#expected = 2.7e-1
expected = 2.3e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 1.5e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=50.0km
M = 7.0
#expected = 6.9e-2
expected = 6.2e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 0.2, M=5.0, R=2.0km
period = 0.2
Rrup = Rjb = 2.0
table2_coeffs = [ -0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
table3_coeffs = [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
M = 5.0
#expected = 4.0e-1
expected = 4.3e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=2.0km
M = 7.0
expected = 1.0e+0
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
#expected = 2.1e-1
expected = 2.2e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=10.0km
M = 7.0
#expected = 6.3e-1
expected = 6.1e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
#expected = 3.2e-2
expected = 3.3e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=50.0km
M = 7.0
expected = 1.4e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 1.0, M=5.0, R=2.0km
period = 1.0
Rrup = Rjb = 2.0
table2_coeffs = [ -6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
table3_coeffs = [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
M = 5.0
#expected = 7.0e-2
expected = 7.1e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=2.0km
M = 7.0
expected = 3.4e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
#expected = 2.6e-2
expected = 2.5e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=10.0km
M = 7.0
expected = 1.8e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
#expected = 4.3e-3
expected = 4.4e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=50.0km
M = 7.0
expected = 5.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 3.0, M=5.0, R=2.0km
period = 3.0
Rrup = Rjb = 2.0
table2_coeffs = [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
table3_coeffs = [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0
M = 5.0
expected = 8.0e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=2.0km
M = 7.0
expected = 1.0e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 3.0e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=10.0km
M = 7.0
#expected = 5.0e-2
expected = 4.9e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 5.0e-4
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=50.0km
M = 7.0
expected = 1.3e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 10.0, M=5.0, R=2.0km
period = 10.0
Rrup = Rjb = 2.0
table2_coeffs = [-13.087, 1.600, -0.070, -0.422, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # 10.0
table3_coeffs = [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # 10.0
M = 5.0
#expected = 6.3e-4
expected = 6.6e-4
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=2.0km
M = 7.0
expected = 2.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 2.2e-4
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=10.0km
M = 7.0
#expected = 1.0e-2
expected = 9.2e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
#expected = 2.8e-5 # estimated
expected = 4.0e-5 # estimated
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=50.0km
M = 7.0
#expected = 2.8e-3
expected = 2.7e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

######################################

Vs30 = 1070.0

print('\n\nCampbell08 model: Ztor=%.1f, Vs30=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Vs30, Frv, Fnm, delta))
print('Tolerance limit=%.2f, tolerance=abs(computed-expected)/'
      'max(computed, expected)'
      % Tolerance)
print('*' * 102)


# period = PGA (0.01), M=5.0, R=2.0km
period = 0.01
Rrup = Rjb = 2.0
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.0
expected = 2.0e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=2.0km
M = 7.0
expected = 4.1e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 9.1e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=10.0km
M = 7.0
expected = 2.2e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 1.3e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=50.0km
M = 7.0
expected = 5.7e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 0.2, M=5.0, R=2.0km
period = 0.2
Rrup = Rjb = 2.0
table2_coeffs = [ -0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
table3_coeffs = [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
M = 5.0
expected = 3.8e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=2.0km
M = 7.0
expected = 8.9e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 2.0e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=10.0km
M = 7.0
expected = 5.4e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 3.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=50.0km
M = 7.0
expected = 1.2e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 1.0, M=5.0, R=2.0km
period = 1.0
Rrup = Rjb = 2.0
table2_coeffs = [ -6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
table3_coeffs = [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
M = 5.0
expected = 5.6e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=2.0km
M = 7.0
expected = 2.7e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 2.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=10.0km
M = 7.0
expected = 1.3e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 3.4e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=50.0km
M = 7.0
expected = 3.9e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 3.0, M=5.0, R=2.0km
period = 3.0
Rrup = Rjb = 2.0
table2_coeffs = [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
table3_coeffs = [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0
M = 5.0
expected = 6.0e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=2.0km
M = 7.0
expected = 7.5e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 2.2e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=10.0km
M = 7.0
expected = 3.5e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 3.8e-4
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=50.0km
M = 7.0
expected = 1.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 10.0, M=5.0, R=2.0km
period = 10.0
Rrup = Rjb = 2.0
table2_coeffs = [-13.087, 1.600, -0.070, -0.422, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # 10.0
table3_coeffs = [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # 10.0
M = 5.0
expected = 4.9e-4
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=2.0km
M = 7.0
expected = 1.4e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 1.8e-4
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=10.0km
M = 7.0
expected = 7.0e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 3.0e-5
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=50.0km
M = 7.0
expected = 2.0e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

######################################

Vs30 = 150.0

print('\n\nCampbell08 model: Ztor=%.1f, Vs30=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Vs30, Frv, Fnm, delta))
print('Tolerance limit=%.2f, tolerance=abs(computed-expected)/'
      'max(computed, expected)'
      % Tolerance)
print('*' * 102)


# period = PGA (0.01), M=5.0, R=2.0km
period = 0.01
Rrup = Rjb = 2.0
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.0
expected = 2.2e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=2.0km
M = 7.0
expected = 3.1e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 1.3e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=10.0km
M = 7.0
expected = 2.2e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 2.5e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=50.0km
M = 7.0
expected = 9.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 0.2, M=5.0, R=2.0km
period = 0.2
Rrup = Rjb = 2.0
table2_coeffs = [ -0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
table3_coeffs = [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
M = 5.0
expected = 3.0e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=2.0km
M = 7.0
expected = 4.0e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 2.4e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=10.0km
M = 7.0
expected = 4.1e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 5.5e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=50.0km
M = 7.0
expected = 2.0e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 1.0, M=5.0, R=2.0km
period = 1.0
Rrup = Rjb = 2.0
table2_coeffs = [ -6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
table3_coeffs = [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
M = 5.0
expected = 1.6e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=2.0km
M = 7.0
expected = 6.0e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 7.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=10.0km
M = 7.0
expected = 3.8e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 1.4e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=50.0km
M = 7.0
expected = 1.4e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 3.0, M=5.0, R=2.0km
period = 3.0
Rrup = Rjb = 2.0
table2_coeffs = [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
table3_coeffs = [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0
M = 5.0
expected = 3.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=2.0km
M = 7.0
expected = 3.8e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 1.1e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=10.0km
M = 7.0
expected = 1.9e-1
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 1.9e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=50.0km
M = 7.0
expected = 5.2e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 10.0, M=5.0, R=2.0km
period = 10.0
Rrup = Rjb = 2.0
table2_coeffs = [-13.087, 1.600, -0.070, -0.422, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # 10.0
table3_coeffs = [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # 10.0
M = 5.0
expected = 2.3e-3
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=2.0km
M = 7.0
expected = 7.1e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 9.0e-4
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=10.0km
M = 7.0
expected = 3.5e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 1.5e-4
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=50.0km
M = 7.0
expected = 1.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

######
# Sigma estimations
# Expected values are from opensha.org
# # These are difficult to organise, due to the way sigma data is shown in the paper.
# # Basically, you have to plug in a Vs30 value, other params, and get a PGA value.
# # Look up the graphs on page 155 and get expected sigma values for that Vs30, period
# # and PGA.  Put that into the code below and *then* check for compliance.
######

print('\n\nCampbell08 model: Ztor=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Frv, Fnm, delta))
print('Tolerance limit=%.2f, tolerance=abs(computed-expected)/'
      'max(computed, expected)'
      % Tolerance)
print('*' * 102)

# period = PGA (0.01), Vs30=760.0, M=5.0, R=2.0km
Vs30 = 760.0
period = 0.01
Rrup = Rjb = 2.0
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.0
expected = 5.2e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (0.20), Vs30=760.0, M=5.0, R=2.0km
Vs30 = 760.0
period = 0.20
Rrup = Rjb = 2.0
table2_coeffs = [ -0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
table3_coeffs = [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
M = 5.0
expected = 5.9e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (1.00), Vs30=760.0, M=5.0, R=2.0km
Vs30 = 760.0
period = 1.00
Rrup = Rjb = 2.0
table2_coeffs = [ -6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
table3_coeffs = [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
M = 5.0
expected = 6.1e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (3.00), Vs30=760.0, M=5.0, R=2.0km
Vs30 = 760.0
period = 3.00
Rrup = Rjb = 2.0
table2_coeffs = [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
table3_coeffs = [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0
M = 5.0
expected = 6.3e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (10.00), Vs30=760.0, M=5.0, R=2.0km
Vs30 = 760.0
period = 10.00
Rrup = Rjb = 2.0
table2_coeffs = [-13.087, 1.600, -0.070, -0.422, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # 10.0
table3_coeffs = [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # 10.0
M = 5.0
expected = 8.1e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('\n\nCampbell08 model: Ztor=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Frv, Fnm, delta))
print('Tolerance limit=%.2f, tolerance=abs(computed-expected)/'
      'max(computed, expected)'
      % Tolerance)
print('*' * 102)

Vs30 = 1070.0

# period = PGA (0.01), Vs30=760.0, M=5.0, R=2.0km
period = 0.01
Rrup = Rjb = 2.0
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.0
expected = 5.2e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (0.20), Vs30=760.0, M=5.0, R=2.0km
period = 0.20
Rrup = Rjb = 2.0
table2_coeffs = [ -0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
table3_coeffs = [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
M = 5.0
expected = 5.9e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (1.00), Vs30=760.0, M=5.0, R=2.0km
period = 1.00
Rrup = Rjb = 2.0
table2_coeffs = [ -6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
table3_coeffs = [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
M = 5.0
expected = 6.1e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (3.00), Vs30=760.0, M=5.0, R=2.0km
period = 3.00
Rrup = Rjb = 2.0
table2_coeffs = [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
table3_coeffs = [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0
M = 5.0
expected = 6.3e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (10.00), Vs30=760.0, M=5.0, R=2.0km
period = 10.00
Rrup = Rjb = 2.0
table2_coeffs = [-13.087, 1.600, -0.070, -0.422, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # 10.0
table3_coeffs = [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # 10.0
M = 5.0
expected = 8.2e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('\n\nCampbell08 model: Ztor=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Frv, Fnm, delta))
print('Tolerance limit=%.2f, tolerance=abs(computed-expected)/'
      'max(computed, expected)'
      % Tolerance)
print('*' * 102)

Vs30 = 150.0

# period = PGA (0.01), Vs30=760.0, M=5.0, R=2.0km
period = 0.01
Rrup = Rjb = 2.0
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.0
expected = 4.1e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=2.0km
M = 7.0
expected = 4.2e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 4.2e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=10.0km
M = 7.0
expected = 4.4e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 4.8e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=50.0km
M = 7.0
expected = 5.1e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (0.20), Vs30=760.0, M=5.0, R=2.0km
period = 0.20
Rrup = Rjb = 2.0
table2_coeffs = [ -0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
table3_coeffs = [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
M = 5.0
expected = 4.3e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=7.0, R=2.0km
M = 7.0
expected = 4.5e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 4.5e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=7.0, R=10.0km
M = 7.0
expected = 5.0e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 5.2e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.20), M=7.0, R=50.0km
M = 7.0
expected = 5.6e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (1.00), Vs30=760.0, M=5.0, R=2.0km
period = 1.00
Rrup = Rjb = 2.0
table2_coeffs = [ -6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
table3_coeffs = [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
M = 5.0
expected = 5.6e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=7.0, R=2.0km
M = 7.0
expected = 5.7e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 5.7e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=7.0, R=10.0km
M = 7.0
expected = 6.0e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 6.0e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (1.00), M=7.0, R=50.0km
M = 7.0
expected = 6.1e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (3.00), Vs30=760.0, M=5.0, R=2.0km
period = 3.00
Rrup = Rjb = 2.0
table2_coeffs = [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
table3_coeffs = [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0
M = 5.0
expected = 6.3e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (3.00), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = PGA (10.00), Vs30=760.0, M=5.0, R=2.0km
period = 10.00
Rrup = Rjb = 2.0
table2_coeffs = [-13.087, 1.600, -0.070, -0.422, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # 10.0
table3_coeffs = [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # 10.0
M = 5.0
expected = 8.2e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (10.00), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('\n\nCampbell08 model: Ztor=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from paper'
      % (Ztor, Frv, Fnm, delta))
print('Tolerance limit=%.2f, tolerance=abs(computed-expected)/'
      'max(computed, expected)'
      % Tolerance)
print('*' * 102)

# period = PGA (0.01), Vs30=1070.0, M=5.0, R=2.0km
# expected sigma is easy for Vs30=1070, constant for each period
Vs30 = 1070.0
period = 0.01
Rrup = Rjb = 2.0
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.0
expected = 0.525
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 0.2, M=5.0, R=2.0km
Vs30 = 1070.0
period = 0.2
Rrup = Rjb = 2.0
table2_coeffs = [ -0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
table3_coeffs = [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
M = 5.0
expected = 0.59
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 1.0, M=5.0, R=2.0km
period = 1.0
Rrup = Rjb = 2.0
table2_coeffs = [ -6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
table3_coeffs = [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
M = 5.0
expected = 0.62
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 3.0, M=5.0, R=2.0km
period = 3.0
Rrup = Rjb = 2.0
table2_coeffs = [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
table3_coeffs = [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0
M = 5.0
expected = 0.65
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 10.0, M=5.0, R=2.0km
period = 10.0
Rrup = Rjb = 2.0
table2_coeffs = [-13.087, 1.600, -0.070, -0.422, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # 10.0
table3_coeffs = [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # 10.0
M = 5.0
expected = 0.825
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

print('-' * 102)

######
# now for different Vs30
######

# period = PGA (0.01), Vs30=150.0, M=5.0, R=2.0km
Vs30 = 150.0
period = 0.01
Rrup = Rjb = 2.0
table2_coeffs = [-1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490, 1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.0
expected = 0.38
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=2.0km
M = 7.0
expected = 0.365
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 0.41
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=10.0km
M = 7.0
expected = 0.385
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 0.49
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = PGA (0.01), M=7.0, R=50.0km
M = 7.0
expected = 0.435
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)

# period = 0.2, Vs30=150.0, M=5.0, R=2.0km
Vs30 = 150.0
period = 0.2
Rrup = Rjb = 2.0
table2_coeffs = [-0.486, 0.500, -0.446, -0.398, -2.220, 0.170, 7.60, 0.280, -0.012, 0.490,  2.194, 0.040, 0.610,  748, -2.188, 1.856] # 0.20
table3_coeffs = [0.534, 0.249, 0.186, 0.589, 0.618, 0.871] # 0.20
M = 5.0
expected = 0.39
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=2.0km
M = 7.0
expected = 0.385
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 0.395
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=10.0km
M = 7.0
expected = 0.38
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 0.495
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 0.2, M=7.0, R=50.0km
M = 7.0
expected = 0.41
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)


# period = 1.0, Vs30=150.0, M=5.0, R=2.0km
Vs30 = 150.0
period = 1.0
Rrup = Rjb = 2.0
table2_coeffs = [-6.406, 1.196, -0.772, -0.314, -2.000, 0.170, 4.00, 0.255,  0.000, 0.490,  1.571, 0.150, 1.000,  400, -1.955, 1.929] # 1.0
table3_coeffs = [0.568, 0.255, 0.225, 0.623, 0.662, 0.534] # 1.0
M = 5.0
expected = 0.58
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=2.0km
M = 7.0
expected = 0.56
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
expected = 0.60
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=10.0km
M = 7.0
expected = 0.60
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
expected = 0.615
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 1.0, M=7.0, R=50.0km
M = 7.0
expected = 0.58
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)


# period = 3.0, Vs30=150.0, M=5.0, R=2.0km
Vs30 = 150.0
period = 3.0
Rrup = Rjb = 2.0
table2_coeffs = [-10.556, 1.600, -0.638, -0.491, -2.000, 0.170, 4.00, 0.000,  0.000, 0.154, -0.820, 0.300, 1.000,  400,  0.000, 2.110] # 3.0
table3_coeffs = [0.558, 0.326, 0.229, 0.646, 0.686, 0.289] # 3.0
M = 5.0
expected = 0.645
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 3.0, M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('-' * 102)


# period = 10.0, Vs30=150.0, M=5.0, R=2.0km
Vs30 = 150.0
period = 10.0
Rrup = Rjb = 2.0
table2_coeffs = [-13.087, 1.600, -0.070, -0.422, -2.000, 0.170, 4.00, 0.000,  0.000, 0.000, -0.820, 0.300, 1.000,  400,  0.000, 2.744] # 10.0
table3_coeffs = [0.667, 0.485, 0.290, 0.825, 0.874, 0.174] # 10.0
M = 5.0
expected = 0.825
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=2.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=10.0km
Rrup = Rjb = 10.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=10.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=5.0, R=50.0km
Rrup = Rjb = 50.0
M = 5.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

# period = 10.0, M=7.0, R=50.0km
M = 7.0
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)


print('~' * 102)

Vs30 = 760.0

Ztor = 1.5
delta = 45.0

print('Campbell08 model: Ztor=%.1f, Vs30=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Vs30, Frv, Fnm, delta))

# period = 0.01, M=5.7, R=50.0km
period = 0.01
Z25 = 0.3
Rrup = 50.0
Rjb = 47.5
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.7
expected = 4.0e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

Ztor = 25.0
delta = 45.0

print('Campbell08 model: Ztor=%.1f, Vs30=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Vs30, Frv, Fnm, delta))

# period = 0.01, M=6.2, R=50.0km
period = 0.01
Z25 = 3.5
Rrup = 50.0
Rjb = 31.3
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 6.2
expected = 6.1e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

Ztor = 0.0
delta = 90.0

print('Campbell08 model: Ztor=%.1f, Vs30=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Vs30, Frv, Fnm, delta))

# period = 0.01, M=6.2, R=50.0km
period = 0.01
Z25 = 2.0
Rrup = 50.0
Rjb = 50.0
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.7
expected = 3.2e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

Ztor = 0.0
delta = 90.0

print('Campbell08 model: Ztor=%.1f, Vs30=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Vs30, Frv, Fnm, delta))

# period = 0.01, M=6.2, R=50.0km
period = 0.01
Z25 = 2.0
Rrup = 50.0
Rjb = 50.0
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.7
expected = 3.2e-2
estimate(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

print('~' * 102)

Vs30 = 760.0

Ztor = 1.5
delta = 45.0

print('Campbell08 model: Ztor=%.1f, Vs30=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Vs30, Frv, Fnm, delta))

# period = 0.01, M=5.7, R=50.0km
period = 0.01
Z25 = 0.3
Rrup = 50.0
Rjb = 47.5
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 5.7
expected = 5.2e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

Ztor = 25.0
delta = 45.0

print('Campbell08 model: Ztor=%.1f, Vs30=%.1f, Frv=%d, Fnm=%d, delta=%d - '
      'expected values from opensha.org'
      % (Ztor, Vs30, Frv, Fnm, delta))

# period = 0.01, M=6.2, R=50.0km
period = 0.01
Z25 = 3.5
Rrup = 50.0
Rjb = 31.3
table2_coeffs = [ -1.715, 0.500, -0.530, -0.262, -2.118, 0.170, 5.60, 0.280, -0.120, 0.490,  1.058, 0.040, 0.610,  865, -1.186, 1.839]  # PGA
table3_coeffs = [0.478, 0.219, 0.166, 0.526, 0.551, 1.000] # PGA
M = 6.2
expected = 5.2e-1
estimate_sigma(period, M, Rrup, Rjb, Ztor, Vs30, delta, table2_coeffs, table3_coeffs, expected)

print('-' * 102)


