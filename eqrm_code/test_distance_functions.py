import os
import sys
import unittest

from scipy import (asarray, allclose, newaxis, sqrt, arccos, sin, cos, pi,
                   newaxis)

from eqrm_code.distance_functions import * #distance_functions, Horizontal, \

from eqrm_code.projections import (azimuthal_orthographic,
                                   azimuthal_orthographic_ll_to_xy as ll2xy,
                                   azimuthal_orthographic_xy_to_ll as xy2ll)
from eqrm_code.sites import Sites
from eqrm_code.distances import Distances


# Warning - a bunch of global variables.
projection = azimuthal_orthographic
lengths = 0.0
azimuths = 0.0
widths = 0.0
dips = 10.0
depths = 0.0
depths_to_top = 0.0

class Test_Distance_functions(unittest.TestCase):
    def test_As_The_Cockey_Flies(self):
        # Test data from GA website 
        # As_The_Cockey_Flies implements the Great Circle method
        # 
        # http://www.ga.gov.au/earth-monitoring/geodesy/geodetic-techniques/distance-calculation-algorithms.html
        rupture_centroid_lat = asarray((-30))
        rupture_centroid_lon = asarray((150))
        
        site_lat = asarray((-31,-31,-32,-33,-34,-35,-40,-50,-60,-70,-80))
        site_lon = asarray((150,151,151,151,151,151,151,151,151,151,151))
        
        expected = asarray([[111.120],
                            [146.677],
                            [241.787],
                            [346.556],
                            [454.351],
                            [563.438],
                            [1114.899],
                            [2223.978],
                            [3334.440],
                            [4445.247],
                            [5556.190]])
        
        d = As_The_Cockey_Flies(rupture_centroid_lat,
                                rupture_centroid_lon,
                                site_lat,
                                site_lon)
        
        assert allclose(d,expected)
    
    def test_Epicentral(self):
        dist = Distances(None,None,None,None,None,None,None,None,None,None,None)
        
        distance_type='Epicentral'

        rupture_centroid_lat=asarray((-31.0))
        rupture_centroid_lon=asarray((116.0))
        
        site_lat=asarray((-31,-32,-33,-34))        
        site_lon=asarray((116.0,116.0,116.0,116.0))

        distance=dist.raw_distances(site_lat,
                                    site_lon,
                                    rupture_centroid_lat,
                                    rupture_centroid_lon,
                                    lengths,
                                    azimuths,
                                    widths,
                                    dips,
                                    depths,
                                    depths_to_top,
                                    distance_type,
                                    projection)


        d=asarray((0,1,2,3))*(1.852*60)
        d=d[:,newaxis]
        d2=As_The_Cockey_Flies(rupture_centroid_lat,
                               rupture_centroid_lon,
                               site_lat,
                               site_lon)

        assert allclose(d,distance,rtol=0.001)
        assert allclose(d,d2)

    def test_Epicentral2(self):
        dist = Distances(None,None,None,None,None,None,None,None,None,None,None)
        
        distance_type='Epicentral'
        rupture_centroid_lat=asarray((-31.0,-33,-36))
        rupture_centroid_lon=asarray((116.0,118,222))
        

        site_lat=asarray((-31,-32,-33,-34))        
        site_lon=asarray((116.0,116.0,116.0,116.0))

        distance=dist.raw_distances(site_lat,
                                    site_lon,
                                    rupture_centroid_lat,
                                    rupture_centroid_lon,
                                    lengths,
                                    azimuths,
                                    widths,
                                    dips,
                                    depths,
                                    depths_to_top,
                                    distance_type,
                                    projection)
        

        
        d = As_The_Cockey_Flies(rupture_centroid_lat,
                                rupture_centroid_lon,
                                site_lat,
                                site_lon)

        assert allclose(d,distance,rtol=0.1)


    def test_mendez_distances(self):
        dist = Distances(None,None,None,None,None,None,None,None,None,None,None)
        
        rupture_centroid_lat=asarray((-31.0,-33,-36))
        rupture_centroid_lon=asarray((116.0,118,222))

        
        site_lat=asarray((-31,-32,-33,-34))        
        site_lon=asarray((116.0,116.0,116.0,116.0))
        
        distance1=dist.raw_distances(site_lat,
                                     site_lon,
                                     rupture_centroid_lat,
                                     rupture_centroid_lon,
                                     lengths,
                                     azimuths,
                                     widths,
                                     dips,
                                     depths,
                                     depths_to_top,
                                     'Epicentral',
                                     projection)

        distance2=dist.raw_distances(site_lat,
                                     site_lon,
                                     rupture_centroid_lat,
                                     rupture_centroid_lon,
                                     lengths,
                                     azimuths,
                                     widths,
                                     dips,
                                     depths,
                                     depths_to_top,
                                     'Obsolete_Mendez_epicentral',
                                     projection,
                                     trace_start_lat=rupture_centroid_lat,
                                     trace_start_lon=rupture_centroid_lon,
                                     rupture_centroid_x=0.0,
                                     rupture_centroid_y=0.0)

        assert allclose(distance1,distance2)
        
    def test_Hypocentral(self):
        dist = Distances(None,None,None,None,None,None,None,None,None,None,None)
        
        distance_type='Hypocentral'
        depths=10.0
        rupture_centroid_lat=asarray((-31.0,-33,-36))
        rupture_centroid_lon=asarray((116.0,118,222))
                
        site_lat=asarray((-31,-32,-33,-34)) 
        site_lon=asarray((116.0,116.0,116.0,116.0))


        d=dist.raw_distances(site_lat,
                             site_lon,
                             rupture_centroid_lat,
                             rupture_centroid_lon,
                             lengths,
                             azimuths,
                             widths,
                             dips,
                             depths,
                             depths_to_top,
                             'Epicentral',
                             projection)
        
        distance=dist.raw_distances(site_lat,
                                    site_lon,
                                    rupture_centroid_lat,
                                    rupture_centroid_lon,
                                    lengths,
                                    azimuths,
                                    widths,
                                    dips,
                                    depths,
                                    depths_to_top,
                                    distance_type,
                                    projection)

        d=sqrt(d*d+depths*depths)
        assert allclose(d,distance)

    def test_Horizontal(self):
        # calculate length of 1 degree of great circle
        R = 6367.0		# Earth radius (km)
        circumference = 2*pi*R
        km_per_degree = circumference / 360.0

        # define array of events, all at 0,0
        lat_events = asarray((0.0,))
        lon_events = asarray((0.0,))

        azimuths = asarray((0.0,))
        widths = asarray((10.0,))
        lengths = asarray((40.0,))
        dips = asarray((90.0,))
        depths = asarray((30.0,))
        trace_start_lat = asarray((0.0,))
        trace_start_lon = asarray((0.0,))
        trace_start_x = asarray((0.0,))
        trace_start_y = asarray((0.0,))

        # define varying sites, at different positions
        # start at 1deg E of start, 0deg N, rotate CW, ~45deg per site
        lon_sites = asarray((1.0, 1.0, 0.0, -1.0, -1.0, -1.0, 0.0, 1.0))
        lat_sites = asarray((0.0, -1.0, -1.0, -1.0, 0.0, 1.0, 1.0, 1.0))

        # don't use this
        projection = None

        # define expected Rx values
        expected_Rx = asarray(
            [[+km_per_degree],	# 1 deg E, 0 deg N of start
             [+km_per_degree],	# 1 deg E, 1 deg S of start
             [ 0.0],			# 0 deg E, 1 deg S of start
             [-km_per_degree],	# 1 deg W, 1 deg S of start
             [-km_per_degree],	# 1 deg W, 0 deg N of start
             [-km_per_degree],	# 1 deg W, 1 deg N of start
             [ 0.0],			# 0 deg E, 1 deg N of start
             [+km_per_degree]])	# 1 deg E, 1 deg N of start
                             

        Rx = Horizontal(lat_sites, 
                        lon_sites, 
                        lat_events, 
                        lon_events, 
                        lengths,
                        azimuths, 
                        widths, 
                        dips, 
                        depths,
                        depths_to_top, 
                        projection,
                        trace_start_lat, 
                        trace_start_lon,
                        trace_start_x, 
                        trace_start_y)

        msg = ('Expected Rx=\n%s\ngot\n%s' % (str(expected_Rx), str(Rx)))
        self.failUnless(allclose(Rx, expected_Rx, rtol=5.0e-3), msg)

        
    def test_Rupture_vertical(self):
        # define varying sites, at different positions, units is deg
        #                      1        2        3
        #                  (-0.1,.5)  (0,.5)  (0.1,.5)
        #                        .      .      .
        #
        #                               (0,.4) end
        #                               |
        #                               |
        #                               |
        #                               |
        #           4  (-0.1,.2) .      . 5     .  6 (0.1,.2)
        #                               |
        #                               |
        #                               |
        #                               |
        #                               (0,0) start
        #
        #                        .      .      .
        #                  (-0.1,-.1)  (0,-.1)  (0.1,-.1)
        #                       7         8         9
        #
        
        # y values, since long is y due to local co-ord system
        y_sites = asarray((-0.1, 0.0, 0.1, -0.1, 0.0, 0.1, -0.1,  0.0,  0.1))
        # x values, since lat is x due to local co-ord system
        x_sites = asarray(( 0.5, 0.5, 0.5,  0.2, 0.2, 0.2, -0.1, -0.1, -0.1))
        
        # define array of events, all at 0,0
        lat_events = asarray((0.0,))
        lon_events = asarray((0.0,))

        azimuths = asarray((0.0,))
        
        widths = asarray((10.0,)) # No used in test
        lengths = asarray((0.4,))
        dips = asarray((90.0,))
        depths_to_top = asarray((0.0,))
        trace_start_lat = asarray((0.0,))
        trace_start_lon = asarray((0.0,))
        rupture_centroid_x = asarray((0.2,))
        rupture_centroid_y = asarray((0.0,))
        
        # Convert sites to lat/lon based on trace_start lat/lon
        lat_sites, lon_sites = xy2ll(x_sites, 
                                     y_sites, 
                                     trace_start_lat,
                                     trace_start_lon, 
                                     azimuths)
        
        projection = azimuthal_orthographic

        # define expected Rx values
        expected_Rrup_deg = asarray(
            [[2**0.5*0.1],
             [.1],
             [ 2**0.5*0.1],
             [.1],
             [0.0],
             [.1],
             [2**0.5*0.1],
             [.1],
             [2**0.5*0.1]])
        expected_Rrup = expected_Rrup_deg

        Rrup = Rupture(lat_sites, 
                       lon_sites, 
                       lat_events, 
                       lon_events, 
                       lengths,
                       azimuths, 
                       widths, 
                       dips, 
                       depths, 
                       depths_to_top,
                       projection,
                       trace_start_lat, 
                       trace_start_lon,
                       rupture_centroid_x, 
                       rupture_centroid_y)

        msg = ('Expected Rrup=\n%s\ngot\n%s' % (str(expected_Rrup), str(Rrup)))
        self.failUnless(allclose(Rrup, expected_Rrup, atol=1e-06), msg)
        
    def test_Rupture_Peer_2010(self):
        """
        Peer 2010/106 May 2010 Test Set 1, Cases 1 through 9  
        A vertical strike and depth_to_top = 0, so Rrup == Rjb
        """
        
        sites = asarray([[38.113, -122.000],
                         [38.113, -122.114],
                         [38.111, -122.570],
                         [38.000, -122.000],
                         [37.910, -122.000],
                         [38.225, -122.000],
                         [38.113, -121.886]]).T
        lat_sites = sites[0]
        lon_sites = sites[1]
        
        trace_start_lat = asarray([38.000])
        trace_start_lon = asarray([-122.000])
        
        lat_events = asarray([38.113])
        lon_events = asarray([-122.000])

        azimuths = asarray([0])
        widths = asarray([12])
        lengths = asarray([25])
        dips = asarray([90])
        depths_to_top = asarray([0])
        rupture_centroid_x = asarray([12.5])
        rupture_centroid_y = asarray([0])
        
        projection = azimuthal_orthographic

        # Expected Rrup == closest distance to rupture plane
        # Using values manually calculated using as_the_cockey_flies
        expected_Rrup= asarray([[0.0],
                                [9.9668666681573406],
                                [49.835436019848508],
                                [0.0],
                                [10.000800000041201],
                                [0.0],
                                [9.9668666681573406]])

        Rrup = Rupture(lat_sites, 
                       lon_sites, 
                       lat_events, 
                       lon_events, 
                       lengths,
                       azimuths, 
                       widths, 
                       dips, 
                       depths, 
                       depths_to_top,
                       projection,
                       trace_start_lat, 
                       trace_start_lon,
                       rupture_centroid_x, 
                       rupture_centroid_y)

        msg = ('Expected Rrup=\n%s\ngot\n%s' % (str(expected_Rrup), str(Rrup)))
        # Using absolute tolerance of 0.005 due to as_the_cockey_flies accuracy
        self.failUnless(allclose(Rrup, expected_Rrup, atol=5.0e-3), msg)
        
    def test_Rupture_non_vertical(self):
        # define varying sites, at different positions, units is deg
        #                      1        2        3
        #                  (-0.1,.5)  (0,.5)  (0.1,.5)
        #                        .      .      .
        #                                
        #                                _______
        #                               |(0,.4) end    
        #                               |       |      
        #                               |       |       
        #                               |       |       
        #           4  (-0.1,.2) .      . 5     |       .  6 (0.2,0.2)
        #                               |       |
        #                               |       |
        #                               |       |
        #                               |_______|
        #                               (0,0) start
        #
        #                        .      .      .
        #                  (-0.1,-.1)  (0,-.1)  (0.1,-.1)
        #                       7         8         9
        #
        # The projection of the rupture plane in this test is also shown in the
        # diagram
        
        # y values, since long is y due to local co-ord system
        y_sites = asarray((-0.1, 0.0, 0.1, -0.1, 0.0, 0.2, -0.1,  0.0,  0.1))
        # x values, since lat is x due to local co-ord system
        x_sites = asarray(( 0.5, 0.5, 0.5,  0.2, 0.2, 0.2, -0.1, -0.1, -0.1))
        
        # define array of events, all at 0,0
        lat_events = asarray((0.0,0.0))
        lon_events = asarray((0.0,0.0))

        azimuths = asarray((0.0,0.0))
        
        widths = asarray((0.14142136,0.14142136))
        lengths = asarray((0.4,0.4))
        dips = asarray((45.0,45.0))
        depths_to_top = asarray((0.0,0.1))
        trace_start_lat = asarray((0.0,0.0))
        trace_start_lon = asarray((0.0,0.0))
        rupture_centroid_x = asarray((0.2,0.2))
        rupture_centroid_y = asarray((0.05,0.05))
        
        # Convert sites to lat/lon based on trace_start lat/lon
        lat_sites, lon_sites = xy2ll(x_sites, 
                                     y_sites, 
                                     trace_start_lat[0],
                                     trace_start_lon[0], 
                                     azimuths[0])
        
        projection = azimuthal_orthographic

        # define expected Rrup values
        # from kaklamanosDis
        expected_Rrup_deg = asarray(
            [[0.14142136, 0.17320508],
             [0.10000000, 0.14142136],
             [0.12247449, 0.17320508],
             [0.10000000, 0.14142136],
             [0.00000000, 0.10000000],
             [0.14142136, 0.21213203],
             [0.14142136, 0.17320508],
             [0.10000000, 0.14142136],
             [0.12247449, 0.17320508]])
        expected_Rrup = expected_Rrup_deg

        Rrup = Rupture(lat_sites, 
                       lon_sites, 
                       lat_events, 
                       lon_events, 
                       lengths,
                       azimuths, 
                       widths, 
                       dips, 
                       depths, 
                       depths_to_top,
                       projection,
                       trace_start_lat, 
                       trace_start_lon,
                       rupture_centroid_x, 
                       rupture_centroid_y)

        msg = ('Expected Rrup=\n%s\ngot\n%s' % (str(expected_Rrup), str(Rrup)))
        self.failUnless(allclose(Rrup, expected_Rrup, atol=1e-06), msg)

    def test_Rupture_issue_143(self):

        #Using the example in the implementation tests, results_check.py file..

        # site order
        # rup centroid - 1st column
        # start trace, 2 km depth - 2nd column
        # start trace, 8 km depth - 3rd column
        # above rupture top edge
        lat_sites = asarray(( 0., -0.013904575, -0.013904575, -0.013904575))
        lon_sites = asarray(( 130., 129.9820023, 129.9280091, 129.9860954))

        # define array of events, 1st column, 2km depth.  2nd column 8km depth.
        lat_events = asarray((0.0,0.0))
        lon_events = asarray((130.0,130.0))

        azimuths = asarray((0.0,0.0))

        widths = asarray((3.090295, 3.090295))
        lengths = asarray((3.090295, 3.090295))
        dips = asarray((45.0, 45.0))
        depths_to_top = asarray((0.4548525, 6.4548525))
        trace_start_lat = asarray((-0.013904575, -0.013904575))
        trace_start_lon = asarray((129.9820023, 129.9280091))
        rupture_centroid_x = asarray((1.545148, 1.545148))
        rupture_centroid_y = asarray((2, 8)) # since the dip is 45 deg

        projection = azimuthal_orthographic

        expected_Rjb = asarray(
            [[.0, .0],
             [0.907415725, 0.907415725],
             [6.907415725, 6.907415725],
             [.0, .0]]) # EQRM is giving 0.45256

        Rjb = Joyner_Boore(lat_sites,
                           lon_sites,
                           lat_events,
                           lon_events,
                           lengths,
                           azimuths,
                           widths,
                           dips,
                           depths,
                           depths_to_top,
                           projection,
                           trace_start_lat,
                           trace_start_lon,
                           rupture_centroid_x,
                           rupture_centroid_y)

        msg = ('Expected Rjb=\n%s\ngot\n%s' % (expected_Rjb, Rjb))
        self.failUnless(allclose(Rjb, expected_Rjb, atol=1e-06), msg)

        # define expected Rrup values
        # from kaklamanosDis
        expected_Rrup = asarray(
            [[1.4202618, 6.9932919],
             [1.283279625, 6.966763617],
             [6.966763617, 9.768561],
             [0.4548525, 6.4548525]])

        Rrup = Rupture(lat_sites,
                       lon_sites,
                       lat_events,
                       lon_events,
                       lengths,
                       azimuths,
                       widths,
                       dips,
                       depths,
                       depths_to_top,
                       projection,
                       trace_start_lat,
                       trace_start_lon,
                       rupture_centroid_x,
                       rupture_centroid_y)

        msg = ('Expected Rrup=\n%s\ngot\n%s' % (str(expected_Rrup), str(Rrup)))
        self.failUnless(allclose(Rrup, expected_Rrup, atol=1e-06), msg)

    def test_Joyner_Boore(self):
        # define varying sites, at different positions, units is deg
        #                      1        2        3
        #                  (-0.1,.5)  (0,.5)  (0.1,.5)
        #                        .      .      .
        #                                
        #                                _______
        #                               |(0,.4) end    
        #                               |       |      
        #                               |       |       
        #                               |       |       
        #           4  (-0.1,.2) .      . 5     |       .  6 (0.2,0.2)
        #                               |       |
        #                               |       |
        #                               |       |
        #                               |_______|
        #                               (0,0) start
        #
        #                        .      .      .
        #                  (-0.1,-.1)  (0,-.1)  (0.1,-.1)
        #                       7         8         9
        #
        # Two events are defined:
        # dip = 90 (vertical)
        # dip = 45 (non-vertical)
        #
        # The projection of the rupture plane where dip-45 test is shown in the
        # diagram
        # Rjb is the closest distance to the projected rupture plane
        
        # y values, since long is y due to local co-ord system
        y_sites = asarray((-0.1, 0.0, 0.1, -0.1, 0.0, 0.2, -0.1,  0.0,  0.1))
        # x values, since lat is x due to local co-ord system
        x_sites = asarray(( 0.5, 0.5, 0.5,  0.2, 0.2, 0.2, -0.1, -0.1, -0.1))
        
        # define array of events, all at 0,0
        lat_events = asarray((0.0,0.0))
        lon_events = asarray((0.0,0.0))

        azimuths = asarray((0.0,0.0))
        
        widths = asarray((0.14142136,0.14142136))
        lengths = asarray((0.4,0.4))
        dips = asarray((90.0,45.0))
        depths_to_top = asarray((0.0,0.1))
        trace_start_lat = asarray((0.0,0.0))
        trace_start_lon = asarray((0.0,0.0))
        rupture_centroid_x = asarray((0.2,0.2))
        rupture_centroid_y = asarray((0.0,0.05))
        
        # Convert sites to lat/lon based on trace_start lat/lon
        lat_sites, lon_sites = xy2ll(x_sites, 
                                     y_sites, 
                                     trace_start_lat[0],
                                     trace_start_lon[0], 
                                     azimuths[0])
        
        projection = azimuthal_orthographic

        
        expected_Rjb = asarray(
            [[0.14142136, 0.14142136],
             [0.10000000, 0.10000000],
             [0.14142136, 0.10000000],
             [0.10000000, 0.10000000],
             [0.00000000, 0.00000000],
             [0.20000000, 0.10000000],
             [0.14142136, 0.14142136],
             [0.10000000, 0.10000000],
             [0.14142136, 0.10000000]])

        Rjb = Joyner_Boore(lat_sites, 
                           lon_sites, 
                           lat_events, 
                           lon_events, 
                           lengths,
                           azimuths, 
                           widths, 
                           dips, 
                           depths, 
                           depths_to_top,
                           projection,
                           trace_start_lat, 
                           trace_start_lon,
                           rupture_centroid_x, 
                           rupture_centroid_y)

        msg = ('Expected Rjb=\n%s\ngot\n%s' % (expected_Rjb, Rjb))
        self.failUnless(allclose(Rjb, expected_Rjb, atol=1e-06), msg)    
        
        
def m_to_py1(m):
    """
    Input
    m='''depth =

     5     6     7    10
    '''
    
    Output
    prints: depth = [5.0, 6.0, 7.0, 10.0]
    """
    name=m.split(' ')[0]
    values=m.split('=')[1]
    values=values.split('\n')
    values=[value for value in values if len(value)>0][0]
    values=values.split(' ')
    values=[float(value) for value in values if len(value)>0]
    print name,'=',values
    
def m_to_py2(m):
    """
    Input
    '''
    depth =

     5
     6
     7
     10
    '''
    
    Output
    prints: depth = [5.0, 6.0, 7.0, 10.0]
    """
    name=m.split(' ')[0]
    values=m.split('=')[1]
    values=values.replace(' ','')
    values=values.split('\n')
    values=[float(value) for value in values if len(value)>0]
    print name,'=',values
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Distance_functions,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
