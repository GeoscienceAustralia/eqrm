"""

Title: check_scenarios - Run the implementation scenarios then check
  the results in the current dir against the results in the standard
  directory.
  
  Author:  Duncan Gray, Duncan.gray@ga.gov.au 

  CreationDate:  2007-08-20 

  Description:
  
   This script checks if the results in the 'current' dir are
   different from the results in the 'standard' dir.

   The results in 'standard' dir represent the correct results.

  To suppress the running the implementation scenarios, do;
  python check_scenarios.py no_run OR
  python check_scenarios.py n

  The THE_PARAM_T.txt files are skipped.

  Timings are also measured and stored in scenario_performance.asc.

  To reset the standard timings, delete the file 
  python_eqrm\implementation_tests\timing\standard*.asc
  
  Version: $Revision: 997 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-07-01 14:14:06 +1000 (Wed, 01 Jul 2009) $


"""

#-------------------------------------------------------------
if __name__ == "__main__":
    from eqrm_code.check_scenarios import check_scenarios_main
    check_scenarios_main()
    
    
