
import os


def is_eqrm_code_module_accessable():
    """
    test if the eqrm_code module is accessable
    """
    try:
        import eqrm_code
    except ImportError:
        for param in os.environ.keys():
            print "%20s %s" % (param, os.environ[param])
        print "'python_eqrm needs to be added to the PYTHONPATH"
        import eqrm_code


def test_all_main():
    # this has to be a python_eqrm dir really.
    # This is needed so tests that rely on data files work
    current_dir = os.getcwd()
    os.chdir('eqrm_code')

    # This works. 
    from eqrm_code.test_all import main
    main()
    os.chdir(current_dir)


#-------------------------------------------------------------
if __name__ == "__main__":
    is_eqrm_code_module_accessable()
    test_all_main()
    
