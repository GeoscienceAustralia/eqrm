      SUBROUTINE AS08_MODEL_subroutine()
 
C.....
C.....PURPOSE: Evaluates Abrahamson-Silva NGA ground motion prediction equation
C              for a single period
C.....

* Call the setup entry point:
*     call AS08_MODEL_SETUP()
 
* Call as a subroutine:
*      call AS08_MODEL  (Mw,Rrup,Rjb,Rx,Frv,Fnm,Fhw,Fas,Ztor,Dip,W,
*     :           Vs30,Z10,Per,Y,Sigest,Sigmea,Tau,SigTest,SigTmea)
 


C.....MODEL VERSION: Final, February 2008 (Earthquake Spectra, Vol. 24, p. 67-97)
C.....
C.....HISTORY
C       12/21/07 - Written by K. Campbell
C       08/13/08 - Updated to Earthquake Spectra version (except as noted below)
C                - Changed Ztop to Ztor to correspond with published paper
C                - Changed Fn to Fnm to correspond with published paper
C                - Corrected Ztor term to corresond with published paper
C                - Corrected large distance term to correspond with published paper
C                - Corrected equation for Alpha (Eq. 26 in paper is incorrect per Abrahamson)
C                - Corrected equation for Sigma (Eq. 24 in paper is incorrect per Abrahamson)
C       01/31/09 - Corrected Constant Displacement Calculation of Ztor term per Goulet
*       03/29/09 - Dave Boore's modifications from this date on:
*                  Added entry points so that only need to read the table of
*                  coefficients once; modernize the code to some extent
*       12/15/09 - Moved the subroutine and coefficient file to the folder containing
*                  the driver, and thus simplified the path part of file
*                  specification in the open statement.
!       04/07/10 - Add path for NGA GMPE coefficients
!       04/08/10 - Inquire to see if coefficient file exists
!                - Revised hanging wall term T5, as per the erratum "AS08_NGA_errata.pdf",
!                  available from http://peer.berkeley.edu/products/Abrahamson-Silva_NGA.html
!       05/01/10 - Revised hanging wall term T5 in a second place (thanks to Jim Kaklamanos for
!                  spotting this).

C.....

C.....
C.....PARAMETER DEFINITIONS
C.....

C     Mw      = Moment magnitude
C     Rrup    = Closest distance to coseismic rupture (km)
C     Rjb     = Closest distance to surface projection of coseismic rupture (km)
C     Rx      = Horizontal distance from top edge of fault perpendicular to strike (km)
C     Ztor    = Depth to top of coseismic rupture (km)
C     Frv     = 1 for Reverse and Reverse-oblique faulting (30 < rake < 150), 0 otherwise
C     Fnm     = 1 for Normal faulting (-120 < rake < -60), 0 otherwise
C     Fas     = 1 for aftershocks, 0 for mainshocks
C     Fhw     = 1 for site on hanging wall side of fault, 0 otherwise
C     Dip     = Average dip of rupture plane (degrees)
C     W       = Downdip rupture width (km)
C     Vs30    = Average shear-wave velocity in top 30m of site profile (m/sec)
C     Z10     = Depth to 1.0 km/sec shear-wave velocity horizon (m)
C     Per     = Spectral period for PSA (sec); 0 for PGA, -1 for PGV
C     Y       = Ground motion parameter: PGA and PSA (g), PGV (cm/sec)
C     Sigest  = Intra-event standard deviation of ln Y for estimated Vs30
C     Sigmea  = intra-event standard deviation of ln Y for measured Vs30
C     Tau     = Inter-event standard deviation of ln Y
C     SigTest = Total standard deviation of geometric mean of ln Y for estimated Vs30
C     SigTmea = Total standard deviation of geometric mean of ln Y for measured Vs30

      save
      
      integer :: i = 0, nper = 0
      integer :: status


      PARAMETER (npermax=30)
!      PARAMETER (nper=24)
      REAL T(npermax), c1(npermax), c4(npermax), 
     :     a3(npermax), a4(npermax), a5(npermax)
      REAL n(npermax), c(npermax), c2(npermax), Vlin(npermax), 
     :     b(npermax), a1(npermax)
      REAL a2(npermax), a8(npermax), a10(npermax), a12(npermax), 
     :     a13(npermax)
      REAL a14(npermax), a15(npermax), a16(npermax), a17(npermax), 
     :     a18(npermax)
      REAL s1est(npermax), s2est(npermax), s1mea(npermax), 
     :     s2mea(npermax), s3(npermax)
      REAL s4(npermax), rho(npermax), nT, Mw

      character path_nga_gmpe_coeff_files*(*)
      
      logical file_exist

      ENTRY AS08_MODEL_SETUP(path_nga_gmpe_coeff_files)
      
C.....
C.....READ MODEL COEFFICIENTS
C.....

      call trim_c(path_nga_gmpe_coeff_files, 
     :            nc_path_nga_gmpe_coeff_files)

      file_exist = .false.
      inquire(file=path_nga_gmpe_coeff_files(1:
     :      nc_path_nga_gmpe_coeff_files)//'AS08_COEFS.TXT', 
     :      exist=file_exist)
      if (.not. file_exist) then
        write(*,'(a)') ' ******* FILE '//path_nga_gmpe_coeff_files(1:
     :      nc_path_nga_gmpe_coeff_files)//'AS08_COEFS.TXT'//
     :      'DOES NOT EXIST ******* '
        STOP
      end if

      nu_coeffs = 10
      OPEN (nu_coeffs,FILE=path_nga_gmpe_coeff_files(1:
     :      nc_path_nga_gmpe_coeff_files)//'AS08_COEFS.TXT',
     :      status='old')
      nskip = 5  ! may be different for each developer's GMPEs
      call skip(nu_coeffs, nskip)
      readloop: DO 
        i = i + 1
        READ (nu_coeffs,*,IOSTAT=status) 
     :    T(i),c1(i),c4(i),a3(i),a4(i),a5(i),n(i),c(i),c2(i),
     *    Vlin(i),b(i),a1(i),a2(i),a8(i),a10(i),a12(i),a13(i),a14(i),
     *    a15(i),a16(i),a18(i),s1est(i),s2est(i),s1mea(i),
     *    s2mea(i),s3(i),s4(i),rho(i)
        if (status /= 0) EXIT
        nper = nper + 1
      END DO readloop
      
      close(nu_coeffs)
!      print *,' in subroutine, nper = ', nper
      
      
      return


      entry AS08_MODEL (Mw,Rrup,Rjb,Rx,Frv,Fnm,Fhw,Fas,Ztor,Dip,W,
     :           Vs30,Z10,Per,Y,Sigest,Sigmea,Tau,SigTest,SigTmea)

C.....
C.....DETERMINE WHICH STRONG MOTION PARAMETER TO EVALUATE
C.....

      DO i = 1, nper
        IF (Per .EQ. T(i)) THEN
          iper = i
          GOTO 1020
        ENDIF
      ENDDO

      print *,' '
      print *, 'In AS08--ERROR: Period ',Per,
     :         ' is not supported; quitting'
      print *,' '
      stop


 1020 c1T    = c1(iper)
      c4T    = c4(iper)
      a3T    = a3(iper)
      a4T    = a4(iper)
      a5T    = a5(iper)
      nT     = n(iper)
      cT     = c(iper)
      c2T    = c2(iper)
      VlinT  = Vlin(iper)
      bT     = b(iper)
      a1T    = a1(iper)
      a2T    = a2(iper)
      a8T    = a8(iper)
      a10T   = a10(iper)
      a12T   = a12(iper)
      a13T   = a13(iper)
      a14T   = a14(iper)
      a15T   = a15(iper)
      a16T   = a16(iper)
      a18T   = a18(iper)
      s1estT = s1est(iper)
      s2estT = s2est(iper)
      s1meaT = s1mea(iper)
      s2meaT = s2mea(iper)
      s3T    = s3(iper)
      s4T    = s4(iper)
      rhoT   = rho(iper)

C.....
C.....CALCULATE ROCK PGA (Per = 0, Vs30 = 1100 m/sec)
C.....
C.....Magnitude and Distance Terms
C.....

      R = SQRT(Rrup**2 + c4(23)**2)

      IF (Mw .LE. c1(23)) THEN
        f_1 = a1(23) + a4(23)*(Mw-c1(23)) + a8(23)*(8.5-Mw)**2
     *    + (a2(23) + a3(23)*(Mw-c1(23)))*ALOG(R)
      ELSE
        f_1 = a1(23) + a5(23)*(Mw-c1(23)) + a8(23)*(8.5-Mw)**2
     *    + (a2(23) + a3(23)*(Mw-c1(23)))*ALOG(R)
      ENDIF

C.....
C.....Hanging-Wall Term
C.....

      pi = 4.0*ATAN(1.0)
      RxTest = W*COS(Dip*pi/180.0)

      IF (Rjb .LT. 30.0) THEN
        T1 = 1.0 - Rjb/30.0
      ELSE
        T1 = 0.0
      ENDIF

      IF ((Rx .GT. RxTest) .OR. (Dip .EQ. 90.0)) THEN
        T2 = 1.0
      ELSE
        T2 = 0.5 + Rx/(2.0*RxTest)
      ENDIF

      IF (Rx .GE. Ztor) THEN
        T3 = 1.0
      ELSE
        T3 = Rx/Ztor
      ENDIF

      IF (Mw .LE. 6.0) THEN
        T4 = 0.0
      ELSEIF (Mw .LT. 7.0) THEN
        T4 = Mw - 6.0
      ELSE
        T4 = 1.0
      ENDIF

      IF (Dip .GE. 30.0) THEN
        T5 = 1.0 - (Dip - 30.0)/60.0
      ELSE
        T5 = 1.0
      ENDIF

      f_4 = a14(23)*T1*T2*T3*T4*T5

C.....
C.....Shallow Site Response Term (Vs30 = 1100 m/sec)
C.....

      f_5 = (a10(23) + b(23)*n(23))*ALOG(1100/Vlin(23))

C.....
C.....Depth to top of Rupture Term
C.....

      IF (Ztor .LT. 10.0) THEN
        f_6 = a16(23)*Ztor/10.0
      ELSE
        f_6 = a16(23)
      ENDIF

C.....
C.....Large Distance Term
C.....

      IF (Mw .LT. 5.5) THEN
        T6 = 1.0
      ELSEIF (Mw .LE. 6.5) THEN
        T6 = 0.5*(6.5 - Mw) + 0.5
      ELSE
        T6 = 0.5
      ENDIF

      IF (Rrup .LT. 100.0) THEN
        f_8 = 0.0
      ELSE
        f_8 = a18(23)*(Rrup - 100.0)*T6
      ENDIF

C.....
C.....Value of PGA on Rock
C.....

      PGA_1100 = EXP(f_1 + a12(23)*Frv + a13(23)*Fnm + a15(23)*Fas + f_5
     *  + Fhw*f_4 + f_6 + f_8)

