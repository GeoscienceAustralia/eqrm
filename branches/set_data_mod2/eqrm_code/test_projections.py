import os
import sys
import unittest


class Test_Projections(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_Projections,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
