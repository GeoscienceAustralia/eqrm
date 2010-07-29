import os
import sys
import unittest

from scipy import allclose

from eqrm_code.geos_interface import *


"""
Geos (a c++ port of JTS-topology-suit) (python bindings at hobu.net) is
an engine to work with polygons.

See the JTS manules for documentation.

It inputs and outputs strings (in well-know-text (wkt)) format, so a lot
of the geos_interface is converting array-format polygons to wkt.

geos doesn't allow complex polygons, but they can be represented as
multipolygons, or polygons with excludes.

geos is really pedantic, and only accepts it's unique representations. For
example, 2 simple polygons that touch at a single point MUST be represented as
a multipolygon, NOT as a single polygon (with a constriction point), and
NOT as a polygon with an exclusion zone.

Linestrings are degenerate (zero area) polygon, which we will just ignore.
"""

l=116.6
r=116.8
hi=-31.6
lo=-31.8
small_square = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,l)]
small_square_area = (hi-lo)*(r-l)

l=116.5
r=117.0
hi=-31.5
lo=-32.0
large_square = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,l)]
large_square_area = (hi-lo)*(r-l)

l=116.65
r=116.75
hi=-31.0
lo=-32.0
narrow_square = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,l)]
narrow_square_area = (hi-lo)*(r-l)

# a polygon that geos should think is invalid
l=116.7
r=118.0
hi=-31.0
lo=-32.2
invalid = [(lo,l),(lo,r),(hi,r),(hi,l),(lo,r)]