C.....
C.....CALCULATE STRONG MOTION PARAMETER
C.....
C.....Determine Index of Period for Constant Displacement Calculation
C.....

      Td = 10.0**(-1.25 + 0.3*Mw)

      iTd1 = nper - 3
      iTd2 = nper - 2
      DO iper = 1, nper-3
        IF ((T(iper) .LE. Td) .AND. (T(iper+1) .GT. Td)) THEN
          iTd1 = iper
          iTd2 = iper + 1
        ENDIF
      ENDDO

C.....
C.....Magnitude and Distance Terms
C.....

      R = SQRT(Rrup**2 + c4T**2)

      IF (Mw .LE. c1T) THEN
        f_1 = a1T + a4T*(Mw-c1T) + a8T*(8.5-Mw)**2
     *    + (a2T + a3T*(Mw-c1T))*ALOG(R)
      ELSE
        f_1 = a1T + a5T*(Mw-c1T) + a8T*(8.5-Mw)**2
     *    + (a2T + a3T*(Mw-c1T))*ALOG(R)
      ENDIF

C        Calculation for Constant Displacement

      RTd1 = SQRT(Rrup**2 + c4(iTd1)**2)

      IF (Mw .LE. c1(iTd1)) THEN
        f_1Td1 = a1(iTd1) + a4(iTd1)*(Mw-c1(iTd1))
     *    + a8(iTd1)*(8.5-Mw)**2 + (a2(iTd1) + a3(iTd1)*(Mw-c1(iTd1)))
     *    * ALOG(RTd1)
      ELSE
        f_1Td1 = a1(iTd1) + a5(iTd1)*(Mw-c1(iTd1))
     *    + a8(iTd1)*(8.5-Mw)**2 + (a2(iTd1) + a3(iTd1)*(Mw-c1(iTd1)))
     *    * ALOG(RTd1)
      ENDIF

      RTd2 = SQRT(Rrup**2 + c4(iTd2)**2)

      IF (Mw .LE. c1(iTd2)) THEN
        f_1Td2 = a1(iTd2) + a4(iTd2)*(Mw-c1(iTd2))
     *    + a8(iTd2)*(8.5-Mw)**2 + (a2(iTd2) + a3(iTd2)*(Mw-c1(iTd2)))
     *    * ALOG(RTd2)
      ELSE
        f_1Td2 = a1(iTd2) + a5(iTd2)*(Mw-c1(iTd2))
     *    + a8(iTd2)*(8.5-Mw)**2 + (a2(iTd2) + a3(iTd2)*(Mw-c1(iTd2)))
     *    * ALOG(RTd2)
      ENDIF

C.....
C.....Hanging-Wall Term
C.....

      pi = 4.0*ATAN(1.0)
      RxTest = W*COS(Dip*pi/180.0)

      IF (Rjb .LT. 30.0) THEN
        T1 = 1.0 - Rjb/30.0
      ELSE
        T1 = 0.0
      ENDIF

      IF ((Rx .GT. RxTest) .OR. (Dip .EQ. 90.0)) THEN
        T2 = 1.0
      ELSE
        T2 = 0.5 + Rx/(2.0*RxTest)
      ENDIF

      IF (Rx .GE. Ztor) THEN
        T3 = 1.0
      ELSE
        T3 = Rx/Ztor
      ENDIF

      IF (Mw .LE. 6.0) THEN
        T4 = 0.0
      ELSEIF (Mw .LT. 7.0) THEN
        T4 = Mw - 6.0
      ELSE
        T4 = 1.0
      ENDIF

      IF (Dip .GE. 30.0) THEN
        T5 = 1.0 - (Dip - 30.0)/60.0
      ELSE
        T5 = 1.0
      ENDIF

      f_4 = a14T*T1*T2*T3*T4*T5

C        Calculation for Constant Displacement

      f_4Td1 = a14(iTd1)*T1*T2*T3*T4*T5
      f_4Td2 = a14(iTd2)*T1*T2*T3*T4*T5

C.....
C.....Shallow Site Response Term for Rock (Vs30 = 1100 m/sec)
C.....

      IF (Per .EQ. -1.0) THEN      !For PGV
        V1 = 862.0
      ELSEIF (Per .LE. 0.5) THEN
        V1 = 1500.0
      ELSEIF (Per .LE. 1.0) THEN
        V1 = EXP(8.0 - 0.795*ALOG(Per/0.21))
      ELSEIF (Per .LT. 2.0) THEN
        V1 = EXP(6.76 - 0.297*ALOG(Per))
      ELSE
        V1 = 700.0
      ENDIF

      IF (1100.0 .LT. V1) THEN
        V30 = Vs30
      ELSE
        V30 = V1
      ENDIF

      f_5 = (a10T + bT*nT)*ALOG(V30/VlinT)

C        Calculation for Constant Displacement

      IF (T(iTd1) .EQ. -1.0) THEN  !For PGV
        V1Td1 = 862.0
      ELSEIF (T(iTd1) .LE. 0.5) THEN
        V1Td1 = 1500.0
      ELSEIF (T(iTd1) .LE. 1.0) THEN
        V1Td1 = EXP(8.0 - 0.795*ALOG(T(iTd1)/0.21))
      ELSEIF (T(iTd1) .LT. 2.0) THEN
        V1Td1 = EXP(6.76 - 0.297*ALOG(T(iTd1)))
      ELSE
        V1Td1 = 700.0
      ENDIF

      IF (1100.0 .LT. V1Td1) THEN
        V30Td1 = Vs30
      ELSE
        V30Td1 = V1Td1
      ENDIF

      f_5Td1 = (a10(iTd1) + b(iTd1)*n(iTd1))*ALOG(V30Td1/Vlin(iTd1))

      IF (T(iTd2) .EQ. -1.0) THEN  !For PGV
        V1Td2 = 862.0
      ELSEIF (T(iTd2) .LE. 0.5) THEN
        V1Td2 = 1500.0
      ELSEIF (T(iTd2) .LE. 1.0) THEN
        V1Td2 = EXP(8.0 - 0.795*ALOG(T(iTd2)/0.21))
      ELSEIF (T(iTd2) .LT. 2.0) THEN
        V1Td2 = EXP(6.76 - 0.297*ALOG(T(iTd2)))
      ELSE
        V1Td2 = 700.0
      ENDIF

      IF (1100.0 .LT. V1Td2) THEN
        V30Td2 = Vs30
      ELSE
        V30Td2 = V1Td2
      ENDIF

      f_5Td2 = (a10(iTd2) + b(iTd2)*n(iTd2))*ALOG(V30Td2/Vlin(iTd2))

C.....
C.....Depth to top of Rupture Term
C.....

      IF (Ztor .LT. 10.0) THEN
        f_6 = a16T*Ztor/10.0
      ELSE
        f_6 = a16T
      ENDIF

C        Calcuation for Constant Dispalcement

      IF (Ztor .LT. 10.0) THEN
        f_6Td1 = a16(iTd1)*Ztor/10.0
      ELSE
        f_6Td1 = a16(iTd1)
      ENDIF

      IF (Ztor .LT. 10.0) THEN
        f_6Td2 = a16(iTd2)*Ztor/10.0
      ELSE
        f_6Td2 = a16(iTd2)
      ENDIF

C.....
C.....Large Distance Term
C.....

      IF (Mw .LT. 5.5) THEN
        T6 = 1.0
      ELSEIF (Mw .LE. 6.5) THEN
        T6 = 0.5*(6.5 - Mw) + 0.5
      ELSE
        T6 = 0.5
      ENDIF

      IF (Rrup .LT. 100.0) THEN
        f_8 = 0.0
      ELSE
        f_8 = a18T*(Rrup - 100.0)*T6
      ENDIF

C        Calculation for Constant Displacement

      IF (Rrup .LT. 100.0) THEN
        f_8Td1 = 0.0
      ELSE
        f_8Td1 = a18(iTd1)*(Rrup - 100.0)*T6
      ENDIF

      IF (Rrup .LT. 100.0) THEN
        f_8Td2 = 0.0
      ELSE
        f_8Td2 = a18(iTd2)*(Rrup - 100.0)*T6
      ENDIF

C.....
C.....Ground Motion on Rock Before Constant Displacement Adjustment
C.....

      Y_1100 = EXP(f_1 + a12T*Frv + a13T*Fnm + a15T*Fas + f_5
     *  + Fhw*f_4 + f_6 + f_8)

      Y_1100Td1 = EXP(f_1Td1 + a12(iTd1)*Frv + a13(iTd1)*Fnm
     *  + a15(iTd1)*Fas + f_5Td1 + Fhw*f_4Td1 + f_6Td1 + f_8Td1)

      Y_1100Td2 = EXP(f_1Td2 + a12(iTd2)*Frv + a13(iTd2)*Fnm
     *  + a15(iTd2)*Fas + f_5Td2 + Fhw*f_4Td2 + f_6Td2 + f_8Td2)

C.....
C.....Ground Motion on Rock After Constant Displacement Adjustment
C.....

      DO iper = 1, nper-3
        IF ((T(iper) .LE. Td) .AND. (T(iper+1) .GT. Td)) THEN
          Y_1100Td0 = EXP(ALOG(Y_1100Td2/Y_1100Td1)
     *      /ALOG(T(iTd2)/T(iTd1))*ALOG(Td/T(iTd1)) + ALOG(Y_1100Td1))
        ENDIF
      ENDDO

      IF (Per .LE. Td) THEN
        Y_1100Td = Y_1100
      ELSE
        Y_1100Td = Y_1100Td0*(Td/Per)**2
      ENDIF

C.....
C.....Ground Motion on Local Site Conditions
C.....

      Y = EXP(ALOG(Y_1100Td) - f_5)

C        Shallow Site Response Term

      IF (Per .EQ. -1.0) THEN
        V1 = 862.0
      ELSEIF (Per .LE. 0.5) THEN
        V1 = 1500.0
      ELSEIF (Per .LE. 1.0) THEN
        V1 = EXP(8.0 - 0.795*ALOG(Per/0.21))
      ELSEIF (Per .LT. 2.0) THEN
        V1 = EXP(6.76 - 0.297*ALOG(Per))
      ELSE
        V1 = 700.0
      ENDIF

      IF (Vs30 .LT. V1) THEN
        V30 = Vs30
      ELSE
        V30 = V1
      ENDIF

      IF (Vs30 .LT. VlinT) THEN
        f_5 = a10T*ALOG(V30/VlinT) - bT*ALOG(PGA_1100 + cT)
     *    + bT*ALOG(PGA_1100 + cT*(V30/VlinT)**nT)
      ELSE
        f_5 = (a10T + bT*nT)*ALOG(V30/VlinT)
      ENDIF

