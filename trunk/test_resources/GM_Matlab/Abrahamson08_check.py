#!/usr/bin/env python

"""An implementation of Abrahamson08.

Modified form of the FORTRAN code for AS08 from the www.daveboore.com site.
"""

import sys
import copy
import math

import numpy


# coefficient tables from the FORTRAN, put through a python converter
PGA_index = 22		# index of tables for period==0.0

T = [0.010,0.020,0.030,0.040,0.050,0.075,0.10,0.15,0.20,0.25,
     0.30,0.40,0.50,0.75,1.00,1.50,2.00,3.00,4.00,5.00,
     7.50,10.0,0.0,-1.0]

nper = len(T)

c1 = [6.75,6.75,6.75,6.75,6.75,6.75,6.75,6.75,6.75,6.75,
      6.75,6.75,6.75,6.75,6.75,6.75,6.75,6.75,6.75,6.75,
      6.75,6.75,6.75,6.75]

c4 = [4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5,
      4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5,
      4.5,4.5,4.5,4.5]

a3 = [0.265,0.265,0.265,0.265,0.265,0.265,0.265,0.265,0.265,0.265,
      0.265,0.265,0.265,0.265,0.265,0.265,0.265,0.265,0.265,0.265,
      0.265,0.265,0.265,0.265]

a4 = [-0.231,-0.231,-0.231,-0.231,-0.231,-0.231,-0.231,-0.231,-0.231,-0.231,
      -0.231,-0.231,-0.231,-0.231,-0.231,-0.231,-0.231,-0.231,-0.231,-0.231,
      -0.231,-0.231,-0.231,-0.231]

a5 = [-0.398,-0.398,-0.398,-0.398,-0.398,-0.398,-0.398,-0.398,-0.398,-0.398,
      -0.398,-0.398,-0.398,-0.398,-0.398,-0.398,-0.398,-0.398,-0.398,-0.398,
      -0.398,-0.398,-0.398,-0.398]

n = [1.18,1.18,1.18,1.18,1.18,1.18,1.18,1.18,1.18,1.18,
     1.18,1.18,1.18,1.18,1.18,1.18,1.18,1.18,1.18,1.18,
     1.18,1.18,1.18,1.18]

c = [1.88,1.88,1.88,1.88,1.88,1.88,1.88,1.88,1.88,1.88,
     1.88,1.88,1.88,1.88,1.88,1.88,1.88,1.88,1.88,1.88,
     1.88,1.88,1.88,1.88]

c2 = [50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,
      50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,
      50.0,50.0,50.0,50.0]

Vlin = [865.1,865.1,907.8,994.5,1053.5,1085.7,1032.5,877.6,748.2,654.3,
        587.1,503.0,456.6,410.5,400.0,400.0,400.0,400.0,400.0,400.0,
        400.0,400.0,865.1,400.0]

b = [-1.186,-1.219,-1.273,-1.308,-1.346,-1.471,-1.624,-1.931,-2.188,-2.381,
     -2.518,-2.657,-2.669,-2.401,-1.955,-1.025,-0.299,0.000,0.000,0.000,
     0.000,0.000,-1.186,-1.955]

a1 = [0.8110,0.8550,0.9620,1.0370,1.1330,1.3750,1.5630,1.7160,1.6870,1.6460,
      1.6010,1.5110,1.3970,1.1370,0.9150,0.5100,0.1920,-0.2800,-0.6390,-0.9360,
      -1.5270,-1.9930,0.8040,5.7578]

a2 = [-0.9679,-0.9774,-1.0024,-1.0289,-1.0508,-1.0810,-1.0833,-1.0357,-0.9700,-0.9202,
      -0.8974,-0.8677,-0.8475,-0.8206,-0.8088,-0.7995,-0.7960,-0.7960,-0.7960,-0.7960,
      -0.7960,-0.7960,-0.9679,-0.9046]

a8 = [-0.0372,-0.0372,-0.0372,-0.0315,-0.0271,-0.0191,-0.0166,-0.0254,-0.0396,-0.0539,
      -0.0656,-0.0807,-0.0924,-0.1137,-0.1289,-0.1534,-0.1708,-0.1954,-0.2128,-0.2263,
      -0.2509,-0.2683,-0.0372,-0.1200]

a10 = [0.9445,0.9834,1.0471,1.0884,1.1333,1.2808,1.4613,1.8071,2.0773,2.2794,
       2.4201,2.5510,2.5395,2.1493,1.5705,0.3991,-0.6072,-0.9600,-0.9600,-0.9208,
       -0.7700,-0.6630,0.9445,1.5390]

a12 = [0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0181,0.0309,0.0409,
       0.0491,0.0619,0.0719,0.0800,0.0800,0.0800,0.0800,0.0800,0.0800,0.0800,
       0.0800,0.0800,0.0000,0.0800]

a13 = [-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,
       -0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,-0.0600,
       -0.0600,-0.0600,-0.0600,-0.0600]

a14 = [1.0800,1.0800,1.1331,1.1708,1.2000,1.2000,1.2000,1.1683,1.1274,1.0956,1.0697,
       1.0288,0.9971,0.9395,0.8985,0.8409,0.8000,0.4793,0.2518,0.0754,0.0000,
       0.0000,1.0800,0.7000]

a15 = [-0.3500,-0.3500,-0.3500,-0.3500,-0.3500,-0.3500,-0.3500,-0.3500,-0.3500,-0.3500,
       -0.3500,-0.3500,-0.3191,-0.2629,-0.2230,-0.1668,-0.1270,-0.0708,-0.0309,0.0000,
       0.0000,0.0000,-0.3500,-0.3900]

a16 = [0.9000,0.9000,0.9000,0.9000,0.9000,0.9000,0.9000,0.9000,0.9000,0.9000,
       0.9000,0.8423,0.7458,0.5704,0.4460,0.2707,0.1463,-0.0291,-0.1535,-0.2500,
       -0.2500,-0.2500,0.9000,0.6300]

a18 = [-0.0067,-0.0067,-0.0067,-0.0067,-0.0076,-0.0093,-0.0093,-0.0093,-0.0083,-0.0069,
       -0.0057,-0.0039,-0.0025,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,
       0.0000,0.0000,-0.0067,0.0000]

s1est = [0.590,0.590,0.605,0.615,0.623,0.630,0.630,0.630,0.630,0.630,
         0.630,0.630,0.630,0.630,0.630,0.615,0.604,0.589,0.578,0.570,
         0.611,0.640,0.590,0.590]

s2est = [0.470,0.470,0.478,0.483,0.488,0.495,0.501,0.509,0.514,0.518,
         0.522,0.527,0.532,0.539,0.545,0.552,0.558,0.565,0.570,0.587,
         0.618,0.640,0.470,0.470]

