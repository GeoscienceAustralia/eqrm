

# FIXME - make a class 'polygon' <- 'complex_polygon' <-
# '_intersection_polygon'
import copy

from shapely.geometry import Point

from eqrm_code.geos_interface import polygon_to_geos_polygon \
    , empty_geos, geos_to_list
from eqrm_code.polygon import is_inside_polygon


class polygon_object(object):

    """

    Polygon terminology for eqrm
    ----------------------------

    Valid polygon: a polygon that does not self-intersect.

    Simple polygon: a polygon that is Valid, and does not have exclusions.

    Multi-polygon: a collection of valid polygons. These polygons should not
                   touch (except at vertexes).

    Valid, Simple and Multi-polygons are all used by geos.

    Simple polygons and simple exclusions are the ONLY things that can be
    sent to polygon_object from the outside.

    All these simple polygons may form a polygon that is not simple, but
    that is dealt with inside the geos interface.

    polygon_object may internally use Valid, Simple or Multi-polygons
    (through geos_interface), but this will only be seen by the user if
    they use polygon_object.to_list().

    Complex polygon: a polygon that may self-intersect.
                     a complex polygon cannot be used by geos_interface.

      note: I have not stated whether a complex polygon can have exclusions
            because it is sometimes a little ambiguous in the code.
    But ideally speaking, a complex polygon should NOT have excludes.

    In the case of complex polygons without excludes (or simple polygons),
    concatenation (ie poly = poly1[:-1] + poly2[:] + poly1[-1]) performs an
    xor operation (symmetric difference).

    Therefore, a Valid multipolygon may be transformed into an equivalent
    polygon by concatenating all its components. There is no need to treat
    exludes and includes seperately. The xor will treat includes as unions
    and excludes as differences, since in Valid multipolygons there are no
    overlaps between includes (so the xor will be +) and all excludes
    completely overlap with an include (so the xor will be -).

    ------------------------------------------------------------------------

    Parameters
    ----------
    linestring : main polygon - a list of tuples representing a polygon?
                 The start and end points are the same.

    exclude : polygons that are excluded from the main polygon

    Both linestring and exlude must be Simple polygons.
    They must be a sequence of points.
    The first point must be repeated as the last point.

    area : geodesic area of the polygon (different to the flat-earth area)

    Attributes:
      geos_polygon : polygon as a geos object (dealt with through
        geos_interface)
      area: property (see methods: set_area and get_area)

    Private attributes:
      _precomputed_points : precomputed contains_point points
      _linestring : the main polygon boundary, used by contains_point and
        __str__
      _exclude : exclusion zones, used by contains_point and __str__
      _area : used by the polygon_object property area

    Methods
    -------
    intersection(polygon = polygon_object (or subclass)):
        Returns a polygon representing the intersection between
        self and polygon.

    difference(polygon = polygon_object (or subclass)):
        Returns a polygon representing the intersection between
        self and polygon.

    union(polygon = polygon_object (or subclass)):
        Returns a polygon representing the intersection between
        self and polygon.

    The polygon return by the above methods will be self, polygon,
    empty_polygon, or a compound polygon.

    contains_point(point=sequence):
        Return True if polygon contains point, otherwise return False.
        Caches answer in self._precomputed_points.

     __contains_point(self,point):
        Interface to polygon.is_inside_polygon.

    scale_area(polygon = polygon):
        Scales self.area by polygon.area/polygon.get_polygon_area().

    get_polygon_area():
        Returns the cartesian area of the polygon.

    set_area(area): Set self._area to area.

    get_area():
        note: self._area = self.area

        if self._area is set, return self._area
        if self._area is not set, return self.get_polygon_area() and set
        self._area to self.get_polygon_area().

    stratified(polygons):
        Intersects the source polygons with the independent polygons.

    to_multipolygon_list():
        Interrogate geos_interface to return a list of:

        [Valid_polygon, Valid_polygon, ...]
        where Valid_polygon = [Simple_polygon,Simple_exclude,...]
        where Simple_polygon = [point,point,...]

    to_list():
        I should really modify it so it can return:
            Complex_polygon
            where Complex_polygon = [point,point,point ...]

            This is done by concatenating (joining) everything in multi_polygon
           (nearly done by to_list).
    """

    def __init__(self, linestring, exclude=None, area=None):
        """
        linestring : main polygon
        exclude : polygons that are excluded from the main polygon

        Both linestring and exlude must be Simple polygons.
        They must be a sequence of points.
        The first point must be repeated as the last point.

        area : geodesic area of the polygon (different to the flat-earth area)
        """
        # print "linestring", linestring
        linestring = [tuple(line) for line in linestring]
        # print "linestring", linestring
        if exclude is None:
            exclude = []
        exclude = [[tuple(line) for line in ex] for ex in exclude]

        self._linestring = linestring
        self._exclude = exclude

        self.geos_polygon = polygon_to_geos_polygon(linestring)
        if not self.geos_polygon.is_valid:
            raise InvalidPolygonError(linestring)

        # These do not work
        #self.outline_geos_polygon =  copy.deepcopy(self.geos_polygon)
        self.outline_geos_polygon = polygon_to_geos_polygon(linestring)
        #self.outline_geos_polygon = None

        for exclusion_zone in exclude:
            exclude_polygon = polygon_to_geos_polygon(exclusion_zone)
            # Checking valid exclude
            if not exclude_polygon.is_valid:
                raise InvalidPolygonError(exclusion_zone)
            # Main = Main - exclude
            self.geos_polygon = self.geos_polygon.difference(exclude_polygon)

        self._precomputed_points = {}
        self._area = area

    def contains_point(self, point, use_cach=True):
        """
        Return True if polygon contains point, otherwise return False.
        Caches answer in self._precomputed_points.
        """

        if not isinstance(point, tuple):
            point = tuple(point)
            # making sure point is a tuple
        if use_cach is True:
            try:
                answer = self._precomputed_points[point]
            except KeyError:
                # geo=self.__contains_point_geo(point)
                answer = self.__contains_point(point)
                self._precomputed_points[point] = answer
                # if not self._precomputed_points[point] == geo:
                # print "****** geo and inhouse contains point different****"
        else:
            answer = self.__contains_point(point)
        return answer

    def __contains_point(self, point):
        """
        Interface to polygon.is_inside_polygon.
        """
        if not is_inside_polygon(point, self._linestring[:-1]):
            # is_inside_polygon uses polygon[:-1] - the first/last point
            # is NOT repeated. Unless you want to spend an hour debugging ;)
            return False
        for exclusion_zone in self._exclude:
            if is_inside_polygon(point, exclusion_zone[:-1]):
                # print "exclusion zone False"
                return False
        return True

    def __contains_point_geo(self, point):
        """
        DO NOT USE
        Interface to using the shapely polygon.contains.
        Gives different results to polygon is_inside_polygon.
        What's more it seems to be wrong.

        And it is not very deterministic.

        Sometimes it is right, sometimes it's wrong, with seemingly the same
        data.

        """

        # This gives the wrong answer, and it is slow.
        poly = polygon_to_geos_polygon(self._linestring)
        if not poly.contains(Point(point)):
            return False

        for exclusion_zone in self._exclude:
            exclude_polygon = polygon_to_geos_polygon(exclusion_zone)
            if exclude_polygon.contains(Point(point)):
                return False
        return True

    def __contains_point_geo_bad(self, point):
        """
        DO NOT USE
        Interface to using the shapely polygon.contains.
        Gives different results to polygon is_inside_polygon.
        What's more it seems to be wrong.

        Alot of code in this function that is going down the wrong track.
        """

        #f = self.y
        if True:
            # This gives the wrong answer, and it is slow.
            poly = polygon_to_geos_polygon(self._linestring)
            if not poly.contains(Point(point)):
                return False
        else:
            outline = not self.outline_geos_polygon.contains(Point(point))
            poly = polygon_to_geos_polygon(self._linestring)
            brute = not poly.contains(Point(point))
            if not outline == brute:
                # This doesn't happen
                print "(self._linestring", self._linestring
                print "self.outline_geos_polygon", self.outline_geos_polygon
                import sys
                sys.exit()

            if outline:
                return False
        if False:
            # This doesn't work
            try:
                if not self.outline_geos_polygon.contains(Point(point)):
                    return False
            except:
                self.outline_geos_polygon = polygon_to_geos_polygon(
                    self._linestring)
                outline = not self.outline_geos_polygon.contains(Point(point))
                poly = polygon_to_geos_polygon(self._linestring)
                if not self.outline_geos_polygon.contains(Point(point)):
                    return False
        for exclusion_zone in self._exclude:

            exclude_polygon = polygon_to_geos_polygon(exclusion_zone)
            if exclude_polygon.contains(Point(point)):
                return False
        return True

    def get_polygon_area(self):
        """Returns the cartesian area of the polygon."""
        return self.geos_polygon.area

    def get_area(self):
        """
        note: self._area = self.area

        if self._area is set, return self._area
        if self._area is not set, return self.get_polygon_area() and set
        self._area to self.get_polygon_area().
        """
        if self._area is not None:
            return self._area
        self._area = self.geos_polygon.area
        return self._area

    def set_area(self, area):
        """Set self._area to area."""
        self._area = area

    def intersection(self, polygon2):
        """
        Returns a polygon representing the intersection between
        self and polygon.
        """
        intersection = polygon_intersection(self, polygon2)
        intersection.scale_area(self)
        if intersection.area == 0:
            return empty_polygon
        if intersection.area == self.area:
            return self
        return intersection

    def difference(self, polygon2):
        """
        Returns a polygon representing the difference between
        self and polygon.
        """
        difference = polygon_difference(self, polygon2)
        difference.scale_area(self)
        if difference.area == 0:
            return empty_polygon
        if difference.area == self.area:
            return self
        return difference

    def union(self, polygon2):
        """
        Returns a polygon representing the union between
        self and polygon.
        """
        union = polygon_union(self, polygon2)
        union.scale_area(self)
        if union.area == self.area:
            return self
        return union

    def scale_area(self, polygon):
        """Scales self.area by polygon.area/polygon.get_polygon_area()."""
        scaling_factor = polygon.area / polygon.get_polygon_area()
        self.area = self.get_polygon_area() * scaling_factor

    def stratified(self, polygons):
        """
        Returns the intersection of self with the input polygons,
        scaled by area of self.
        """
        stratified_polygons = []
        for polygon in polygons:
            stratified_polygon = self.intersection(polygon)
            if stratified_polygon.area > 0:
                stratified_polygons.append(stratified_polygon)
        return stratified_polygons

    def to_multipolygon_list(self):
        """
        Interrogate geos_interface to return a list of:

        [Valid_polygon, Valid_polygon, ...]
        where Valid_polygon = [Simple_polygon,Simple_exclude,...]
        where Simple_polygon = [point,point,...]
        """
        return geos_to_list(self.geos_polygon)

    def to_list(self):  # FIXME - more to do
        multi_polygon_list = geos_to_list(self.geos_polygon)
        answer = []
        for poly in multi_polygon_list:
            answer.extend(poly)
        return answer

    def __str__(self):
        """Polygon is represented by its rounded coordinates"""
        string = self.__simple_str(self._linestring)
        for exclusion_zone in self._exclude:
            string += '\n  NOT\n'
            string += '  ' + self.__simple_str(exclusion_zone)

        return string

    def __repr__(self):
        return str(self)

    def __simple_str(self, linestring):
        return '[' +\
               ','.join(['(%g,%g)' % pair for pair in linestring])\
               + ']'

    area = property(get_area, set_area)
    polygon_area = property(get_polygon_area)