C        Soil Depth Term

      IF (Vs30 .LT. 180.0) THEN
        Z10_med = EXP(6.745)
      ELSEIF (Vs30 .LE. 500.0) THEN
        Z10_med = EXP(6.745 - 1.35*ALOG(Vs30/180.0))
      ELSE
        Z10_med = EXP(5.394 - 4.48*ALOG(Vs30/500.0))
      ENDIF

      IF ((Per .EQ. -1.0) .AND. (Vs30 .GT. 1000.0)) THEN
        e2 = 0.0
        GOTO 1040
      ELSEIF (Per .EQ. -1.0) THEN
        e2 = -0.25*ALOG(Vs30/1000.0)*ALOG(1.0/0.35)
        GOTO 1040
      ELSEIF ((Per .LT. 0.35) .OR. (Vs30 .GT. 1000.0)) THEN
        e2 = 0.0
      ELSEIF (Per .LE. 2.0) THEN
        e2 = -0.25*ALOG(Vs30/1000.0)*ALOG(Per/0.35)
      ELSE
        e2 = -0.25*ALOG(Vs30/1000.0)*ALOG(2.0/0.35)
      ENDIF

 1040 IF (Per .LT. 2.0) THEN
        a22 = 0.0
      ELSE
        a22 = 0.0625*(Per - 2.0)
      ENDIF

      a21Test = (a10T + bT*nT)*ALOG(V30/MIN(V1,1000.0))
     *  + e2*ALOG((Z10+c2T)/(Z10_med+c2T))

      IF (Vs30 .GE. 1000.0) THEN
        a21 = 0.0
      ELSEIF (a21Test .LT. 0.0) THEN
        a21 = -(a10T + bT*nT)
     *  * ALOG(V30/MIN(V1,1000.0))/ALOG((Z10+c2T)/(Z10_med+c2T))
      ELSE
        a21 = e2
      ENDIF

      IF (Z10 .GE. 200.0) THEN
        f_10 = a21*ALOG((Z10+c2T)/(Z10_med+c2T))
     *    + a22*ALOG(Z10/200.0)
      ELSE
        f_10 = a21*ALOG((Z10+c2T)/(Z10_med+c2T))
      ENDIF

C.....
C.....Value of Ground Motion Parameter
C.....

      Y = EXP(ALOG(Y) + f_5 + f_10)

C.....
C.....CALCULATE ALEATORY UNCERTAINTY
C.....
C.....Partial Derivative of ln f_5 With Respect to ln PGA
C.....

      IF (Vs30 .LT. VlinT) THEN
        Alpha = bT*PGA_1100 * (1.0/(PGA_1100 + cT*(V30/VlinT)**nT)
     *    - 1.0/(PGA_1100 + cT))
      ELSE
        Alpha = 0.0
      ENDIF

C.....
C.....Intra-Event Standard Deviation
C.....

      slnAF = 0.3

C        Estimated Vs30

      IF (Mw .LT. 5.0) THEN  !For PGA
        s0Aest = s1est(23)
      ELSEIF (Mw .LE. 7.0) THEN
        s0Aest = s1est(23) + (s2est(23)-s1est(23))*(Mw-5.0)/2.0
      ELSE
        s0Aest = s2est(23)
      ENDIF

      IF (Mw .LT. 5.0) THEN  !For Y
        s0Yest = s1estT
      ELSEIF (Mw .LE. 7.0) THEN
        s0Yest = s1estT + (s2estT-s1estT)*(Mw-5.0)/2.0
      ELSE
        s0Yest = s2estT
      ENDIF

      sBAest = SQRT(s0Aest**2 - slnAF**2)  !For PGA at base of profile
      sBYest = SQRT(s0Yest**2 - slnAF**2)  !For Y at base of profile

C        Measured Vs30

      IF (Mw .LT. 5.0) THEN  !For PGA
        s0Amea = s1mea(23)
      ELSEIF (Mw .LE. 7.0) THEN
        s0Amea = s1mea(23) + (s2mea(23)-s1mea(23))*(Mw-5.0)/2.0
      ELSE
        s0Amea = s2mea(23)
      ENDIF

      IF (Mw .LT. 5.0) THEN  !For Y
        s0Ymea = s1meaT
      ELSEIF (Mw .LE. 7.0) THEN
        s0Ymea = s1meaT + (s2meaT-s1meaT)*(Mw-5.0)/2.0
      ELSE
        s0Ymea = s2meaT
      ENDIF

      sBAmea = SQRT(s0Amea**2 - slnAF**2)  !For PGA at base of profile
      sBYmea = SQRT(s0Ymea**2 - slnAF**2)  !For Y at base of profile

C.....
C.....Inter-Event Standard Deviation
C.....

      IF (Mw .LT. 5.0) THEN  !For PGA
        tau0A = s3(23)
      ELSEIF (Mw .LE. 7.0) THEN
        tau0A = s3(23) + (s4(23)-s3(23))*(Mw-5.0)/2.0
      ELSE
        tau0A = s4(23)
      ENDIF

      IF (Mw .LT. 5.0) THEN  !For Y
        tau0Y = s3T
      ELSEIF (Mw .LE. 7.0) THEN
        tau0Y = s3T + (s4T-s3T)*(Mw-5.0)/2.0
      ELSE
        tau0Y = s4T
      ENDIF

      tauBA = tau0A  !For PGA at base of profile
      tauBY = tau0Y  !For Y at base of profile

C.....
C.....Standard Deviation of Geometric Mean of ln Y
C.....

      Tau = SQRT(tau0Y**2 + (Alpha**2)*(tauBA**2)
     *  + 2.0*Alpha*rhoT*tauBY*tauBA)

C        Estimated Vs30

      Sigest = SQRT(sBYest**2 + slnAF**2 + (Alpha**2)*(sBAest**2)
     *  + 2.0*Alpha*rhoT*sBYest*sBAest)

      SigTest = SQRT(Sigest**2 + Tau**2)

C        Measured Vs30

      Sigmea = SQRT(sBYmea**2 + slnAF**2 + (Alpha**2)*(sBAmea**2)
     *  + 2.0*Alpha*rhoT*sBYmea*sBAmea)

      SigTmea = SQRT(Sigmea**2 + Tau**2)

      RETURN

      END
      SUBROUTINE BA08_MODEL_sub() 
      
C.....
C.....PURPOSE: Evaluates Boore-Atkinson NGA ground motion prediction equation
C              for a single period
C.....

* Call the setup entry point:
*     call ba08_model_setup()
 
* Call as a subroutine:
*      call ba08_model (Mw,Rjb,U,SS,NS,RS,Vs30,Per,Y,Sigma,Tau_U,
*     :           Sig_TU,Tau_M,Sig_TM)
 
C.....
C.....PARAMETER DEFINITIONS
C.....

C     Mw     = Moment magnitude
C     Rjb    = Closest distance to surface projection of coseismic rupture (km)
C     U      = 1 for Unspecified faulting mechanism, 0 otherwise
C     SS     = 1 for Strike-Slip faulting mechanism
C              (-30 < rake < 30 or T- and P-plunge < 40), 0 otherwise
C     NS     = 1 for Normal and Normal-oblique faulting mechanism
C              (-150 < rake < -30 or P-plunge > 40), 0 otherwise
C     RS     = 1 for Reverse and Reverse-oblique faulting mechanism
C              (30 < rake < 150 or T-plunge > 40), 0 otherwise
C     Vs30   = Average shear-wave velocity in top 30m of site profile (m/sec)
C     Per    = Spectral period of PSA (sec), 0 for PGA, -1 for PGV
C     Y      = Ground motion parameter: PGA and PSA (g), PGV (cm/sec)
C     Sigma  = Intra-event standard deviation of ln Y
C     Tau_U  = Inter-event standard deviation of ln Y for Unspecified faulting mechanism
C     Sig_TU = Total standard deviation of geometric mean of ln Y for Unspecified faulting mechanism
C     Tau_M  = Inter-event standard deviation of ln Y for known faulting mechanism
C     Sig_TM = Total standard deviation of geometric mean of ln Y for known faulting mechanism

C.....MODEL VERSION: Final, February 2008 (Earthquake Spectra, Vol. 24, p. 99-138)
C.....
C.....HISTORY
C       11/20/07 - Written by K. Campbell
C       12/14/07 - Corrected parameter definitions
C       01/04/08 - Corrected e3 coefficient for T = 10 s in BA08_COEFS.TXT
C       08/12/08 - Corrected to estimate pga4nl from PGA (Vs30 = 760 m/sec; erratum)
C                - Updated to Earthquake Spectra Version
C       08/16/08 _ Ken Campbell
*       03/27/09 - Dave Boore's modifications from this date on:
*                  Added entry points so that only need to read the table of
*                  coefficients once; modernize the code to some extent
*       12/15/09 - Moved the subroutine and coefficient file to the folder containing
*                  the driver, and thus simplified the path part of file
*                  specification in the open statement.
!       04/07/10 - Add path for NGA GMPE coefficients
 
      save
      
      integer :: i = 0, nper = 0
      integer :: status


      PARAMETER (npermax=30)
!      PARAMETER (nper=23)
      REAL T(npermax), e1(npermax), e2(npermax), e3(npermax), 
     :     e4(npermax), e5(npermax)
      REAL e6(npermax), e7(npermax), Mh(npermax), c1(npermax), 
     :     c2(npermax), c3(npermax)
      REAL Mref(npermax), Rref(npermax), h(npermax), blin(npermax), 
     :     Vref(npermax)
      REAL b1(npermax), b2(npermax), V1(npermax), V2(npermax), 
     :     a1(npermax)
      REAL pga_low(npermax), a2(npermax), sig(npermax), tauU(npermax), 
     :     sigTU(npermax)
      REAL tauM(npermax), sigTM(npermax), Mw, MhT, MrefT, NS

      character path_nga_gmpe_coeff_files*(*)

      ENTRY BA08_MODEL_SETUP(path_nga_gmpe_coeff_files)
      
C.....
C.....READ MODEL COEFFICIENTS
C.....

      call trim_c(path_nga_gmpe_coeff_files, 
     :            nc_path_nga_gmpe_coeff_files)
      nu_coeffs = 10
      OPEN (nu_coeffs,FILE=path_nga_gmpe_coeff_files(1:
     :      nc_path_nga_gmpe_coeff_files)//'BA08_COEFS.TXT',
     :      status='old')
      nskip = 4  ! may be different for each developer's GMPEs
      call skip(nu_coeffs, nskip)
      readloop: DO 
        i = i + 1
        READ (nu_coeffs,*,IOSTAT=status) 
     :    T(i),e1(i),e2(i),e3(i),e4(i),e5(i),e6(i),e7(i),
     :    Mh(i),c1(i),c2(i),c3(i),Mref(i),Rref(i),h(i),blin(i),Vref(i),
     :    b1(i),b2(i),V1(i),V2(i),a1(i),pga_low(i),a2(i),sig(i),tauU(i),
     :    sigTU(i),tauM(i),sigTM(i)
        if (status /= 0) EXIT
        nper = nper + 1
      END DO readloop
      
      close(nu_coeffs)
!      print *,' in subroutine, nper = ', nper
      
      RETURN



      entry BA08_MODEL(Mw,Rjb,U,SS,NS,RS,Vs30,Per,Y,Sigma,Tau_U,
     :           Sig_TU,Tau_M,Sig_TM)
