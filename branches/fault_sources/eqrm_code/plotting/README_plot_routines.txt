This file contains some raw documentation on the plot_* routines.
It is expected that this text will be placed into a larger LaTeX
or Word document.
------------------------------------------------------------------

Discussion

There are two basic types of plot routines - graph or 
map.  The graph plots draw a simple graph of values
and the map plots data onto a map of the Earth's surface.

Graph plots use the python matplotlib library and allow you
to optionally display the graph on the screen after generation.  The
map plots use the GMT package to generate the graph and do
not allow automatic display of the image at this time.


General Plot Parameters

The interface to the plot routines is much the same no matter what sort
of data you are plotting.  Here we discuss the parameters that are common
to most plot routines.

output_file

Specifies the name of the generated image file.


title

Defines the string used to title the graph.


show_graph

If 'True' the generated image will be displayed on the screen.  Note that
this will only work for graph plots.

annotate

Can be used to add annotations to a map.  Annotations can be any of:
. A predefined 'generated on ...' text string
. Any text you require
. Any image(s) you require
. Any polygon, filled or unfilled

If annotation=None no annotations are added to the graph.

If annotation=[] (the default), only the predefined 'generated on ...'
text is added.

Otherwise the annotation parameter is a list of one or more tuples like
(<type>, <point>, ...)
where <type> defines the type of annotation (one of 'text', 'image' or 'polygon)
and <point> is a position tuple (longitude, latitude).  Further parameters
depend on the annotation type.  There may be an *optional* final parameter that
is a dictionary of extra parameters to fine-tune the annotation.  This dictionary
is discussed below for each type of annotation.

A moderately complex example of annotations is in eqrm_code/plotting/example_plot_gmt_annotation.py.

    <picture example_annotation1.png>


Text Annotation

The text annotation tuple for a map plot may be either of:
('text', (lon, lat), <string>)
('text', (lon, lat), <string>, <dictionary>)

The (lon, lat) tuple defines the position of the string and the <string> parameter
defines the text of the string.  The <string> text may contain a number of escapes 
allowing you to add special characters.  See http://gmt.soest.hawaii.edu/gmt/doc/gmt/html/man/pstext.html#DESCRIPTION
for the details of the escape sequences.

As a very simple example, the annotation
('text', (0.0, 51.47), 'Greenwich Observatory') would place the text string at
the approximate position of the Greenwich Observatory.

The optional <dictionary> parameter can be used to fine-tune the annotation.  Using your
own dictionary allows you to control things such as:
fontsize     a string holding the font point size (eg, '10').  Default is '8'.
fontno       a string defining the font to use.  Default is 'Helvetica'.
colour       an escape sequence that sets the text colour.  Default is '@;0/0/0;' (r/g/b, in this case, black).
angle        the angle in degrees to rotate text counter-clockwise.  Default is '0'.
justify      a two character string setting the text justification (see below).  Default is 'ML'.
linespace    sets the line spacing in points.  Default is '10p'.
parwidth     defines the width allowed before text is automatically wrapped.  Default is '17.5c' (17.5cm).

A more complicated example to display the Danish capital name in blue just to the left of a
famous landmark is:
dictionary= {'fontsize': '10',
             'justify': 'RM'}
annotation = ('text', (12.599151, 55.692721), '@;blue;K@obenhavn', dictionary) 


Text Justification

When a text string is placed onto a particular position you must specify which one of a set of 
predefined points on the text 'box' is placed on the position.  A text box has width and height
and there are three lines drawn through the edges and centre of the text box.  Considering the
box width, the lines are named 'L', 'C' and 'R' for left, centre and right, respectively.  For
height the lines are 'T', 'M' and 'B' meaning top, middle and bottom, respectively.  So any of
the nine points defined by the intersections of the lines may be specified by a two letter
code.  That is, 'TL' specifies the point at the top-left of the text box, 'CM' means the centre
point, 'CB' means the centre-bottom of the box, and so on.

    <picture text_justify.png>

When placing the text the point indicated is placed on top of the specified longitude and latitude.


Image Annotation

An image annotation has one of these forms:
('image', <position>, <imagefile>)
('image', <position>, <imagefile>, <dictionary>)

The <position> parameter is either a short string or a (lon, lat) tuple.
A placement string is a short string of 1 to 3 characters defining the final position for the
image.

    <picture placement1.png>

The above figure shows the allowed placement strings and the approximate position of the image.
The rectangle shows the silhouette of the plot, so the ENE placement is just outside the plot.

The longitude plus latitude placement puts the centre of the image over the given point.

The optional <dictionary> parameter allows you to override some of the image attributes.  Keys
to the dictionary are:
framewidth   sets the width (pixels) of a frame drawn around the image.  Default is 1.0.
framecolour  sets the colour of the frame.  Default is '0/0/0' (r/g/b, black).
imagewidth   sets the width of the image in centimeters.  Default is 4.0.
imageheight  sets the height of the image in centimeters.  Default is 3.0.

You would place a square image 'test.png' in the top-left corner of a graph using this annotation:
dictionary = {'framecolour': '255/0/0',    # red frame
              'imagewidth': 2.0,
              'imageheight': 2.0}
annotation = ('image', 'NW', 'test.png', dictionary)


Polygon Annotation

The polygon annotation tuple has the form:
('polygon', <polygon>)
('polygon', <polygon>, <dictionary>)

The <polygon> parameters is a list of two or more tuples (lon, lat).  This will cause a *closed*
polygon to be drawn through the specified points.

The <dictionary> parameter allows you some control over the polgon attributes.  The dictionary
has these keys:
linewidth    sets the polygon line width in pixels.  Default is 1.0.
linecolour   sets the polygon outline colour.  Default is '0/0/0' (r/g/b, black).
fillcolour   sets the fill colour of the polygon.  Default is None (no fill).
noclose      specifies that the polygon is not to be closed.  Default is False (closed polygon).

This annotation tuple will draw a closed green unfilled rectangle around the centre of Melbourne:
dictionary = {'linecolour': '0/255/0'}
annotation = ('polygon', ((144.5,-37.6),(145.2,-37.6),
                          (145.2,-38.0),(144.5,-38.0)), dictionary)


np_posn

Sets the position for a 'northpointer' symbol.  The np_posn parameter may be a placement string (see above)
or a (longitude, latitude) tuple.  If nothing is specified for the np_posn parameter no pointer is drawn.


s_posn

Sets the position for a 'scale' symbol showing the size of a distance at the centre latitude of
the graph.  The np_posn parameter may be a placement string (see above) or a
(longitude, latitude) tuple.  If nothing is specified for the s_posn parameter no scale is drawn.


bins

The 'bins' parameter will be recognised by any plot routine that is required to bin
data that is randomly scattered over the X-Y plane.

The 'bins' parameter may be either an integer or a 2-tuple on integers.  The single integer
specifies the number of bins in the X and Y directions used to collect random points into
processing bins.  The 2-tuple allows the user to specify different X and Y numbers.


cb_label

The 'cb_label' parameter allows the user to specify the label text applied to the graph
colourbar.  If the cb_label parameter is not specified, no colourbar is drawn.


cb_steps

This parameter allows the user some control over the colourbar.  The values the parameter
may take are:

None
    The colourbar will be continuous and cover the data value range.

[]
    The colourbar will be discrete and cover the data value range.  Plot code will
    determine the data values at which the colours change.

[val1, val2, ..., valn]
    The colourbar will cover the range of data values from val1 to valn and the colour 
    changes will occur at the intermediate val? values.

Note that any contous plot will silently change a None value for cb_steps to [].


colourmap

This parameter is a string containing the name of the colourmap to use.  The name 
may be one specified by the underlying plotting mechanism (matplotlib or GMT), or 
may be a 'local' colourmap name.

For the map plots (GMT), local colourmaps are defined in eqrm_code/plotting/colourmaps.


ignore
[check in all appropriate routines]

SHOULD *NOT* BE USED IN plot_*.py ROUTINES!
USE IN A calc_*.py routine instead.


save_file

This parameter names the file that will contain the plot data used to create any output
plot.  If this parameter is not set no plot data is saved.


invert
SHOULD BE REMOVED - LOAD ROUTINES SHOULD DO THIS.


bin_sum

This parameter controls the processing of data during 'binning'.

When data is binned into a one or two dimensional collection, the question arises about what to do
with the one or more data values in a bin.  Do we simply count the number of values in each bin,
do we summ the values, or do we calculate the mean of the values?

The bin_sum parameter can have the following values:
eqrm.BIN_COUNT  count the number of values in each bin (-An)
eqrm.BIN_SUM    sum the values in each bin (-A)
eqrm.BIN_MEAN   calculate the mean of the values in each bin (no -A at all)

See also the 'bins' parameter.


xlabel

The 'xlabel' parameter sets the label text for the plot X axis.


ylabel

The 'ylabel' parameter sets the label text for the plot Y axis.


xrange

Sets the maximum X value to plot on the X axis.

Used only by the plot_barchart.py and plot_scen_loss_stats.py routines.


yrange

Sets the maximum Y value to plot on the Y axis.

Used only by the plot_barchart.py and plot_scen_loss_stats.py routines.


grid

The 'grid' parameter controls the display of gridlines in a graph plot.

If 'grid' is True the gridlines are displayed.