
import unittest

from scipy import asarray, allclose

from eqrm_code.interp import interp


class Test_Interp(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_interp(self):
        functx = asarray([1,2])
        functy = asarray([10,20])
        x = asarray([0.5,1.5,2.5])
        y = interp(x, functy, functx)
        y_ans = x * 10.0
        self.assert_(allclose(y, y_ans, rtol=0.05))
     
    def test_interp_no_extrapolate_high(self):
        functx = asarray([1,2])
        functy = asarray([10,20])
        
        x = asarray([1.3,1.5,1.7])
        y = interp(x, functy, functx, extrapolate_high=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, y_ans, rtol=0.05))
        
        x = asarray([0.5,1.5,2.5])
        y = interp(x, functy, functx, extrapolate_high=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, [5.,15.,20.], rtol=0.05))   

    def test_interp_no_extrapolate_low(self):
        functx = asarray([1,2])
        functy = asarray([10,20])
        
        x = asarray([1.3,1.5,1.7])
        y = interp(x, functy, functx, extrapolate_low=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, y_ans, rtol=0.05))
        
        x = asarray([0.5,1.5,2.5])
        y = interp(x, functy, functx, extrapolate_low=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, [10.,15.,25.], rtol=0.05))
        
    def test_interp_no_extrapolating(self):
        functx = asarray([1,2])
        functy = asarray([10,20])
        
        x = asarray([1.3,1.5,1.7])
        y = interp(x, functy, functx, extrapolate_low=False,
                   extrapolate_high=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, y_ans, rtol=0.05))
        
        x = asarray([0.5,1.5,2.5])
        y = interp(x, functy, functx, extrapolate_low=False,
                   extrapolate_high=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, [10.,15.,20.], rtol=0.05))

        
    def test_interp_no_extrapolate_low_decending(self):
        functx = asarray([2,1])
        functy = asarray([20,10])
        
        x = asarray([1.3,1.5,1.7])
        y = interp(x, functy, functx, extrapolate_low=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, y_ans, rtol=0.05))
        
        x = asarray([0.5,1.5,2.5])
        y = interp(x, functy, functx, extrapolate_low=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, [10.,15.,25.], rtol=0.05))
        
    def test_interp_no_extrapolate_low_bad_ordering(self):
        functx = asarray([2, 1, 0.8])
        functy = asarray([20, 10, 8])
        
        x = asarray([1.3,1.5,1.7])
        y = interp(x, functy, functx, extrapolate_low=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, y_ans, rtol=0.05))
        
        x = asarray([0.5,1.5,2.5])
        y = interp(x, functy, functx, extrapolate_low=False)
        y_ans = x * 10.0
        self.assert_(allclose(y, [8.,15.,25.], rtol=0.05))

    def test_interp_no_extrapolate_high_local_max(self):
        functx = asarray([2, 1, 3])
        functy = asarray([30, 10, 20])
        
        x = asarray([0.5, 1.5, 2.5, 3.0, 4.0])
        y = interp(x, functy, functx, extrapolate_high=False)
        #print "y", y
        self.assert_(allclose(y, [0., 20., 25., 20., 20.], rtol=0.05))
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Interp,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
