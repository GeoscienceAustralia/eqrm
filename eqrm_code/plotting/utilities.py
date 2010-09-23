#!/usr/bin/env python

"""
Various utility functions used by the plotting module.
 
Copyright 2007 by Geoscience Australia

"""


import os
import sys
import math
import tempfile
import shutil
import numpy as num
import copy
import glob
import atexit

import eqrm_code.plotting.plot_config as cfg
import eqrm_code.eqrm_filesystem as ef
import eqrm_code.plotting.util_get_extent as uge


def do_cmd(cmd, fail=False, verbose=True):
    """Execute a command in another process.
    
    cmd     the command string to execute
    fail    if 'cmd' errors fail here if this is True
    verbose if True will echo commands to stdout

    Prints combined stdout+stderr output, if any.

    """

    # TODO: log this rather than print
    if verbose:
        print(cmd)
    (_, fd_stdout, fd_stderr) = os.popen3(cmd)
    result = fd_stdout.read()
    error = fd_stderr.read()
    fd_stdout.close()
    fd_stderr.close()
    if result and verbose:
        print(result)
    if error:
        if not verbose:
            print(cmd)
        print(error)
        if fail:
            msg = '\n' + cmd
            if result:
                msg += '\n' + result
            if error:
                msg += '\n' + error
            raise RuntimeError(msg)


def lat_width(width_deg, lat):
    """
    Convert a degree width at a latitude to kilometres.
    
    width_deg  the width in degrees
    lat        the latitude (degrees) for which kilometre width is required

    Assumes circumference of a spherical earth to be 40,075km.

    Returns the absolute width in kilometres.

    """
   
    # convert latitude degrees to radians
    lat_radians = (lat * math.pi * 2) / 360.0

    # get width of degrees in kilometres at that latitude
    width_km = (40075.0 * abs(width_deg) * math.cos(lat_radians)) / 360.0

    return width_km


def get_scale_skip(max_val, min_val=0.0):
    """Determine the scale skip value to be used by psscale.

    max_val   the maximum value on colorbar scale
    min_val   the minimum value on colorbar scale

    Returns a number that is to be used as skip on the option:
        -Tmin/max/skip
    Skip is such that there will be 5 to 10 steps in scale.

    """

    # check we don't have a Nan as max/min
    if num.isnan(max_val) or num.isnan(min_val):
        raise RuntimeError('get_scale_skip: max_val or min_val is a NaN')

    # get *range* of colorbar
    range = float(max_val) - min_val

    # normalise range to one of 1, 2 or 5
    scale = 1.0
    while int(range) < 1:
        scale *= 10.0
        range *= 10.0
    while int(range) > 10:
        scale /= 10.0
        range /= 10.0
        
    range = int(range)
    
    if range < 1:
        range = 1
    elif range < 2:
        range = 2
    else:
        range = 5
    
    return float(range) / scale / 10


def get_scale_min_max_step(max_val, min_val=0.0):
    """Get a sane min+max+step set of values for a range.

    max_val   the maximum value on colorbar scale
    min_val   the minimum value on colorbar scale

    Returns a tuple (start, stop, step) where 'start' and 'stop' are the
    suggested minimum and maximum scale values, and 'step' is the delta
    to step up with.

    """

    delta = 0.001

    step = get_scale_skip(max_val, min_val)

    # try to latch start/stop to multiples of step that are
    # just outside min_val/max_val
    if min_val < 0.0:
        start = (int((min_val+delta)/step) - 1) * step
    else:
        start = int(min_val/step) * step

    if max_val < 0.0:
        stop = (int((max_val+step)/step) - 1) * step
    else:
        stop = (int((max_val-delta)/step) + 1) * step

    return (start, stop, step)
    
    
