#!/usr/bin/env python

"""
Place annotations on a GMT plot.
 
Copyright 2007 by Geoscience Australia

"""


import os
import time

import eqrm_code.plotting.plot_config as cfg
import eqrm_code.plotting.utilities as util
import eqrm_code.plotting.util_gmt_placement as ugp
import eqrm_code.plotting.plot_config as cfg


######
# Do a 'generated at ...' annotation.
# Never directly called by user code.
######

def generated_annotation(tmpdir, psfile, extent, mapsize, jok_opt):
    """
    Place 'generated at ...'  annotation on a GMT graph.

    tmpdir    is the path to a temporary scratch directory
    psfile    path to the POSTSCRIPT file to write to
    extent    the map extent ()
    mapsize   notional mapsize (cm)
    jok_opt   the GMT -J, -O and -K options string

    """

    # file we fill with annotation text
    txt_file = os.path.join(tmpdir, 'data.txt')

    # get string we are going to use
    ann_str = time.strftime('Generated at %H:%M:%S on %d %b %Y')

    # figure out where we are going to put the annotation
    # -1.0c from origin, -1.0c down
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    vert_deg = (ur_lat - ll_lat)
    offset_lon = ll_lon - (vert_deg/mapsize)*1.0
    offset_lat = ll_lat - (vert_deg/mapsize)*1.0

    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # create the annotation text file
    ann_hdr = '%f %f 6 0 0 bl ' % (offset_lon, offset_lat)
    fd = open(txt_file, 'w')
    fd.write(ann_hdr)
    fd.write(ann_str)
    fd.close()

    # annotate the plot
    cmd = 'pstext %s %s %s -N >> %s' % (txt_file, r_opt, jok_opt, psfile)
    util.do_cmd(cmd)


######
# Do a text annotation.
######

# GMT 'pstext' default strings
DefaultFontSize = '8'           # 8 point font
DefaultFontNo = 'Helvetica'     # font name
DefaultColour = '@;0/0/0;'      # text is black
DefaultAngle = '0'              # 0 degrees rotation ccw
DefaultJustify = 'ML'           # text justification
DefaultLinespace = '10p'        # line spacing in points
DefaultParWidth = '%.2fc' % cfg.MapWidthCentimetres  # para width
DefaultParJust = 'l'            # paragraph justification


def text_annotation(tmpdir, psfile, extent, j_opt, ok_opt, annotate):
    """
    Place user text annotation on a GMT graph.

    tmpdir    is the path to a temporary scratch directory
    psfile    path to the POSTSCRIPT file to write to
    extent    extent of the map
    j_opt     the GMT J option string
    ok_opt    the GMT O and K option string
    annotate  user annotations
              a list of tuples like
                  (type, (lon, lat), str) or
                  (type, (lon, lat), str, dict)
              where lon, lat are lon/lat coordinate values
                    str      is the text string to write
                    dict     is a set of args controlling
                             the text write

    The 'dict' annotate parameter has the form:
        {'fontsize': <fontsize float>,
         'colour': <colour>,
        }

    The user annotation string may contain any of the '@' escape sequences
    described at:
    http://gmt.soest.hawaii.edu/gmt/doc/gmt/html/man/pstext.html#DESCRIPTION
    
    """

    # file we fill with annotation text
    txt_file = os.path.join(tmpdir, 'data.txt')

    # unpack the annotation sequence
    if len(annotate) == 3:
        (_, point, annstr) = annotate
        anndict = {}
    elif len(annotate) == 4:
        (_, point, annstr, anndict) = annotate
    else:   # handle overflow
        (_, point, annstr, anndict, _) = annotate

    (x, y) = point

    # set defaults, if required
    fontsize = anndict.get('fontsize', DefaultFontSize)
    fontno = anndict.get('fontno', DefaultFontNo)
    colour = anndict.get('colour', DefaultColour)
    angle = anndict.get('angle', DefaultAngle)
    justify = anndict.get('justify', DefaultJustify)
    linespace = anndict.get('linespace', DefaultLinespace)
    parwidth = anndict.get('parwidth', DefaultParWidth)
    parjust = anndict.get('parjust', DefaultParJust)

    # unpack extent
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # create the annotation text file
    ann_hdr = ('%f %f %s %s %s %s %s'
                % (x, y, fontsize, angle, fontno, justify, colour))
    fd = open(txt_file, 'w')
    fd.write(ann_hdr)
    fd.write(annstr)
    fd.close()

    # annotate the plot
    cmd = ('pstext %s %s %s %s -N >> %s'
           % (txt_file, r_opt, j_opt, ok_opt, psfile))
    util.do_cmd(cmd)