s1mea = [0.576,0.576,0.591,0.602,0.610,0.617,0.617,0.616,0.614,0.612,
         0.611,0.608,0.606,0.602,0.594,0.566,0.544,0.527,0.515,0.510,
         0.572,0.612,0.576,0.576]

s2mea = [0.453,0.453,0.461,0.466,0.471,0.479,0.485,0.491,0.495,0.497,
         0.499,0.501,0.504,0.506,0.503,0.497,0.491,0.500,0.505,0.529,
         0.579,0.612,0.453,0.453]

s3 = [0.420,0.420,0.462,0.492,0.515,0.550,0.550,0.550,0.520,0.497,
      0.479,0.449,0.426,0.385,0.350,0.350,0.350,0.350,0.350,0.350,
      0.350,0.350,0.470,0.420]

s4 = [0.300,0.300,0.305,0.309,0.312,0.317,0.321,0.326,0.329,0.332,
      0.335,0.338,0.341,0.346,0.350,0.350,0.350,0.350,0.350,0.350,
      0.350,0.350,0.300,0.300]

rho = [1.000,1.000,0.991,0.982,0.973,0.952,0.929,0.896,0.874,0.856,
       0.841,0.818,0.783,0.680,0.607,0.504,0.431,0.328,0.255,0.200,
       0.200,0.200,1.000,0.740]

######
# The Abrahamson08 equation(s)
# Taken from nga_gm_tmr_subs.for
######

##       entry AS08_MODEL (Mw,Rrup,Rjb,Rx,Frv,Fnm,Fhw,Fas,Ztor,Dip,W,
##      :           Vs30,Z10,Per,Y,Sigest,Sigmea,Tau,SigTest,SigTmea)
## 
## C.....
## C.....DETERMINE WHICH STRONG MOTION PARAMETER TO EVALUATE
## C.....
## 
##       DO i = 1, nper
##         IF (Per .EQ. T(i)) THEN
##           iper = i
##           GOTO 1020
##         ENDIF
##       ENDDO
## 
##       print *,' '
##       print *, 'In AS08--ERROR: Period ',Per,
##      :         ' is not supported; quitting'
##       print *,' '
##       stop
## 
## 
##  1020 c1T    = c1(iper)
##       c4T    = c4(iper)
##       a3T    = a3(iper)
##       a4T    = a4(iper)
##       a5T    = a5(iper)
##       nT     = n(iper)
##       cT     = c(iper)
##       c2T    = c2(iper)
##       VlinT  = Vlin(iper)
##       bT     = b(iper)
##       a1T    = a1(iper)
##       a2T    = a2(iper)
##       a8T    = a8(iper)
##       a10T   = a10(iper)
##       a12T   = a12(iper)
##       a13T   = a13(iper)
##       a14T   = a14(iper)
##       a15T   = a15(iper)
##       a16T   = a16(iper)
##       a18T   = a18(iper)
##       s1estT = s1est(iper)
##       s2estT = s2est(iper)
##       s1meaT = s1mea(iper)
##       s2meaT = s2mea(iper)
##       s3T    = s3(iper)
##       s4T    = s4(iper)
##       rhoT   = rho(iper)

def AS08_MODEL(Mw, Rrup, Rjb, Rx, Frv, Fnm, Fhw, Fas, Ztor, Dip, W, Vs30, Z10, Per):
    # DETERMINE WHICH STRONG MOTION PARAMETER TO EVALUATE
    try:
        iper = T.index(Per)
    except ValueError:
        print('In AS08--ERROR: Period %.2f is not supported; quitting' % Per)

    c1T = c1[iper]
    c4T = c4[iper]
    a3T = a3[iper]
    a4T = a4[iper]
    a5T = a5[iper]
    nT = n[iper]
    cT = c[iper]
    c2T = c2[iper]
    VlinT = Vlin[iper]
    bT = b[iper]
    a1T = a1[iper]
    a2T = a2[iper]
    a8T = a8[iper]
    a10T = a10[iper]
    a12T = a12[iper]
    a13T = a13[iper]
    a14T = a14[iper]
    a15T = a15[iper]
    a16T = a16[iper]
    a18T = a18[iper]
    s1estT = s1est[iper]
    s2estT = s2est[iper]
    s1meaT = s1mea[iper]
    s2meaT = s2mea[iper]
    s3T = s3[iper]
    s4T = s4[iper]
    rhoT = rho[iper]

## C.....
## C.....CALCULATE ROCK PGA (Per = 0, Vs30 = 1100 m/sec)
## C.....
## C.....Magnitude and Distance Terms
## C.....
## 
##       R = SQRT(Rrup**2 + c4(23)**2)
## 
##       IF (Mw .LE. c1(23)) THEN
##         f_1 = a1(23) + a4(23)*(Mw-c1(23)) + a8(23)*(8.5-Mw)**2
##      *    + (a2(23) + a3(23)*(Mw-c1(23)))*ALOG(R)
##       ELSE
##         f_1 = a1(23) + a5(23)*(Mw-c1(23)) + a8(23)*(8.5-Mw)**2
##      *    + (a2(23) + a3(23)*(Mw-c1(23)))*ALOG(R)
##       ENDIF

    #####
    # CALCULATE ROCK PGA (Per = 0, Vs30 = 1100 m/sec)
    #####

    R = math.sqrt(Rrup**2 + c4[PGA_index]**2)

    if Mw <= c1[PGA_index]:
        f_1 = a1[PGA_index] + a4[PGA_index]*(Mw-c1[PGA_index]) + a8[PGA_index]*(8.5-Mw)**2 + (a2[PGA_index] + a3[PGA_index]*(Mw-c1[PGA_index]))*math.log(R)
    else:
        f_1 = a1[PGA_index] + a5[PGA_index]*(Mw-c1[PGA_index]) + a8[PGA_index]*(8.5-Mw)**2 + (a2[PGA_index] + a3[PGA_index]*(Mw-c1[PGA_index]))*math.log(R)