def get_unique_key(d, key):
    """Get unique dictionary 'd' key matching 'key'.

    d    the dictionary to interrogate
    key  the key string we look for in 'd'

    Return the full key of dictionary 'd' matching 'key'.
    Return None if no match or > 1 match.

    """

    # create string: |key1|key2|key3|...
    key_string = '|' + '|'.join(d.keys())
    key = '|' + key

    # look for one and only one match of '|key' in key_string
    match1 = key_string.find(key)
    if match1 < 0:
        return None

    # look for a second match beyond the first
    match2 = key_string.find(key, match1+1)
    if  match2 >= 0:
        return None

    # dig out the full matched key text
    try:
        (full_key, _) = key_string[match1+1:].split('|', 1)
    except ValueError:
        full_key = key_string[match1+1:]

    return full_key


# dictionary to map file extension to 'ps2raster' T option char
Extension2TOpt = {'bmp':  'b',
                  'eps':  'e',
                  'pdf':  'f',
                  'jpeg': 'j',
                  'jpg':  'j',
                  'png':  'g',
                  'ppm':  'm',
                  'tiff': 't'}


def make_discrete_cpt(filename, colourmap, seq):
    """Make a discrete CPT file from a user CPT iterable.

    filename   path to CPT file to create
    colourmap  colourmap to base new CPT on (path or name)
    seq        sequence describing required CPT: [val, val, ...]

    """

    # create a scratch directory for ephemeral files
    tmp_dir = tempfile.mkdtemp(prefix='make_discrete_cpt_')

    # sort the seq first, just in case
    seq_list = list(seq)
    seq_list.sort()

    # write out a temporary file with cb_step values, one per line
    temp_cbstep_text = os.path.join(tmp_dir, 'cb_step.txt')
    temp_file = os.path.join(tmp_dir, temp_cbstep_text)
    fd = open(temp_file, 'w')
    for val in seq_list:
        fd.write('%s\n' % str(val))
    fd.close()

    # create new CPT file
    cmd = 'makecpt -C%s -T%s > %s' % (colourmap, temp_file, filename)
    do_cmd(cmd, verbose=False)

    # delete the temporary directory
    shutil.rmtree(tmp_dir)


def make_discrete_cpt_from_seq(filename, seq):
    """Make a discrete CPT file from a user cpt_sequence.

    filename   path to CPT file to create
    seq        sequence describing required CPT:
               [(val, col), (val, col), ...]

    The colour sequence is a hazmap modification.
    For now, leave the colour option undone.

    TODO:
    If *every* element of seq has a colour value, use it.
    Else if first and last have a colour, use that range only.
    Else just use the hazmap colour idea.

    """

    # sort the seq first, just in case
    seq.sort()

    # create a 0-511 sample continuous colour range
    # using the hazmap scheme
    sample = []
    for i in range(256):
        sample.append((i, 255, 0))
    for i in range(256):
        sample.append((255, 255-i, 0))

    # start the CPT file
    fd = open(filename, 'w')
    fd.write('# cpt file created by: make_discrete_cpt_from_seq(%s)\n'
             % str(seq))
    fd.write('# COLOR_MODEL = RGB\n')
    fd.write('#\n')

    # figure out number of steps and step size in sample[]
    num_steps = len(seq)
    step_len = int(len(sample)/num_steps)

    # now generate body of the CPT file
    sample_i = step_len
    for i in range(num_steps-1):
        left = seq[i]
        right = seq[i+1]
        (left_r, left_g, left_b) = sample[sample_i]
        fd.write('%f\t%03d %03d %03d\t%f\t%03d %03d %03d\n'
                 % (left, left_r, left_g, left_b,
                    right, left_r, left_g, left_b))
        sample_i += step_len

    # finish with background, foreground and NaN colours
    fd.write('B\t0\t255\t0\n')
    fd.write('F\t255\t0\t0\n')
    fd.write('N\t-\n')

    fd.close()