######
# Do an image annotation.
######

# dictionary to convert simple place string to x,y,justify
ImagePlacement = {'ne':  ('x=map_width;'
                          'y=map_height;'
                          'justify="TR"'),
                  'ce':  ('x=map_width;'
                          'y=map_height/2;'
                          'justify="MR"'),
                  'se':  ('x=map_width;'
                          'y=0.0;'
                          'justify="BR"'),
                  'cs':  ('x=map_width/2;'
                          'y=0.0;'
                          'justify="BC"'),
                  'sw':  ('x=0.0;'
                          'y=0.0;'
                          'justify="BL"'),
                  'cw':  ('x=0.0;'
                          'y=map_height/2;'
                          'justify="ML"'),
                  'nw':  ('x=0.0;'
                          'y=map_height;'
                          'justify="TL"'),
                  'cn':  ('x=map_width/2;'
                          'y=map_height;'
                          'justify="TC"'),
                  'c':   ('x=map_width/2;'
                          'y=map_height/2;'
                          'justify="CM"'),
                  'nne': ('x=map_width;'
                          'y=map_height+imageheight+margin_y;'
                          'justify="TR"'),
                  'ene': ('x=map_width+imagewidth+margin_x;'
                          'y=map_height;'
                          'justify="TR"'),
                  'ece': ('x=map_width+imagewidth+margin_x;'
                          'y=map_height/2;'
                          'justify="MR"'),
                  'ese': ('x=map_width+imagewidth+margin_x;'
                          'y=0.0;'
                          'justify="BR"'),
                  'sse': ('x=map_width;'
                          'y=0.0-imageheight-margin_y;'
                          'justify="BR"'),
                  'scs': ('x=map_width/2;'
                          'y=0.0-imageheight-margin_y;'
                          'justify="BC"'),
                  'ssw': ('x=0.0;'
                          'y=0.0-imageheight-margin_y;'
                          'justify="BL"'),
                  'wsw': ('x=0.0-imagewidth-margin_x;'
                          'y=0.0;'
                          'justify="BL"'),
                  'wcw': ('x=0.0-imagewidth-margin_x;'
                          'y=y=map_height/2;'
                          'justify="ML"'),
                  'wnw': ('x=0.0-imagewidth-margin_x;'
                          'y=map_height;'
                          'justify="TL"'),
                  'nnw': ('x=0.0;'
                          'y=map_height+imageheight+margin_y;'
                          'justify="TL"'),
                  'ncn': ('x=map_width/2;'
                          'y=map_height+imageheight+margin_y;'
                          'justify="BC"')}

def image_annotation(tmpdir, psfile, extent, j_opt, ok_opt, annotate):
    """Image annotation.

    tmpdir   a temporary scratch directory
    psfile   output postscript file
    extent   extent of the map
    j_opt    GMT -J option string
    ok_opt   GMT -O and -K option string
    annotate the annotation data:
             ('image', <posn>, <imagefile>, <kwargs>)
             where <posn>      is a position specifier
                               (string or lon,lat tuple)
                   <imagefile> is the path to the EPS image file
                   <kwargs>    is a dictionary of extra args
                               (optional)

    """
   
    # set default polygon attributes
    framewidth = 1.0
    framecolour = '0/0/0'
    imagewidth = 4.0
    imageheight = 3.0

    # unpack the annotate command object
    try:
        (_, posn, imagefile, kwargs) = annotate
    except ValueError:
        (_, posn, imagefile) = annotate
        kwargs = {}

    # if given image height but not width, calculate width assuming
    # aspect ratio of default image width and height, etc
    if (kwargs.get('imagewidth', None) is None
            and kwargs.get('imageheight', None) is not None):
        kwargs['imagewidth'] = kwargs['imageheight']*imagewidth/imageheight
    elif (kwargs.get('imageheight', None) is None
              and kwargs.get('imagewidth', None) is not None):
        kwargs['imageheight'] = kwargs['imagewidth']*imageheight/imagewidth

    # override default polygon attributes from kwargs
    framewidth = float(kwargs.get('framewidth', framewidth))
    framecolour = kwargs.get('framecolour', framecolour)
    imagewidth = float(kwargs.get('imagewidth', imagewidth))
    imageheight = float(kwargs.get('imageheight', imageheight))
    want_frame = not kwargs.get('noframe', False)

    # set X and Y margins
    margin_x = 1.0
    margin_y = 1.0

    # unpack the extent and get map size in cm
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    (map_width, map_height) = util.get_coords_cm(ur_lon, ur_lat, extent, j_opt)

    # figure out image placement, convert to cm
    if isinstance(posn, basestring):
        lower_posn = posn.lower()
        try:
            eval_str = ImagePlacement[lower_posn]
        except KeyError:
            raise RuntimeError("Placement string '%s' is not recognised" % posn)
    else:
        # we have a (lon, lat) tuple
        # TODO: implement!
        pass

    # execute the posn eval_str - gives us x, y and justify
    exec(eval_str)

    # set -W option - final image size
    w_opt = '-W%.2f/%.2f' % (imagewidth, imageheight)

    # do -C option as well as the frame, if required
    c_opt = '-C%.3f/%.3f/%s' % (x, y, justify)
    if want_frame:
        f_opt = '-F%.1f,%s' % (framewidth, framecolour)

    # now put image into PS file
    cmd = ('psimage %s %s %s %s %s >> %s'
           % (imagefile, ok_opt, w_opt, c_opt, f_opt, psfile))
    util.do_cmd(cmd)


