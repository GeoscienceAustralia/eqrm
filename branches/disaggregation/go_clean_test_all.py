"""
Remove compiled files and run test_all
"""

import test_all
from eqrm_code import clean_all


#-------------------------------------------------------------
if __name__ == "__main__":
    clean_all.clean_all_main(verbose=False, prompt=False)
    test_all.is_eqrm_code_module_accessable()
    test_all.test_all_main()
