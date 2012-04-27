import os
import sys
import unittest

'''

'''

class Test_eqrm_audit_wrapper(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    

#-------------------------------------------------------------
if __name__ == "__main__":
    suite = unittest.makeSuite(Test_eqrm_audit_wrapper,'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