def make_continuous_cpt_from_seq(filename, seq):
    """Make a continuous CPT file from a user cpt_sequence.

    filename   path to CPT file to create
    seq        sequence describing required CPT:
               [(val, col), (val, col), ...]

    The colour sequence is a hazmap modification.
    For now, leave the colour option undone.

    TODO:
    If *every* element of seq has a colour value, use it.
    Else if first and last have a colour, use that range only.
    Else just use the hazmap colour idea.

    """

    # sort the seq first, just in case
    seq.sort()

    # create a 0-511 sample continuous colour range
    # using the hazmap scheme
    sample = []
    for i in range(256):
        sample.append((i, 255, 0))
    for i in range(256):
        sample.append((255, 255-i, 0))

    # start the CPT file
    fd = open(filename, 'w')
    fd.write('# cpt file created by: make_cpt_from_seq(%s)\n' % str(seq))
    fd.write('# COLOR_MODEL = RGB\n')
    fd.write('#\n')

    # figure out number of steps and step size in sample[]
    num_steps = len(seq)
    step_len = int(len(sample)/num_steps)

    # now generate body of the CPT file
    sample_i = step_len
    for i in range(num_steps-1):
        left = seq[i]
        right = seq[i+1]
        (left_r, left_g, left_b) = sample[sample_i]
        (right_r, right_g, right_b) = sample[sample_i+step_len]
        fd.write('%f\t%03d %03d %03d\t%f\t%03d %03d %03d\n'
                 % (left, left_r, left_g, left_b,
                    right, right_r, right_g, right_b))
        sample_i += step_len

    # finish with background, foreground and NaN colours
    fd.write('B\t0\t255\t0\n')
    fd.write('F\t255\t0\t0\n')
    fd.write('N\t-\n')

    fd.close()


def set_gmt_defaults(tmp_dir):
    """Set the 'standard' GMT default values for plotting.
    
    tmp_dir  path to the temporary directory GMT should use
             for storing .gmtdefaults

    """

    # delete local copies of files '.gmt*'
    files = glob.glob('.gmt*')
    for f in files:
        os.remove(f)
    
    # set up GMT isolation mode
    if sys.platform == 'win32':
        do_cmd('set GMT_TMPDIR=%s' % tmp_dir)
    else:
        do_cmd('export GMT_TMPDIR=%s' % tmp_dir)

    # set the GMT parameters we require
    do_cmd('gmtset PAPER_MEDIA = Custom_100cx100c')
    do_cmd('gmtset BASEMAP_TYPE = plain')
    do_cmd('gmtset PAGE_ORIENTATION = portrait')
    do_cmd('gmtset MEASURE_UNIT = cm')
    do_cmd('gmtset PLOT_DEGREE_FORMAT = +D.x')
    do_cmd('gmtset OUTPUT_DEGREE_FORMAT = +D.x')
    do_cmd('gmtset D_FORMAT = "%.02f"')

    # header text sizes, offset
    do_cmd('gmtset HEADER_FONT_SIZE = 20p')
    do_cmd('gmtset HEADER_OFFSET = 0.25c')

    # text labelling the scale
    do_cmd('gmtset LABEL_FONT_SIZE = 10p')
    do_cmd('gmtset LABEL_OFFSET = 0.25c')

    do_cmd('gmtset ANNOT_FONT_SIZE_PRIMARY = 10p')
    do_cmd('gmtset ANNOT_FONT_SIZE_SECONDARY = 8p')


