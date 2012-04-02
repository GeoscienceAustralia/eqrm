import os
import sys
import string
import unittest
import tempfile
import scipy

import eqrm_code.csv_interface as csvi
import util


"""
Test CVS interface.

Note that the csv interface is a little more advanced than the functions
below - it is designed to not fall over from MemorErrors if a huge sites
file is sent (though it will be rather slow).
"""

class Test_Csv_Interface(unittest.TestCase):

    def setUp(self):
        # create test data structures
        self.LONGITUDE = [115, 116, 117, 118]
        self.LATITUDE = [-31, -32, -33, -34]
        self.WALLS = ['Brick veneer', 'Double Brick', 'Fibro', 'Double Brick']
        self.dummy_f = ['LONGITUDE,LATITUDE,WALLS',
                        '115,-31,Brick veneer',
                        '116,-32,Double Brick',
                        '117,-33,Fibro',
                        '118,-34,Double Brick']

    def test_quick_convert_csv_to_arrays(self):
        lon = csvi.quick_convert_csv_to_arrays(self.dummy_f, LONGITUDE=float)
        assert lon.keys()[0] == 'LONGITUDE'
        assert len(lon.keys()) == 1
        assert scipy.alltrue(self.LONGITUDE == lon['LONGITUDE'])
        
        all_conversions = {'LONGITUDE': float,
                           'LATITUDE': float,
                           'WALLS': str}

        all = csvi.quick_convert_csv_to_arrays(self.dummy_f, **all_conversions)
        assert len(all.keys()) == 3
        assert scipy.alltrue(self.LATITUDE == all['LATITUDE'])
        assert scipy.alltrue(self.LONGITUDE == all['LONGITUDE'])
        assert scipy.alltrue(self.WALLS == all['WALLS'])

    def test_quick_convert_csv_to_arrays_lats_longs(self):
        lon = csvi.quick_convert_csv_to_arrays(self.dummy_f, LONGITUDE=float)
        assert lon.keys()[0] == 'LONGITUDE'
        assert len(lon.keys()) == 1
        assert scipy.alltrue(self.LONGITUDE == lon['LONGITUDE'])
        
        all_conversions = {'LONGITUDE': float,
                           'LATITUDE': float,
                           'WALLS': str}

        all = csvi.quick_convert_csv_to_arrays(self.dummy_f, **all_conversions)
        assert len(all.keys()) == 3
        assert scipy.alltrue(self.LATITUDE == all['LATITUDE'])
        assert scipy.alltrue(self.LONGITUDE == all['LONGITUDE'])
        assert scipy.alltrue(self.WALLS == all['WALLS'])
       
    def unnfinished_test_quick_convert_csv_to_arrays_lats_longs_file(self):
        (handle, file_name) = tempfile.mkstemp('.csv', 'test_csv_interface_')
        os.close(handle)
        
        LONGITUDE = [11.5, 11.6, 11.7, 11.8]
        LATITUDE = [-3.1, -3.2, -3.3, -3.4]
        WALLS = ['Brick veneer', 'Double Brick', 'Fibro', 'Double Brick']
        
        attribute_dic = {'LONGITUDE': LONGITUDE,
                         'LATITUDE': LATITUDE,
                         'WALLS': WALLS}
        title_index_dic = {'LONGITUDE': 0,
                           'LATITUDE': 1,
                           'WALLS': 2}
        util.dict2csv(file_name, title_index_dic, attribute_dic)
        print "file_name", file_name
        lon = csvi.quick_convert_csv_to_arrays(file_name, LONGITUDE=float)
        assert lon.keys()[0] == 'LONGITUDE'
        assert len(lon.keys()) == 1
        assert scipy.allclose(LONGITUDE, lon['LONGITUDE'])
        
        all_conversions = {'LONGITUDE': float,
                           'LATITUDE': float,
                           'WALLS': str}

        all = csvi.quick_convert_csv_to_arrays(self.dummy_f, **all_conversions)
        assert len(all.keys()) == 3
        assert scipy.allclose(LATITUDE, all['LATITUDE'])
        assert scipy.allclose(LONGITUDE, all['LONGITUDE'])
        assert scipy.allclose(self.WALLS == all['WALLS'])

        os.remove(file_name)
        
    def test_csv_to_arrays(self):
        (handle, file_name) = tempfile.mkstemp('.csv', 'test_csv_interface_')
        os.close(handle)

        f = open(file_name,"wb")
        f.write('\n'.join(self.dummy_f))
        f.close()
        
        lon = csvi.csv_to_arrays(file_name, LONGITUDE=float)
        assert lon.keys()[0] == 'LONGITUDE'
        assert len(lon.keys()) == 1
        assert scipy.alltrue(self.LONGITUDE == lon['LONGITUDE'])

        all_conversions = {'LONGITUDE': float,
                           'LATITUDE': float,
                           'WALLS': str}

        all = csvi.csv_to_arrays(file_name, **all_conversions)
        assert len(all.keys()) == 3
        assert scipy.alltrue(self.LATITUDE == all['LATITUDE'])
        assert scipy.alltrue(self.LONGITUDE == all['LONGITUDE'])
        assert scipy.alltrue(self.WALLS == all['WALLS'])

        os.remove(file_name)
            
    def test_csv_to_array(self):
        lat = csvi.csv_to_array(self.dummy_f, 'LATITUDE', float)        
        lon = csvi.csv_to_array(self.dummy_f, 'LONGITUDE', float)        
        wal = csvi.csv_to_array(self.dummy_f, 'WALLS', str)
        
        assert scipy.alltrue(self.LATITUDE == lat)
        assert scipy.alltrue(self.LONGITUDE == lon)
        assert scipy.alltrue(self.WALLS == wal)

    def test_dict2csv(self):
        (handle, file_name) = tempfile.mkstemp('.csv', 'test_csv_interface_')
        os.close(handle)
        
        attribute_dic = {'LONGITUDE': self.LONGITUDE,
                         'LATITUDE': self.LATITUDE,
                         'WALLS': self.WALLS}
        title_index_dic = {'LONGITUDE': 0,
                           'LATITUDE': 1,
                           'WALLS': 2}

        util.dict2csv(file_name, title_index_dic, attribute_dic)

        (attribute_dic_new, title_index_dic_new) = \
            csvi.csv2dict(file_name, title_check_list=title_index_dic)
        attribute_dic_new['LONGITUDE'] = \
            [float(x) for x in attribute_dic_new['LONGITUDE']]
        attribute_dic_new['LATITUDE'] = \
            [float(x) for x in attribute_dic_new['LATITUDE']]

        self.assert_(attribute_dic_new == attribute_dic)
        self.assert_(title_index_dic_new == title_index_dic_new)
        
        os.remove(file_name)

    def test_dict2csv_bad(self):
        (handle, file_name) = tempfile.mkstemp('.csv', 'test_csv_interface_')
        os.close(handle)
        
        attribute_dic = {'LONGITUDE': self.LONGITUDE,
                         'LATITUDE': self.LATITUDE,
                         'WALLS': self.WALLS}
        title_index_dic = {'LONGITUDE': 0,
                           'LATITUDE': 1,
                           'WALLS': 2}
        util.dict2csv(file_name, title_index_dic, attribute_dic)

        try:
            attribute_dic_new, title_index_dic_new = \
                csvi.csv2dict(file_name, title_check_list={'wire': 8})
        except IOError:
            os.remove(file_name)
        else:
            os.remove(file_name)
            self.failUnless(False, "Error not thrown")

    def test_dict2csv_convert(self):
        (handle, file_name) = tempfile.mkstemp('.csv', 'test_csv_interface_')
        os.close(handle)
        
        attribute_dic = {'LONGITUDE': self.LONGITUDE,
                         'LATITUDE': self.LATITUDE,
                         'WALLS': self.WALLS}
        # This is actually assumed to be a list in the code...
        title_index_dic = {'LONGITUDE': 0,
                           'LATITUDE': 1,
                           'WALLS': 2}
        convert = {'LONGITUDE': float,
                   'LATITUDE': float,
                   'WALLS' :str}
        util.dict2csv(file_name, title_index_dic, attribute_dic)

        attribute_dic_new, title_index_dic_new = \
            csvi.csv2dict(file_name, title_check_list=title_index_dic,
                          convert=convert)
        self.assert_(attribute_dic_new['LONGITUDE'] == self.LONGITUDE)
        self.assert_(attribute_dic_new['LATITUDE'] == self.LATITUDE)
        self.assert_(attribute_dic_new['WALLS'] == self.WALLS)
        self.assert_(attribute_dic_new == attribute_dic)
        self.assert_(title_index_dic_new == title_index_dic_new)
        
        os.remove(file_name)

    def test_csv2rowdict(self):
        (handle, filename) = tempfile.mkstemp('.csv', 'test_csv_interface_')
        os.close(handle)

        # create test file with known data
        f = open(filename, 'w')
        f.write('A,B,C,D\n')
        f.write('row1,1,1.0,one\n')
        f.write('row2,2,2.0,two\n')
        f.write('row3,3,3.0,three\n')
        f.write('row4,4,4.0,four\n')
        f.write('row5,5,5.0,five\n')
        f.close()

        # simple smoke test - get all columns as strings
        expected = {'row1': ['1', '1.0', 'one'],
                    'row2': ['2', '2.0', 'two'],
                    'row3': ['3', '3.0', 'three'],
                    'row4': ['4', '4.0', 'four'],
                    'row5': ['5', '5.0', 'five']}
        d = csvi.csv2rowdict(filename)
        self.failUnlessEqual(d, expected)

        # now see if we can select columns A, D and B (in that order)
        expected = {'row1': ['one', '1'],
                    'row2': ['two', '2'],
                    'row3': ['three', '3'],
                    'row4': ['four', '4'],
                    'row5': ['five', '5']}
        d =  csvi.csv2rowdict(filename, columns=['A','D','B'])
        self.failUnlessEqual(d, expected)

        # try changing the key column to column B
        expected = {'1': ['row1', 'one'],
                    '2': ['row2', 'two'],
                    '3': ['row3', 'three'],
                    '4': ['row4', 'four'],
                    '5': ['row5', 'five']}
        d =  csvi.csv2rowdict(filename, columns=['B','A','D'])
        self.failUnlessEqual(d, expected)

        # repeat above test, converting col B into int
        expected = {'row1': ['one', 1],
                    'row2': ['two', 2],
                    'row3': ['three', 3],
                    'row4': ['four', 4],
                    'row5': ['five', 5]}
        d = csvi.csv2rowdict(filename, columns=['A','D','B'],
                             convert={'B': int})
        self.failUnlessEqual(d, expected)

        # get all columns, reorder and convert int and float
        expected = {'row1': ['one', 1.0, 1],
                    'row2': ['two', 2.0, 2],
                    'row3': ['three', 3.0, 3],
                    'row4': ['four', 4.0, 4],
                    'row5': ['five', 5.0, 5]}
        d =  csvi.csv2rowdict(filename, columns=['A','D','C','B'],
                              convert={'B':int, 'C':float})
        self.failUnlessEqual(d, expected)

        # now see if we get expected errors - missing required column
        self.failUnlessRaises(IOError, csvi.csv2rowdict, filename,
                              columns=['A','D','Q'])

        # now see if we get expected errors - missing convert column
        self.failUnlessRaises(IOError, csvi.csv2rowdict, filename,
                              columns=['A','D','B'],
                              convert={'Q':int})

        # now see if we get expected errors - file not found
        self.failUnlessRaises(IOError, csvi.csv2rowdict, 'xyzzy_42_xyzzy')

        os.remove(filename)

################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Csv_Interface,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
