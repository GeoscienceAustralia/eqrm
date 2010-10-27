#!/usr/bin/env python

"""An implementation of Abrahamson08.

Follows Hadi's Matlab code.
Tries to output in the same format as the As08*.out files
in the Campbell_NGA_tests.
"""

import copy
import math

import numpy


######
# The Abrahamson08 equation(s)
# Taken from AS_2008_nga.m
######

def AS_2008_nga(M, Vs30, T, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, FVs30):

    Td = 10.0**(-1.25 + 0.3*M)
    SaTd = AS_2008_nga_sub(M, 1100, Td, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, FVs30, 0.0, 0.0)
    return AS_2008_nga_sub(M, Vs30, T, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, FVs30, Td, SaTd)
 
 
def AS_2008_nga_sub(M, Vs30, T, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, FVs30, Td, SaTd):
    """Modified a bit since T will always be a scalar and nver == 1000."""

    # for the given period T, get the index for the constants
    period = [0.0, -1.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2,
              0.25, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.5, 10.0];

    Td = 10**(-1.25 + 0.3*M)

    pga_rock = math.exp(calc_val(M, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, 0, 1100, get_abrahamson_silva_constants(0, 1100, FVs30)))
    (tsigma, sigma, tau, pga_sigmaB, pga_tauB) = abrahamson_silva_sigma(M, pga_rock, Vs30,0, 0, get_abrahamson_silva_constants(0, Vs30, FVs30))

#    nT = len(T)
    iflg = 0
# commented out since T will never be 1000
#    if nT == 1:
    if T == 1000:
        raise Exception('T is 1000??')
#            iflg = 1
#            nperi = len(period)
#            Sa = zeros(1, nperi-2)
#            tsigma = zeros(1, nperi-2)
#            period1 = period(3:end)
#    
#            for index=3:1:nperi:
#                # get constants for the given index value
#                V = get_abrahamson_silva_constants(index, Vs30, FVs30)
#                if period[index] <= Td or SaTd == 0 or Vs30 < 1100.0:
#                    Sa[index-2] = math.exp(calc_val(M, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, pga_rock, Vs30, V))
#                else:
#                    Sa[index-2] = math.exp(calc_val2(SaTd, Td, period[index], Z10, pga_rock, Vs30, V))
#                (tsigma[index-2], sigma, tau, sigmaB, tauB) = abrahamson_silva_sigma(M, pga_rock, Vs30, pga_sigmaB, pga_tauB, V)

# The following is heavily modifed as the python will not handle a T array, just a scalar 
    if iflg == 0:
        Sa = 0.0
        tsigma = 0.0
        period1 = T
        # interpolate between periods if neccesary
        if T not in period:
            T_low = 0
            for t in period:
                if t > T:
                    break
                T_low = t

            T_hi = len(period) - 1
            for t in period:
                if t > T:
                    T_hi = t
                    break

            (sa_low, sigma_low, _) = AS_2008_nga_sub(M, Vs30, T_low, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, FVs30, Td, SaTd)
            (sa_hi, sigma_hi, _) = AS_2008_nga_sub(M, Vs30, T_hi, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, FVs30, Td, SaTd)

            # interpolate values for Sa and tsigma
            x = [math.log(T_low), math.log(T_hi)]
            Y_sa = [math.log(sa_low), math.log(sa_hi)]
            Y_sigma = [sigma_low, sigma_hi]
            Sa = math.exp(numpy.interp(math.log(T), x, Y_sa))
            tsigma = numpy.interp(math.log(T), x, Y_sigma)
        else:
            index = period.index(T)

            # get constants for the given index value
            V = get_abrahamson_silva_constants(index, Vs30, FVs30);
            if (period[index] <= Td) or (SaTd == 0) or (Vs30 < 1100.0):
                Sa = math.exp(calc_val(M, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, pga_rock, Vs30, V))
            else:
                Sa = math.exp(calc_val2(SaTd, Td, period[index], Z10, pga_rock, Vs30, V))

            (tsigma, sigma, tau, sigmaB, tauB) = abrahamson_silva_sigma(M, pga_rock, Vs30, pga_sigmaB, pga_tauB, V)

    return (Sa, tsigma, period1)

