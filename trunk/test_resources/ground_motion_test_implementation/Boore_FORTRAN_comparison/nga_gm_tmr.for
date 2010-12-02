      Program nga_gm_tmr
      
* Computes NGA motions

*! Control file for program nga_gm_tmr.for
*! Revision of program involving a change in the control file on this date:
*   09/09/10
*!Header to add to output file (no "!" at beginning; 
*! "[blank]" means that no header is printed!)
* [blank]
*!name of path in which these coefficient files are stored:
*!                     AS08_COEFS.TXT
*!                     BA08_COEFS.TXT
*!                     CB08_COEFS.TXT
*!                     CY08_COEFS.TXT
*! ** DO NOT FORGET CLOSING "\" IN PATH **
*   C:\gm_predictions\working\
*!name of path in which these coefficient files for rjb2rrup are stored:
*!                     rjb2rrup_gen_m_5_6.75.txt
*!                     rjb2rrup_gen_m_6.75_7.5.txt
*!                     rjb2rrup_shd_m_5_6.75.txt
*!                     rjb2rrup_shd_m_6.75_7.5.txt
*!                     rjb2rrup_ss_m_5_6.75.txt
*!                     rjb2rrup_ss_m_6.75_7.5.txt
*! ** DO NOT FORGET CLOSING "\" IN PATH **
*   C:\gm_predictions\working\
*!name of output file:
*!   hanging_wall_example_m7_vs30_760_test4.out
*   check_tuna_onur_plot_t0.2.test3.out
*!PSA, PGA values in cm/s/s (gals)? (Y,N):
*! Note: N = units in g:
* N
*! available periods for BA08:  -1.0 0.0 0.01 0.02 0.03 0.05 0.075 0.1 0.15 0.2 0.25 0.3 0.4 0.5 0.75 1 1.5 2 3 4 5 7.5 10
*! force the program to derive Ztor from RHyp and Wells and Coppersmith W by setting Ztor<0.0
*! If dip < 0, the program uses generic values of 90 for SS, 55 for N, 40 for r (after CY08)
*! abs(rake) > 180.0 will result in motion for an undefined fault type for BA08 and null values for the other GMPEs
*! Note: Fhw=1 for hw; Rjb, Rrup, Rx, Zhyp, Ztor in km; Vs30 in m/s; Zsed1.0, Zsed2.5 in m (CB use km for Zsed2.5, but the NGA flatfile uses m).
*!
*! Undefined values (values will be assigned, unless pairs of values are 
*! inconsistent, as noted below): 
*!                 Fhw < 0; 
*!             abs(az)>180; 
*!                  rrup<0; 
*!                  zhyp<0; 
*!              dip<0; w<0; 
*!                  ztor<0; 
*!           Zsed1p0as08<0; 
*!               Zsed2p5<0
*!
*! Inconsistent values (program will stop): 
*!       Fhw < 0.0 .and. abs(az) > 180.0; 
*!       Fhw == 0.0 .and. 0<=az<=180;
*!       Fhw == 1.0 .and. -180<az<0
*!
*!       Rx is computed from provided information, rather than being an input parameter.
*!
*! Minimum required input parameters:
*!
*!       T
*!       M
*!       Rjb
*!       Fhw or az
*!       rake (0.0, 90.0, -90.0 for SS, RS, NS)
*!       Vs30
*!
*!T      M  Fhw   Az  Rjb(km) Rrup(km) Zhyp(km) rake Dip W(km) Ztor(km) V30(m/s) Zsed1p0(m) Zsed2p5(m) as(1=aftershock)
*0.2	6    0 -400	1	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	1.2	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	1.4	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	1.6	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	1.8	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	2	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	3	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	4	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	5	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	6	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	7	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	8	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400	9	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400    10	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400    20	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
*0.2	6    0 -400   100	-1	-5.00	90  -45	-21.2      -10      760      -1.0	-1.0	0
* stop

* Generic dips (from CY08, p. 175):  SS = 90, RS = 40, NS = 55.

