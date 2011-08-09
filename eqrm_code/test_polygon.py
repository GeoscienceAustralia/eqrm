#!/usr/bin/env python
import os
import sys
#sys.path.append(os.getcwd()+os.sep+os.pardir+os.sep+'eqrm_code')


import unittest
from scipy import zeros, array, allclose
from math import sqrt, pi
from numerical_tools import ensure_numeric
from eqrm_code.conversions import calc_ll_dist
from eqrm_code.polygon import *

from eqrm_code.polygon import point_on_line

def test_function(x, y):
    return x+y

class Test_Polygon(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def do_not_test_that_C_extension_compiles(self):
        # disabled. EQRM should not depend on numeric
        FN = 'polygon_ext.c'
        try:
            import polygon_ext
        except:
            from compile import compile

            try:
                compile(FN)
            except:
                raise 'Could not compile %s' %FN
            else:
                import polygon_ext


    def test_point_on_line(self):
        
	#Endpoints first
	assert point_on_line( 0, 0, 0,0, 1,0 )
	assert point_on_line( 1, 0, 0,0, 1,0 )

	#Then points on line
	assert point_on_line( 0.5, 0, 0,0, 1,0 )
	assert point_on_line( 0, 0.5, 0,1, 0,0 )
	assert point_on_line( 1, 0.5, 1,1, 1,0 )
	assert point_on_line( 0.5, 0.5, 0,0, 1,1 )

	#Then points not on line
	assert not point_on_line( 0.5, 0, 0,1, 1,1 )
	assert not point_on_line( 0, 0.5, 0,0, 1,1 )

	#From real example that failed
	assert not point_on_line( 40,50, 40,20, 40,40 )


	#From real example that failed
	assert not point_on_line( 40,19, 40,20, 40,40 )




    def test_is_inside_polygon_main(self):


        #Simplest case: Polygon is the unit square
        polygon = [[0,0], [1,0], [1,1], [0,1]]

	assert is_inside_polygon( (0.5, 0.5), polygon )
	assert not is_inside_polygon( (0.5, 1.5), polygon )
	assert not is_inside_polygon( (0.5, -0.5), polygon )
	assert not is_inside_polygon( (-0.5, 0.5), polygon )
	assert not is_inside_polygon( (1.5, 0.5), polygon )

	#Try point on borders
	assert is_inside_polygon( (1., 0.5), polygon, closed=True)
	assert is_inside_polygon( (0.5, 1), polygon, closed=True)
	assert is_inside_polygon( (0., 0.5), polygon, closed=True)
	assert is_inside_polygon( (0.5, 0.), polygon, closed=True)

	assert not is_inside_polygon( (0.5, 1), polygon, closed=False)
	assert not is_inside_polygon( (0., 0.5), polygon, closed=False)
	assert not is_inside_polygon( (0.5, 0.), polygon, closed=False)
	assert not is_inside_polygon( (1., 0.5), polygon, closed=False)


    def test_inside_polygon_main(self):

        #Simplest case: Polygon is the unit square
        polygon = [[0,0], [1,0], [1,1], [0,1]]        

        #From real example (that failed)
	polygon = [[20,20], [40,20], [40,40], [20,40]]
	points = [ [40, 50] ]
	res = inside_polygon(points, polygon)
	assert len(res) == 0

	polygon = [[20,20], [40,20], [40,40], [20,40]]
        points = [ [25, 25], [30, 20], [40, 50], [90, 20], [40, 90] ]
	res = inside_polygon(points, polygon)
	assert len(res) == 2
	assert allclose(res, [0,1])



	#More convoluted and non convex polygon
        polygon = [[0,0], [1,0], [0.5,-1], [2, -1], [2,1], [0,1]]
	assert is_inside_polygon( (0.5, 0.5), polygon )
	assert is_inside_polygon( (1, -0.5), polygon )
	assert is_inside_polygon( (1.5, 0), polygon )

	assert not is_inside_polygon( (0.5, 1.5), polygon )
	assert not is_inside_polygon( (0.5, -0.5), polygon )


	#Very convoluted polygon
        polygon = [[0,0], [10,10], [15,5], [20, 10], [25,0], [30,10], [40,-10]]
	assert is_inside_polygon( (5, 5), polygon )
	assert is_inside_polygon( (17, 7), polygon )
	assert is_inside_polygon( (27, 2), polygon )
	assert is_inside_polygon( (35, -5), polygon )
	assert not is_inside_polygon( (15, 7), polygon )
	assert not is_inside_polygon( (24, 3), polygon )
	assert not is_inside_polygon( (25, -10), polygon )



	#Another combination (that failed)
        polygon = [[0,0], [10,0], [10,10], [0,10]]
	assert is_inside_polygon( (5, 5), polygon )
	assert is_inside_polygon( (7, 7), polygon )
	assert not is_inside_polygon( (-17, 7), polygon )
	assert not is_inside_polygon( (7, 17), polygon )
	assert not is_inside_polygon( (17, 7), polygon )
	assert not is_inside_polygon( (27, 8), polygon )
	assert not is_inside_polygon( (35, -5), polygon )




	#Multiple polygons

        polygon = [[0,0], [1,0], [1,1], [0,1], [0,0],
		   [10,10], [11,10], [11,11], [10,11], [10,10]]
        assert is_inside_polygon( (0.5, 0.5), polygon )
        assert is_inside_polygon( (10.5, 10.5), polygon )

	#FIXME: Fails if point is 5.5, 5.5
        assert not is_inside_polygon( (0, 5.5), polygon )

	#Polygon with a hole
        polygon = [[-1,-1], [2,-1], [2,2], [-1,2], [-1,-1],
	           [0,0], [1,0], [1,1], [0,1], [0,0]]

        assert is_inside_polygon( (0, -0.5), polygon )
        assert not is_inside_polygon( (0.5, 0.5), polygon )



    def test_duplicate_points_being_ok(self):


        #Simplest case: Polygon is the unit square
        polygon = [[0,0], [1,0], [1,0], [1,0], [1,1], [0,1], [0,0]]

	assert is_inside_polygon( (0.5, 0.5), polygon )
	assert not is_inside_polygon( (0.5, 1.5), polygon )
	assert not is_inside_polygon( (0.5, -0.5), polygon )
	assert not is_inside_polygon( (-0.5, 0.5), polygon )
	assert not is_inside_polygon( (1.5, 0.5), polygon )

	#Try point on borders
	assert is_inside_polygon( (1., 0.5), polygon, closed=True)
	assert is_inside_polygon( (0.5, 1), polygon, closed=True)
	assert is_inside_polygon( (0., 0.5), polygon, closed=True)
	assert is_inside_polygon( (0.5, 0.), polygon, closed=True)

	assert not is_inside_polygon( (0.5, 1), polygon, closed=False)
	assert not is_inside_polygon( (0., 0.5), polygon, closed=False)
	assert not is_inside_polygon( (0.5, 0.), polygon, closed=False)
	assert not is_inside_polygon( (1., 0.5), polygon, closed=False)

        #From real example
	polygon = [[20,20], [40,20], [40,40], [20,40]]
	points = [ [40, 50] ]
	res = inside_polygon(points, polygon)
	assert len(res) == 0

        

    def test_inside_polygon_vector_version(self):
	#Now try the vector formulation returning indices
        polygon = [[0,0], [1,0], [0.5,-1], [2, -1], [2,1], [0,1]]
	points = [ [0.5, 0.5], [1, -0.5], [1.5, 0], [0.5, 1.5], [0.5, -0.5]]
	res = inside_polygon( points, polygon, verbose=False )

	assert allclose( res, [0,1,2] )

    def test_outside_polygon(self):
        U = [[0,0], [1,0], [1,1], [0,1]] #Unit square    

        assert not is_outside_polygon( [0.5, 0.5], U )
        #evaluate to False as the point 0.5, 0.5 is inside the unit square
        
        assert is_outside_polygon( [1.5, 0.5], U )
        #evaluate to True as the point 1.5, 0.5 is outside the unit square
        
        indices = outside_polygon( [[0.5, 0.5], [1, -0.5], [0.3, 0.2]], U )
        assert allclose( indices, [1] )
        
        #One more test of vector formulation returning indices
        polygon = [[0,0], [1,0], [0.5,-1], [2, -1], [2,1], [0,1]]
	points = [ [0.5, 0.5], [1, -0.5], [1.5, 0], [0.5, 1.5], [0.5, -0.5]]
	res = outside_polygon( points, polygon )

	assert allclose( res, [3, 4] )



        polygon = [[0,0], [1,0], [0.5,-1], [2, -1], [2,1], [0,1]]
	points = [ [0.5, 1.4], [0.5, 0.5], [1, -0.5], [1.5, 0], [0.5, 1.5], [0.5, -0.5]]
	res = outside_polygon( points, polygon )

	assert allclose( res, [0, 4, 5] )        
     
    def test_outside_polygon2(self):
        U = [[0,0], [1,0], [1,1], [0,1]] #Unit square    
   
        assert not outside_polygon( [0.5, 1.0], U, closed = True )
        #evaluate to False as the point 0.5, 1.0 is inside the unit square
        
        assert is_outside_polygon( [0.5, 1.0], U, closed = False )
        #evaluate to True as the point 0.5, 1.0 is outside the unit square

    def test_all_outside_polygon(self):
        """Test case where all points are outside poly
        """
        
        U = [[0,0], [1,0], [1,1], [0,1]] #Unit square    

        points = [[2,2], [1,3], [-1,1], [0,2]] #All outside


        indices, count = separate_points_by_polygon(points, U)
        #print indices, count
        assert count == 0 #None inside
        assert allclose(indices, [3,2,1,0])

        indices = outside_polygon(points, U, closed = True)
        assert allclose(indices, [0,1,2,3])

        indices = inside_polygon(points, U, closed = True)
        assert allclose(indices, [])                


    def test_all_inside_polygon(self):
        """Test case where all points are inside poly
        """
        
        U = [[0,0], [1,0], [1,1], [0,1]] #Unit square    

        points = [[0.5,0.5], [0.2,0.3], [0,0.5]] #All inside (or on edge)


        indices, count = separate_points_by_polygon(points, U)
        assert count == 3 #All inside
        assert allclose(indices, [0,1,2])

        indices = outside_polygon(points, U, closed = True)
        assert allclose(indices, [])

        indices = inside_polygon(points, U, closed = True)
        assert allclose(indices, [0,1,2])
        

    def test_separate_points_by_polygon(self):
        U = [[0,0], [1,0], [1,1], [0,1]] #Unit square    

        indices, count = separate_points_by_polygon( [[0.5, 0.5], [1, -0.5], [0.3, 0.2]], U )
        assert allclose( indices, [0,2,1] )
        assert count == 2
        
        #One more test of vector formulation returning indices
        polygon = [[0,0], [1,0], [0.5,-1], [2, -1], [2,1], [0,1]]
	points = [ [0.5, 0.5], [1, -0.5], [1.5, 0], [0.5, 1.5], [0.5, -0.5]]
	res, count = separate_points_by_polygon( points, polygon )

	assert allclose( res, [0,1,2,4,3] )
	assert count == 3


        polygon = [[0,0], [1,0], [0.5,-1], [2, -1], [2,1], [0,1]]
	points = [ [0.5, 1.4], [0.5, 0.5], [1, -0.5], [1.5, 0], [0.5, 1.5], [0.5, -0.5]]
	res, count = separate_points_by_polygon( points, polygon )

	assert allclose( res, [1,2,3,5,4,0] )        
     	assert count == 3
	
    def test_populate_geo_coord_polygon(self):
        # Checks that the Y distance between points gets larger as the latitude 
        # gets larger.
        randoms=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
        polygon = [[0,0], [50,0], [50,0.5], [0,0.5]]
        points = populate_geo_coord_polygon(polygon, 9, None, None,randoms)
        prevDiff =0.0
        for i in xrange(len(points)-1):
            if i <> 0:
                assert (points[i][0] -points[i-1][0])> prevDiff
                prevDiff = points[i][0] -points[i-1][0]
        assert len(points) == 9
        for point in points:
            assert is_inside_polygon(point, polygon)

        # Checks that the distance between points changes in proportion to the
        # the change in width of the polygon due to the curvature of the earth.
        randoms = [0.09, 0.1, 0.89, 0.9]
        points = populate_geo_coord_polygon(polygon, 4, None, None,randoms)
        
        midA_lat = abs(points[1][0]-points[0][0]) + points[0][0]
        length_X_A= calc_ll_dist(midA_lat, 0.0, midA_lat, 0.5)
        length_Y_A= calc_ll_dist(points[1][0], 0.25, points[0][0], 0.25)
        
        midB_lat = abs(points[3][0]-points[2][0]) + points[2][0]
        length_X_B= calc_ll_dist(midB_lat, 0.0, midB_lat, 0.5)
        length_Y_B= calc_ll_dist(points[3][0], 0.25, points[2][0], 0.25)
        
        ratioX = length_X_A/length_X_B
        ratioY = length_Y_B/length_Y_A
        
        assert abs(ratioX - ratioY) < 0.01
        
    #Very convoluted polygon
        polygon = [[0,0], [10,10], [15,5], [20, 10], [25,0], [30,10], [40,-10]]

        points = populate_geo_coord_polygon(polygon, 5)

        assert len(points) == 5
        for point in points:
            assert is_inside_polygon(point, polygon)
    def test_populate_geo_coord_polygon_with_exclude(self):
        

        polygon = [[0,0], [1,0], [1,1], [0,1]]
        ex_poly = [[0,0], [0.5,0], [0.5, 0.5], [0,0.5]] #SW quarter
        points = populate_geo_coord_polygon(polygon, 5, exclude = [ex_poly])

        assert len(points) == 5
        for point in points:
            assert is_inside_polygon(point, polygon)
            assert not is_inside_polygon(point, ex_poly)            


        #overlap
        polygon = [[0,0], [1,0], [1,1], [0,1]]
        ex_poly = [[-1,-1], [0.5,0], [0.5, 0.5], [-1,0.5]]
        points = populate_geo_coord_polygon(polygon, 5, exclude = [ex_poly])

        assert len(points) == 5
        for point in points:
            assert is_inside_polygon(point, polygon)
            assert not is_inside_polygon(point, ex_poly)
        
        #Multiple
        polygon = [[0,0], [1,0], [1,1], [0,1]]
        ex_poly1 = [[0,0], [0.5,0], [0.5, 0.5], [0,0.5]] #SW quarter
        ex_poly2 = [[0.5,0.5], [0.5,1], [1, 1], [1,0.5]] #NE quarter        
        
        points = populate_geo_coord_polygon(polygon, 20, 
        exclude = [ex_poly1, ex_poly2])

        assert len(points) == 20
        for point in points:
            assert is_inside_polygon(point, polygon)
            assert not is_inside_polygon(point, ex_poly1)
            assert not is_inside_polygon(point, ex_poly2)
        

    #Very convoluted polygon
        polygon = [[0,0], [10,10], [15,5], [20, 10], [25,0], [30,10], 
                   [40,-10]]
        ex_poly = [[-1,-1], [5,0], [5, 5], [-1,5]]
        points = populate_geo_coord_polygon(polygon, 20, exclude = [ex_poly])
        
        assert len(points) == 20
        for point in points:
            assert is_inside_polygon(point, polygon)
            assert not is_inside_polygon(point, ex_poly), '%s' %str(point)


    def non_deterministic_test_populate_geo_coord_polygon(self):
#Check that proportion of points in an area is roughly what it should be
#given the latitude of the area
        polygon = [[0,0], [-50,0], [-50,10], [0,10]]
        points = populate_geo_coord_polygon(polygon, 100000)
        polygonA = [[0,0], [-2,0], [-2,10], [0,10]]
        polygonB = [[-48,0], [-50,0], [-50,10], [-48,10]]
        countA = 0.0
        countB = 0.0
        for point in points:
            if is_inside_polygon(point, polygonA):
                countA+=1
            elif is_inside_polygon(point, polygonB):
                countB+=1
        pointsRatio = countA/countB
        lengthA= calc_ll_dist(-1.0, 0.0, -1.0, 10.0)
        lengthB= calc_ll_dist(-49.0, 0.0, -49.0, 10.0)
        areaRatio= lengthA/lengthB
        
        assert abs(pointsRatio - areaRatio) < 0.2

    def test_populate_polygon(self):

        polygon = [[0,0], [1,0], [1,1], [0,1]]
        points = populate_polygon(polygon, 5)

        assert len(points) == 5
        for point in points:
            assert is_inside_polygon(point, polygon)


	#Very convoluted polygon
        polygon = [[0,0], [10,10], [15,5], [20, 10], [25,0], [30,10], [40,-10]]

        points = populate_polygon(polygon, 5)

        assert len(points) == 5
        for point in points:
            assert is_inside_polygon(point, polygon)


    def test_populate_polygon_with_exclude(self):
        

        polygon = [[0,0], [1,0], [1,1], [0,1]]
        ex_poly = [[0,0], [0.5,0], [0.5, 0.5], [0,0.5]] #SW quarter
        points = populate_polygon(polygon, 5, exclude = [ex_poly])

        assert len(points) == 5
        for point in points:
            assert is_inside_polygon(point, polygon)
            assert not is_inside_polygon(point, ex_poly)            


        #overlap
        polygon = [[0,0], [1,0], [1,1], [0,1]]
        ex_poly = [[-1,-1], [0.5,0], [0.5, 0.5], [-1,0.5]]
        points = populate_polygon(polygon, 5, exclude = [ex_poly])

        assert len(points) == 5
        for point in points:
            assert is_inside_polygon(point, polygon)
            assert not is_inside_polygon(point, ex_poly)                        
        
        #Multiple
        polygon = [[0,0], [1,0], [1,1], [0,1]]
        ex_poly1 = [[0,0], [0.5,0], [0.5, 0.5], [0,0.5]] #SW quarter
        ex_poly2 = [[0.5,0.5], [0.5,1], [1, 1], [1,0.5]] #NE quarter        
        
        points = populate_polygon(polygon, 20, exclude = [ex_poly1, ex_poly2])

        assert len(points) == 20
        for point in points:
            assert is_inside_polygon(point, polygon)
            assert not is_inside_polygon(point, ex_poly1)
            assert not is_inside_polygon(point, ex_poly2)                                
        

	#Very convoluted polygon
        polygon = [[0,0], [10,10], [15,5], [20, 10], [25,0], [30,10], [40,-10]]
        ex_poly = [[-1,-1], [5,0], [5, 5], [-1,5]]
        points = populate_polygon(polygon, 20, exclude = [ex_poly])
        
        assert len(points) == 20
        for point in points:
            assert is_inside_polygon(point, polygon)
            assert not is_inside_polygon(point, ex_poly), '%s' %str(point)                        


    def test_populate_polygon_with_exclude2(self):
        

        min_outer = 0 
        max_outer = 1000
        polygon_outer = [[min_outer,min_outer],[max_outer,min_outer],
                   [max_outer,max_outer],[min_outer,max_outer]]

        delta = 10
        min_inner1 = min_outer + delta
        max_inner1 = max_outer - delta
        inner1_polygon = [[min_inner1,min_inner1],[max_inner1,min_inner1],
                   [max_inner1,max_inner1],[min_inner1,max_inner1]]
      
        
        density_inner2 = 1000 
        min_inner2 = min_outer +  2*delta
        max_inner2 = max_outer -  2*delta
        inner2_polygon = [[min_inner2,min_inner2],[max_inner2,min_inner2],
                   [max_inner2,max_inner2],[min_inner2,max_inner2]]      
        
        points = populate_polygon(polygon_outer, 20, exclude = [inner1_polygon, inner2_polygon])

        assert len(points) == 20
        for point in points:
            assert is_inside_polygon(point, polygon_outer)
            assert not is_inside_polygon(point, inner1_polygon)
            assert not is_inside_polygon(point, inner2_polygon)                                
        

	#Very convoluted polygon
        polygon = [[0,0], [10,10], [15,5], [20, 10], [25,0], [30,10], [40,-10]]
        ex_poly = [[-1,-1], [5,0], [5, 5], [-1,5]]
        points = populate_polygon(polygon, 20, exclude = [ex_poly])
        
        assert len(points) == 20
        for point in points:
            assert is_inside_polygon(point, polygon)
            assert not is_inside_polygon(point, ex_poly), '%s' %str(point)                        

    def test_point_in_polygon(self):
        polygon = [[0,0], [1,0], [1,1], [0,1]]
        point = point_in_polygon(polygon)
        assert is_inside_polygon(point, polygon)

        #this may get into a vicious loop
        #polygon = [[1e32,1e54], [1,0], [1,1], [0,1]]
        
        polygon = [[1e15,1e7], [1,0], [1,1], [0,1]]
        point = point_in_polygon(polygon)
        assert is_inside_polygon(point, polygon)


        polygon = [[0,0], [1,0], [1,1], [1e8,1e8]]
        point = point_in_polygon(polygon)
        assert is_inside_polygon(point, polygon)

        
        polygon = [[1e32,1e54], [-1e32,1e54], [1e32,-1e54]]
        point = point_in_polygon(polygon)
        assert is_inside_polygon(point, polygon)

        
        polygon = [[1e18,1e15], [1,0], [0,1]]
        point = point_in_polygon(polygon)
        assert is_inside_polygon(point, polygon)

    def test_in_and_outside_polygon_main(self):


        #Simplest case: Polygon is the unit square
        polygon = [[0,0], [1,0], [1,1], [0,1]]

	inside, outside =  in_and_outside_polygon( (0.5, 0.5), polygon )
	assert inside[0] == 0
	assert len(outside) == 0
        
        inside, outside =  in_and_outside_polygon(  (1., 0.5), polygon, closed=True)
	assert inside[0] == 0
	assert len(outside) == 0
        
        inside, outside =  in_and_outside_polygon(  (1., 0.5), polygon, closed=False)
	assert len(inside) == 0
	assert outside[0] == 0

        points =  [(1., 0.25),(1., 0.75) ]
        inside, outside =  in_and_outside_polygon( points, polygon, closed=True)
	
	assert (allclose(array(inside), array([0,1])))
	assert len(outside) == 0
        
        inside, outside =  in_and_outside_polygon( points, polygon, closed=False)
	assert len(inside) == 0
	assert (allclose(array(outside), array([0,1])))

       
        points =  [(100., 0.25),(0.5, 0.5) ] 
        inside, outside =  in_and_outside_polygon( points, polygon)
	assert (allclose(array(inside), array([1])))
	assert outside[0] == 0
        
        points =  [(100., 0.25),(0.5, 0.5), (39,20), (0.6,0.7),(56,43),(67,90) ] 
        inside, outside =  in_and_outside_polygon( points, polygon)
	assert (allclose(array(inside), array([1,3])))
	assert (allclose(array(outside), array([0,2,4,5])))
        
    def zzztest_inside_polygon_main(self):  
        print "inside",inside
        print "outside",outside
        
	assert not inside_polygon( (0.5, 1.5), polygon )
	assert not inside_polygon( (0.5, -0.5), polygon )
	assert not inside_polygon( (-0.5, 0.5), polygon )
	assert not inside_polygon( (1.5, 0.5), polygon )

	#Try point on borders
	assert inside_polygon( (1., 0.5), polygon, closed=True)
	assert inside_polygon( (0.5, 1), polygon, closed=True)
	assert inside_polygon( (0., 0.5), polygon, closed=True)
	assert inside_polygon( (0.5, 0.), polygon, closed=True)

	assert not inside_polygon( (0.5, 1), polygon, closed=False)
	assert not inside_polygon( (0., 0.5), polygon, closed=False)
	assert not inside_polygon( (0.5, 0.), polygon, closed=False)
	assert not inside_polygon( (1., 0.5), polygon, closed=False)



        #From real example (that failed)
	polygon = [[20,20], [40,20], [40,40], [20,40]]
	points = [ [40, 50] ]
	res = inside_polygon(points, polygon)
	assert len(res) == 0

	polygon = [[20,20], [40,20], [40,40], [20,40]]
        points = [ [25, 25], [30, 20], [40, 50], [90, 20], [40, 90] ]
	res = inside_polygon(points, polygon)
	assert len(res) == 2
	assert allclose(res, [0,1])

    def test_polygon_area(self):

        #Simplest case: Polygon is the unit square
        polygon = [[0,0], [1,0], [1,1], [0,1]]
	assert polygon_area(polygon) == 1

	#Simple case: Polygon is a rectangle
        polygon = [[0,0], [1,0], [1,4], [0,4]]
	assert polygon_area(polygon) == 4

	#Simple case: Polygon is a unit triangle
        polygon = [[0,0], [1,0], [0,1]]
	assert polygon_area(polygon) == 0.5

	#Simple case: Polygon is a diamond
        polygon = [[0,0], [1,1], [2,0], [1, -1]]
	assert polygon_area(polygon) == 2.0

    def test_poly_xy(self):
 
        #Simplest case: Polygon is the unit square
        polygon = [[0,0], [1,0], [1,1], [0,1]]
        x, y = poly_xy(polygon)
	assert len(x) == len(polygon)+1
	assert len(y) == len(polygon)+1
	assert x[0] == 0
	assert x[1] == 1
	assert x[2] == 1
	assert x[3] == 0
	assert y[0] == 0
	assert y[1] == 0
	assert y[2] == 1
	assert y[3] == 1

	#Arbitrary polygon
        polygon = [[1,5], [1,1], [100,10], [1,10], [3,6]]
        x, y = poly_xy(polygon)
	assert len(x) == len(polygon)+1
	assert len(y) == len(polygon)+1
	assert x[0] == 1
	assert x[1] == 1
	assert x[2] == 100
	assert x[3] == 1
	assert x[4] == 3
	assert y[0] == 5
	assert y[1] == 1
	assert y[2] == 10
	assert y[3] == 10
	assert y[4] == 6

    # Disabled    
    def xtest_plot_polygons(self):
        
        import os
        
        #Simplest case: Polygon is the unit square
        polygon1 = [[0,0], [1,0], [1,1], [0,1]]
        polygon2 = [[1,1], [2,1], [3,2], [2,2]]
        v = plot_polygons([polygon1, polygon2],'test1')
	assert len(v) == 4
	assert v[0] == 0
	assert v[1] == 3
	assert v[2] == 0
	assert v[3] == 2

	#Another case
        polygon3 = [[1,5], [10,1], [100,10], [50,10], [3,6]]
        v = plot_polygons([polygon2,polygon3],'test2')
	assert len(v) == 4
	assert v[0] == 1
	assert v[1] == 100
	assert v[2] == 1
	assert v[3] == 10

	os.remove('test1.png')
	os.remove('test2.png')

	
        
#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Polygon,'test')
    #suite = unittest.makeSuite(Test_Polygon,'test_inside_polygon_geo_ref')
    runner = unittest.TextTestRunner()
    runner.run(suite)




