#!/usr/bin/env python

import os
import sys
import unittest
from os.path import join

from scipy import allclose

from eqrm_code import polygon_class
from eqrm_code.polygon_class import get_independent_polygons_obsolete, \
     Empty_polygon, polygon_object
from eqrm_code.util import determine_eqrm_path
#from geos_interface import Empty_polygon

australia = [(-11.0, 142.0), (-25.0, 153.0), (-38.0, 149.0), \
             (-37.0, 140.0), (-31.0, 130.0), (-35.0, 117.0), \
             (-21.0, 113.0), (-11.0, 133.0), (-11.0, 142.0)]

australia_exclude = [[(-11.0, 142.0),(-17.0, 140.0),\
                      (-14.0, 134.0),(-7.0, 139.0),(-11.0, 142.0)]]
#The Great Australian Bite (as an exclude)

l=116.6
r=116.8
hi=-31.6
lo=-31.8
small_square = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,l)]
small_square_area = (hi-lo)*(r-l)

l=116.65
r=116.75
hi=-31.0
lo=-32.0
narrow_square = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,l)]
narrow_square_area = (hi-lo)*(r-l)

l=116.5
r=117.0
hi=-31.5
lo=-32.0
large_square = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,l)]
large_square_area = (hi-lo)*(r-l)


l=116.7
r=118.0
hi=-31.0
lo=-32.2
source_square = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,l)]
source_square_area = (hi-lo)*(r-l)

invalid = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,r)]