* Dates: 07/29/09 - Written by D.M. Boore, based on ab06_gm_vs_r.
*        10/27/09 - Compute Zsed1.0, Zsed2.5 in program if negative values are provided.
*                   For CB08, include Y for Z2.5 using AS and CY estimates of Z1.0
*        11/05/09 - Assign Fhw based on sign of Rx.
*                 - Add Zhyp as an independent parameter (to compute Ztor if Ztor <0.0)
*        11/08/09 - If Rrup < 0, use the Scherbaum et al (2004) median relations
*        11/11/09 - I declared "NS" real.  I should use implicit none to avoid
*                   this type of error.
*        12/15/09 - I placed the NGA subroutines and coefficient files in the same folder
*                   as the main program (and thus simplified the path specification
*                   used before in the include and open statements).
*        01/12/10 - Modify so can compute PSA for periods for which coefficients are not provided.
*                   Rather than change the subroutines (which might lead to confusion on my part),
*                   I decided to call them as needed, making the driver messier, with lots of repeated
*                   code.  But the upside is that it may be easier to debug the program,
*                   and the calculations are so fast that code efficiency is not an issue.  This requires
*                   reading a file of periods for which coefficients are available for each
*                   NGA relation.
*        01/19/10 - Specified path in open nga_periods.txt. 
!        04/07/10 - Read in paths for the NGA GMPE and the rjb2rrup coefficients files.
!        04/08/10 - Hardwire NGA periods, rather than read them from a file.
!                 - Use more precise relations between rake angle and FRV and FNM (see 
!                   C:\nga_gmpes_r_fortran_ofr\Kaklamanos-Thompson nga v0.3 in R\
!                   dmb_answers_to_queries_re_fortran_code.doc).  The changes were also
!                   made in using rjb2rrup, in determining fault width if unspecified,
!                   and in assigning dip from the rake angle.
!                   Note that terminology
!                   "WITHIN (caps added) 30 degrees of horizontal" as being a strikeslip event can be
!                   taken to mean abs(rake<30 and abs(rake>150.  Similarly,
!                   Boore and Atkinson (2008) use this wording: "rakes angles within 30° of 
!                   horizontal are strikeslip, angles from 30° to 150° are reverse, and 
!                   angles from -30° to -150° are normal".  This can be interpreted to mean
!                   a reverse slip event is defined by 30<= rake <= 150, for example.
!        04/10/10 - Remove restriction on W for the AS08 evaluation, as per email from Ken Campbell
!                   today.
!        04/11/10 - Use Scherbaum et al (BSSA 94, 1053) Table 1 to determine Zhyp if unspecified.
!                 - Add Fhw and az to input, and compute Rx and Rrup as needed.
!        04/19/10 - set Zsed1p0_AS08 to Zsed1p0 if Zsed1p0 >= 0.0 outside of AS08 block, because
!                   Zsed1p0_AS08 can be used in the CB08 block and in the previous version of
!                   the program it would not be defined if Zsed1p0_in >= 0.0.
!        04/27/10 - Place calls to subroutines to evaluate GMPEs for each developer into a subroutine.
!        04/30/10 - Place code in main program into subroutines to improve readibility.
!        05/01/10 - Removed Rx as an input parameter.
!        05/07/10 - Added check to ensure that az = +-90 for Rjb = 0 (as per Jim Kaklamanos's
!                   suggestion in NGA R Package - Report 2.pdf).  In addition, require Fhw=1
!                   when Rjb = 0.0.
!        09/09/10 - Add option of PSA, PGA units being g or cm/s/s
    
!      implicit none
      
      integer nc_buf
      
      real AS, Zsed2p5_in, Zsed1p0_in, Vs30, Ztor, W, Dip, rake,
     :     Zhyp, Rx, Rrup, T, Fhw, stress_factor,  
     : Zsed1p0_AS08, Zsed1p0_CY08, W2use, Frv, Fnm, Zsed1p0,
     : abs_rx, SigTmea_as08, SigTest_as08, Tau_as08,
     : Sigmea_as08, Sigest_as08, Y_as08, U, SS, RS, 
     : Sig_TM_ba08, Tau_M_ba08, Sig_TU_ba08,  
     : Tau_U_ba08, Sigma_ba08, Y_ba08 , 
     : Zsed2p5, Zsed2p5_km,  
     : SigT_cb08, SigmaArb_cb08,  
     : Tau_cb08, Sigma_cb08,  
     : Y_cb08, SigTmeas_cy08,      
     : SigMeas_cy08, SigTinfer_cy08, 
     : SigInfer_cy08, Tau_cy08, Y_cy08   
 
      character buf*300, buf4*4, f_ctl*80, f_file*160,
     :  f_out*160, header4output*160, buf7*7, format_out*160 

      character coeff_head(10)*3
      character cmnts2skip(200)*79
      character f_file_tbl*80
      character version_ctl*8, version_in*30
      
      character path_nga_gmpe_coeff_files*150
      character path_rjb2rrup_coeff_files*150
      
      logical file_exist, output_in_gals 

      real m, logy_jb, mstart, mstop, dmag, rjb, rcd
      real saab05, sigab05, freq, ns
      real freq_tbl(50), coeff(50,10)
      
      character y_type*10  
      
      integer :: nmag, status
      
      integer nc_version_ctl, nc_f_ctl, nu_ctl      
      
      real pi, twopi, d2r 
      integer nc_cmnts2skip, nc_version_in, nc_h4out, nc_f_out, nu_out 
      
      integer, parameter :: nper_as = 24, nper_ba = 23, 
     :                      nper_cb = 23, nper_cy = 24
     
      real per_as(nper_as), per_ba(nper_ba), 
     :     per_cb(nper_cb), per_cy(nper_cy)

      data per_as/ 0.010, 0.020, 0.030, 0.040, 0.050, 0.075, 0.100, 
     :             0.150, 0.200, 0.250, 0.300, 0.400, 0.500, 0.750, 
     :             1.000, 1.500, 2.000, 3.000, 4.000, 5.000, 7.500, 
     :            10.000, 0.000, -1.000 /

      data per_ba/ 0.010, 0.020, 0.030,        0.050, 0.075, 0.100, 
     :             0.150, 0.200, 0.250, 0.300, 0.400, 0.500, 0.750, 
     :             1.000, 1.500, 2.000, 3.000, 4.000, 5.000, 7.500, 
     :            10.000, 0.000, -1.000	/

      data per_cb/ 0.010, 0.020, 0.030,        0.050, 0.075, 0.100, 
     :             0.150, 0.200, 0.250, 0.300, 0.400, 0.500, 0.750, 
     :             1.000, 1.500, 2.000, 3.000, 4.000, 5.000, 7.500, 
     :            10.000, 0.000, -1.000 /

      data per_cy/ 0.010, 0.020, 0.030, 0.040, 0.050, 0.075, 0.100, 
     :             0.150, 0.200, 0.250, 0.300, 0.400, 0.500, 0.750, 
     :             1.000, 1.500, 2.000, 3.000, 4.000, 5.000, 7.500, 
     :            10.000, 0.000, -1.000	/
     
      logical absrake_gt_180

      real zhyp_a(3), zhyp_b(3)
      data zhyp_a/7.08, 11.24, 5.63/
      data zhyp_b/0.61, -0.20, 0.68/
      
      pi = 4.0*atan(1.0)
      twopi = 2.0 * pi
      d2r = pi/180.0
      ynull = -9.99

      file_exist = .false.
      do while (.not. file_exist)
        f_ctl = ' '
C        write(*, '(a\)') 
        write(*, '(a)') 
     :    ' Enter name of control file ("Enter" = nga_gm_tmr.ctl): '
        read(*, '(a)') f_ctl
        if (f_ctl == ' ') f_ctl = 'nga_gm_tmr.ctl'
        call trim_c(f_ctl,nc_f_ctl)
        inquire(file=f_ctl(1:nc_f_ctl), exist=file_exist)
        if (.not. file_exist) then
          write(*,'(a)') ' ******* FILE DOES NOT EXIST ******* '
        end if
      end do
      
      call get_lun(nu_ctl)
      open(unit=nu_ctl,file=f_ctl(1:nc_f_ctl),status='old')

      call skipcmnt(nu_ctl, cmnts2skip, nc_cmnts2skip)
      version_in = ' '
      read(nu_ctl,'(a)') version_in
      call trim_c(version_in,nc_version_in)
      
      version_ctl = ' '
      version_ctl = '09/09/10'
      call trim_c(version_ctl,nc_version_ctl)

      if (version_ctl(1:nc_version_ctl) .ne. 
     :    version_in(1:nc_version_in)) then
        write(*,'(a)') 
     :     ' The control file has the wrong version date; STOP!'
        close(nu_ctl)
        stop
      end if
      
      call skipcmnt(nu_ctl,cmnts2skip,nc_cmnts2skip)  
      header4output = ' '
      read(nu_ctl,'(a)') header4output
      call trim_c(header4output,nc_h4out)
      
      call skipcmnt(nu_ctl,cmnts2skip,nc_cmnts2skip)  
      path_nga_gmpe_coeff_files = ' '
      read(nu_ctl,'(a)') path_nga_gmpe_coeff_files
      call trim_c(path_nga_gmpe_coeff_files,
     :            nc_path_nga_gmpe_coeff_files)
      
      call skipcmnt(nu_ctl,cmnts2skip,nc_cmnts2skip)  
      path_rjb2rrup_coeff_files = ' '
      read(nu_ctl,'(a)') path_rjb2rrup_coeff_files
      call trim_c(path_rjb2rrup_coeff_files,
     :            nc_path_rjb2rrup_coeff_files)
      
      call skipcmnt(nu_ctl,cmnts2skip,nc_cmnts2skip)      
      f_out = ' '
      read(nu_ctl,'(a)') f_out 
      call trim_c(f_out,nc_f_out)
      call get_lun(nu_out)
      open(unit=nu_out,file=f_out(1:nc_f_out),status='unknown')
      
      buf7 = ' '
      buf7 = header4output
      call upstr(buf7)
      
      if (buf7(1:7) /= '[BLANK]') then      
        write(nu_out,'(a)') '!'//header4output(1:nc_h4out)
        write(nu_out,'(a)') '!'
      end if

      call skipcmnt(nu_ctl,cmnts2skip,nc_cmnts2skip)
      buf = ' '
      read(nu_ctl,'(a)') buf
      call upstr(buf)
      call trim_c(buf, nc_buf)
      write(nu_out,'(a)') '! Units of PGV: cm/s'
      if (buf(1:1) == 'Y') then
        output_in_gals = .true.
        acc_factor = 981.0
        write(nu_out,'(a)') '! Units of PSA, PGA: cm/s/s'
      else
        output_in_gals = .false.
        acc_factor = 1.0
        write(nu_out,'(a)') '! Units of PSA, PGA: g'
      end if
      write(nu_out,'(a)') '!'
      
      write(nu_out,'(6x,a, 4x,a, 
     :               3x,a, 1x,a,
     :               3x,a, 
     :               1x,a, 1x,a, 1x,a, 4x,a, 
     :               1x,a, 
     :               1x,a, 1x,a,
     :               1x,a, 1x,a, 
     :               3x,a,     
     :               1x,a, 1x,a,     
     :               3x,a, 1x,a,     
     :               1x,a, 1x,a, 
     :               3x,a,
     :               1x,a, 1x,a, 1x,a, 
     :               1x,a, 1x,a,
     :               1x,a,
     :               9x,a, 3x,a, 3x,a, 7x,a,            
     :                 3x,a, 3x,a,
     :               9x,a, 5x,a, 5x,a, 4x,a,            
     :                 5x,a, 4x,a,
     :               9x,a, 5x,a, 7x,a, 3x,a, 6x,a,     
     :               9x,a, 2x,a, 3x,a, 3x,a,
     :                 3x,a, 3x,a 
     :                                                  )') 
     :       'T', 'M', 
     :       'Az_in', 'Az_use', 
     :       'Rjb', 
     :       'Rrup_in', 'Rrup_calc', 'Rrup_scherbaum', 'Rrup_use', 
     :       'Rx_calc', 
     :       'Zhyp_in', 'Zhyp_use',
     :       'Fhw_in', 'Fhw', 
     :       'rake',     
     :       'Dip_in', 'Dip_use',     
     :       'W_in', 'W_use',     
     :       'Ztor_in', 'Ztor_use',      
     :       'Vs30', 
     :       'Zsd1p0_in', 'Zsd1p0_AS', 'Zsd1p0_CY',  
     :       'Zsd2p5_in', 'Zsd2p5(km)',
     :       'AS',
     :      'Y_as', 'Sigestv_as', 'Sigmeav_as', 'Tau_as',
     :         'SigTest_as', 'SigTmea_as',
     :      'Y_ba', 'Sigma_ba', 'Tau_U_ba', 'Sig_TU_ba',
     :         'Tau_M_ba', 'Sig_TM_ba',
     :      'Y_cb', 'Sigma_cb', 'Tau_cb', 'Sig_Arb_cb', 'SigT_cb',
     :      'Y_cy', 'Tau_cy', 'SigInfr_cy', 'SgTinfr_cy',
     :         'SigMeas_cy', 'SgTmeas_cy'
     

! setup models:

      call model_setup(path_nga_gmpe_coeff_files,
     :  per_as, nper_as, indx_permin_as, indx_permax_as, indx_pgv_as,
     :                                                   indx_pga_as, 
     :  per_ba, nper_ba, indx_permin_ba, indx_permax_ba, indx_pgv_ba, 
     :                                                   indx_pga_ba, 
     :  per_cb, nper_cb, indx_permin_cb, indx_permax_cb, indx_pgv_cb, 
     :                                                   indx_pga_cb, 
     :  per_cy, nper_cy, indx_permin_cy, indx_permax_cy, indx_pgv_cy, 
     :                                                   indx_pga_cy)

      
      call skipcmnt(nu_ctl,cmnts2skip,nc_cmnts2skip)      
! positioned to read tmr values

      readloop: DO
      
        buf = ' '
        read(nu_ctl,'(a)',IOSTAT=status) buf

        if (status /= 0) then  ! reached end of file
          EXIT readloop
        end if

        call trim_c(buf, nc_buf)
        buf4 = ' '
        buf4(1:4) = buf(1:4)
        call upstr(buf4)
        if (buf4 == 'STOP') then
          EXIT readloop
        end if
        
        read(buf(1:nc_buf),*) T, M, Fhw_in, 
     :    Az_in, Rjb, Rrup_in, Zhyp_in, 
     :    rake, Dip_in, W_in, Ztor_in, Vs30, Zsed1p0_in, Zsed2p5_in, AS
     
        if (T < 0.0) then ! pgv, reset acc_factor
          acc_factor = 1.0
        end if
     
!check for unspecified required parameters:
!       T
!       M
!       Rjb
!       Fhw or az
!       rake (0.0, 90.0, -90.0 for SS, RS, NS)
!       Vs30

        if (T < 0.0 .and. T /= -1.0) then
          write(*,*) ' ERROR: T<0 and T/=-1, not a valid entry, '//
     :      'SKIP TO NEXT RECORD!!!'
          CYCLE
        end if

        if (M < 0.0 ) then
          write(*,*) ' ERROR: M is unspecified, '//
     :      'SKIP TO NEXT RECORD!!!'
          CYCLE
        end if

        if (Rjb < 0.0 ) then
          write(*,*) ' ERROR: Rjb is unspecified, '//
     :      'SKIP TO NEXT RECORD!!!'
          CYCLE
        end if

        if (Fhw_in < 0.0 .and. abs(az_in) > 180.0) then
          write(*,*) ' ERROR: Both Fhw_in and az_in are undefined, '//
     :      'SKIP TO NEXT RECORD!!!'
          CYCLE
        end if

        if (Vs30 <= 0.0 ) then
          write(*,*) ' ERROR: Vs30 is unspecified, '//
     :      'SKIP TO NEXT RECORD!!!'
          CYCLE
        end if

        if (abs(rake) > 180.0) then
          absrake_gt_180 = .true.
        else
          absrake_gt_180 = .false.
        end if
      
!check for inconsistent combinations of parameters:
!       Fhw < 0.0 .and. abs(az) > 180.0; 
!       Fhw == 0.0 .and. 0<=az<=180;
!       Fhw == 1.0 .and. -180<az<0

        if (Fhw_in == 0.0 .and. 
     :      (az_in >= 0.0 .and. az_in <= 180.0)) then
          write(*,*) 
     :      ' ERROR: Inconsistent values of Fhw_in (0) and az_in'//
     :                                              ' (>= 0.0); '//
     :      'SKIP TO NEXT RECORD!!!'
          CYCLE
        end if

        if (Fhw_in == 1.0 .and. 
     :      (az_in > -180.0 .and. az_in < 0.0)) then
          write(*,*) 
     :      ' ERROR: Inconsistent values of Fhw_in (1) and az_in'//
     :                                               ' (< 0.0); '//
     :      'SKIP TO NEXT RECORD!!!'
          CYCLE
        end if

        call assign_parameters(M, Fhw_in, 
     :    Az_in, Rjb, Rrup_in, Zhyp_in, 
     :    rake, Dip_in, W_in, Ztor_in, Vs30, Zsed1p0_in, Zsed2p5_in,
     :    zhyp, w, dip, ztor, az, path_rjb2rrup_coeff_files,
     :    Fhw,
     :    Rx, Rrup_calc, Rrup_scherbaum, Rrup, 
     :    Zsed1p0_AS08, Zsed1p0_CY08, Zsed2p5_km,
     :    Fnm_as08, Frv_as08, 
     :    U, SS, NS, RS,
     :    Fnm_cb08, Frv_cb08, 
     :    Fnm_cy08, Frv_cy08,
     :    ynull 
     :                           ) 

!
C        write(*,'(a,1x,f4.2,1x,f5.1,1x,ff7.3)') 
        write(*,'(a,1x,f4.2,1x,f5.1,1x,f7.3)') 
     :        '+Compute output for M, Rjb, T=', M, Rjb, T
!
        call get_gm_for_as08_ba08_cb08_cy08(
     :     M, AS, Dip, W, Ztor, Vs30, Rrup, Rjb, Rx, Fhw, T,  
     :     per_as, nper_as, indx_permin_as, indx_permax_as,
     :     per_ba, nper_ba, indx_permin_ba, indx_permax_ba,
     :     per_cb, nper_cb, indx_permin_cb, indx_permax_cb,
     :     per_cy, nper_cy, indx_permin_cy, indx_permax_cy,
     :     Zsed1p0_AS08, Zsed1p0_CY08, Zsed2p5_km,
     :     Frv_AS08, Fnm_AS08, 
     :     U, SS, NS, RS, 
     :     Frv_cb08, Fnm_cb08, 
     :     Frv_cy08, Fnm_cy08, 
     :     Y_AS08, Sigest_as08, Sigmea_as08, Tau_as08, 
     :       SigTest_as08, SigTmea_as08, 
     :     Y_BA08, Sigma_ba08, Tau_U_ba08, Tau_M_ba08,
     :       Sig_TU_ba08, Sig_TM_ba08,
     :     Y_CB08, Sigma_cb08, Tau_cb08,
     :       SigmaArb_cb08, SigT_cb08,
     :     Y_CY08, SigInfer_cy08, SigMeas_cy08, Tau_cy08,
     :       SigTinfer_cy08, SigTmeas_cy08,
     :     ynull, absrake_gt_180
     :                                          )

! write a line of output

      write(nu_out,'(1x,f6.3, 1x,f4.2, 
     :               1x,f7.1, 1x,f6.1,
     :               1x,f5.1, 
     :               1x,f7.1, 3x,f7.1, 9x,f6.1, 3x,f9.3, 
     :               1x,f7.2, 
     :               2x,f6.2, 3x,f6.2,
     :               5x,i2, 2x,i2,
     :               1x,f6.1,     
     :               1x,f6.1, 4x,f4.1,     
     :               1x,f6.1, 1x,f5.1,     
     :               3x,f5.1, 5x,f4.1,     
     :               1x,f6.1, 
     :               3x,f7.1, 3x,f7.1, 3x,f7.1,
     :               3x,f7.1, 4x,f7.3, 
     :               2x,i1,
     :               23(1x,es12.5))') 
     :      T, M, 
     :      Az_in, Az, 
     :      Rjb, 
     :      Rrup_in, Rrup_calc, Rrup_scherbaum, Rrup, 
     :      Rx, 
     :      Zhyp_in, Zhyp,
     :      int(Fhw_in), int(Fhw),
     :      rake,      
     :      Dip_in, Dip,      
     :      W_in, W,     
     :      Ztor_in, Ztor,      
     :      Vs30, 
     :      Zsed1p0_in, Zsed1p0_AS08, Zsed1p0_CY08,
     :      Zsed2p5_in, Zsed2p5_km,
     :      int(AS),
     :      acc_factor*Y_as08, Sigest_as08, Sigmea_as08, Tau_as08,
     :         SigTest_as08, SigTmea_as08,
     :      acc_factor*Y_ba08, Sigma_ba08, Tau_U_ba08, Sig_TU_ba08,
     :         Tau_M_ba08, Sig_TM_ba08,
     :      acc_factor*Y_cb08, Sigma_cb08, Tau_cb08, 
     :         SigmaArb_cb08, SigT_cb08,
     :      acc_factor*Y_cy08, Tau_cy08, SigInfer_cy08, SigTinfer_cy08,
     :      SigMeas_cy08, SigTmeas_cy08
     
      END DO readloop ! loop back for another set of input parameters
      
      close(nu_ctl)
      close(nu_out)
      
      END
      

!begin subroutine get_indices
      subroutine get_indices(per_gmpe, nper_gmpe, 
     :             indx_permin, indx_permax, indx_pgv, indx_pga)
     
* Dates: 01/12/10 - Written by D. Boore
*        05/01/10 - Added indx_permin

      real per_gmpe(*)
      integer indx_permax, indx_pgv, indx_pga

! Find the index of the minimum period (excluding 0.0)
      per_min = 9999.9
      DO i = 1, nper_gmpe
        IF (per_gmpe(i) < per_min .and. per_gmpe(i) > 0.0) THEN
          per_min = per_gmpe(i)
          indx_permin = i
        END IF
      END DO
 
! Find the index of the maximum period
      per_max = -1.0
      DO i = 1, nper_gmpe
        IF (per_gmpe(i) > per_max) THEN
          per_max = per_gmpe(i)
          indx_permax = i
        END IF
      END DO
 
!    Find index for pgv (period = -1.0):
      indx_pgv = 0
      find_pgv_index: DO i = 1, nper_gmpe
        IF (per_gmpe(i) == -1.0) THEN
          indx_pgv = i
          EXIT find_pgv_index
        END IF
      END DO find_pgv_index
      IF (indx_pgv == 0) THEN
        print *,' ERROR; coefficients for pgv not found; QUIT'
        stop
      END IF
      
!    Find index for pga (period = 0.0):
      indx_pga = 0
      find_pga_index: DO i = 1, nper_gmpe
        IF (per_gmpe(i) == 0.0) THEN
          indx_pga = i
          EXIT find_pga_index
        END IF
      END DO find_pga_index
      IF (indx_pga == 0) THEN
        PRINT *,' ERROR; coefficients for pga not found; QUIT'
        STOP
      END IF

      return
      end
!end subroutine get_indices
      
!begin subroutine get_y_type
      subroutine get_y_type(per, y_type)

* Dates: 01/12/10 - Written by D. Boore

      character y_type*(*)
      real per
      
      y_type = ' '
      IF (per <= 0) THEN
        y_type = 'PGVorPGA'
      ELSE
        y_type = 'PSA'        
      END IF
      
      return
      end
!end subroutine get_y_type
        
      
!begin subroutine trap_per_outside_range
      subroutine trap_per_outside_range(per, per_gmpe, nper_gmpe, 
     :                                  indx_permin, indx_permax)
     
* Dates: 01/12/10 - Written by D. Boore
*        05/01/10 - Added indx_permin

      real per, per_gmpe(*)
      integer nper_gmpe, indx_permin, indx_permax
          
      if (per <= 0.0) return
      
      if (per < per_gmpe(indx_permin) .or. 
     :    per > per_gmpe(indx_permax) )     then
        print *,' ERROR: per = ', per,
     :     ' is outside the tabulated range in per_gmpe table'
        print *,' per_gmpe '
        do i = 1, nper_gmpe
          print *, per_gmpe(i)
        end do
        print *, ' QUITTING!!!'
        stop
      end if
      
      return
      end       
!end subroutine trap_per_outside_range

!begin subroutine get_period_interval
          subroutine get_period_interval(per, per_gmpe, nper_gmpe,
     :                                   per1, per2)
     
* Dates: 01/12/10 - Written by D. Boore

      real per, per_gmpe(*), per1, per2
      integer nper_gmpe

* Find the two tabulated periods that span the interval
* containing the input period

! assume that the periods are sorted from small to large, and that period values
! for indices nper_gmpe-1 and nper_gmpe correspond to pga and pgv.

      if (per == per_gmpe(nper_gmpe-2)) then
        per1 = per_gmpe(nper_gmpe-3)
        per2 = per_gmpe(nper_gmpe-2)
        return
      else
        do i = 1, nper_gmpe - 3
          if (per >= per_gmpe(i) .and. per < per_gmpe(i+1) ) then
            per1 = per_gmpe(i)
            per2 = per_gmpe(i+1)
            return
          end if
        end do
      end if
      print *,' ERROR: could not find per = ',per,
     :      ' in per_gmpe table'
      print *,' per_gmpe '
      do i = 1, nper_gmpe
        print *, per_gmpe(i)
      end do
      print *, ' QUITTING!!!'
      stop
  
      end
!end subroutine get_period_interval
      
!begin subroutine model_setup
      subroutine model_setup(path_nga_gmpe_coeff_files,
     :  per_as, nper_as, indx_permin_as, indx_permax_as, indx_pgv_as,
     :                                                   indx_pga_as, 
     :  per_ba, nper_ba, indx_permin_ba, indx_permax_ba, indx_pgv_ba, 
     :                                                   indx_pga_ba, 
     :  per_cb, nper_cb, indx_permin_cb, indx_permax_cb, indx_pgv_cb, 
     :                                                   indx_pga_cb, 
     :  per_cy, nper_cy, indx_permin_cy, indx_permax_cy, indx_pgv_cy, 
     :                                                   indx_pga_cy)
     
      character path_nga_gmpe_coeff_files*(*)
      
      real per_as(nper_as), per_ba(nper_ba), 
     :     per_cb(nper_cb), per_cy(nper_cy) 
     
      
      call AS08_MODEL_SETUP(path_nga_gmpe_coeff_files)
      call BA08_MODEL_SETUP(path_nga_gmpe_coeff_files)
      call CB08_MODEL_SETUP(path_nga_gmpe_coeff_files)
      call CY08_MODEL_SETUP(path_nga_gmpe_coeff_files)
      
      call get_indices(per_as, nper_as, 
     :      indx_permin_as, indx_permax_as, indx_pgv_as, indx_pga_as)
      call get_indices(per_ba, nper_ba, 
     :      indx_permin_ba, indx_permax_ba, indx_pgv_ba, indx_pga_ba)
      call get_indices(per_cb, nper_cb, 
     :      indx_permin_cb, indx_permax_cb, indx_pgv_cb, indx_pga_cb)
      call get_indices(per_cy, nper_cy, 
     :      indx_permin_cy, indx_permax_cy, indx_pgv_cy, indx_pga_cy)
     
      return
      end
!end subroutine model_setup

!begin subroutine assign_parameters
        subroutine assign_parameters(M, Fhw_in, 
     :    Az_in, Rjb, Rrup_in, Zhyp_in, 
     :    rake, Dip_in, W_in, Ztor_in, Vs30, Zsed1p0_in, Zsed2p5_in,
     :    zhyp, w, dip, ztor, az, path_rjb2rrup_coeff_files,
     :    Fhw,
     :    Rx, Rrup_calc, Rrup_scherbaum, Rrup, 
     :    Zsed1p0_AS08, Zsed1p0_CY08, Zsed2p5_km,
     :    Fnm_as08, Frv_as08, 
     :    U, SS, NS, RS,
     :    Fnm_cb08, Frv_cb08, 
     :    Fnm_cy08, Frv_cy08,
     :    ynull 
     :                           ) 
     
! Dates: 05/07/10 - Reassign az to 180.0 if it equals -180.0 
!                 - Added istatus to indicate whether all is OK (istatus=0)
!                   or not (istatus = 1); if not, the calling program can skip
!                   to the next record, which is better than quitting from within
!                   this subroutine.
!                 - After adding this check I removed it, because the only time
!                   it would be found is if Fhw_in = 1 and -180<az_in<0, and
!                   I've trapped this case in the calling program.
!        08/06/10 - Special consideration for abs(rake > 180 (for BA08 use U, others are
!                   provide no motion)
     
      real M, Zsed2p5_in, Zsed1p0_in, Vs30, Ztor, W, Dip, rake,
     :     Zhyp, Rx, Rrup, Fhw, stress_factor,  
     : Zsed1p0_AS08, Zsed1p0_CY08, ynull
     
      real U, NS, SS, RS 
      
      character path_rjb2rrup_coeff_files*(*)
      character fault_type*10
        
      real zhyp_a(3), zhyp_b(3)
      data zhyp_a/7.08, 11.24, 5.63/
      data zhyp_b/0.61, -0.20, 0.68/
      
      pi = 4.0*atan(1.0)
      twopi = 2.0 * pi
      d2r = pi/180.0
      

     
        if (Zhyp_in .lt. 0.0) then
          fault_type = ' '
          if (abs(rake) > 180.0) then  ! undefined
            fault_type = 'GEN'   
            index_zhyp = 1
          else if (abs(rake) < 30.0 .or. abs(rake) > 150.0) then ! ss
            fault_type = 'SS'
            index_zhyp = 3
          else
            fault_type = 'SHD'  ! no use for "GEN" (index_zhyp=1) in this application.
            index_zhyp = 2
          end if
          Zhyp = zhyp_a(index_zhyp) + M*zhyp_b(index_zhyp)
        else
          Zhyp = Zhyp_in
        end if

        if (w_in .lt. 0.0) then
          if (abs(rake) > 180.0) then
            w = 10.0**(-1.01+0.32*m)
          else if (abs(rake) < 30.0 .or. abs(rake) > 150.0) then ! ss 
            w = 10.0**(-0.76+0.27*m)
          else if (rake >= -150.0 .and. rake <= -30.0 ) then ! n
            w = 10.0**(-1.14+0.35*m)
          else ! r
            w = 10.0**(-1.61+0.41*m)
          end if
!      stress_factor = (stress_ref/stress)**(1.0/3.0)
          stress_factor = 1.0
          w = stress_factor * w
        else
          w = w_in
        end if
      
!        if(fault_type(1:1) .eq. 'S') then
!          faultwidth = 10.0**(-0.76+0.27*m)
!        else if(fault_type(1:1) .eq. 'R') then
!          faultwidth = 10.0**(-1.61+0.41*m)
!        else if(fault_type(1:1) .eq. 'N') then
!          faultwidth = 10.0**(-1.14+0.35*m)
!        else
!          faultwidth = 10.0**(-1.01+0.32*amag)
!        end if
        
! assign dip based on rake

        if (dip_in .lt. 0.0) then
          if (abs(rake) > 180.0) then ! assume 45 degree dip
            dip = 45.0
          else if (abs(rake) < 30.0 .or. abs(rake) > 150.0) then ! ss
            dip = 90.0
          else if (rake >= -150.0 .and. rake <= -30.0) then ! n
            dip = 55.0
          else ! r
            dip = 40.0
          end if
        else
          dip = dip_in
        end if

        if (ztor_in .lt. 0.0) then
          ztor = amax1(0.0, Zhyp-0.6*w*sin(d2r*dip))
        else
          ztor = ztor_in
        end if

! consistency:
!  if Fhw_in < 0.0 .and. abs(az_in) > 180.0, then both are undefined, 
!                                     give an error message and stop
!  else consistency requires
!   Fhw == 0.0 .and. -180.0<az<0.0 .and. Rx < 0.0
!   Fhw == 1.0 .and.    0.0<=az<=180.0 .and. Rx >= 0.0
! In all cases, compute Rx; do not read it in
! if not consistent, precedence:
!   If az_in undefined, assign it a value based on Fhw_in, compute Rx
!   If fhw_in undefined, assign it a value based on az_in, compute Rx
!      

! Check for and force consistency in fhw, rx, az

        if (az_in == -180.0) then
          az_in = 180.0
          write(*,*) ' az_in=-180, resetting to +180'
        end if
        
        if (fhw_in < 0.0) then
          if (az_in < 0.0) then
            fhw = 0.0
          else
            fhw = 1.0
          end if
        else
          fhw = fhw_in
        end if
        
        if (rjb == 0.0) then
           fhw = 1.0
           az_in = 90.0
        end if
 
!        if (rjb == 0.0) then
!          if (fhw == 0.0) then
!            az_in = -90.0
!          else if (fhw == 1.0) then
!            az_in = +90.0
!          else
!          write(*,*) ' ERROR: rjb = 0 but Fhw not specified; QUITTING!'
!          stop
!        end if

        if (abs(az_in) > 180.0) then
          if (fhw == 0.0) then
            az = -50.0
          else
            az = +50.0
          end if
        else
          az = az_in
        end if
        
        call rx_calc_sub(rx_calc, rjb, ztor, w, dip, az, rrup_in)
        call rrup_calc_sub(rrup_calc, rjb, rx_calc, 
     :                     ztor, w, dip, az)
        
!        if (fhw == 0.0 .or. (fhw >= 0.0 .and. rx_in < 0.0)) then
!          rx = rx_calc
!        else
!          rx = rx_in
!        end if

         rx = rx_calc
        
        if (fhw == 0.0 .or. (fhw >= 0.0 .and. rrup_in < 0.0)) then
          rrup = rrup_calc
        else
          rrup = rrup_in
        end if

        fault_type = ' '
        if (abs(rake) > 180.0) then
          fault_type = 'GEN'
        else if (abs(rake) .lt. 30.0 .or. abs(rake) .gt. 150.0) then ! ss
          fault_type = 'SS'
        else
          fault_type = 'SHD'  !  
        end if
        call rjb2rrup(fault_type, M, rjb, rrup_scherbaum,
     :                  path_rjb2rrup_coeff_files)
	     !* Computed mean rrup given fault_type (GEN, SS, SHD), magnitude, and R_JB,
	     !* Using Scherbaum et al. (2004) equations. (Note: "SHD" stands for "SHallow Dipping")

* DEBUG
!        print *,' M, Az, Rjb, Rrup, Rx, Zhyp, Fhw'//
!     :        'rake, Dip, W, Ztor, Vs30, Zsed1p0_in, Zsed2p5_in'
!        print *,  M, Az, Rjb, Rrup, Rx, Zhyp, Fhw, 
!     :      rake, Dip, W, Ztor, Vs30, Zsed1p0_in, Zsed2p5_in
* DEBUG

! Compute Z1.0, Z2.5 if input values are less than 0:
      
        if (Zsed1p0_in .lt. 0.0) then
          if (Vs30 .lt. 180.0) then
            Zsed1p0_AS08 = EXP(6.745)
          else if (Vs30 .gt. 500.0) then
            Zsed1p0_AS08 = EXP(5.394-4.48*alog(Vs30/500.0))
          else
            Zsed1p0_AS08 = EXP(6.745-1.35*alog(Vs30/180.0))
          end if

          Zsed1p0_CY08 = EXP(28.5-(3.82/8.0)*alog(Vs30**8+378.7**8))
        else
          Zsed1p0_AS08 = Zsed1p0_in
          Zsed1p0_CY08 = Zsed1p0_in
        end if


        if (Zsed2p5_in .lt. 0.0) then
          Zsed2p5 = 1000.0*(0.519+3.595*(Zsed1p0_as08/1000.0)) ! use AS08 because the CB08 correlation may have used the SCEC v2.
                                                               ! model, not the v4. model as in CY08
        else
          Zsed2p5 = Zsed2p5_in
        end if

        Zsed2p5_km = Zsed2p5/1000.0  !  convert from meters to km; used by CB08


!From NGA_documentation.xls in peer_nga\database
!Mechanism Based on Rake Angle	 
!    Mechanism         Class              Rake Angles
!---------------------------------------------------------------------- 
!Strike - Slip            00                   -180 < Rake < -150
!                                               -30 < Rake <  30
!                                               150 < Rake < 180
!---------------------------------------------------------------------- 
!Normal                   01                   -120 < Rake < -60
!---------------------------------------------------------------------- 
!Reverse                  02                     60 < Rake < 120
!---------------------------------------------------------------------- 
!Reverse - Oblique        03                     30 < Rake < 60
!                                               120 < Rake < 150
!---------------------------------------------------------------------- 
!Normal - Oblique         04                   -150 < Rake < -120
!                                               -60 < Rake < -30
!But note: this is not accurate, because the NGA papers makes it clear
! that, e.g., FRV = 1 for 30<= rake <= 150.   I've used the more 
! accurate descriptions below.



!FOR AS08:

! convert rake to type of fault 
        if(abs(rake) > 180.0) then
          Frv_AS08 = ynull
          Fnm_AS08 = ynull
        else if( rake >= -120.0 .and. rake <= -60.0 ) then
          Fnm_AS08 = 1.0
          Frv_AS08 = 0.0
	else if( rake >= 30.0 .and. rake <= 150.0 ) then
	  Frv_AS08 = 1.0
C          Fnm_AS08 = 1.0		BUG? BUG? BUG? BUG? BUG? BUG? BUG?
          Fnm_AS08 = 0.0
        else         
          Frv_AS08 = 0.0
          Fnm_AS08 = 0.0
	end if
	
!FOR BA08:

! convert rake to type of fault  
        U = 0.0
        SS = 0.0
        NS = 0.0
        RS = 0.0
        if( abs(rake) > 180.0) then
          U = 1.0
        else if( (rake >= -150.0) .and. (rake <= -30.0) ) then
          NS = 1.0
	else if( (rake >= 30.0) .and. (rake <= 150.0) ) then
	  RS = 1.0
	else
	  SS = 1.0
	end if
	
!FOR CB08:

! convert rake to type of fault  
        if(abs(rake) > 180.0) then
          Frv_CB08 = ynull
          Fnm_CB08 = ynull
        else if( rake > -150.0 .and. rake < -30.0 ) then
          Fnm_CB08 = 1.0
          Frv_CB08 = 0.0
 	else if( rake > 30.0 .and. rake < 150.0 ) then
	  Frv_CB08 = 1.0
          Fnm_CB08 = 0.0
        else
          Frv_CB08 = 0.0
          Fnm_CB08 = 0.0
	end if
	
!FOR CY08:		 

! convert rake to type of fault  
        if(abs(rake) > 180.0) then
          Frv_CY08 = ynull
          Fnm_CY08 = ynull
        else if( rake >= -120.0 .and. rake <= -60.0 ) then
          Fnm_CY08 = 1.0
          Frv_CY08 = 0.0
	else if( rake >= 30.0 .and. rake <= 150.0 ) then
	  Frv_CY08 = 1.0
          Fnm_CY08 = 0.0
        else
          Frv_CY08 = 0.0
          Fnm_CY08 = 0.0
	end if
	
	return
	end
!end subroutine assign_parameters
	
!begin subroutine get_gm_for_as08_ba08_cb08_cy08 
        subroutine get_gm_for_as08_ba08_cb08_cy08(
     :     M, AS, Dip, W, Ztor, Vs30, Rrup, Rjb, Rx, Fhw, T,  
     :     per_as, nper_as, indx_permin_as, indx_permax_as,
     :     per_ba, nper_ba, indx_permin_ba, indx_permax_ba,
     :     per_cb, nper_cb, indx_permin_cb, indx_permax_cb,
     :     per_cy, nper_cy, indx_permin_cy, indx_permax_cy,
     :     Zsed1p0_AS08, Zsed1p0_CY08, Zsed2p5_km,
     :     Frv_AS08, Fnm_AS08, 
     :     U, SS, NS, RS, 
     :     Frv_cb08, Fnm_cb08, 
     :     Frv_cy08, Fnm_cy08, 
     :     Y_AS08, Sigest_as08, Sigmea_as08, Tau_as08, 
     :       SigTest_as08, SigTmea_as08, 
     :     Y_BA08, Sigma_ba08, Tau_U_ba08, Tau_M_ba08,
     :       Sig_TU_ba08, Sig_TM_ba08,
     :     Y_CB08, Sigma_cb08, Tau_cb08,
     :       SigmaArb_cb08, SigT_cb08,
     :     Y_CY08, SigInfer_cy08, SigMeas_cy08, Tau_cy08,
     :       SigTinfer_cy08, SigTmeas_cy08,
     :     ynull, absrake_gt_180
     :                                                   )
     
        real m, u, ss, ns, rs
        real per_as(*), per_ba(*),per_cb(*),per_cy(*)
        
        logical absrake_gt_180
        
        character developer*4

!Evaluate AS08:

!        write(*,*) ' Call AS08_model'
        
        developer = 'AS08'

        call get_nga_gm(
     :     developer, per_as, nper_as, indx_permin_as, indx_permax_as,
     :     M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv_AS08, Fnm_AS08, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0_AS08, Zsed2p5_km,
     :     T, Y_AS08, 
     :     Sigest_as08, Sigmea_as08, Tau_as08, Tau2,
     :     SigTest_as08, SigTmea_as08,
     :     ynull, absrake_gt_180
     :                                             )
     
!Evaluate BA08:

!        write(*,*) ' Call BA08_model'
        
        developer = 'BA08'

        call get_nga_gm(
     :     developer, per_ba, nper_ba, indx_permin_ba, indx_permax_ba,
     :     M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv_AS08, Fnm_AS08, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0_AS08, Zsed2p5_km,
     :     T, Y_BA08, 
     :     Sigma_ba08, Sigma, Tau_U_ba08, Tau_M_ba08,
     :     Sig_TU_ba08, Sig_TM_ba08,
     :     ynull, absrake_gt_180
     :                                             )
     
!Evaluate CB08:

!        write(*,*) ' Call CB08_model'
        
        developer = 'CB08'

        call get_nga_gm(
     :     developer, per_cb, nper_cb, indx_permin_cb, indx_permax_cb,
     :     M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv_CB08, Fnm_CB08, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0_AS08, Zsed2p5_km,
     :     T, Y_CB08, 
     :     Sigma_cb08, Sigma, Tau_cb08, Tau,
     :     SigmaArb_cb08, SigT_cb08,
     :     ynull, absrake_gt_180
     :                                             )
     
!Evaluate CY08:

!        write(*,*) ' Call CY08_model'
        
        developer = 'CY08'

        call get_nga_gm(
     :     developer, per_cy, nper_cy, indx_permin_cy, indx_permax_cy,
     :     M, AS, Dip, W, Ztor, 
     :     U, SS, NS, RS, Frv_CY08, Fnm_CY08, 
     :     Rrup, Rjb, Rx, Fhw,
     :     Vs30, Zsed1p0_CY08, Zsed2p5_km,
     :     T, Y_CY08, 
     :     SigInfer_cy08, SigMeas_cy08, Tau_cy08, Tau,
     :     SigTinfer_cy08, SigTmeas_cy08,
     :     ynull, absrake_gt_180
     :                                             )
     
!Developer      Sig1     Sig2    Tau1    Tau2      SigT1     SigT2
!     AS08    SigEst  SigMeas     Tau     -     SigT_Est SigT_Meas
!     BA08     Sigma      -     Tau_U   Tau_M   SigT_U      SigT_M
!     CB08     Sigma      -       Tau     -     SigT_Arb   SigT_GM
!     CY08  SigInfer  SigMeas     Tau     -   SigT_Infer SigT_Meas

      return
      end
!end subroutine get_gm_for_as08_ba08_cb08_cy08 

      include 'nga_gm_tmr_subs.for'

!      include 'get_nga_gm.for' 
!      include 'evaluate_nga_gmpes.for'
      
      
!      include 'as08_model_subroutine.for'
!      include 'ba08_model_subroutine.for'
!      include 'cb08_model_subroutine.for'
!      include 'cy08_model_subroutine.for'
!      include 'get_lun.for'
!      include 'skipcmnt.for'
!      include 'skip.for'
!      include 'upstr.for'
!      include 'trim_c.for'
!      include 'interpolate.for'
!      include 'lin_interp.for'
!      include 'locate.for'      
!      include 'rjb2rrup.for'
!      include '\forprogs\get_lun.for'
!      include '\forprogs\skipcmnt.for'
!      include '\forprogs\skip.for'
!      include '\forprogs\upstr.for'
!      include '\forprogs\trim_c.for'
!      include '\forprogs\interpolate.for'
!      include '\forprogs\lin_interp.for'
!      include '\forprogs\locate.for'      
!      include '\forprogs\rjb2rrup.for'


  