## C.....
## C.....Hanging-Wall Term
## C.....
## 
##       pi = 4.0*ATAN(1.0)
##       RxTest = W*COS(Dip*pi/180.0)
## 
##       IF (Rjb .LT. 30.0) THEN
##         T1 = 1.0 - Rjb/30.0
##       ELSE
##         T1 = 0.0
##       ENDIF
## 
##       IF ((Rx .GT. RxTest) .OR. (Dip .EQ. 90.0)) THEN
##         T2 = 1.0
##       ELSE
##         T2 = 0.5 + Rx/(2.0*RxTest)
##       ENDIF
## 
##       IF (Rx .GE. Ztor) THEN
##         T3 = 1.0
##       ELSE
##         T3 = Rx/Ztor
##       ENDIF
## 
##       IF (Mw .LE. 6.0) THEN
##         T4 = 0.0
##       ELSEIF (Mw .LT. 7.0) THEN
##         T4 = Mw - 6.0
##       ELSE
##         T4 = 1.0
##       ENDIF
## 
##       IF (Dip .GE. 30.0) THEN
##         T5 = 1.0 - (Dip - 30.0)/60.0
##       ELSE
##         T5 = 1.0
##       ENDIF
## 
##       f_4 = a14(23)*T1*T2*T3*T4*T5

    #####
    # Hanging-Wall Term
    #####

    RxTest = W*math.cos(Dip*math.pi/180.0)

    if Rjb < 30.0:
        T1 = 1.0 - Rjb/30.0
    else:
        T1 = 0.0

    if (Rx > RxTest) or (Dip == 90.0):
        T2 = 1.0
    else:
        T2 = 0.5 + Rx/(2.0*RxTest)

    if Rx >= Ztor:
        T3 = 1.0
    else:
        T3 = Rx/Ztor

    if Mw <= 6.0:
        T4 = 0.0
    elif Mw < 7.0:
        T4 = Mw - 6.0
    else:
        T4 = 1.0

    if Dip >= 30.0:
        T5 = 1.0 - (Dip - 30.0)/60.0
    else:
        T5 = 1.0

    f_4 = a14[PGA_index]*T1*T2*T3*T4*T5

## C.....
## C.....Shallow Site Response Term (Vs30 = 1100 m/sec)
## C.....
## 
##       f_5 = (a10(23) + b(23)*n(23))*ALOG(1100/Vlin(23))

    #####
    # Shallow Site Response Term (Vs30 = 1100 m/sec)
    #####

    f_5 = (a10[PGA_index] + b[PGA_index]*n[PGA_index])*math.log(1100/Vlin[PGA_index])

## C.....
## C.....Depth to top of Rupture Term
## C.....
## 
##       IF (Ztor .LT. 10.0) THEN
##         f_6 = a16(23)*Ztor/10.0
##       ELSE
##         f_6 = a16(23)
##       ENDIF

    # depth to top of rupture term

    if Ztor < 10.0:
        f_6 = a16[PGA_index]*Ztor/10.0
    else:
        f_6 = a16[PGA_index]

## C.....
## C.....Large Distance Term
## C.....
## 
##       IF (Mw .LT. 5.5) THEN
##         T6 = 1.0
##       ELSEIF (Mw .LE. 6.5) THEN
##         T6 = 0.5*(6.5 - Mw) + 0.5
##       ELSE
##         T6 = 0.5
##       ENDIF
## 
##       IF (Rrup .LT. 100.0) THEN
##         f_8 = 0.0
##       ELSE
##         f_8 = a18(23)*(Rrup - 100.0)*T6
##       ENDIF

    # large distance term

    if Mw < 5.5:
        T6 = 1.0
    elif Mw <= 6.5:
        T6 = 0.5*(6.5 - Mw) + 0.5
    else:
        T6 = 0.5

    if Rrup < 100.0:
        f_8 = 0.0
    else:
        f_8 = a18[PGA_index]*(Rrup - 100.0)*T6

## C.....
## C.....Value of PGA on Rock
## C.....
## 
##       PGA_1100 = EXP(f_1 + a12(23)*Frv + a13(23)*Fnm + a15(23)*Fas + f_5
##      *  + Fhw*f_4 + f_6 + f_8)

    # PGA value for rock

    PGA_1100 = math.exp(f_1 + a12[PGA_index]*Frv + a13[PGA_index]*Fnm + a15[PGA_index]*Fas + f_5  + Fhw*f_4 + f_6 + f_8)

## C.....
## C.....CALCULATE STRONG MOTION PARAMETER
## C.....
## C.....Determine Index of Period for Constant Displacement Calculation
## C.....
## 
##       Td = 10.0**(-1.25 + 0.3*Mw)
## 
##       iTd1 = nper - 3
##       iTd2 = nper - 2
##       DO iper = 1, nper-3
##         IF ((T(iper) .LE. Td) .AND. (T(iper+1) .GT. Td)) THEN
##           iTd1 = iper
##           iTd2 = iper + 1
##         ENDIF
##       ENDDO

    # determine index of period for constant displacement calculation
    Td = 10.0**(-1.25 + 0.3*Mw)

    iTd1 = nper - 3 - 1		# 10.0s (adjusted for python zero index)
    iTd2 = nper - 2 - 1		# 0.0s (adjusted for python zero index)
    for iper in xrange(nper - 3 - 1):
        if (T[iper] <= Td) and (T[iper+1] > Td):
            iTd1 = iper
            iTd2 = iper + 1