C.....
C.....DETERMINE WHICH STRONG MOTION PARAMETER TO EVALUATE
C

      DO i = 1, nper
        IF (Per .EQ. T(i)) THEN
          iper = i
          GOTO 1020
        ENDIF
      ENDDO

      print *,' '
      print *, 'In BA08--ERROR: Period ',Per,
     :         ' is not supported; quitting'
      print *,' '
      stop

 1020 e1T      = e1(iper)
      e2T      = e2(iper)
      e3T      = e3(iper)
      e4T      = e4(iper)
      e5T      = e5(iper)
      e6T      = e6(iper)
      e7T      = e7(iper)
      MhT      = Mh(iper)
      c1T      = c1(iper)
      c2T      = c2(iper)
      c3T      = c3(iper)
      MrefT    = Mref(iper)
      RrefT    = Rref(iper)
      hT       = h(iper)
      blinT    = blin(iper)
      VrefT    = Vref(iper)
      b1T      = b1(iper)
      b2T      = b2(iper)
      V1T      = V1(iper)
      V2T      = V2(iper)
      a1T      = a1(iper)
      pga_lowT = pga_low(iper)
      a2T      = a2(iper)
      Sigma    = sig(iper)
      Tau_U    = tauU(iper)
      Sig_TU   = sigTU(iper)
      Tau_M    = tauM(iper)
      Sig_TM   = sigTM(iper)

C.....
C.....CALCULATE ROCK PGA (Per = 0; Vs30 = 760 m/sec)
C.....
C.....Magnitude Term
C.....

      IF (Mw. LE. Mh(22)) THEN
        F_M = e1(22)*U + e2(22)*SS + e3(22)*NS + e4(22)*RS
     *    + e5(22)*(Mw-Mh(22)) + e6(22)*(Mw-Mh(22))**2
      ELSE
        F_M = e1(22)*U + e2(22)*SS + e3(22)*NS + e4(22)*RS
     *    + e7(22)*(Mw-Mh(22))
      ENDIF

C.....
C.....Distance Term
C.....

      R = SQRT(Rjb**2 + h(22)**2)
      F_D = (c1(22) + c2(22)*(Mw-Mref(22)))*ALOG(R/Rref(22))
     *  + c3(22)*(R-Rref(22))

C.....
C.....Linear Site Response Term
C.....

      F_LIN = blin(22)*ALOG(760/Vref(22))

C.....
C.....Value of PGA on Rock
C.....

      pga4nl = EXP(F_M + F_D + F_LIN)

C.....
C.....CALCULATE STRONG MOTION PARAMETER
C.....
C.....Magnitude Term
C.....

      IF (Mw. LE. MhT) THEN
        F_M = e1T*U + e2T*SS + e3T*NS + e4T*RS
     *    + e5T*(Mw-MhT) + e6T*(Mw-MhT)**2
      ELSE
        F_M = e1T*U + e2T*SS + e3T*NS + e4T*RS
     *    + e7T*(Mw-MhT)
      ENDIF

C.....
C.....Distance Term
C.....

      R = SQRT(Rjb**2 + hT**2)
      F_D = (c1T + c2T*(Mw-MrefT))*ALOG(R/RrefT)
     *  + c3T*(R-RrefT)

C.....
C.....Linear Site Response Term
C.....

      F_LIN = blinT*ALOG(Vs30/VrefT)

C.....
C.....Nonlinear Site Response Term
C.....

      IF (Vs30 .LE. V1T) THEN
        bnl = b1T
      ELSEIF (Vs30 .LE. V2T) THEN
        bnl = (b1T-b2T)*ALOG(Vs30/V2T)/ALOG(V1T/V2T) + b2T
      ELSEIF (Vs30 .LT. VrefT) THEN
        bnl = b2T*ALOG(Vs30/VrefT)/ALOG(V2T/VrefT)
      ELSE
        bnl = 0
      ENDIF

      dx = ALOG(a2T/a1T)
      dy = bnl*ALOG(a2T/pga_lowT)
      c = (3.0*dy - bnl*dx)/dx**2
      d = -(2.0*dy - bnl*dx)/dx**3

      IF (pga4nl .LE. a1T) THEN
        F_NL = bnl*ALOG(pga_lowT/0.1)
      ELSEIF (pga4nl .LE. a2T) THEN
        F_NL = bnl*ALOG(pga_lowT/0.1) + c*ALOG(pga4nl/a1T)**2
     *    + d*ALOG(pga4nl/a1T)**3
      ELSE
        F_NL = bnl*ALOG(pga4nl/0.1)
      ENDIF

C.....
C.....Value of Ground Motion Parameter
C.....

      Y = EXP(F_M + F_D + F_LIN + F_NL)

      RETURN


      END
      SUBROUTINE CB08_MODEL_subroutine()
 
C.....
C.....PURPOSE: Evaluates Campbell-Bozorgnia NGA ground motion prediction equation
C              for a single period
C.....

* Call the setup entry point:
*     call CB08_MODEL_SETUP()
 
* Call as a subroutine:
*     call CB08_MODEL (Mw,Rrup,Rjb,Frv,Fnm,Ztor,Dip,Vs30,Z25,Per,
*    :       Y,Sigma,Tau,SigArb,SigT)
 


C.....MODEL VERSION: Final, February 2008 (Earthquake Spectra, Vol. 24, p. 139-171)
C.....
C.....HISTORY
C       11/10/06 - Written by K. Campbell and Y. Bozorgnia
C       12/15/06 - Corrected values of sigc (component-to-component standard deviation)
C       11/17/07 - Updated to Earthquake Spectra version
C                - Modified to read in table of model coefficients
C                - Removed arbitrary horizontal component factor (Kc)
C       08/14/08 - Updated to Earthquake Spectra version
*       03/29/09 - Dave Boore's modifications from this date on:
*                  Added entry points so that only need to read the table of
*                  coefficients once; modernize the code to some extent
*       12/15/09 - Moved the subroutine and coefficient file to the folder containing
*                  the driver, and thus simplified the path part of file
*                  specification in the open statement.
!       04/07/10 - Add path for NGA GMPE coefficients

C.....
C.....PARAMETER DEFINITIONS
C.....

C     Mw     = Moment magnitude
C     Rrup   = Closest distance to coseismic rupture (km)
C     Rjb    = Closest distance to surface projection of coseismic rupture (km)
C     Frv    = 1 for Reverse and Reverse-oblique faulting (30 < rake < 150), 0 otherwise
C     Fnm    = 1 for Normal and Normal-oblique faulting (-150 < rake < -30), 0 otherwise
C     Ztor   = Depth to top of coseismic rupture (km)
C     Dip    = Average dip of rupture plane (degrees)
C     Vs30   = Average shear-wave velocity in top 30m of site profile (m/sec)
C     Z25    = Basin (Sediment) depth; depth to 2.5 km/sec shear-wave velocity horizon (km)
C     Per    = Spectral period of PSA (sec); 0 for PGA, -1 for PGV, -2 for PGD
C     Y      = Ground motion parameter: PGA and PSA (g), PGV (cm/sec), PGD (cm)
C     Sigma  = Intra-event standard deviation of ln Y
C     Tau    = Inter-event standard deviation of ln Y
C     SigArb = Total standard deviation of arbitrary horizontal component of ln Y
C     SigT   = Total standard deviation of geometric mean of ln Y

      save
      
      integer :: i = 0, nper = 0
      integer :: status


      PARAMETER (npermax=30)
!      PARAMETER (nper=24)
      REAL T(npermax), c0(npermax), c1(npermax), c2(npermax), 
     :     c3(npermax), c4(npermax)
      REAL c5(npermax), c6(npermax), c7(npermax), c8(npermax), 
     :     c9(npermax), c10(npermax)
      REAL c11(npermax), c12(npermax), k1(npermax), k2(npermax), 
     :     k3(npermax), c(npermax)
      REAL n(npermax), slnY(npermax), tlnY(npermax), slnAF(npermax), 
     :     sigC(npermax)
      REAL rho(npermax), k1T, k2T, k3T, nT, Mw

      character path_nga_gmpe_coeff_files*(*)

      entry cb08_model_setup(path_nga_gmpe_coeff_files)

C.....
C.....READ MODEL COEFFICIENTS
C.....

      call trim_c(path_nga_gmpe_coeff_files, 
     :            nc_path_nga_gmpe_coeff_files)
      nu_coeffs = 10
      OPEN (nu_coeffs,FILE=path_nga_gmpe_coeff_files(1:
     :      nc_path_nga_gmpe_coeff_files)//'CB08_COEFS.TXT',
     :      status='old')
      nskip = 5  ! may be different for each developer's GMPEs
      call skip(nu_coeffs, nskip)
      readloop: DO 
        i = i + 1
        READ (nu_coeffs,*,IOSTAT=status) 
     :    T(i),c0(i),c1(i),c2(i),c3(i),c4(i),c5(i),c6(i),
     *    c7(i),c8(i),c9(i),c10(i),c11(i),c12(i),k1(i),k2(i), k3(i),
     *    c(i),n(i),slnY(i),tlnY(i),slnAF(i),sigC(i),rho(i)
        if (status /= 0) EXIT
        nper = nper + 1
      END DO readloop
      
      close(nu_coeffs)
!      print *,' in subroutine, nper = ', nper
      
      
      return

      entry CB08_MODEL (Mw,Rrup,Rjb,Frv,Fnm,Ztor,Dip,Vs30,Z25,Per,
     :           Y,Sigma,Tau,SigArb,SigT)

C.....
C.....DETERMINE WHICH STRONG MOTION PARAMETER TO EVALUATE
C.....

      DO i = 1, nper
        IF (Per .EQ. T(i)) THEN
          iper = i
          GOTO 1020
        ENDIF
      ENDDO

      print *,' '
      print *, 'In CB08--ERROR: Period ',Per,
     :         ' is not supported; quitting'
      print *,' '
      stop


 1020 c0T    = c0(iper)
      c1T    = c1(iper)
      c2T    = c2(iper)
      c3T    = c3(iper)
      c4T    = c4(iper)
      c5T    = c5(iper)
      c6T    = c6(iper)
      c7T    = c7(iper)
      c8T    = c8(iper)
      c9T    = c9(iper)
      c10T   = c10(iper)
      c11T   = c11(iper)
      c12T   = c12(iper)
      k1T    = k1(iper)
      k2T    = k2(iper)
      k3T    = k3(iper)
      cT     = c(iper)
      nT     = n(iper)
      slnYT  = slnY(iper)
      tlnYT  = tlnY(iper)
      slnAFT = slnAF(iper)
      sigCT  = sigC(iper)
      rhoT   = rho(iper)

C.....
C.....CALCULATE ROCK PGA (Per = 0; Vs30 = 1100 m/sec)
C.....
C.....Magnitude Term
C.....

      IF (Mw .LE. 5.5) THEN
        f_mag = c0(22) + c1(22)*Mw
      ELSEIF (Mw .LE. 6.5) THEN
        f_mag = c0(22) + c1(22)*Mw + c2(22)*(Mw-5.5)
      ELSE
        f_mag = c0(22) + c1(22)*Mw + c2(22)*(Mw-5.5) + c3(22)*(Mw-6.5)
      ENDIF

C.....
C.....Distance Term
C.....

      R = SQRT(Rrup**2 + c6(22)**2)
      f_dis = (c4(22) + c5(22)*Mw)*ALOG(R)

