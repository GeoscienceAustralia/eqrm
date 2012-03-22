    
    
#-------------------------------------------------------------
    
if __name__ == "__main__":
    #import os    
    #os.chdir('..')
    import sys
    from eqrm_code.check_scenarios import check_scenarios_main, \
                      LONG_SCENARIO_DIR, LONG_STANDARD_DIR, LONG_CURRENT_DIR, \
                      LONG_STANDARD_STRING, LONG_CURRENT_STRING
 
    c_failed_missing_file = check_scenarios_main(
        scenario_dir=LONG_SCENARIO_DIR,
        standard_dir=LONG_STANDARD_DIR,
        standard_string=LONG_STANDARD_STRING,
        current_dir=LONG_CURRENT_DIR,
        current_string=LONG_CURRENT_STRING)
    sys.exit(c_failed_missing_file) 
