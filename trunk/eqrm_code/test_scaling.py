
import unittest
import math

from scipy import array, allclose, exp, log, power, asarray

from eqrm_code.conversions import conversion_functions
from eqrm_code.scaling import *

class Test_scaling(unittest.TestCase):
    def test_modified_Wells_and_Coppersmith_94_rup_width(self):

        Mw = array([6.64 , 4.51 , 5.27 , 5.61 , 6.4])
        area=array([4.16869383e+02,3.09029543e+00,1.77827941e+01,
                    3.89045145e+01,2.39883292e+02])
        dip = array([ 35. , 35. , 35. , 35. , 35. ])
        fault_width = array([ 15. , 15. , 15. , 15. , 15. ])
        scaling_dic = {'scaling_rule':'modified_Wells_and_Coppersmith_94'}
        
        width = scaling_calc_rup_width(Mw, scaling_dic,
                                       dip, rup_area=area,
                                       max_rup_width=fault_width)
        
        correct = [ 15, 1.75792361 ,4.21696503, 6.05476637, 12.97166415]
        assert allclose(correct,
                        width)
               
    def test_modified_Wells_and_Coppersmith_94_rup_width2(self):
        # 
        Mw = array([4.5, 6.5, 13., 13.])
        area=array([100., 100., 100., 100.])
        dip = array([ 0., 0., 90., 90.])
        fault_width = array([ 15000. , 15000. , 15000., 2.])
        scaling_dic = {'scaling_rule':'modified_Wells_and_Coppersmith_94'}
        
        width = scaling_calc_rup_width(Mw, scaling_dic,
                                       dip, rup_area=area,
                                       max_rup_width=fault_width)
        
        correct = [ 10., 10., 5., 2.]
        assert allclose(correct,
                        width)
               
    def test_modified_Wells_and_Coppersmith_94_rup_area(self):
        # 
        Mw = array([4.02, 5.02, 6.02])
        # testing name shortening
        scaling_dic = {'scaling_rule':'mod'}
        
        width = scaling_calc_rup_area(Mw, scaling_dic)
        
        correct = [ 1., 10., 100.]
        assert allclose(correct,
                        width)
        
    def test_Wells_and_Coppersmith_94_rup_area(self):
        # 0.1 = 10**-1 = 10**(-2.87+1.87) = 10**(-2.87+(0.82*1.87/0.82))
        Mw = array([1.87/0.82])
        scaling_dic = {'scaling_rule':'Wells_and_Coppersmith_94',
                       'scaling_fault_type':"normal"}       
        area = scaling_calc_rup_area(Mw, scaling_dic)        
        correct = [ 0.1, ]
        assert allclose(correct, area)
        
        Mw = array([2.99/0.98])
        scaling_dic = {'scaling_rule':'Wells_and_Coppersmith_94',
                       'scaling_fault_type':"reverse"}       
        area = scaling_calc_rup_area(Mw, scaling_dic)
        correct = [ 0.1, ]
        assert allclose(correct, area)
        
        Mw = array([2.42/0.9])
        scaling_dic = {'scaling_rule':'Wells_and_Coppersmith_94',
                       'scaling_fault_type':"strike_slip"}       
        area = scaling_calc_rup_area(Mw, scaling_dic)        
        correct = [ 0.1, ]
        assert allclose(correct, area)
        
        Mw = array([2.497/0.91])
        scaling_dic = {'scaling_rule':'Wells_and_Coppersmith_94',
                       'scaling_fault_type':"unspecified"}       
        area = scaling_calc_rup_area(Mw, scaling_dic)        
        correct = [ 0.1, ]
        assert allclose(correct, area)
        
    def test_Wells_and_Coppersmith_94_rup_width(self):
        # Try and get an answer of 0.1
        # 0.1 = 10**-1 = 10**(-1.14+0.14) = 10**(-1.14+(0.35*0.14/0.35))
        # Mw = 0.14/0.35 gives a width of 0.1 
        Mw = array([0.14/0.35])
        scaling_dic = {'scaling_rule':'Wells_and_Coppersmith_94',
                       'scaling_fault_type':"normal"}
        # Dip is None here, for testing this model
        # but in production the actual dip must be passed in
        # since the scaling model may require it.
        dip = None
        width = scaling_calc_rup_width(Mw, scaling_dic, dip)        
        correct = [ 0.1, ]
        assert allclose(correct, width)
        
        Mw = array([0.61/0.41])
        scaling_dic = {'scaling_rule':'Wells_and_Coppersmith_94',
                       'scaling_fault_type':"reverse"}       
        width = scaling_calc_rup_width(Mw, scaling_dic, dip)
        correct = [ 0.1, ]
        assert allclose(correct, width)
        
        Mw = array([(0.76-1.)/0.27])
        scaling_dic = {'scaling_rule':'Wells_and_Coppersmith_94',
                       'scaling_fault_type':"strike_slip"}       
        width = scaling_calc_rup_width(Mw, scaling_dic, dip)        
        correct = [ 0.1, ]
        assert allclose(correct, width)
        
        Mw = array([0.01/0.32])
        scaling_dic = {'scaling_rule':'Wells_and_Coppersmith_94',
                       'scaling_fault_type':"unspecified"}       
        width = scaling_calc_rup_width(Mw, scaling_dic, dip)        
        correct = [ 0.1, ]
        assert allclose(correct, width)
        
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_scaling,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
