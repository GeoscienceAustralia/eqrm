
import unittest

from scipy import array,allclose

from eqrm_code.conversions import conversion_functions
from eqrm_code.xml_interface import Xml_Interface

"""
Some of the values in event_set (such as fault length)
are dependent on other values (such as Mw), unless they
are explicitly set.

Testing to see that pyeqrm gets the same dependent values
as the original.
"""

class Test_Conversions(unittest.TestCase):
    def test_width2(self):
        width_function=conversion_functions[
            'modified_Wells_and_Coppersmith_94_width']
        Mw = array([6.64 , 4.51 , 5.27 , 5.61 , 6.4])
        area=array([4.16869383e+02,3.09029543e+00,1.77827941e+01,
                    3.89045145e+01,2.39883292e+02])
        dip = array([ 35. , 35. , 35. , 35. , 35. ])
        width = width_function(dip,Mw,area)
        assert allclose([ 15,1.75792361,4.21696503,\
                          6.05476637,12.97166415],width)
        
    def test_length(self):
        Mw = 6.02
        dip = 45
        fault_width = 5

        area = conversion_functions[
            'modified_Wells_and_Coppersmith_94_area'](Mw)
        self.assert_ (allclose([area],[100]))
        width = conversion_functions[
            'modified_Wells_and_Coppersmith_94_width'](dip,Mw,area,
                                                        fault_width)
        self.assert_ (allclose([width],[5]))
        
        length = area/width
        self.assert_ (allclose([length],[20]))
        
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Conversions,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
