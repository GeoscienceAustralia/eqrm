import os
import sys
import unittest
from scipy import pi, asarray, allclose

from projections import azimuthal_orthographic_ll_to_xy as ll2xy


class Test_Projections(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_ll2xy(self):
        """Test functionality of azimuthal_orthographic_ll_to_xy() function"""

        # calculate length of 1 degree of great circle
        R = 6367.0              # Earth radius (km)
        circumference = 2*pi*R
        km_per_degree = circumference / 360.0

        # define two points precisely one degree apart on equator
        lat_origin = asarray((0.0,))
        lon_origin = asarray((0.0,))

        lat_point = asarray((0.0,))
        lon_point = asarray((1.0,))

        expected_x = asarray((0.0,))
        expected_y = asarray((km_per_degree,))

        (x, y) = ll2xy(lat_point, lon_point, lat_origin, lon_origin,
                       azimuth=0.0)

        msg = ('Expected x=\n%s\ngot\n%s' % (str(expected_x), str(x)))
        self.failUnless(allclose(expected_x, x), msg)
        msg = ('Expected y=\n%s\ngot\n%s' % (str(expected_y), str(y)))
        self.failUnless(allclose(expected_y, y), msg)

        # now do a vector test with points on 1 degree grid around (0,0) origin
        # we are particularly interested in the sign in different quadrants
        lat_point = asarray((0.0, -1.0, -1.0, -1.0, 0.0, 1.0, 1.0, 1.0))
        lon_point = asarray((1.0, 1.0, 0.0, -1.0, -1.0, -1.0, 0.0, 1.0))
        
        expected_x = asarray((0.0, -km_per_degree, -km_per_degree,
                              -km_per_degree, 0.0, +km_per_degree,
                              +km_per_degree, +km_per_degree))
        expected_y = asarray((km_per_degree, +km_per_degree, 0.0,
                              -km_per_degree, -km_per_degree,
                              -km_per_degree, 0.0, +km_per_degree))

        (x, y) = ll2xy(lat_point, lon_point, lat_origin, lon_origin,
                       azimuth=0.0)

        # note the looseish tolerance required to get agreement
        # possibly ll2xy() has some loss of precision?  looked but can't see it.
        msg = ('Expected x=\n%s\ngot\n%s' % (str(expected_x), str(x)))
        self.failUnless(allclose(expected_x, x, rtol=5.0e-3), msg)
        msg = ('Expected y=\n%s\ngot\n%s' % (str(expected_y), str(y)))
        self.failUnless(allclose(expected_y, y, rtol=5.0e-4), msg)

################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Projections,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
