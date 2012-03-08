
import unittest
from scipy import array, allclose, log
from eqrm_code.ground_motion_specification import Ground_motion_specification
from eqrm_code.ground_motion_interface import *

class Test_Boore_08(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_Boore_08(self):
        c_tab = array([
#T(s)   e1       e2       e3       e4      e5       e6      e7      Mh    c1       c2       c3      Mref Rref h     blin  Vref  b1     b2   V1  V2  a1   pga_low a2   Sig   TauU  SigTU TauM  SigTM
[0.010,-0.52883,-0.49429,-0.74551,-0.49966,0.28897,-0.10019,0.00000,6.75,-0.66220, 0.12000,-0.01151,4.5, 1.0, 1.35,-0.360,760, -0.640,-0.14,180,300,0.03,0.06,   0.09,0.502,0.267,0.569,0.262,0.566],
[0.020,-0.52192,-0.48508,-0.73906,-0.48895,0.25144,-0.11006,0.00000,6.75,-0.66600, 0.12280,-0.01151,4.5, 1.0, 1.35,-0.340,760, -0.630,-0.12,180,300,0.03,0.06,   0.09,0.502,0.267,0.569,0.262,0.566],
[0.030,-0.45285,-0.41831,-0.66722,-0.42229,0.17976,-0.12858,0.00000,6.75,-0.69010, 0.12830,-0.01151,4.5, 1.0, 1.35,-0.330,760, -0.620,-0.11,180,300,0.03,0.06,   0.09,0.507,0.276,0.578,0.274,0.576],
[0.050,-0.28476,-0.25022,-0.48462,-0.26092,0.06369,-0.15752,0.00000,6.75,-0.71700, 0.13170,-0.01151,4.5, 1.0, 1.35,-0.290,760, -0.640,-0.11,180,300,0.03,0.06,   0.09,0.516,0.286,0.589,0.286,0.589],
[0.075, 0.00767, 0.04912,-0.20578, 0.02706,0.01170,-0.17051,0.00000,6.75,-0.72050, 0.12370,-0.01151,4.5, 1.0, 1.55,-0.230,760, -0.640,-0.11,180,300,0.03,0.06,   0.09,0.513,0.322,0.606,0.320,0.606],
[0.10,  0.20109, 0.23102, 0.03058, 0.22193,0.04697,-0.15948,0.00000,6.75,-0.70810, 0.11170,-0.01151,4.5, 1.0, 1.68,-0.250,760, -0.600,-0.13,180,300,0.03,0.06,   0.09,0.520,0.313,0.608,0.318,0.608],
[0.15,  0.46128, 0.48661, 0.30185, 0.49328,0.17990,-0.14539,0.00000,6.75,-0.69610, 0.09884,-0.01113,4.5, 1.0, 1.86,-0.280,760, -0.530,-0.18,180,300,0.03,0.06,   0.09,0.518,0.288,0.592,0.290,0.594],
[0.20,  0.57180, 0.59253, 0.40860, 0.61472,0.52729,-0.12964,0.00102,6.75,-0.58300, 0.04273,-0.00952,4.5, 1.0, 1.98,-0.310,760, -0.520,-0.19,180,300,0.03,0.06,   0.09,0.523,0.283,0.596,0.288,0.596],
[0.25,  0.51884, 0.53496, 0.33880, 0.57747,0.60880,-0.13843,0.08607,6.75,-0.57260, 0.02977,-0.00837,4.5, 1.0, 2.07,-0.390,760, -0.520,-0.16,180,300,0.03,0.06,   0.09,0.527,0.267,0.592,0.267,0.592],
[0.30,  0.43825, 0.44516, 0.25356, 0.51990,0.64472,-0.15694,0.10601,6.75,-0.55430, 0.01955,-0.00750,4.5, 1.0, 2.14,-0.440,760, -0.520,-0.14,180,300,0.03,0.06,   0.09,0.546,0.272,0.608,0.269,0.608],
[0.40,  0.39220, 0.40602, 0.21398, 0.46080,0.78610,-0.07843,0.02262,6.75,-0.64430, 0.04394,-0.00626,4.5, 1.0, 2.24,-0.500,760, -0.510,-0.10,180,300,0.03,0.06,   0.09,0.541,0.267,0.603,0.267,0.603],
[0.50,  0.18957, 0.19878, 0.00967, 0.26337,0.76837,-0.09054,0.00000,6.75,-0.69140, 0.06080,-0.00540,4.5, 1.0, 2.32,-0.600,760, -0.500,-0.06,180,300,0.03,0.06,   0.09,0.555,0.265,0.615,0.265,0.615],
[0.75, -0.21338,-0.19496,-0.49176,-0.10813,0.75179,-0.14053,0.10302,6.75,-0.74080, 0.07518,-0.00409,4.5, 1.0, 2.46,-0.690,760, -0.470, 0.00,180,300,0.03,0.06,   0.09,0.571,0.311,0.649,0.299,0.645],
[1.00, -0.46896,-0.43443,-0.78465,-0.39330,0.67880,-0.18257,0.05393,6.75,-0.81830, 0.10270,-0.00334,4.5, 1.0, 2.54,-0.700,760, -0.440, 0.00,180,300,0.03,0.06,   0.09,0.573,0.318,0.654,0.302,0.647],
[1.50, -0.86271,-0.79593,-1.20902,-0.88085,0.70689,-0.25950,0.19082,6.75,-0.83030, 0.09793,-0.00255,4.5, 1.0, 2.66,-0.720,760, -0.400, 0.00,180,300,0.03,0.06,   0.09,0.566,0.382,0.684,0.373,0.679],
[2.00, -1.22652,-1.15514,-1.57697,-1.27669,0.77989,-0.29657,0.29888,6.75,-0.82850, 0.09432,-0.00217,4.5, 1.0, 2.73,-0.730,760, -0.380, 0.00,180,300,0.03,0.06,   0.09,0.580,0.398,0.702,0.389,0.700],
[3.00, -1.82979,-1.74690,-2.22584,-1.91814,0.77966,-0.45384,0.67466,6.75,-0.78440, 0.07282,-0.00191,4.5, 1.0, 2.83,-0.740,760, -0.340, 0.00,180,300,0.03,0.06,   0.09,0.566,0.410,0.700,0.401,0.695],
[4.00, -2.24656,-2.15906,-2.58228,-2.38168,1.24961,-0.35874,0.79508,6.75,-0.68540, 0.03758,-0.00191,4.5, 1.0, 2.89,-0.750,760, -0.310, 0.00,180,300,0.03,0.06,   0.09,0.583,0.394,0.702,0.385,0.698],
[5.00, -1.28408,-1.21270,-1.50904,-1.41093,0.14271,-0.39006,0.00000,8.50,-0.50960,-0.02391,-0.00191,4.5, 1.0, 2.93,-0.750,760, -0.291, 0.00,180,300,0.03,0.06,   0.09,0.601,0.414,0.730,0.437,0.744],
[7.50, -1.43145,-1.31632,-1.81022,-1.59217,0.52407,-0.37578,0.00000,8.50,-0.37240,-0.06568,-0.00191,4.5, 1.0, 3.00,-0.692,760, -0.247, 0.00,180,300,0.03,0.06,   0.09,0.626,0.465,0.781,0.477,0.787],
[10.0, -2.15446,-2.16137,-2.53323,-2.14635,0.40387,-0.48492,0.00000,8.50,-0.09824,-0.13800,-0.00191,4.5, 1.0, 3.04,-0.650,760, -0.215, 0.00,180,300,0.03,0.06,   0.09,0.645,0.355,0.735,0.477,0.801],
[ 0.0, -0.53804,-0.50350,-0.75472,-0.50970,0.28805,-0.10164,0.00000,6.75,-0.66050, 0.11970,-0.01151,4.5, 1.0, 1.35,-0.360,760, -0.640,-0.14,180,300,0.03,0.06,   0.09,0.502,0.265,0.566,0.260,0.564],
[-1.0,  5.00121, 5.04727, 4.63188, 5.08210,0.18322,-0.12736,0.00000,8.50,-0.87370, 0.10060,-0.00334,4.5, 1.0, 2.54,-0.600,760, -0.500,-0.06,180,300,0.03,0.06,   0.09,0.500,0.286,0.576,0.256,0.560],
])

        # generate coefficients for varying periods
        #[c1, c2, c3, h, e1, e2, e3, e4, e5, e6, e7, mh, sig, tu, sigtu, tm, sigtm, blin, b1, b2]
        # 9   10  11  14 1   2   3   4   5   6   7   8   24   25  26     27  28     15    17  18
        # 0.01
        c_dict = {}
        periods = [('0.01', 0), ('0.20', 7), ('1.00', 13), ('3.00', 16)]
        for (T, i) in periods:
            c = array([c_tab[i][9], c_tab[i][10], c_tab[i][11], c_tab[i][14], c_tab[i][1],
                       c_tab[i][2], c_tab[i][3], c_tab[i][4], c_tab[i][5], c_tab[i][6],
                       c_tab[i][7], c_tab[i][8], c_tab[i][24], c_tab[i][25], c_tab[i][26],
                       c_tab[i][27], c_tab[i][28], c_tab[i][15], c_tab[i][17], c_tab[i][18]])
            c.shape = (-1, 1, 1, 1)
            c_dict[T] = c
        s_tab = array([[0.566, 0.569, 0.569, 0.578, 0.589, 0.606, 0.608, 0.592, 0.596, 0.592, 0.608,
0.603, 0.615, 0.649, 0.654, 0.684, 0.702, 0.7, 0.702, 0.73, 0.781, 0.735]])

        s_dict = {}
        periods = [('0.01', 0), ('0.20', 0), ('1.00', 0), ('3.00', 0)]
        for (T, i) in periods:
            s = s_tab[i]
            s.shape = (-1, 1, 1, 1)
            s_dict[T] = s

        mrtol = 1.0e-2
        matol = 1.0e-2

        srtol = 5.0e-3
        satol = 5.0e-3

        # now run all tests
        model_name = 'Boore_08'
        model = Ground_motion_specification(model_name)

        # T=0.01, M=4.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        fault_type = array([[[2]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-2.530992]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.530992), abs((log_mean--2.530992)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.530992]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-3.002555]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.002555), abs((log_mean--3.002555)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.002555]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-3.179415]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.179415), abs((log_mean--3.179415)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.179415]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-3.300900]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.300900), abs((log_mean--3.300900)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.300900]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-3.381395]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.381395), abs((log_mean--3.381395)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.381395]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-3.065940]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.065940), abs((log_mean--3.065940)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.065940]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-3.540115]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.540115), abs((log_mean--3.540115)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.540115]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-3.717279]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.717279), abs((log_mean--3.717279)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.717279]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-3.839237]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.839237), abs((log_mean--3.839237)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.839237]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-3.919551]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.919551), abs((log_mean--3.919551)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.919551]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-3.894183]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.894183), abs((log_mean--3.894183)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.894183]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-4.368518]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.368518), abs((log_mean--4.368518)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.368518]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-4.545958]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.545958), abs((log_mean--4.545958)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.545958]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-4.667471]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.667471), abs((log_mean--4.667471)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.667471]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-4.747771]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.747771), abs((log_mean--4.747771)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.747771]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-4.681511]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.681511), abs((log_mean--4.681511)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.681511]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-5.155950]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.155950), abs((log_mean--5.155950)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.155950]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-5.333116]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.333116), abs((log_mean--5.333116)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.333116]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-5.454737]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.454737), abs((log_mean--5.454737)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.454737]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-5.535053]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.535053), abs((log_mean--5.535053)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.535053]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-5.757183]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.757183), abs((log_mean--5.757183)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.757183]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-6.231754]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.231754), abs((log_mean--6.231754)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.231754]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-6.408800]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.408800), abs((log_mean--6.408800)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.408800]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-6.530690]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.530690), abs((log_mean--6.530690)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.530690]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-6.610618]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.610618), abs((log_mean--6.610618)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.610618]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-7.408796]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.408796), abs((log_mean--7.408796)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.408796]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-7.883265]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.883265), abs((log_mean--7.883265)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.883265]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-8.060401]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.060401), abs((log_mean--8.060401)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.060401]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-8.182151]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.182151), abs((log_mean--8.182151)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.182151]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-8.262551]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.262551), abs((log_mean--8.262551)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.262551]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-1.836966]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.836966), abs((log_mean--1.836966)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.836966]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-2.109488]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.109488), abs((log_mean--2.109488)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.109488]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-2.258568]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.258568), abs((log_mean--2.258568)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.258568]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-2.363822]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.363822), abs((log_mean--2.363822)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.363822]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-2.444149]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.444149), abs((log_mean--2.444149)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.444149]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-2.112792]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.112792), abs((log_mean--2.112792)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.112792]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-2.534643]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.534643), abs((log_mean--2.534643)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.534643]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-2.704556]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.704556), abs((log_mean--2.704556)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.704556]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-2.821947]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.821947), abs((log_mean--2.821947)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.821947]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-2.902242]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.902242), abs((log_mean--2.902242)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.902242]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-2.767959]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.767959), abs((log_mean--2.767959)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.767959]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-3.242400]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.242400), abs((log_mean--3.242400)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.242400]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-3.419463]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.419463), abs((log_mean--3.419463)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.419463]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-3.541149]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.541149), abs((log_mean--3.541149)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.541149]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-3.621595]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.621595), abs((log_mean--3.621595)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.621595]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-3.472156]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.472156), abs((log_mean--3.472156)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.472156]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-3.946614]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.946614), abs((log_mean--3.946614)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.946614]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-4.123979]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.123979), abs((log_mean--4.123979)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.123979]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-4.245400]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.245400), abs((log_mean--4.245400)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.245400]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-4.326024]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.326024), abs((log_mean--4.326024)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.326024]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-4.464539]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.464539), abs((log_mean--4.464539)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.464539]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-4.939245]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.939245), abs((log_mean--4.939245)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.939245]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-5.116496]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.116496), abs((log_mean--5.116496)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.116496]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-5.238163]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.238163), abs((log_mean--5.238163)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.238163]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-5.318520]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.318520), abs((log_mean--5.318520)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.318520]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-6.033120]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.033120), abs((log_mean--6.033120)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.033120]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-6.507638]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.507638), abs((log_mean--6.507638)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.507638]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-6.684612]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.684612), abs((log_mean--6.684612)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.684612]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-6.806102]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.806102), abs((log_mean--6.806102)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.806102]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=5.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=5.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-6.886973]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.886973), abs((log_mean--6.886973)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.886973]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=5.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-1.496556]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.496556), abs((log_mean--1.496556)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.496556]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-1.443923]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.443923), abs((log_mean--1.443923)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.443923]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-1.547873]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.547873), abs((log_mean--1.547873)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.547873]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-1.627093]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.627093), abs((log_mean--1.627093)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.627093]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-1.707051]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.707051), abs((log_mean--1.707051)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.707051]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-1.672378]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.672378), abs((log_mean--1.672378)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.672378]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-1.785579]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.785579), abs((log_mean--1.785579)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.785579]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-1.912572]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.912572), abs((log_mean--1.912572)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.912572]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-2.005448]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.005448), abs((log_mean--2.005448)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.005448]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-2.085862]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.085862), abs((log_mean--2.085862)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.085862]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.971125]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.971125), abs((log_mean--1.971125)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.971125]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-2.339664]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.339664), abs((log_mean--2.339664)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.339664]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-2.502134]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.502134), abs((log_mean--2.502134)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.502134]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-2.615380]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.615380), abs((log_mean--2.615380)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.615380]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-2.695628]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.695628), abs((log_mean--2.695628)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.695628]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-2.470176]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.470176), abs((log_mean--2.470176)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.470176]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-2.938974]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.938974), abs((log_mean--2.938974)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.938974]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-3.115192]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.115192), abs((log_mean--3.115192)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.115192]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-3.236531]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.236531), abs((log_mean--3.236531)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.236531]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-3.317040]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.317040), abs((log_mean--3.317040)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.317040]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-3.372902]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.372902), abs((log_mean--3.372902)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.372902]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-3.847172]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.847172), abs((log_mean--3.847172)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.847172]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-4.024073]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.024073), abs((log_mean--4.024073)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.024073]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-4.145848]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.145848), abs((log_mean--4.145848)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.145848]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-4.226734]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.226734), abs((log_mean--4.226734)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.226734]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-4.857871]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.857871), abs((log_mean--4.857871)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.857871]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-5.332288]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.332288), abs((log_mean--5.332288)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.332288]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-5.509532]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.509532), abs((log_mean--5.509532)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.509532]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-5.631276]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.631276), abs((log_mean--5.631276)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.631276]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=6.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=6.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-5.711714]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.711714), abs((log_mean--5.711714)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.711714]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=6.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-1.278696]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.278696), abs((log_mean--1.278696)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.278696]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-1.018877]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.018877), abs((log_mean--1.018877)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.018877]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-1.094222]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.094222), abs((log_mean--1.094222)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.094222]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-1.156453]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.156453), abs((log_mean--1.156453)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.156453]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-1.236840]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.236840), abs((log_mean--1.236840)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.236840]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-1.417166]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.417166), abs((log_mean--1.417166)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.417166]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-1.288079]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.288079), abs((log_mean--1.288079)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.288079]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-1.381506]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.381506), abs((log_mean--1.381506)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.381506]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-1.454573]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.454573), abs((log_mean--1.454573)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.454573]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-1.534794]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.534794), abs((log_mean--1.534794)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.534794]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.649739]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.649739), abs((log_mean--1.649739)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.649739]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-1.741256]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.741256), abs((log_mean--1.741256)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.741256]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-1.864976]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.864976), abs((log_mean--1.864976)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.864976]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-1.956163]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.956163), abs((log_mean--1.956163)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.956163]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-2.036382]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.036382), abs((log_mean--2.036382)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.036382]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.901128]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.901128), abs((log_mean--1.901128)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.901128]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-2.227478]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.227478), abs((log_mean--2.227478)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.227478]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-2.384229]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.384229), abs((log_mean--2.384229)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.384229]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-2.493988]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.493988), abs((log_mean--2.493988)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.493988]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-2.574394]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.574394), abs((log_mean--2.574394)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.574394]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-2.550021]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.550021), abs((log_mean--2.550021)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.550021]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-3.022076]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.022076), abs((log_mean--3.022076)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.022076]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-3.198828]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.198828), abs((log_mean--3.198828)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.198828]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-3.320355]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.320355), abs((log_mean--3.320355)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.320355]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-3.400698]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.400698), abs((log_mean--3.400698)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.400698]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-3.949206]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.949206), abs((log_mean--3.949206)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.949206]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-4.423682]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.423682), abs((log_mean--4.423682)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.423682]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-4.600183]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.600183), abs((log_mean--4.600183)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.600183]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-4.722378]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.722378), abs((log_mean--4.722378)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.722378]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=7.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=7.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-4.802646]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.802646), abs((log_mean--4.802646)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.802646]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=7.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-1.186788]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.186788), abs((log_mean--1.186788)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.186788]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.840488]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.840488), abs((log_mean--0.840488)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.840488]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-0.903868]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.903868), abs((log_mean--0.903868)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.903868]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-0.959198]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.959198), abs((log_mean--0.959198)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.959198]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-1.039589]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.039589), abs((log_mean--1.039589)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.039589]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-1.288079]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.288079), abs((log_mean--1.288079)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.288079]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-1.037611]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.037611), abs((log_mean--1.037611)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.037611]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-1.114132]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.114132), abs((log_mean--1.114132)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.114132]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-1.177331]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.177331), abs((log_mean--1.177331)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.177331]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-1.257725]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.257725), abs((log_mean--1.257725)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.257725]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.470111]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.470111), abs((log_mean--1.470111)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.470111]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-1.391910]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.391910), abs((log_mean--1.391910)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.391910]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-1.492544]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.492544), abs((log_mean--1.492544)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.492544]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-1.569256]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.569256), abs((log_mean--1.569256)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.569256]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-1.649739]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.649739), abs((log_mean--1.649739)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.649739]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.680934]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.680934), abs((log_mean--1.680934)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.680934]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-1.803023]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.803023), abs((log_mean--1.803023)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.803023]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-1.931022]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.931022), abs((log_mean--1.931022)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.931022]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-2.024196]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.024196), abs((log_mean--2.024196)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.024196]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-2.104554]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.104554), abs((log_mean--2.104554)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.104554]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-2.073062]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.073062), abs((log_mean--2.073062)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.073062]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-2.483028]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.483028), abs((log_mean--2.483028)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.483028]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-2.651292]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.651292), abs((log_mean--2.651292)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.651292]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-2.767800]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.767800), abs((log_mean--2.767800)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.767800]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-2.848002]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.848002), abs((log_mean--2.848002)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.848002]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-3.313187]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.313187), abs((log_mean--3.313187)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.313187]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-3.787595]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.787595), abs((log_mean--3.787595)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.787595]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-3.964896]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.964896), abs((log_mean--3.964896)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.964896]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-4.086376]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.086376), abs((log_mean--4.086376)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.086376]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=8.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=8.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-4.166915]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.166915), abs((log_mean--4.166915)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.166915]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=8.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-1.095118]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.095118), abs((log_mean--1.095118)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.095118]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.662230]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.662230), abs((log_mean--0.662230)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.662230]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-0.713554]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.713554), abs((log_mean--0.713554)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.713554]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-0.761854]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.761854), abs((log_mean--0.761854)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.761854]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-0.842111]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.842111), abs((log_mean--0.842111)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.842111]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-1.159318]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.159318), abs((log_mean--1.159318)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.159318]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-0.787018]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.787018), abs((log_mean--0.787018)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.787018]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-0.846531]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.846531), abs((log_mean--0.846531)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.846531]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-0.899925]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.899925), abs((log_mean--0.899925)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.899925]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-0.980296]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.980296), abs((log_mean--0.980296)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.980296]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.290621]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.290621), abs((log_mean--1.290621)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.290621]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-1.042705]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.042705), abs((log_mean--1.042705)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.042705]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-1.119632]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.119632), abs((log_mean--1.119632)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.119632]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-1.182864]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.182864), abs((log_mean--1.182864)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.182864]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-1.263369]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.263369), abs((log_mean--1.263369)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.263369]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.463175]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.463175), abs((log_mean--1.463175)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.463175]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-1.378723]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.378723), abs((log_mean--1.378723)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.378723]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-1.478410]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.478410), abs((log_mean--1.478410)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.478410]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-1.554950]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.554950), abs((log_mean--1.554950)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.554950]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-1.635269]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.635269), abs((log_mean--1.635269)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.635269]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-1.769020]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.769020), abs((log_mean--1.769020)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.769020]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-1.975442]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.975442), abs((log_mean--1.975442)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.975442]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-2.115276]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.115276), abs((log_mean--2.115276)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.115276]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-2.215490]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.215490), abs((log_mean--2.215490)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.215490]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-2.295609]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.295609), abs((log_mean--2.295609)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.295609]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-2.677715]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.677715), abs((log_mean--2.677715)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.677715]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-3.151918]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.151918), abs((log_mean--3.151918)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.151918]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-3.328970]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.328970), abs((log_mean--3.328970)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.328970]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-3.450808]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.450808), abs((log_mean--3.450808)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.450808]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=9.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=9.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-3.531192]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.531192), abs((log_mean--3.531192)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.531192]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=9.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-2.254748]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.254748), abs((log_mean--2.254748)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.254748]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-2.631089]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.631089), abs((log_mean--2.631089)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.631089]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-2.798686]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.798686), abs((log_mean--2.798686)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.798686]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-2.912127]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.912127), abs((log_mean--2.912127)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.912127]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-2.981435]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.981435), abs((log_mean--2.981435)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.981435]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-2.683992]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.683992), abs((log_mean--2.683992)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.683992]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-3.062727]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.062727), abs((log_mean--3.062727)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.062727]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-3.230695]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.230695), abs((log_mean--3.230695)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.230695]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-3.344439]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.344439), abs((log_mean--3.344439)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.344439]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-3.413675]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.413675), abs((log_mean--3.413675)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.413675]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-3.369699]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.369699), abs((log_mean--3.369699)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.369699]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-3.748629]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.748629), abs((log_mean--3.748629)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.748629]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-3.916533]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.916533), abs((log_mean--3.916533)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.916533]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-4.030244]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.030244), abs((log_mean--4.030244)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.030244]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-4.099558]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.099558), abs((log_mean--4.099558)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.099558]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-4.024632]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.024632), abs((log_mean--4.024632)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.024632]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-4.403863]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.403863), abs((log_mean--4.403863)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.403863]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-4.571735]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.571735), abs((log_mean--4.571735)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.571735]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-4.685405]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.685405), abs((log_mean--4.685405)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.685405]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-4.754599]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.754599), abs((log_mean--4.754599)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.754599]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-4.919196]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.919196), abs((log_mean--4.919196)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.919196]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-5.297917]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.297917), abs((log_mean--5.297917)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.297917]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-5.466026]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.466026), abs((log_mean--5.466026)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.466026]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-5.579885]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.579885), abs((log_mean--5.579885)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.579885]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-5.649010]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.649010), abs((log_mean--5.649010)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.649010]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-6.289871]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.289871), abs((log_mean--6.289871)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.289871]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-6.668738]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.668738), abs((log_mean--6.668738)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.668738]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-6.836365]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.836365), abs((log_mean--6.836365)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.836365]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-6.950558]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.950558), abs((log_mean--6.950558)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.950558]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-7.019693]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.019693), abs((log_mean--7.019693)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.019693]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-1.276185]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.276185), abs((log_mean--1.276185)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.276185]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-1.507784]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.507784), abs((log_mean--1.507784)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.507784]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-1.637837]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.637837), abs((log_mean--1.637837)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.637837]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-1.729912]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.729912), abs((log_mean--1.729912)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.729912]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-1.798784]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.798784), abs((log_mean--1.798784)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.798784]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-1.528319]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.528319), abs((log_mean--1.528319)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.528319]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-1.868209]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.868209), abs((log_mean--1.868209)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.868209]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-2.026470]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.026470), abs((log_mean--2.026470)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.026470]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-2.134532]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.134532), abs((log_mean--2.134532)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.134532]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-2.203645]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.203645), abs((log_mean--2.203645)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.203645]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-2.121097]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.121097), abs((log_mean--2.121097)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.121097]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-2.500061]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.500061), abs((log_mean--2.500061)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.500061]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-2.668157]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.668157), abs((log_mean--2.668157)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.668157]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-2.781912]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.781912), abs((log_mean--2.781912)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.781912]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-2.851113]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.851113), abs((log_mean--2.851113)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.851113]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-2.746999]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.746999), abs((log_mean--2.746999)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.746999]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-3.125613]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.125613), abs((log_mean--3.125613)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.125613]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-3.293599]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.293599), abs((log_mean--3.293599)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.293599]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-3.407618]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.407618), abs((log_mean--3.407618)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.407618]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-3.476676]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.476676), abs((log_mean--3.476676)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.476676]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-3.611918]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.611918), abs((log_mean--3.611918)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.611918]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-3.990525]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.990525), abs((log_mean--3.990525)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.990525]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-4.158563]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.158563), abs((log_mean--4.158563)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.158563]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-4.272276]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.272276), abs((log_mean--4.272276)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.272276]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-4.341269]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.341269), abs((log_mean--4.341269)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.341269]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-4.952885]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.952885), abs((log_mean--4.952885)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.952885]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-5.331667]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.331667), abs((log_mean--5.331667)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.331667]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-5.499699]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.499699), abs((log_mean--5.499699)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.499699]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-5.613576]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.613576), abs((log_mean--5.613576)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.613576]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=5.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=5.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-5.682510]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.682510), abs((log_mean--5.682510)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.682510]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=5.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-0.686966]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.686966), abs((log_mean--0.686966)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.686966]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.681614]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.681614), abs((log_mean--0.681614)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.681614]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-0.750353]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.750353), abs((log_mean--0.750353)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.750353]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-0.806316]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.806316), abs((log_mean--0.806316)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.806316]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-0.875629]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.875629), abs((log_mean--0.875629)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.875629]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-0.894285]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.894285), abs((log_mean--0.894285)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.894285]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-1.009778]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.009778), abs((log_mean--1.009778)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.009778]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-1.109875]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.109875), abs((log_mean--1.109875)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.109875]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-1.184170]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.184170), abs((log_mean--1.184170)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.184170]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-1.253163]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.253163), abs((log_mean--1.253163)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.253163]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.240983]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.240983), abs((log_mean--1.240983)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.240983]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-1.542714]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.542714), abs((log_mean--1.542714)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.542714]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-1.690648]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.690648), abs((log_mean--1.690648)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.690648]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-1.792760]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.792760), abs((log_mean--1.792760)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.792760]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-1.861753]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.861753), abs((log_mean--1.861753)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.861753]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.734434]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.734434), abs((log_mean--1.734434)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.734434]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-2.108664]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.108664), abs((log_mean--2.108664)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.108664]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-2.275943]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.275943), abs((log_mean--2.275943)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.275943]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-2.389015]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.389015), abs((log_mean--2.389015)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.389015]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-2.458187]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.458187), abs((log_mean--2.458187)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.458187]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-2.563560]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.563560), abs((log_mean--2.563560)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.563560]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-2.942192]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.942192), abs((log_mean--2.942192)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.942192]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-3.110246]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.110246), abs((log_mean--3.110246)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.110246]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-3.224140]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.224140), abs((log_mean--3.224140)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.224140]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-3.293330]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.293330), abs((log_mean--3.293330)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.293330]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-3.875209]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.875209), abs((log_mean--3.875209)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.875209]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-4.253809]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.253809), abs((log_mean--4.253809)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.253809]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-4.422016]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.422016), abs((log_mean--4.422016)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.422016]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-4.535644]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.535644), abs((log_mean--4.535644)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.535644]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=6.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=6.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-4.605170]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.605170), abs((log_mean--4.605170)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.605170]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=6.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-0.358963]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.358963), abs((log_mean--0.358963)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.358963]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.202728]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.202728), abs((log_mean--0.202728)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.202728]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-0.232563]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.232563), abs((log_mean--0.232563)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.232563]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-0.265790]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.265790), abs((log_mean--0.265790)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.265790]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-0.335053]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.335053), abs((log_mean--0.335053)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.335053]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-0.574831]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.574831), abs((log_mean--0.574831)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.574831]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-0.514165]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.514165), abs((log_mean--0.514165)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.514165]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-0.568631]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.568631), abs((log_mean--0.568631)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.568631]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-0.616186]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.616186), abs((log_mean--0.616186)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.616186]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-0.685377]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.685377), abs((log_mean--0.685377)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.685377]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-0.919045]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.919045), abs((log_mean--0.919045)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.919045]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-1.018877]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.018877), abs((log_mean--1.018877)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.018877]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-1.114742]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.114742), abs((log_mean--1.114742)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.114742]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-1.186460]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.186460), abs((log_mean--1.186460)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.186460]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-1.255617]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.255617), abs((log_mean--1.255617)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.255617]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.244795]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.244795), abs((log_mean--1.244795)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.244795]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-1.515492]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.515492), abs((log_mean--1.515492)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.515492]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-1.655482]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.655482), abs((log_mean--1.655482)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.655482]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-1.753308]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.753308), abs((log_mean--1.753308)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.753308]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-1.822631]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.822631), abs((log_mean--1.822631)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.822631]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-1.900459]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.900459), abs((log_mean--1.900459)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.900459]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-2.277892]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.277892), abs((log_mean--2.277892)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.277892]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-2.445186]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.445186), abs((log_mean--2.445186)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.445186]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-2.558768]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.558768), abs((log_mean--2.558768)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.558768]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-2.627900]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.627900), abs((log_mean--2.627900)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.627900]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-3.180136]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.180136), abs((log_mean--3.180136)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.180136]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-3.558904]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.558904), abs((log_mean--3.558904)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.558904]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-3.726789]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.726789), abs((log_mean--3.726789)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.726789]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-3.840633]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.840633), abs((log_mean--3.840633)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.840633]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=7.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=7.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-3.910025]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.910025), abs((log_mean--3.910025)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.910025]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=7.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-0.374984]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.374984), abs((log_mean--0.374984)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.374984]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.155719]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.155719), abs((log_mean--0.155719)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.155719]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-0.169129]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.169129), abs((log_mean--0.169129)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.169129]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-0.192978]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.192978), abs((log_mean--0.192978)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.192978]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-0.262144]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.262144), abs((log_mean--0.262144)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.262144]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-0.599657]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.599657), abs((log_mean--0.599657)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.599657]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-0.450201]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.450201), abs((log_mean--0.450201)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.450201]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-0.481752]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.481752), abs((log_mean--0.481752)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.481752]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-0.516006]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.516006), abs((log_mean--0.516006)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.516006]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-0.585190]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.585190), abs((log_mean--0.585190)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.585190]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-0.954512]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.954512), abs((log_mean--0.954512)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.954512]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-0.930643]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.930643), abs((log_mean--0.930643)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.930643]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-0.994793]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.994793), abs((log_mean--0.994793)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.994793]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-1.047824]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.047824), abs((log_mean--1.047824)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.047824]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-1.117184]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.117184), abs((log_mean--1.117184)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.117184]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.286268]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.286268), abs((log_mean--1.286268)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.286268]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-1.408131]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.408131), abs((log_mean--1.408131)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.408131]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-1.509593]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.509593), abs((log_mean--1.509593)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.509593]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-1.584745]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.584745), abs((log_mean--1.584745)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.584745]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-1.653912]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.653912), abs((log_mean--1.653912)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.653912]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-1.766677]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.766677), abs((log_mean--1.766677)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.766677]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-2.098013]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.098013), abs((log_mean--2.098013)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.098013]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-2.253795]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.253795), abs((log_mean--2.253795)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.253795]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-2.360956]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.360956), abs((log_mean--2.360956)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.360956]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-2.430078]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.430078), abs((log_mean--2.430078)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.430078]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-2.952673]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.952673), abs((log_mean--2.952673)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.952673]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-3.331205]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.331205), abs((log_mean--3.331205)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.331205]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-3.499251]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.499251), abs((log_mean--3.499251)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.499251]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-3.613401]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.613401), abs((log_mean--3.613401)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.613401]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=8.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-3.682500]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.682500), abs((log_mean--3.682500)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.682500]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-0.391119]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.391119), abs((log_mean--0.391119)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.391119]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.108588]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.108588), abs((log_mean--0.108588)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.108588]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-0.105805]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.105805), abs((log_mean--0.105805)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.105805]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-0.120023]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.120023), abs((log_mean--0.120023)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.120023]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-0.189225]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.189225), abs((log_mean--0.189225)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.189225]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-0.624554]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.624554), abs((log_mean--0.624554)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.624554]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-0.386251]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.386251), abs((log_mean--0.386251)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.386251]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-0.394822]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.394822), abs((log_mean--0.394822)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.394822]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-0.415819]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.415819), abs((log_mean--0.415819)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.415819]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-0.484995]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.484995), abs((log_mean--0.484995)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.484995]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-0.990206]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.990206), abs((log_mean--0.990206)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.990206]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-0.842576]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.842576), abs((log_mean--0.842576)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.842576]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-0.874669]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.874669), abs((log_mean--0.874669)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.874669]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-0.909067]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.909067), abs((log_mean--0.909067)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.909067]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-0.978432]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.978432), abs((log_mean--0.978432)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.978432]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.329536]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.329536), abs((log_mean--1.329536)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.329536]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-1.301218]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.301218), abs((log_mean--1.301218)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.301218]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-1.364142]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.364142), abs((log_mean--1.364142)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.364142]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-1.416754]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.416754), abs((log_mean--1.416754)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.416754]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-1.485894]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.485894), abs((log_mean--1.485894)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.485894]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-1.777857]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.777857), abs((log_mean--1.777857)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.777857]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-1.961125]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.961125), abs((log_mean--1.961125)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.961125]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-2.078642]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.078642), abs((log_mean--2.078642)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.078642]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-2.162823]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.162823), abs((log_mean--2.162823)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.162823]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-2.232127]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.232127), abs((log_mean--2.232127)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.232127]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-2.725400]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.725400), abs((log_mean--2.725400)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.725400]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-3.103986]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.103986), abs((log_mean--3.103986)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.103986]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-3.272013]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.272013), abs((log_mean--3.272013)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.272013]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-3.385816]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.385816), abs((log_mean--3.385816)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.385816]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=9.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=9.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-3.454915]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.454915), abs((log_mean--3.454915)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.454915]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=9.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-4.085781]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.085781), abs((log_mean--4.085781)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.085781]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-4.747425]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.747425), abs((log_mean--4.747425)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.747425]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-5.031195]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.031195), abs((log_mean--5.031195)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.031195]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-5.232530]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.232530), abs((log_mean--5.232530)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.232530]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-5.388680]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.388680), abs((log_mean--5.388680)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.388680]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-4.629668]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.629668), abs((log_mean--4.629668)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.629668]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-5.293330]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.293330), abs((log_mean--5.293330)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.293330]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-5.576974]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.576974), abs((log_mean--5.576974)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.576974]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-5.778614]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.778614), abs((log_mean--5.778614)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.778614]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-5.934706]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.934706), abs((log_mean--5.934706)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.934706]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-5.453335]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.453335), abs((log_mean--5.453335)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.453335]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-6.117028]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.117028), abs((log_mean--6.117028)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.117028]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-6.400938]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.400938), abs((log_mean--6.400938)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.400938]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-6.601742]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.601742), abs((log_mean--6.601742)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.601742]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-6.758474]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.758474), abs((log_mean--6.758474)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.758474]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-6.135797]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.135797), abs((log_mean--6.135797)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.135797]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-6.799798]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.799798), abs((log_mean--6.799798)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.799798]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-7.083419]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.083419), abs((log_mean--7.083419)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.083419]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-7.284779]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.284779), abs((log_mean--7.284779)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.284779]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-7.440997]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.440997), abs((log_mean--7.440997)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.440997]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-6.904760]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.904760), abs((log_mean--6.904760)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.904760]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-7.568435]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.568435), abs((log_mean--7.568435)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.568435]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-7.852188]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.852188), abs((log_mean--7.852188)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.852188]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-8.053774]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.053774), abs((log_mean--8.053774)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.053774]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-8.209708]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.209708), abs((log_mean--8.209708)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.209708]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-7.841447]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.841447), abs((log_mean--7.841447)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.841447]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-8.504771]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.504771), abs((log_mean--8.504771)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.504771]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-8.789002]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.789002), abs((log_mean--8.789002)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.789002]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-8.990402]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.990402), abs((log_mean--8.990402)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.990402]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-9.146427]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--9.146427), abs((log_mean--9.146427)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-9.146427]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-2.566551]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.566551), abs((log_mean--2.566551)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.566551]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-3.070025]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.070025), abs((log_mean--3.070025)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.070025]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-3.353837]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.353837), abs((log_mean--3.353837)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.353837]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-3.555048]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.555048), abs((log_mean--3.555048)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.555048]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-3.711534]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.711534), abs((log_mean--3.711534)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.711534]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-2.931444]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.931444), abs((log_mean--2.931444)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.931444]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-3.553300]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.553300), abs((log_mean--3.553300)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.553300]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-3.836916]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.836916), abs((log_mean--3.836916)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.836916]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-4.038153]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.038153), abs((log_mean--4.038153)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.038153]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-4.194386]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.194386), abs((log_mean--4.194386)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.194386]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-3.621969]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.621969), abs((log_mean--3.621969)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.621969]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-4.285263]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.285263), abs((log_mean--4.285263)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.285263]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-4.568838]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.568838), abs((log_mean--4.568838)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.568838]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-4.770635]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.770635), abs((log_mean--4.770635)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.770635]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-4.926754]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.926754), abs((log_mean--4.926754)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.926754]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-4.233607]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.233607), abs((log_mean--4.233607)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.233607]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-4.897396]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.897396), abs((log_mean--4.897396)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.897396]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-5.181246]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.181246), abs((log_mean--5.181246)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.181246]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-5.382569]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.382569), abs((log_mean--5.382569)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.382569]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-5.538861]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.538861), abs((log_mean--5.538861)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.538861]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-4.931454]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.931454), abs((log_mean--4.931454)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.931454]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-5.595107]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.595107), abs((log_mean--5.595107)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.595107]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-5.878850]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.878850), abs((log_mean--5.878850)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.878850]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-6.080514]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.080514), abs((log_mean--6.080514)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.080514]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-6.236343]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.236343), abs((log_mean--6.236343)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.236343]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-5.796885]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.796885), abs((log_mean--5.796885)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.796885]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-6.460509]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.460509), abs((log_mean--6.460509)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.460509]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-6.743937]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.743937), abs((log_mean--6.743937)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.743937]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-6.945665]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.945665), abs((log_mean--6.945665)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.945665]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=5.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=5.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-7.101826]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.101826), abs((log_mean--7.101826)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.101826]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=5.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-1.512311]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.512311), abs((log_mean--1.512311)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.512311]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-1.757358]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.757358), abs((log_mean--1.757358)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.757358]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-2.041760]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.041760), abs((log_mean--2.041760)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.041760]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-2.242431]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.242431), abs((log_mean--2.242431)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.242431]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-2.398986]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.398986), abs((log_mean--2.398986)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.398986]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-1.801204]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.801204), abs((log_mean--1.801204)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.801204]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-2.178599]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.178599), abs((log_mean--2.178599)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.178599]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-2.462167]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.462167), abs((log_mean--2.462167)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.462167]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-2.663555]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.663555), abs((log_mean--2.663555)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.663555]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-2.819764]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.819764), abs((log_mean--2.819764)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.819764]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-2.239610]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.239610), abs((log_mean--2.239610)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.239610]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-2.819093]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.819093), abs((log_mean--2.819093)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.819093]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-3.102872]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.102872), abs((log_mean--3.102872)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.102872]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-3.304161]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.304161), abs((log_mean--3.304161)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.304161]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-3.460629]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.460629), abs((log_mean--3.460629)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.460629]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-2.701124]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.701124), abs((log_mean--2.701124)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.701124]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-3.360151]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.360151), abs((log_mean--3.360151)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.360151]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-3.643906]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.643906), abs((log_mean--3.643906)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.643906]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-3.845299]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.845299), abs((log_mean--3.845299)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.845299]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-4.001401]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.001401), abs((log_mean--4.001401)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.001401]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-3.323403]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.323403), abs((log_mean--3.323403)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.323403]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-3.986747]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.986747), abs((log_mean--3.986747)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.986747]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-4.270843]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.270843), abs((log_mean--4.270843)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.270843]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-4.472389]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.472389), abs((log_mean--4.472389)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.472389]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-4.628336]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.628336), abs((log_mean--4.628336)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.628336]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-4.117204]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.117204), abs((log_mean--4.117204)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.117204]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-4.781072]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.781072), abs((log_mean--4.781072)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.781072]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-5.064986]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.064986), abs((log_mean--5.064986)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.064986]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-5.266237]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.266237), abs((log_mean--5.266237)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.266237]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=6.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=6.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-5.422521]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.422521), abs((log_mean--5.422521)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.422521]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=6.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-0.874190]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.874190), abs((log_mean--0.874190)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.874190]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.955291]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.955291), abs((log_mean--0.955291)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.955291]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-1.239255]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.239255), abs((log_mean--1.239255)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.239255]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-1.440539]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.440539), abs((log_mean--1.440539)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.440539]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-1.596522]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.596522), abs((log_mean--1.596522)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.596522]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-1.128247]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.128247), abs((log_mean--1.128247)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.128247]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-1.313416]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.313416), abs((log_mean--1.313416)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.313416]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-1.597015]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.597015), abs((log_mean--1.597015)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.597015]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-1.798784]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.798784), abs((log_mean--1.798784)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.798784]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-1.954749]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.954749), abs((log_mean--1.954749)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.954749]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.502828]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.502828), abs((log_mean--1.502828)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.502828]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-1.862397]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.862397), abs((log_mean--1.862397)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.862397]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-2.146436]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.146436), abs((log_mean--2.146436)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.146436]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-2.347896]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.347896), abs((log_mean--2.347896)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.347896]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-2.504089]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.504089), abs((log_mean--2.504089)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.504089]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.786772]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.786772), abs((log_mean--1.786772)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.786772]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-2.333044]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.333044), abs((log_mean--2.333044)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.333044]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-2.616885]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.616885), abs((log_mean--2.616885)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.616885]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-2.818256]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.818256), abs((log_mean--2.818256)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.818256]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-2.974362]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.974362), abs((log_mean--2.974362)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.974362]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-2.226550]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.226550), abs((log_mean--2.226550)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.226550]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-2.888673]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.888673), abs((log_mean--2.888673)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.888673]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-3.172469]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.172469), abs((log_mean--3.172469)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.172469]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-3.373777]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.373777), abs((log_mean--3.373777)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.373777]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-3.530168]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.530168), abs((log_mean--3.530168)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.530168]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-2.948086]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.948086), abs((log_mean--2.948086)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.948086]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-3.611548]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.611548), abs((log_mean--3.611548)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.611548]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-3.895658]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.895658), abs((log_mean--3.895658)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.895658]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-4.097148]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.097148), abs((log_mean--4.097148)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.097148]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=7.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=7.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-4.253106]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.253106), abs((log_mean--4.253106)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.253106]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=7.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-0.711922]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.711922), abs((log_mean--0.711922)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.711922]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.724225]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.724225), abs((log_mean--0.724225)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.724225]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-1.008132]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.008132), abs((log_mean--1.008132)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.008132]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-1.209320]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.209320), abs((log_mean--1.209320)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.209320]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-1.365708]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.365708), abs((log_mean--1.365708)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.365708]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-0.931404]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.931404), abs((log_mean--0.931404)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.931404]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-1.019709]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.019709), abs((log_mean--1.019709)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.019709]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-1.303425]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.303425), abs((log_mean--1.303425)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.303425]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-1.505078]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.505078), abs((log_mean--1.505078)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.505078]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-1.661258]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.661258), abs((log_mean--1.661258)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.661258]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.252463]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.252463), abs((log_mean--1.252463)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.252463]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-1.477533]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.477533), abs((log_mean--1.477533)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.477533]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-1.761424]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.761424), abs((log_mean--1.761424)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.761424]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-1.962548]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.962548), abs((log_mean--1.962548)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.962548]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-2.119431]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.119431), abs((log_mean--2.119431)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.119431]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.493434]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.493434), abs((log_mean--1.493434)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.493434]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-1.877317]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.877317), abs((log_mean--1.877317)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.877317]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-2.161086]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.161086), abs((log_mean--2.161086)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.161086]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-2.362441]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.362441), abs((log_mean--2.362441)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.362441]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-2.518629]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.518629), abs((log_mean--2.518629)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.518629]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-1.749275]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.749275), abs((log_mean--1.749275)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.749275]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-2.361698]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.361698), abs((log_mean--2.361698)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.361698]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-2.645498]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.645498), abs((log_mean--2.645498)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.645498]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-2.846968]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.846968), abs((log_mean--2.846968)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.846968]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-3.003160]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.003160), abs((log_mean--3.003160)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.003160]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-2.349991]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.349991), abs((log_mean--2.349991)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.349991]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-3.013693]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.013693), abs((log_mean--3.013693)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.013693]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-3.297378]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.297378), abs((log_mean--3.297378)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.297378]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-3.498920]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.498920), abs((log_mean--3.498920)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.498920]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=8.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=8.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-3.655058]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.655058), abs((log_mean--3.655058)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.655058]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=8.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-0.549566]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.549566), abs((log_mean--0.549566)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.549566]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.493313]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.493313), abs((log_mean--0.493313)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.493313]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-0.777181]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.777181), abs((log_mean--0.777181)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.777181]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-0.978432]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.978432), abs((log_mean--0.978432)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.978432]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-1.134758]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.134758), abs((log_mean--1.134758)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.134758]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-0.734386]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.734386), abs((log_mean--0.734386)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.734386]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-0.726084]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.726084), abs((log_mean--0.726084)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.726084]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-1.010052]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.010052), abs((log_mean--1.010052)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.010052]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-1.211333]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.211333), abs((log_mean--1.211333)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.211333]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-1.367669]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.367669), abs((log_mean--1.367669)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.367669]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.002121]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.002121), abs((log_mean--1.002121)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.002121]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-1.092730]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.092730), abs((log_mean--1.092730)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.092730]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-1.376344]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.376344), abs((log_mean--1.376344)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.376344]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-1.577939]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.577939), abs((log_mean--1.577939)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.577939]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-1.733868]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.733868), abs((log_mean--1.733868)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.733868]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.200977]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.200977), abs((log_mean--1.200977)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.200977]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-1.421300]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.421300), abs((log_mean--1.421300)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.421300]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-1.705398]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.705398), abs((log_mean--1.705398)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.705398]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-1.906497]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.906497), abs((log_mean--1.906497)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.906497]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-2.062781]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.062781), abs((log_mean--2.062781)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.062781]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-1.383897]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.383897), abs((log_mean--1.383897)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.383897]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-1.835085]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.835085), abs((log_mean--1.835085)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.835085]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-2.118598]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.118598), abs((log_mean--2.118598)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.118598]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-2.320036]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.320036), abs((log_mean--2.320036)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.320036]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-2.476224]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.476224), abs((log_mean--2.476224)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.476224]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-1.752154]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.752154), abs((log_mean--1.752154)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.752154]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-2.415530]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.415530), abs((log_mean--2.415530)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.415530]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-2.699338]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.699338), abs((log_mean--2.699338)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.699338]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-2.900786]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.900786), abs((log_mean--2.900786)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.900786]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=9.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=9.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-3.056970]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.056970), abs((log_mean--3.056970)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.056970]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=9.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-7.643184]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.643184), abs((log_mean--7.643184)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.643184]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-8.292451]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.292451), abs((log_mean--8.292451)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.292451]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-8.592456]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.592456), abs((log_mean--8.592456)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.592456]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-8.805542]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.805542), abs((log_mean--8.805542)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.805542]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-8.970536]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.970536), abs((log_mean--8.970536)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.970536]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-8.137046]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.137046), abs((log_mean--8.137046)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.137046]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-8.787690]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.787690), abs((log_mean--8.787690)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.787690]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-9.088123]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--9.088123), abs((log_mean--9.088123)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-9.088123]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-9.300593]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--9.300593), abs((log_mean--9.300593)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-9.300593]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-9.465749]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--9.465749), abs((log_mean--9.465749)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-9.465749]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-8.891160]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.891160), abs((log_mean--8.891160)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.891160]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-9.541626]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--9.541626), abs((log_mean--9.541626)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-9.541626]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-9.841640]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--9.841640), abs((log_mean--9.841640)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-9.841640]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-10.054543]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--10.054543), abs((log_mean--10.054543)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-10.054543]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-10.219569]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--10.219569), abs((log_mean--10.219569)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-10.219569]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-9.503504]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--9.503504), abs((log_mean--9.503504)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-9.503504]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-10.154259]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--10.154259), abs((log_mean--10.154259)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-10.154259]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-10.454441]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--10.454441), abs((log_mean--10.454441)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-10.454441]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-10.667057]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--10.667057), abs((log_mean--10.667057)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-10.667057]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-10.832357]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--10.832357), abs((log_mean--10.832357)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-10.832357]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-10.166932]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--10.166932), abs((log_mean--10.166932)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-10.166932]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-10.817780]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--10.817780), abs((log_mean--10.817780)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-10.817780]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-11.117511]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--11.117511), abs((log_mean--11.117511)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-11.117511]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-11.330604]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--11.330604), abs((log_mean--11.330604)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-11.330604]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-11.496068]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--11.496068), abs((log_mean--11.496068)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-11.496068]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-10.926251]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--10.926251), abs((log_mean--10.926251)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-10.926251]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-11.577251]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--11.577251), abs((log_mean--11.577251)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-11.577251]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-11.877345]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--11.877345), abs((log_mean--11.877345)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-11.877345]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-12.090247]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--12.090247), abs((log_mean--12.090247)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-12.090247]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=4.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=4.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-12.255263]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--12.255263), abs((log_mean--12.255263)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-12.255263]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=4.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-4.816015]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.816015), abs((log_mean--4.816015)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.816015]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-5.343106]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.343106), abs((log_mean--5.343106)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.343106]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-5.643064]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.643064), abs((log_mean--5.643064)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.643064]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-5.855885]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.855885), abs((log_mean--5.855885)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.855885]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-6.021099]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.021099), abs((log_mean--6.021099)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.021099]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-5.176808]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.176808), abs((log_mean--5.176808)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.176808]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-5.795240]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.795240), abs((log_mean--5.795240)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.795240]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-6.095493]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.095493), abs((log_mean--6.095493)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.095493]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-6.308369]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.308369), abs((log_mean--6.308369)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.308369]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-6.473379]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.473379), abs((log_mean--6.473379)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.473379]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-5.834119]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.834119), abs((log_mean--5.834119)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.834119]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-6.485105]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.485105), abs((log_mean--6.485105)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.485105]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-6.784653]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.784653), abs((log_mean--6.784653)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.784653]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-6.997789]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.997789), abs((log_mean--6.997789)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.997789]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-7.162906]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.162906), abs((log_mean--7.162906)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.162906]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-6.396730]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.396730), abs((log_mean--6.396730)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.396730]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-7.047362]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.047362), abs((log_mean--7.047362)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.047362]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-7.347346]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.347346), abs((log_mean--7.347346)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.347346]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-7.560144]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.560144), abs((log_mean--7.560144)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.560144]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-7.725333]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.725333), abs((log_mean--7.725333)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.725333]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-7.009567]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.009567), abs((log_mean--7.009567)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.009567]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-7.660228]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.660228), abs((log_mean--7.660228)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.660228]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-7.960439]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.960439), abs((log_mean--7.960439)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.960439]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-8.173249]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.173249), abs((log_mean--8.173249)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.173249]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-8.338211]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.338211), abs((log_mean--8.338211)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.338211]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-7.718786]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--7.718786), abs((log_mean--7.718786)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-7.718786]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-8.369636]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.369636), abs((log_mean--8.369636)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.369636]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-8.669762]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.669762), abs((log_mean--8.669762)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.669762]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-8.882477]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--8.882477), abs((log_mean--8.882477)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-8.882477]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=5.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[5.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=5.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-9.047372]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--9.047372), abs((log_mean--9.047372)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-9.047372]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=5.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-2.973971]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.973971), abs((log_mean--2.973971)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.973971]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-3.301443]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.301443), abs((log_mean--3.301443)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.301443]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-3.601601]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.601601), abs((log_mean--3.601601)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.601601]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-3.814443]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.814443), abs((log_mean--3.814443)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.814443]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-3.979767]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.979767), abs((log_mean--3.979767)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.979767]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-3.281017]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.281017), abs((log_mean--3.281017)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.281017]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-3.710716]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.710716), abs((log_mean--3.710716)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.710716]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-4.010739]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.010739), abs((log_mean--4.010739)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.010739]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-4.223315]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.223315), abs((log_mean--4.223315)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.223315]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-4.388447]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.388447), abs((log_mean--4.388447)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.388447]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-3.749904]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.749904), abs((log_mean--3.749904)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.749904]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-4.335907]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.335907), abs((log_mean--4.335907)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.335907]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-4.635732]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.635732), abs((log_mean--4.635732)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.635732]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-4.848644]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.848644), abs((log_mean--4.848644)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.848644]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-5.013740]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.013740), abs((log_mean--5.013740)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.013740]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-4.201039]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.201039), abs((log_mean--4.201039)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.201039]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-4.848006]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.848006), abs((log_mean--4.848006)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.848006]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-5.148175]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.148175), abs((log_mean--5.148175)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.148175]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-5.361044]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.361044), abs((log_mean--5.361044)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.361044]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-5.526222]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.526222), abs((log_mean--5.526222)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.526222]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-4.759838]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.759838), abs((log_mean--4.759838)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.759838]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-5.410591]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.410591), abs((log_mean--5.410591)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.410591]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-5.710807]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.710807), abs((log_mean--5.710807)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.710807]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-5.923432]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.923432), abs((log_mean--5.923432)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.923432]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-6.088857]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.088857), abs((log_mean--6.088857)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.088857]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-5.418679]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.418679), abs((log_mean--5.418679)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.418679]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-6.069210]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.069210), abs((log_mean--6.069210)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.069210]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-6.369509]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.369509), abs((log_mean--6.369509)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.369509]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-6.582055]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.582055), abs((log_mean--6.582055)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.582055]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=6.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[6.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=6.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-6.747339]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.747339), abs((log_mean--6.747339)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.747339]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=6.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-1.964685]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.964685), abs((log_mean--1.964685)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.964685]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-2.165435]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.165435), abs((log_mean--2.165435)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.165435]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-2.465457]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.465457), abs((log_mean--2.465457)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.465457]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-2.678443]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.678443), abs((log_mean--2.678443)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.678443]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-2.843526]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.843526), abs((log_mean--2.843526)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.843526]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-2.249993]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.249993), abs((log_mean--2.249993)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.249993]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-2.531370]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.531370), abs((log_mean--2.531370)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.531370]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-2.831405]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.831405), abs((log_mean--2.831405)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.831405]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-3.044292]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.044292), abs((log_mean--3.044292)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.044292]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-3.209421]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.209421), abs((log_mean--3.209421)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.209421]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-2.676116]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.676116), abs((log_mean--2.676116)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.676116]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-3.092023]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.092023), abs((log_mean--3.092023)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.092023]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-3.392039]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.392039), abs((log_mean--3.392039)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.392039]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-3.604906]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.604906), abs((log_mean--3.604906)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.604906]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-3.770090]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.770090), abs((log_mean--3.770090)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.770090]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-2.994533]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.994533), abs((log_mean--2.994533)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.994533]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-3.554349]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.554349), abs((log_mean--3.554349)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.554349]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-3.854226]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.854226), abs((log_mean--3.854226)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.854226]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-4.067508]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.067508), abs((log_mean--4.067508)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.067508]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-4.232228]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.232228), abs((log_mean--4.232228)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.232228]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-3.417327]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.417327), abs((log_mean--3.417327)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.417327]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-4.066340]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.066340), abs((log_mean--4.066340)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.066340]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-4.366941]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.366941), abs((log_mean--4.366941)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.366941]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-4.579502]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.579502), abs((log_mean--4.579502)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.579502]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-4.744662]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.744662), abs((log_mean--4.744662)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.744662]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-4.024073]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.024073), abs((log_mean--4.024073)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.024073]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-4.674842]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.674842), abs((log_mean--4.674842)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.674842]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-4.974930]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.974930), abs((log_mean--4.974930)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.974930]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-5.187850]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.187850), abs((log_mean--5.187850)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.187850]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=7.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[7.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=7.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-5.352985]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.352985), abs((log_mean--5.352985)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.352985]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=7.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-1.216045]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.216045), abs((log_mean--1.216045)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.216045]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-1.363359]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.363359), abs((log_mean--1.363359)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.363359]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-1.663366]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.663366), abs((log_mean--1.663366)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.663366]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-1.876664]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.876664), abs((log_mean--1.876664)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.876664]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-2.041760]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.041760), abs((log_mean--2.041760)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.041760]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-1.479726]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.479726), abs((log_mean--1.479726)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.479726]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-1.686319]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.686319), abs((log_mean--1.686319)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.686319]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-1.986316]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.986316), abs((log_mean--1.986316)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.986316]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-2.199126]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.199126), abs((log_mean--2.199126)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.199126]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-2.364248]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.364248), abs((log_mean--2.364248)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.364248]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.870803]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.870803), abs((log_mean--1.870803)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.870803]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-2.183026]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.183026), abs((log_mean--2.183026)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.183026]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-2.482669]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.482669), abs((log_mean--2.482669)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.482669]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-2.695480]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.695480), abs((log_mean--2.695480)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.695480]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-2.860677]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.860677), abs((log_mean--2.860677)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.860677]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-2.160218]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.160218), abs((log_mean--2.160218)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.160218]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-2.594677]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.594677), abs((log_mean--2.594677)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.594677]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-2.894802]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.894802), abs((log_mean--2.894802)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.894802]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-3.107558]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.107558), abs((log_mean--3.107558)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.107558]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-3.272804]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.272804), abs((log_mean--3.272804)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.272804]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-2.445417]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.445417), abs((log_mean--2.445417)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.445417]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-3.056544]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.056544), abs((log_mean--3.056544)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.056544]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-3.356702]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.356702), abs((log_mean--3.356702)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.356702]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-3.569498]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.569498), abs((log_mean--3.569498)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.569498]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-3.734714]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.734714), abs((log_mean--3.734714)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.734714]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-2.963652]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.963652), abs((log_mean--2.963652)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.963652]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-3.614514]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.614514), abs((log_mean--3.614514)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.614514]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-3.914526]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.914526), abs((log_mean--3.914526)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.914526]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-4.127074]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.127074), abs((log_mean--4.127074)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.127074]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=8.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=8.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-4.292552]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.292552), abs((log_mean--4.292552)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.292552]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=8.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=5.0, Vs30=200.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=5.0, Vs30=200.0: got=%s, expected=[[[-0.466968]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.466968), abs((log_mean--0.466968)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.466968]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=5.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=5.0, Vs30=400.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=5.0, Vs30=400.0: got=%s, expected=[[[-0.561593]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.561593), abs((log_mean--0.561593)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.561593]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=5.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-0.861566]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.861566), abs((log_mean--0.861566)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.861566]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=5.0, Vs30=800.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=5.0, Vs30=800.0: got=%s, expected=[[[-1.074408]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.074408), abs((log_mean--1.074408)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.074408]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=5.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=5.0, Vs30=1000.0
        R = array([[[5.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[-1.239600]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.239600), abs((log_mean--1.239600)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.239600]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=5.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=10.0, Vs30=200.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=10.0, Vs30=200.0: got=%s, expected=[[[-0.709480]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.709480), abs((log_mean--0.709480)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.709480]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=10.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=10.0, Vs30=400.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=10.0, Vs30=400.0: got=%s, expected=[[[-0.841183]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.841183), abs((log_mean--0.841183)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.841183]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=10.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-1.140998]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.140998), abs((log_mean--1.140998)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.140998]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=10.0, Vs30=800.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=10.0, Vs30=800.0: got=%s, expected=[[[-1.354021]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.354021), abs((log_mean--1.354021)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.354021]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=10.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=10.0, Vs30=1000.0
        R = array([[[10.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[-1.519140]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.519140), abs((log_mean--1.519140)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.519140]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=10.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=25.0, Vs30=200.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=25.0, Vs30=200.0: got=%s, expected=[[[-1.065081]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.065081), abs((log_mean--1.065081)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.065081]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=25.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=25.0, Vs30=400.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=25.0, Vs30=400.0: got=%s, expected=[[[-1.272966]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.272966), abs((log_mean--1.272966)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.272966]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=25.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-1.573106]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.573106), abs((log_mean--1.573106)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.573106]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=25.0, Vs30=800.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=25.0, Vs30=800.0: got=%s, expected=[[[-1.786175]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.786175), abs((log_mean--1.786175)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.786175]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=25.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=25.0, Vs30=1000.0
        R = array([[[25.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[-1.951224]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.951224), abs((log_mean--1.951224)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.951224]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=25.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=50.0, Vs30=200.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=50.0, Vs30=200.0: got=%s, expected=[[[-1.326894]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.326894), abs((log_mean--1.326894)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.326894]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=50.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=50.0, Vs30=400.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=50.0, Vs30=400.0: got=%s, expected=[[[-1.635269]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.635269), abs((log_mean--1.635269)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.635269]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=50.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=50.0, Vs30=600.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=50.0, Vs30=600.0: got=%s, expected=[[[-1.935168]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.935168), abs((log_mean--1.935168)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.935168]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=50.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=50.0, Vs30=800.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=50.0, Vs30=800.0: got=%s, expected=[[[-2.148149]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.148149), abs((log_mean--2.148149)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.148149]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=50.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=50.0, Vs30=1000.0
        R = array([[[50.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[-2.313141]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.313141), abs((log_mean--2.313141)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.313141]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=50.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=100.0, Vs30=200.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=100.0, Vs30=200.0: got=%s, expected=[[[-1.560172]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.560172), abs((log_mean--1.560172)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.560172]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=100.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=100.0, Vs30=400.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=100.0, Vs30=400.0: got=%s, expected=[[[-2.046394]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.046394), abs((log_mean--2.046394)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.046394]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=100.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=100.0, Vs30=600.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=100.0, Vs30=600.0: got=%s, expected=[[[-2.346537]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.346537), abs((log_mean--2.346537)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.346537]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=100.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=100.0, Vs30=800.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=100.0, Vs30=800.0: got=%s, expected=[[[-2.559415]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.559415), abs((log_mean--2.559415)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.559415]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=100.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=100.0, Vs30=1000.0
        R = array([[[100.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[-2.724637]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.724637), abs((log_mean--2.724637)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.724637]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=100.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=200.0, Vs30=200.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[200.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=200.0, Vs30=200.0: got=%s, expected=[[[-1.903138]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--1.903138), abs((log_mean--1.903138)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-1.903138]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=200.0, Vs30=200.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=200.0, Vs30=400.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[400.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=200.0, Vs30=400.0: got=%s, expected=[[[-2.553871]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.553871), abs((log_mean--2.553871)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.553871]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=200.0, Vs30=400.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=200.0, Vs30=600.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=200.0, Vs30=600.0: got=%s, expected=[[[-2.853886]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.853886), abs((log_mean--2.853886)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.853886]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=200.0, Vs30=600.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=200.0, Vs30=800.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[800.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=200.0, Vs30=800.0: got=%s, expected=[[[-3.066799]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.066799), abs((log_mean--3.066799)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.066799]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=200.0, Vs30=800.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=3.00, M=9.0, R=200.0, Vs30=1000.0
        R = array([[[200.000000]]])
        M = array([[[9.000000]]])
        Vs30 = array([[[1000.000000]]])
        coefficient = c_dict['3.00']
        sigma_coefficient = s_dict['3.00']
        (log_mean, sigma) = model.distribution(mag=M, distance=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=3.00, M=9.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[-3.231961]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.231961), abs((log_mean--3.231961)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.231961]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=3.00, M=9.0, R=200.0, Vs30=1000.0: got=%s, expected=[[[0.695000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.695000), abs((sigma-0.695000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.695000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Boore_08, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