class Test_Polygon_Class(unittest.TestCase):
    def test_polygon_object(self):
        poly = polygon_class.polygon_object(small_square)
        assert allclose(poly.area,small_square_area)

    def test_polygon_object_with_excludes(self):
        poly = polygon_class.polygon_with_excludes(large_square,[small_square])
        assert allclose(poly.area,large_square_area-small_square_area)
        
    def FIXME_test_polygon_object_invalid(self):
        try:
            poly = polygon_class.polygon_object(invalid)
            msg = 'Should have raised an invalid polygon!!!!'
            assert 1 == 0, msg
        except ValueError:
            pass

    def test_polygon_difference(self):
        poly1 = polygon_class.polygon_object(large_square)
        poly2 = polygon_class.polygon_object(small_square)
        poly = poly1.difference(poly2)
        assert allclose(poly.area,large_square_area-small_square_area)

    def test_polygon_difference2(self):
        poly1 = polygon_class.polygon_object(small_square)
        poly2 = polygon_class.polygon_object(source_square)
        poly = poly1.difference(poly2)
        assert allclose(poly.area,small_square_area/2)

    def test_polygon_difference3(self):
        poly1 = polygon_class.polygon_object(large_square)
        poly2 = polygon_class.polygon_object(source_square)
        poly = poly1.difference(poly2)
        assert allclose(poly.area,large_square_area*2/5)

    def test_polygon_difference4(self):
        poly1 = polygon_class.polygon_object(large_square)
        poly2 = polygon_class.polygon_object(large_square)
        poly = poly1.difference(poly2)
        assert allclose(poly.area,0.)
        assert poly is polygon_class.empty_polygon

        
    def test_complex_polygon_difference(self):
        poly1 = polygon_class.polygon_object(small_square)
        poly2 = polygon_class.polygon_object(narrow_square)
        poly = poly1.difference(poly2)
        assert allclose(poly.area,small_square_area/2)
        
        
    def test_polygon_intersection(self):
        poly1 = polygon_class.polygon_object(small_square)
        poly2 = polygon_class.polygon_object(large_square)
        poly = poly1.intersection(poly2)
        assert poly1 is poly

    def test_polygon_intersection2(self):
        poly1 = polygon_class.polygon_object(small_square)
        poly2 = polygon_class.polygon_object(source_square)
        poly = poly1.intersection(poly2)
        assert allclose(poly.area,small_square_area/2)

    def test_polygon_system_test(self):
        poly1 = polygon_class.polygon_object(small_square)
        poly2 = polygon_class.polygon_object(large_square)
        poly3 = polygon_class.polygon_object(source_square)
        poly = poly3.difference(poly1)
        assert allclose(poly.area,source_square_area-small_square_area/2)
        poly = poly2.intersection(poly)
        assert allclose(poly.area,large_square_area*3/5-small_square_area/2)

    def test_polygon_with_exclude(self):
        poly = polygon_class.polygon_object\
               (large_square,[small_square,narrow_square])
        area_small_union_narrow = (small_square_area/2+narrow_square_area)
        area_narrow_diff_large = narrow_square_area/2
        area = large_square_area - area_small_union_narrow\
               + area_narrow_diff_large
        assert allclose(area,poly.area)

    def _test_speed(self):
        from time import time
        t0=time()
        for i in xrange(1000):
            poly1 = polygon_class.polygon_object(small_square)
            poly2 = polygon_class.polygon_object(large_square)
            poly3 = polygon_class.polygon_object(source_square)
            poly = poly3.difference(poly1)
            assert allclose(poly.area,source_square_area-small_square_area/2)
            poly = poly2.intersection(poly)
            assert allclose(poly.area,large_square_area*3/5-small_square_area/2)
        print 'Time to run 1000 polygon diffs: '+str(time()-t0)

    def _test_get_independent_polygons(self):
        from eqrm_code.generation_polygon import polygons_from_xml
        eqrm_dir = determine_eqrm_path()
        #print "eqrm_dir", eqrm_dir
        file_location = join(eqrm_dir, 'test_resources','sample_event.xml')
        #print "file_location", file_location
        polygons,mag_type = polygons_from_xml(file_location,
                      azi=[180,180],
                      dazi=[10,10],
                      fault_dip=[30,30],
                      fault_width=15,
                      override_xml=True)
        independent_polygons=get_independent_polygons_obsolete(polygons)
        assert len(independent_polygons)==3
        
        #conformance tests, could change if I change the way area works
        assert allclose(independent_polygons[0].area,80.685560816)
        assert allclose(independent_polygons[1].area,16.314439184)
        assert allclose(independent_polygons[2].area, 27.919220365)

        #no more conformance tests (these are real ones):
        for i in range(len(independent_polygons)):
            for j in range(len(independent_polygons)):
                if not i == j:
                    polygoni = independent_polygons[i]
                    polygonj = independent_polygons[j]
                    int = polygoni.intersection(polygonj)
                    assert int.area == 0

        area1=0
        area2=0

        for poly in polygons:
            area1+=poly.area
        for poly in independent_polygons:
            area2+=poly.area
        assert not allclose(area1,area2)
        assert allclose(area2,area1-polygons[0].intersection(polygons[1]).area)
                    
    def _test_get_independent_polygons2(self):
        # This fails. The only way to fix it is to play with geos.

        # The error occurs because a linestring (a degenerate poly)
        # is used somewhere.
        # It should work if union works ;)
        from eqrm_code.generation_polygon import polygons_from_xml
        polygons,mag_type = polygons_from_xml(join('..','test_resources',
                                                   'sample_event.xml'))
        independent_polygons=get_independent_polygons_obsolete(polygons)

        super_poly = independent_polygons[0]
        area = 0
        for poly in independent_polygons:
            area+=poly.area
            super_poly = super_poly.union(poly)
        assert allclose(super_poly.area,area)

    def test_contains_point(self):
        outline = [(-32.3999999999999990, 151.1500000000000100),
     (-32.7500000000000000, 152.1699999999999900),
     (-33.4500000000000030, 151.4300000000000100),
     (-32.3999999999999990, 151.1500000000000100)]

        # This point is outside the triangle
        point = (-33.280000000000001, 151.61000000000001)
        po = polygon_object(outline)
        is_in = po.contains_point(point)
        assert not is_in    
     
    def test_contains_point2(self):
        outline = [(-35.0, 149.5), (-32.399999999999999, 149.5),
                      (-32.399999999999999, 151.15000000000001),
                      (-33.450000000000003, 151.43000000000001),
                      (-32.75, 152.16999999999999),
                      (-32.75, 152.75999999999999),
                      (-34.399999999999999, 151.34999999999999),
                      (-34.740000000000002, 151.15000000000001),
                      (-35.0, 151.09999999999999), (-35.0, 149.5)]
        
        # This point is outside 
        point = (-32.789999999999999, 151.96000000000001)
        po = polygon_object(outline)
        is_in = po.contains_point(point)
        assert not is_in     

        point = (-33.170000000000002, 152.12)
        is_in = po.contains_point(point)
        assert is_in
          
     
    def test_contains_point3(self):
        outline = [[ -35.    , 149.5  ],
                   [ -32.925  ,149.5  ],
                   [ -32.925  ,151.4  ],
                   [ -33.5    ,151.9  ],
                   [ -33.25   ,152.25 ],
                   [ -33.25   ,152.33 ],
                   [ -34.4    ,151.35 ],
                   [ -34.74   ,151.15 ],
                   [ -35.     ,151.1  ],
                   [ -35.     ,149.5  ]]
        
        # The position of these points have not been manually checked.
        point = (-32.789999999999999, 151.96000000000001)
        po = polygon_object(outline)
        is_in = po.contains_point(point)
        assert not is_in

        point = (-33.109999999999999, 151.94)
        is_in = po.contains_point(point)
        assert not is_in

        point = (-33.170000000000002, 152.12)
        is_in = po.contains_point(point)
        assert not is_in
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Polygon_Class,'test')
    #suite = unittest.makeSuite(Test_Polygon_Class,'test_contains_point2')
    runner = unittest.TextTestRunner()
    runner.run(suite)