def get_xyz_bin_inc(xyz, epsilon=1.0e-6):
    """Get any X and Y binning numbers of an XYZ data object.

    xyz      Sequence of (lon, lat, val) tuples.
    epsilon  allowable difference between bin size

    Returns (x_num, y_num) if binning exists, or None if no binning.
    (x_num and y_num are the number of bins in X and Y directions)

    """

    # initialise empty sets of X and Y coords
    x_coords = set()
    y_coords = set()

    # now get the X and Y coordinate sets, convert to sorted lists
    for (lon, lat, _) in xyz:
        x_coords.add(lon)
        y_coords.add(lat)

    x_coords = list(x_coords)
    x_coords.sort()
    y_coords = list(y_coords)
    y_coords.sort()

    if len(x_coords) < 2 or len(y_coords) < 2:
        return None

    # get initial X and Y increment steps and ensure same for all coordinates
    x_inc = x_coords[1] - x_coords[0]
    y_inc = y_coords[1] - y_coords[0]

    for i in range(len(x_coords)-1):
        inc = x_coords[i+1] - x_coords[i]
        if abs(x_inc - inc) > epsilon:
            return None

    for i in range(len(y_coords)-1):
        inc = y_coords[i+1] - y_coords[i]
        if abs(y_inc - inc) > epsilon:
            return None

    # return number of bins in X & Y directions
    x_num = int((x_coords[-1] - x_coords[0])/x_inc) + 1
    y_num = int((y_coords[-1] - y_coords[0])/y_inc) + 1

    return (x_num, y_num)


def get_coords_cm(lon, lat, extent, j_opt):
    """Convert lon+lat into map pixel coordinates.

    lon      longitude of point
    lat      latitiude of point
    extent   the map extent (ll_lat, ll_lon, ur_lat, ur_lon)
    j_opt    the GMT -J option string

    Returns a tuple (x, y) of the point position in cm from the map
    bottom left origin.

    """

    # create a scratch directory for ephemeral files
    tmp_dir = tempfile.mkdtemp(prefix='get_coords_cm')

    # unpack the extent
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # create data file for psxy
    data_file = os.path.join(tmp_dir, 'point.txt')
    fd = open(data_file, 'w')
    fd.write('%f %f\n' % (lon, lat))
    fd.close()

    # get PNG coordinates and associate with lon+lat+height
    ps_file = os.path.join(tmp_dir, 'point.ps')
    cmd = ('psxy %s %s %s -Sp -G255/0/0 -K -O > %s'
           % (data_file, r_opt, j_opt, ps_file))
    do_cmd(cmd)

    # read the postscript file
    fd = open(ps_file, 'r')
    lines = fd.readlines()
    fd.close()

    # look in lines for X,Y coords
    x = None        # assume not found

    for i in range(len(lines)):
        l = lines[i]
        if l.find('1 setlinecap') != -1:
            (_, x, y, _) = lines[i+1].split(' ')
            break

    if x is None:
        raise RuntimeError("Didn't find X+Y in postscript file:\n%s"
                           % str(lines))

    # convert pixel values to cm
    x = float(x)/cfg.PointsPerCentimetre
    y = float(y)/cfg.PointsPerCentimetre

    return (x, y)


def convert_lonlat_cm(lon, lat, extent):
    """Convert a lon+lat to x+y in centimetres.

    lon     longitude of point of interest
    lat     latitude of point of interest
    extent  extent of map (ll_lat, ll_lon, ur_lat, ur_lon)

    Returns a tuple (x, y) of position (centimetres).

    """

    # unpack extent
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # get width+height of map in centimetres
    j_opt = '-JM%f' % cfg.MapWidthCentimetres
    (width, height) = get_coords_cm(ur_lon, ur_lat, extent, j_opt)

    # get posn of desired point
    (x_offset, y_offset) = get_coords_cm(lon, lat, extent, j_opt)

    return (x_offset, y_offset)


