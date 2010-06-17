"""
 Title: demo risk
 
  Description: A demonstration scenario using the risk module.
 
  Version: $Revision: 901 $  
  ModifiedBy: $Author: dgray $
  ModifiedDate: $Date: 2009-03-27 17:16:42 +1100 (Fri, 27 Mar 2009) $
"""
from os.path import join
from eqrm_code.risk import multi_risk

# The hazarad info is from create_par_file_simple in check_risk.
input_dir = join(".", "input")
site_file = join(input_dir, "multi_risk_site_db.csv")
site_tag = "newc"
risk_save_dir =  join(".", "output","demo_multi_risk")
Mw_file = join(input_dir, "newc_Mw.txt")

# The hazard files must be in the hazard_saved_dir.
# the hazard file format is [site_tag]_hazard_ev[event_id].txt

#  The event_id must be 0, 1, 2 etc, corresponding to the rows in the
#  earthquake magnitude file. Each row in the earthquake magnitude file
#  is the magnitude(Mw) of the earthquake.

# The results are in folders in risk_save_dir.  The names of the folders
# are  0, 1, 2 etc, corresponding to the rows in the earthquake magnitude file.

multi_risk(site_file,
           site_tag,
           risk_save_dir,
           Mw_file,
           buildpars_flag='workshop_3',
           hazard_saved_dir=input_dir,
           input_dir=input_dir)