## C.....
## C.....Magnitude and Distance Terms
## C.....
## 
##       R = SQRT(Rrup**2 + c4T**2)
## 
##       IF (Mw .LE. c1T) THEN
##         f_1 = a1T + a4T*(Mw-c1T) + a8T*(8.5-Mw)**2
##      *    + (a2T + a3T*(Mw-c1T))*ALOG(R)
##       ELSE
##         f_1 = a1T + a5T*(Mw-c1T) + a8T*(8.5-Mw)**2
##      *    + (a2T + a3T*(Mw-c1T))*ALOG(R)
##       ENDIF
## 
## C        Calculation for Constant Displacement
## 
##       RTd1 = SQRT(Rrup**2 + c4(iTd1)**2)
## 
##       IF (Mw .LE. c1(iTd1)) THEN
##         f_1Td1 = a1(iTd1) + a4(iTd1)*(Mw-c1(iTd1))
##      *    + a8(iTd1)*(8.5-Mw)**2 + (a2(iTd1) + a3(iTd1)*(Mw-c1(iTd1)))
##      *    * ALOG(RTd1)
##       ELSE
##         f_1Td1 = a1(iTd1) + a5(iTd1)*(Mw-c1(iTd1))
##      *    + a8(iTd1)*(8.5-Mw)**2 + (a2(iTd1) + a3(iTd1)*(Mw-c1(iTd1)))
##      *    * ALOG(RTd1)
##       ENDIF
## 
##       RTd2 = SQRT(Rrup**2 + c4(iTd2)**2)
## 
##       IF (Mw .LE. c1(iTd2)) THEN
##         f_1Td2 = a1(iTd2) + a4(iTd2)*(Mw-c1(iTd2))
##      *    + a8(iTd2)*(8.5-Mw)**2 + (a2(iTd2) + a3(iTd2)*(Mw-c1(iTd2)))
##      *    * ALOG(RTd2)
##       ELSE
##         f_1Td2 = a1(iTd2) + a5(iTd2)*(Mw-c1(iTd2))
##      *    + a8(iTd2)*(8.5-Mw)**2 + (a2(iTd2) + a3(iTd2)*(Mw-c1(iTd2)))
##      *    * ALOG(RTd2)
##       ENDIF

    ######
    # Magnitude and Distance Terms
    ######

    R = math.sqrt(Rrup**2 + c4T**2)

    if Mw <= c1T:
        f_1 = a1T + a4T*(Mw-c1T) + a8T*(8.5-Mw)**2 + (a2T + a3T*(Mw-c1T))*math.log(R)
    else:
        f_1 = a1T + a5T*(Mw-c1T) + a8T*(8.5-Mw)**2 + (a2T + a3T*(Mw-c1T))*math.log(R)

    # Calculation for Constant Displacement

    RTd1 = math.sqrt(Rrup**2 + c4[iTd1]**2)

    if Mw <= c1[iTd1]:
        f_1Td1 = (a1[iTd1] + a4[iTd1]*(Mw-c1[iTd1]) + a8[iTd1]*(8.5-Mw)**2 +
                  (a2[iTd1] + a3[iTd1]*(Mw-c1[iTd1])) * math.log(RTd1))
    else:
        f_1Td1 = (a1[iTd1] + a5[iTd1]*(Mw-c1[iTd1]) + a8[iTd1]*(8.5-Mw)**2 +
                  (a2[iTd1] + a3[iTd1]*(Mw-c1[iTd1])) * math.log(RTd1))

    RTd2 = math.sqrt(Rrup**2 + c4[iTd2]**2)

    if Mw <= c1[iTd2]:
        f_1Td2 = (a1[iTd2] + a4[iTd2]*(Mw-c1[iTd2]) + a8[iTd2]*(8.5-Mw)**2 +
                  (a2[iTd2] + a3[iTd2]*(Mw-c1[iTd2])) * math.log(RTd2))
    else:
        f_1Td2 = (a1[iTd2] + a5[iTd2]*(Mw-c1[iTd2]) + a8[iTd2]*(8.5-Mw)**2 +
                  (a2[iTd2] + a3[iTd2]*(Mw-c1[iTd2])) * math.log(RTd2))

## C.....
## C.....Hanging-Wall Term
## C.....
## 
##       pi = 4.0*ATAN(1.0)
##       RxTest = W*COS(Dip*pi/180.0)
## 
##       IF (Rjb .LT. 30.0) THEN
##         T1 = 1.0 - Rjb/30.0
##       ELSE
##         T1 = 0.0
##       ENDIF
## 
##       IF ((Rx .GT. RxTest) .OR. (Dip .EQ. 90.0)) THEN
##         T2 = 1.0
##       ELSE
##         T2 = 0.5 + Rx/(2.0*RxTest)
##       ENDIF
## 
##       IF (Rx .GE. Ztor) THEN
##         T3 = 1.0
##       ELSE
##         T3 = Rx/Ztor
##       ENDIF
## 
##       IF (Mw .LE. 6.0) THEN
##         T4 = 0.0
##       ELSEIF (Mw .LT. 7.0) THEN
##         T4 = Mw - 6.0
##       ELSE
##         T4 = 1.0
##       ENDIF
## 
##       IF (Dip .GE. 30.0) THEN
##         T5 = 1.0 - (Dip - 30.0)/60.0
##       ELSE
##         T5 = 1.0
##       ENDIF
## 
##       f_4 = a14T*T1*T2*T3*T4*T5

    ######
    # Hanging-Wall Term
    ######

    RxTest = W*math.cos(Dip*math.pi/180.0)

    if Rjb < 30.0:
        T1 = 1.0 - Rjb/30.0
    else:
        T1 = 0.0

    if (Rx > RxTest) or (Dip == 90.0):
        T2 = 1.0
    else:
        T2 = 0.5 + Rx/(2.0*RxTest)

    if Rx >= Ztor:
        T3 = 1.0
    else:
        T3 = Rx/Ztor

    if Mw <= 6.0:
        T4 = 0.0
    elif Mw < 7.0:
        T4 = Mw - 6.0
    else:
        T4 = 1.0

    if Dip >= 30.0:
        T5 = 1.0 - (Dip - 30.0)/60.0
    else:
        T5 = 1.0

    f_4 = a14T*T1*T2*T3*T4*T5
 
## C        Calculation for Constant Displacement
## 
##       f_4Td1 = a14(iTd1)*T1*T2*T3*T4*T5
##       f_4Td2 = a14(iTd2)*T1*T2*T3*T4*T5

    # Calculation for Constant Displacement

    f_4Td1 = a14[iTd1]*T1*T2*T3*T4*T5
    f_4Td2 = a14[iTd2]*T1*T2*T3*T4*T5

## C.....
## C.....Shallow Site Response Term for Rock (Vs30 = 1100 m/sec)
## C.....
## 
##       IF (Per .EQ. -1.0) THEN      !For PGV
##         V1 = 862.0
##       ELSEIF (Per .LE. 0.5) THEN
##         V1 = 1500.0
##       ELSEIF (Per .LE. 1.0) THEN
##         V1 = EXP(8.0 - 0.795*ALOG(Per/0.21))
##       ELSEIF (Per .LT. 2.0) THEN
##         V1 = EXP(6.76 - 0.297*ALOG(Per))
##       ELSE
##         V1 = 700.0
##       ENDIF
## 
##       IF (1100.0 .LT. V1) THEN
##         V30 = Vs30
##       ELSE
##         V30 = V1
##       ENDIF
## 
##       f_5 = (a10T + bT*nT)*ALOG(V30/VlinT)

    ######
    # Shallow Site Response Term for Rock (Vs30 = 1100 m/sec)
    ######

    if Per == -1.0:      # For PGV
        V1 = 862.0
    elif Per <= 0.5:
        V1 = 1500.0
    elif Per <= 1.0:
        V1 = math.exp(8.0 - 0.795*math.log(Per/0.21))
    elif Per < 2.0:
        V1 = math.exp(6.76 - 0.297*math.log(Per))
    else:
        V1 = 700.0

    if 1100.0 < V1:
        V30 = Vs30
    else:
        V30 = V1

    f_5 = (a10T + bT*nT)*math.log(V30/VlinT)