###############################################################################


def polygon_with_excludes(linestring, excludes=None, area=None):
    if excludes is None:
        excludes = []
    main = polygon_object(linestring)
    for exclude in excludes:
        main = main.difference(polygon_object(exclude))
    main.area = area
    return main
###############################################################################


class compound_polygon(polygon_object):

    """
    Abstract class.

    """

    def __init__(self, polygon1, polygon2):
        self.polygon1 = polygon1
        self.polygon2 = polygon2
        self._area = None

    def __str__(self):
        p1str = str(self.polygon1)
        p1str = indent_string(p1str)
        p2str = str(self.polygon2)
        p2str = indent_string(p2str)
        sep = self.sep
        sep = indent_string(self.sep)
        return ''.join(['Compound Polygon:\n', p1str, sep, p2str])
###############################################################################


class polygon_intersection(compound_polygon):

    def __init__(self, polygon1, polygon2):
        compound_polygon.__init__(self, polygon1, polygon2)
        self.sep = 'AND'

        geos_polygon1 = polygon1.geos_polygon
        geos_polygon2 = polygon2.geos_polygon
        try:
            self.geos_polygon = geos_polygon1.intersection(geos_polygon2)
        except ValueError:
            # No shape could be created.
            self.geos_polygon = empty_polygon
        # Geos *may* crash here from numerical bugs (in geos).
        # Try to slightly perturb the polygon if this happens (or
        # upgrade geos).

    def contains_point(self, point):
        """
        Return True if polygon contains point, otherwise return False.
        """
        if not self.polygon1.contains_point(point):
            return False
        if not self.polygon2.contains_point(point):
            return False
        return True
