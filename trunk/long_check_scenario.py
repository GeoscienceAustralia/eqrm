    
    
#-------------------------------------------------------------
    
if __name__ == "__main__":
    #import os    
    #os.chdir('..')
    from os.path import join
    import sys
    
    from eqrm_code import util
    from eqrm_code.check_scenarios import check_scenarios_main
    
    eqrm_path = util.determine_eqrm_path()
    
    IMP_DIR = join(eqrm_path,'implementation_tests')
    SCENARIO_DIR = join(IMP_DIR, 'long_scenarios')
    
    STANDARD_DIR = join(IMP_DIR, 'long_standard')
    CURRENT_DIR = join(IMP_DIR, 'long_current')
    STANDARD_STRING = "long_standard_timings_"
    CURRENT_STRING = "long_current_timings_"
    
    c_failed_missing_file = check_scenarios_main(
        scenario_dir=SCENARIO_DIR,
        standard_dir=STANDARD_DIR,
        standard_string=STANDARD_STRING,
        current_dir=CURRENT_DIR,
        current_string=CURRENT_STRING)
    sys.exit(c_failed_missing_file) 
