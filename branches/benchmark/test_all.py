"""
Execute all of the unit tests
"""

import os, socket
from optparse import OptionParser

from eqrm_code.get_version import get_version

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
    parser = OptionParser()
    parser.add_option('-b', '--bench', dest='benchmark', 
                                       action='store_true',
                                       help='Benchmark test suite')
    parser.add_option('-d', '--dir',   dest='dir', 
                                       default='.',
                                       help='Save directory for benchmark tests. Default: ./')
    options, args = parser.parse_args()
    
    is_eqrm_code_module_accessable()
    
    if options.benchmark:
        try:
            from bench import benchmarker
            
            version, _, _ = get_version(quiet=True)
            benchmarker.set_version_tag(version)
            
            benchmarker.set_archiving(options.dir,
                                      'EQRM_benchmark',
                                      socket.gethostname(),
                                      'test_all')

            benchmarker.restart_recording()
        
            test_all_main()
            
            benchmarker.stop_recording()
            print "Benchmark statistics stored in %s" % benchmarker.LOGFILE_NAME
            benchmarker.export_csv_performance_report('%s.csv' % benchmarker.LOGFILE_NAME)
            print "Exported to %s.csv" % benchmarker.LOGFILE_NAME
            
        except ImportError:
            print "benchmarker.py not available. Not benchmarking."
            test_all_main()
        except Exception:
            import traceback
            traceback.print_exc()
    
    else:
        test_all_main()
    
    