def convert_cm_lonlat(x, y, extent):
    """Convert a point in centimetres to lon+lat.

    x       X coordinate of point in centimetres from lower left origin
    y       Y coordinate of point in centimetres from lower left origin
    extent  extent of map (ll_lat, ll_lon, ur_lat, ur_lon)

    Returns a tuple (lon, lat) of position.

    """

    # unpack extent
    (ll_lat, ll_lon, ur_lat, ur_lon) = extent
    r_opt = '-R%f/%f/%f/%f' % (ll_lon, ur_lon, ll_lat, ur_lat)

    # get width+height of map in centimetres
    j_opt = '-JM%f' % cfg.MapWidthCentimetres
    (width_cm, height_cm) = get_coords_cm(ur_lon, ur_lat, extent, j_opt)

    (x,y) = get_coords_cm(ll_lon+0.1, ll_lat+0.1, extent, j_opt)

    # get width+height of map in decimal degrees
    width_deg = ur_lon - ll_lon
    height_deg = ur_lat - ll_lat

    # get linear estimate of degree position
    x_offset_deg = x * width_deg / width_cm
    y_offset_deg = y * height_deg / height_cm

    return (x_offset_deg+ll_lon, y_offset_deg+ll_lat)


def get_colourmap(cmap, tmpdir=None):
    """Get a colourmap name given a user name string.

    cmap  a colourmap name string (case insensitive)
    tmpdir  path to a user temporary directory to use
            (if None, create our own)

    Returns either a GMT colormap name or a path to a local colourmap file.

    This function gets the current GMT colormap name list from the makecpt
    command itself.  This means we don't have to do anything when the 
    installed GMT is updated.

    NOTE: Due to limitations in GMT executables (grd2cpt, I'm looking at you!)
          this routine copies the local CPT file to the temporary directory
          and returns that path.  This shortens the path, which is the problem
          with grd2cpt.

    """

    # make sure the requested name is lowercase
    lower_cmap = cmap.lower()

    # get the current list of GMT colormap names
    (_, fd_stdouterr) = os.popen4('makecpt')
    result = fd_stdouterr.read()
    fd_stdouterr.close()
    lines = result.split('\n')

    state = 0       # 0 means before '---- delimiter
                    # 1 means found delimiter, reading names
    names = []      # put known names in this list
    for l in lines:
        l = l.strip()
        if state == 0:
            if '------' in l:
                state = 1
        else:
            if '------' in l:
                break
            (name, _) = l.split(':', 1)
            names.append(name.strip())

    # if cmap is in the GMT colormap name list, just return that
    if lower_cmap in names:
        return lower_cmap

    # create temporary directory if necessary
    if tmpdir is None:
        tmpdir = tempfile.mkdtemp(prefix='cpt_', dir='.')
        atexit.register(shutil.rmtree, tmpdir, {'ignore_errors': True})

    # else look in the local colourmap directory
    cmap_path = os.path.join(ef.Eqrmcode_Plotting_Colourmaps_Path,
                             lower_cmap + '.cpt')
    if os.path.isfile(cmap_path):
        # if it's there, copy to the temp directory, return that
        cpt_file = os.path.join(tmpdir, lower_cmap + '.cpt')
        shutil.copy(cmap_path, cpt_file)
        return cpt_file

    msg = "Colourmap name '%s' isn't recognised" % cmap
    raise RuntimeError(msg)


def bin_extent(lat, lon, bins=100):
    """Bin random lon+lat points.

    lat    Nx1 array of latitude values
    lon    Nx1 array of longitude values
    bins   an integer or (bin_x, bin_y) describing how the extent
           of the data in (lat, lon) is to be binned
           If one integer is supplied the extent determined from the
           point data (lat, lon) is binned that number of times in the
           Y and X direction.  If (M, N), the number of Y bins is M, etc.

    Returns a 2D array (bin_x, bin_y) of lists containing indices of points 
    binned into each grid cell.
    """

    # get bin width and number of cells
    try:
        (gnumy, gnumx) = bins
    except TypeError:
        gnumx = gnumy = bins

    # convert two Nx1 arrays lat and lon to [[lon, lat], ...]
    data = zip(lon, lat)

    (ll_lat, ll_lon, ur_lat, ur_lon) = uge.get_extent(data, margin=0)

    lon_width = ur_lon - ll_lon
    lat_width =  ur_lat - ll_lat

    gwidx = lon_width / gnumx
    gwidy = lat_width / gnumy

    return bin_data(lat, lon, ll_lon, ll_lat, gwidx, gwidy, gnumx, gnumy)


