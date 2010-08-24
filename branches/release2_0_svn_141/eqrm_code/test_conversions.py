
import unittest
import math

from scipy import array, allclose, exp, log, power

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
        

    def test_calc_depth_to_top(self):
        """Test the calc_depth_to_top() function."""

        calc_depth_to_top = conversion_functions['calc_depth_to_top']

        # test an invalid datatype case (raises AssertError)
        depth = 10.0
        width = 20.0
        delta = 0
        self.failUnlessRaises(AssertionError,
                              calc_depth_to_top, depth, width, delta)

        # test an invalid shape case (raises AssertError)
        depth = array([10.0, 20.0])
        width = array([20.0])
        delta = array([0])
        self.failUnlessRaises(AssertionError,
                              calc_depth_to_top, depth, width, delta)

        # test a single value, delta=0, depth_to_top == depth
        depth = array([10.0])
        width = array([20.0])
        delta = array([0])
        expected = depth		# Ztor == depth if delta == 0
        Ztor = calc_depth_to_top(depth, width, delta)
        self.failUnless(allclose(Ztor, expected))
        
        # test many cases in one array set
        Ztor_45 = 20.0-10.0/2*math.sin(math.pi*2*45.0/360) # depth at 45 degrees
        #                  +- horizontal, Ztor==depth
        #                  |     +- vertical, Ztor=depth-width/2
        #                  |     |     +- 30 degrees, Ztor=depth-width/4
        #                  |     |     |     +- vertical, Ztor=depth-width/2
        #                  |     |     |     |            (negative depth)
        #                  |     |     |     |     +- 45 fault -> .707 sin()
        #                  V     V     V     V     V
        depth =    array([20.0, 20.0, 20.0, 10.0, 20.0])
        width =    array([10.0, 10.0, 10.0, 30.0, 10.0])
        delta =    array([ 0.0, 90.0, 30.0, 90.0, 45.0])
        expected = array([20.0, 15.0, 17.5, -5.0, Ztor_45])
        Ztor = calc_depth_to_top(depth, width, delta)
        msg = 'Expected %s same as %s' % (str(Ztor), str(expected))
        self.failUnless(allclose(Ztor, expected), msg)
        

    def test_convert_Z10_to_Z25(self):
        """Test the convert_Z10_to_Z25() function."""

        convert_Z10_to_Z25 = conversion_functions['convert_Z10_to_Z25']

        # test a scalar value
        Z10 = 1000.0
        expected_Z25 = 3595 + 0.519
        Z25 = convert_Z10_to_Z25(Z10)
        msg = ('Z1.0 is %.1f, expected Z2.5=%.1f, got %.1f'
               % (Z10, expected_Z25, Z25))
        self.failUnlessEqual(Z25, expected_Z25, msg)

        # now try an array
        Z10 = array([[1.0, 10.0],[100.0, 1000.0]])
        expected_Z25 = Z10*3.595 + 0.519
        Z25 = convert_Z10_to_Z25(Z10)
        msg = ('Z1.0 is %s, expected Z2.5=%s, got %s'
               % (str(Z10), str(expected_Z25), str(Z25)))
        self.failUnless(allclose(Z25, expected_Z25), msg)

        
    def test_convert_Vs30_to_Z10(self):
        """Test the convert_Vs30_to_Z10() function."""

        convert_Vs30_to_Z10 = conversion_functions['convert_Vs30_to_Z10']

        # internal reimplementation of the convert_Vs30_to_Z10() function
        def fudge(Vs30):
            return exp(28.5 - (3.82/8.0)*log(power(Vs30, 8) + power(378.7, 8)))

        # test a scalar value
        Vs30 = 1000.0
        expected_Z10 = fudge(Vs30)
        Z10 = convert_Vs30_to_Z10(Vs30)
        msg = ('Vs30 is %.1f, expected Z1.0=%.1f, got %.1f'
               % (Vs30, expected_Z10, Z10))
        self.failUnlessEqual(Z10, expected_Z10, msg)

        # now try an array
        Vs30 = array([[1.0, 10.0],[100.0, 1000.0]])
        expected_Z10 = fudge(Vs30)
        Z10 = convert_Vs30_to_Z10(Vs30)
        msg = ('Vs30 is %s, expected Z1.0=%s, got %s'
               % (str(Vs30), str(expected_Z10), str(Z10)))
        self.failUnless(allclose(Z10, expected_Z10), msg)

        

################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Conversions,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
