#!/usr/bin/env python
import os
import sys
#sys.path.append(os.getcwd()+os.sep+os.pardir+os.sep+'eqrm_code')


import unittest
from scipy import zeros, array, allclose
from math import sqrt, pi

from eqrm_code.numerical_tools import *

from eqrm_code import perf

epsilon=0.00001


def test_function(x, y):
    return x+y

class Test_Numerical_Tools(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @perf.benchmark
    def test_angle1(self):
        """Test angles between one vector and the x-axis
	"""
        assert allclose(angle([1.0, 0.0])/pi*180, 0.0)	    
        assert allclose(angle([1.0, 1.0])/pi*180, 45.0)
        assert allclose(angle([0.0, 1.0])/pi*180, 90.0)		
        assert allclose(angle([-1.0, 1.0])/pi*180, 135.0)		
        assert allclose(angle([-1.0, 0.0])/pi*180, 180.0)
        assert allclose(angle([-1.0, -1.0])/pi*180, 225.0)
        assert allclose(angle([0.0, -1.0])/pi*180, 270.0)
        assert allclose(angle([1.0, -1.0])/pi*180, 315.0)		
		
    @perf.benchmark
    def test_angle2(self):
        """Test angles between two arbitrary vectors
	"""    
	
        assert allclose(angle([1.0, 0.0], [1.0, 1.0])/pi*180, 315.0)
        assert allclose(angle([1.0, 1.0], [1.0, 0.0])/pi*180, 45.0)
		
        assert allclose(angle([-1.0, -1.0], [1.0, 1.0])/pi*180, 180)	
        assert allclose(angle([-1.0, -1.0], [-1.0, 1.0])/pi*180, 90.0)	
	
        assert allclose(angle([-1.0, 0.0], [1.0, 1.0])/pi*180, 135.0)
        assert allclose(angle([0.0, -1.0], [1.0, 1.0])/pi*180, 225.0)	
	
        assert allclose(angle([1.0, -1.0], [1.0, 1.0])/pi*180, 270.0)	
        assert allclose(angle([1.0, 0.0], [0.0, 1.0])/pi*180, 270.0)

        #From test_get_boundary_polygon_V
        v_prev = [-0.5, -0.5]
        vc = [ 0.0,  -0.5]
        assert allclose(angle(vc, v_prev)/pi*180, 45.0)

        vc = [ 0.5,  0.0]
        assert allclose(angle(vc, v_prev)/pi*180, 135.0)

        vc = [ -0.5,  0.5]
        assert allclose(angle(vc, v_prev)/pi*180, 270.0)                

    @perf.benchmark
    def test_err(self):
        x = [2,5] # diff at first position = 4, 4^2 = 16
        y = [6,7] # diff at secnd position = 2, 2^2 = 4
        # 16 + 4 = 20
        
        # If there is x and y, n=2 and relative=False, this will calc;
        # sqrt(sum_over_x&y((xi - yi)^2))
        err__1 = err(x,y,2,False)
        assert err__1 == sqrt(20)
        #print "err_", err_
        #rmsd_1 = err__1*sqrt(1./len(x))
        #print "err__1*sqrt(1./len(x))", err__1*sqrt(1./len(x))
        #print "sqrt(10)", sqrt(10)
        
        x = [2,7,100]
        y = [5,10,103]
        err__2 = err(x,y,2,False)
        assert err__2 == sqrt(27)
        #rmsd_2 = err__2*sqrt(1./len(x))
        #print "err__2*sqrt(1./len(x))", err__2*sqrt(1./len(x))

        x = [2,5,2,7,100]
        y = [6,7,5,10,103]
        err_3 = err(x,y,2,False)
        assert err_3 == sqrt(47)

    @perf.benchmark
    def test_anglediff(self):
        assert allclose(anglediff([0.0, 1.], [1.0, 1.0])/pi*180, 45.0)

    @perf.benchmark
    def test_ensure_numeric(self):
        from numerical_tools import ensure_numeric
        from scipy import ndarray, array

        A = [1,2,3,4]
        B = ensure_numeric(A)
        assert isinstance(B,ndarray)
        assert B.dtype == array((1,2),dtype='l').dtype
        assert B[0] == 1 and B[1] == 2 and B[2] == 3 and B[3] == 4


        A = [1,2,3.14,4]
        B = ensure_numeric(A)
        assert isinstance(B,ndarray)
        assert B.dtype == array((1,2),dtype='d').dtype
        assert B[0] == 1 and B[1] == 2 and B[2] == 3.14 and B[3] == 4


        A = [1,2,3,4]
        B = ensure_numeric(A, float)
        assert isinstance(B,ndarray)
        assert B.dtype == array((1,2),dtype='d').dtype
        assert B[0] == 1.0 and B[1] == 2.0 and B[2] == 3.0 and B[3] == 4.0


        A = [1,2,3,4]
        B = ensure_numeric(A, float)
        assert isinstance(B,ndarray)
        assert B.dtype == array((1,2),dtype='d').dtype
        assert B[0] == 1.0 and B[1] == 2.0 and B[2] == 3.0 and B[3] == 4.0


        A = array([1,2,3,4])
        B = ensure_numeric(A)
        assert isinstance(B,ndarray)
        assert B.dtype == array((1,2),dtype='l').dtype 
        assert (A == B).all()
        assert A is B   #Same object


        A = array([1,2,3,4])
        B = ensure_numeric(A, float)
        assert isinstance(B,ndarray)
        assert B.dtype == array((1,2),dtype='d').dtype        
        assert (A == B).all()
        assert A is not B   #Not the same object

    @perf.benchmark
    def test_histogram(self):
        """Test histogram with different bin boundaries
        """
        
        a = [1,1,1,1,1,2,1,3,2,3,1,2,3,4,1]


        #There are four elements greater than or equal to 3
        bins = [3]
        assert allclose(histogram(a, bins), [4])


        bins = [ min(a) ]
        assert allclose(histogram(a, bins), [len(a)])


        bins = [ max(a)+0.00001 ]
        assert allclose(histogram(a, bins), [0])        

        
        bins = [1,2,3,4]
        assert allclose(histogram(a, bins), [8,3,3,1])


        bins = [1.1,2,3.1,4]
        #print histogram(a, bins)
        assert allclose(histogram(a, bins), [0,6,0,1])


        bins = [0,1.5,2,3]
        assert allclose(histogram(a, bins), [8,0,3,4])
        assert allclose(histogram(a, [0,3]), histogram(a, [-0.5,3]))

        # Check situation with #bins >= #datapoints
        a = [1.7]
        bins = [0,1.5,2,3]
        assert allclose(histogram(a, bins), [0,1,0,0])

        a = [1.7]
        bins = [0]
        assert allclose(histogram(a, bins), [1])

        a = [-1.7]
        bins = [0]
        assert allclose(histogram(a, bins), [0])

        a = [-1.7]
        bins = [-1.7]
        assert allclose(histogram(a, bins), [1])
        

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Numerical_Tools,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
