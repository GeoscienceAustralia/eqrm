    
    
#-------------------------------------------------------------
    
if __name__ == "__main__":
    #import os    
    #os.chdir('..')
    import sys
    from optparse import OptionParser
    from eqrm_code.check_scenarios import check_scenarios_main, \
                      LONG_SCENARIO_DIR, LONG_STANDARD_DIR, LONG_CURRENT_DIR, \
                      LONG_STANDARD_STRING, LONG_CURRENT_STRING
    from eqrm_code import file_store
    
    parser = OptionParser()
    parser.add_option('-f', '--file_array', 
                      dest='file_array',
                      action='store_true',
                      help='Turn on file based arrays. Note that the default is on for EQRM.')
    options, args = parser.parse_args()
    if not options.file_array:
        file_store.SAVE_METHOD = None
 
    c_failed_missing_file = check_scenarios_main(
        scenario_dir=LONG_SCENARIO_DIR,
        standard_dir=LONG_STANDARD_DIR,
        standard_string=LONG_STANDARD_STRING,
        current_dir=LONG_CURRENT_DIR,
        current_string=LONG_CURRENT_STRING)
    sys.exit(c_failed_missing_file) 
