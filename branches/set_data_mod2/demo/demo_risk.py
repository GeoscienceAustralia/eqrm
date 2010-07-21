"""
 Title: demo risk
 
  Description: A demonstration scenario using the risk module.
 
  Version: $Revision: 901 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-03-27 17:16:42 +1100 (Fri, 27 Mar 2009) $
"""
from os.path import join
from eqrm_code.risk import risk_main

# The hazarad info is from create_par_file_simple in check_risk.
input_dir = join(".", "input")
site_file = join(input_dir, "structure_example.csv")
site_tag = "demo_risk"
risk_save_dir =  join(".", "output","demo_risk")
hazard_file_full_name = join(input_dir, "example_soil_SA.txt")
Mw = 7.6

# Note, a buildpars_flag of 'demo_risk' is passed to show how a
# new structural classification scheme can be used.
# The scheme is in .\input, it is called
# building_parameters_demo_risk_params.csv and it is
# only an example of using a differnet scheme, it is not a real scheme.

risk_main(site_file,
          site_tag,
          risk_save_dir,
          hazard_file_full_name=hazard_file_full_name,
          Mw=Mw,
          buildpars_flag='demo_risk',
          input_dir=input_dir)