C.....
C.....Style-of-Faulting (Fault Mechanism) Term
C.....

      IF (Ztor .LT. 1.0) THEN
        f_fltZ = Ztor
      ELSE
        f_fltZ = 1.0
      ENDIF

      f_flt = c7(22)*Frv*f_fltZ + c8(22)*Fnm

C.....
C.....Hanging-Wall Term
C.....

      IF (Rjb .EQ. 0.0) THEN
        f_hngR = 1.0
      ELSEIF (Ztor .LT. 1.0) THEN
        Rmax = MAX(Rrup, SQRT(Rjb**2 + 1.0))
        f_hngR = (Rmax - Rjb)/Rmax
      ELSE
        f_hngR = (Rrup - Rjb)/Rrup
      ENDIF

      IF (Mw .LE. 6.0) THEN
        f_hngM = 0.0
      ELSEIF (Mw .LT. 6.5) THEN
        f_hngM = 2.0*(Mw - 6.0)
      ELSE
        f_hngM = 1.0
      ENDIF

      IF (Ztor .GE. 20.0) THEN
        f_hngZ = 0.0
      ELSE
        f_hngZ = (20.0 - Ztor)/20.0
      ENDIF

      IF (Dip .LE. 70.0) THEN
        f_hngD = 1.0
      ELSE
        f_hngD = (90.0 - Dip)/20.0
      ENDIF

      f_hng = c9(22)*f_hngR*f_hngM*f_hngZ*f_hngD

C.....
C.....Shallow Site Response Term (Vs30 = 1100 m/s)
C.....

      f_site = (c10(22) + k2(22)*n(22))*ALOG(1100.0/k1(22))

C.....
C.....Basin (Sediment) Response Term
C.....

      IF (Z25 .LT. 1.0) THEN
        f_sed = c11(22)*(Z25 - 1.0)
      ELSEIF (Z25 .LE. 3.0) THEN
        f_sed = 0.0
      ELSE
        f_sed = c12(22)*k3(22)*EXP(-0.75)*(1.0 - EXP(-0.25*(Z25 - 3.0)))
      ENDIF

C.....
C.....Value of PGA on Rock
C.....

      A_1100 = EXP(f_mag + f_dis + f_flt + f_hng + f_site + f_sed)

C.....
C.....Value of PGA on Local Site Conditions
C.....

      PGA = EXP(ALOG(A_1100) - f_site)

      IF (Vs30 .LT. k1(22)) THEN
        f_site = c10(22)*ALOG(Vs30/k1(22))
     *    + k2(22)*(ALOG(A_1100 + c(22)*(Vs30/k1(22))**n(22))
     *    - ALOG(A_1100 + c(22)))
      ELSEIF (Vs30 .LT. 1100.0) THEN
        f_site = (c10(22) + k2(22)*n(22))*ALOG(Vs30/k1(22))
      ELSE
        f_site = (c10(22) + k2(22)*n(22))*ALOG(1100.0/k1(22))
      ENDIF

      PGA = EXP(ALOG(PGA) + f_site)

C.....
C.....CALCULATE STRONG MOTION PARAMETER
C.....
C.....Magnitude Term
C.....

      IF (Mw .LE. 5.5) THEN
        f_mag = c0T + c1T*Mw
      ELSEIF (Mw .LE. 6.5) THEN
        f_mag = c0T + c1T*Mw + c2T*(Mw-5.5)
      ELSE
        f_mag = c0T + c1T*Mw + c2T*(Mw-5.5) + c3T*(Mw-6.5)
      ENDIF
      
C.....
C.....Distance Term
C.....

      R = SQRT(Rrup**2 + c6T**2)
      f_dis = (c4T + c5T*Mw)*ALOG(R)

C.....
C.....Style-of-Faulting Term
C.....

      IF (Ztor .LT. 1.0) THEN
        f_fltZ = Ztor
      ELSE
        f_fltZ = 1.0
      ENDIF

      f_flt = c7T*Frv*f_fltZ + c8T*Fnm

C.....
C.....Hanging-Wall Term
C.....

      IF (Rjb .EQ. 0.0) THEN
        f_hngR = 1.0
      ELSEIF (Ztor .LT. 1.0) THEN
        Rmax = MAX(Rrup, SQRT(Rjb**2 + 1.0))
        f_hngR = (Rmax - Rjb)/Rmax
      ELSE
        f_hngR = (Rrup - Rjb)/Rrup
      ENDIF

      IF (Mw .LE. 6.0) THEN
        f_hngM = 0.0
      ELSEIF (Mw .LT. 6.5) THEN
        f_hngM = 2.0*(Mw - 6.0)
      ELSE
        f_hngM = 1.0
      ENDIF

      IF (Ztor .GE. 20.0) THEN
        f_hngZ = 0.0
      ELSE
        f_hngZ = (20.0 - Ztor)/20.0
      ENDIF

      IF (Dip .LE. 70.0) THEN
        f_hngD = 1.0
      ELSE
        f_hngD = (90.0 - Dip)/20.0
      ENDIF

      f_hng = c9T*f_hngR*f_hngM*f_hngZ*f_hngD 

C.....
C.....Shallow Site Response Term
C.....

      IF (Vs30 .LT. k1T) THEN
        f_site = c10T*ALOG(Vs30/k1T)
     *    + k2T*(ALOG(A_1100 + cT*(Vs30/k1T)**nT)
     *    - ALOG(A_1100 + cT))
      ELSEIF (Vs30 .LT. 1100.0) THEN
        f_site = (c10T + k2T*nT)*ALOG(Vs30/k1T)
      ELSE
        f_site = (c10T + k2T*nT)*ALOG(1100.0/k1T)
      ENDIF

C.....

      IF (Z25 .LT. 1.0) THEN
        f_sed = c11T*(Z25 - 1.0)
      ELSEIF (Z25 .LE. 3.0) THEN
        f_sed = 0.0
      ELSE
        f_sed = c12T*k3T*EXP(-0.75)*(1.0 - EXP(-0.25*(Z25 - 3.0)))
      ENDIF

C.....
C.....Calculate Ground Motion Parameter
C.....

      Y = EXP(f_mag + f_dis + f_flt + f_hng + f_site + f_sed)

C.....
C.....Check Whether Y < PGA at Short Periods
C.....

      IF (Per .GE. 0.0 .AND. Per .LE. 0.25 .AND. Y .LT. PGA) Y = PGA

C.....
C.....CALCULATE ALEATORY UNCERTAINTY
C.....
C.....Linearized Relationship Between f_site and ln PGA
C.....

      IF (Vs30 .LT. k1T) THEN
        Alpha = k2T*A_1100*(1.0/(A_1100 + cT*(Vs30/k1T)**nT)
     *    - 1.0/(A_1100 + cT))
      ELSE
        Alpha = 0.0
      ENDIF

C.....
C     Intra-Event Standard Deviation at Base of Site Profile
C.....

      slnPGA = slnY(22)
      tlnPGA = tlnY(22)
      slnYB = SQRT(slnYT**2 - slnAFT**2)
      slnAB = SQRT(slnPGA**2 - slnAFT**2)

C.....
C     Standard Deviation of Geometric Mean of ln Y
C.....

      Sigma  = SQRT(slnYB**2 + slnAFT**2 + Alpha**2*slnAB**2
     *  + 2.0*Alpha*rhoT*slnYB*slnAB)
      Tau    = tlnYT
      SigT = SQRT(Sigma**2 + Tau**2)

C.....
C.....Standard Deviation of Arbitrary Horizontal Component of ln Y
C.....

      SigArb = SQRT(SigT**2 + sigCT**2)

      RETURN
      
      END
C     Last change:  KC   16 Aug 2008   10:52 am
      SUBROUTINE CY08_MODEL_subroutine()
 
C.....
C.....PURPOSE: Evaluates Chiou-Youngs NGA ground motion prediction equation
C              for single period
C.....
* Call the setup entry point:
*     call CY08_MODEL_SETUP()
 
* Call as a subroutine:
*      call CY08_MODEL (Mw,Rrup,Rjb,Rx,Fhw,Dip,Ztor,Frv,Fnm,AS,
*     :           Vs30,Z10,Per,Y,Tau,SigInfer,SigTinfer,SigMeas,
*     :           SigTmeas)
 

C.....MODEL VERSION: Final, February 2008 (Earthquake Spectra, Vol. 24, p. 173-215)
C.....
C.....HISTORY
C       11/23/07 - Written by K. Campbell
C       12/14/07 - Corrected parameter definitions
C       08/12/08 - Updated to Earthquake Spectra version
C                - Added PGV
C                - Corrected sediment depth term to avoid COSH error per Chiou
*       03/29/09 - Dave Boore's modifications from this date on:
*                  Added entry points so that only need to read the table of
*                  coefficients once; modernize the code to some extent
*       12/15/09 - Moved the subroutine and coefficient file to the folder containing
*                  the driver, and thus simplified the path part of file
*                  specification in the open statement.
!       04/07/10 - Add path for NGA GMPE coefficients

C.....
C.....PARAMETER DEFINITIONS
C.....

C     Mw        = Moment magnitude
C     Rrup      = Closest distance to coseismic rupture (km)
C     Rjb       = Closest distance to surface projection of coseismic rupture (km)
C     Rx        = Horizontal distance from top of rupture perpendicular to strike (km)
C     Fhw       = 1 for site on down-dip side of top of rupture, 0 otherwise
C     Frv       = 1 for Reverse and Reverse-oblique faulting (30 < rake < 150), 0 otherwise
C     Fnm       = 1 for Normal faulting (-120 < rake < -60), 0 otherwise
C     Ztor      = Depth to top of coseismic rupture (km)
C     Dip       = Average dip of rupture plane (degrees)
C     W         = Width of rupture plane (not used)
C     Vs30      = Average shear-wave velocity in top 30m of site profile (m/sec)
C     Zsed      = Depth to 1.0 km/sec shear-wave velocity horizon (m)
C     AS        = 1 for aftershock, 0 otherwise
C     Per       = Spectral period of PSA (sec), 0 for PGA, -1 for PGV
C     Y         = Ground motion parameter: PGA and PSA (g), PGV (cm/sec)
C     Tau       = Inter-event standard deviation of ln Y
C     SigInfer  = Intra-event standard deviation of ln Y for inferred Vs30
C     SigTinfer = Total standard deviation of geometric mean of ln Y for inferred Vs30
C     SigMeas   = Intra-event standard deviation of ln Y for Measured Vs30
C     SigTmeas  = Total standard deviation of geometric mean of ln Y for measured Vs30

      save

      integer :: i = 0, nper = 0
      integer :: status


      PARAMETER (npermax=30)
!      PARAMETER (nper=24)
      REAL T(npermax), c2(npermax), c3(npermax), c4(npermax), 
     :     c4a(npermax), crb(npermax)
      REAL chm(npermax), cg3(npermax), c1(npermax), c1a(npermax), 
     :     c1b(npermax)
      REAL cn(npermax), cm(npermax), c5(npermax), c6(npermax), 
     :     c7(npermax), c7a(npermax)
      REAL c9(npermax), c9a(npermax), c10(npermax), cg1(npermax), 
     :     cg2(npermax)
      REAL phi1(npermax), phi2(npermax), phi3(npermax), phi4(npermax), 
     :     phi5(npermax)
      REAL phi6(npermax), phi7(npermax), phi8(npermax), tau1(npermax), 
     :     tau2(npermax)
      REAL sig1(npermax), sig2(npermax), sig3(npermax), sig4(npermax), 
     :     Mw, NL0
     
      character path_nga_gmpe_coeff_files*(*)

      entry cy08_model_setup(path_nga_gmpe_coeff_files)