class Test_Geos_Interface(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_polygon_to_geos_polygon(self):
        geos_poly = polygon_to_geos_polygon(small_square)
        #assert geos_poly.isSimple()
        assert geos_poly.is_valid
        assert allclose(geos_poly.area,small_square_area)

    def test_polygon_to_geos_polygon_invalid(self):
        error_raised = False
        try:
            geos_poly=polygon_to_geos_polygon(invalid)
            print "geos_poly.is_ring", geos_poly.boundary.is_ring
        except:
            error_raised = True
        assert error_raised
       
    def test_polygon_to_geos_polygon_invalidII(self):
        error_raised = False
        try:
            geos_poly=polygon_to_geos_polygon([(0,0),(1,0),(0,1),(1,1)])
            print "geos_poly.is_ring", geos_poly.boundary.is_ring
        except:
            error_raised = True
        assert error_raised
        
                 

    def test_polygon_to_geos_polygon_with_excludes(self):
        geos_poly = polygon_to_geos_polygon(small_square,[narrow_square])
        assert allclose(geos_poly.area,small_square_area/2)

    def test_wkt_to_list_empty_polygon(self):
        geos_poly1 = polygon_to_geos_polygon(small_square)
        geos_poly2 = polygon_to_geos_polygon(large_square)
        geos_poly = geos_poly1.difference(geos_poly2)
        # [[]] older version of shapely 1.0.7
        # [] newer version of shapely 1.2.1
        assert list_multipolygon(geos_poly)==[[]] or list_multipolygon(geos_poly)==[]
        
        
    def test_wkt_to_multipolygon_list_simple_polygon(self):
        geos_poly = polygon_to_geos_polygon(small_square)
        
        poly_list = list_multipolygon(geos_poly)
        #print "list_multipolygon poly_list", poly_list
        poly_list = wkt_to_multipolygon_list(geos_poly.wkt)
        #print "poly_list", poly_list
        geos_poly2 = obsolete_multipolygon_list_to_geos_polygon(poly_list)
        assert same_polygon(geos_poly,geos_poly2)

    def test_wkt_to_multipolygon_list_complex_polygon(self):
        geos_poly = polygon_to_geos_polygon(large_square)
        geos_poly = geos_poly.difference(polygon_to_geos_polygon(small_square))

        poly_list = wkt_to_multipolygon_list(geos_poly.wkt)
        geos_poly2 = obsolete_multipolygon_list_to_geos_polygon(poly_list) 
        assert same_polygon(geos_poly,geos_poly2)


    def test_wkt_to_multipolygon_list_multipolygon(self):
        geos_poly = polygon_to_geos_polygon(narrow_square)
        geos_poly = geos_poly.difference(polygon_to_geos_polygon(small_square))
        poly_list = wkt_to_multipolygon_list(geos_poly.wkt)
        
        geos_poly2 = obsolete_multipolygon_list_to_geos_polygon(poly_list)
        assert same_polygon(geos_poly,geos_poly2)

    def test_obsolete_points_to_linestring(self):
        point_a=(0,0)
        point_b=(1,1)
        point_c=(2,2)
        points=(point_a,point_b,point_c)
        linestring=obsolete_points_to_linestring(points)
        points_2=obsolete_linestring_to_points(linestring)
        assert allclose(points,points_2)

    def _test_matlab_polygon_to_multipolygon_list(self):
        points=[[0,0],[0,3],[3,3],[3,0],[0,0]]
        exclude=[[1,1],[1,2],[0,0]]
        
        poly=polygon_to_geos_polygon(points)
        print poly.is_valid
        answer=matlab_polygon_to_multipolygon_list(points+exclude)
        print (answer.area)

        print (answer.wkt)
        assert allclose(answer.area,8.5)

    def _test_matlab_polygon_to_multipolygon_list_big(self):
        from scipy.stats import uniform       
        n_triangles=3
        triangle_array=uniform(0).rvs(n_triangles*6)
        triangle_array.shape=n_triangles,3,2

        triangle=triangle_array[0].tolist()
        triangle=triangle+[triangle[0]]
        print triangle
        poly1=polygon_to_geos_polygon(triangle)
        for triangle in triangle_array[1:]:
            triangle=triangle.tolist()
            triangle=triangle+[triangle[0]]          
            poly1=poly1.symDifference(polygon_to_geos_polygon(triangle))


        print
        print
        print triangle_array.tolist()
        triangle_list=[]
        point0=triangle_array.tolist()[0][0]
        for triangle in triangle_array.tolist():
            print "triangle"
            print triangle
            triangle.append(triangle[0])
            triangle.append(point0)
            print "triangle2"
            print triangle
            
            triangle_list+=[triangle]
        triangle_list[0].pop()
        print 'TRIANLGE LIST',triangle_list
        print
        print
        print
        triangle_list2=[]
        for triangle in triangle_list:
            triangle_list2+=triangle
       
        #for triangle in triangle_list:
        #    print "triangle2",triangle
            
            
            
        print triangle_list2
        #triangle_list=triangle_list+[triangle_list[0]]
        print
        print triangle_list2
        print
        print
        print
        print
        print
        print
        print
        print
        poly2=matlab_polygon_to_multipolygon_list(
            triangle_list2)
        print poly1.area
        print poly2.area
        
        print triangle_list
        assert allclose(poly1.area,poly2.area)
        
        
    def test_obsolete_matlab_polygon_to_geos_quick(self):
        
        points=[[0,0],[0,3],[3,3],[3,0],[0,0]]
        exclude=[[1,1],[1,2],[2,2],[1,1]]

        points=[tuple(point) for point in points]
        exclude=[tuple(point) for point in exclude]
        
        poly=polygon_to_geos_polygon(points)
        #print poly.is_valid
        answer=obsolete_matlab_polygon_to_geos(points+exclude)
        answer=obsolete_matlab_polygon_to_geos(points[:2]+exclude+points[1:])

        #print (answer.wkt)
        assert allclose(answer.area,8.5)
        
        
def same_polygon(geos_poly1,geos_poly2):
    if not allclose(geos_poly1.area,geos_poly2.area):
        return False
    if not allclose(geos_poly1.difference(geos_poly2).area,0.):
        return False
    return True
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Geos_Interface,'test')
    #suite = unittest.makeSuite(Test_Geos_Interface,'test_obsolete_points_to_linestring')
    runner = unittest.TextTestRunner()
    runner.run(suite)
