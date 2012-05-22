import os
import sys
import unittest
import tempfile
from projections import azimuthal_orthographic
from scipy import array, allclose
import numpy as np

from eqrm_code.sites import Sites, truncate_sites_for_test
from eqrm_code import file_store

projection = azimuthal_orthographic


class Test_Sites(unittest.TestCase):
    def setUp(self):
        file_store.SAVE_METHOD = None

    def tearDown(self):
        pass

    def testing(self):
        attributes = {'mo': array(['money', 'soup']),
                      'SITE_CLASS': array(['E', 'C'])}
        latitude = [10, 20]
        longitude = [1, 2]
        sites = Sites(latitude, longitude, **attributes)
        site_class2Vs30 = {'C': 30, 'E': 40}
        sites.set_Vs30(site_class2Vs30)

        actual = array(latitude)
        self.assert_(allclose(sites.latitude, actual, 0.001))
        actual = array(longitude)
        self.assert_(allclose(sites.longitude, actual, 0.001))
        actual = array(['money', 'soup'])
        for (att, act) in map(None, sites.attributes['mo'], actual):
            self.assert_(att == act)
        actual = array([40, 30])
        self.assert_(allclose(sites.attributes['Vs30'], actual, 0.001))

        site_class2Vs30 = {'C': 30}
        try:
            sites.set_Vs30(site_class2Vs30)
        except KeyError:
            pass
        else:
            self.failUnless(False, "KeyError not raised")

    def test_read_from_file(self):
        """Test reading Sites data from a file."""

        # create dummy CSV file - this is bridges data, but sites should handle anything
        lat = [-35.352085, -35.348677, -35.336884, -35.345209,
               -35.340859, -35.301472, -35.293012, -35.320122]
        lon = [149.236994, 149.239383, 149.241625, 149.205986,
               149.163037, 149.141364, 149.126767, 149.063810]
        clsf = ['HWB17', 'HWB17', 'HWB17', 'HWB22',
                 'HWB3', 'HWB17', 'HWB10', 'HWB28']
        cat = ['BRIDGE', 'BRIDGE', 'BRIDGE', 'BRIDGE',
               'BRIDGE', 'BRIDGE', 'BRIDGE', 'BRIDGE']
        skew = [0, 32, 20, 4, 0, 0, 12, 0]
        span = [2, 3, 6, 2, 1, 1, 3, 3]
        cls = ['E', 'F', 'G', 'D', 'E', 'F', 'G', 'C']
        attribute_keys = ['BID', 'STRUCTURE_CLASSIFICATION']

        dummy_csv_data = ['BID,LONGITUDE,LATITUDE,STRUCTURE_CLASSIFICATION,'
                          'STRUCTURE_CATEGORY,SKEW,SPAN,SITE_CLASS',
                          '2,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (lon[0], lat[0], clsf[0], cat[0], skew[0], span[0], cls[0]),
                          '3,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (lon[1], lat[1], clsf[1], cat[1], skew[1], span[1], cls[1]),
                          '4,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (lon[2], lat[2], clsf[2], cat[2], skew[2], span[2], cls[2]),
                          '5,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (lon[3], lat[3], clsf[3], cat[3], skew[3], span[3], cls[3]),
                          '6,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (lon[4], lat[4], clsf[4], cat[4], skew[4], span[4], cls[4]),
                          '7,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (lon[5], lat[5], clsf[5], cat[5], skew[5], span[5], cls[5]),
                          '8,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (lon[6], lat[6], clsf[6], cat[6], skew[6], span[6], cls[6]),
                          '9,%.6f,%.6f,%s,%s,%s,%s,%s'
                              % (lon[7], lat[7], clsf[7], cat[7], skew[7], span[7], cls[7])]

        (handle, filename) = tempfile.mkstemp('.csv', 'test_sites_')
        os.close(handle)

        f = open(filename, 'wb')
        f.write('\n'.join(dummy_csv_data))
        f.close()

        # now read file - pass attribute_conversion as **kwargs data
        sites = Sites.from_csv(filename, BID=int, STRUCTURE_CLASSIFICATION=str)

        # make sure we have required attributes, and only those attributes
        self.failUnless(hasattr(sites, 'longitude'))
        self.failUnless(np.all(sites.longitude == lon))
        self.failUnless(hasattr(sites, 'latitude'))
        self.failUnless(np.all(sites.latitude == lat))

        self.failUnless(len(sites.attributes) == len(attribute_keys))
        for key in sites.attributes:
            if key not in attribute_keys:
                self.fail("Found unexpected .attribute key '%s'" % key)

        # repeat above test, pass attributes a dict
        attr_dict = {'BID': int, 'STRUCTURE_CATEGORY': str, 'SKEW': float,
                     'SPAN': int, 'SITE_CLASS': str}
        attribute_keys = ['BID', 'STRUCTURE_CATEGORY', 'SKEW', 'SPAN', 'SITE_CLASS']
        sites = Sites.from_csv(filename, **attr_dict)

        # make sure we have required attributes, and only those attributes
        self.failUnless(hasattr(sites, 'longitude'))
        self.failUnless(np.all(sites.longitude == lon))
        self.failUnless(hasattr(sites, 'latitude'))
        self.failUnless(np.all(sites.latitude == lat))

        self.failUnless(len(sites.attributes) == len(attribute_keys))
        for key in sites.attributes:
            if key not in attribute_keys:
                self.fail("Found unexpected .attribute key '%s'" % key)

        # get rid of test data file 
        os.remove(filename)

    def testing_truncate_sites_for_test(self):
        attributes = {'mo': array(['money', 'soup']),
                      'SITE_CLASS': array(['E', 'C']),
                      'id': array([1, 2])}
        latitude = [10, 20]
        longitude = [1, 2]
        sites = Sites(latitude, longitude, **attributes)
        use_site_indexes = False
        site_indexes = array([2])
        new_sites = truncate_sites_for_test(use_site_indexes, sites,
                                            site_indexes)
        self.failUnless(allclose(array([1, 2]), new_sites.attributes['id']))

        use_site_indexes = True
        site_indexes = array([2])
        new_sites = truncate_sites_for_test(use_site_indexes,sites,
                                            site_indexes)
        self.failUnlessEqual(site_indexes, new_sites.attributes['id'])

    def test_closest_site(self):
        # Test data from GA website 
        # http://www.ga.gov.au/earth-monitoring/geodesy/geodetic-techniques/distance-calculation-algorithms.html
        latitude  = [-31,-31,-32,-33,-34,-35,-40,-50,-60,-70,-80]
        longitude = [150,151,151,151,151,151,151,151,151,151,151]
        sites = Sites(latitude, longitude)
        
        # Point A from website
        point_lat = -30
        point_lon = 150
        
        closest_site = sites.closest_site(point_lat, point_lon)
        
        assert sites.latitude[closest_site] == latitude[0]
        assert sites.longitude[closest_site] == longitude[0]

################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Sites, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
