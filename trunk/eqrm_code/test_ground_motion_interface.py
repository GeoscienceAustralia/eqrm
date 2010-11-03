

import unittest

from scipy import array, exp, log, allclose, sqrt, resize, e
from eqrm_code.ground_motion_specification import Ground_motion_specification
from eqrm_code.ground_motion_interface import *
import numpy


class Test_ground_motion_interface(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
  
    def test_Allen_interpolation(self):
        new_period = [0.45]
        model_name = 'Allen'
        model = Ground_motion_specification(model_name)
        result = model.calc_coefficient(new_period)
        Allen_coefficient_period = gound_motion_init['Allen'][4]
        calc_period = (Allen_coefficient_period[7] \
                       + Allen_coefficient_period[8])/2.
        self.failUnless(calc_period == new_period[0], 'Failed')
        Allen_coefficient = gound_motion_init['Allen'][3]
        #print "Allen_coefficient", Allen_coefficient
        calc_coefficient = (Allen_coefficient[0][7] \
                       + Allen_coefficient[0][8])/2.
        #print "calc_coefficient", calc_coefficient
        #print "result[0][0]", result[0][0]
        self.failUnless(calc_coefficient == result[0][0], 'Failed')
        
        result = model.calc_sigma_coefficient(new_period)
        Allen_sigma_coefficient_period = gound_motion_init['Allen'][7]
        calc_period = (Allen_sigma_coefficient_period[7] \
                       + Allen_sigma_coefficient_period[8])/2.
        self.failUnless(calc_period == new_period[0], 'Failed')
        Allen_sigma_coefficient = gound_motion_init['Allen'][6]
        #print "Allen_sigma_coefficient", Allen_sigma_coefficient
        calc_sigma_coefficient = (Allen_sigma_coefficient[0][7] \
                       + Allen_sigma_coefficient[0][8])/2.
        #print "calc_sigma_coefficient", calc_sigma_coefficient
        #print "result[0][0]", result[0][0]
        self.failUnless(calc_sigma_coefficient == result[0][0], 'Failed')
        
        
    def test_Gaull_1990_WA_distribution(self):
        model_name = 'Gaull_1990_WA'
        model = Ground_motion_specification(model_name)
        
        mag = [[7.0]]
        #FIXME DSG-EQRM should log_sigma = sigma_coefficient[0]
        a = 100
        distance = array([[[exp(10)]]])
        b = 3.0
        c = 2.0
        coefficient = array([[[[a]]],[[[b]]],[[[c]]]])
        sigma_1 =  0.7
        dummy  =  43543545
        sigma_coefficient = array([[[[sigma_1]]],[[[dummy]]]])
        log_mean,log_sigma = model.distribution(mag=mag,
            distance=distance,
            coefficient=coefficient,
            sigma_coefficient=sigma_coefficient)
        self.failUnless(log_sigma==sigma_1,
                        'Model incorrect.')
        
        # log_mean = ln(a) -c*ln(distance)+ b*mag   (5.6)EQRM tech manual
        # log_mean=100-20+21=101
        self.failUnless(101.0==log_mean,
                        'Model incorrect.')
        

    def test_Youngs_97_distribution(self):
        model_name='Youngs_97_interface'
        model=Ground_motion_specification(model_name)
        
        mag=7.0
        #FIXME DSG-EQRM should log_sigma=sigma_coefficient[0]
        
        distance=10.0
        r_z=10.0
        Z_t=0.0
        a=1.0
        b=1.0
        c=1.0
        
        coefficient=(a,b,c,Z_t)
        s1=1.0
        s2=1.0
        #sigma=s1+s2*mag=1+1*7
        sigma_1=8.0
        sigma_coefficient=(s1,s2)
        # log_mean_1=0.2418+1.414*mag+a+b*((10.0-mag)**3)+ \
        #  c*log(distance+1.7818*exp(0.554*mag))+0.00607*r_z+0.3846*Z_t
        #log_mean_1=
        
        log_mean,log_sigma=model.distribution(
            mag=mag,
            distance= distance,
            coefficient=coefficient,
            sigma_coefficient=sigma_coefficient,
            depth=r_z)
        
        self.failUnless(sigma_1==log_sigma,
                        'Model incorrect.')
        
        
        self.failUnless(42.76599206==(round(log_mean,8)),
                        'Model incorrect.')


    def test_Sadigh_97_distribution(self):
        model_name='Sadigh_97'
        model=Ground_motion_specification(model_name)
        
        mag=array([[[7.0]]])
       
        F=1.0
        distance=array([[[10.0]]])
        r_z=10.0
        Z_t=0.0
        a=1.0
        b=1.0
        c=1.0
        d=1.0
        e=1.0
        f=1.0
        g=1.0
        h=1.0
        
        coefficient=array([[[[a]]],[[[b]]],[[[c]]],[[[d]]],[[[e]]],[[[f]]],
                           [[[g]]],[[[h]]],
                           [[[a]]],[[[b]]],[[[c]]],[[[d]]],[[[e]]],[[[f]]],
                           [[[g]]],[[[h]]]])
                           
        
        s1=1.0
        s2=1.0
        s3=1.0
        # FIXME: This is not the formula in the manual
        # (manual has **2, not **2.5)
        # or in the original paper.  
        R = distance + g*exp(h*mag)
        log_mean_calc = (a*F + b + c*mag + d*(8.5-mag)**(2.5)+e*log(R)+ \
                    f*log(distance+2))  
        sigma_coefficient = array([[[[s1]]],[[[s2]]],[[[s3]]]])
        sigma_1=s1-s2*mag
        #sigma_1=-6
        log_mean,log_sigma=model.distribution(mag=mag,
            distance=distance,
            coefficient=coefficient,
            sigma_coefficient=sigma_coefficient)
        self.failUnless(sigma_1==log_sigma, 'Model incorrect.')
        self.assert_(allclose(log_mean_calc, log_mean))

 
    def test_Toro_1997_midcontinent_distribution(self):
        
        model_name = 'Toro_1997_midcontinent'
        model = Ground_motion_specification(model_name)
        
        distance = array([[[8.6602540]]])
        mag = array([[[8.0]]])

        c1 = 1.0
        c2 = 2.0
        c3 = 3.0
        c4 = 4.0
        c5 = 5.0
        c6 = 6.0
        c7 = 5.0
        
        coefficient = array([[[[c1]]], [[[c2]]], [[[c3]]], [[[c4]]], [[[c5]]],
                       [[[c6]]], [[[c7]]]])
        
        sigma_coefficient = coefficient
        
        log_mean,log_sigma=model.distribution(
            mag=mag,
            distance=distance,
            coefficient=coefficient,
            sigma_coefficient=sigma_coefficient)
        log_mean_p, log_sigma_p=Toro_1997_midcontinent_distribution_python(
            mag=mag,
            distance=distance,
            coefficient=coefficient,
            sigma_coefficient=sigma_coefficient)

        # From Toro et al (1997)
        # Note the manual has a typo, (rjb + c7^2)^0.5 - which is incorrect
        # Rm = (rjb^2 + c7^2)^0.5
        # Rm = (75 + 25)^0.5
        # Rm = 10
        
        # 1 + 2*(8 - 6) + 3*(8 - 6)^2 - 4In(10)-6*10
        # 1 + 4 + 12 - 4In(10) -60
        # 4In(10) - 43
        # -9.21 -43
        # -52.21034037197618
        actual = -52.21034037197618
        #print "log_mean", log_mean
        #print "log_mean_p", log_mean_p
        self.assert_(allclose(actual, log_mean[0][0][0]))
        self.assert_(allclose(actual, log_mean_p[0][0][0]))
        
    def test_Atkinson_Boore_97_distribution(self):
        
        model_name='Atkinson_Boore_97'
        model=Ground_motion_specification(model_name)
        
        distance = array([[[10]]])
        mag = array([[[8.0]]])

        c1 = 1.0
        c2 = 2.0
        c3 = 3.0
        c4 = 4.0
        
        coefficient = array([[[[c1]]], [[[c2]]], [[[c3]]], [[[c4]]]])

        # Atkinson and Boore (1997)
        # EQRM manual sect 5.2.3. eq 5.8
        # 1 + 2*(8 - 6) + 3*(8 - 6)^2 - In(10)-4*10
        # 1 + 4 + 12 - In(10) -40
        # -9.21 - 23
        # -25.302585092994047
        actual = -25.302585092994047
        
        sigma_coefficient = array([[[[3.0]]]])
        
        log_mean,log_sigma=model.distribution(
            mag=mag,
            distance=distance,
            coefficient=coefficient,
            sigma_coefficient=sigma_coefficient)
        log_mean_p, log_sigma_p=Atkinson_Boore_97_distribution_python(
            mag,distance,
            coefficient,sigma_coefficient,
            None)
        #print "log_mean", log_mean
        #print "log_mean_p", log_mean_p
        self.assert_(allclose(actual, log_mean_p[0][0][0]))
        self.assert_(allclose(actual, log_mean[0][0][0]))

    def test_Boore_08_distribution_subfunctions(self):
        
        model_name='Boore_08'
        model=Ground_motion_specification(model_name)
        
        distance = array([[[4]]])
        mag = array([[[5.5]]])
        Vs30 = array([[[100.0]]])
        
        c1 = 1.0
        c2 = 2.0
        c3 = 3.0
        c4 = 4.0

        h = 3.0
        
        e1 = 1.0
        e2 = 2.0
        e3 = 3.0
        e4 = 4.0
        e5 = 5.0
        e6 = 6.0
        e7 = 7.0
        
        mh = 3.5
        sig = 2.0
        tu = 2.0
        sigtu = 2.0
        tm = 2.0
        sigtm = 2.0
        blin = 2.0
        b1 = 1.0
        b2  = 2.0
        
        coefficient = array([c1, c2, c3, h, e1, e2, e3, e4, e5, e6, e7, mh,
                             sig, tu, sigtu, tm, sigtm, blin, b1, b2])
        coefficient.shape = (-1, 1, 1, 1)
        
        sigma_coefficient = array([[[[3.0]]]])

        # R = 5
        # Fd = [1 + 2(5.5-4.5)]ln(5/1)+3(5-1)
        fd_actual = 3*log(5) + 12
        fd = fd_Boore_08(c1, c2, c3, distance, h, mag)
        self.assert_(allclose(fd_actual, fd))

        fm = fm_Boore_08(e1, e5, e6, e7, 6.75, 6.75)
        self.assert_(allclose(1, fm))

        # m-mh = -2  mh = 6.75     
        fm_actual = 1+5*-2+6*4
        fm = fm_Boore_08(e1, e5, e6, e7, 4.75, 6.75)
        self.assert_(allclose(fm_actual, fm))
        
        # m-mh = 2       
        fm_actual = 1+7*2
        fm = fm_Boore_08(e1, e5, e6, e7, 8.75, 6.75)
        self.assert_(allclose(fm_actual, fm))

        bnl = bnl_Boore_08(b1, b2, 100)        
        self.assert_(allclose(1, bnl))

        # bnl_actual = (1-2)log(200/300)/log(180/300) + 2
        bnl_actual = 2-log(200./300.)/log(180./300.)
        bnl = bnl_Boore_08(b1, b2, 200.)
        self.assert_(allclose(bnl_actual, bnl))
        
        bnl = bnl_Boore_08(b1, b2, 770.)
        self.assert_(allclose(0.0, bnl))
        
        bnl = bnl_Boore_08(b1, b2, Vs30)
        self.assert_(allclose(1, bnl))

        bnl_local = 2
        Vs30_local = VREF_BOORE_08*100
        pga4nl = 0.01
        fs = fs_Boore_08(blin, pga4nl, bnl_local, Vs30_local)
        

        # this has got some messy constants
        delx = log(0.09/0.03)
        dely = bnl_local*log(0.09/0.06)
        c = (3*dely - bnl_local*delx)/delx**2
        d = -(2*dely - bnl_local*delx)/delx**3
        flin = bnl_local*log(Vs30_local/760)
        
        fnl = bnl_local* log(0.06/0.1)
        fs_actual = flin + fnl        
        self.assert_(allclose(fs_actual, fs))
        
        pga4nl = 0.05
        fnl = bnl_local* log(0.06/0.1) + c*log(pga4nl/0.03)**2. + \
              d*log(pga4nl/0.03)**3.
        fs_actual = flin + fnl
        fs = fs_Boore_08(blin, pga4nl, bnl_local, Vs30_local)     
        self.assert_(allclose(fs_actual, fs))
        
        pga4nl = 0.1
        fnl = bnl_local* log(pga4nl/0.1)
        fs_actual = flin + fnl
        fs = fs_Boore_08(blin, pga4nl, bnl_local, Vs30_local)     
        self.assert_(allclose(fs_actual, fs))

        
    def test_Boore_08_distribution(self):
        
        model_name='Boore_08'
        model=Ground_motion_specification(model_name)
        
        distance = array([[[4]]])
        mag = array([[[5.5]]])
        Vs30 = array([[[100.0]]])
        
        c1 = 1.0
        c2 = 2.0
        c3 = 3.0
        c4 = 4.0

        h = 3.0
        
        e1 = 1.0
        e2 = 2.0
        e3 = 3.0
        e4 = 4.0
        e5 = 5.0
        e6 = 6.0
        e7 = 7.0
        
        mh = 6.75
        sig = 2.0
        tu = 2.0
        sigtu = 2.0
        tm = 2.0
        sigtm = 2.0
        blin = 2.0
        b1 = 1.0
        b2  = 2.0
        
        coefficient = array([c1, c2, c3, h, e1, e2, e3, e4, e5, e6, e7, mh,
                             sig, tu, sigtu, tm, sigtm, blin, b1, b2])
        coefficient.shape = (-1, 1, 1, 1)
        
        sigma_coefficient = array([[[[3.0]]]])

        fd = fd_Boore_08(c1, c2, c3, distance, h, mag)
        fm = fm_Boore_08(e1, e5, e6, e7, mag, 6.75)

        pga4nl = 0.13899198 # From running gmi.
        bnl = bnl_Boore_08(b1, b2, Vs30)
        fs = fs_Boore_08(blin, pga4nl, bnl, Vs30)
        
        log_mean_actual = fd + fm + fs
        
        log_mean,log_sigma=model.distribution(
            mag=mag,
            distance=distance,
            coefficient=coefficient,
            sigma_coefficient=sigma_coefficient,
            Vs30=Vs30)
        self.assert_(allclose(log_mean_actual, log_mean[0][0][0]))
        self.assert_(allclose(sigtu, log_sigma[0][0][0]))
   

    def test_Boore_08_distribution2(self):
        pga4nl = array([[[0.01, 0.04, 0.11, 0.04],
                         [ 0.04, 0.01, 0.11, 0.01]]])
        
        bnl  = array([[[1., 1., 2., 2.  ]]])
        blin = array([[[0., 0., 0., 0.]]]) # this is checked in a test above

        Vs30 = 760
        fs = fs_Boore_08(blin, pga4nl, bnl, Vs30)
        #pgalow = 0.06
        low = log(0.06/0.1)
        high = log(0.11/0.1)
        mid = fs_Boore_08(0, 0.04, 1, 760)
        fs_actual = array([[[low, mid, 2*high, 2*mid],
                         [ mid, low, 2*high, 2*low]]])
        self.assert_(allclose(fs_actual, fs))
               
         
    def test_Boore_08_distribution3(self):
        
        model_name='Boore_08'
        model=Ground_motion_specification(model_name)
        
        distance = array([[[4]]])
        mag = array([[[5.5]]])
        Vs30 = array([[[100.0]]])
        
        c1 = 1.0
        c2 = 2.0
        c3 = 3.0
        c4 = 4.0

        h = 3.0
        
        e1 = 1.0
        e2 = 2.0
        e3 = 3.0
        e4 = 4.0
        e5 = 5.0
        e6 = 6.0
        e7 = 7.0
        
        mh = 6.75
        sig = 2.0
        tu = 2.0
        sigtu = 2.0
        tm = 2.0
        sigtm = 2.0
        blin = 2.0
        b1 = 1.0
        b2  = 2.0
        
        coefficient_base = array([c1, c2, c3, h, e1, e2, e3, e4, e5, e6, e7,
                                  mh,
                             sig, tu, sigtu, tm, sigtm, blin, b1, b2])
        array_3 = [0,0,0]
        coefficient = []
        for i, base_element in enumerate(coefficient_base):
            coefficient.extend(coefficient_base[i] + array_3)
        coefficient = asarray(coefficient)
        #print "coefficient", coefficient
        coefficient.shape = (-1, 1, 1, len(array_3))

        sigma_coefficient = array([[[[3.0]]]])
        c1, c2, c3, h, e1, e2, e3, e4, e5, e6, e7 = coefficient[:11]
        mh, sig, tu, sigtu, tm, sigtm, blin, b1, b2 = coefficient[11:]

        # Setting mh array
        mh = array([6.75, 6.75, 4.75])
        
        fd = fd_Boore_08(c1, c2, c3, distance, h, mag)
        fm = fm_Boore_08(e1, e5, e6, e7, mag, 6.75)
        
        log_mean,log_sigma=model.distribution(
            mag=mag,
            distance=distance,
            coefficient=coefficient,
            sigma_coefficient=sigma_coefficient,
            Vs30=Vs30)
        
        # From running gmi.
        pga4nl = array([[[0.13899198, 0.1389919, 0.1389919]]])
        
        bnl = bnl_Boore_08(b1, b2, Vs30)
        fs = fs_Boore_08(blin, pga4nl, bnl, Vs30)
        
        log_mean_actual = fd + fm + fs
        

        self.assert_(allclose(log_mean_actual, log_mean[0][0][0]))
        self.assert_(allclose(log_mean_actual, log_mean[0][0][1]))
        self.assert_(allclose(log_mean_actual, log_mean[0][0][2]))
        self.assert_(allclose(sigtu, log_sigma[0][0][0]))

    def test_Boore_08_distribution_subfunctions2(self):
        
        model_name = 'Boore_08'
        model = Ground_motion_specification(model_name)
        
        distance = array([[[4]]])
        mag = array([[[5.5]]])
        Vs30 = array([[[100.0]]])
        
        c1 = 1.0
        c2 = 2.0
        c3 = 3.0
        c4 = 4.0

        h = 3.0
        
        e1 = 1.0
        e2 = 2.0
        e3 = 3.0
        e4 = 4.0
        e5 = 5.0
        e6 = 6.0
        e7 = 7.0
        
        mh = 3.5
        sig = 2.0
        tu = 2.0
        sigtu = 2.0
        tm = 2.0
        sigtm = 2.0
        blin = 2.0
        b1 = 1.0
        b2  = 2.0
        
        coefficient_base = array([c1, c2, c3, h, e1, e2, e3, e4, e5, e6, e7,
                                  mh,
                             sig, tu, sigtu, tm, sigtm, blin, b1, b2])
        periods = [0,0,0]
        coefficient = []
        for i, base_element in enumerate(coefficient_base):
            coefficient.extend(coefficient_base[i]+periods)
        coefficient = asarray(coefficient)
        #print "coefficient", coefficient
        coefficient.shape = (-1, 1, 1, len(periods))

        sigma_coefficient = array([[[[3.0]]]])
        
        c1, c2, c3, h, e1, e2, e3, e4, e5, e6, e7 = coefficient[:11]
        mh, sig, tu, sigtu, tm, sigtm, blin, b1, b2 = coefficient[11:]

        mh = array([6.75, 6.75, 6.75])
        mag = array([6.75, 4.75, 8.75])
        
        # m-mh = -2  mh = 6.75  fm_actual = 1+5*-2+6*4
        # m-mh = 2  fm_actual = 1+7*2
        
        fm = fm_Boore_08(e1, e5, e6, e7, mag, mh)
        self.assert_(allclose([1, 1+5*-2+6*4, 15], fm))

        mh = array([60.75, 60.75, 60.75])
        mag = array([60.75, 58.75, 62.75])
        
        # m-mh = -2  mh = 6.75  fm_actual = 1+5*-2+6*4
        # m-mh = 2  fm_actual = 1+7*2        
        fm = fm_Boore_08(e1, e5, e6, e7, mag, mh)
        self.assert_(allclose([1, 1+5*-2+6*4, 15], fm))


    def test_Somerville09_Yilgarn_distribution(self):
        model_name='Somerville09_Yilgarn'
        model=Ground_motion_specification(model_name)
        
        mag = 5.4
        ##>>> distance = (e**4 - 36)**0.5
        ## distance = 4.3125572498396156
        distance = 4.3125572498396156
        # R = e**2 # 7.3890560989306495
        c1 = 1.0
        c2 = 2.0
        c3 = 3.0
        c4 = 4.0
        c5 = 5.0
        c6 = 6.0
        c7 = 7.0
        c8 = 8.0
        
        coefficient=(c1, c2, c3, c4, c5, c6, c7, c8)
        log_mean = Somerville09_log_mean(coefficient, mag, distance)
        #print "log_mean", log_mean


        # for M<m1, r<r1
        log_mean_actual = 1. + 2.*(-1.) + 3.*2. + 4.*(-1.)*2. + \
                          5.*(e**4. - 36.)**0.5 + 8.0*(8.5-mag)**2
        self.failUnless(allclose(asarray(log_mean_actual), log_mean),
                          'log_mean Model incorrect.')
        mag = 7.4
        log_mean = Somerville09_log_mean(coefficient, mag, distance)
        
        # for M>m1, r<r1
        log_mean_actual = 1. + 7.*(1.) + 3.*2. + 4.*(1.)*2. + \
                          5.*(e**4. - 36.)**0.5 + 8.0*(8.5-mag)**2 
        self.failUnless(allclose(asarray(log_mean_actual), log_mean),
                          'log_mean Model incorrect.')
        mag = 5.4
        #>>> distance = (e**8 - 36)**0.5
        distance = 54.267467114669422
        ln_R1 = log((50**2+6**2)**0.5)
        #ln_R = 4.
        
        # for M<m1, r>r1
        log_mean_actual = 1. + 2.*(-1.) + 3.*ln_R1 + 4.*(-1.)*4. \
                          + 5.*(e**8. - 36.)**0.5 + 6.*(4 - ln_R1) \
                          + 8.0*(8.5-5.4)**2
        log_mean = Somerville09_log_mean(coefficient, mag, distance)
        self.failUnless(allclose(asarray(log_mean_actual), log_mean),
                          'log_mean Model incorrect.')

        
        mag = 7.4
        # for M>m1, r>r1
        log_mean_actual = 1. + 7.*(1.) + 3.*ln_R1 + 4.*(1.)*4. \
                          + 5.*(e**8. - 36.)**0.5 + 6.*(4 - ln_R1) \
                          + 8.0*(8.5-mag)**2
        log_mean = Somerville09_log_mean(coefficient, mag, distance)
        self.failUnless(allclose(asarray(log_mean_actual), log_mean),
                          'log_mean Model incorrect.')
        
    def Xtest_Somerville09_Yilgarn_coefficents_sigma(self):

        # how this test could work.
        # it will call some internal functions, to do the math,
        # since the test before checks up on on this.
        # this test is for the coefficients
        model_name = 'Somerville09_Yilgarn'
        model = Ground_motion_specification(model_name)
        
        distance = array([[[4]]])
        mag = array([[[5.5]]])
        Vs30 = array([[[100.0]]])
        

        
        log_mean,log_sigma=model.distribution(
            mag=mag,
            distance=distance,
            coefficient=coefficient,
            sigma_coefficient=sigma_coefficient)
        self.assert_(allclose(log_mean_actual, log_mean[0][0][0]))
        self.assert_(allclose(sigtu, log_sigma[0][0][0]))


    def test_Liang_2008(self):
        """Test the Liang_2008 model by calling Liang_2008() directly."""

        # The data here is from a spreadsheet that implemented the algorithm
        # in the paper and compared the results against values taken from the
        # graphs in figure 15.  The match there was sometimes broad, but 
        # good enough overall to trust the spreadsheet implementation, given
        # that the estimate of SA values from the graphs was difficult.
        # 
        # The spreadsheet is in 'Liang_2008.xls'.
        # 
        # This test compares the python implementation against the spreadsheet
        # results.  The match is expected to be much tighter.

        model_name = 'Liang_2008'
        model = Ground_motion_specification(model_name)

        # conversion factor: ln mm/s2 -> ln g
        g_factor = math.log(9.80665 * 1000)
        #g_factor = 9.1908160059617412

        ######
        # period = 10.0s, ML=4.0, R=50.0
        ######

        period = 10.0
        ML = numpy.array([[[4.0]]])
        R = numpy.array([[[50.0]]])

        # get coeffs for this period
        coeffs = numpy.array([[[[-10.565]]],[[[2.380]]],[[[-0.019]]],
                              [[[-0.395]]],[[[0.044]]]])

        # sigma coefficients - these are static
        sigma_coeffs = numpy.array([[[[1.166]]],[[[1.166]]]])


        # expected values from paper, corrected for result in g, not mm/s2
        log_mean_expected = -2.852 - g_factor
        log_sigma_expected = sigma_coeffs[0][0] - g_factor

        (log_mean,
             log_sigma) = model.distribution(coefficient=coeffs,
                                             sigma_coefficient=sigma_coeffs,
                                             mag=ML, distance=R)
        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                        msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                        msg)

        ######
        # period = 1.0s, ML=5.0, R=100.0
        ######

        period = 1.0
        ML = numpy.array([[[5.0]]])
        R = numpy.array([[[100.0]]])

        # get coeffs for this period
        coeffs = numpy.array([[[[-3.901]]],[[[1.892]]],[[[-0.019]]],
                              [[[0.134]]],[[[-0.070]]]])

        # sigma coefficients - these are static
        sigma_coeffs = numpy.array([[[[1.166]]],[[[1.166]]]])

        # expected values from paper, corrected for result in g, not mm/s2
        log_mean_expected = 2.664 - g_factor
        log_sigma_expected = Liang_2008_sigma_coefficient[0][0] - g_factor

        (log_mean,
             log_sigma) = model.distribution(coefficient=coeffs,
                                             sigma_coefficient=sigma_coeffs,
                                             mag=ML, distance=R)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                        msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                        msg)

        ######
        # period = 0.1s, ML=7.0, R=200.0
        ######

        period = 0.1
        ML = numpy.array([[[7.0]]])
        R = numpy.array([[[200.0]]])

        # get coeffs for this period
        coeffs = numpy.array([[[[1.598]]],[[[1.312]]],[[[-0.010]]],
                              [[[-0.507]]],[[[-0.028]]]])

        # sigma coefficients - these are static
        sigma_coeffs = numpy.array([[[[1.166]]],[[[1.166]]]])

        # expected values from paper, corrected for result in g, not mm/s2
        log_mean_expected = 5.057 - g_factor
        log_sigma_expected = Liang_2008_sigma_coefficient[0][0] - g_factor

        (log_mean,
             log_sigma) = model.distribution(coefficient=coeffs,
                                             sigma_coefficient=sigma_coeffs,
                                             mag=ML, distance=R)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                        msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                        msg)

        ######
        # check that results for a scenario with distance=1.0 km are same
        # as for distance=10.0 km.  we limit minimum distance to 10.0 km.
        ######

        period = 1.0
        ML = numpy.array([[[7.0]]])
        R = numpy.array([[[10.0]]])

        # get coeffs for this period
        period_index = Liang_2008_coefficient_period.index(period)
        coeffs = Liang_2008_coefficient[:,period_index]
        coeffs = reshape(coeffs, (5, 1, 1, 1))

        # sigma coefficients - these are static
        sigma_coeffs = numpy.array([[[[1.166]]],[[[1.166]]]])

        # get results for R=10.0 km
        (log_mean_10, _) = model.distribution(coefficient=coeffs,
                                              sigma_coefficient=sigma_coeffs,
                                              mag=ML, distance=R)

        # then get results for R=1.0 km
        R = numpy.array([[[1.0]]])
        (log_mean_1, _) = model.distribution(coefficient=coeffs,
                                             sigma_coefficient=sigma_coeffs,
                                             mag=ML, distance=R)

        # check results are same
        msg = ("Results for T=%.1f, ML=%.1f, R=%.1f:\n%s\n"
               "don't equal those for R=%.1f:\n%s"
               % (period, ML, 10.0, str(log_mean_10), 1.0, str(log_mean_1)))
        self.failUnless(allclose(log_mean_10, log_mean_1, rtol=1.0e-4,
                                 atol=1.0e-4),
                        msg)


    def test_Atkinson06_basic(self):
        """Test the Atkinson06_basic function."""

        # The data here is from a spreadsheet that implemented the algorithm
        # in the paper and compared the results against values taken from the
        # graphs in figure 6.
        # 
        # This test compares the Atkinson06_basic python implementation against
        # the spreadsheet results. 
        #
        # Note that the Atkinson06_basic() function returns log10 values with
        # units mm/s/s.

        ######
        # period = 1.0s, ML=5.5, R=100.0 - call Atkinson06_basic(),
        #     returns log10 cm/s/s
        ######

        period = 1.0				# frequency = 1.0
        ML = numpy.array([[[5.5]]])		# magnitude
        R = numpy.array([[[100.0]]])		# distance

        # get coeffs for period 1.0 (includes three extra values for table 8)
        coeffs = numpy.array([[[[-5.27e+0]]],[[[2.26e+0]]],[[[-1.48e-1]]],
                              [[[-2.07e+0]]],[[[1.50e-1]]],[[[-8.13e-1]]],
                              [[[ 4.67e-2]]],[[[8.26e-1]]],[[[-1.62e-1]]],
                              [[[-4.86e-4]]],[[[0]]],[[[0]]],[[[0]]]])

        # sigma coefficients - these are static
        sigma = 0.30
        sigma_coeffs = numpy.array([[[[sigma]]],[[[sigma]]]])

        # expected values from paper (log10 mm/s/s)
        log_mean_expected = numpy.array([[[0.33]]])
        log_sigma_expected = numpy.array([[[0.30]]])

        (log_mean, log_sigma) = Atkinson06_basic(coefficient=coeffs,
                                                 sigma_coefficient=sigma_coeffs,
                                                 mag=ML, distance=R, S=0.0)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-2, atol=1.0e-2),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                                 msg)


    def test_Atkinson06_hard_bedrock(self):
        """Test the Atkinson06_hard_bedrock function."""

        # This is a repeat of test_Atkinson06_basic() above, except that we
        # go through model.distribution() and get results converted to ln g.

        model_name = 'Atkinson06_hard_bedrock'
        model = Ground_motion_specification(model_name)

        # conversion factor: mm/s2 -g_factor -> g
        g_factor = math.log(9.80665e+2)
        # conversion factor: log10/ln_factor -> loge
        ln_factor = math.log10(math.e)

        ######
        # period = 1.0s, ML=5.5, R=100.0 - call Atkinson06_hard_bedrock(),
        #     returns ln g
        ######

        period = 1.0
        ML = numpy.array([[[5.5]]])
        R = numpy.array([[[100.0]]])

        # get coeffs for this period (includes 3 unused table 8 values)
        coeffs = numpy.array([[[[-5.27e+0]]],[[[2.26e+0]]],[[[-1.48e-1]]],
                              [[[-2.07e+0]]],[[[1.50e-1]]],[[[-8.13e-1]]],
                              [[[ 4.67e-2]]],[[[8.26e-1]]],[[[-1.62e-1]]],
                              [[[-4.86e-4]]],[[[0]]],[[[0]]],[[[0]]]])

        # sigma coefficients - these are static
        sigma = 0.30
        sigma_coeffs = numpy.array([[[[sigma]]],[[[sigma]]]])

        # expected values from paper (converted to ln g)
        log_mean_expected = numpy.array([[[0.33]]])/ln_factor - g_factor
        log_sigma_expected = 0.30/ln_factor - g_factor

        (log_mean, log_sigma) = model.distribution(coefficient=coeffs,
                                                   sigma_coefficient=\
                                                       sigma_coeffs,
                                                   mag=ML, distance=R)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-2, atol=1.0e-2),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                                 msg)

        ######
        # period = 2.0s, ML=7.5, R=300.0 - call Atkinson06_hard_bedrock(),
        #     returns ln g
        ######

        period = 2.0
        ML = numpy.array([[[7.5]]])
        R = numpy.array([[[300.0]]])

        # get coeffs for this period (includes 3 unused table 8 values)
        coeffs = numpy.array([[[[-6.18e+0]]],[[[2.30e+0]]],[[[-1.44e-1]]],
                              [[[-2.22e+0]]],[[[1.77e-1]]],[[[-9.37e-1]]],
                              [[[ 7.07e-2]]],[[[9.52e-1]]],[[[-1.77e-1]]],
                              [[[-3.22e-4]]],[[[0]]],[[[0]]],[[[0]]]])

        # sigma coefficients - these are static
        sigma = 0.30
        sigma_coeffs = numpy.array([[[[sigma]]],[[[sigma]]]])

        # expected values from paper (converted to ln g)
        log_mean_expected = numpy.array([[[1.08]]])/ln_factor - g_factor
        log_sigma_expected = 0.30/ln_factor - g_factor

        (log_mean, log_sigma) = model.distribution(coefficient=coeffs,
                                                   sigma_coefficient=\
                                                       sigma_coeffs,
                                                   mag=ML, distance=R)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-2, atol=1.0e-2),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                                 msg)

    def test_Atkinson06_soil(self):
        """Test the Atkinson06_soil function."""

        # Run one scenario from Atkinson06_soil_check.py - scenario 4.
        # period=1.0, distance=100.0, magnitude=7.5, Vs30=400.0, logPSA=1.757910

        model_name = 'Atkinson06_soil'
        model = Ground_motion_specification(model_name)

        # conversion factor: cm/s/s -> g
        g_factor = math.log(9.80665*100)
        # conversion factor: log10 -> loge
        ln_factor = math.log10(math.e)

        ######
        # period = 1.0s, ML=7.5, R=100.0, Vs30=400.0 - call Atkinson06_soil(),
        #     returns ln g
        ######

        period = 1.0
        ML = numpy.array([[[7.5]]])
        R = numpy.array([[[100.0]]])
        Vs30 = numpy.array([400.0])

        # get coeffs for this period
        coeffs = numpy.array([[[[-5.27e+0]]],[[[2.26e+0]]],[[[-1.48e-1]]],
                              [[[-2.07e+0]]],[[[1.50e-1]]],[[[-8.13e-1]]],
                              [[[ 4.67e-2]]],[[[8.26e-1]]],[[[-1.62e-1]]],
                              [[[-4.86e-4]]],
                              [[[-0.7]]],[[[-0.44]]],[[[0]]]])

        # sigma coefficients - these are static
        sigma = 0.30
        sigma_coeffs = numpy.array([[[[sigma]]],[[[sigma]]]])

        # expected values from Atkinson06_soil_check.py (converted to ln g)
        log_mean_expected = numpy.array([[[1.757910]]])/ln_factor - g_factor
        log_sigma_expected = Atkinson06_sigma_coefficient[0][0]/ln_factor - \
                                 g_factor

        (log_mean, log_sigma) = model.distribution(coefficient=coeffs,
                                                   sigma_coefficient=\
                                                       sigma_coeffs,
                                                   mag=ML, distance=R,
                                                   Vs30=Vs30)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-2, atol=1.0e-2),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                                 msg)

    def test_Atkinson06_bc_boundary_bedrock(self):
        """Test the Atkinson06_bc_boundary_bedrock function."""

        # This is a repeat of test_Atkinson06_hard_bedrock() above.
        # We compare results with those generated by the program
        # test_resources/GM_Matlab/Atkinson06_bc_boundary_bedrock_check.py

        model_name = 'Atkinson06_bc_boundary_bedrock'
        model = Ground_motion_specification(model_name)

        # conversion factor: mm/s2 -g_factor -> g
        g_factor = math.log(9.80665e+2)
        # conversion factor: log10/ln_factor -> loge
        ln_factor = math.log10(math.e)

        ######
        # period = 1.0s, ML=5.5, R=100.0 - call Atkinson06_bc_boundary_bedrock(),
        #     returns ln g
        ######

        period = 1.0
        ML = numpy.array([[[5.5]]])
        R = numpy.array([[[100.0]]])

        # get coeffs for this period (includes 3 unused table 8 values)
        coeffs = numpy.array([[[[-5.06E+00]]],[[[2.23E+00]]],[[[-1.45E-01]]],
                              [[[-2.03E+00]]],[[[1.41E-01]]],[[[-8.74E-01]]],
                              [[[5.41E-02]]],[[[7.92E-01]]],[[[-1.70E-01]]],
                              [[[-4.89E-04]]],[[[0]]],[[[0]]],[[[0]]]])

        # sigma coefficients - these are static
        sigma = 0.30
        sigma_coeffs = numpy.array([[[[sigma]]],[[[sigma]]]])

        # expected values from paper (converted to ln g)
        log_mean_expected = numpy.array([[[0.455175]]])/ln_factor - g_factor
        log_sigma_expected = 0.30/ln_factor - g_factor

        (log_mean, log_sigma) = model.distribution(coefficient=coeffs,
                                                   sigma_coefficient=\
                                                       sigma_coeffs,
                                                   mag=ML, distance=R)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-2, atol=1.0e-2),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-3, atol=1.0e-3),
                                 msg)

    def test_Chiou08_basic(self):
        """Test the Chiou08 model by calling Chiou08_distribution() directly."""

        # The data here is from a program that implemented the algorithm
        # in the paper and compared the results against values taken from the
        # graphs in figure 19 (rock).  The match there was good(ish).
        # The program is test_resources/GM_Matlab/Chiou08_check.py.
        # 
        # This test compares the python implementation against the check program
        # results.

        ######
        # period = 0.01s, ML=7.5, R=20.0, etc (see figure 19)
        ######

        period = 0.01
        ML = numpy.array([[[7.0]]])
        R = numpy.array([[25.0]])
        Vs30 = numpy.array([300.0])
        fault_type = numpy.array([[[2]]], dtype=int)
        Ztor = numpy.array([[[0.0]]])
        dip = numpy.array([[[90.0]]])

        # get coeffs for this period
        coeffs = numpy.array([[[[1.06]]],[[[3.45]]],[[[-2.1]]],
                              [[[-0.5]]],[[[50.0]]],[[[3.0]]],
                              [[[4.0]]],[[[-1.2687]]],[[[0.1000]]],
                              [[[-0.2550]]],[[[2.996]]],[[[4.1840]]],
                              [[[6.1600]]],[[[0.4893]]],[[[0.0512]]],
                              [[[0.0860]]],[[[0.7900]]],[[[1.5005]]],
                              [[[-0.3218]]],[[[-0.00804]]],[[[-0.00785]]],
                              [[[-0.4417]]],[[[-0.1417]]],[[[-0.007010]]],
                              [[[0.102151]]],[[[0.2289]]],[[[0.014996]]],
                              [[[580.0]]],[[[0.0700]]]])

        # sigma coefficients - these are static
        sigma_coeffs = numpy.array([[[[0.3437]]],[[[0.2637]]],[[[0.4458]]],
                                    [[[0.3459]]],[[[0.8000]]],[[[0.0663]]]])


        # a fake dist_object class
        # assume Rrup & Rx = the R value
        class DistObj(object):
            def __init__(self):
                self.Rupture = numpy.array(R)
                self.Joyner_Boore = numpy.array(R)
                self.Horizontal = numpy.array(R)
        distances = DistObj()

        Rrup = distances.Rupture

        # expected values from paper (sigma can be anything, make it very small)
        log_mean_expected = numpy.array([[[math.log(1.565E-01)]]])
        log_sigma_expected = numpy.array([[[4.844E-01]]])

        (log_mean,
             log_sigma) = Chiou08_distribution(mag=ML, dist_object=distances,
                                               fault_type=fault_type, dip=dip,
                                               depth_to_top=Ztor, Vs30=Vs30,
                                               coefficient=coeffs,
                                               sigma_coefficient=sigma_coeffs)
        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, log_mean_expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                        msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, log_sigma_expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                        msg)

    def test_Chiou08(self):
        """Test the Chiou8 model."""

        # This is a repeat of test_Chiou08_basic() above, except that we
        # go through model.distribution() and get results in ln g.

        model_name = 'Chiou08'
        model = Ground_motion_specification(model_name)

        ######
        # period = 0.01s, ML=7.5, R=20.0, etc (see figure 19)
        ######

        period = 0.01
        ML = numpy.array([[[4.0]]])
        R = numpy.array([[5.0]])
        Vs30 = numpy.array([300.0])
        fault_type = numpy.array([[[2]]], dtype=int)
        dip = numpy.array([[[90.0]]])
        Ztor = numpy.array([[[0.0]]])

        # get coeffs for this period
        coeffs = numpy.array([[[[1.06]]],[[[3.45]]],[[[-2.1]]],
                              [[[-0.5]]],[[[50.0]]],[[[3.0]]],
                              [[[4.0]]],[[[-1.2687]]],[[[0.1000]]],
                              [[[-0.2550]]],[[[2.996]]],[[[4.1840]]],
                              [[[6.1600]]],[[[0.4893]]],[[[0.0512]]],
                              [[[0.0860]]],[[[0.7900]]],[[[1.5005]]],
                              [[[-0.3218]]],[[[-0.00804]]],[[[-0.00785]]],
                              [[[-0.4417]]],[[[-0.1417]]],[[[-0.007010]]],
                              [[[0.102151]]],[[[0.2289]]],[[[0.014996]]],
                              [[[580.0]]],[[[0.0700]]]])

        # sigma coefficients - these are static
        sigma_coeffs = numpy.array([[[[0.3437]]],[[[0.2637]]],[[[0.4458]]],
                                    [[[0.3459]]],[[[0.8000]]],[[[0.0663]]]])

        # a fake dist_object class
        # assume Rrup & Rx = the R value
        class DistObj(object):
            def __init__(self):
                self.Rupture = numpy.array(R)
                self.Joyner_Boore = numpy.array(R)
                self.Horizontal = numpy.array(R)
        distances = DistObj()

        # expected values from paper (sigma can be anything, make it very small)
        log_mean_expected = numpy.array([[[math.log(5.581E-02)]]])
        log_sigma_expected = numpy.array([[[6.508E-01]]])

        (log_mean,
             log_sigma) = model.distribution(mag=ML, dist_object=distances,
                                             fault_type=fault_type, dip=dip,
                                             depth_to_top=Ztor, Vs30=Vs30,
                                             coefficient=coeffs,
                                             sigma_coefficient=sigma_coeffs)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(log_mean, log_mean_expected,
                                 rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(log_sigma, log_sigma_expected,
                                 rtol=1.0e-4, atol=1.0e-4),
                                 msg)

    def test_Campbell03(self):
        """Test the Campbell03 model."""

        model_name = 'Campbell03'
        model = Ground_motion_specification(model_name)

        ######
        # period = 0.2, ML=7.0, R=10.0,
        # expect lnY=0.0663, sigma=0.4904 (from Campbell03_check.py)
        ######

        period = 0.2
        ML = numpy.array([[[7.0]]])
        R = numpy.array([[[10.0]]])

        # get coeffs for this period (C1 -> C10 from table 6)
        coeffs = numpy.array([[[[-0.432800]]], [[[ 0.617000]]], [[[-0.058600]]],
                              [[[-1.320000]]], [[[-0.004600]]], [[[ 0.000337]]],
                              [[[ 0.399000]]], [[[ 0.493000]]], [[[ 1.250000]]],
                              [[[-0.928000]]]])

        # sigma coefficients for this period (C11 -> C13 from table 6)
        sigma_coeffs = numpy.array([[[[1.077]]], [[[-0.0838]]], [[[0.478]]]])


        # expected values from Campbell03_check.py
        log_mean_expected = numpy.array([[[0.0663]]])
        log_sigma_expected = numpy.array([[[0.4904]]])

        (log_mean, log_sigma) = model.distribution(mag=ML, distance=R,
                                                   coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)

        # tests for equality should be quite tight as we check against
        # Campbell03_check.py
        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

    def test_Campbell08_SS1(self):
        """Test the Campbell08 model - strike_slip fault."""

        model_name = 'Campbell08'
        model = Ground_motion_specification(model_name)

        # a fake dist_object class
        # assume Rrup=200 and Rjb=199.9
        class DistObj(object):
            def __init__(self):
                self.Rupture = numpy.array([[2.0000e+2]])
                self.Joyner_Boore = numpy.array([[1.9990e+2]])

        ######
        # period = 0.01, ML=5.0, Rrup=200.0, Rjb=1.999
        # expect lnY=math.log(2.7675e-3) (from Campbell08_check.py)
        #        lnE=math.log(4.7793e-1)
        ######

        period = 0.01
        periods = numpy.array([period])
        dist_object = DistObj()
        ML = numpy.array([[[5.0]]])
        depth = numpy.array([[[5.0]]])
        dip = numpy.array([[[90.0]]])
        fault_type = numpy.array([[[2]]], dtype=int)	# SS
        Vs30 = numpy.array([760.0])
        Z25 = numpy.array([2.0])	# force Z25 = 2.0km

        # get coeffs for this period (C0 -> K3 from table 2)
        coeffs = numpy.array([[[[-1.715]]], [[[0.500]]],  [[[-0.530]]],
                              [[[-0.262]]], [[[-2.118]]], [[[0.170]]],
                              [[[5.60]]],   [[[0.280]]],  [[[-0.120]]],
                              [[[0.490]]],  [[[1.058]]],  [[[0.040]]],
                              [[[0.610]]],  [[[865]]],    [[[-1.186]]],
                              [[[1.839]]]])

        # sigma coefficients for this period (ElnY -> rho from table 3)
        sigma_coeffs = numpy.array([[[[0.478]]], [[[0.219]]], [[[0.166]]],
                                    [[[0.526]]], [[[0.551]]], [[[1.000]]]])


        # expected values from Campbell08_check.py
        log_mean_expected = numpy.array([[[math.log(2.7675e-3)]]])
        log_sigma_expected = numpy.array([[[math.log(4.7793e-1)]]])

        (log_mean, log_sigma) = model.distribution(dist_object=dist_object,
                                                   mag=ML, periods=periods,
                                                   depth_to_top=depth,
                                                   fault_type=fault_type,
                                                   dip=dip,
                                                   Vs30=Vs30, Z25=Z25,
                                                   coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)

        # tests for equality should be quite tight as we check against
        # Campbell08_check.py
        msg = ('T=%.2f, ML=%.1f, Rrup=%.1f: log_mean=%s, expected=%s'
               % (period, ML, 10.0, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.2f, ML=%.1f, Rrup=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, 10.0, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

    def test_Campbell08_SS1(self):
        """Test the Campbell08 model - strike_slip fault."""

        model_name = 'Campbell08'
        model = Ground_motion_specification(model_name)

        # a fake dist_object class
        # assume Rrup=200 and Rjb=199.9
        class DistObj(object):
            def __init__(self):
                self.Rupture = numpy.array([[2.0000e+2]])
                self.Joyner_Boore = numpy.array([[1.9990e+2]])

        ######
        # period = 0.01, ML=5.0, Rrup=200.0, Rjb=1.999
        # expect lnY=math.log(2.7675e-3) (from Campbell08_check.py)
        #        lnE=math.log(4.7793e-1)
        ######

        period = 0.01
        periods = numpy.array([period])
        dist_object = DistObj()
        ML = numpy.array([[[5.0]]])
        depth = numpy.array([[[5.0]]])
        dip = numpy.array([[[90.0]]])
        fault_type = numpy.array([[[2]]], dtype=int)	# SS
        Vs30 = numpy.array([760.0])
        Z25 = numpy.array([2.0])	# force Z25 = 2.0km

        # get coeffs for this period (C0 -> K3 from table 2)
        coeffs = numpy.array([[[[-1.715]]], [[[0.500]]],  [[[-0.530]]],
                              [[[-0.262]]], [[[-2.118]]], [[[0.170]]],
                              [[[5.60]]],   [[[0.280]]],  [[[-0.120]]],
                              [[[0.490]]],  [[[1.058]]],  [[[0.040]]],
                              [[[0.610]]],  [[[865]]],    [[[-1.186]]],
                              [[[1.839]]]])

        # sigma coefficients for this period (ElnY -> rho from table 3)
        sigma_coeffs = numpy.array([[[[0.478]]], [[[0.219]]], [[[0.166]]],
                                    [[[0.526]]], [[[0.551]]], [[[1.000]]]])


        # expected values from Campbell08_check.py
        log_mean_expected = numpy.array([[[math.log(2.7675e-3)]]])
        log_sigma_expected = numpy.array([[[math.log(4.7793e-1)]]])

        (log_mean, log_sigma) = model.distribution(dist_object=dist_object,
                                                   mag=ML, periods=periods,
                                                   depth_to_top=depth,
                                                   fault_type=fault_type,
                                                   dip=dip,
                                                   Vs30=Vs30, Z25=Z25,
                                                   coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)

        # tests for equality should be quite tight as we check against
        # Campbell08_check.py
        msg = ('T=%.2f, ML=%.1f, Rrup=%.1f: log_mean=%s, expected=%s'
               % (period, ML, 10.0, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.2f, ML=%.1f, Rrup=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, 10.0, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

    def test_Campbell08_SS2(self):
        """Test the Campbell08 model - strike_slip fault."""

        model_name = 'Campbell08'
        model = Ground_motion_specification(model_name)

        Rrup = 5.0000e+0
        Rjb = 5.0000e+0

        # a fake dist_object class
        class DistObj(object):
            def __init__(self):
                self.Rupture = numpy.array([[Rrup]])
                self.Joyner_Boore = numpy.array([[Rjb]])

        ######
        # period = 0.2, ML=7.0
        ######

        period = 0.2
        periods = numpy.array([period])
        dist_object = DistObj()
        ML = numpy.array([[[7.0]]])
        depth = numpy.array([[[0.0]]])
        dip = numpy.array([[[90.0]]])
        fault_type = numpy.array([[[2]]], dtype=int)	# SS
        Vs30 = numpy.array([760.0])
        Z25 = numpy.array([2.0])	# force Z25 = 2.0km

        # get coeffs for this period (C0 -> K3 from table 2)
        coeffs = numpy.array([[[[-0.486]]], [[[0.500]]], [[[-0.446]]],
                              [[[-0.398]]], [[[-2.220]]], [[[0.170]]],
                              [[[7.60]]], [[[0.280]]], [[[-0.012]]],
                              [[[0.490]]], [[[2.194]]], [[[0.040]]],
                              [[[0.610]]], [[[748]]], [[[-2.188]]],
                              [[[1.856]]]])

        # sigma coefficients for this period (ElnY -> rho from table 3)
        sigma_coeffs = numpy.array([[[[0.534]]], [[[0.249]]], [[[0.186]]],
                                    [[[0.589]]], [[[0.618]]], [[[0.871]]]])


        # expected values from Campbell08_check.py
        log_mean_expected = numpy.array([[[math.log(8.7425e-1)]]])
        log_sigma_expected = numpy.array([[[math.log(5.3400e-1)]]])

        (log_mean, log_sigma) = model.distribution(dist_object=dist_object,
                                                   mag=ML, periods=periods,
                                                   depth_to_top=depth,
                                                   fault_type=fault_type,
                                                   dip=dip,
                                                   Vs30=Vs30, Z25=Z25,
                                                   coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)

        # tests for equality should be quite tight as we check against
        # Campbell08_check.py
        msg = ('T=%.2f, ML=%.1f, Rrup=%.1f: log_mean=%s, expected=%s'
               % (period, ML, Rrup, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.2f, ML=%.1f, Rrup=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, Rrup, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

    def test_Campbell08_RV1(self):
        """Test the Campbell08 model - Reverse fault."""

        model_name = 'Campbell08'
        model = Ground_motion_specification(model_name)

        Rrup = 2.0000e+2
        Rjb = 1.9990e+2

        # a fake dist_object class
        class DistObj(object):
            def __init__(self):
                self.Rupture = numpy.array([[Rrup]])
                self.Joyner_Boore = numpy.array([[Rjb]])

        ######
        # period = 0.01, M=5.0
        ######

        period = 0.01
        periods = numpy.array([period])
        dist_object = DistObj()
        M = numpy.array([[[5.0]]])
        depth = numpy.array([[[5.0]]])
        dip = numpy.array([[[45.0]]])
        fault_type = numpy.array([[[0]]], dtype=int)	# RV
        Vs30 = numpy.array([760.0])
        Z25 = numpy.array([[[2.0]]])	# force Z25 = 2.0km

        # get coeffs for this period (C0 -> K3 from table 2)
        coeffs = numpy.array([[[[-1.715]]], [[[0.500]]],  [[[-0.530]]],
                              [[[-0.262]]], [[[-2.118]]], [[[0.170]]],
                              [[[5.60]]],   [[[0.280]]],  [[[-0.120]]],
                              [[[0.490]]],  [[[1.058]]],  [[[0.040]]],
                              [[[0.610]]],  [[[865]]],    [[[-1.186]]],
                              [[[1.839]]]])

        # sigma coefficients for this period (ElnY -> rho from table 3)
        sigma_coeffs = numpy.array([[[[0.478]]], [[[0.219]]], [[[0.166]]],
                                    [[[0.526]]], [[[0.551]]], [[[1.000]]]])


        # expected values from Campbell08_check.py
        log_mean_expected = numpy.array([[[math.log(3.6614e-3)]]])
        log_sigma_expected = numpy.array([[[math.log(4.7790e-1)]]])

        (log_mean, log_sigma) = model.distribution(dist_object=dist_object,
                                                   mag=M, periods=periods,
                                                   depth_to_top=depth,
                                                   fault_type=fault_type,
                                                   dip=dip,
                                                   Vs30=Vs30, Z25=Z25,
                                                   coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)

        # tests for equality should be quite tight as we check against
        # Campbell08_check.py
        msg = ('T=%.2f, M=%.1f, Rrup=%.1f: log_mean=%s, expected=%s'
               % (period, M, Rrup, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.2f, M=%.1f, Rrup=%.1f: log_sigma=%s, expected=%s'
               % (period, M, Rrup, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

    def test_Campbell08_RV2(self):
        """Test the Campbell08 model - Reverse fault."""

        model_name = 'Campbell08'
        model = Ground_motion_specification(model_name)

        Rrup = 5.0000e+0
        Rjb = 0.0000e+0

        # a fake dist_object class
        class DistObj(object):
            def __init__(self):
                self.Rupture = numpy.array([[Rrup]])
                self.Joyner_Boore = numpy.array([[Rjb]])

        ######
        # period = 0.01, M=7.0
        ######

        period = 0.01
        periods = numpy.array([period])
        dist_object = DistObj()
        M = numpy.array([[[7.0]]])
        depth = numpy.array([[[0.0]]])
        dip = numpy.array([[[45.0]]])
        fault_type = numpy.array([[[0]]], dtype=int)	# RV
        Vs30 = numpy.array([760.0])
        Z25 = numpy.array([[[2.0]]])	# force Z25 = 2.0km

        # get coeffs for this period (C0 -> K3 from table 2)
        coeffs = numpy.array([[[[-1.715]]], [[[0.500]]],  [[[-0.530]]],
                              [[[-0.262]]], [[[-2.118]]], [[[0.170]]],
                              [[[5.60]]],   [[[0.280]]],  [[[-0.120]]],
                              [[[0.490]]],  [[[1.058]]],  [[[0.040]]],
                              [[[0.610]]],  [[[865]]],    [[[-1.186]]],
                              [[[1.839]]]])

        # sigma coefficients for this period (ElnY -> rho from table 3)
        sigma_coeffs = numpy.array([[[[0.478]]], [[[0.219]]], [[[0.166]]],
                                    [[[0.526]]], [[[0.551]]], [[[1.000]]]])


        # expected values from Campbell08_check.py
        log_mean_expected = numpy.array([[[math.log(5.9403e-1)]]])
        log_sigma_expected = numpy.array([[[math.log(4.6852e-1)]]])

        (log_mean, log_sigma) = model.distribution(dist_object=dist_object,
                                                   mag=M, periods=periods,
                                                   depth_to_top=depth,
                                                   fault_type=fault_type,
                                                   dip=dip,
                                                   Vs30=Vs30, Z25=Z25,
                                                   coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)

        # tests for equality should be quite tight as we check against
        # Campbell08_check.py
        msg = ('T=%.2f, M=%.1f, Rrup=%.1f: log_mean=%s, expected=%s'
               % (period, M, Rrup, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.2f, M=%.1f, Rrup=%.1f: log_sigma=%s, expected=%s'
               % (period, M, Rrup, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

    def test_Abrahamson08(self):
        """Test the Abrahamson08 model.

        Compare with data from Abrahamson08_check.py.
        """

        model_name = 'Abrahamson08'
        model = Ground_motion_specification(model_name)

        # a fake dist_object class
        # it can be this simple since delta=90 and Ztor=0.0
        class DistObj(object):
            def __init__(self, distance):
                self.Rupture = distance
                self.Joyner_Boore = distance
                self.Horizontal = distance

        # Test various scenarios for period=0.2
        period = 0.2
        periods = numpy.array([period])
        Rrup = 100.0
        dist_object = DistObj(numpy.array(numpy.array([[Rrup, Rrup]])))
        ML = numpy.array([[[7.0], [5.0]]])
        depth = numpy.array([[[0.0], [0.0]]])
        dip = numpy.array([[[90.0], [90.0]]])
        fault_type = numpy.array([[[2], [2]]], dtype=int)	# strike_slip
        Vs30 = numpy.array([760.0])
        width = numpy.array([[[10.0], [10.0]]])

        # get coeffs for this period
        coeffs = numpy.array([[[[6.75]]],[[[4.5]]],[[[0.265]]],[[[-0.231]]],
                              [[[-0.398]]],[[[1.18]]],[[[1.88]]],[[[50.0]]],
                              [[[748.2]]],[[[-2.188]]], [[[1.6870]]],
                              [[[-0.9700]]],[[[-0.0396]]], [[[2.0773]]],
                              [[[0.0309]]],[[[-0.0600]]],[[[1.1274]]],
                              [[[-0.3500]]], [[[0.9000]]],[[[-0.0083]]]])

        # sigma coefficients for this period (S1 -> rho from table 6)
        sigma_coeffs = numpy.array([[[[0.630]]],[[[0.514]]],[[[0.614]]],
                                    [[[0.495]]],[[[0.520]]],[[[0.329]]],
                                    [[[0.874]]]])

        # expected values from Abrahamson08_check.py
        log_mean_expected = numpy.array([[[6.909E-02], [6.699E-03]]])
        log_sigma_expected = numpy.array([[[6.103E-01], [8.169E-01]]])

        (log_mean, log_sigma) = model.distribution(dist_object=dist_object,
                                                   mag=ML, periods=periods,
                                                   depth_to_top=depth,
                                                   width=width,
                                                   fault_type=fault_type,
                                                   dip=dip, Vs30=Vs30,
                                                   coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)

        # tests for equality should be quite tight as we check against
        # Abrahamson08_check.py
#        msg = ('Shape error:\nlog_mean.shape=%s\nexpected.shape=%s' %
#               (str(log_mean.shape), str(log_mean_expected.shape)))
#        self.failUnlessEqual(log_mean.shape, log_mean_expected.shape, msg)
        msg = ('\nT=%.2f, Rrup=%.1f, ML=\n%s\nlog_mean=\n%s\nexpected=\n%s' %
               (period, Rrup, str(ML), str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(log_mean, log_mean_expected,
                                 rtol=1.0e-4, atol=1.0e-4),
                        msg)

#        msg = ('Shape error:\nlog_sigma.shape=%s\nexpected.shape=%s' %
#               (str(log_sigma.shape), str(log_sigma_expected.shape)))
#        self.failUnlessEqual(log_sigma.shape, log_sigma_expected.shape, msg)
        msg = ('\nT=%.2f, Rrup=%.1f, ML=\n%s\nlog_sigma=\n%s\nexpected=\n%s'
               % (period, Rrup, str(ML), str(log_sigma),
                  str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                 rtol=1.0e-4, atol=1.0e-4),
                        msg)

    def test_mean_10_sigma_1(self):
        model_name = 'mean_10_sigma_1'
        model = Ground_motion_specification(model_name)

        num_sites =  2
        num_events =  3
        num_periods = 4
        
        distance = zeros((num_sites, num_events, 1))
        coefficient = zeros((1, 1, 1, num_periods))
        (log_mean, log_sigma) = model.distribution(
            distance=distance, coefficient=coefficient)
        act_log_sigma = ones((num_sites, num_events, num_periods))
        act_log_mean = ones((num_sites, num_events, num_periods))*10
        self.failUnless(allclose(log_mean, act_log_mean))
        self.failUnless(allclose(log_sigma, act_log_sigma))

        
    def test_Zhao_2006_intraslab(self):
        """Test the Campbell03 model."""

        model_name = 'Zhao_2006_intraslab'
        model = Ground_motion_specification(model_name)

        ######
        # period = 0.2, ML=7.0, R=10.0,
        # expect lnY=0.0663, sigma=0.4904 (from Campbell03_check.py)
        ######

        period = 0.0
        ML = numpy.array([[[5.0]]])
        R = numpy.array([[[1.0]]])
        h = numpy.array([[[100]]])
        Vs30 = numpy.array([[[760]]])
        

        # get coeffs for this period (C1 -> C10 from table 6)
        coeffs = numpy.array([[[[1.1010]]], [[[ -0.00564]]], [[[0.0055]]],
                              [[[1.08]]], [[[0.01412]]], [[[ 2.6070]]],
                              [[[ -0.528]]], [[[ 0.293]]], [[[ 1.111]]],
                              [[[1.344]]], [[[ 1.355]]], [[[ 1.420]]],
                             [[[0.1392]]], [[[ 0.1584]]], [[[ -0.0529]]]])

        # sigma coefficients for this period (C11 -> C13 from table 6)
        sigma_coeffs = numpy.array([[[[0.604]]], [[[0.321]]]])


        # expected values from Campbell03_check.py
        log_mean_expected = numpy.array([[[2.8272]]])
        log_sigma_expected = numpy.array([[[0.6840]]])

        (log_mean, log_sigma) = model.distribution(periods = period, mag=ML,
                                                   distance=R,depth = h,
                                                   Vs30 = Vs30,coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)
##        print log_mean

        # tests for equality should be quite tight as we check against
        # Campbell03_check.py
        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)


    def test_Zhao_2006_interface(self):
        """Test the Campbell03 model."""

        model_name = 'Zhao_2006_interface'
        model = Ground_motion_specification(model_name)

        ######
        # period = 0.2, ML=7.0, R=10.0,
        # expect lnY=0.0663, sigma=0.4904 (from Campbell03_check.py)
        ######

        period = 0.0
        ML = numpy.array([[[5.0]]])
        R = numpy.array([[[1.0]]])
        h = numpy.array([[[100]]])
        Vs30 = numpy.array([[[760]]])
        

        # get coeffs for this period (C1 -> C10 from table 6)
        coeffs = numpy.array([[[[1.1010]]], [[[ -0.00564]]], [[[0.0055]]],
                              [[[1.08]]], [[[0.01412]]], [[[ 0]]],
                              [[[ 0.293]]], [[[ 1.111]]],
                              [[[1.344]]], [[[ 1.355]]], [[[ 1.420]]],
                              [[[ 0.0]]], [[[ 0.0]]]])

        # sigma coefficients for this period (C11 -> C13 from table 6)
        sigma_coeffs = numpy.array([[[[0.604]]], [[[0.308]]]])


        # expected values from Campbell03_check.py
        log_mean_expected = numpy.array([[[ 0.1255]]])
        log_sigma_expected = numpy.array([[[0.6780]]])

        (log_mean, log_sigma) = model.distribution(periods = period, mag=ML,
                                                   distance=R,depth = h,
                                                   Vs30 = Vs30,coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)
##        print log_mean

        # tests for equality should be quite tight as we check against
        # Campbell03_check.py
        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)


    def test_Atkinson_2003_interface(self):
        """Test the Campbell03 model."""

        model_name = 'Atkinson_2003_interface'
        model = Ground_motion_specification(model_name)

        ######
        # period = 0.2, ML=7.0, R=10.0,
        # expect lnY=0.0663, sigma=0.4904 (from Campbell03_check.py)
        ######

        period = 0.0
        ML = numpy.array([[[5.0]]])
        R = numpy.array([[[10.0]]])
        h = numpy.array([[[100]]])
        Vs30 = numpy.array([[[760]]])
        

        # get coeffs for this period (C1 -> C10 from table 6)
        coeffs = numpy.array([[[[2.9910]]], [[[ 3.1400]]], [[[2.7900]]],
                              [[[0.03525]]], [[[0.00759]]], [[[ -0.00206]]],
                              [[[0.1900 ]]], [[[0.2400 ]]], [[[ 0.2900]]],
                              ])

        # sigma coefficients for this period (C11 -> C13 from table 6)
        sigma_coeffs = numpy.array([[[[0.2]]], [[[0.11]]]])


        # expected values from Campbell03_check.py
        log_mean_expected = numpy.array([[[ -2.0876]]])
        log_sigma_expected = numpy.array([[[0.5256]]])

        (log_mean, log_sigma) = model.distribution(periods = period, mag=ML,
                                                   distance=R,depth = h,
                                                   Vs30 = Vs30,coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)
##        print log_mean

        # tests for equality should be quite tight as we check against
        # Campbell03_check.py
        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

    def test_Atkinson_2003_intraslab(self):
        """Test the Campbell03 model."""

        model_name = 'Atkinson_2003_intraslab'
        model = Ground_motion_specification(model_name)

        ######
        # period = 0.2, ML=7.0, R=10.0,
        # expect lnY=0.0663, sigma=0.4904 (from Campbell03_check.py)
        ######

        period = 0.0
        ML = numpy.array([[[5.0]]])
        R = numpy.array([[[10.0]]])
        h = numpy.array([[[100]]])
        Vs30 = numpy.array([[[500]]])
        

        # get coeffs for this period (C1 -> C10 from table 6)
        coeffs = numpy.array([[[[-0.04713]]], [[[ 0.1]]], [[[-0.25]]],
                              [[[0.6909]]], [[[0.0113]]], [[[ -0.00202]]],
                              [[[0.19 ]]], [[[0.2400 ]]], [[[ 0.2900]]],
                              ])

        # sigma coefficients for this period (C11 -> C13 from table 6)
        sigma_coeffs = numpy.array([[[[0.23]]], [[[0.14]]]])


        # expected values from Campbell03_check.py
        log_mean_expected = numpy.array([[[ -0.6462]]])
        log_sigma_expected = numpy.array([[[ 0.6200]]])

        (log_mean, log_sigma) = model.distribution(periods = period, mag=ML,
                                                   distance=R,depth = h,
                                                   Vs30 = Vs30,coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)
##        print log_mean

        # tests for equality should be quite tight as we check against
        # Campbell03_check.py
        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)
         
    def test_Akkar_2010_crustal(self):
        """Test the Akkar2010 model."""

        model_name = 'Akkar_2010_crustal'
        model = Ground_motion_specification(model_name)

        ######
        # period = 0.2, ML=7.0, R=10.0,
        # expect lnY=0.0663, sigma=0.4904 (from Campbell03_check.py)
        ######

        period = 0.0
        ML = numpy.array([[[5.0]]])
        R = numpy.array([[[10.0]]])
        Vs30 = numpy.array([[[760]]])
        FT = numpy.array([[[0]]])
        

        # get coeffs for this period (C1 -> C10 from table 6)
        coeffs = numpy.array([[[[1.04159]]], [[[0.91333 ]]], [[[-0.08140]]],
                              [[[-2.92728]]], [[[0.2812]]], [[[ 7.86638]]],
                              [[[ 0.08753]]], [[[ 0.01527]]], [[[ -0.04189]]],
                              [[[0.08015]]]])

        # sigma coefficients for this period (C11 -> C13 from table 6)
        sigma_coeffs = numpy.array([[[[0.261]]], [[[0.0994]]]])


        # expected values from Campbell03_check.py
        log_mean_expected = numpy.array([[[ -2.3456]]])
        log_sigma_expected = numpy.array([[[0.6431]]])

        (log_mean, log_sigma) = model.distribution(periods = period, mag=ML,
                                                   distance=R,fault_type = FT,
                                                   Vs30 = Vs30,coefficient=coeffs,
                                                   sigma_coefficient=
                                                       sigma_coeffs)
##        print log_mean

        # tests for equality should be quite tight as we check against
        # Campbell03_check.py
        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_mean=%s, expected=%s'
               % (period, ML, R, str(log_mean), str(log_mean_expected)))
        self.failUnless(allclose(asarray(log_mean), log_mean_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)

        msg = ('T=%.1f, ML=%.1f, R=%.1f: log_sigma=%s, expected=%s'
               % (period, ML, R, str(log_sigma), str(log_sigma_expected)))
        self.failUnless(allclose(asarray(log_sigma), log_sigma_expected,
                                         rtol=1.0e-4, atol=1.0e-4),
                                 msg)      
        
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_ground_motion_interface,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)

