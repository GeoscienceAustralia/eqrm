
import os
import sys
import unittest

from scipy import array,allclose,newaxis,exp,pi,nan_to_num
from numpy import nanmax

from eqrm_code.equivalent_linear_solver import find_intersection, \
     get_intersection_indices, findfirst

class Test_damage_solver(unittest.TestCase):
    def test_findfirst(self):
        
        condition=array((False,False,True))
        assert (findfirst(condition)==2)
        
        condition=array(((False,True,False),
                         (False,False,False),
                         (True,True,True),
                         (True,False,False)))
        no_match=-1        
        axis_0=findfirst(condition,axis=0,no_intersection=no_match)
        axis_1=findfirst(condition,axis=1,no_intersection=no_match)

        assert allclose(axis_0,(2,0,2))
        assert allclose(axis_1,(1,no_match,0,0))
        
        # check that nve axis works
        # (note no_match=-1 is the default anyway, so don't specify)
        assert allclose(axis_1,findfirst(condition,axis=-1))        
        assert allclose(axis_0,findfirst(condition,axis=-2))
        
    def test_get_intersection_indices(self):
        
        condition=array((False,False,True))
        assert allclose(get_intersection_indices(condition),([1],[2]))
        
        condition=array(((False,True,False),
                         (False,False,False),
                         (True,True,True),
                         (True,False,False)))

        """
        for axis = 0, search down until condition = True
        |*|
        | |
        * *

                      axis         filler
        raw_answer=[[( 1,-1, 1),( 0, 1, 2)], #point before
                    [( 2, 0, 2),( 0, 1, 2)]] #point true

        then change -1 to zero.

        ###########################################################
        for axis = 1, search across until condition = True

        -*
        ---   not found *
        *https://lists.sourceforge.net/lists/listinfo/eqrm-user
        *

                      filler      axis
        raw_answer=[[(0,1,2,3),( 0, 2*,-1,-1)], #point before
                    [(0,1,2,3),( 1, 3*, 0, 0)]] #point true   
        then change -1 to zero, and 3 to 2
    

            * note that the point that wasn't found was set to (n-1) = 2
        """

        answer0=[[(1,0,1),(0,1,2)],
                 [(2,1,2),(0,1,2)]]
        
        answer1=[[(0,1,2,3),(0,2,0,0)],
                 [(0,1,2,3),(1,2,1,1)]]

        assert allclose(get_intersection_indices(condition,axis=0),answer0)
        assert allclose(get_intersection_indices(condition,axis=1),answer1)

        # check that axis = -ve works:
        assert allclose(get_intersection_indices(condition,axis=-1),answer1)
        assert allclose(get_intersection_indices(condition,axis=-2),answer0)
    
    def test_find_intersection(self):

        # SA == SAcap at index 1.5, therefore SD=2.5
        SD=array([1,2,3.0]) # x-axis
        SA=array([2,4,6.0]) # y-axis
        SAcap=array([0,3,7.0]) # y-axis
        assert (find_intersection(SD,SA,SAcap)==2.5)
        
        # SA exceeds SAcap the whole way, so SD = max(SD)
        SD=array([1,2,3.0])
        SA=array([2,4,6.0])
        SAcap=array([0,3,4.0])
        assert (find_intersection(SD,SA,SAcap)==3.0)
        
        
        # SA is exceeded by SAcap in the first bin
        SD=array([1,2,3.0])
        SA=array([2,4,6.0])
        SAcap=array([0,6,7.0])
        assert (find_intersection(SD,SA,SAcap)==1.5)

    def test_find_intersectionII(self):
        # If there is 2 intersections, are they found? No
        SD=array([1,2,3.0])
        SA=array([2,4,6.0])
        SAcap=array([0,6,4.0])
        assert (find_intersection(SD,SA,SAcap)==1.5)
        

    def test_find_intersection_array(self):
        # SA == SAcap at index 1.5, therefore SD=2.5
        SD=array([[1,2,3.0],[1,2,3.0],[1,2,3.0]])
        SA=array([[2,4,6.0],[2,4,6.0],[2,4,6.0]])
        SAcap=array([[0,3,7.0],[0,3,4.0],[0,6,7.0]])
        answer = [2.5,3,1.5]
        assert allclose(find_intersection(SD,SA,SAcap),answer)

        
    def test_array_ab_diff(self):
        a = array([7.35287023,  3.98947559,  0.])
        b = array([ 7.38625883, 3.98947559, 0.])
        diff=abs(a-b)/b
        # diff [ 0.00452037  0.                 NaN]
        # Windows can't handle the NaN,
        # so it has to be set to zero
        diff=nan_to_num(diff)
        #print "diff", diff

        # this would return max_diff -1.#IND if NaN's aren't removed,
        # in windows.
        max_diff=diff.max()
        #print "max_diff", max_diff
        assert max_diff == diff[0]
    
    
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_damage_solver,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
