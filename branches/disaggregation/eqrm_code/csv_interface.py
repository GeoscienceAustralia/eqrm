"""
 Title: csv_interface.py
  
  Author:  Peter Row, peter.row@ga.gov.au

  Description: Functions to convert csv files to arrays.

  Version: $Revision: 1687 $  
  ModifiedBy: $Author: rwilson $
  ModifiedDate: $Date: 2010-06-08 16:12:19 +1000 (Tue, 08 Jun 2010) $
  
  Copyright 2007 by Geoscience Australia
"""


import string
import csv
import scipy


def csv_to_arrays(filename, **attributes):
    """Convert a CSV file into a dictionary indexed by attributes.

    filename    path to the data file to read, or open file object
                (can't be iterable, as we call filename.close())
    attributes  dictionary of required attributes

    The attributes dict has the required columns from the data file
    as keys, with the data type as the values.

    The result is a dictionary with keys from attributes and a list
    of values for the columns.

    For example:
        filename = "site_data.csv"
        attributes = {"LATITUDE": float, "LONGITUDE": float, "ADDRESS": str}
        site_data = csv_to_arrays(filename, **attributes)

    'site_data' -> {'LATITUDE': [float, float, ...],
                    'LONGITUDE': [float, float, ...],
                    'ADDRESS': [str, str, ...]}
    where the lists are SciPy arrays.
    """

    # ensure we have a file object
    if isinstance(filename, file):
        f = filename
    else:
        f = open(filename, 'rb')

    # try to read entire file at once, if error, go to slower method
    try:
        answer = quick_convert_csv_to_arrays(f, **attributes)
        f.close()
        return answer
    except MemoryError:
        # file too big for memory, read one column at a time
        answer = {}
        for (key, convert) in attributes.items():
            answer[key] = csv_to_array(f, key, convert)
        f.close()
        return answer


def quick_convert_csv_to_arrays(f, **attributes):
    """Read entire CSV file into memory, return required columns, converted.

    f           an open file object (or any iterable)
    attributes  a dictionary, keys are required columns,
                values are conversion functions applied to each value in column

    Returns a dictionary with column keys, values are SciPy arrays of values
    for the column:
        {'header1': [<value>, <value, ...],
         'header2': [<value>, <value, ...],
         ...}
    Columns with headers not mentioned in 'attributes' are not returned.
    """

    reader = csv.DictReader(f)
    keys = attributes.keys()
    if True:
        data = [[attributes[key](row[key].strip(' ')) for key in keys]
                for row in reader]
    else:
        data = []
        for row in reader:
            data.append([attributes[key](row[key].strip(' ')) for key in keys])

    answer = {}
    for (i, key) in enumerate(keys):
        answer[key] = scipy.array([row[i] for row in data])
    return answer


def csv_to_array(f, key, conversion):
    """Read a CSV file and convert/return one column of the file.

    f           an open file object
    key         index into row of column to extract and convert
    conversion  function used to convert 'key' value in each row

    Returns a SciPy array of column values for the column.
    """

    reader = csv.DictReader(f)
    return scipy.array([conversion(row[key].strip(' ')) for row in reader])
        

def csv2dict(file_name, title_check_list=None, convert=None, delimiter=','):
    """Load a csv file into a Python dictionary.
    
    file_name         path to data file, or already open file object
    title_check_list  list of titles that *must* be columns in the file
    convert           a dictionary with titles as keys, values are functions to
                      convert the data from string to the correct type
    delimiter         the CSV delimiter to use
        
    Returns two dicts: ({header:column}, {header:column index}).
    The column is a list of the values.  The second dict is to keep track of
    the column order.

    Values are returned as strings, unless convert is used.
    """

    attribute_dic = {}
    title_index_dic = {}
    titles_stripped = []		# List of titles (stripped)

    # ensure we have an open file object
    if isinstance(file_name, file):
        file_handle = file_name
    else:
        file_handle = open(file_name,"rb")
        
    reader = csv.reader(file_handle, delimiter=delimiter)

    # Read in and manipulate the title info
    titles = reader.next()
    for (i, title) in enumerate(titles):
        header = title.strip()
        titles_stripped.append(header)
        title_index_dic[header] = i
    title_count = len(titles_stripped)

    # Check required columns
    if title_check_list:
        for title_check in title_check_list:
            if not title_index_dic.has_key(title_check):
                msg = ('Reading error. This column is not present %s'
                       % title_check)
                file_handle.close()
                raise IOError(msg)

    # Create a dictionary of column values, indexed by column title
    for line in reader:
        n = len(line) # Number of entries
        if n != title_count:
            msg = 'Entry in file %s had %d columns ' % (file_name, n)
            msg += 'although there were %d headers' % title_count
            raise IOError, msg
        for i, value in enumerate(line):
            attribute_dic.setdefault(titles_stripped[i], []).append(value)
            
    file_handle.close()

    if convert:
        for (key, value) in attribute_dic.items():
            if convert.has_key(key):
                attribute_dic[key] = [convert[key](x) for x in value]
    
    return (attribute_dic, title_index_dic)


def csv2rowdict(filename, columns=None, convert=None, delimiter=','):
    """Read a CSV file into a row-oriented dictionary.

    filename   pathname for the file, or a file object for an already open file
    columns    optional list of column headers to include in the result
    convert    optional dictionary to convert column values
    delimiter  CSV field delimiter

    Returns a dictionary of {'key': <row>, ...}.  The 'key' is the first column
    in 'columns'.  The <row> data is a list of other columns in the specified
    order.

    If 'columns' is specified, those columns *must* exist and will be placed
    in the <row> value lists in the specified order.  If there is no column
    with a required title then IOError exception is thrown.

    If 'convert' is specified, then any column matching a key in 'convert'
    is converted according to the expression in the key value.
    """

    # handle the file name or object parameter
    filehandle = filename   # assume file already open
    if not isinstance(filename, file):
        # if not, open it
        filehandle = open(filename, 'rb')

    # open CSV file
    reader = csv.reader(filehandle, delimiter=delimiter)

    # Read in and manipulate the title info - strip, etc
    headers = reader.next()
    headers = map(string.strip, headers)

    # if 'columns' not specified accept all columns
    if columns is None:
        columns = headers

    # check required column titles exist
    for col in columns:
        if col not in headers:
            filehandle.close()
            msg = "Required column '%s' doesn't exist in CSV file" % col
            raise IOError(msg)

    # check convert columns exist in required columns
    if convert is not None:
        for col in convert:
            if col not in columns:
                filehandle.close()
                msg = "Convert column '%s' doesn't exist in CSV file" % col
                raise IOError(msg)

    # convert list of column titles to column indices
    column_indices = []
    for col in columns:
        column_indices.append(headers.index(col))

    # also convert the convert dict to column *indices*
    convert_indices = {}
    if convert is not None:
        for (col, val) in convert.iteritems():
            convert_indices[headers.index(col)] = val

    # now read data rows and manipulate columns - first column is dict key
    result = {}
    num_headers = len(headers)
    for (line_num, line) in enumerate(reader):
        if len(line) != num_headers:
            filehandle.close()
            msg = ("Line %d has %d columns, expected %d"
                   % (line_num+2, len(line), num_headers))
            raise IOError(msg)

        # put row results into dictionary
        row = []
        for i in column_indices[1:]:
            convert_op = convert_indices.get(i, str)
            row.append(convert_op(line[i]))
        result[line[column_indices[0]]] = row

    return result


