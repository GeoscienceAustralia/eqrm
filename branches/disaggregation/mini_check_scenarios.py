"""

Title: mini_check_scenarios - Run a sub set of the implementation
  scenarios then check the results in the current dir against the
  results in the standard directory.
  
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  CreationDate:  2007-08-20 

  Description:
  
   This script checks if the results in the 'mini_current' dir are
   different from the results in the 'mini_standard' dir.

   The results in 'mini_standard' dir represent the correct results.

  To suppress the running the implementation scenarios, do;
  python mini_check_scenarios.py no_run OR
  python mini_check_scenarios.py n


  Timings are also measured and stored in scenario_performance.asc.

  To reset the standard timings, delete the file 
  python_eqrm\implementation_tests\timing\mini_standard*.asc
  
  Version: $Revision: 632 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2008-06-18 11:42:19 +1000 (Wed, 18 Jun 2008) $


"""

#-------------------------------------------------------------
if __name__ == "__main__":
    from eqrm_code import check_scenarios
    import sys

    c_failed_missing_file = check_scenarios.mini_check_scenarios_main()
    sys.exit(c_failed_missing_file) 