###############################################################################


class polygon_difference(compound_polygon):

    def __init__(self, polygon1, polygon2):
        compound_polygon.__init__(self, polygon1, polygon2)
        self.sep = 'NOT'

        geos_polygon1 = polygon1.geos_polygon
        geos_polygon2 = polygon2.geos_polygon

        self.geos_polygon = geos_polygon1.difference(geos_polygon2)
        # Geos *may* crash here from numerical bugs (in geos).
        # Try to slightly perturb the polygon if this happens (or
        # upgrade geos).

    def contains_point(self, point):
        """
        Return True if polygon contains point, otherwise return False.
        """
        if not self.polygon1.contains_point(point):
            return False
        if self.polygon2.contains_point(point):
            return False
        return True
###############################################################################


class polygon_union(compound_polygon):

    def __init__(self, polygon1, polygon2):
        compound_polygon.__init__(self, polygon1, polygon2)
        self.sep = 'OR'

        geos_polygon1 = polygon1.geos_polygon
        geos_polygon2 = polygon2.geos_polygon

        # geos_polygon.union() does not appear to exist. Damm
        # use difference + symDifference for equivalent behaviour
        self.geos_polygon = geos_polygon1.difference(geos_polygon2)
        self.geos_polygon = self.geos_polygon.symDifference(geos_polygon2)
        # Geos *may* crash here from numerical bugs (in geos).
        # Try to slightly perturb the polygon if this happens (or
        # upgrade geos).

    def contains_point(self, point):
        """
        Return True if polygon contains point, otherwise return False.
        """
        if self.polygon1.contains_point(point):
            return True
        if self.polygon2.contains_point(point):
            return True
        return False