## C        Calculation for Constant Displacement
## 
##       IF (T(iTd1) .EQ. -1.0) THEN  !For PGV
##         V1Td1 = 862.0
##       ELSEIF (T(iTd1) .LE. 0.5) THEN
##         V1Td1 = 1500.0
##       ELSEIF (T(iTd1) .LE. 1.0) THEN
##         V1Td1 = EXP(8.0 - 0.795*ALOG(T(iTd1)/0.21))
##       ELSEIF (T(iTd1) .LT. 2.0) THEN
##         V1Td1 = EXP(6.76 - 0.297*ALOG(T(iTd1)))
##       ELSE
##         V1Td1 = 700.0
##       ENDIF
## 
##       IF (1100.0 .LT. V1Td1) THEN
##         V30Td1 = Vs30
##       ELSE
##         V30Td1 = V1Td1
##       ENDIF
## 
##       f_5Td1 = (a10(iTd1) + b(iTd1)*n(iTd1))*ALOG(V30Td1/Vlin(iTd1))
## 
##       IF (T(iTd2) .EQ. -1.0) THEN  !For PGV
##         V1Td2 = 862.0
##       ELSEIF (T(iTd2) .LE. 0.5) THEN
##         V1Td2 = 1500.0
##       ELSEIF (T(iTd2) .LE. 1.0) THEN
##         V1Td2 = EXP(8.0 - 0.795*ALOG(T(iTd2)/0.21))
##       ELSEIF (T(iTd2) .LT. 2.0) THEN
##         V1Td2 = EXP(6.76 - 0.297*ALOG(T(iTd2)))
##       ELSE
##         V1Td2 = 700.0
##       ENDIF
## 
##       IF (1100.0 .LT. V1Td2) THEN
##         V30Td2 = Vs30
##       ELSE
##         V30Td2 = V1Td2
##       ENDIF
## 
##       f_5Td2 = (a10(iTd2) + b(iTd2)*n(iTd2))*ALOG(V30Td2/Vlin(iTd2))

    # Calculation for Constant Displacement

    if T[iTd1] == -1.0:  # For PGV
        V1Td1 = 862.0
    elif T[iTd1] <= 0.5:
        V1Td1 = 1500.0
    elif T[iTd1] <= 1.0:
        V1Td1 = math.exp(8.0 - 0.795*math.log(T[iTd1]/0.21))
    elif T[iTd1] < 2.0:
        V1Td1 = math.exp(6.76 - 0.297*math.log(T[iTd1]))
    else:
        V1Td1 = 700.0

    if 1100.0 < V1Td1:
        V30Td1 = Vs30
    else:
        V30Td1 = V1Td1

    f_5Td1 = (a10[iTd1] + b[iTd1]*n[iTd1])*math.log(V30Td1/Vlin[iTd1])

    if T[iTd2] == -1.0:  # For PGV
        V1Td2 = 862.0
    elif T[iTd2] <= 0.5:
        V1Td2 = 1500.0
    elif T[iTd2] <= 1.0:
        V1Td2 = math.exp(8.0 - 0.795*math.log(T[iTd2]/0.21))
    elif T[iTd2] < 2.0:
        V1Td2 = math.exp(6.76 - 0.297*math.log(T[iTd2]))
    else:
        V1Td2 = 700.0

    if 1100.0 < V1Td2:
        V30Td2 = Vs30
    else:
        V30Td2 = V1Td2

    f_5Td2 = (a10[iTd2] + b[iTd2]*n[iTd2])*math.log(V30Td2/Vlin[iTd2])

## C.....
## C.....Depth to top of Rupture Term
## C.....
## 
##       IF (Ztor .LT. 10.0) THEN
##         f_6 = a16T*Ztor/10.0
##       ELSE
##         f_6 = a16T
##       ENDIF
## 
## C        Calcuation for Constant Dispalcement
## 
##       IF (Ztor .LT. 10.0) THEN
##         f_6Td1 = a16(iTd1)*Ztor/10.0
##       ELSE
##         f_6Td1 = a16(iTd1)
##       ENDIF
## 
##       IF (Ztor .LT. 10.0) THEN
##         f_6Td2 = a16(iTd2)*Ztor/10.0
##       ELSE
##         f_6Td2 = a16(iTd2)
##       ENDIF

    ######
    # Depth to top of Rupture Term
    ######

    if Ztor < 10.0:
        f_6 = a16T*Ztor/10.0
    else:
        f_6 = a16T

    # Calcuation for Constant Dispalcement

    if Ztor < 10.0:
        f_6Td1 = a16[iTd1]*Ztor/10.0
    else:
        f_6Td1 = a16[iTd1]

    if Ztor < 10.0:
        f_6Td2 = a16[iTd2]*Ztor/10.0
    else:
        f_6Td2 = a16[iTd2]

## C.....
## C.....Large Distance Term
## C.....
## 
##       IF (Mw .LT. 5.5) THEN
##         T6 = 1.0
##       ELSEIF (Mw .LE. 6.5) THEN
##         T6 = 0.5*(6.5 - Mw) + 0.5
##       ELSE
##         T6 = 0.5
##       ENDIF
## 
##       IF (Rrup .LT. 100.0) THEN
##         f_8 = 0.0
##       ELSE
##         f_8 = a18T*(Rrup - 100.0)*T6
##       ENDIF
## 
## C        Calculation for Constant Displacement
## 
##       IF (Rrup .LT. 100.0) THEN
##         f_8Td1 = 0.0
##       ELSE
##         f_8Td1 = a18(iTd1)*(Rrup - 100.0)*T6
##       ENDIF
## 
##       IF (Rrup .LT. 100.0) THEN
##         f_8Td2 = 0.0
##       ELSE
##         f_8Td2 = a18(iTd2)*(Rrup - 100.0)*T6
##       ENDIF

    ######
    # Large Distance Term
    ######

    if Mw < 5.5:
        T6 = 1.0
    elif Mw <= 6.5:
        T6 = 0.5*(6.5 - Mw) + 0.5
    else:
        T6 = 0.5

    if Rrup < 100.0:
        f_8 = 0.0
    else:
        f_8 = a18T*(Rrup - 100.0)*T6

    # Calculation for Constant Displacement

    if Rrup < 100.0:
        f_8Td1 = 0.0
    else:
        f_8Td1 = a18[iTd1]*(Rrup - 100.0)*T6

    if Rrup < 100.0:
        f_8Td2 = 0.0
    else:
        f_8Td2 = a18[iTd2]*(Rrup - 100.0)*T6