def bin_data(lat, lon, minlon, minlat, gwidx, gwidy, gnumx, gnumy):
    """Bin random lon+lat points into a given grid.

    lat    Nx1 array of latitude values
    lon    Nx1 array of longitude values
    minlon longitude of lower left corner of binning grid
    minlat latitude of lower left corner of binning grid
    gwidx  width of grid cell longitude
    gwidy  width of grid cell latitude
    gnumx  number of cells along grid longitude
    gnumy  number of cells along grid latitude

    Returns a list of lists (gnumx, gnumy) of a dictionary.
    The dictionary has two keys;
      'index': a list containing indices of points 
               binned into each grid cell.
      'mid_lat_lon': an array of [lat, lon] values, describing the
                     mid-point of the grid cell.
    """

    # ensure lon and lat arrays of same length
    if len(lon) != len(lat):
        msg  = 'lon and lat arrays have different lengths!?'
        raise RuntimeError(msg)

    res = []
    # prepare the result array
    gwidx_half = gwidx/2.0
    gwidy_half = gwidy/2.0
    for x in range(gnumx):
        res.append([])
        for y in range(gnumy):
            res[x].append({'index':[],
                           'mid_lat_lon':num.array(
                [minlat + gwidy*y + gwidy_half,
                 minlon + gwidx*x + gwidx_half])})

    # get max+min lon and lat
    maxlon = minlon + gwidx*gnumx
    maxlat = minlat + gwidy*gnumy

    for x in range(len(lon)):
        plon = lon[x]
        plat = lat[x]

        if minlon <= plon <= maxlon and minlat <= plat <= maxlat:
            i = min(gnumx-1, int((plon - minlon)/gwidx))
            j = min(gnumy-1, int((plat - minlat)/gwidy))
            res[i][j]['index'].append(x)

    return res

######
# Why do we need these two functions?  Note the following:
#
#    import numpy as num
#
#    a = num.array([[num.nan],[6],[9]])
#    print num.max(a)        # prints 9.0
#    a = num.array([[3],[num.nan],[9]])
#    print num.max(a)        # prints 9.0 
#    a = num.array([[3],[6],[num.nan]])
#    print num.max(a)        # prints nan
#
#    b = num.array([[num.nan,6,9]])
#    print num.max(b)        # prints 9.0
#    b = num.array([[3,num.nan,9]])
#    print num.max(b)        # prints 9.0
#    b = num.array([[3,6,num.nan]])
#    print num.max(b)        # prints nan
#
######

def max_nan(vector):
    """Get maximum value in a vector ignoring NaN values.

    vector  a Nx1 array of values possibly including NaN

    Returns a scalar that is the maximum value, ignoring NaN values.
    """

    return vector[num.nanargmax(vector)]

def min_nan(vector):
    """Get minimum value in a vector ignoring NaN values.

    vector  a Nx1 array of values possibly including NaN

    Returns a scalar that is the minimum value, ignoring NaN values.
    """

    return vector[num.nanargmin(vector)]

######
# 
######

def get_canonical_range(plot_range):
    """Convert a plot range value to the canonical form.

    plot_range  a range value, either None, a scalar or a 2-tuple of scalars

    Plot ranges are specified as a 2-tuple of scalars (int or float).
    Convert a range of either None, 1 scalar or a tuple/list to a 2-tuple
    of floats.

    If only one scalar is supplied, assume it's the upper limit and assume
    the lower limit is 0.
    """
    
    if plot_range:
        if isinstance(plot_range, int) or isinstance(plot_range, float):
            plot_range = (0, float(plot_range))
        else:
            if len(plot_range) == 1:
                plot_range = (0, float(plot_range[0]))

    return plot_range


