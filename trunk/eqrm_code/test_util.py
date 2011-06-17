#!/usr/bin/env python

import os
import unittest
import shutil

from eqrm_code.util import *


class Dummy:
    def __init__(self):
        pass

class Test_Util(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_determine_eqrm_path(self):
        # WARNING - just runs the model, does not check the results,
        # since the results are based on where EQRM is installed.
        determine_eqrm_path()
        # determine_eqrm_path is used in the test below though.
        
    def test_get_local_or_default(self):
        eqrm_dir = determine_eqrm_path()
        input_dir =  os.path.join(eqrm_dir, 'eqrm_code')
        default_input_dir = os.path.join(eqrm_dir, 'resources', 'data', '')
        file_name = 'building_parameters_hazus_params.csv'
        fid = get_local_or_default(file_name, default_input_dir, input_dir)

        # This will fail if the start of building_parameters_hazus_params.csv
        # changes, or if the file is removed.
        self.failUnless(fid.read(9) == 'structure')

    def test_WeaveIOError(self):
        try:
            raise WeaveIOError
        except IOError:
            pass
        else:
            self.fail("Error not thrown")

    def test_add_directories(self):
        import tempfile

        # get a temporary directory
        root_dir = tempfile.mkdtemp('_test_util', 'test_util_')

        directories = ['ja', 'ne', 'ke']

        kens_dir = add_directories(root_dir, directories)
        assert kens_dir == os.path.join(root_dir, os.sep.join(directories))
        assert access(root_dir, F_OK)

        # do again, make sure there is no error due to 'already exists'
        kens_dir = add_directories(root_dir, directories)
        assert kens_dir == os.path.join(root_dir, os.sep.join(directories))
        assert access(root_dir, F_OK)
        
        # clean up!
        shutil.rmtree(root_dir)

    def test_add_directories_bad(self):
        
        import tempfile
        root_dir = tempfile.mkdtemp('_test_util', 'test_util_')
        directories = ['/\/!@#@#$%^%&*((*:*:','ne','ke']
        
        try:
            kens_dir = add_directories(root_dir, directories)
        except OSError:
            pass
        else:
            msg = 'bad dir name should give OSError'
            raise Exception(msg)    
            
        #clean up!
        os.rmdir(root_dir)       

    def test_find_bridge_sa(self):
        """Test the find_bridge_sa() function."""

        # OK find, finds both, precise values
        SA = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
        expect = (3, 10)
        got = find_bridge_sa_indices(SA)
        self.failUnlessEqual(expect, got)

        # OK find, finds both, imprecise values
        SA = [0.0, 0.1, 0.2, 0.31, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 1.1, 1.2]
        expect = (3, 10)
        got = find_bridge_sa_indices(SA, epsilon=0.02)
        self.failUnlessEqual(expect, got)

        # BAD find, doesn't find 0.3
        SA = [0.0, 0.1, 0.2, 0.301, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
        self.failUnlessRaises(RuntimeError, find_bridge_sa_indices, SA)

        # BAD find, doesn't find 1.0
        SA = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.999, 1.1, 1.2]
        self.failUnlessRaises(RuntimeError, find_bridge_sa_indices, SA)

    def dont_test_run_call(self):
        # Too flaky for a test.
        retcode = run_call('get_python_version.py', 'python')
        
    def test_string_convert(self):
        
        s = r'foo\bar'
        out = convert_path_string_to_join(s)
        self.failUnlessEqual(out, "join('foo', 'bar')")
        
        s = r'.\s\i/'
        out = convert_path_string_to_join(s)
        self.failUnlessEqual(out, "join('.', 's', 'i')")

        s = r'.\i\s'
        out = convert_path_string_to_join(s)
        self.failUnlessEqual(out, "join('.', 'i', 's')")
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Util,'test')
    #suite = unittest.makeSuite(Test_Util,'test_string_convert')
    runner = unittest.TextTestRunner() #verbosity=2)
    runner.run(suite)