###############################################################################


class Empty_polygon(polygon_object):

    def __init__(self):
        self.area = 0.
        self.geos_polygon = empty_geos()

    def contains_point(point):
        """
        Return True if polygon contains point, otherwise return False.
        """
        return False

    def intersection(self, polygon2):
        """
        Returns a polygon representing the intersection between
        self and polygon.
        """
        return self

    def difference(self, polygon2):
        """
        Returns a polygon representing the difference between
        self and polygon.
        """
        return self

    def union(self,):
        """
        Returns a polygon representing the union between
        self and polygon.
        """
        return None

    def area(self,):
        """
        empty polygon has no area.
        """
        return 0

    def __str__(self):
        return 'Empty polygon'
###############################################################################


class InvalidPolygonError(Exception):

    def __init__(self, linestring):
        self.linestring = linestring

    def __str__(self):
        msg = 'Polygon not valid. Polygon = '
        msg = msg + str(self.linestring)
        return msg
###############################################################################


def indent_string(string, n=4):
    """
    Indent all the lines in a string.
    """
    string_list = string.split('\n')
    ind = ' ' * n
    string_list = [ind + string + '\n' for string in string_list]
    blank_string = ''
    return blank_string.join(string_list)
###############################################################################
empty_polygon = Empty_polygon()
###############################################################################


def get_independent_polygons_obsolete(polygon_objects):
    """
    Returns a list of independent polygons made from polygon_objects.

    implimentation:
        independent_polygons = []
        for polygon in polygons:
            for independent_polygon in independent_polygons:
                intersection = independent_polygon.intersection(polygon)
                independent_polygon=independent_polygon.difference(intersection)
                independent_polygons.append(intersection)
                polygon = polygon.difference(intersection)
    """
    independent_polygons = []
    for polygon in polygon_objects:
        length = len(independent_polygons)
        for i in range(length):
            intersection = independent_polygons[i].intersection(polygon)
            if intersection.area > 0:  # If intersection is non-trivial
                part1 = independent_polygons[i].difference(intersection)
                part2 = polygon.difference(intersection)
                if part1.area > 0:
                    independent_polygons[i] = part1
                    independent_polygons.append(intersection)
                # else independent_polygons[i] already equals intersection
                polygon = part2
        independent_polygons.append(polygon)
    return independent_polygons