## C.....
## C.....Ground Motion on Rock Before Constant Displacement Adjustment
## C.....
## 
##       Y_1100 = EXP(f_1 + a12T*Frv + a13T*Fnm + a15T*Fas + f_5
##      *  + Fhw*f_4 + f_6 + f_8)
## 
##       Y_1100Td1 = EXP(f_1Td1 + a12(iTd1)*Frv + a13(iTd1)*Fnm
##      *  + a15(iTd1)*Fas + f_5Td1 + Fhw*f_4Td1 + f_6Td1 + f_8Td1)
## 
##       Y_1100Td2 = EXP(f_1Td2 + a12(iTd2)*Frv + a13(iTd2)*Fnm
##      *  + a15(iTd2)*Fas + f_5Td2 + Fhw*f_4Td2 + f_6Td2 + f_8Td2)

    #####
    # Ground Motion on Rock Before Constant Displacement Adjustment
    #####

    Y_1100 = math.exp(f_1 + a12T*Frv + a13T*Fnm + a15T*Fas + f_5 + Fhw*f_4 + f_6 + f_8)

    Y_1100Td1 = math.exp(f_1Td1 + a12[iTd1]*Frv + a13[iTd1]*Fnm +
                         a15[iTd1]*Fas + f_5Td1 + Fhw*f_4Td1 + f_6Td1 + f_8Td1)

    Y_1100Td2 = math.exp(f_1Td2 + a12[iTd2]*Frv + a13[iTd2]*Fnm +
                         a15[iTd2]*Fas + f_5Td2 + Fhw*f_4Td2 + f_6Td2 + f_8Td2)

## C.....
## C.....Ground Motion on Rock After Constant Displacement Adjustment
## C.....
## 
##       DO iper = 1, nper-3
##         IF ((T(iper) .LE. Td) .AND. (T(iper+1) .GT. Td)) THEN
##           Y_1100Td0 = EXP(ALOG(Y_1100Td2/Y_1100Td1)
##      *      /ALOG(T(iTd2)/T(iTd1))*ALOG(Td/T(iTd1)) + ALOG(Y_1100Td1))
##         ENDIF
##       ENDDO
## 
##       IF (Per .LE. Td) THEN
##         Y_1100Td = Y_1100
##       ELSE
##         Y_1100Td = Y_1100Td0*(Td/Per)**2
##       ENDIF

    #####
    # Ground Motion on Rock After Constant Displacement Adjustment
    #####

    for iper in xrange(nper-3-1):
        if (T[iper] <= Td) and (T[iper+1] > Td):
            Y_1100Td0 = math.exp(math.log(Y_1100Td2/Y_1100Td1) /
                                     math.log(T[iTd2]/T[iTd1]) *
                                     math.log(Td/T[iTd1]) +
                                  math.log(Y_1100Td1))

    if Per <= Td:
        Y_1100Td = Y_1100
    else:
        Y_1100Td = Y_1100Td0*(Td/Per)**2

## C.....
## C.....Ground Motion on Local Site Conditions
## C.....
## 
##       Y = EXP(ALOG(Y_1100Td) - f_5)
## 
## C        Shallow Site Response Term
## 
##       IF (Per .EQ. -1.0) THEN
##         V1 = 862.0
##       ELSEIF (Per .LE. 0.5) THEN
##         V1 = 1500.0
##       ELSEIF (Per .LE. 1.0) THEN
##         V1 = EXP(8.0 - 0.795*ALOG(Per/0.21))
##       ELSEIF (Per .LT. 2.0) THEN
##         V1 = EXP(6.76 - 0.297*ALOG(Per))
##       ELSE
##         V1 = 700.0
##       ENDIF
## 
##       IF (Vs30 .LT. V1) THEN
##         V30 = Vs30
##       ELSE
##         V30 = V1
##       ENDIF
## 
##       IF (Vs30 .LT. VlinT) THEN
##         f_5 = a10T*ALOG(V30/VlinT) - bT*ALOG(PGA_1100 + cT)
##      *    + bT*ALOG(PGA_1100 + cT*(V30/VlinT)**nT)
##       ELSE
##         f_5 = (a10T + bT*nT)*ALOG(V30/VlinT)
##       ENDIF

    #####
    # Ground Motion on Local Site Conditions
    #####

    Y = math.exp(math.log(Y_1100Td) - f_5)

    # Shallow Site Response Term

    if Per == -1.0:
        V1 = 862.0
    elif Per <= 0.5:
        V1 = 1500.0
    elif Per <= 1.0:
        V1 = math.exp(8.0 - 0.795*math.log(Per/0.21))
    elif Per < 2.0:
        V1 = math.exp(6.76 - 0.297*math.log(Per))
    else:
        V1 = 700.0

    if Vs30 < V1:
        V30 = Vs30
    else:
        V30 = V1

    if Vs30 < VlinT:
        f_5 = (a10T*math.log(V30/VlinT) - bT*math.log(PGA_1100 + cT) +
               bT*math.log(PGA_1100 + cT*(V30/VlinT)**nT))
    else:
        f_5 = (a10T + bT*nT)*math.log(V30/VlinT)

## C        Soil Depth Term
## 
##       IF (Vs30 .LT. 180.0) THEN
##         Z10_med = EXP(6.745)
##       ELSEIF (Vs30 .LE. 500.0) THEN
##         Z10_med = EXP(6.745 - 1.35*ALOG(Vs30/180.0))
##       ELSE
##         Z10_med = EXP(5.394 - 4.48*ALOG(Vs30/500.0))
##       ENDIF
## 
##       IF ((Per .EQ. -1.0) .AND. (Vs30 .GT. 1000.0)) THEN
##         e2 = 0.0
##         GOTO 1040
##       ELSEIF (Per .EQ. -1.0) THEN
##         e2 = -0.25*ALOG(Vs30/1000.0)*ALOG(1.0/0.35)
##         GOTO 1040
##       ELSEIF ((Per .LT. 0.35) .OR. (Vs30 .GT. 1000.0)) THEN
##         e2 = 0.0
##       ELSEIF (Per .LE. 2.0) THEN
##         e2 = -0.25*ALOG(Vs30/1000.0)*ALOG(Per/0.35)
##       ELSE
##         e2 = -0.25*ALOG(Vs30/1000.0)*ALOG(2.0/0.35)
##       ENDIF

    # Soil Depth Term

    if Vs30 < 180.0:
        Z10_med = math.exp(6.745)
    elif Vs30 <= 500.0:
        Z10_med = math.exp(6.745 - 1.35*math.log(Vs30/180.0))
    else:
        Z10_med = math.exp(5.394 - 4.48*math.log(Vs30/500.0))

    if (Per == -1.0) and (Vs30 > 1000.0):
        e2 = 0.0
    elif Per == -1.0:
        e2 = -0.25*math.log(Vs30/1000.0)*math.log(1.0/0.35)
    elif (Per < 0.35) or (Vs30 > 1000.0):
        e2 = 0.0
    elif Per <= 2.0:
        e2 = -0.25*math.log(Vs30/1000.0)*math.log(Per/0.35)
    else:
        e2 = -0.25*math.log(Vs30/1000.0)*math.log(2.0/0.35)