C.....
C.....READ MODEL COEFFICIENTS
C.....

      call trim_c(path_nga_gmpe_coeff_files, 
     :            nc_path_nga_gmpe_coeff_files)
      nu_coeffs = 10
      OPEN (nu_coeffs,FILE=path_nga_gmpe_coeff_files(1:
     :      nc_path_nga_gmpe_coeff_files)//'CY08_COEFS.TXT',
     :      status='old')
      nskip = 5  ! may be different for each developer's GMPEs
      call skip(nu_coeffs, nskip)
      readloop: DO 
        i = i + 1
        READ (nu_coeffs,*,IOSTAT=status) 
     :    T(i),c2(i),c3(i),c4(i),c4a(i),crb(i),chm(i),cg3(i),
     *    c1(i),c1a(i),c1b(i),cn(i),cm(i),c5(i),c6(i),c7(i),c7a(i),
     *    c9(i),c9a(i),c10(i),cg1(i),cg2(i),phi1(i),phi2(i),phi3(i),
     *    phi4(i),phi5(i),phi6(i),phi7(i),phi8(i),tau1(i),tau2(i),
     *    sig1(i),sig2(i),sig3(i),sig4(i)
        if (status /= 0) EXIT
        nper = nper + 1
      END DO readloop
      
      close(nu_coeffs)
!      print *,' in subroutine, nper = ', nper
      
      RETURN

      entry CY08_MODEL (Mw,Rrup,Rjb,Rx,Fhw,Dip,Ztor,Frv,Fnm,AS,
     :           Vs30,Z10,Per,Y,Tau,SigInfer,SigTinfer,SigMeas,
     :           SigTmeas)

C.....
C.....DETERMINE WHICH STRONG MOTION PARAMETER TO EVALUATE
C.....

      DO i = 1, nper
        IF (Per .EQ. T(i)) THEN
          iper = i
          GOTO 1020
        ENDIF
      ENDDO

      print *,' '
      print *, 'In CY08--ERROR: Period ',Per,
     :         ' is not supported; quitting'
      print *,' '
      stop


 1020 c2T   = c2(iper)
      c3T   = c3(iper)
      c4T   = c4(iper)
      c4aT  = c4a(iper)
      crbT  = crb(iper)
      chmT  = chm(iper)
      cg3T  = cg3(iper)
      c1T   = c1(iper)
      c1aT  = c1a(iper)
      c1bT  = c1b(iper)
      cnT   = cn(iper)
      cmT   = cm(iper)
      c5T   = c5(iper)
      c6T   = c6(iper)
      c7T   = c7(iper)
      c7aT  = c7a(iper)
      c9T   = c9(iper)
      c9aT  = c9a(iper)
      c10T  = c10(iper)
      cg1T  = cg1(iper)
      cg2T  = cg2(iper)
      phi1T = phi1(iper)
      phi2T = phi2(iper)
      phi3T = phi3(iper)
      phi4T = phi4(iper)
      phi5T = phi5(iper)
      phi6T = phi6(iper)
      phi7T = phi7(iper)
      phi8T = phi8(iper)
      tau1T = tau1(iper)
      tau2T = tau2(iper)
      sig1T = sig1(iper)
      sig2T = sig2(iper)
      sig3T = sig3(iper)
      sig4T = sig4(iper)

C.....
C.....CALCULATE ROCK PSA (Vs30 = 1130 m/sec)
C.....
C.....Style-of-Faulting Term
C.....

      f_flt = c1T + (c1aT*Frv + c1bT*Fnm + c7T*(Ztor - 4.0))*(1.0 - AS)
     *  + (c10T + c7aT*(Ztor - 4.0))*AS

C.....
C.....Magnitude Term
C.....

      f_mag = c2T*(Mw - 6.0)
     *  + ((c2T-c3T)/cnT)*ALOG(1.0 + EXP(cnT*(cmT - Mw)))

C.....
C.....Distance Term
C.....

      R = SQRT(Rrup**2 + crbT**2)
      f_dis = c4T*ALOG(Rrup + c5T*COSH(c6T*MAX(Mw-chmT,0.0)))
     *  + (c4aT-c4T)*ALOG(R)
     *  + (cg1T + cg2T/COSH(MAX(Mw-cg3T,0.0)))*Rrup

C.....
C.....Hanging-Wall Term
C.....

      pi = 4.0*ATAN(1.0)
      f_hng = c9T*Fhw*TANH(Rx*(COS(Dip*pi/180.0)**2)/c9aT)
     *     * (1.0 - SQRT(Rjb**2+Ztor**2)/(Rrup+0.001))

C.....
C.....Value of PSA on Rock (Vs30 = 1130 m/sec)
C.....

      Yref = EXP(f_flt + f_mag + f_dis + f_hng)


C.....
C.....CALCULATE STRONG MOTION PARAMETER
C.....
C.....Site Response Term
C.....

      a = phi1T*MIN(ALOG(Vs30/1130.0),0.0)
      b = phi2T*(EXP(phi3T*(MIN(Vs30,1130.0)-360.0)) - EXP(phi3T*770.0))
      c = phi4T

      f_site = a + b*ALOG((Yref+c)/c)

C.....
C.....Sediment Depth Term
C.....

      f_sed = phi5T*(1.0 - 1.0/COSH(phi6T*MAX(Z10-phi7T,0.0)))
     *  + phi8T/COSH(0.15*MIN(MAX(Z10-15.0,0.0),300.0))

C.....
C.....Value of Ground Motion Parameter
C.....

      Y = EXP(ALOG(Yref) + f_site + f_sed)

C.....
C.....CALCULATE ALEATORY UNCERTAINTY
C.....
C.....
C     Standard Deviation of Geometric Mean of ln Y
C.....

      NL0 = b*Yref/(Yref+c)
      Tau = tau1T + ((tau2T-tau1T)/2.0)*(MIN(MAX(Mw,5.0),7.0)-5.0)

C       Inferred Vs30

      Finferred = 1.0
      Fmeasured = 0.0

      SigInfer = (sig1T + ((sig2T-sig1T)/2.0)*(MIN(MAX(Mw,5.0),7.0)-5.0)
     *  + sig4T*AS)*SQRT(sig3T*Finferred + 0.7*Fmeasured + (1.0+NL0)**2)
      SigTinfer = SQRT(((1.0+NL0)**2)*Tau**2 + SigInfer**2)

C       Measured Vs30

      Finferred = 0.0
      Fmeasured = 1.0

      SigMeas = (sig1T + ((sig2T-sig1T)/2.0)*(MIN(MAX(Mw,5.0),7.0)-5.0)
     *  + sig4T*AS)*SQRT(sig3T*Finferred + 0.7*Fmeasured + (1.0+NL0)**2)
      SigTmeas = SQRT(((1.0+NL0)**2)*Tau**2 + SigMeas**2)
      
      return

      END

! --------------------------- BEGIN GET_LUN ----------------
      subroutine get_lun(lun)

* Finds a logical unit number not in use; returns
* -1 if it cannot find one.

* Dates -- 05/19/98 - Written by D. Boore, following
*                     Larry Baker's suggestion

      logical isopen
      do i = 99,10,-1
        inquire (unit=i, opened=isopen)
        if(.not.isopen) then
          lun = i
          return
        end if
      end do
      lun = -1

      return
      end
! --------------------------- END GET_LUN ----------------
     
! ------------------------------------------------------------------ skipcmnt
      subroutine skipcmnt(nu, comment, ncomments)

* Skip text comments in the file attached to unit nu, but save skipped 
* comments in character array comment.  Skip at least one line, and more as 
* long as the lines are preceded by "|" or "!".

* Dates: 04/16/01 - Written by D. Boore
*        12/07/01 - Added check for eof
*        11/04/03 - Use trim_c to trim possible leading blank
*        02/03/07 - Initialize comments to blank

      character comment(*)*(*), buf*80

      ncomments = 0
100   buf = ' '
      read (nu,'(a)',end=999) buf
      call trim_c(buf,nc_buf)
      if (buf(1:1) .eq.'!' .or. buf(1:1) .eq.'|' .or. 
     :                     ncomments + 1 .eq. 1) then
        ncomments = ncomments + 1
        comment(ncomments) = ' '
        comment(ncomments) = buf(1:nc_buf)
        goto 100
      else 
        backspace nu
      end if

999   continue
 
      return
      end
! ------------------------------------------------------------------ skipcmnt
! ---------------------- BEGIN SKIP -------------------
      subroutine SKIP(lunit, nlines)
        if (nlines .lt. 1) then
          return
        else
          do i = 1, nlines
             read(lunit, *)
          end do
          return
        end if
      end
! ---------------------- END SKIP -------------------
! --------------------- BEGIN UPSTR ----------------------------------
      Subroutine UPSTR ( text )
* Converts character string in TEXT to uppercase
* Dates: 03/12/96 - Written by Larry Baker

C
      Implicit   None
C
      Character  text*(*)
C
      Integer    j
      Character  ch
C
      Do 1000 j = 1,LEN(text)
         ch = text(j:j)
         If ( LGE(ch,'a') .and. LLE(ch,'z') ) Then
            text(j:j) = CHAR ( ICHAR(ch) - ICHAR('a') + ICHAR('A') )
         End If
 1000    Continue
C
      Return
      End
! --------------------- END UPSTR ----------------------------------
! --------------------------- BEGIN TRIM_C -----------------------
      subroutine trim_c(cstr, nchar)

* strips leading and trailing blanks from cstr, returning the
* result in cstr, which is now nchar characters in length

* Strip off tabs also.

* Here is a sample use in constructing a column header, filled out with 
* periods:

** Read idtag:
*        idtag = ' '
*        read(nu_in, '(1x,a)') idtag
*        call trim_c(idtag, nc_id)
** Set up the column headings:
*        colhead = ' '
*        colhead = idtag(1:nc_id)//'......' ! nc_id + 6 > length of colhead

* Dates: 12/23/97 - written by D. Boore
*        12/08/00 - pad with trailing blanks.  Otherwise some comparisons
*                   of the trimmed character string with other strings
*                   can be in error because the original characters are left
*                   behind after shifting.  For example, here is a string
*                   before and after shifting, using the old version:
*                      col:12345
*                           MTWH  before
*                          MTWHH  after (but nc = 4).
*        03/21/01 - Check for a zero length input string
*        11/09/01 - Change check for zero length string to check for all blanks
*        10/19/09 - Strip off tabs

      character cstr*(*)

      if(cstr .eq. ' ') then
        nchar = 0
        return
      end if

      nend = len(cstr)

! Replace tabs with blanks:

      do i = 1, nend
        if(ichar(cstr(i:i)) .eq. 9) then
           cstr(i:i) = ' '
        end if
      end do