def f_1(M, R, V):
    if M <= V.c1:
        f1 = V.a1 + V.a4 * (M - V.c1) + V.a8 * (8.5 - M)**2 + (V.a2 + V.a3 * (M - V.c1)) * math.log(R);
    else:
        f1 = V.a1 + V.a5 * (M - V.c1) + V.a8 * (8.5 - M)**2 + (V.a2 + V.a3 * (M - V.c1)) * math.log(R);
    return f1

def f_4(Rjb, Rx, dip, Ztor, M, W, V, FHW):
    if FHW == 1:
        if Rjb < 30.0:
            T1 = 1-Rjb/30.0
        else:
            T1 =0.0
        W1 = W*cos(dip*Deg2Rad)
        if Rx <= W1:
            T2 = 0.5+Rx/(2*W1)
        elif Rx > W1 or dip == 90.0:
            T2 = 1.0
        if Rx >= Ztor:
            T3  =1.0
        else:
            T3 = Rx/Ztor
        if M <= 6.0:
            T4 = 0.0
        elif M < 7.0:
            T4 = M-6
        else:
            T4 =1.0
        if dip >= 30:
            T5 = 1-(dip-30.0)/60.0
        else:
            T5 =1.0
 
        f4 = V.a14*T1*T2*T3*T4*T5
    else:
        f4 = 1.0

    return f4

def f_5(pga_rock, Vs30, V):
    if Vs30 < V.lin:
        f5 = V.a10 * math.log(V.Vs30s/V.lin) - V.b*math.log(pga_rock+V.c) + V.b*math.log(pga_rock+V.c*((V.Vs30s/V.lin)**V.n))
    else:
        f5 = (V.a10 + V.b*V.n) * math.log(V.Vs30s/V.lin)
    return f5

def f_6(Ztor, V):
    if Ztor < 10.0:
        f6 = V.a16*Ztor/10.0
    else:
        f6 = V.a16
    return f6

def f_8(Rrup, M, V):
    if M < 5.5:
        T6 = 1.0
    elif M <= 6.5:
        T6 = 0.5*(6.5-M)+0.5
    else:
        T6 = 0.5
    if Rrup < 100.0:
        f8 = 0.0
    else:
        f8 = V.a18*(Rrup-100.0)*T6
    return f8

def f_10(Z10, Vs30, V):
    if Vs30 < 180.0:
        Z10h = math.exp(6.745)
    elif Vs30 <= 500.0:
        Z10h = math.exp(6.745-1.35*math.log(Vs30/180))
    else:
        Z10h = math.exp(5.394-4.48*math.log(Vs30/500.0))
    a211 = (V.a10+V.b*V.n)*math.log(V.Vs30s/min(V.v1,1000.0))
    a212 = math.log((Z10+V.c2)/(Z10h+V.c2))
    if Vs30 >= 1000.0:
        a21 = 0.0
    elif a211+V.e2*a212 < 0:
        a21 = -a211/a212
    else:
        a21 = V.e2
    
    f10 = a21*a212
    if Z10 >= 200.0:
        f10 = f10+V.a22*math.log(Z10/200.0)
    return f10

def calc_val(M, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, pga_rock, Vs30, constants):
    R = math.sqrt(Rrup**2 + constants.c4**2)

    X = f_1(M, R, constants) +  constants.a12*FRV + constants.a13*FNM + constants.a15*FAS \
        + f_5(pga_rock, Vs30, constants) + FHW*f_4(Rjb, Rx, dip, Ztor, M, W, constants,FHW) + f_6(Ztor, constants) \
        + f_8(Rrup, M, constants) + f_10(Z10, Vs30, constants)
    return X

def calc_val2(SaTd, Td, T, Z10, pga_rock, Vs30, constants):
    X = math.log(SaTd * Td**2 / T**2) - f_5(pga_rock, 1100.0, constants) - f_10(Z10, 1100.0, constants) + f_5(pga_rock, Vs30, constants) + f_10(Z10, Vs30, constants)
    return X

class DataObj(object):
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            msg = 'DataObj() must be called with keyword args ONLY!'
            raise RuntimeError(msg)

        self.__dict__ = kwargs

