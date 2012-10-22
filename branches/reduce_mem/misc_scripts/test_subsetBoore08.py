
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
            
        mrtol = 1.0e-3
        matol = 1.0e-3

        srtol = 5.0e-3
        satol = 5.0e-3

        # now run all tests
        model_name = 'Boore_08'
        model = Ground_motion_specification(model_name)

        # T=0.01, M=4.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        fault_type = array([[[2]]])
        
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, Joyner_Boore=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-3.179415]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.179415), abs((log_mean--3.179415)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.179415]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, Joyner_Boore=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-3.717279]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.717279), abs((log_mean--3.717279)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.717279]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.01, M=4.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.01']
        sigma_coefficient = s_dict['0.01']
        (log_mean, sigma) = model.distribution(mag=M, Joyner_Boore=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.01, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-4.545958]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--4.545958), abs((log_mean--4.545958)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-4.545958]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.01, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.566000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.566000), abs((sigma-0.566000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.566000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)


        # T=0.20, M=8.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[8.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, Joyner_Boore=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-0.169129]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--0.169129), abs((log_mean--0.169129)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-0.169129]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=8.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)


        # T=0.20, M=4.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, Joyner_Boore=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-2.798686]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--2.798686), abs((log_mean--2.798686)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-2.798686]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=0.20, M=4.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['0.20']
        sigma_coefficient = s_dict['0.20']
        (log_mean, sigma) = model.distribution(mag=M, Joyner_Boore=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=0.20, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-3.916533]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--3.916533), abs((log_mean--3.916533)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-3.916533]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=0.20, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.596000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.596000), abs((sigma-0.596000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.596000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=5.0, Vs30=600.0
        R = array([[[5.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, Joyner_Boore=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[-5.031195]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.031195), abs((log_mean--5.031195)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.031195]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=5.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=10.0, Vs30=600.0
        R = array([[[10.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, Joyner_Boore=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[-5.576974]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--5.576974), abs((log_mean--5.576974)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-5.576974]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=10.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

        # T=1.00, M=4.0, R=25.0, Vs30=600.0
        R = array([[[25.000000]]])
        M = array([[[4.000000]]])
        Vs30 = array([[[600.000000]]])
        coefficient = c_dict['1.00']
        sigma_coefficient = s_dict['1.00']
        (log_mean, sigma) = model.distribution(mag=M, Joyner_Boore=R, Vs30=Vs30,
           coefficient=coefficient, sigma_coefficient=sigma_coefficient,
                                               fault_type=fault_type)
        msg1 = 'log_mean: T=1.00, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[-6.400938]]]' % str(log_mean)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(log_mean--6.400938), abs((log_mean--6.400938)/log_mean))
        self.failUnless(allclose(log_mean, array([[[-6.400938]]]), atol=matol, rtol=mrtol), msg1+'\n'+msg2)
        msg1 = 'sigma: T=1.00, M=4.0, R=25.0, Vs30=600.0: got=%s, expected=[[[0.647000]]]' % str(sigma)
        msg2 = 'abs_delta=%f, rel_delta=%f' % (abs(sigma-0.647000), abs((sigma-0.647000)/sigma))
        self.failUnless(allclose(sigma, array([[[0.647000]]]), atol=satol, rtol=srtol), msg1+'\n'+msg2)

################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Boore_08, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