*      if(nend .eq. 0) then
*        nchar = 0
*        return
*      end if

      do i = nend, 1, -1
        if (cstr(i:i) .ne. ' ') then
           nchar2 = i
           goto 10
        end if
      end do

10    continue

      do j = 1, nchar2
        if (cstr(j:j) .ne. ' ') then
          nchar1 = j
          goto 20
        end if
      end do

20    continue
   
      nchar = nchar2 - nchar1 + 1
      cstr(1:nchar) = cstr(nchar1: nchar2)
      if (nchar .lt. nend) then
        do i = nchar+1, nend
          cstr(i:i) = ' '
        end do
      end if

      return
      end
! --------------------------- END TRIM_C -----------------------
! begin subroutine interpolate
      subroutine interpolate(y1, y2, x1, x2, x, y)
      
* Dates: 01/12/10 - Written by D. Boore

      real y1, y2, x1, x2, x, y, slope

      slope = (y2 - y1)/(x2-x1)
      y  = y1 + slope*(x - x1)
      
      return
      end
! end subroutine interpolate
      
      subroutine lin_interp(x, y, n, j, x_intrp, y_intrp)
      
* Computes linearly interpolated value of y

* Values out of range are assigned end values

* Dates: 03/16/05 - Written by D. Boore
*        07/24/05 - Added index j for end cases

      real x(*), y(*), slope, x_intrp, y_intrp
      integer j, n
      
      if (x_intrp .le. x(1)) then
        j = 1
        y_intrp = y(1)
        return
      end if
      
      if (x_intrp .ge. x(n)) then
        j = n
        y_intrp = y(n)
        return
      end if          
      
      call locate(x,n,x_intrp,j)
      
      slope = (y(j+1) - y(j))/(x(j+1)-x(j))
      y_intrp = y(j) + slope*(x_intrp - x(j))
      
      return
      end
      


!* --------------------- BEGIN LOCATE -----------------
      SUBROUTINE locate(xx,n,x,j)
      
* Comments added by D. Boore on 26feb2010:
*  finds j such that xx(j) < x <= xx(j+1)
*  EXCEPT if x = xx(1), then j = 1 (logically it would be 0 from
*  the above relation, but this is the same returned value of j
*  for a point out of range).
*  Also, if x = xx(n), j = n-1, which is OK
*  Note that j = 0 or j = n indicates that x is out of range.
*
* See the program test_locate.for to test this routine.

      INTEGER j,n
      REAL x,xx(n)
      INTEGER jl,jm,ju
      jl=0
      ju=n+1
10    if(ju-jl.gt.1)then
        jm=(ju+jl)/2
        if((xx(n).ge.xx(1)).eqv.(x.ge.xx(jm)))then
          jl=jm
        else
          ju=jm
        endif
      goto 10
      endif
      if(x.eq.xx(1))then
        j=1
      else if(x.eq.xx(n))then
        j=n-1
      else
        j=jl
      endif
      return
      END
!* --------------------- END LOCATE -----------------

      subroutine rjb2rrup(fault_type, m, rjb, rrup, 
     :             path_rjb2rrup_coeff_files)
     
* Computed mean rrup given fault_type (GEN, SS, SHD), magnitude, and R_JB,
* Using Scherbaum et al. (2004) equations. (Note: "SHD" stands for "SHallow Dipping")

* Dates: 09/07/09 - Written by D. Boore
*        12/23/09 - Close nu_coeff
!        04/07/10 - Add path to folder containing the
!                   coefficient files.
!        04/18/10 - Suspend m out of range check for now.
!        06/02/10 - Comment out print f_coeff

      character fault_type*10, f_coeff*150
      character path_rjb2rrup_coeff_files*(*)
      
      real coeff(4,5)  ! columns give distance dependence.
      real m, rjb, rrup
      real d_vector(4), m_vector(5)
      
      call trim_c(fault_type, nc_fault_type)
      
      call upstr(fault_type(1:nc_fault_type))
      
      call trim_c(path_rjb2rrup_coeff_files, 
     :        nc_path_rjb2rrup_coeff_files)
      
!rjb2rrup_gen_m_5_6.75.txt
!rjb2rrup_gen_m_6.75_7.5.txt
!rjb2rrup_shd_m_5_6.75.txt
!rjb2rrup_shd_m_6.75_7.5.txt
!rjb2rrup_ss_m_5_6.75.txt
!rjb2rrup_ss_m_6.75_7.5.txt

!      if (m < 5.0) then
!        print *,' m out of range, QUITTING!'
!        stop
!      else if (m > 7.5) then
!        print *,' m out of range, QUITTING!'
!        stop
!      else if (m <= 6.75) then
       if (m <= 6.75) then
        f_coeff = ' '
        if (fault_type(1:3) .eq. 'GEN') then
          f_coeff = path_rjb2rrup_coeff_files(1:
     :     nc_path_rjb2rrup_coeff_files)//'rjb2rrup_gen_m_5_6.75.txt'
        else if (fault_type(1:3) .eq. 'SHD') then
          f_coeff = path_rjb2rrup_coeff_files(1:
     :     nc_path_rjb2rrup_coeff_files)//'rjb2rrup_shd_m_5_6.75.txt'
        else if (fault_type(1:2) .eq. 'SS') then
          f_coeff = path_rjb2rrup_coeff_files(1:
     :     nc_path_rjb2rrup_coeff_files)//'rjb2rrup_ss_m_5_6.75.txt'
        else
          print *,' Invalid fault type ('//fault_type(1:nc_fault_type)//
     :          ') QUITTING!'
          stop
        end if
      else
        f_coeff = ' '
        if (fault_type(1:3) .eq. 'GEN') then
          f_coeff = path_rjb2rrup_coeff_files(1:
     :     nc_path_rjb2rrup_coeff_files)//'rjb2rrup_gen_m_6.75_7.5.txt'
        else if (fault_type(1:3) .eq. 'SHD') then
          f_coeff = path_rjb2rrup_coeff_files(1:
     :     nc_path_rjb2rrup_coeff_files)//'rjb2rrup_shd_m_6.75_7.5.txt'
        else if (fault_type(1:2) .eq. 'SS') then
          f_coeff = path_rjb2rrup_coeff_files(1:
     :     nc_path_rjb2rrup_coeff_files)//'rjb2rrup_ss_m_6.75_7.5.txt'
        else
          print *,' Invalid fault type ('//fault_type(1:nc_fault_type)//
     :          ') QUITTING!'
          stop
        end if
      end if
      
      call trim_c(f_coeff, nc_f_coeff)
      
!      print *,' f_coeff: ', f_coeff(1:nc_f_coeff)
      
        
      call get_lun(nu_coeff)
      open(unit=nu_coeff,file=f_coeff(1:nc_f_coeff),
     :     status='unknown')
     
      call skip(nu_coeff,1)
      
      nrows = 4
      ncols = 5
      do i = 1, nrows
        read(nu_coeff,*) (coeff(i,j), j = 1, ncols)
      end do
      
      close(nu_coeff)
      
      do i = 1, nrows
        d_vector(i) = rjb**float(i-1)
      end do
      
      do j = 1, ncols
        m_vector(j) = m**float(j-1)
      end do
      
      sum_row  = 0.0
      do i = 1, nrows
        sum_col = 0.0
        do j = 1, ncols
          sum_col = sum_col + coeff(i,j)*m**float(j-1)
        end do
        sum_row = sum_row + sum_col*rjb**float(i-1)
      end do
      
      rrup = rjb+ sum_row
      
      return
      end

      
      
      subroutine rx_calc_sub(rx, rjb, ztor, w, dip, azimuth, rrup)
      
!# For details on these derived equations, please see the following paper:
!# Kaklamanos, J., and L. G. Baise (2010).  Relationships between Distance
!# Measures in Recent Ground Motion Prediction Equations, Seismological
!# Research Letters (in review).
!# The equation numbers and figures in this code refer to the equation numbers
!# and figures in Kaklamanos and Baise (2010).

! Dates: 04/11/10 - Written by D. Boore, based on J. Kaklamanos's R program 
!        04/28/10 - Minor change, as per Jim's 28 April 2010 email.
!        05/07/10 - trap case of dip=90, Rjb=0 (as per Jim Kaklamanos's
!                   suggestion in NGA R Package - Report 2.pdf).

! Necessary trigonometric functions for Rx calculations
!csc <- function(x) {1/sin(x)}
!sec <- function(x) {1/cos(x)}
!cot <- function(x) {1/tan(x)}

      pi = 4.0*atan(1.)
      d2r = pi/180.0
      
      d = d2r*dip
      a = d2r*azimuth
      
! check for valid azimuth:
      if (abs(azimuth) > 180.0) then
        write(*,*) ' Invalid azimuth (= ', azimuth, 
     :             ') for this call to rx_calc; QUITTING!'
        stop
      end if
      
      if (azimuth < 0.0) then  ! footwall wall, Cases 1, 4, and 7 (Eqn 8)
        Rx = Rjb*sin(a) 
        return
      end if
 
      if (Rjb == 0.0 .and. dip == 90.0) then
        Rx = 0.0
        return
      end if
      
      if (azimuth == 90.0 .or. Rjb == 0.0) then   ! modified on 28 April 2010
       
        if (Rjb > 0.0) then              ! Case 6 in Figure 3 (Eqn 5)
          Rx = Rjb + W*cos(d)
          return
        end if
        
        if (Rrup >= 0.0) then                     ! If Rrup is known...
          if (Rrup < Ztor/cos(d)) then           ! Case 5A in Figure 3 (Eqn 6)
            Rx = sqrt(Rrup**2 - Ztor**2)
            return
          else                                  ! Case 5B (Eqn 7)
            Rx = Rrup/sin(d) - Ztor/tan(d)
            return
          end if
         ! If Rrup is unknown, assume that the site is located at
         ! the center of the surface projection of the ruptured area
        else
          Rx = W*cos(d)/2.0
          return
        end if  
        
      end if
      
      if (azimuth /= 90.0) then
        
        ! Cases 2 and 8 (Eqn 3)
        if(Rjb*abs(tan(a)) <= W*cos(d)) then
          Rx = Rjb*abs(tan(a))
          return

        ! Cases 3 and 9 (Eqn 4)
        else
          Rx = Rjb*tan(a)*cos(a - asin(W*cos(d)*cos(a)/Rjb))
          return
        end if
      
      end if
        
      end
      
      

      subroutine rrup_calc_sub(rrup, rjb, rx, ztor, w, dip, azimuth)

!# For details on these derived equations, please see the following paper:
!# Kaklamanos, J., and L. G. Baise (2010).  Relationships between Distance
!# Measures in Recent Ground Motion Prediction Equations, Seismological
!# Research Letters (in review).
!# The equation numbers and figures in this code refer to the equation numbers
!# and figures in Kaklamanos and Baise (2010).

! Dates: 04/11/10 - Written by D. Boore, based on J. Kaklamanos's R program 

!# Function for Rupture Distance, Rrup
 
      pi = 4.0*atan(1.)
      d2r = pi/180.0
      
      d = d2r*dip
      a = d2r*azimuth
      