def get_abrahamson_silva_constants(index,Vs30,FVs30):
    # arrays with values by index
    period = [      0,      -1,    0.01,    0.02,    0.03,    0.04,    0.05,   0.075,     0.1,    0.15,     0.2,    0.25,     0.3,     0.4,     0.5,    0.75,       1,     1.5,       2,       3,       4,       5,     7.5,      10]
    lin    = [  865.1,   400.0,   865.1,   865.1,   907.8,   994.5,  1053.5,  1085.7,  1032.5,   877.6,   748.2,   654.3,   587.1,   503.0,   456.6,   410.5,   400.0,   400.0,   400.0,   400.0,   400.0,   400.0,   400.0,   400.0]
    b      = [ -1.186,  -1.955,  -1.186,  -1.219,  -1.273,  -1.308,  -1.346,  -1.471,  -1.624,  -1.931,  -2.188,  -2.381,  -2.518,  -2.657,  -2.669,  -2.401,  -1.955,  -1.025,  -0.299,     0.0,     0.0,     0.0,     0.0,     0.0]
    a1     = [  0.804,  5.7578,   0.811,   0.855,   0.962,   1.037,   1.133,   1.375,   1.563,   1.716,   1.687,   1.646,   1.601,   1.511,   1.397,   1.137,   0.915,   0.510,   0.192,  -0.280,  -0.639,  -0.936,  -1.527,  -1.993]
    a2     = [-0.9679, -0.9046, -0.9679, -0.9774, -1.0024, -1.0289, -1.0508, -1.0810, -1.0833, -1.0357, -0.9700, -0.9202, -0.8974, -0.8677, -0.8475, -0.8206, -0.8088, -0.7995, -0.7960, -0.7960, -0.7960, -0.7960, -0.7960, -0.7960]
    a8     = [-0.0372,   -0.12, -0.0372, -0.0372, -0.0372, -0.0315, -0.0271, -0.0191, -0.0166, -0.0254, -0.0396, -0.0539, -0.0656, -0.0807, -0.0924, -0.1137, -0.1289, -0.1534, -0.1708, -0.1954, -0.2128, -0.2263, -0.2509, -0.2683]
    a10    = [ 0.9445,  1.5390,  0.9445,  0.9834,  1.0471,  1.0884,  1.1333,  1.2808,  1.4613,  1.8071,  2.0773,  2.2794,  2.4201,  2.5510,  2.5395,  2.1493,  1.5705,  0.3991, -0.6072, -0.9600, -0.9600, -0.9208, -0.7700, -0.6630]
    a12    = [ 0.0000,  0.0800,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0181,  0.0309,  0.0409,  0.0491,  0.0619,  0.0719,  0.0800,  0.0800,  0.0800,  0.0800,  0.0800,  0.0800,  0.0800,  0.0800,  0.0800]
    a13    = [-0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600, -0.0600]
    
    a14    = [ 1.0800,  0.7000,  1.0800,  1.0800,  1.1331,  1.1708,  1.2000,  1.2000,  1.2000,  1.1683,  1.1274,  1.0956,  1.0697,  1.0288,  0.9971,  0.9395,  0.8985,  0.8409,  0.8000,  0.4793,  0.2518,  0.0754,  0.0000,  0.0000]
    a15    = [-0.3500, -0.3900, -0.3500, -0.3500, -0.3500, -0.3500, -0.3500, -0.3500, -0.3500, -0.3500, -0.3500, -0.3500, -0.3500, -0.3500, -0.3191, -0.2629, -0.2230, -0.1668, -0.1270, -0.0708, -0.0309,  0.0000,  0.0000,  0.0000]
    a16    = [ 0.9000,  0.6300,  0.9000,  0.9000,  0.9000,  0.9000,  0.9000,  0.9000,  0.9000,  0.9000,  0.9000,  0.9000,  0.9000,  0.8423,  0.7458,  0.5704,  0.4460,  0.2707,  0.1463, -0.0291, -0.1535, -0.2500, -0.2500, -0.2500]
    a18    = [-0.0067,  0.0000, -0.0067, -0.0067, -0.0067, -0.0067, -0.0076, -0.0093, -0.0093, -0.0093, -0.0083, -0.0069, -0.0057, -0.0039, -0.0025,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000]
    
    
    s1e    = [  0.590,   0.590,   0.590,   0.590,   0.605,   0.615,   0.623,   0.630,   0.630,   0.630,   0.630,   0.630,   0.630,   0.630,   0.630,   0.630,   0.630,   0.615,   0.604,   0.589,   0.578,   0.570,   0.611,   0.640]
    s2e    = [  0.470,   0.470,   0.470,   0.470,   0.478,   0.483,   0.488,   0.495,   0.501,   0.509,   0.514,   0.518,   0.522,   0.527,   0.532,   0.539,   0.545,   0.552,   0.558,   0.565,   0.570,   0.587,   0.618,   0.640]
    s1m    = [  0.576,   0.576,   0.576,   0.576,   0.591,   0.602,   0.610,   0.617,   0.617,   0.616,   0.614,   0.612,   0.611,   0.608,   0.606,   0.602,   0.594,   0.566,   0.544,   0.527,   0.515,   0.510,   0.572,   0.612]
    s2m    = [  0.453,   0.453,   0.453,   0.453,   0.461,   0.466,   0.471,   0.479,   0.485,   0.491,   0.495,   0.497,   0.499,   0.501,   0.504,   0.506,   0.503,   0.497,   0.491,   0.500,   0.505,   0.529,   0.579,   0.612]
    s3     = [  0.470,   0.420,   0.420,   0.420,   0.462,   0.492,   0.515,   0.550,   0.550,   0.550,   0.520,   0.497,   0.479,   0.449,   0.426,   0.385,   0.350,   0.350,   0.350,   0.350,   0.350,   0.350,   0.350,   0.350]
    s4     = [  0.300,   0.300,   0.300,   0.300,   0.305,   0.309,   0.312,   0.317,   0.321,   0.326,   0.329,   0.332,   0.335,   0.338,   0.341,   0.346,   0.350,   0.350,   0.350,   0.350,   0.350,   0.350,   0.350,   0.350]
    ro     = [  1.000,   0.740,   1.000,   1.000,   0.991,   0.982,   0.973,   0.952,   0.929,   0.896,   0.874,   0.856,   0.841,   0.818,   0.783,   0.680,   0.607,   0.504,   0.431,   0.328,   0.255,   0.200,   0.200,   0.200]
    
    c1=6.75
    c4=4.5
    a3=0.265
    a4=-0.231
    a5=-0.398
    n=1.18
    c=1.88
    c2=50.0
    
    if FVs30 == 1:
        s1 = s1e[index]
        s2 = s2e[index]
    else:
        s1 = s1m[index]
        s2 = s2m[index]

    T = period[index]
    
    if index == 2:
        v1 = 862.0;
    elif T <= 0.5:
        v1 = 1500.0
    elif T <= 1.0:
        v1 = math.exp(8.0-0.795*math.log(T/0.21))
    elif T < 2.0:
        v1 = math.exp(6.76-0.297*math.log(T))
    else:
        v1 = 700.0

    if (T < 0.35) or (Vs30 > 1000.0):
        e2 = 0.0
    elif T <= 2.0:
        e2 = -0.25*math.log(Vs30/1000)*math.log(T/0.35)
    else:
        e2 = -0.25*math.log(Vs30/1000)*math.log(2/0.35)

    if T < 2.0:
        a22 = 0.0
    else:
        a22 = 0.0625*(T-2.0)
    
    Vs30s = min(Vs30, v1)

    constants = DataObj(period=period[index], lin=lin[index], a1=a1[index],
                        a2=a2[index], a3=a3, a4=a4, a5=a5, a8=a8[index],
                        a10=a10[index], a12=a12[index], a13=a13[index],
                        a14=a14[index], a15=a15[index], a16=a16[index],
                        a18=a18[index], b=b[index], c=c, c1=c1, c2=c2, c4=c4,
                        n=n, s1=s1, s2=s2, s3=s3[index], s4=s4[index],
                        ro=ro[index], v1=v1, e2=e2, a22=a22, Vs30s=Vs30s)
    
    return constants

