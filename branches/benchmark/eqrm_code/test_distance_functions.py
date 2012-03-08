import os
import sys
import unittest

from scipy import (asarray, allclose, newaxis, sqrt, arccos, sin, cos, pi,
                   newaxis)

from eqrm_code.distance_functions import distance_functions, Horizontal
from eqrm_code.projections import (azimuthal_orthographic,
                                   azimuthal_orthographic_ll_to_xy as ll2xy)
from eqrm_code.sites import Sites
from eqrm_code.distances import Distances

from eqrm_code import perf

#site=Sites(None,None)
projection=azimuthal_orthographic

lengths=0.0
azimuths=0.0
widths=0.0
dips = 10.0
depths=0.0

class Test_Distance_functions(unittest.TestCase):
    
    @perf.benchmark
    def test_Epicentral(self):
        dist = Distances(None,None,None,None,None,None,None,None,None,None)
        
        distance_type='Epicentral'

        rupture_centroid_lat=asarray((-31.0))
        rupture_centroid_lon=asarray((116.0))
        
        site_lat=asarray((-31,-32,-33,-34))        
        site_lon=asarray((116.0,116.0,116.0,116.0))

        distance=dist.raw_distances(site_lat,site_lon,
                                         rupture_centroid_lat,
                                         rupture_centroid_lon,
                                         lengths,azimuths,widths,dips,depths,
                                         distance_type,projection)


        d=asarray((0,1,2,3))*(1.852*60)
        d=d[:,newaxis]
        #rupture_centroid_lat=rupture_centroid_lat[newaxis,:]
        #rupture_centroid_lon=rupture_centroid_lon[newaxis,:]
        d2=self.as_the_cockey_flies(rupture_centroid_lat,
                                    rupture_centroid_lon,
                                    site_lat,site_lon)

        assert allclose(d,distance,rtol=0.001)
        assert allclose(d,d2)

    @perf.benchmark
    def test_Epicentral2(self):
        dist = Distances(None,None,None,None,None,None,None,None,None,None)
        
        distance_type='Epicentral'
        rupture_centroid_lat=asarray((-31.0,-33,-36))
        rupture_centroid_lon=asarray((116.0,118,222))
        

        site_lat=asarray((-31,-32,-33,-34))        
        site_lon=asarray((116.0,116.0,116.0,116.0))

        distance=dist.raw_distances(site_lat,site_lon,
                                         rupture_centroid_lat,
                                         rupture_centroid_lon,
                                         lengths,azimuths,widths,dips,depths,
                                         distance_type,projection)
        

        
        d=self.as_the_cockey_flies(rupture_centroid_lat,rupture_centroid_lon,
                                   site_lat,site_lon)

        assert allclose(d,distance,rtol=0.1)

    @perf.benchmark
    def test_mendez_distances(self):
        dist = Distances(None,None,None,None,None,None,None,None,None,None)
        
        rupture_centroid_lat=asarray((-31.0,-33,-36))
        rupture_centroid_lon=asarray((116.0,118,222))

        
        site_lat=asarray((-31,-32,-33,-34))        
        site_lon=asarray((116.0,116.0,116.0,116.0))
        
        distance1=dist.raw_distances(site_lat,site_lon,
                                          rupture_centroid_lat,
                                          rupture_centroid_lon,
                                          lengths,azimuths,widths,dips,depths,
                                          'Epicentral',projection)

        distance2=dist.raw_distances(site_lat,site_lon,
                                          rupture_centroid_lat,
                                          rupture_centroid_lon,
                                          lengths,azimuths,widths,dips,depths,
                                          'Obsolete_Mendez_epicentral',projection,
                                          trace_start_lat=rupture_centroid_lat,
                                          trace_start_lon=rupture_centroid_lon,
                                          rupture_centroid_x=0.0,rupture_centroid_y=0.0)

        assert allclose(distance1,distance2)
        
    @perf.benchmark
    def test_Hypocentral(self):
        dist = Distances(None,None,None,None,None,None,None,None,None,None)
        
        distance_type='Hypocentral'
        depths=10.0
        rupture_centroid_lat=asarray((-31.0,-33,-36))
        rupture_centroid_lon=asarray((116.0,118,222))
                
        site_lat=asarray((-31,-32,-33,-34)) 
        site_lon=asarray((116.0,116.0,116.0,116.0))


        d=dist.raw_distances(site_lat,site_lon,
                                  rupture_centroid_lat,
                                  rupture_centroid_lon,
                                  lengths,azimuths,widths,dips,depths,
                                  'Epicentral',projection)
        
        distance=dist.raw_distances(site_lat,site_lon,
                                         rupture_centroid_lat,
                                         rupture_centroid_lon,
                                         lengths,azimuths,widths,dips,depths,
                                         distance_type,projection)

        d=sqrt(d*d+depths*depths)
        assert allclose(d,distance)

    def as_the_cockey_flies(self,lat0,lon0,lat,lon):
        # Algorithm from ga website
        # Uses spherical geometry (rather than a projection)
        # to calculate epicentral distance
        lat=lat[:,newaxis]
        lon=lon[:,newaxis]
        L1=lat0*(pi/180)
        L2=lat*(pi/180)
        DG=(lon-lon0)*(pi/180)
        D = 1.852*60*180/pi*arccos(sin(L1)*sin(L2)+cos(L1)*cos(L2)*cos(DG))
        return D

    @perf.benchmark
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
        lengths = asarray((20.0,))
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
                             

        Rx = Horizontal(lat_sites, lon_sites, lat_events, lon_events, lengths,
                        azimuths, widths, dips, depths, projection,
                        trace_start_lat, trace_start_lon,
                        trace_start_x, trace_start_y)

        msg = ('Expected Rx=\n%s\ngot\n%s' % (str(expected_Rx), str(Rx)))
        self.failUnless(allclose(Rx, expected_Rx, rtol=5.0e-3), msg)

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