! check for valid azimuth:
      if (abs(azimuth) > 180.0) then
        write(*,*) ' Invalid azimuth (= ', azimuth, 
     :             ') for this call to rx_calc; QUITTING!'
        stop
      end if
      
  ! Calculate Rrup'
      if (dip /= 90.0) then
      ! Zone A in Figure 5 (Eqn 10)
        if (Rx < Ztor*tan(d)) then
          Rrup_prime = sqrt(Rx**2 + Ztor**2)
      ! Zone B (Eqn 11)
        else if (Rx >= Ztor*tan(d) .and. 
     :           Rx <= Ztor*tan(d) + W/cos(d)) then
          Rrup_prime = Rx*sin(d) + Ztor*cos(d)
      ! Zone C (Eqn 12)
        else 
          Rrup_prime = sqrt((Rx - W*cos(d))**2 + 
     :                      (Ztor + W*sin(d))**2)
        end if  
      else  ! Eqn 16
        Rrup_prime = sqrt(Rx**2 + Ztor**2)
      end if


  ! Calculate Ry

  ! Eqn 13
      if(abs(azimuth) == 90.0) then
        Ry = 0.0
  ! Eqn 14
      else if (azimuth == 0.0 .or. abs(azimuth) == 180.0) then
        Ry = Rjb
  ! Eqn 15  
      else 
        Ry = abs(Rx/tan(a))
      end if
 
  ! Calculate Rrup (Eqn 9)
      Rrup = sqrt(Rrup_prime**2 + Ry**2)
  
      return
      end
 


      subroutine get_nga_gm(
     :     developer, per,nper,indx_permin,indx_permax,
     :     M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv, Fnm, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0, Zsed2p5_km,
     :     T, Y, 
     :     Sig1, Sig2, Tau1, Tau2, SigT1, SigT2,
     :     ynull, absrake_gt_180
     :                                             )
     
!NOTE: Because interpolation requires two evaluations of the GMPEs,
!  I've made the evaluations into a separate subprogram.

!Developer      Sig1     Sig2    Tau1    Tau2      SigT1     SigT2
!     AS08    SigEst  SigMeas     Tau     -     SigT_Est SigT_Meas
!     BA08     Sigma      -     Tau_U   Tau_M   SigT_U      SigT_M
!     CB08     Sigma      -       Tau     -     SigT_Arb   SigT_GM
!     CY08  SigInfer  SigMeas     Tau     -   SigT_Infer SigT_Meas

! Dates: 04/26/10 - Written by D. Boore, based on ba_gm_tmr
!        05/01/10 - Added indx_permin
!        08/06/10 - Added ynull to trap for unspecified fault type

      implicit none
      
      real M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv, Fnm, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0, Zsed2p5_km,
     :     T, Y, 
     :     Sig1, Sig2, Tau1, Tau2, SigT1, SigT2
     
      real Tb, Yb, Sig1b, Sig2b, Tau1b, Tau2b, SigT1b, SigT2b 
      real Te, Ye, Sig1e, Sig2e, Tau1e, Tau2e, SigT1e, SigT2e, alogy
      
      real ynull
     
      real per(*)
      integer nper, indx_permin, indx_permax

      character developer*4
      character y_type*10 
      
      integer nc_buf
      
      logical absrake_gt_180

      call upstr(developer)
      
! Special consideration for abs(rake) > 180  

      if (absrake_gt_180 .and. developer(1:4) /= 'BA08') then
      
        Y = ynull
        Sig1 = ynull
        Sig2 = ynull
        Tau1 = ynull
        Tau2 = ynull
        SigT1 = ynull
        SigT2 = ynull
        
        return
        
      end if
            
        
      
        call get_y_type(T, y_type)

        SELECT CASE (y_type)        
        
        CASE ('PGVorPGA')
C          write(*,*) 'Case PGVorPGA'

          CALL evaluate_nga_gmpes(
     :     developer, 
     :     M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv, Fnm, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0, Zsed2p5_km,
     :     T, Y, 
     :     Sig1, Sig2, Tau1, Tau2, SigT1, SigT2
     :                                             )

        CASE ('PSA')
        
C          write(*,*) 'Case PSA'

* Trap for per outside the range of the tabulated periods (but only if not pga or pgv):

          call trap_per_outside_range(t,per,nper,
     :                                indx_permin,indx_permax)

          call get_period_interval(t, per, nper, tb, te)

          CALL evaluate_nga_gmpes(
     :     developer, 
     :     M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv, Fnm, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0, Zsed2p5_km,
     :     Tb, Yb, 
     :     Sig1b, Sig2b, Tau1b, Tau2b, SigT1b, SigT2b
     :                                             )
     
          CALL evaluate_nga_gmpes(
     :     developer, 
     :     M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv, Fnm, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0, Zsed2p5_km,
     :     Te, Ye, 
     :     Sig1e, Sig2e, Tau1e, Tau2e, SigT1e, SigT2e
     :                                             )
     
* Note: y is not in log units, but sigma is.  The interpolation
* is done in log space.

          call interpolate(alog(yb), alog(ye), 
     :                     alog(tb), alog(te), 
     :                     alog(t),  alogy)
          y  = exp(alogy)
          
          call interpolate(Sig1b, Sig1e,  
     :                     alog(tb), alog(te), 
     :                     alog(t), Sig1)
          call interpolate(Sig2b, Sig2e,  
     :                     alog(tb), alog(te), 
     :                     alog(t), Sig2)
          call interpolate(Tau1b, Tau1e,  
     :                     alog(tb), alog(te), 
     :                     alog(t), Tau1)
          call interpolate(Tau2b, Tau2e,  
     :                     alog(tb), alog(te), 
     :                     alog(t), Tau2)
          call interpolate(SigT1b, SigT1e,  
     :                     alog(tb), alog(te), 
     :                     alog(t), SigT1)
          call interpolate(SigT2b, SigT2e,  
     :                     alog(tb), alog(te), 
     :                     alog(t), SigT2)
  

        CASE DEFAULT
        
          PRINT *, ' In get_nga_gm: Neither PGVorPGA'//
     :             ' or PSA were selected; '//
     :              'something is wrong; QUITTING'
          STOP

        END SELECT

      RETURN
      END

 


        subroutine evaluate_nga_gmpes(
     :     developer, 
     :     M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv, Fnm, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0, Zsed2p5_km,
     :     T, Y, 
     :     Sig1, Sig2, Tau1, Tau2, SigT1, SigT2
     :                                             )


!Developer      Sig1     Sig2    Tau1    Tau2      SigT1     SigT2
!     AS08    SigEst  SigMeas     Tau     -     SigT_Est SigT_Meas
!     BA08     Sigma      -     Tau_U   Tau_M   SigT_U      SigT_M
!     CB08     Sigma      -       Tau     -     SigT_Arb   SigT_GM
!     CY08  SigInfer  SigMeas     Tau     -   SigT_Infer SigT_Meas

! Dates: 04/26/10 - Written by D. Boore

      IMPLICIT none
      
      real M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv, Fnm, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0, Zsed2p5_km,
     :     T, Y, 
     :     Sig1, Sig2, Tau1, Tau2, SigT1, SigT2

      real abs_Rx, 
     :     SigTmea_as08, SigTest_as08, Tau_as08,  
     :     Sigmea_as08, Sigest_as08, Y_as08, 
     :     Sig_TM_ba08, Tau_M_ba08, Sig_TU_ba08, Tau_U_ba08, 
     :     Sigma_ba08, Y_ba08, 
     :     SigT_cb08, SigmaArb_cb08, Tau_cb08,
     :     Sigma_cb08, Y_cb08, 
     :     SigTmeas_cy08, SigMeas_cy08, SigTinfer_cy08, 
     :     SigInfer_cy08, Tau_cy08, Y_cy08 
     
      character developer*4
      
      CALL upstr(developer)
      
      IF (developer == 'AS08') THEN
      
          abs_Rx = abs(Rx)

          CALL AS08_MODEL (M,Rrup,Rjb,abs_Rx,Frv,
     :     Fnm,Fhw,AS,Ztor,Dip,W,Vs30,
     :     Zsed1p0,T,Y_as08,
     :     Sigest_as08,Sigmea_as08,Tau_as08,SigTest_as08,SigTmea_as08)
          Y     = Y_as08
          Sig1  = Sigest_as08
          Sig2  = Sigmea_as08
          Tau1  = Tau_as08
          Tau2  = -9.99
          SigT1 = SigTest_as08
          SigT2 = SigTmea_as08

      ELSE IF (developer == 'BA08') THEN
      
          IF (as == 1) THEN  !GMPEs not defined for aftershocks
          
            Y     = -9.99
            Sig1  = -9.99
            Sig2  = -9.99
            Tau1  = -9.99
            Tau2  = -9.99
            SigT1 = -9.99
            SigT2 = -9.99
            
          ELSE

            CALL BA08_MODEL (M,Rjb,U,SS,NS,RS,Vs30,T, Y_ba08, 
     :      Sigma_ba08,Tau_U_ba08,Sig_TU_ba08,Tau_M_ba08,Sig_TM_ba08)
            Y     = Y_ba08
            Sig1  = Sigma_ba08
            Sig2  = -9.99
            Tau1  = Tau_U_ba08
            Tau2  = Tau_M_ba08
            SigT1 = Sig_TU_ba08
            SigT2 = Sig_TM_ba08
            
          END IF
     
      ELSE IF (developer == 'CB08') THEN
      
          IF (as == 1) THEN  !GMPEs not defined for aftershocks
          
            Y     = -9.99
            Sig1  = -9.99
            Sig2  = -9.99
            Tau1  = -9.99
            Tau2  = -9.99
            SigT1 = -9.99
            SigT2 = -9.99
            
          ELSE

            CALL CB08_MODEL (M,Rrup,Rjb,Frv,Fnm,
     :             Ztor,Dip,Vs30,Zsed2p5_km,T,Y_cb08,
     :             Sigma_cb08, Tau_cb08,SigmaArb_cb08,SigT_cb08)
            Y     = Y_cb08
            Sig1  = Sigma_cb08
            Sig2  = -9.99
            Tau1  = Tau_cb08
            Tau2  = -9.99
            SigT1 = SigmaArb_cb08
            SigT2 = SigT_cb08

          END IF

      ELSE IF (developer == 'CY08') THEN

          CALL CY08_MODEL (
     :    M,Rrup,Rjb,Rx,Fhw,Dip,Ztor,Frv,Fnm,AS,Vs30,Zsed1p0,T,
     :    Y_cy08,
     :    Tau_cy08,SigInfer_cy08,SigTinfer_cy08,SigMeas_cy08,
     :    SigTmeas_cy08)
     
          Y     = Y_cy08
          Sig1  = SigInfer_cy08
          Sig2  = SigMeas_cy08
          Tau1  = Tau_cy08
          Tau2  = -9.99
          SigT1 = SigTinfer_cy08
          SigT2 = SigTmeas_cy08

      ELSE
      
         write(*,*) ' ERROR: developer = '//developer//
     :              '; not valid; QUITTING!!!'
     
      END IF
      
      RETURN
      END
