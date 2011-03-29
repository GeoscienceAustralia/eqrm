
import unittest
import math

from scipy import array, allclose, exp, power, asarray

from eqrm_code.conversions import conversion_functions
from eqrm_code.scaling import *
from eqrm_code.scaling_functions import *

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
        # Mw = 1.87/0.82 gives a width of 0.1 
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
        # Mw = 0.14/0.35 gives a width of 0.1 
        # 0.1 = 10**-1 = 10**(-1.14+0.14) = 10**(-1.14+(0.35*0.14/0.35))
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
        
    def test_Leonard_SCR_area(self):
        
        Mw = array([5.5])
        scaling_dic = {'scaling_rule':'Leonard_SCR'}           
        area = scaling_calc_rup_area(Mw, scaling_dic)  
        correct = [ 20.73322, ] # From Scaling_Relations_Leonard_2010.xls
        assert allclose(correct, area)
        correct = Leonard_Mw_to_Area(Mw)
        assert allclose(correct, area)
        
        Mw = array([5.5, 6.5, 7.0, 7.5])
        scaling_dic = {'scaling_rule':'Leonard_SCR'}           
        area = scaling_calc_rup_area(Mw, scaling_dic)  
        correct = Leonard_Mw_to_Area(Mw)
        assert allclose(correct, area)

    def test_Leonard_SCR_width(self):
        scaling_dic = {'scaling_rule':'Leonard_SCR'} 
        area = 1.0   
        Mw = array([5.5])     
        width = scaling_calc_rup_width(Mw, scaling_dic, dip=None, 
        rup_area=area) 
        length = 5.12861 # From Scaling_Relations_Leonard_2010.xls
        width_actual = area/length
        assert allclose(width_actual, width)
            
        scaling_dic = {'scaling_rule':'Leonard_SCR'} 
        area = 1.0   
        Mw = array([8.5])     
        width = scaling_calc_rup_width(Mw, scaling_dic, dip=None, 
        rup_area=area) 
        length = 323593.66/1000 # From Scaling_Relations_Leonard_2010.xls
        width_actual = area/length
        assert allclose(width_actual, width)
            
        scaling_dic = {'scaling_rule':'Leonard_SCR'} 
        area = 5100.0   
        Mw = array([5.5])   
        max_rup_width = 25.0  
        width = scaling_calc_rup_width(Mw, scaling_dic, dip=None, 
        rup_area=area, max_rup_width=max_rup_width) 
        length = 5.12861 # From Scaling_Relations_Leonard_2010.xls
        width_actual = area/length
        assert allclose(width, max_rup_width)
        
    def test_Leonard_SCR_constants(self):
    
        Mw = array([4., 8.]) 
        e, f = Leonard_SCR_constants(Mw)
        assert allclose(e, [1.5/3., 1.5/2.5])
        assert allclose(f, [(1.5*6.07-6.39)/3.-3.0, (1.5*6.07-8.08)/2.5-3.0])
        
        
def Mw_to_Mo(Mw):
    """
    Returns:
      Mo units Nm
    """   
    c = 1.5
    d = 9.105
    Mo = 10**(c*Mw + d)
    return Mo
    
def Leonard_Mw_to_Area(Mw):
    a = 1.5
    b = 6.38
    Mo = Mw_to_Mo(Mw)
    Area = ((Mo/10**b)**(1/a))/1000000
    return Area
    
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_scaling,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
