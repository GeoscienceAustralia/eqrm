import os
import sys
import unittest
import tempfile
import shutil

from multiple_runs import *

class Test_multiple_runs(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_sites_list(self):
        input_tups = [(3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,290)]
        for tup in input_tups:
            site_indexs = create_sites_list(*tup)
            self.assertEqual(len(site_indexs), tup[1])
            self.assertTrue(max(site_indexs) <= tup[0])
            self.assertEqual(min(site_indexs), 1)
            
            
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_multiple_runs, 'test')
    runner = unittest.TextTestRunner() #verbosity=2) 
    runner.run(suite)