##  1040 IF (Per .LT. 2.0) THEN
##         a22 = 0.0
##       ELSE
##         a22 = 0.0625*(Per - 2.0)
##       ENDIF
## 
##       a21Test = (a10T + bT*nT)*ALOG(V30/MIN(V1,1000.0))
##      *  + e2*ALOG((Z10+c2T)/(Z10_med+c2T))
## 
##       IF (Vs30 .GE. 1000.0) THEN
##         a21 = 0.0
##       ELSEIF (a21Test .LT. 0.0) THEN
##         a21 = -(a10T + bT*nT)
##      *  * ALOG(V30/MIN(V1,1000.0))/ALOG((Z10+c2T)/(Z10_med+c2T))
##       ELSE
##         a21 = e2
##       ENDIF
## 
##       IF (Z10 .GE. 200.0) THEN
##         f_10 = a21*ALOG((Z10+c2T)/(Z10_med+c2T))
##      *    + a22*ALOG(Z10/200.0)
##       ELSE
##         f_10 = a21*ALOG((Z10+c2T)/(Z10_med+c2T))
##       ENDIF

    if Per < 2.0:
        a22 = 0.0
    else:
        a22 = 0.0625*(Per - 2.0)

    a21Test = ((a10T + bT*nT)*math.log(V30/min(V1,1000.0)) +
               e2*math.log((Z10+c2T)/(Z10_med+c2T)))

    if Vs30 >= 1000.0:
        a21 = 0.0
    elif a21Test < 0.0:
        a21 = (-(a10T + bT*nT) *
               math.log(V30/min(V1,1000.0))/math.log((Z10+c2T)/(Z10_med+c2T)))
    else:
        a21 = e2

    if Z10 >= 200.0:
        f_10 = a21*math.log((Z10+c2T)/(Z10_med+c2T)) + a22*math.log(Z10/200.0)
    else:
        f_10 = a21*math.log((Z10+c2T)/(Z10_med+c2T))

## C.....
## C.....Value of Ground Motion Parameter
## C.....
## 
##       Y = EXP(ALOG(Y) + f_5 + f_10)

    #####
    # Value of Ground Motion Parameter
    #####

    Y = math.exp(math.log(Y) + f_5 + f_10)

## C.....
## C.....CALCULATE ALEATORY UNCERTAINTY
## C.....
## C.....Partial Derivative of ln f_5 With Respect to ln PGA
## C.....
## 
##       IF (Vs30 .LT. VlinT) THEN
##         Alpha = bT*PGA_1100 * (1.0/(PGA_1100 + cT*(V30/VlinT)**nT)
##      *    - 1.0/(PGA_1100 + cT))
##       ELSE
##         Alpha = 0.0
##       ENDIF

    #####
    # CALCULATE ALEATORY UNCERTAINTY
    # Partial Derivative of ln f_5 With Respect to ln PGA
    #####

    if Vs30 < VlinT:
        Alpha = bT*PGA_1100 * (1.0/(PGA_1100 + cT*(V30/VlinT)**nT) - 1.0/(PGA_1100 + cT))
    else:
        Alpha = 0.0

## C.....
## C.....Intra-Event Standard Deviation
## C.....
## 
##       slnAF = 0.3
## 
## C        Estimated Vs30
## 
##       IF (Mw .LT. 5.0) THEN  !For PGA
##         s0Aest = s1est(23)
##       ELSEIF (Mw .LE. 7.0) THEN
##         s0Aest = s1est(23) + (s2est(23)-s1est(23))*(Mw-5.0)/2.0
##       ELSE
##         s0Aest = s2est(23)
##       ENDIF
## 
##       IF (Mw .LT. 5.0) THEN  !For Y
##         s0Yest = s1estT
##       ELSEIF (Mw .LE. 7.0) THEN
##         s0Yest = s1estT + (s2estT-s1estT)*(Mw-5.0)/2.0
##       ELSE
##         s0Yest = s2estT
##       ENDIF
## 
##       sBAest = SQRT(s0Aest**2 - slnAF**2)  !For PGA at base of profile
##       sBYest = SQRT(s0Yest**2 - slnAF**2)  !For Y at base of profile

    #####
    # Intra-Event Standard Deviation
    #####

    slnAF = 0.3

    # Estimated Vs30

    if Mw < 5.0:  # For PGA
        s0Aest = s1est[PGA_index]
    elif Mw <= 7.0:
        s0Aest = (s1est[PGA_index] +
                  (s2est[PGA_index]-s1est[PGA_index])*(Mw-5.0)/2.0)
    else:
        s0Aest = s2est[PGA_index]

    if Mw < 5.0:  # For Y
        s0Yest = s1estT
    elif Mw <= 7.0:
        s0Yest = s1estT + (s2estT-s1estT)*(Mw-5.0)/2.0
    else:
        s0Yest = s2estT

    sBAest = math.sqrt(s0Aest**2 - slnAF**2)  # For PGA at base of profile
    sBYest = math.sqrt(s0Yest**2 - slnAF**2)  # For Y at base of profile

## C        Measured Vs30
## 
##       IF (Mw .LT. 5.0) THEN  !For PGA
##         s0Amea = s1mea(23)
##       ELSEIF (Mw .LE. 7.0) THEN
##         s0Amea = s1mea(23) + (s2mea(23)-s1mea(23))*(Mw-5.0)/2.0
##       ELSE
##         s0Amea = s2mea(23)
##       ENDIF
## 
##       IF (Mw .LT. 5.0) THEN  !For Y
##         s0Ymea = s1meaT
##       ELSEIF (Mw .LE. 7.0) THEN
##         s0Ymea = s1meaT + (s2meaT-s1meaT)*(Mw-5.0)/2.0
##       ELSE
##         s0Ymea = s2meaT
##       ENDIF
## 
##       sBAmea = SQRT(s0Amea**2 - slnAF**2)  !For PGA at base of profile
##       sBYmea = SQRT(s0Ymea**2 - slnAF**2)  !For Y at base of profile

    # Measured Vs30

    if Mw < 5.0:  # For PGA
        s0Amea = s1mea[PGA_index]
    elif Mw <= 7.0:
        s0Amea = (s1mea[PGA_index] +
                  (s2mea[PGA_index]-s1mea[PGA_index])*(Mw-5.0)/2.0)
    else:
        s0Amea = s2mea[PGA_index]

    if Mw < 5.0:  # For Y
        s0Ymea = s1meaT
    elif Mw <= 7.0:
        s0Ymea = s1meaT + (s2meaT-s1meaT)*(Mw-5.0)/2.0
    else:
        s0Ymea = s2meaT

    sBAmea = math.sqrt(s0Amea**2 - slnAF**2)  # For PGA at base of profile
    sBYmea = math.sqrt(s0Ymea**2 - slnAF**2)  # For Y at base of profile

