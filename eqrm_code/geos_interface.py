
from shapely.geometry import Polygon, LineString


def polygon_to_geos_polygon(polygon,exclude=None):
    """
    INPUT: List of polygon points (clockwise or anticlockwise).
    OUTPUT: geos polygon.

    The exclude argument is a bit fragile (numerical bug in geos).

    Implimentation:
    
    Use main_polygon = main_polygon.difference(exclusion) for all excludes.
    This is an inbuilt geos_polygon method, and may return TopologyException
    if the internal numerics get tempermental.

    (To be precise - TopologyException : side location conflict)
    
    TopologyException seems to indicate that "theoretically" parallel lines
    have been deemed non-parallel (by their roundoff), so the roundoff gets
    inverted  to calculate the intercept, returning a near-infinite number,
    which causes a crash. But that's just a guess.

    Sloped lines (ie triangles) seem to cause a crash, but not
    vertical / horizontal lines (ie the sort of squares you write for
    a unittest). Vertical
    
    /horizontal lines will not have different roundoffs, but two sloped lines
    may. This seems consistant with my guess.

    Hopefull a geos upgrade (I'm on geos-2.11) will fix this.
    """
    
    if exclude is None: exclude = []
    
    geos_polygon = _list_to_geos_poly(polygon)
    for exclusion in exclude:
        geos_exclusion=_list_to_geos_poly(exclusion)
        geos_polygon = geos_polygon.difference(geos_exclusion)
    return geos_polygon

def _list_to_geos_poly(polygon):
    geos_polygon = Polygon(polygon)
#    if geos_polygon.boundary.is_ring == False:
#        raise ValueError, 'Polygon is not a ring'
    return geos_polygon

##############################################################################
def geos_to_list(geos_poly):
    """
    Used
    """
    return wkt_to_multipolygon_list(geos_poly.wkt)
    #return list_multipolygon(geos_poly)

def list_multipolygon(geos):
    """
    Used in one test.  So not really used.
    
    I started to replace wkt_to_multipolygon_list, but decided I
    shouldn't.  list(geos) din't work well, when intelligently
    replacing wkt_to_multipolygon_list in the tests
    
    """
    
    try:
        polygon_list = list(geos)
    except TypeError:
        """
        This is too broad.  It catches;
        TypeError: 'Polygon' object is not iterable as well.
        """
        return [[]]
    return polygon_list

def wkt_to_multipolygon_list(wkt):
    """
    Used
    """
    if wkt[:8] == 'POLYGON ': return [__wkt_polygon_to_list(wkt[10:-2])]
    elif wkt[:13] == 'MULTIPOLYGON ':
        wkt_polygons = wkt[16:-3].split(')), ((')
        return map(__wkt_polygon_to_list,wkt_polygons)
        # Equivelent to
        # multipolygon_list = []
        # for wkt_polygon in wkt_polygons:
        #     multipolygon_list.append(__wkt_polygon_to_list(polygon))
        # return multipolygon_list
    elif wkt == 'GEOMETRYCOLLECTION EMPTY': return [[]]
    elif wkt[:11] == 'LINESTRING ': return [[]]
    elif wkt[:19] == 'GEOMETRYCOLLECTION ':
        multipolygon_list = []
        for sub_wkt in wkt[20:-2].split('), '):
            sub_wkt = sub_wkt+ ')' # since the ')' has been split off,
                                   # or truncated by wkt[20:-2]
            # sub_wkt should now look like a wkt_polygon, or a wkt_linestring 
            multipolygon_list.extend(wkt_to_multipolygon_list(sub_wkt))
        return multipolygon_list
    
    print 'Warning - poly may be wrong:'
    print wkt
    print 'Returned as [[]]'
    return [[]]
    

def __wkt_polygon_to_list(wkt_polygon):
    """
    Used
    """
    wkt_component_polygons = wkt_polygon.split('), (')
    return map(__wkt_component_polygon_to_list,wkt_component_polygons)

def __wkt_component_polygon_to_list(wkt_component_polygon):
    """
    Used
    """
    polygon_list = []
    for pair in wkt_component_polygon.split(', '):
        pair = pair.split(' ')
        pair = (float(pair[0]),float(pair[1]))
        polygon_list.append(pair)
    return polygon_list

def empty_geos():
    return LineString()


#############################################################################
#                        OBSOLETE      
#############################################################################
        
def obsolete_points_to_linestring(point_list):
    # DONT MOVE IMPORT.  OBSOLETE
    from shapely.wkt import loads
    wkt="LINESTRING ("
    for point in point_list:
        wkt+=(str(point[0])+' '+str(point[1])+', ')
    wkt = wkt[:-2] #chomp off the last ', '
    wkt+=')'
    linestring=loads(wkt)
    if not linestring.is_valid:
        raise ValueError,wkt+' was invalid'
    return linestring


def obsolete_matlab_polygon_to_geos(points):
    
    """
    This function is not used by anything else other than test_geos_interface

    The tests work.
    
    try:
        polygon=polygon_to_geos_polygon(points)
    except:
    """
    
    if True:
        #print 'to poly'
        #print points
        points_dict={}
        polygon=[]
        extra_polygons=[]
        i=0
        for point in points[:-1]:
            if not point in points_dict:
                points_dict[point]=i
                polygon.append(point)
                i+=1
            else:
                #print 'clipping at ',point
                j=points_dict.pop(point)
                if i>j+1:
                    extra_polygon=polygon[j:i+1]+[point]
                    # clip off the new polygon
                    # note, the new polygon is gets the endpoint added
                    # on again
                    if len(extra_polygon)==3:
                        assert extra_polygon[0]==extra_polygon[2]
                    else:
                        extra_polygon=obsolete_matlab_polygon_to_geos( \
                            extra_polygon)
                        extra_polygons.append(extra_polygon)
                    i=j 
                    polygon=polygon[:j]
                else:
                    # this is a degenerate poly
                    i=j+1
                    polygon=polygon[:j+1]
                       
        polygon=polygon+[polygon[0]]
        #print 'making geos'
        #print polygon
        polygon=polygon_to_geos_polygon(polygon)
        
        for extra_polygon in extra_polygons:
            polygon=polygon.symmetric_difference(extra_polygon)
            
        if not polygon.is_valid:
            raise ValueError,polygon.wkt+' was invalid'    
    return polygon
                         
def obsolete_linestring_to_points(linestring):
    wkt=linestring.wkt[12:][:-1]
    point_list = []
    for pair in wkt.split(', '):
        pair = pair.split(' ')
        pair = (float(pair[0]),float(pair[1]))
        point_list.append(pair)
    return point_list


def obsolete_multipolygon_list_to_geos_polygon(multipolygon_list):
    """
    Input:
    [poly1,poly2...]
    poly1 = [[points ...][exclude_points ...] [more exclude_points ...] ...]

    Output:
    geos_polygon (or multipolygon)
    """
    if len(multipolygon_list[0])==0: return _empty_geos()
    
    main_geos_poly=polygon_to_geos_polygon(\
        multipolygon_list[0][0],multipolygon_list[0][1:])
    
    for extra_poly in multipolygon_list[1:]:
        extra_geos_poly=polygon_to_geos_polygon(\
            extra_poly[0],extra_poly[1:])
        # take the union:
        #     No union implimented - combine difference
        #     and symmetric_difference 
        #     to getunion:
        #         A OR B = (A-B) XOR (B)
        main_geos_poly=main_geos_poly.difference(extra_geos_poly)
        main_geos_poly=main_geos_poly.symmetric_difference(extra_geos_poly)
    return main_geos_poly
    