######
# Do a polygon annotation.
######

def polygon_annotation(tmpdir, psfile, extent, j_opt, ok_opt, annotate):
    """Polygon annotation.

    tmpdir   a temporary scratch directory
    psfile   output postscript file
    extent   extent of the map
    j_opt    GMT -J option string (unused!)
    ok_opt   GMT -O and -K option string
    annotate the annotation data:
             ('polygon', ((lon,lat),(lon',lat'),...), <kwargs>)

    By default the polygon will be closed.

    The optional <kwargs> will be a dictionary of extra parameters,
    such as line width, fill colour, etc.  The dictionary will be optional.

    """

    # set default polygon attributes
    linewidth = 1.0
    linecolour = '0/0/0'
    fillcolour = None
    l_opt = '-L'

    # unpack the annotate command object
    try:
        (_, points, kwargs) = annotate
    except ValueError:
        (_, points) = annotate
        kwargs = {}

    # set polygon attributes from kwargs
    linewidth = kwargs.get('linewidth', linewidth)
    linecolour = kwargs.get('linecolour', linecolour)
    fillcolour = kwargs.get('fillcolour', fillcolour)
    if kwargs.get('noclose', False):
        l_opt = ''

    # unpack extent, get -R option
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # file we fill with annotation text
    txt_file = os.path.join(tmpdir, 'polygon.txt')

    # write polygon data to the text file
    fd = open(txt_file, 'w')
    for (lon, lat) in points:
        fd.write('%f %f\n' % (lon, lat))
    fd.close()

    # do GMT command
    w_opt = '-W%.2f,%s' % (linewidth, linecolour)
    g_opt = ''
    if fillcolour:
        g_opt = '-G%s' % fillcolour
    cmd = ('psxy %s %s %s %s %s %s %s >> %s'
           % (txt_file, j_opt, r_opt, ok_opt, l_opt, w_opt, g_opt, psfile))
    util.do_cmd(cmd)


##########
# General annotation routine - passes off to specific handlers
##########

# define dictionary mapping annotation 'type' to handler function
AnnDictType = {'text': text_annotation,
               'image': image_annotation,
               'polygon': polygon_annotation}


def user_annotation(tmpdir, psfile, extent, j_opt, ok_opt, annotate):
    """
    Place user annotations on a GMT graph.

    tmpdir    is the path to a temporary scratch directory
    psfile    path to the POSTSCRIPT file to write to
    extent    extent of the map
    j_opt     the GMT J option string
    ok_opt    the GMT O and K option string
    annotate  user annotations
              a list of tuples like
                  (type, lon, lat, ...)
              where type     is the annotation type
                    lat, lon are lon/lat coordinate values
                    ...      are type-specific parameters

    Passes data to the specific handler for each annotation.

    """

    # do each user annotation
    for n in annotate:
        # pick out the type and get handler function
        ann_type = n[0]
        if not isinstance(ann_type, basestring):
            raise RuntimeError('Annotation type must be a string: %s'
                               % str(ann_type))
        at = util.get_unique_key(AnnDictType, ann_type.lower())
        if at is None:
            raise RuntimeError("Annotation type '%s' is unrecognised"
                               % ann_type)

        handler = AnnDictType[at]

        # now call the handler, passing data
        handler(tmpdir, psfile, extent, j_opt, ok_opt, n)