def abrahamson_silva_sigma(M, pga_rock, Vs30, pga_sigmaB, pga_tauB, V):
    # use the published coefficients for the geometric mean
    if M < 5.0:
        sigma0 = V.s1
    elif M <= 7.0:
        sigma0 = V.s1 + (V.s2-V.s1)/2 * (M-5.0)
    else:
        sigma0 = V.s2

    sigmaAMP = 0.3
    sigmaB = math.sqrt(sigma0**2-sigmaAMP**2)

    if M < 5.0:
        tau0 = V.s3
    elif M <= 7.0:
        tau0 = V.s3 + (V.s4-V.s3)/2.0 * (M-5.0)
    else:
        tau0 = V.s4

    tauB = tau0
    
    if Vs30 >= V.lin:
        term1 = 0.0
    else:
        # from openSHA
        term1 = V.b * pga_rock * ((-1/(pga_rock+V.c)) + (1/(pga_rock + V.c*((Vs30/V.lin)**V.n))))

    # from openSHA
    sigma = math.sqrt(sigma0**2 + term1**2 * pga_sigmaB**2 + 2*term1 * sigmaB*pga_sigmaB*V.ro)
    tau = math.sqrt(tau0**2 + term1**2 * pga_tauB**2 + 2*term1 * tauB  *pga_tauB  *V.ro)
    
    tsigma = math.sqrt(sigma**2 + tau**2)

    return (tsigma, sigma, tau, sigmaB, tauB)

