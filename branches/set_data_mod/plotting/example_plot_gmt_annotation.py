#!/usr/bin/env python

"""
Show placing annotations on a GMT plot.
 
Copyright 2007 by Geoscience Australia

"""


import eqrm_code.plotting.plot_gmt_map as pgm


################################################################################
# A Hilbert class to produce hilbert curve data.
#
# Found at:
# http://svn.python.org/projects/python/trunk/Demo/turtle/tdemo_fractalcurves.py
#
# Modified to return a list of points on the curve.
################################################################################

class Hilbert(object):
    def get_curve(self, size, order, parity, lon_offset, lat_offset):
        """Get a list of points on a Hilbert curve of given order.

        size       step size for each forward movement
        order      order of required curve
        parity     direction initial heading is set at
        lon_offset where the origin of curve is
        lat_offset where the origin of curve is
        """
        self.x = self.y = 0
        self.heading = 0
        self.lon_offset = lon_offset
        self.lat_offset = lat_offset
        self.curve = []
        self.curve.append((self.lon_offset+float(self.x)/100,
                           self.lat_offset+float(self.y)/100))
        self.hilbert(size, order, parity)
        return self.curve

    def left(self, degrees):
        self.heading += degrees
        if self.heading >= 360:
            self.heading -= 360
        if self.heading < 0:
            self.heading += 360

    def right(self, degrees):
        self.heading -= degrees
        if self.heading >= 360:
            self.heading -= 360
        if self.heading < 0:
            self.heading += 360

    def forward(self, steps):
        if self.heading == 0:
            self.x += steps
        elif self.heading == 90:
            self.y += steps
        elif self.heading == 180:
            self.x -= steps
        elif self.heading == 270:
            self.y -= steps
        else:
            raise RuntimeError('ERROR: self.heading=%s' % str(self.heading))
        self.curve.append((self.lon_offset+float(self.x)/100,
                           self.lat_offset+float(self.y)/100))

    def hilbert(self, size, order, parity):
        """Make a Hilbert curve of given order.

        size   step size for each forward movement
        order  order of required curve
        parity direction initial heading is set at
        """

        if order == 0:
            return

        # rotate and draw first subcurve with opposite parity to big curve
        self.left(parity * 90)
        self.hilbert(size, order - 1, -parity)

        # interface to and draw second subcurve with same parity as big curve
        self.forward(size)
        self.right(parity * 90)
        self.hilbert(size, order - 1, parity)

        # third subcurve
        self.forward(size)
        self.hilbert(size, order - 1, parity)

        # fourth subcurve
        self.right(parity * 90)
        self.forward(size)
        self.hilbert(size, order - 1, -parity)

        # a final turn is needed to make the turtle
        # end up facing outward from the large square
        self.left(parity * 90)


################################################################################
# Run a simple map, exercising the annotation methods.
# Code lifted from plot_gmt_xyz.py and really simplified.
#
# We don't do this in a unit test as we want to *see* the results!
################################################################################

if __name__ == '__main__':
    # set extent and -R option (around Melbourne)
    extent = (-39.0, 144.0, -37.0, 146.0)
    r_opt = '-R144.0/146.0/-39.0/-37.0'

    # get hilbert curve polygon points
    h = Hilbert()
    hcurve = h.get_curve(1, 6, 1, 145.01, -38.49)

    # do a selection of annotations
    annotations = [('polygon',  # filled closed complex polygon
                    ((145.8,-37.55),(145.9,-37.8),(145.65,-37.65),(145.95,-37.65),(145.7,-37.8)),
                    {'linewidth': 4.0,
                     'linecolour': '0/255/0',
                     'fillcolour': '0/255/255'}),
                   ('polygon',  # filled closed simple polygon
                    ((144.4,-37.3),(144.4,-37.9),(145.5,-37.9),(145.5,-37.3)),
                    {'linewidth': 2.0,
                     'linecolour': '255/0/0',
                     'fillcolour': '255/255/0'}),
                   ('polygon',  # big unfilled open polygon
                    hcurve,
                    {'linewidth': 3.0,
                     'linecolour': '0/0/255',
                     'noclose': True}),
                   ('text',     # label the hilbert curve
                    (145.665, -38.493),
                    'Hilbert Curve, order 6',
                    {'angle': '90'}),
                   # now show features available for text annotation
                   ('text', (144.5, -37.40),
                    '@;red;RED @;green;GREEN@;; and @;blue;BLUE@;; text'),
                   ('text', (144.5, -37.45),
                    '@:16:LARGER@:: text'),
                   ('text', (144.5, -37.50),
                    '@_UNDERLINE@_ text'),
                   ('text', (144.5, -37.55),
                    'Accented chars: @a@c@e@n@o@s@u@A@C@E@N@O@U'),
                   ('text', (144.5, -37.60),
                    'Symbol: @~ABCDEFGHIJKLMNOPQRSTUVWXYZ@~'),
                   ('text', (144.5, -37.65),
                    '@-subscript@- normal @+superscript@+'),
                   ('text', (144.5, -37.70),
                    'Overstrike: @@!O~ gives @!O~'),
                   ('text', (144.5, -37.75),
                    'ZapfDingbats: @%34%ZapfDingbats@%%'),
                   ('text', (144.5, -37.80),
                    '@#Small Caps@#'),
                   ('text', (144.5, -37.85),
                    'Rotated 45 degrees, right justified',
                    {'angle': '45', 'justify': 'MR'}),
                   # now place an image on  the map
                   ('image', 'SW', 'austgov-stacked.sun',
                    {'framewidth': 1.0, 'framecolour': '255/0/0',
                     'imagewidth': 3.0, 'imageheight': 2.0})
                  ]

    pgm.plot_gmt_map(extent, 'example_plot_gmt_annotation.png',
                     title='Annotation test', np_posn='NE',
                     s_posn='SE', annotate=annotations)