## C.....
## C.....Inter-Event Standard Deviation
## C.....
## 
##       IF (Mw .LT. 5.0) THEN  !For PGA
##         tau0A = s3(23)
##       ELSEIF (Mw .LE. 7.0) THEN
##         tau0A = s3(23) + (s4(23)-s3(23))*(Mw-5.0)/2.0
##       ELSE
##         tau0A = s4(23)
##       ENDIF
## 
##       IF (Mw .LT. 5.0) THEN  !For Y
##         tau0Y = s3T
##       ELSEIF (Mw .LE. 7.0) THEN
##         tau0Y = s3T + (s4T-s3T)*(Mw-5.0)/2.0
##       ELSE
##         tau0Y = s4T
##       ENDIF
## 
##       tauBA = tau0A  !For PGA at base of profile
##       tauBY = tau0Y  !For Y at base of profile

    #####
    # Inter-Event Standard Deviation
    #####

    if Mw < 5.0:  # For PGA
        tau0A = s3[PGA_index]
    elif Mw <= 7.0:
        tau0A = s3[PGA_index] + (s4[PGA_index]-s3[PGA_index])*(Mw-5.0)/2.0
    else:
        tau0A = s4[PGA_index]

    if Mw < 5.0:  # For Y
        tau0Y = s3T
    elif Mw <= 7.0:
        tau0Y = s3T + (s4T-s3T)*(Mw-5.0)/2.0
    else:
        tau0Y = s4T

    tauBA = tau0A  # For PGA at base of profile
    tauBY = tau0Y  # For Y at base of profile

## C.....
## C.....Standard Deviation of Geometric Mean of ln Y
## C.....
## 
##       Tau = SQRT(tau0Y**2 + (Alpha**2)*(tauBA**2)
##      *  + 2.0*Alpha*rhoT*tauBY*tauBA)
## 
## C        Estimated Vs30
## 
##       Sigest = SQRT(sBYest**2 + slnAF**2 + (Alpha**2)*(sBAest**2)
##      *  + 2.0*Alpha*rhoT*sBYest*sBAest)
## 
##       SigTest = SQRT(Sigest**2 + Tau**2)
## 
## C        Measured Vs30
## 
##       Sigmea = SQRT(sBYmea**2 + slnAF**2 + (Alpha**2)*(sBAmea**2)
##      *  + 2.0*Alpha*rhoT*sBYmea*sBAmea)
## 
##       SigTmea = SQRT(Sigmea**2 + Tau**2)
## 
##       RETURN

    #####
    # Standard Deviation of Geometric Mean of ln Y
    #####

    Tau = math.sqrt(tau0Y**2 + (Alpha**2)*(tauBA**2) +
                    2.0*Alpha*rhoT*tauBY*tauBA)

    # Estimated Vs30

    Sigest = math.sqrt(sBYest**2 + slnAF**2 + (Alpha**2)*(sBAest**2) +
                       2.0*Alpha*rhoT*sBYest*sBAest)

    SigTest = math.sqrt(Sigest**2 + Tau**2)

    # Measured Vs30

    Sigmea = math.sqrt(sBYmea**2 + slnAF**2 + (Alpha**2)*(sBAmea**2) +
                       2.0*Alpha*rhoT*sBYmea*sBAmea)

    SigTmea = math.sqrt(Sigmea**2 + Tau**2)

    return (Y, SigTest)

######
# Routine to convert Vs30 to Z1.0 value - taken from nga_gm_tmr.for.
######

#          if (Vs30 .lt. 180.0) then
#            Zsed1p0_AS08 = EXP(6.745)
#          else if (Vs30 .gt. 500.0) then
#            Zsed1p0_AS08 = EXP(5.394-4.48*alog(Vs30/500.0))
#          else
#            Zsed1p0_AS08 = EXP(6.745-1.35*alog(Vs30/180.0))
#          end if

def convert_Vs30_to_Z10(Vs30):
    if Vs30 < 180.0:
        Z10 = math.exp(6.745)
    elif Vs30 > 500.0:
        Z10 = math.exp(5.394-4.48*math.log(Vs30/500.0))
    else:
        Z10 = math.exp(6.745-1.35*math.log(Vs30/180.0))

    return Z10

######
# Start generating results
######

# generate CTL data to produce same data that produces AS08_MEDIAN_MS_FW_SS.OUT
FRV = 0
FNM = 0
#FHW = 0
FAS = 0

Rake = -1
# use Rake = -70 -> FNM=1.0, FRV=0.0
#              0 -> FNM=0.0, FRV=0.0
#             70 -> FNM=1.0, FRV=1.0

W = 10.0

AZ = 0
Z25 = -1
Zhyp = -1

T_range = (0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.5, 10.0)

Vs30_range = (150.0, 180.0, 255.0, 360.0, 525.0, 760.0, 1070.0, 1500.0)

Ztor_range = (0.0, 5.0)

Dip_range = (30.0, 60.0, 90.0)

Rjb_range = (0.0,1.0,5.0,10.0,50.0,100.0,200.0,)

Mw_range = (4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0, 8.5)

# print header here
print('!T        Mw        Fhw       Az        Rjb       Rrup      Zhyp      Rake      Dip       W         Ztor      Vs30      Z10       Z25       FAS')

# now loop through all parameters
for Mw in Mw_range:
    for Rjb in Rjb_range:
        Rx = Rrup = Rjb
        for Dip in Dip_range:
            for Ztor in Ztor_range:
                for Vs30 in Vs30_range:
                    Z10 = convert_Vs30_to_Z10(Vs30)
                    for Per in T_range:
                        for FHW in (0, 1):
                            (Sa, tsigma) = AS08_MODEL(Mw, Rrup, Rjb, Rx, FRV, FNM, FHW, FAS, Ztor, Dip, W, Vs30, Z10, Per)
                            print('%9.3e %9.3E %9.3E %9.3E %9.3E %9.3E %9.3E %9.3E %9.3E %9.3E %9.3E %9.3E'
                                  % (Per,Mw,Rrup,Rjb,Rx,Dip,W,Ztor,Vs30,Z10,Sa,tsigma))