######
# Start generating results
######

M = 4.0
Vs30 = 150.0
Rrup = 0.0
Rjb = 0.0
Rx = -1.0
dip = 30.0
Ztor = 0.0
Z10 = 0.0
W = 0.9
FRV = 0
FNM = 0
FAS = 0
FHW = 0
FVs30 = 1

for T in [0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 3.000E-01, 4.000E-01, 5.000E-01, 7.500E-01, 1.000E+00, 1.500E+00, 2.000E+00, 3.000E+00, 4.000E+00, 5.000E+00, 7.500E+00, 1.000E+01]:
    (Sa, tsigma, period1) = AS_2008_nga(M, Vs30, T, Rrup, Rjb, Rx, dip, Ztor, Z10, W, FRV, FNM, FAS, FHW, FVs30)
    print('M=%.1f, Vs30=%6.1f, period=%6.3f, Rrup=%5.1f, Rjb=%5.1f, Rx=%5.1f, Sa=%f, tsigma=%f' % (M, Vs30, T, Rrup, Rjb, Rx, Sa, tsigma))
    print('*'*80)

# Mw        Rrup      Rjb       Rx         Dip       W         Ztor      Vs30      Zsed     
# 4.000E+00 0.000E+00 0.000E+00 -1.000E+00 3.000E+01 9.000E-01 0.000E+00 1.500E+02 0.000E+00


# 1.000E-02 2.000E-02 3.000E-02 4.000E-02 5.000E-02 7.500E-02 1.000E-01 1.500E-01 2.000E-01 2.500E-01 3.000E-01 4.000E-01 5.000E-01 7.500E-01 1.000E+00 1.500E+00 2.000E+00 3.000E+00 4.000E+00 5.000E+00 7.500E+00 1.000E+01 PGA       PGV
# 2.182E-01 2.219E-01 2.317E-01 2.619E-01 2.961E-01 3.957E-01 4.726E-01 4.742E-01 3.895E-01 3.091E-01 2.471E-01 1.513E-01 8.401E-02 2.826E-02 1.390E-02 7.035E-03 4.380E-03 2.030E-03 1.142E-03 7.307E-04 3.247E-04 1.827E-04 2.167E-01 1.903E+00

# Mw        Rrup      Rjb       Rx         Dip       W         Ztor      Vs30      Zsed     
# 8.500E+00 2.000E+02 2.000E+02 -2.000E+02 9.000E+01 1.000E+01 5.000E+00 2.550E+02 7.000E+02

# 1.000E-02 2.000E-02 3.000E-02 4.000E-02 5.000E-02 7.500E-02 1.000E-01 1.500E-01 2.000E-01 2.500E-01 3.000E-01 4.000E-01 5.000E-01 7.500E-01 1.000E+00 1.500E+00 2.000E+00 3.000E+00 4.000E+00 5.000E+00 7.500E+00 1.000E+01 PGA       PGV
# 1.315E-01 1.302E-01 1.275E-01 1.211E-01 1.140E-01 1.119E-01 1.294E-01 1.863E-01 2.658E-01 3.502E-01 3.945E-01 4.416E-01 4.489E-01 4.302E-01 3.616E-01 2.550E-01 1.987E-01 1.238E-01 8.787E-02 6.611E-02 4.160E-02 3.026E-02 1.306E-01 3.070E+01

