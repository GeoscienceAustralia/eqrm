import os
import sys
import unittest

from eqrm_code.distributions import distribution_functions

from eqrm_code.util import reset_seed


class Test_Distributions(unittest.TestCase):

    def setUp(self):
        reset_seed(True)

    def tearDown(self):
        pass

    def test_constant(self):
        constant_func = distribution_functions['constant']
        ans = constant_func(mean=54, n=2)
        # print "ans", ans
        actual = [54., 54.]
        self.failUnless(ans == actual,
                        'Failed!')

    def test_uniform(self):
        func = distribution_functions['uniform']
        ans = func(20, 30, n=3)
        # print "ans test_uniform", ans
        actual = [27.28207076565548, 23.884363318551443, 27.350381515484784]
        actual = [24.523795535098188, 25.597723860804962, 29.242105840237294]
        self.failUnless(ans == actual,
                        'Failed!')

    def test_normal(self):
        func = distribution_functions['normal']
        ans = func(10, 1, n=3)
        # print "ans test_normal", ans
        actual = [8.7759273242860356, 10.377588198301599, 10.994999627670939]
        self.failUnless(ans == actual,
                        'Failed!')

    def test_normalB(self):
        func = distribution_functions['normal']
        ans = func(10, 10, n=3)
        # print "ans test_normalB", ans
        actual = [4.8679005141056466, -3.2897920068630899, 9.344705949865638]
        actual = [-2.240726757139651, 13.775881983015978, 19.949996276709399]
        self.failUnless(ans == actual,
                        'Failed!')

    def test_normalC(self):
        func = distribution_functions['normal']
        ans = func(10, 10, n=3, minimum=9, maximum=9.2)
        # print "ans test_normalC", ans
        actual = [9.0733009505271482, 9.1829822262389467, 9.1365862664274857]
        self.failUnless(ans == actual,
                        'Failed!')

    def test_lognormal(self):
        func = distribution_functions['normal']
        ans = func(10, 1, n=3)
        # print "ans test_lognormal", ans
        actual = [8.7759273242860356, 10.377588198301599, 10.994999627670939]
        self.failUnless(ans == actual,
                        'Failed!')

    def test_lognormalB(self):
        func = distribution_functions['normal']
        ans = func(10, 10, n=3)
        # print "ans test_lognormalB", ans
        actual = [-2.240726757139651, 13.775881983015978, 19.949996276709399]
        self.failUnless(ans == actual,
                        'Failed!')

    def test_lognormalC(self):
        func = distribution_functions['normal']
        ans = func(10, 10, n=3, minimum=9, maximum=9.2)
        # print "ans test_normalC", ans
        actual = [9.0733009505271482, 9.1829822262389467, 9.1365862664274857]
        self.failUnless(ans == actual,
                        'Failed!')

    def test_catagory(self):
        func = distribution_functions['catagory']
        answers = func(n=10, a=0.7, b=0.2, c=0.1)
        # print "ans test_catagory", ans
        actuals = ['c', 'a', 'a', 'c', 'a', 'a', 'a', 'c', 'a', 'a']
        for answer, actual in map(None, answers, actuals):
            self.failUnless(answer == actual, 'Failed!')

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Distributions, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
